import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import simbench as sb
import pandapower.topology as top

# ---------- Data ----------
rural = pd.read_csv("results/hosting_capacity_full_comparison.csv")
rural_th = pd.read_csv("results/rural_baseline_thermal.csv").rename(
    columns={"hosting_capacity_kW": "baseline_thermal_kW"})
rural = rural.merge(rural_th, on="bus").sort_values("baseline_kW").reset_index(drop=True)
urban = pd.read_csv("results/urban_full_comparison.csv").sort_values("baseline_kW").reset_index(drop=True)

# ---------- Figure 1: Rural feeder, four cases ----------
x = np.arange(len(rural))
w = 0.2
fig, ax = plt.subplots(figsize=(11, 5))
ax.bar(x - 1.5 * w, rural["baseline_kW"], w, label="No control (voltage limit only)")
ax.bar(x - 0.5 * w, rural["baseline_thermal_kW"], w, label="No control (voltage + thermal)")
ax.bar(x + 0.5 * w, rural["voltvar_kW"], w, label="Volt-VAr (voltage + thermal)")
ax.bar(x + 1.5 * w, rural["voltwatt_kW"], w, label="Volt-Watt (voltage + thermal)")
ax.set_xticks(x)
ax.set_xticklabels(rural["bus"])
ax.set_xlabel("Bus")
ax.set_ylabel("Hosting capacity (kW)")
ax.set_title("Rural feeder (1-LV-rural1): hosting capacity by control strategy")
ax.legend(fontsize=8)
plt.tight_layout()
plt.savefig("results/fig1_rural_comparison.png", dpi=300)
plt.close()

# ---------- Figure 2: Urban feeder, three cases ----------
xu = np.arange(len(urban))
fig, ax = plt.subplots(figsize=(13, 5))
ax.plot(xu, urban["baseline_kW"], marker="o", markersize=3, label="No control")
ax.plot(xu, urban["voltvar_kW"], marker="s", markersize=3, label="Volt-VAr")
ax.plot(xu, urban["voltwatt_kW"], marker="^", markersize=3, label="Volt-Watt")
ax.set_xlabel("Bus (sorted by no-control capacity)")
ax.set_ylabel("Hosting capacity (kW)")
ax.set_title("Urban feeder (1-LV-urban6): voltage + thermal constraints, 53 buses")
ax.legend()
plt.tight_layout()
plt.savefig("results/fig2_urban_comparison.png", dpi=300)
plt.close()

# ---------- Figure 3: Path length vs capacity (rural) ----------
net = sb.get_simbench_net("1-LV-rural1--0-sw")
dist_km = top.calc_distance_to_bus(net, net.trafo.lv_bus.iloc[0])
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