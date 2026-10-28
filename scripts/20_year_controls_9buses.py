"""Script 20: time-series hosting capacity with Volt-VAr and cos phi(P) at nine buses.

Why
  Script 15 found the Volt-VAr capacity over the year at the far bus of each
  feeder only (three buses). This script extends it to the near, middle and far
  bus of each feeder (the nine buses of script 12), so the year result does not
  rest on three buses. It also adds the cos phi(P) characteristic of the type in
  VDE-AR-N 4105:2018 (script 19, cosphi_q_kvar), the German default for LV
  generators, so the IEEE 1547 curve is compared with a European one.

Method
  The search is the one of script 15 (and script 12): same daylight steps, same
  ranking, same critical set, same verification set (every daylight step by
  default), same random seed, same skip list. Only the control of the added unit
  changes:
    vvar    default IEEE 1547 Volt-VAr, Q = ratio(V) x Pn (script 14 vvar_iterate)
    cosphi  Q = cos phi(P) characteristic, P = Pn x f(t); no voltage input, no iteration
  The no-control capacity is read from results/timeseries_hc.csv (script 12).
  With --reuse-far (default) the Volt-VAr far-bus rows are copied from
  results/vvar_timeseries_hc.csv (script 15, same method), so they are not run twice.
  A power flow that does not converge counts as a violation (conservative).
  Column nonconverged_at_or_below_capacity must be 0.

Pre-registered predictions: see docs/predictions_19_21.md (register before the run).

Run from the repository root:
  python scripts/20_year_controls_9buses.py --workers 3
  python scripts/20_year_controls_9buses.py --controls cosphi --workers 3      (cos phi only, faster)
  python scripts/20_year_controls_9buses.py --grids rural1 --sampled --k-crit 10 --k-verify 30 --k-rand 10 --out test
Outputs: results/year_controls_hc.csv and results/year_controls_summary.md
(--out NAME replaces 'year_controls'). The run saves after every bus; --resume continues.
Send back: results/year_controls_summary.md
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


ts = _load("ts12", "12_timeseries.py")             # Data, Case, pick_buses, hc_timeseries, limits
vv = _load("s14", "14_vvar_annual.py")             # vvar_iterate, FAR_BUS
s19 = _load("s19", "19_studycase_snapshot.py")     # cosphi_q_kvar
GRIDS = ["rural1", "semiurb5", "urban6"]
POSITIONS = ["near", "middle", "far"]
CONTROLS = ["vvar", "cosphi"]


class CtrlCase(ts.Case):
    """Added unit with a reactive power control, solved inside every power flow."""

    def __init__(self, D, bus, control):
        super().__init__(D, bus)
        self.control = control
        self.nonconv_kw = []

    def run_size(self, size_kw, t, hourly=False):
        try:
            f = self.D.h_f[t] if hourly else self.D.f[t]
            self.set_state(t, hourly)
            p = size_kw * f
            self.net.sgen.at[self.idx, "p_mw"] = p / 1000
            self.net.sgen.at[self.idx, "q_mvar"] = 0.0
            if self.control == "cosphi":
                self.net.sgen.at[self.idx, "q_mvar"] = s19.cosphi_q_kvar(p, size_kw) / 1000
                pp.runpp(self.net)
            else:
                pp.runpp(self.net)                       # Q = 0 first (as scripts 14 and 15)
                v0 = self.net.res_bus.vm_pu.at[self.bus]
                vv.vvar_iterate(self, size_kw, v0)
        except Exception:
            self.nonconv_kw.append(size_kw)
            raise


_DATA = {}


def get_data(code):
    if code not in _DATA:
        _DATA[code] = ts.Data(code)
    return _DATA[code]


def run_job(job):
    grid, bus, position, control, a = job
    t0 = time.time()
    code = f"1-LV-{grid}--0-sw"
    D = get_data(code)
    picks = ts.pick_buses(D.net)

    hc_nc = pd.read_csv(os.path.join(ROOT, "results", "timeseries_hc.csv"))
    rows_nc = hc_nc[hc_nc.code == code]
    snaps = [float(rows_nc[rows_nc.bus == b].hc_snapshot.iloc[0]) for b, _ in picks]
    p_ref = float(np.median(snaps)) / 1000
    row_b = rows_nc[rows_nc.bus == bus].iloc[0]
    hc_ts_nc = float(row_b.hc_ts)

    # --- same critical and verification sets as scripts 12 and 15 -----------------
    day = np.where(D.f > ts.DAY_F)[0]
    score = D.N + p_ref * D.f
    order = day[np.argsort(-score[day])]
    C0 = [int(t) for t in order[:a["k_crit"]]]
    rng = np.random.default_rng(0)
    rand = rng.choice(day, size=min(a["k_rand"], len(day)), replace=False)
    V = list(dict.fromkeys([int(t) for t in order[:a["k_verify"]]] + [int(t) for t in rand]))

    probe = ts.Case(D, picks[0][0])
    skip = set()
    for t in set(C0) | set(V):
        try:
            probe.run_p(0.0, t)
            if not ts.limits_ok(probe.net):
                skip.add(t)
        except Exception:
            skip.add(t)

    case = CtrlCase(D, bus, control)
    if not a["sampled"]:
        V = [int(t) for t in day if int(t) not in skip]        # every daylight step
    hc_c, crit, rounds, nchk, nviol = ts.hc_timeseries(case, C0, V, skip)
    limit = ts.limiting_element(case, hc_c, crit) if crit is not None else "none"

    row = {
        "code": code, "bus": bus, "position": position, "control": control,
        "hc_ts_nc": hc_ts_nc, "hc_ts_ctrl": hc_c,
        "delta_kW": round(hc_c - hc_ts_nc, 1),
        "delta_pct": round(100 * (hc_c - hc_ts_nc) / hc_ts_nc, 2) if hc_ts_nc else float("nan"),
        "limit_at_capacity": limit,
        "binding_time": ts.stamp(crit) if crit is not None else "-",
        "refine_rounds": rounds, "verify_steps": nchk, "unresolved_violations": nviol,
        "nonconverged_checks": len(case.nonconv_kw),
        "nonconverged_at_or_below_capacity": sum(1 for s_ in case.nonconv_kw if s_ <= hc_c),
        "skipped_base_violation": len(skip),
        "verify_set": "sampled" if a["sampled"] else "all daylight steps",
        "source": "script 20", "minutes": round((time.time() - t0) / 60, 1),
    }
    print(f"{code}: bus {bus} ({position}), {control}: no control {hc_ts_nc} kW, "
          f"with control {hc_c} kW ({row['delta_pct']:+.2f}%), {row['minutes']} min", flush=True)
    return row


def reused_far_row(code, bus):
    """Volt-VAr far-bus row of script 15, in the columns of this script."""
    p = os.path.join(ROOT, "results", "vvar_timeseries_hc.csv")
    if not os.path.exists(p):
        return None
    d = pd.read_csv(p)
    d = d[(d.code == code) & (d.bus == bus)]
    if d.empty:
        return None
    r = d.iloc[0]
    return {"code": code, "bus": bus, "position": "far", "control": "vvar",
            "hc_ts_nc": r.hc_ts_nc, "hc_ts_ctrl": r.hc_ts_vvar, "delta_kW": r.delta_kW,
            "delta_pct": r.delta_pct, "limit_at_capacity": r.limit_at_vvar_capacity,
            "binding_time": "-", "refine_rounds": r.refine_rounds, "verify_steps": r.verify_steps,
            "unresolved_violations": r.unresolved_violations,
            "nonconverged_checks": r.nonconverged_checks,
            "nonconverged_at_or_below_capacity": r.nonconverged_at_or_below_capacity,
            "skipped_base_violation": r.skipped_base_violation, "verify_set": r.verify_set,
            "source": "script 15 (reused)", "minutes": r.minutes}


def write_summary(path, df, seconds):
    md = ts.md_table
    cols = ["code", "bus", "position", "control", "hc_ts_nc", "hc_ts_ctrl", "delta_pct",
            "limit_at_capacity", "binding_time", "unresolved_violations",
            "nonconverged_at_or_below_capacity", "verify_set", "source"]
    d = df.copy()
    d["pos_order"] = d.position.map({p: i for i, p in enumerate(POSITIONS)})
    d = d.sort_values(["control", "code", "pos_order"])
    agg = []
    for ctrl, g in d.groupby("control"):
        agg.append({"control": ctrl, "buses": len(g),
                    "higher (> +0.2 kW)": int((g.delta_kW > 0.2).sum()),
                    "equal": int((g.delta_kW.abs() <= 0.2).sum()),
                    "lower (< -0.2 kW)": int((g.delta_kW < -0.2).sum()),
                    "median change %": round(g.delta_pct.median(), 2),
                    "min %": round(g.delta_pct.min(), 2), "max %": round(g.delta_pct.max(), 2)})
    lines = ["# Time-series hosting capacity with Volt-VAr and cos phi(P), nine buses (script 20)", "",
             "Search of scripts 12 and 15 (critical-step method, same sets, 15-minute steps, one",
             "weather year). Change relative to the no-control time-series capacity of script 12.", "",
             "## Per bus", "", md(d[cols]), "", "## Summary", "", md(pd.DataFrame(agg)), "",
             "## Run checks", "",
             f"Unresolved violations (must be 0): {int(d.unresolved_violations.sum())}.",
             f"Non-converged at or below the capacity (must be 0): "
             f"{int(d.nonconverged_at_or_below_capacity.sum())}.",
             (f"Total time: {seconds / 60:.1f} min." if seconds else ""), "",
             "Send this file back: " + os.path.relpath(path, ROOT), ""]
    with open(path, "w", encoding="utf-8") as fh:
        fh.write("\n".join(lines))


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--grids", nargs="+", default=GRIDS, choices=GRIDS)
    ap.add_argument("--controls", nargs="+", default=CONTROLS, choices=CONTROLS)
    ap.add_argument("--positions", nargs="+", default=POSITIONS, choices=POSITIONS)
    ap.add_argument("--workers", type=int, default=1)
    ap.add_argument("--k-crit", type=int, default=100)
    ap.add_argument("--k-verify", type=int, default=1500)
    ap.add_argument("--k-rand", type=int, default=500)
    ap.add_argument("--sampled", action="store_true")
    ap.add_argument("--no-reuse-far", action="store_true",
                    help="run the Volt-VAr far buses again instead of copying script 15")
    ap.add_argument("--resume", action="store_true")
    ap.add_argument("--out", default="year_controls")
    args = ap.parse_args()
    a = dict(k_crit=args.k_crit, k_verify=args.k_verify, k_rand=args.k_rand, sampled=args.sampled)

    os.makedirs(os.path.join(ROOT, "results"), exist_ok=True)
    p_csv = os.path.join(ROOT, "results", f"{args.out}_hc.csv")
    p_md = os.path.join(ROOT, "results", f"{args.out}_summary.md")
    old = pd.read_csv(p_csv) if args.resume and os.path.exists(p_csv) else pd.DataFrame()
    done = set(zip(old.code, old.bus, old.control)) if len(old) else set()

    rows, jobs = [], []
    for g in args.grids:
        code = f"1-LV-{g}--0-sw"
        D = get_data(code)
        picks = ts.pick_buses(D.net)
        if picks[-1][0] != vv.FAR_BUS[g]:
            raise RuntimeError(f"{g}: far bus is {picks[-1][0]}, expected {vv.FAR_BUS[g]}")
        for (b, _), pos in zip(picks, POSITIONS):
            if pos not in args.positions:
                continue
            for c in args.controls:
                if (code, b, c) in done:
                    continue
                if c == "vvar" and pos == "far" and not args.no_reuse_far:
                    r = reused_far_row(code, b)
                    if r is not None:
                        rows.append(r)
                        continue
                jobs.append((g, int(b), pos, c, a))
    print(f"{len(jobs)} searches to run ({len(rows)} rows reused), workers = {args.workers}", flush=True)

    t0 = time.time()

    def save():
        d = pd.concat([old, pd.DataFrame(rows)], ignore_index=True)
        d.to_csv(p_csv, index=False, encoding="utf-8")
        return d

    if args.workers > 1 and len(jobs) > 1:
        ctx = multiprocessing.get_context("spawn")
        with ctx.Pool(min(args.workers, len(jobs))) as pool:
            for row in pool.imap_unordered(run_job, jobs):
                rows.append(row)
                save()
    else:
        for job in jobs:
            rows.append(run_job(job))
            save()

    df = save()
    write_summary(p_md, df, time.time() - t0)
    print(f"\nTotal time {(time.time() - t0) / 60:.1f} min")
    print(f"Send me this file: {p_md}")


if __name__ == "__main__":
    multiprocessing.freeze_support()
    main()
