"""Script 11: hosting capacity on several SimBench low-voltage feeders.

Question: on which feeders and buses does the default Volt-VAr curve raise,
keep or lower the hosting capacity of a PV unit, and does the answer depend on
which limit (voltage or thermal) binds first without control?

Hypothesis (to be tested here, NOT a result): Volt-VAr helps when the voltage
limit binds first, and does not help (or lowers the capacity) when a thermal
limit binds first.

For every load bus of every selected network, one PV unit is added at that bus
(voltage limit 1.05 pu, thermal limit 100 %, current-based loading, as in
scripts 08 to 10). Four hosting capacities (kW) are found by binary search:
  hc_v     no control, voltage limit only
  hc_t     no control, thermal limit only
  hc_nc    no control, both limits
  hc_vvar  default IEEE 1547-2018 Volt-VAr, both limits
and two more that split the Volt-VAr effect into its two parts:
  hc_v_vvar  Volt-VAr, voltage limit only   (the gain: reactive power lowers voltage)
  hc_t_vvar  Volt-VAr, thermal limit only   (the penalty: extra reactive current)
Then hc_vvar should equal min(hc_v_vvar, hc_t_vvar).
Derived columns:
  first_limit  voltage / thermal / both (|hc_v - hc_t| <= 0.2 kW)
  effect       higher / equal / lower (|hc_vvar - hc_nc| <= 0.2 kW counts as equal)
  thermal_element  trafo or line, the element that binds at hc_t
  v_pv_nc      voltage at the PV bus at hc_nc (no control)
  ratio_t_v    hc_t / hc_v, a screening indicator (above 1: voltage binds first)
  gain_pct     100 * (hc_v_vvar - hc_v) / hc_v
  penalty_pct  100 * (hc_t - hc_t_vvar) / hc_t

A network whose base case (no added PV) already violates a limit is skipped and
reported, because its hosting capacity would be zero everywhere.

Buses: all load buses of a small network; for a larger one, --per-grid buses
(default 20) chosen evenly along the electrical distance from the transformer,
so near and far buses are both included. Use --per-grid 0 for all buses (slow).

Run time: about one hour with one process (default settings); less with --workers.

Run from the repository root:
  python scripts/11_multi_feeder_snapshot.py                    (6 networks, scenario 0)
  python scripts/11_multi_feeder_snapshot.py --workers 4        (faster, uses 4 processes)
  python scripts/11_multi_feeder_snapshot.py --resume           (continue after an interruption)
  python scripts/11_multi_feeder_snapshot.py --summarize-only   (rebuild the summary from the saved CSV)
  python scripts/11_multi_feeder_snapshot.py --grids rural1 --per-grid 2 --out test   (quick test)
Outputs: results/multi_feeder_snapshot.csv and results/multi_feeder_summary.md
(with --out NAME the files are results/NAME_snapshot.csv and results/NAME_summary.md).
"""
import argparse
import copy
import multiprocessing
import os
import time
import warnings

import numpy as np
import pandapower as pp
import pandapower.topology as top
import pandas as pd
import simbench as sb

warnings.filterwarnings("ignore")

LOADING_LIMIT = 100.0
V_LIMIT = 1.05
MAX_KW = 2000.0
TOL_KW = 0.1
EQUAL_TOL_KW = 0.2
DEADBAND_UPPER = 1.02

GRIDS = ["rural1", "rural2", "rural3", "semiurb4", "semiurb5", "urban6"]


def sb_code(grid, scenario):
    return f"1-LV-{grid}--{scenario}-sw"


def vvar_q_ratio(v):
    V1, V2, V3, V4 = 0.92, 0.98, 1.02, 1.08
    if v <= V1:
        return 0.44
    if v <= V2:
        return 0.44 * (V2 - v) / (V2 - V1)
    if v <= V3:
        return 0.0
    if v <= V4:
        return -0.44 * (v - V3) / (V4 - V3)
    return -0.44


def limits_ok(net, check_v, check_t):
    if check_v and net.res_bus.vm_pu.max() > V_LIMIT:
        return False
    if check_t and (net.res_line.loading_percent.max() > LOADING_LIMIT or
                    net.res_trafo.loading_percent.max() > LOADING_LIMIT):
        return False
    return True


