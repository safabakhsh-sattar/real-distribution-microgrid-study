"""Script 14: Volt-VAr over one year at the far bus of each feeder (Study 2c).

Question
  With the Volt-VAr curve active in every step of the year, how much reactive
  energy does the PV inverter exchange, how many hours do the voltage and the
  thermal limits stay violated, and how do the losses change? The three sizes
  are those of Table 12 (snapshot capacity, time-series capacity and 1.5 times
  the larger), so the results compare directly with the Volt-Watt analysis.

Method
  Networks, profiles, limits and the added PV follow script 12, which is
  imported (not copied). Every step of the year is simulated, night included:
  the inverter keeps its Volt-VAr function at zero active power. Reactive power
  is Q = ratio(V) x nameplate size (kVA), with the IEEE 1547 default curve of
  script 11, iterated to 0.1 kvar in the same way as script 11.

  Two shortcuts. Both give the same numbers as the full iteration (checked by
  --selftest):
    1. Dead band: if the bus voltage without Volt-VAr lies in [0.98, 1.02] pu,
       the curve gives Q = 0, so the Volt-VAr result equals the no-control result.
    2. No PV output: at a step with zero PV output the state is the same for
       every size, so it is solved once per step and reused.

  Metrics, weighted by the step length dt:
    E_avail      available PV energy (kWh). Volt-VAr does not curtail: delivered = available.
    Q_supplied   reactive energy supplied, Q > 0 (kvarh); Q_absorbed, Q < 0 (kvarh).
    hours        hours with a violated limit, without control and with Volt-VAr.
                 A step counts only where the limit holds without the added PV.
    dLoss        change of network losses against the case without the added PV (kWh).

  Time resolution: 'quarter' (35,136 steps, default) or 'hour' (hourly means,
  as in Table 12; about four times faster, same resolution as the Volt-Watt pass).

Run from the repository root:
  python scripts/14_vvar_annual.py --workers 3
  python scripts/14_vvar_annual.py --step hour --workers 3 --out vvar_annual_hour
  python scripts/14_vvar_annual.py --selftest --sample 200 --grids rural1
Outputs: results/vvar_annual.csv (or --out NAME), results/vvar_annual_summary.md
"""
import argparse
import importlib.util
import multiprocessing
import os
import time
import warnings

import numpy as np
import pandas as pd
import pandapower as pp

warnings.filterwarnings("ignore")

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)


def _load(name, file):
    spec = importlib.util.spec_from_file_location(name, os.path.join(HERE, file))
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


ts = _load("ts12", "12_timeseries.py")                 # Data, Case, pick_buses, limits
s11 = _load("s11", "11_multi_feeder_snapshot.py")      # vvar_q_ratio, IEEE 1547 default curve

DB_LOW, DB_HIGH = 0.98, 1.02                           # dead band of the curve (Q = 0)
GRIDS = ["rural1", "semiurb5", "urban6"]
FAR_BUS = {"rural1": 4, "semiurb5": 51, "urban6": 17}  # far buses of script 12 (Table 12)
TOL_TEST = 1e-9


def in_deadband(v):
    return DB_LOW <= v <= DB_HIGH


def vvar_iterate(case, size_kw, v_first):
    """Volt-VAr fixed point, same steps as script 11 solve().

    The net must hold P = the PV output and Q = 0. v_first is the bus voltage at
    Q = 0 (already solved); if None, the first power flow is run here (self-test).
    Returns (Q in kvar, number of power flows)."""
    net, idx, bus = case.net, case.idx, case.bus
    q_prev, v, n_pf = 0.0, v_first, 0
    for k in range(20):
        if k > 0 or v_first is None:
            pp.runpp(net)
            n_pf += 1
            v = net.res_bus.vm_pu.at[bus]
        q = s11.vvar_q_ratio(v) * size_kw
        net.sgen.at[idx, "q_mvar"] = q / 1000
        if abs(q - q_prev) < 0.1:
            break
        q_prev = q
    else:
        raise RuntimeError("Volt-VAr did not converge")
    pp.runpp(net)
    n_pf += 1
    return q, n_pf


def _state(case):
    net = case.net
    return dict(v=float(net.res_bus.vm_pu.at[case.bus]),
                loss=case.losses_kw(), flags=case.flags())


