import simbench as sb
import pandapower as pp
import pandas as pd
import copy

VOLTAGE_LIMIT = 1.05
LOADING_LIMIT = 100.0
MAX_KW = 1000.0
TOLERANCE_KW = 1.0

VW1, VW2 = 1.06, 1.10
PW1, PW2 = 1.0, 0.2

def volt_watt_p_ratio(voltage_pu):
    if voltage_pu <= VW1:
        return PW1
    elif voltage_pu <= VW2:
        return PW1 + (PW2 - PW1) * (voltage_pu - VW1) / (VW2 - VW1)
    else:
        return PW2

def is_feasible(base_net, bus, pv_kw):
    net_test = copy.deepcopy(base_net)
    sgen_idx = pp.create_sgen(net_test, bus=bus, p_mw=pv_kw / 1000, q_mvar=0)

    current_p = pv_kw
    DAMPING = 0.3

    for _ in range(30):
        try:
            pp.runpp(net_test)
        except:
            return False
        v_bus = net_test.res_bus.vm_pu.at[bus]
        ratio = volt_watt_p_ratio(v_bus)
        target_p = pv_kw * ratio
        current_p = current_p + DAMPING * (target_p - current_p)
        net_test.sgen.at[sgen_idx, "p_mw"] = current_p / 1000

    if net_test.res_bus.vm_pu.max() > VOLTAGE_LIMIT:
        return False
    if len(net_test.res_line) and net_test.res_line.loading_percent.max() > LOADING_LIMIT:
        return False
    if len(net_test.res_trafo) and net_test.res_trafo.loading_percent.max() > LOADING_LIMIT:
        return False
    return True

base_net = sb.get_simbench_net("1-LV-rural1--0-sw")
load_buses = base_net.load.bus.unique()
results = []

for bus in load_buses:
    low, high = 0.0, MAX_KW
    while high - low > TOLERANCE_KW:
        mid = (low + high) / 2
        if is_feasible(base_net, bus, mid):
            low = mid
        else:
            high = mid
    results.append({"bus": bus, "hosting_capacity_kW": round(low, 1)})
    print(f"Bus {bus} completed — Capacity: {round(low,1)} kW")

df_voltwatt = pd.DataFrame(results).sort_values("hosting_capacity_kW")
print("\n=== PV Hosting Capacity WITH Volt-Watt (Voltage + Thermal Limits) ===")
print(df_voltwatt.to_string(index=False))

df_voltvar = pd.read_csv("results/hosting_capacity_comparison.csv")[["bus", "hosting_capacity_kW_voltvar"]]
df_baseline = pd.read_csv("results/hosting_capacity_baseline.csv")

comparison = df_baseline.merge(df_voltvar, on="bus").merge(df_voltwatt, on="bus")
comparison.columns = ["bus", "baseline_kW", "voltvar_kW", "voltwatt_kW"]
print("\n=== Three-way comparison: Baseline vs Volt-VAr vs Volt-Watt ===")
print(comparison.to_string(index=False))

comparison.to_csv("results/hosting_capacity_full_comparison.csv", index=False)