def solve(net, idx, bus, kw, control):
    """Set the PV output (and Volt-VAr reactive power) and run the power flow."""
    net.sgen.at[idx, "p_mw"] = kw / 1000
    net.sgen.at[idx, "q_mvar"] = 0.0
    if control == "none":
        pp.runpp(net)
        return
    q_prev = 0.0
    for _ in range(20):
        pp.runpp(net)
        q = vvar_q_ratio(net.res_bus.vm_pu.at[bus]) * kw
        net.sgen.at[idx, "q_mvar"] = q / 1000
        if abs(q - q_prev) < 0.1:
            break
        q_prev = q
    else:
        raise RuntimeError("Volt-VAr did not converge")
    pp.runpp(net)


def hosting_capacity(net, idx, bus, control, check_v, check_t):
    lo, hi = 0.0, MAX_KW
    while hi - lo > TOL_KW:
        mid = (lo + hi) / 2
        try:
            solve(net, idx, bus, mid, control)
            ok = limits_ok(net, check_v, check_t)
        except Exception:
            ok = False
        if ok:
            lo = mid
        else:
            hi = mid
    return round(lo, 1)


def hosting_capacity_near(net, idx, bus, control, check_v, check_t, guess):
    """Same boundary as hosting_capacity, but the search starts around a guess
    (fewer power flows). Used only for the two Volt-VAr split searches."""
    def feasible(kw):
        try:
            solve(net, idx, bus, kw, control)
            return limits_ok(net, check_v, check_t)
        except Exception:
            return False

    step = 1.3
    guess = min(max(guess, 1.0), MAX_KW)
    if feasible(guess):
        lo, hi = guess, guess * step
        while hi < MAX_KW and feasible(hi):
            lo, hi = hi, hi * step
        hi = min(hi, MAX_KW)
    else:
        hi, lo = guess, guess / step
        while lo > TOL_KW and not feasible(lo):
            hi, lo = lo, lo / step
        if lo <= TOL_KW:
            lo = 0.0
    while hi - lo > TOL_KW:
        mid = (lo + hi) / 2
        if feasible(mid):
            lo = mid
        else:
            hi = mid
    return round(lo, 1)


_NETS = {}


def get_base(code):
    if code not in _NETS:
        _NETS[code] = sb.get_simbench_net(code)
    return _NETS[code]


def pick_buses(net, k):
    """Load buses with their electrical distance (ohm) to the grid connection.
    If there are more than k, take k evenly spaced along that distance."""
    buses = sorted(int(b) for b in net.load.bus.unique())
    g = top.create_nxgraph(net, calc_branch_impedances=True, respect_switches=True)
    dist = top.calc_distance_to_bus(net, int(net.ext_grid.bus.iloc[0]), weight="weight", g=g)
    pairs = sorted(((float(dist.loc[b]), b) for b in buses))
    if k > 0 and len(pairs) > k:
        pairs = [pairs[i] for i in np.unique(np.linspace(0, len(pairs) - 1, k).round().astype(int))]
    return [(b, d) for d, b in pairs]