def simulate_step(case, t, hourly, sizes, dt, full=False):
    """Run step t for the base case (no added PV) and for each size.
    full=True switches the shortcuts off (self-test only)."""
    D, net, idx = case.D, case.net, case.idx
    f_t = float(D.h_f[t] if hourly else D.f[t])
    case.set_state(t, hourly)
    net.sgen.at[idx, "p_mw"] = 0.0
    net.sgen.at[idx, "q_mvar"] = 0.0
    pp.runpp(net)
    base = _state(case)
    out = {}
    for label, size in sizes:
        p = size * f_t
        net.sgen.at[idx, "p_mw"] = p / 1000          # reset P and Q for this size
        net.sgen.at[idx, "q_mvar"] = 0.0
        n_pf = 0
        if full or f_t > 0:
            pp.runpp(net)
            n_pf += 1
            nc = _state(case)
        else:
            nc = base                                  # zero PV: same state as the base case
        if not full and in_deadband(nc["v"]):
            q, shortcut, vv = 0.0, True, nc            # Q = 0: Volt-VAr equals no control
        else:
            q, n = vvar_iterate(case, size, None if full else nc["v"])
            n_pf += n
            vv, shortcut = _state(case), False
        out[label] = dict(p=p, q=q, nc=nc, vv=vv, n_pf=n_pf, shortcut=shortcut)
    return base, out


def setup(grid, step):
    code = f"1-LV-{grid}--0-sw"
    D = ts.Data(code)
    far = ts.pick_buses(D.net)[-1][0]
    if far != FAR_BUS[grid]:
        raise RuntimeError(f"{grid}: far bus is {far}, expected {FAR_BUS[grid]}")
    hc = pd.read_csv(os.path.join(ROOT, "results", "timeseries_hc.csv"))
    row = hc[(hc.code == code) & (hc.bus == far)].iloc[0]
    s_snap, s_ts = float(row.hc_snapshot), float(row.hc_ts)
    big = round(1.5 * max(s_snap, s_ts), 1)            # same rule as Table 12
    sizes = [("snapshot capacity", s_snap), ("time-series capacity", s_ts),
             ("1.5 x larger capacity", big)]
    hourly = step == "hour"
    dt = 1.0 if hourly else 0.25
    T = len(D.h_f) if hourly else len(D.f)
    return code, D, far, sizes, hourly, dt, T


def run_feeder(job):
    grid, a = job
    t0 = time.time()
    code, D, far, sizes, hourly, dt, T = setup(grid, a["step"])
    case = ts.Case(D, far)
    f_arr = D.h_f if hourly else D.f
    acc = {label: dict(size_kw=size, E=0.0, Qs=0.0, Qa=0.0, vh_nc=0.0, th_nc=0.0,
                       dL_nc=0.0, vh_vv=0.0, th_vv=0.0, dL_vv=0.0, shortcuts=0)
           for label, size in sizes}
    cnt = dict(steps=T, day_steps=int(np.sum(f_arr > 0)), power_flows=0, failed=[])
    for t in range(T):
        try:
            base, out = simulate_step(case, t, hourly, sizes, dt)
        except Exception as exc:                       # reported in the summary, must be 0
            cnt["failed"].append((t, str(exc)[:60]))
            continue
        cnt["power_flows"] += 1 + sum(o["n_pf"] for o in out.values())
        for label, _ in sizes:
            o, r = out[label], acc[label]
            nc, vv = o["nc"], o["vv"]
            r["E"] += o["p"] * dt
            r["Qs"] += max(o["q"], 0.0) * dt
            r["Qa"] += max(-o["q"], 0.0) * dt
            r["vh_nc"] += dt * (nc["flags"][0] and not base["flags"][0])
            r["th_nc"] += dt * (nc["flags"][1] and not base["flags"][1])
            r["vh_vv"] += dt * (vv["flags"][0] and not base["flags"][0])
            r["th_vv"] += dt * (vv["flags"][1] and not base["flags"][1])
            r["dL_nc"] += (nc["loss"] - base["loss"]) * dt
            r["dL_vv"] += (vv["loss"] - base["loss"]) * dt
            r["shortcuts"] += int(o["shortcut"])
    rows = []
    for label, size in sizes:
        r = acc[label]
        rows.append({
            "code": code, "bus": far, "step": a["step"], "size_label": label,
            "size_kW": size,
            "E_avail_MWh": round(r["E"] / 1000, 2),
            "Q_supplied_kvarh": round(r["Qs"], 1),
            "Q_absorbed_kvarh": round(r["Qa"], 1),
            "hours_volt_nc": round(r["vh_nc"], 2), "hours_therm_nc": round(r["th_nc"], 2),
            "hours_volt_vvar": round(r["vh_vv"], 2), "hours_therm_vvar": round(r["th_vv"], 2),
            "dLoss_nc_kWh": round(r["dL_nc"], 1), "dLoss_vvar_kWh": round(r["dL_vv"], 1),
            "deadband_steps": r["shortcuts"],
        })
    return grid, rows, cnt, round(time.time() - t0, 1)


