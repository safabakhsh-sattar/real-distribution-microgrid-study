import simbench as sb
import pandapower as pp
import pandas as pd
import copy

VOLTAGE_LIMIT = 1.05
LOADING_LIMIT = 100.0
MAX_KW = 1000.0
TOLERANCE_KW = 1.0

def is_feasible(base_net, bus, pv_kw):
    net = copy.deepcopy(base_net)
    pp.create_sgen(net, bus=bus, p_mw=pv_kw / 1000, q_mvar=0)
    try:
        pp.runpp(net)
    except Exception:
        return False
    if net.res_bus.vm_pu.max() > VOLTAGE_LIMIT:
        return False
    if net.res_line.loading_percent.max() > LOADING_LIMIT:
        return False
    if net.res_trafo.loading_percent.max() > LOADING_LIMIT:
        return False
    return True

base_net = sb.get_simbench_net("1-LV-rural1--0-sw")
print("Line types:", base_net.line.std_type.unique())

results = []
for bus in base_net.load.bus.unique():
    low, high = 0.0, MAX_KW
    while high - low > TOLERANCE_KW:
        mid = (low + high) / 2
        if is_feasible(base_net, bus, mid):
            low = mid
        else:
            high = mid
    results.append({"bus": bus, "hosting_capacity_kW": round(low, 1)})

df = pd.DataFrame(results)
df.to_csv("results/rural_baseline_thermal.csv", index=False, encoding="utf-8")

full = pd.read_csv("results/hosting_capacity_full_comparison.csv")
full = full.merge(df.rename(columns={"hosting_capacity_kW": "baseline_thermal_kW"}), on="bus")
print(full[["bus", "baseline_kW", "baseline_thermal_kW", "voltvar_kW", "voltwatt_kW"]]
      .sort_values("baseline_kW").to_string(index=False))