def analyse_bus(task):
    code, bus, dist = task
    net = copy.deepcopy(get_base(code))
    idx = pp.create_sgen(net, bus=bus, p_mw=0.0, q_mvar=0.0)

    hc_v = hosting_capacity(net, idx, bus, "none", True, False)
    hc_t = hosting_capacity(net, idx, bus, "none", False, True)
    hc_nc = hosting_capacity(net, idx, bus, "none", True, True)
    hc_vv = hosting_capacity(net, idx, bus, "vvar", True, True)
    hc_v_vv = hosting_capacity_near(net, idx, bus, "vvar", True, False, hc_v)
    hc_t_vv = hosting_capacity_near(net, idx, bus, "vvar", False, True, hc_t)

    solve(net, idx, bus, hc_t, "none")
    t_el = ("trafo" if net.res_trafo.loading_percent.max() >= net.res_line.loading_percent.max()
            else "line")
    solve(net, idx, bus, hc_nc, "none")
    v_pv = round(float(net.res_bus.vm_pu.at[bus]), 4)

    if abs(hc_v - hc_t) <= EQUAL_TOL_KW:
        first = "both"
    else:
        first = "voltage" if hc_v < hc_t else "thermal"
    delta = round(hc_vv - hc_nc, 1)
    if delta > EQUAL_TOL_KW:
        effect = "higher"
    elif delta < -EQUAL_TOL_KW:
        effect = "lower"
    else:
        effect = "equal"
    return {
        "code": code, "bus": int(bus), "z_ohm": round(dist, 4),
        "hc_v": hc_v, "hc_t": hc_t, "hc_nc": hc_nc, "hc_vvar": hc_vv,
        "hc_v_vvar": hc_v_vv, "hc_t_vvar": hc_t_vv,
        "delta_kW": delta,
        "delta_pct": round(100 * delta / hc_nc, 2) if hc_nc > 0 else float("nan"),
        "first_limit": first, "effect": effect, "thermal_element": t_el,
        "v_pv_nc": v_pv,
        "ratio_t_v": round(hc_t / hc_v, 3) if hc_v > 0 else float("nan"),
        "gain_pct": round(100 * (hc_v_vv - hc_v) / hc_v, 2) if hc_v > 0 else float("nan"),
        "penalty_pct": round(100 * (hc_t - hc_t_vv) / hc_t, 2) if hc_t > 0 else float("nan"),
        "vvar_is_min": abs(hc_vv - min(hc_v_vv, hc_t_vv)) <= EQUAL_TOL_KW,
        "nc_is_min": abs(hc_nc - min(hc_v, hc_t)) <= EQUAL_TOL_KW,
        "capped": max(hc_v, hc_t, hc_nc, hc_vv, hc_v_vv, hc_t_vv) >= MAX_KW - 0.5,
    }


def network_info(code):
    net = get_base(code)
    pp.runpp(net)
    v_max = float(net.res_bus.vm_pu.max())
    l_max = float(net.res_line.loading_percent.max())
    t_max = float(net.res_trafo.loading_percent.max())
    return {
        "code": code,
        "buses": len(net.bus),
        "trafo_kVA": round(float(net.trafo.sn_mva.sum()) * 1000),
        "load_kW": round(float(net.load.p_mw.sum()) * 1000, 1),
        "existing_pv_kW": round(float(net.sgen.p_mw.sum()) * 1000, 1),
        "load_buses": int(net.load.bus.nunique()),
        "base_v_max": round(v_max, 4),
        "base_line_%": round(l_max, 1),
        "base_trafo_%": round(t_max, 1),
        "base_ok": v_max <= V_LIMIT and l_max <= LOADING_LIMIT and t_max <= LOADING_LIMIT,
    }


def md_table(df):
    cols = list(df.columns)
    lines = ["| " + " | ".join(str(c) for c in cols) + " |",
             "|" + "---|" * len(cols)]
    for _, r in df.iterrows():
        lines.append("| " + " | ".join(str(r[c]) for c in cols) + " |")
    return "\n".join(lines)