def selftest(grid, n, step):
    """Shortcuts against the full iteration on a random sample of steps."""
    code, D, far, sizes, hourly, dt, T = setup(grid, step)
    case = ts.Case(D, far)
    steps = np.random.default_rng(0).choice(T, size=min(n, T), replace=False)
    worst = dict(q=0.0, loss=0.0, v=0.0)
    bad, n_short = [], 0
    for t in steps:
        t = int(t)
        _, fast = simulate_step(case, t, hourly, sizes, dt)
        _, full = simulate_step(case, t, hourly, sizes, dt, full=True)
        for label, _ in sizes:
            f, g = fast[label], full[label]
            n_short += int(f["shortcut"])
            diffs = dict(q=abs(f["q"] - g["q"]),
                         loss=abs(f["vv"]["loss"] - g["vv"]["loss"]),
                         v=abs(f["vv"]["v"] - g["vv"]["v"]))
            for k in worst:
                worst[k] = max(worst[k], diffs[k])
            same_flags = (f["vv"]["flags"] == g["vv"]["flags"] and
                          f["nc"]["flags"] == g["nc"]["flags"])
            if not same_flags or any(d > TOL_TEST for d in diffs.values()):
                bad.append((t, label))
    return (f"{grid}: {len(steps)} steps x {len(sizes)} sizes; shortcut used {n_short} times; "
            f"mismatches {len(bad)}; largest differences Q {worst['q']:.2e} kvar, "
            f"loss {worst['loss']:.2e} kW, V {worst['v']:.2e} pu")


def md_table(df):
    cols = list(df.columns)
    lines = ["| " + " | ".join(cols) + " |", "|" + "---|" * len(cols)]
    for _, r in df.iterrows():
        lines.append("| " + " | ".join(str(r[c]) for c in cols) + " |")
    return "\n".join(lines)


def write_summary(path, df, cnts, secs, step):
    n_fail = sum(len(c["failed"]) for c in cnts.values())
    lines = [
        "# Volt-VAr over one year, far bus of each feeder (script 14)", "",
        f"Time resolution: {step} ({'35,136 quarter-hour steps' if step == 'quarter' else '8,784 hourly means'}).",
        "Limits: 1.05 pu voltage, 100 % current-based loading. Volt-VAr: IEEE 1547 default curve, Q = ratio(V) x nameplate.",
        "", "## Results", "", md_table(df), "",
        "## Run checks", "",
        f"Failed steps (power flow did not converge): {n_fail}. This must be 0.", "",
    ]
    for g, c in cnts.items():
        lines.append(f"- {g}: steps {c['steps']}, daylight steps {c['day_steps']}, "
                     f"power flows {c['power_flows']}, time {secs[g]} s, "
                     f"failed {len(c['failed'])}")
    lines += ["", "Send this file back: " + path]
    with open(path, "w", encoding="utf-8") as fh:
        fh.write("\n".join(lines) + "\n")


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--grids", nargs="+", default=GRIDS, choices=GRIDS)
    ap.add_argument("--workers", type=int, default=1)
    ap.add_argument("--step", choices=["quarter", "hour"], default="quarter")
    ap.add_argument("--out", default="vvar_annual")
    ap.add_argument("--selftest", action="store_true")
    ap.add_argument("--sample", type=int, default=200)
    a = vars(ap.parse_args())

    if a["selftest"]:
        for g in a["grids"]:
            print(selftest(g, a["sample"], a["step"]), flush=True)
        return

    os.makedirs(os.path.join(ROOT, "results"), exist_ok=True)
    jobs = [(g, a) for g in a["grids"]]
    rows, cnts, secs = [], {}, {}
    t0 = time.time()

    def collect(res):
        grid, r, c, s = res
        rows.extend(r)
        cnts[grid], secs[grid] = c, s
        print(f"== {grid} finished in {s / 60:.1f} min, failed steps {len(c['failed'])}", flush=True)

    if a["workers"] > 1 and len(jobs) > 1:
        ctx = multiprocessing.get_context("spawn")
        with ctx.Pool(min(a["workers"], len(jobs))) as pool:
            for res in pool.imap_unordered(run_feeder, jobs):
                collect(res)
    else:
        for job in jobs:
            collect(run_feeder(job))

    df = pd.DataFrame(rows)
    p_csv = os.path.join(ROOT, "results", f"{a['out']}.csv")
    p_md = os.path.join(ROOT, "results", f"{a['out']}_summary.md")
    df.to_csv(p_csv, index=False, encoding="utf-8")
    write_summary(p_md, df, cnts, secs, a["step"])
    print(f"\nTotal time {(time.time() - t0) / 60:.1f} min")
    print(f"Send me this file: {p_md}")


if __name__ == "__main__":
    main()