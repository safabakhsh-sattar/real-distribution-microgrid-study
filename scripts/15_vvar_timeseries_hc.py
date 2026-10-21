"""Script 15: time-series hosting capacity with Volt-VAr at the far bus of each feeder.

Question (week 6)
  The snapshot study (script 11) gives the indicator r = hc_t / hc_v without control.
  Does the sign of the Volt-VAr effect on the capacity follow r when the capacity
  is found over one year of 15-minute profiles, as in script 12?

Method
  The search is the one of script 12 (critical-step method): same daylight steps,
  same ranking, same critical set, same verification set, same random seed, same
  base-violation skip list. The only change: the added unit follows the default
  IEEE 1547 Volt-VAr curve (script 14, vvar_iterate) in every power flow of the
  search. Q = ratio(V) x nameplate, solved as a fixed point.

  Only the far bus of each feeder is searched.
  The no-control time-series capacity is read from results/timeseries_hc.csv.
  The snapshot ratio r is read from results/multi_feeder_snapshot.csv (ratio_t_v).

  Verification (default): the final Volt-VAr capacity is checked on every daylight
  step, as in script 12 --verify-full, so the result does not depend on the sampled
  verification set. --sampled uses the critical and verification sets only (quick test).
  A power flow that does not converge counts as a violation (conservative).
  Non-convergence at sizes above the final capacity is expected (the bisection
  starts at 2000 kW) and does not change the result. Column
  nonconverged_at_or_below_capacity must be 0.

Run from the repository root:
  python scripts/15_vvar_timeseries_hc.py --workers 3
  python scripts/15_vvar_timeseries_hc.py --grids rural1 --sampled --k-crit 10 --k-verify 30 --k-rand 10 --out test
Outputs: results/vvar_timeseries_hc.csv and results/vvar_timeseries_summary.md
(--out NAME replaces 'vvar_timeseries').
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


ts = _load("ts12", "12_timeseries.py")       # Data, Case, pick_buses, hc_timeseries, limits
vv = _load("s14", "14_vvar_annual.py")       # vvar_iterate, FAR_BUS
GRIDS = ["rural1", "semiurb5", "urban6"]


class VVarCase(ts.Case):
    """Added unit with the default Volt-VAr curve, solved inside every power flow."""

    def __init__(self, D, bus):
        super().__init__(D, bus)
        self.nonconv_kw = []                 # size of each non-converged check

    def run_size(self, size_kw, t, hourly=False):
        try:
            f = self.D.h_f[t] if hourly else self.D.f[t]
            self.set_state(t, hourly)
            self.net.sgen.at[self.idx, "p_mw"] = size_kw * f / 1000
            self.net.sgen.at[self.idx, "q_mvar"] = 0.0
            pp.runpp(self.net)                        # Q = 0 first (as script 14)
            v0 = self.net.res_bus.vm_pu.at[self.bus]
            vv.vvar_iterate(self, size_kw, v0)        # Q = ratio(V) x nameplate, fixed point
        except Exception:
            self.nonconv_kw.append(size_kw)
            raise


def band(r):
    if r >= 1.05:
        return "gain expected"
    if r < 1.0:
        return "no gain expected"
    return "mixed band"


def run_feeder(job):
    grid, a = job
    t0 = time.time()
    code = f"1-LV-{grid}--0-sw"
    D = ts.Data(code)
    picks = ts.pick_buses(D.net)
    far = picks[-1][0]
    if far != vv.FAR_BUS[grid]:
        raise RuntimeError(f"{grid}: far bus is {far}, expected {vv.FAR_BUS[grid]}")

    hc_nc = pd.read_csv(os.path.join(ROOT, "results", "timeseries_hc.csv"))
    rows_nc = hc_nc[hc_nc.code == code]
    snaps = [float(rows_nc[rows_nc.bus == b].hc_snapshot.iloc[0]) for b, _ in picks]
    p_ref = float(np.median(snaps)) / 1000
    row_far = rows_nc[rows_nc.bus == far].iloc[0]
    hc_ts_nc, hc_snap = float(row_far.hc_ts), float(row_far.hc_snapshot)

    ms = pd.read_csv(os.path.join(ROOT, "results", "multi_feeder_snapshot.csv"))
    r = float(ms[(ms.code == code) & (ms.bus == far)].ratio_t_v.iloc[0])

    # --- same critical and verification sets as script 12 -------------------------
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

    # --- Volt-VAr capacity search at the far bus -----------------------------------
    case = VVarCase(D, far)
    if not a["sampled"]:
        V = [int(t) for t in day if int(t) not in skip]     # every daylight step
    hc_v, crit, rounds, nchk, nviol = ts.hc_timeseries(case, C0, V, skip)
    limit = ts.limiting_element(case, hc_v, crit) if crit is not None else "none"

    row = {
        "code": code, "bus": far,
        "r_snapshot_t_over_v": round(r, 3),
        "rule_band": band(r),
        "hc_snapshot_nc": hc_snap,
        "hc_ts_nc": hc_ts_nc,
        "hc_ts_vvar": hc_v,
        "delta_kW": round(hc_v - hc_ts_nc, 1),
        "delta_pct": round(100 * (hc_v - hc_ts_nc) / hc_ts_nc, 2) if hc_ts_nc else float("nan"),
        "limit_at_vvar_capacity": limit,
        "refine_rounds": rounds,
        "verify_steps": nchk,
        "unresolved_violations": nviol,
        "nonconverged_checks": len(case.nonconv_kw),
        "min_nonconverged_kW": round(min(case.nonconv_kw), 1) if case.nonconv_kw else "",
        "nonconverged_at_or_below_capacity": sum(1 for s_ in case.nonconv_kw if s_ <= hc_v),
        "skipped_base_violation": len(skip),
        "verify_set": "sampled" if a["sampled"] else "all daylight steps",
        "minutes": round((time.time() - t0) / 60, 1),
    }
    print(f"{code}: bus {far}, no control {hc_ts_nc} kW, Volt-VAr {hc_v} kW "
          f"({row['delta_pct']:+.2f}%), r = {r:.3f}, non-converged {len(case.nonconv_kw)} (at or below capacity: {row['nonconverged_at_or_below_capacity']}), "
          f"{row['minutes']} min", flush=True)
    return grid, row


def md_table(df):
    cols = list(df.columns)
    lines = ["| " + " | ".join(str(c) for c in cols) + " |", "|" + "---|" * len(cols)]
    for _, r in df.iterrows():
        lines.append("| " + " | ".join(str(r[c]) for c in cols) + " |")
    return "\n".join(lines)


def write_summary(path, df, seconds):
    lines = [
        "# Time-series hosting capacity with Volt-VAr (script 15)",
        "",
        "Far bus of each feeder. Same search as script 12 (critical-step method, same",
        "critical and verification sets). Added unit follows the default IEEE 1547",
        "Volt-VAr curve in every power flow. One weather year, 15-minute steps.",
        "",
        "## Results",
        "",
        md_table(df),
        "",
        "## Run checks",
        "",
        f"Non-converged power flows (all sizes): {int(df.nonconverged_checks.sum())}.",
        f"Non-converged at or below the capacity (must be 0): {int(df.nonconverged_at_or_below_capacity.sum())}.",
        f"Total time: {seconds / 60:.1f} min.",
        "",
        "Send this file back: results/vvar_timeseries_summary.md",
        "",
    ]
    with open(path, "w", encoding="utf-8") as fh:
        fh.write("\n".join(lines))


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--grids", nargs="+", default=GRIDS, choices=GRIDS)
    ap.add_argument("--workers", type=int, default=1)
    ap.add_argument("--k-crit", type=int, default=100)
    ap.add_argument("--k-verify", type=int, default=1500)
    ap.add_argument("--k-rand", type=int, default=500)
    ap.add_argument("--out", default="vvar_timeseries")
    ap.add_argument("--sampled", action="store_true")
    args = ap.parse_args()
    a = dict(k_crit=args.k_crit, k_verify=args.k_verify, k_rand=args.k_rand, sampled=args.sampled)

    os.makedirs(os.path.join(ROOT, "results"), exist_ok=True)
    p_csv = os.path.join(ROOT, "results", f"{args.out}_hc.csv")
    p_md = os.path.join(ROOT, "results", f"{args.out}_summary.md")
    jobs = [(g, a) for g in args.grids]
    print(f"feeders: {[j[0] for j in jobs]}, workers = {args.workers}", flush=True)

    t0 = time.time()
    rows = []
    if args.workers > 1 and len(jobs) > 1:
        ctx = multiprocessing.get_context("spawn")
        with ctx.Pool(min(args.workers, len(jobs))) as pool:
            for grid, row in pool.imap_unordered(run_feeder, jobs):
                rows.append(row)
                print(f"== {grid} finished", flush=True)
    else:
        for job in jobs:
            grid, row = run_feeder(job)
            rows.append(row)

    seconds = time.time() - t0
    df = pd.DataFrame(rows).sort_values("code").reset_index(drop=True)
    df.to_csv(p_csv, index=False, encoding="utf-8")
    write_summary(p_md, df, seconds)
    print(f"\nTotal time {seconds / 60:.1f} min")
    print(f"Send me this file: {p_md}")


if __name__ == "__main__":
    multiprocessing.freeze_support()
    main()