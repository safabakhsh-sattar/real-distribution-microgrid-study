"""Figures 4 to 6 for study 2 (multi-feeder snapshot and time-series).

Reads the CSV files written by scripts 11 and 12 (run those first):
    results/multi_feeder_snapshot.csv   (script 11)
    results/timeseries_hc.csv           (script 12)
    results/timeseries_energy.csv       (script 12)

Writes:
    results/fig4_effect_vs_ratio.png        Volt-VAr effect against r = hc_t / hc_v
    results/fig5_snapshot_vs_timeseries.png Snapshot vs time-series hosting capacity
    results/fig6_energy_curtailment.png     Annual energy and curtailment vs nameplate

Run from the repository root:  python scripts/13_figures_study2.py
Optional: --results DIR (input and output folder, default results)
"""
import argparse
import os

import numpy as np
import pandas as pd
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

# Same neutral style as script 07. Colours here encode the effect (figure 4)
# or the feeder (figures 5 and 6), not the control strategy.
INK, MUTED, GRID = "#0b0b0b", "#52514e", "#e4e3df"
C_HIGHER, C_EQUAL, C_LOWER = "#2f8f5b", "#b9b8b2", "#eb6834"
C_SNAP, C_TS = "#9a9993", "#2a78d6"
FEEDER_COLOR = {"rural1": "#2a78d6", "semiurb5": "#d9822b", "urban6": "#4a3aa7"}

plt.rcParams.update({
    "font.size": 10, "text.color": INK, "axes.labelcolor": INK,
    "axes.spines.top": False, "axes.spines.right": False, "axes.edgecolor": "#9a9993",
    "xtick.color": MUTED, "ytick.color": MUTED,
    "axes.grid": True, "grid.color": GRID, "grid.linewidth": 0.6, "axes.axisbelow": True,
    "legend.frameon": False,
})


def short(code):
    """'1-LV-rural1--0-sw' -> 'rural1'."""
    return code.split("-LV-")[1].split("--")[0]


def figure4(snap, path):
    d = snap.dropna(subset=["ratio_t_v", "delta_pct"]).copy()
    colors = {"higher": C_HIGHER, "equal": C_EQUAL, "lower": C_LOWER}

    fig, (ax, bx) = plt.subplots(1, 2, figsize=(11, 4.6),
                                 gridspec_kw={"width_ratios": [1.5, 1]})

    for eff in ("lower", "equal", "higher"):
        g = d[d.effect == eff]
        ax.scatter(g.ratio_t_v, g.delta_pct, s=26, color=colors[eff], edgecolor="white",
                   linewidth=0.5, label=f"{eff} ({len(g)})", zorder=3)
    ax.set_xscale("log")
    ax.axhline(0, color=INK, linewidth=1.0)
    ax.axvline(1.0, color=MUTED, linewidth=0.8, linestyle="--")
    ax.axvline(1.05, color=MUTED, linewidth=0.8, linestyle=":")
    ymax = ax.get_ylim()[1]
    ax.text(0.94, ymax * 0.97, "r = 1", ha="right", va="top", fontsize=8, color=MUTED)
    ax.text(1.12, ymax * 0.97, "r = 1.05", ha="left", va="top", fontsize=8, color=MUTED)
    ax.set_xlabel("r = hc_t / hc_v  (no control; r > 1: voltage limit binds first)")
    ax.set_ylabel("Change of hosting capacity with Volt-VAr (%)")
    ax.set_title(f"(a) Each point is one bus ({len(d)} buses)", loc="left", fontsize=10)
    ax.legend(loc="upper left", fontsize=9, title="Volt-VAr effect", title_fontsize=9)

    bins = [0, 1.0, 1.05, 1.10, 1.25, 1.50, np.inf]
    labels = ["< 1", "1.00-1.05", "1.05-1.10", "1.10-1.25", "1.25-1.50", ">= 1.50"]
    d["bin"] = pd.cut(d.ratio_t_v, bins=bins, labels=labels, right=False)
    counts = (d.groupby(["bin", "effect"], observed=False).size()
                .unstack(fill_value=0).reindex(columns=["lower", "equal", "higher"], fill_value=0))
    x = np.arange(len(labels))
    bottom = np.zeros(len(labels))
    for eff in ("lower", "equal", "higher"):
        vals = counts[eff].reindex(labels).fillna(0).values
        bx.bar(x, vals, bottom=bottom, color=colors[eff], edgecolor="white", linewidth=0.8,
               label=eff)
        bottom += vals
    for i, tot in enumerate(bottom):
        bx.text(i, tot + bottom.max() * 0.01, f"{int(tot)}", ha="center", va="bottom", fontsize=8, color=INK)
    bx.set_ylim(0, bottom.max() * 1.12)
    bx.set_xticks(x)
    bx.set_xticklabels(labels, rotation=30, ha="right")
    bx.set_xlabel("Bin of r")
    bx.set_ylabel("Number of buses")
    bx.set_title("(b) Counts per bin of r", loc="left", fontsize=10)
    fig.tight_layout()
    fig.savefig(path, dpi=200)
    plt.close(fig)


