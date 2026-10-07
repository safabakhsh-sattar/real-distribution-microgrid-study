import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import simbench as sb
import pandapower.topology as top

# ---------- Style (fixed colour per control strategy across all figures) ----------
C_NC, C_VVAR, C_VWA = "#2a78d6", "#eb6834", "#4a3aa7"   # no control, Volt-VAr, Volt-Watt adapted
C_VWA_LIGHT = "#cfc9ee"                                  # light tint of Volt-Watt adapted (nameplate)
INK, MUTED, GRID = "#0b0b0b", "#52514e", "#e4e3df"

plt.rcParams.update({
    "font.size": 10, "text.color": INK, "axes.labelcolor": INK,
    "axes.spines.top": False, "axes.spines.right": False, "axes.edgecolor": "#9a9993",
    "xtick.color": MUTED, "ytick.color": MUTED,
    "axes.grid": True, "grid.color": GRID, "grid.linewidth": 0.6, "axes.axisbelow": True,
    "legend.frameon": False,
})


def load_sensitivity(path):
    df = pd.read_csv(path)
    nameplate = df.pivot(index="bus", columns="scenario", values="nameplate_kW")
    delivered = df.pivot(index="bus", columns="scenario", values="delivered_kW")
    return nameplate, delivered


def pct_vs_nc(delivered, scenario):
    return (delivered[scenario] / delivered["NC_1.05"] - 1.0) * 100.0


# ---------- Data ----------
rural_np, rural_dl = load_sensitivity("results/sensitivity_rural.csv")
urban_np, urban_dl = load_sensitivity("results/sensitivity_urban.csv")

net = sb.get_simbench_net("1-LV-rural1--0-sw")
dist_km = top.calc_distance_to_bus(net, net.trafo.lv_bus.iloc[0])

# ---------- Figure 1: Rural feeder (sensitivity analysis) ----------
order = dist_km[rural_dl.index].sort_values().index          # nearest -> farthest from transformer
x = np.arange(len(order))
labels = [str(int(b)) for b in order]

fig, (axa, axb) = plt.subplots(2, 1, figsize=(10, 8), sharex=True)

# (a) delivered capacity relative to no control
w = 0.38
vvar = pct_vs_nc(rural_dl, "VVAR_1.05").loc[order]
vwa = pct_vs_nc(rural_dl, "VW_adapted_1.05").loc[order]
axa.bar(x - w / 2, vvar, w, color=C_VVAR, edgecolor="white", linewidth=0.8, label="Volt-VAr")
axa.bar(x + w / 2, vwa, w, color=C_VWA, edgecolor="white", linewidth=0.8, label="Volt-Watt (adapted, 1.03-1.05 pu)")
axa.axhline(0, color=INK, linewidth=1.0)
axa.set_ylabel("Delivered capacity vs no control (%)")
axa.set_title("(a) Delivered hosting capacity relative to no control", loc="left", fontsize=10)
axa.legend(loc="upper right", fontsize=9, ncol=2)
i_min, i_max = vvar.values.argmin(), vvar.values.argmax()
for i in (i_min, i_max):
    axa.annotate(f"{vvar.values[i]:.1f}%", (i - w / 2, vvar.values[i]), textcoords="offset points",
                 xytext=(0, -11), ha="center", fontsize=8, color=INK)
axa.text(0.01, 0.06, "Volt-Watt default curve = no control (0%) at every bus (not drawn)",
         transform=axa.transAxes, fontsize=8, color=MUTED)
axa.set_ylim(min(vvar.min(), vwa.min()) - 1.0, 1.6)

# (b) nameplate vs delivered capacity, Volt-Watt adapted
nameplate = rural_np["VW_adapted_1.05"].loc[order]
delivered = rural_dl["VW_adapted_1.05"].loc[order]
axb.bar(x, nameplate, 0.72, color=C_VWA_LIGHT, edgecolor=C_VWA, linewidth=0.8,
        label="Nameplate hosting capacity")
axb.bar(x, delivered, 0.40, color=C_VWA, edgecolor="white", linewidth=0.8,
        label="Delivered active power")
axb.plot(x, rural_dl["NC_1.05"].loc[order], linestyle="none", marker="o", markersize=5,
         markerfacecolor=C_NC, markeredgecolor="white", markeredgewidth=1.0,
         label="No control (reference)")
for i in (0, len(order) - 2, len(order) - 1):
    ratio = nameplate.values[i] / delivered.values[i]
    axb.annotate(f"{ratio:.1f}x", (i, nameplate.values[i]), textcoords="offset points",
                 xytext=(0, 4), ha="center", fontsize=9)
