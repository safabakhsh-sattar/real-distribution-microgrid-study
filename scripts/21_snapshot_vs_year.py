"""Script 21: does a snapshot predict the year? Stored point against study cases.

Why
  At the stored operating point the sign of the Volt-VAr effect was wrong over
  the year at two of three far buses (Section 3.9). This script asks whether a
  snapshot at a SimBench study case (script 19) predicts the year sign better,
  on the nine buses of the time-series study (scripts 12, 15 and 20).

Inputs (no power flow is run here)
  results/studycase_snapshot.csv     script 19 (stored point and study cases, nine buses)
  results/multi_feeder_snapshot.csv  script 11 (check that the stored rows of script 19 match)
  results/timeseries_hc.csv          script 12 (year capacity without control)
  results/year_controls_hc.csv       script 20 (year capacity with Volt-VAr and cos phi(P))

For each bus and each operating point (stored, and each study case):
  sign of the snapshot effect   higher / equal / lower (0.2 kW tolerance, as script 11)
  rule of r                     gain expected (r >= 1.05), no gain expected (r < 1), mixed band
  agreement with the year       snapshot sign = year sign; and, outside the mixed band,
                                rule = year outcome (gain expected and year higher, or
                                no gain expected and year not higher)

Pre-registered predictions: see docs/predictions_19_21.md.

Run from the repository root:
  python scripts/21_snapshot_vs_year.py
Output: results/snapshot_vs_year_summary.md (send back)
"""
import os

import pandas as pd

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
RES = os.path.join(ROOT, "results")
TOL = 0.2
POS = {"near": 0, "middle": 1, "far": 2}


def sign(delta_kw):
    if delta_kw > TOL:
        return "higher"
    if delta_kw < -TOL:
        return "lower"
    return "equal"


def rule(r):
    if r >= 1.05:
        return "gain expected"
    if r < 1.0:
        return "no gain expected"
    return "mixed band"


def rule_hit(band, year_sign):
    if band == "gain expected":
        return year_sign == "higher"
    if band == "no gain expected":
        return year_sign != "higher"
    return None


def md_table(df):
    cols = list(df.columns)
    lines = ["| " + " | ".join(str(c) for c in cols) + " |", "|" + "---|" * len(cols)]
    for _, r in df.iterrows():
        lines.append("| " + " | ".join(str(r[c]) for c in cols) + " |")
    return "\n".join(lines)