def figure5(hc, path):
    d = hc.copy()
    d["feeder"] = d.code.map(short)
    d["label"] = d.apply(lambda r: f"{r.feeder}  bus {int(r.bus)}\n({r.limit} limit)", axis=1)
    n = len(d)
    y = np.arange(n)[::-1]
    h = 0.36

    fig, ax = plt.subplots(figsize=(10, 0.62 * n + 1.6))
    ax.barh(y + h / 2, d.hc_snapshot, h, color=C_SNAP, edgecolor="white", linewidth=0.8,
            label="Snapshot (stored SimBench operating point)")
    ax.barh(y - h / 2, d.hc_ts, h, color=C_TS, edgecolor="white", linewidth=0.8,
            label="Time series (one year, 15-min steps)")
    xmax = max(d.hc_snapshot.max(), d.hc_ts.max())
    for yi, (_, r) in zip(y, d.iterrows()):
        ax.text(r.hc_ts + xmax * 0.01, yi - h / 2, f"{r.hc_ts:.0f} kW  (x{r.ratio_ts_snapshot:.2f})",
                va="center", fontsize=8, color=INK)
        ax.text(r.hc_snapshot + xmax * 0.01, yi + h / 2, f"{r.hc_snapshot:.0f}",
                va="center", fontsize=8, color=MUTED)
    ax.set_yticks(y)
    ax.set_yticklabels(d.label, fontsize=8.5)
    ax.set_xlim(0, xmax * 1.22)
    ax.set_xlabel("Additional PV hosting capacity, no control (kW)")
    ax.set_title("Snapshot vs time-series hosting capacity: the sign of the bias depends on the binding limit",
                 loc="left", fontsize=10)
    ax.legend(loc="lower right", fontsize=9)
    ax.grid(axis="y", visible=False)
    fig.tight_layout()
    fig.savefig(path, dpi=200)
    plt.close(fig)


def figure6(en, path):
    d = en.copy()
    d["feeder"] = d.code.map(short)

    fig, (ax, bx) = plt.subplots(1, 2, figsize=(11, 4.6))
    for feeder, g in d.groupby("feeder"):
        g = g.sort_values("size_kW")
        c = FEEDER_COLOR.get(feeder, "#444444")
        ax.plot(g.size_kW, g.E_avail_MWh, color=c, linestyle="--", linewidth=1.2, marker="o",
                markersize=4, markerfacecolor="white", label=f"{feeder}  available")
        ax.plot(g.size_kW, g.E_vw_MWh, color=c, linewidth=1.8, marker="o", markersize=5,
                label=f"{feeder}  delivered (Volt-Watt)")
        bx.plot(g.size_kW, g["curtailed_%"], color=c, linewidth=1.8, marker="o", markersize=5,
                label=feeder)
        for _, r in g.iterrows():
            if r.volt_h_nc > 0:
                bx.annotate(f"{int(r.volt_h_nc)} h", (r.size_kW, r["curtailed_%"]),
                            textcoords="offset points", xytext=(-6, 6), ha="right",
                            fontsize=8, color=c)
    ax.set_xlabel("Nameplate of the added PV (kW)")
    ax.set_ylabel("Annual energy (MWh)")
    ax.set_title("(a) Available (dashed) and delivered (solid) energy", loc="left", fontsize=10)
    ax.legend(fontsize=8, loc="upper left")
    bx.set_xlabel("Nameplate of the added PV (kW)")
    bx.set_ylabel("Energy curtailed by Volt-Watt (%)")
    bx.set_title("(b) Curtailment; labels: hours/year above 1.05 pu without control",
                 loc="left", fontsize=10)
    bx.legend(fontsize=9, loc="upper left")
    fig.tight_layout()
    fig.savefig(path, dpi=200)
    plt.close(fig)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--results", default="results")
    ap.add_argument("--snap", default=None)
    ap.add_argument("--hc", default=None)
    ap.add_argument("--energy", default=None)
    a = ap.parse_args()
    snap_p = a.snap or os.path.join(a.results, "multi_feeder_snapshot.csv")
    hc_p = a.hc or os.path.join(a.results, "timeseries_hc.csv")
    en_p = a.energy or os.path.join(a.results, "timeseries_energy.csv")

    if os.path.exists(snap_p):
        figure4(pd.read_csv(snap_p), os.path.join(a.results, "fig4_effect_vs_ratio.png"))
        print("written fig4_effect_vs_ratio.png")
    else:
        print("missing", snap_p)
    if os.path.exists(hc_p):
        figure5(pd.read_csv(hc_p), os.path.join(a.results, "fig5_snapshot_vs_timeseries.png"))
        print("written fig5_snapshot_vs_timeseries.png")
    else:
        print("missing", hc_p)
    if os.path.exists(en_p):
        figure6(pd.read_csv(en_p), os.path.join(a.results, "fig6_energy_curtailment.png"))
        print("written fig6_energy_curtailment.png")
    else:
        print("missing", en_p)


if __name__ == "__main__":
    main()