axb.set_ylabel("Hosting capacity (kW)")
axb.set_xlabel("Bus (ordered by distance from transformer, nearest to farthest)")
axb.set_title("(b) Volt-Watt (adapted): nameplate vs delivered", loc="left", fontsize=10)
axb.legend(loc="upper left", fontsize=9)
axb.set_ylim(0, nameplate.max() * 1.12)
axb.set_xticks(x)
axb.set_xticklabels(labels)
for a in (axa, axb):
    a.grid(axis="x", visible=False)

plt.tight_layout()
plt.savefig("results/fig1_rural_comparison.png", dpi=300)
plt.close()

# ---------- Figure 2: Urban feeder (sensitivity analysis) ----------
order_u = urban_dl["NC_1.05"].sort_values().index             # sorted by no-control capacity
xu = np.arange(len(order_u))

fig, (axa, axb) = plt.subplots(2, 1, figsize=(10, 8), sharex=True)

vvar_u = pct_vs_nc(urban_dl, "VVAR_1.05").loc[order_u]
vwa_u = pct_vs_nc(urban_dl, "VW_adapted_1.05").loc[order_u]
axa.axhline(0, color=INK, linewidth=1.0)
axa.plot(xu, vvar_u, linestyle="none", marker="o", markersize=6, markerfacecolor=C_VVAR,
         markeredgecolor="white", markeredgewidth=1.0, label="Volt-VAr")
axa.plot(xu, vwa_u, linestyle="none", marker="^", markersize=6, markerfacecolor=C_VWA,
         markeredgecolor="white", markeredgewidth=1.0, label="Volt-Watt (adapted, 1.03-1.05 pu)")
axa.set_ylabel("Delivered capacity vs no control (%)")
axa.set_title("(a) Delivered hosting capacity relative to no control", loc="left", fontsize=10)
axa.legend(loc="lower right", fontsize=9)
j = vvar_u.values.argmin()
axa.annotate(f"{vvar_u.values[j]:.1f}%", (j, vvar_u.values[j]), textcoords="offset points",
             xytext=(8, -3), ha="left", fontsize=8)
axa.text(0.01, 0.06, "Volt-Watt default curve = no control (0%) at every bus (not drawn)",
         transform=axa.transAxes, fontsize=8, color=MUTED)
axa.set_ylim(min(vvar_u.min(), vwa_u.min()) - 0.5, 0.5)

axb.plot(xu, urban_dl["NC_1.05"].loc[order_u], color=C_NC, linewidth=2, label="No control (delivered)")
axb.plot(xu, urban_np["VW_adapted_1.05"].loc[order_u], color=C_VWA, linewidth=2, linestyle="--",
         marker="^", markersize=4, markerfacecolor=C_VWA, markeredgecolor="white",
         label="Volt-Watt (adapted), nameplate")
axb.set_ylabel("Hosting capacity (kW)")
axb.set_xlabel("Bus rank (ordered by no-control capacity, lowest to highest)")
axb.set_title("(b) No-control capacity vs Volt-Watt (adapted) nameplate", loc="left", fontsize=10)
axb.legend(loc="upper left", fontsize=9)
axb.set_ylim(0, urban_np["VW_adapted_1.05"].max() * 1.08)
for a in (axa, axb):
    a.grid(axis="x", visible=False)

plt.tight_layout()
plt.savefig("results/fig2_urban_comparison.png", dpi=300)
plt.close()

# ---------- Figure 3: Path length vs capacity (rural), unchanged ----------
rural = pd.read_csv("results/hosting_capacity_full_comparison.csv")
rural_th = pd.read_csv("results/rural_baseline_thermal.csv").rename(
    columns={"hosting_capacity_kW": "baseline_thermal_kW"})
rural = rural.merge(rural_th, on="bus").sort_values("baseline_kW").reset_index(drop=True)
rural["distance_km"] = rural["bus"].map(dist_km)

fig, ax = plt.subplots(figsize=(7, 5))
ax.scatter(rural["distance_km"], rural["baseline_kW"], label="Voltage limit only")
ax.scatter(rural["distance_km"], rural["baseline_thermal_kW"], marker="x", label="Voltage + thermal")
for _, r in rural.iterrows():
    ax.annotate(int(r["bus"]), (r["distance_km"], r["baseline_kW"]),
                textcoords="offset points", xytext=(4, 4), fontsize=8)
ax.set_xlabel("Feeder path length from transformer (km)")
ax.set_ylabel("Hosting capacity (kW)")
ax.set_title("Rural feeder: distance vs hosting capacity")
ax.legend()
plt.tight_layout()
plt.savefig("results/fig3_distance_vs_capacity.png", dpi=300)
plt.close()

print("Saved: fig1_rural_comparison.png, fig2_urban_comparison.png, fig3_distance_vs_capacity.png")