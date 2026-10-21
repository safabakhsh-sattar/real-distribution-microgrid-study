"""Script 16: cross-check of the Volt-VAr capacity code (script 15) at the snapshot.

Question
  Script 15 finds a larger time-series capacity with Volt-VAr than without control
  at the far buses, while script 11 finds a smaller snapshot capacity. Is this a
  difference in the code or a difference in the operating points?

Test
  The stored operating point of each feeder (the snapshot of script 11, no
  profiles) is searched with the same Volt-VAr iteration as script 15, with both
  limits (1.05 pu and 100 % loading), by bisection. The no-control capacity is
  searched the same way.
  The results must reproduce script 11 (results/multi_feeder_snapshot.csv):
    hc_nc (no control) and hc_vvar (with Volt-VAr).
  If they do, the Volt-VAr code agrees with script 11, and the gap to script 15
  comes from the operating points of the year. If they do not, there is a bug.

Run from the repository root:
  python scripts/16_vvar_snapshot_check.py
Output: printed table and results/snapshot_vvar_check.csv
"""
import importlib.util
import os
import warnings

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


ts = _load("ts12", "12_timeseries.py")        # Data, Case, limits_ok, pick_buses
s15 = _load("s15", "15_vvar_timeseries_hc.py")  # VVarCase (Volt-VAr iteration), vv (script 14)

FAR = {"rural1": 4, "semiurb5": 51, "urban6": 17}
MAX_KW, TOL = 2000.0, 0.1


def bisect(check):
    lo, hi = 0.0, MAX_KW
    while hi - lo > TOL:
        mid = (lo + hi) / 2
        try:
            ok = check(mid)
        except Exception:
            ok = False
        if ok:
            lo = mid
        else:
            hi = mid
    return round(lo, 1)


def hc_no_control(case):
    net, idx = case.net, case.idx

    def check(kw):
        net.sgen.at[idx, "p_mw"] = kw / 1000
        net.sgen.at[idx, "q_mvar"] = 0.0
        pp.runpp(net)
        return ts.limits_ok(net)

    return bisect(check)


def hc_volt_var(case):
    net, idx = case.net, case.idx

    def check(kw):
        net.sgen.at[idx, "p_mw"] = kw / 1000
        net.sgen.at[idx, "q_mvar"] = 0.0
        pp.runpp(net)
        v0 = net.res_bus.vm_pu.at[case.bus]
        s15.vv.vvar_iterate(case, kw, v0)     # same iteration as script 15 and script 14
        return ts.limits_ok(net)

    return bisect(check)


def main():
    ms = pd.read_csv(os.path.join(ROOT, "results", "multi_feeder_snapshot.csv"))
    rows = []
    for grid, bus in FAR.items():
        code = f"1-LV-{grid}--0-sw"
        D = ts.Data(code)                     # stored operating point (no profiles)
        ref = ms[(ms.code == code) & (ms.bus == bus)].iloc[0]
        case_nc = ts.Case(D, bus)
        case_vv = s15.VVarCase(D, bus)
        nc = hc_no_control(case_nc)
        vv = hc_volt_var(case_vv)
        rows.append({
            "code": code, "bus": bus,
            "hc_nc_recomputed": nc, "hc_nc_script11": float(ref.hc_nc),
            "hc_vvar_recomputed": vv, "hc_vvar_script11": float(ref.hc_vvar),
            "match": bool(abs(nc - float(ref.hc_nc)) < 0.2 and abs(vv - float(ref.hc_vvar)) < 0.2),
        })
        print(f"{code}: bus {bus}  no control {nc} (script 11: {ref.hc_nc})  "
              f"Volt-VAr {vv} (script 11: {ref.hc_vvar})", flush=True)

    df = pd.DataFrame(rows)
    out = os.path.join(ROOT, "results", "snapshot_vvar_check.csv")
    df.to_csv(out, index=False, encoding="utf-8")
    print("\n" + df.to_string(index=False))
    print(f"\nAll match: {bool(df.match.all())}")
    print(f"Saved: {out}")


if __name__ == "__main__":
    main()