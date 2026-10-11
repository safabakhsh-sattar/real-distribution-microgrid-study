"""Script 12b: operating conditions at the time step that binds the time-series
hosting capacity (supports Section 3.8.2 of the paper).

For every bus of results/timeseries_hc.csv (script 12) it reports
  stored_load_kW      total load stored in the SimBench network (the snapshot value)
  profile_peak_kW     largest total load of the year in the SimBench profiles
  load_at_bind_kW     total load at the binding step, and its share of the stored load
  f_at_bind           PV profile factor at the binding step (share of nameplate)
and, per feeder, the largest PV factor of the year.

Run from the repository root after script 12:
  python scripts/12b_binding_conditions.py
Output: results/binding_conditions.csv and results/binding_conditions.md
Run time: about 1 minute.
"""
import importlib.util
import os
import sys

import pandas as pd

HERE = os.path.dirname(os.path.abspath(__file__))
spec = importlib.util.spec_from_file_location("s12", os.path.join(HERE, "12_timeseries.py"))
s12 = importlib.util.module_from_spec(spec)
spec.loader.exec_module(s12)

RES = sys.argv[1] if len(sys.argv) > 1 else "results"


def step_of(label):
    """'20 May 12:00' -> index of the 15-minute step in 2016."""
    ts = pd.Timestamp(f"{label} 2016")
    return int((ts - s12.START) / pd.Timedelta(minutes=15))


def main():
    hc = pd.read_csv(os.path.join(RES, "timeseries_hc.csv"))
    rows, feeders = [], {}
    for code, g in hc.groupby("code", sort=False):
        D = s12.Data(code)
        stored = float(D.net.load.p_mw.sum() * 1000)
        total = D.lp.sum(1) * 1000
        feeders[code] = (stored, float(total.max()), float(D.f.max()))
        for _, r in g.iterrows():
            t = step_of(r.binding_time)
            assert s12.stamp(t) == r.binding_time, (code, r.binding_time, s12.stamp(t))
            rows.append({
                "code": code, "bus": int(r.bus), "limit": r.limit, "binding_time": r.binding_time,
                "stored_load_kW": round(stored, 1), "profile_peak_kW": round(float(total.max()), 1),
                "load_at_bind_kW": round(float(total[t]), 1),
                "load_share_of_stored_%": round(100 * float(total[t]) / stored, 1),
                "f_at_bind": round(float(D.f[t]), 3),
            })
    out = pd.DataFrame(rows)
    out.to_csv(os.path.join(RES, "binding_conditions.csv"), index=False)

    lines = ["# Conditions at the binding step (script 12b)", "",
             "| code | stored load kW | profile peak kW | stored / peak | max PV factor |",
             "|---|---|---|---|---|"]
    for code, (stored, peak, fmax) in feeders.items():
        lines.append(f"| {code} | {stored:.1f} | {peak:.1f} | {stored / peak:.2f} | {fmax:.3f} |")
    lines += ["", "| code | bus | limit | binding time | load at bind kW | share of stored load % | PV factor |",
              "|---|---|---|---|---|---|---|"]
    for _, r in out.iterrows():
        lines.append(f"| {r.code} | {r.bus} | {r.limit} | {r.binding_time} | {r.load_at_bind_kW} | "
                     f"{r['load_share_of_stored_%']} | {r.f_at_bind} |")
    with open(os.path.join(RES, "binding_conditions.md"), "w", encoding="utf-8") as fh:
        fh.write("\n".join(lines) + "\n")
    print("\n".join(lines))


if __name__ == "__main__":
    main()
