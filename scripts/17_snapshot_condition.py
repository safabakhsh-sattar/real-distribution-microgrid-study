"""Script 17: does the year reach the snapshot operating point?

Why
  At the far buses the snapshot (script 11) finds a thermal limit with Volt-VAr
  (rural1 78.9 kW, urban6 263.8 kW) that no quarter hour of the year reaches
  (script 15 gives 165.1 kW and 390.8 kW, with every daylight step verified).
  The snapshot uses the stored study case: existing PV at full nameplate and
  the stored loads. This script compares that condition with the one-year
  profiles. No power flow is run, so it is fast.

Columns
  snapshot_load_kW, snapshot_existing_pv_kW : stored study case (same net as script 11)
  year_load_min_kW, year_load_max_kW        : total load over the year (quarter hours)
  year_pv_max_kW                            : highest total existing PV over the year
  steps_load_le_snapshot                    : quarter hours with load <= snapshot load
  steps_pv_ge_90pct_and_load_le_snapshot    : quarter hours with PV >= 90 % of the
                                              snapshot PV and load <= snapshot load
                                              (the snapshot condition, roughly)

Run from the repository root:
  python scripts/17_snapshot_condition.py
Output: printed table and results/snapshot_condition.csv
"""
import importlib.util
import os
import warnings

import pandas as pd

warnings.filterwarnings("ignore")

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)


def _load(name, file):
    spec = importlib.util.spec_from_file_location(name, os.path.join(HERE, file))
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


ts = _load("ts12", "12_timeseries.py")       # Data (profiles), DAY_F

FAR = {"rural1": 4, "semiurb5": 51, "urban6": 17}


def main():
    rows = []
    for grid, bus in FAR.items():
        code = f"1-LV-{grid}--0-sw"
        D = ts.Data(code)
        # snapshot = the stored study case, the same net that script 11 uses
        load_snap = float(D.net.load.p_mw.sum()) * 1000
        pv_snap = float(D.net.sgen.p_mw.sum()) * 1000
        day = D.f > ts.DAY_F
        load_y = D.lp.sum(1) * 1000          # total load, kW, every quarter hour
        pv_y = D.sp.sum(1) * 1000            # total existing PV, kW

        le_load = load_y <= load_snap
        near = day & (pv_y >= 0.9 * pv_snap) & le_load

        row = {
            "code": code, "bus": bus,
            "snapshot_load_kW": round(load_snap, 1),
            "snapshot_existing_pv_kW": round(pv_snap, 1),
            "year_load_min_kW": round(float(load_y.min()), 1),
            "year_load_max_kW": round(float(load_y.max()), 1),
            "year_pv_max_kW": round(float(pv_y.max()), 1),
            "daylight_steps": int(day.sum()),
            "steps_load_le_snapshot": int(le_load.sum()),
            "steps_pv_ge_90pct_and_load_le_snapshot": int(near.sum()),
        }
        rows.append(row)
        print(f"{code}: bus {bus}  snapshot load {row['snapshot_load_kW']} kW, "
              f"snapshot PV {row['snapshot_existing_pv_kW']} kW | year load "
              f"{row['year_load_min_kW']}..{row['year_load_max_kW']} kW, year PV max "
              f"{row['year_pv_max_kW']} kW | snapshot-like steps: "
              f"{row['steps_pv_ge_90pct_and_load_le_snapshot']}", flush=True)

    df = pd.DataFrame(rows)
    out = os.path.join(ROOT, "results", "snapshot_condition.csv")
    df.to_csv(out, index=False, encoding="utf-8")
    print("\n" + df.to_string(index=False))
    print(f"\nSaved: {out}")


if __name__ == "__main__":
    main()