def write_summary(path, info, df, seconds=None):
    out = ["# Multi-feeder snapshot results (script 11)", ""]
    out.append(f"Voltage limit {V_LIMIT} pu, thermal limit {LOADING_LIMIT:.0f} % (current-based), "
               f"search tolerance {TOL_KW} kW, ceiling {MAX_KW:.0f} kW. "
               f"'Equal' means within {EQUAL_TOL_KW} kW. "
               + (f"Run time {seconds / 60:.1f} min." if seconds is not None
                  else "Regenerated from the saved CSV."))
    out += ["", "## Networks", "", md_table(pd.DataFrame(info))]
    if df.empty:
        out += ["", "No network had a clean base case."]
        with open(path, "w", encoding="utf-8") as f:
            f.write("\n".join(out) + "\n")
        return

    rows = []
    for code, g in df.groupby("code"):
        eff = g.effect.value_counts()
        rows.append({
            "code": code, "buses": len(g),
            "hc_nc median": round(g.hc_nc.median(), 1),
            "hc_nc min-max": f"{g.hc_nc.min()}-{g.hc_nc.max()}",
            "hc_vvar median": round(g.hc_vvar.median(), 1),
            "higher": int(eff.get("higher", 0)), "equal": int(eff.get("equal", 0)),
            "lower": int(eff.get("lower", 0)),
            "median change %": round(g.delta_pct.median(), 2),
        })
    out += ["", "## Hosting capacity (kW) and effect of default Volt-VAr", "",
            md_table(pd.DataFrame(rows))]

    rows = []
    for code, g in df.groupby("code"):
        fl = g.first_limit.value_counts()
        el = g.thermal_element.value_counts()
        rows.append({
            "code": code,
            "voltage first": int(fl.get("voltage", 0)),
            "thermal first": int(fl.get("thermal", 0)),
            "both": int(fl.get("both", 0)),
            "thermal element: trafo": int(el.get("trafo", 0)),
            "thermal element: line": int(el.get("line", 0)),
        })
    out += ["", "## Which limit binds first without control", "",
            md_table(pd.DataFrame(rows))]

    rows = []
    for (code, fl), g in df.groupby(["code", "first_limit"]):
        eff = g.effect.value_counts()
        rows.append({
            "code": code, "first limit": fl, "buses": len(g),
            "higher": int(eff.get("higher", 0)), "equal": int(eff.get("equal", 0)),
            "lower": int(eff.get("lower", 0)),
            "median change %": round(g.delta_pct.median(), 2),
        })
    out += ["", "## Hypothesis test: effect of Volt-VAr by first limit, per network", "",
            md_table(pd.DataFrame(rows))]

    rows = []
    for fl, g in df.groupby("first_limit"):
        eff = g.effect.value_counts()
        rows.append({
            "first limit": fl, "buses": len(g),
            "higher": int(eff.get("higher", 0)), "equal": int(eff.get("equal", 0)),
            "lower": int(eff.get("lower", 0)),
            "median change %": round(g.delta_pct.median(), 2),
            "min change %": round(g.delta_pct.min(), 2),
            "max change %": round(g.delta_pct.max(), 2),
        })
    out += ["", "## Hypothesis test: all networks together", "",
            md_table(pd.DataFrame(rows))]

    rows = []
    for code, g in df.groupby("code"):
        vf = g[g.first_limit == "voltage"]
        rows.append({
            "code": code,
            "voltage-first buses": len(vf),
            "median gain % (voltage-first buses)": round(vf.gain_pct.median(), 1) if len(vf) else "-",
            "median penalty % (all buses)": round(g.penalty_pct.median(), 1),
            "max penalty % (all buses)": round(g.penalty_pct.max(), 1),
            "hc_vvar = min(parts)": f"{int(g.vvar_is_min.sum())}/{len(g)}",
        })
    out += ["", "## Volt-VAr split: gain on the voltage limit, penalty on the thermal limit", "",
            "Gain is shown only where the voltage limit binds first. Elsewhere hc_v is very "
            "large (PV of several hundred kW or more) and the Volt-VAr iteration may not "
            "converge, so hc_v_vvar there is a numerical limit, not a physical one.", "",
            md_table(pd.DataFrame(rows))]

    bins = [-1, 1.0, 1.05, 1.10, 1.25, 1.5, float("inf")]
    labels = ["< 1 (thermal first)", "1.00-1.05", "1.05-1.10", "1.10-1.25", "1.25-1.50", ">= 1.50"]
    d = df.copy()
    d["r_bin"] = pd.cut(d.ratio_t_v, bins=bins, labels=labels, right=False)
    rows = []
    for lab in labels:
        g = d[d.r_bin == lab]
        if g.empty:
            continue
        eff = g.effect.value_counts()
        rows.append({
            "ratio hc_t / hc_v": lab, "buses": len(g),
            "higher": int(eff.get("higher", 0)), "equal": int(eff.get("equal", 0)),
            "lower": int(eff.get("lower", 0)),
            "median change %": round(g.delta_pct.median(), 2),
        })
    out += ["", "## Screening indicator: effect of Volt-VAr by ratio r = hc_t / hc_v", "",
            md_table(pd.DataFrame(rows))]

    inside = df[df.v_pv_nc <= DEADBAND_UPPER + 0.0005]
    outside = df[df.v_pv_nc > DEADBAND_UPPER + 0.0005]
    out += ["", "## Dead-band check (PV-bus voltage at the no-control capacity)", "",
            f"- PV bus inside the dead band (<= {DEADBAND_UPPER} pu): {len(inside)} buses, "
            f"effect equal in {int((inside.effect == 'equal').sum())}",
            f"- PV bus above the dead band: {len(outside)} buses, "
            f"equal in {int((outside.effect == 'equal').sum())}, "
            f"higher in {int((outside.effect == 'higher').sum())}, "
            f"lower in {int((outside.effect == 'lower').sum())}"]

    out += ["", "## Checks", "",
            f"- hc_nc equals min(hc_v, hc_t) within {EQUAL_TOL_KW} kW: "
            f"{int(df.nc_is_min.sum())} of {len(df)} buses",
            f"- hc_vvar equals min(hc_v_vvar, hc_t_vvar) within {EQUAL_TOL_KW} kW: "
            f"{int(df.vvar_is_min.sum())} of {len(df)} buses",
            f"- buses where at least one search reached the {MAX_KW:.0f} kW ceiling "
            f"(that limit never binds below it): {int(df.capped.sum())}"]
    with open(path, "w", encoding="utf-8") as f:
        f.write("\n".join(out) + "\n")


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--grids", nargs="+", default=GRIDS, choices=GRIDS)
    ap.add_argument("--scenarios", nargs="+", default=["0"])
    ap.add_argument("--workers", type=int, default=1)
    ap.add_argument("--per-grid", type=int, default=20)
    ap.add_argument("--out", default="multi_feeder")
    ap.add_argument("--summarize-only", action="store_true",
                    help="rebuild the summary .md from the saved CSV, no new power flows")
    ap.add_argument("--resume", action="store_true")
    args = ap.parse_args()

    os.makedirs("results", exist_ok=True)
    csv_path = f"results/{args.out}_snapshot.csv"
    md_path = f"results/{args.out}_summary.md"

    if args.summarize_only:
        all_df = pd.read_csv(csv_path)
        info = [network_info(c) for c in sorted(all_df.code.unique())]
        for r in info:
            r["status"] = "ok" if r["base_ok"] else "base violation"
            del r["base_ok"]
        write_summary(md_path, info, all_df)
        print(f"Summary rebuilt: {md_path}")
        return

    df = pd.DataFrame()
    if args.resume and os.path.exists(csv_path):
        df = pd.read_csv(csv_path)
        print("resuming, already done:", sorted(df.code.unique()))

    t0 = time.time()
    info, tasks = [], []
    for s in args.scenarios:
        for g in args.grids:
            code = sb_code(g, s)
            inf = network_info(code)
            info.append({k: v for k, v in inf.items()})
            if not inf["base_ok"]:
                print(f"{code}: base case violates a limit, skipped")
                continue
            if not df.empty and code in set(df.code):
                continue
            tasks += [(code, b, d) for b, d in pick_buses(get_base(code), args.per_grid)]
    for r in info:
        r["status"] = "ok" if r["base_ok"] else "base violation"
        del r["base_ok"]

    print(f"{len(tasks)} buses to analyse, workers = {args.workers}", flush=True)
    new = []

    def save():
        all_df = pd.concat([df, pd.DataFrame(new)], ignore_index=True)
        if not all_df.empty:
            all_df = all_df.sort_values(["code", "bus"]).reset_index(drop=True)
            all_df.to_csv(csv_path, index=False, encoding="utf-8")
        return all_df

    if args.workers > 1:
        ctx = multiprocessing.get_context("spawn")
        with ctx.Pool(args.workers) as pool:
            it = pool.imap_unordered(analyse_bus, tasks, chunksize=1)
            for k, row in enumerate(it, 1):
                new.append(row)
                if k % 10 == 0 or k == len(tasks):
                    print(f"{k}/{len(tasks)} buses, {(time.time() - t0) / 60:.1f} min", flush=True)
                    save()
    else:
        for k, task in enumerate(tasks, 1):
            new.append(analyse_bus(task))
            if k % 10 == 0 or k == len(tasks):
                print(f"{k}/{len(tasks)} buses ({task[0]}), {(time.time() - t0) / 60:.1f} min",
                      flush=True)
                save()

    all_df = save()
    write_summary(md_path, info, all_df, time.time() - t0)
    print(f"\nDone. Send me this file: {md_path}")
    print(f"Full per-bus table: {csv_path}")


if __name__ == "__main__":
    main()