def main():
    sc = pd.read_csv(os.path.join(RES, "studycase_snapshot.csv"), keep_default_na=False, na_values=[""])
    sc["position"] = sc.position.fillna("")
    sc = sc[sc.position != ""]
    s11 = pd.read_csv(os.path.join(RES, "multi_feeder_snapshot.csv"))
    yr = pd.read_csv(os.path.join(RES, "year_controls_hc.csv"))
    nc = pd.read_csv(os.path.join(RES, "timeseries_hc.csv"))

    out = ["# Snapshot against year: stored point and study cases (script 21)", ""]

    # --- check: stored rows of script 19 = script 11 -------------------------------
    st = sc[sc.case == "stored"].merge(s11, on=["code", "bus"], suffixes=("", "_s11"))
    if len(st):
        d_nc = (st.hc_nc - st.hc_nc_s11).abs().max()
        d_vv = (st.hc_vvar - st.hc_vvar_s11).abs().max()
        out += ["## Check: stored rows of script 19 against script 11", "",
                f"Buses in both: {len(st)}. Largest difference: hc_nc {d_nc:.1f} kW, "
                f"hc_vvar {d_vv:.1f} kW (must be 0.0, or within 0.1 kW of search tolerance).", ""]

    # --- Volt-VAr -------------------------------------------------------------------
    yv = yr[yr.control == "vvar"][["code", "bus", "hc_ts_nc", "hc_ts_ctrl", "delta_kW", "delta_pct"]]
    yv = yv.rename(columns={"hc_ts_ctrl": "year_vvar_kW", "delta_kW": "year_dkW",
                            "delta_pct": "year_vvar_%", "hc_ts_nc": "year_nc_kW"})
    rows, score = [], []
    for (code, bus), g in sc.groupby(["code", "bus"]):
        y = yv[(yv.code == code) & (yv.bus == bus)]
        if y.empty:
            continue
        y = y.iloc[0]
        ys = sign(y.year_dkW)
        for _, r in g.iterrows():
            ss = sign(r.hc_vvar - r.hc_nc)
            band = rule(r.ratio_t_v)
            hit = rule_hit(band, ys)
            rows.append({
                "grid": code.split("-")[2], "bus": bus, "position": r.position,
                "point": r.case, "f_pv": r.f_pv, "snapshot hc_nc": r.hc_nc,
                "r": r.ratio_t_v, "rule": band, "snapshot Volt-VAr %": r.delta_pct,
                "snapshot sign": ss, "year Volt-VAr %": y["year_vvar_%"], "year sign": ys,
                "sign agrees": ss == ys, "rule agrees": "-" if hit is None else hit})
            score.append({"point": r.case, "sign agrees": ss == ys, "rule hit": hit})
    if rows:
        t = pd.DataFrame(rows)
        t["o"] = t.position.map(POS)
        t = t.sort_values(["grid", "o", "point"]).drop(columns="o")
        out += ["## Volt-VAr: snapshot effect and rule of r against the year, nine buses", "",
                md_table(t), ""]
        s = pd.DataFrame(score)
        agg = []
        for p, g in s.groupby("point"):
            ruled = g[g["rule hit"].notna()]
            agg.append({"operating point": p, "buses": len(g),
                        "snapshot sign = year sign": f"{int(g['sign agrees'].sum())} of {len(g)}",
                        "rule of r correct (outside mixed band)":
                            f"{int(ruled['rule hit'].astype(bool).sum())} of {len(ruled)}"})
        out += ["## Volt-VAr: agreement with the year per operating point", "",
                md_table(pd.DataFrame(agg)), ""]

    # --- cos phi(P) -----------------------------------------------------------------
    yc = yr[yr.control == "cosphi"]
    rows, agg = [], {}
    for _, r in sc.iterrows():
        y = yc[(yc.code == r.code) & (yc.bus == r.bus)]
        if y.empty:
            continue
        y = y.iloc[0]
        ss, ys = sign(r.hc_cosphi - r.hc_nc), sign(y.delta_kW)
        rows.append({"grid": r.code.split("-")[2], "bus": r.bus, "position": r.position,
                     "point": r.case, "snapshot cos phi %": r.cosphi_pct, "snapshot sign": ss,
                     "year cos phi %": y.delta_pct, "year sign": ys, "sign agrees": ss == ys})
        a = agg.setdefault(r.case, [0, 0])
        a[0] += ss == ys
        a[1] += 1
    if rows:
        t = pd.DataFrame(rows)
        t["o"] = t.position.map(POS)
        t = t.sort_values(["grid", "o", "point"]).drop(columns="o")
        out += ["## cos phi(P): snapshot effect against the year, nine buses", "", md_table(t), "",
                "Agreement of the sign per operating point: "
                + "; ".join(f"{p}: {v[0]} of {v[1]}" for p, v in sorted(agg.items())), ""]

    # --- year: Volt-VAr against cos phi(P) -------------------------------------------
    piv = yr.pivot_table(index=["code", "bus"], columns="control", values="delta_pct").reset_index()
    if {"vvar", "cosphi"} <= set(piv.columns):
        piv = piv.merge(nc[["code", "bus", "hc_ts", "limit"]], on=["code", "bus"], how="left")
        piv = piv.rename(columns={"hc_ts": "year no control kW", "limit": "year limit (no control)",
                                  "vvar": "year Volt-VAr %", "cosphi": "year cos phi %"})
        out += ["## Year: Volt-VAr against cos phi(P)", "", md_table(piv.round(2)), ""]

    out += ["Send this file back: results/snapshot_vs_year_summary.md", ""]
    p = os.path.join(RES, "snapshot_vs_year_summary.md")
    with open(p, "w", encoding="utf-8") as f:
        f.write("\n".join(out))
    print(f"Done. Send me this file: {p}")


if __name__ == "__main__":
    main()
