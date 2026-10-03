import simbench as sb
import pandapower as pp
import pandas as pd
import copy

VOLTAGE_LIMIT = 1.05
LOADING_LIMIT = 100.0
MAX_KW = 500.0
TOLERANCE_KW = 1.0

# --- Volt-VAr curve (IEEE 1547-2018) ---
V1, V2, V3, V4 = 0.92, 0.98, 1.02, 1.08
Q1, Q2, Q3, Q4 = 0.44, 0.0, 0.0, -0.44

def volt_var_q(voltage_pu, inverter_kva):
    if voltage_pu <= V1:
        ratio = Q1
    elif voltage_pu <= V2:
        ratio = Q1 + (Q2 - Q1) * (voltage_pu - V1) / (V2 - V1)
    elif voltage_pu <= V3:
        ratio = Q2
    elif voltage_pu <= V4:
        ratio = Q3 + (Q4 - Q3) * (voltage_pu - V3) / (V4 - V3)
    else:
        ratio = Q4
    return ratio * inverter_kva

# --- Volt-Watt curve (IEEE 1547-2018) ---
VW1, VW2 = 1.06, 1.10
PW1, PW2 = 1.0, 0.2

def volt_watt_p_ratio(voltage_pu):
    if voltage_pu <= VW1:
        return PW1
    elif voltage_pu <= VW2:
        return PW1 + (PW2 - PW1) * (voltage_pu - VW1) / (VW2 - VW1)
    else:
        return PW2

def check_limits(net_test, bus):
    if net_test.res_bus.vm_pu.max() > VOLTAGE_LIMIT:
        return False
    if len(net_test.res_line) and net_test.res_line.loading_percent.max() > LOADING_LIMIT:
        return False
    if len(net_test.res_trafo) and net_test.res_trafo.loading_percent.max() > LOADING_LIMIT:
        return False
    return True

def is_feasible_voltvar(base_net, bus, pv_kw):
    net_test = copy.deepcopy(base_net)
    sgen_idx = pp.create_sgen(net_test, bus=bus, p_mw=pv_kw / 1000, q_mvar=0)
    for _ in range(10):
        try:
            pp.runpp(net_test)
        except:
            return False
        v_bus = net_test.res_bus.vm_pu.at[bus]
        q_kvar = volt_var_q(v_bus, pv_kw)
        net_test.sgen.at[sgen_idx, "q_mvar"] = q_kvar / 1000
    return check_limits(net_test, bus)

def is_feasible_voltwatt(base_net, bus, pv_kw):
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
    return check_limits(net_test, bus)

def binary_search_capacity(base_net, bus, feasibility_fn):
    low, high = 0.0, MAX_KW
    while high - low > TOLERANCE_KW:
        mid = (low + high) / 2
        if feasibility_fn(base_net, bus, mid):
            low = mid
        else:
            high = mid
    return round(low, 1)

base_net = sb.get_simbench_net("1-LV-urban6--0-sw")
load_buses = base_net.load.bus.unique()

results_var, results_watt = [], []

for bus in load_buses:
    cap_var = binary_search_capacity(base_net, bus, is_feasible_voltvar)
    cap_watt = binary_search_capacity(base_net, bus, is_feasible_voltwatt)
    results_var.append({"bus": bus, "voltvar_kW": cap_var})
    results_watt.append({"bus": bus, "voltwatt_kW": cap_watt})
    print(f"Bus {bus} — VAr: {cap_var} kW | Watt: {cap_watt} kW")

df_var = pd.DataFrame(results_var)
df_watt = pd.DataFrame(results_watt)
df_baseline = pd.read_csv("results/validation_urban_feeder.csv").rename(
    columns={"hosting_capacity_kW": "baseline_kW"})

comparison = df_baseline.merge(df_var, on="bus").merge(df_watt, on="bus")
comparison["watt_vs_var_improvement_%"] = (
    (comparison["voltwatt_kW"] - comparison["voltvar_kW"]) / comparison["voltvar_kW"] * 100
).round(1)

print("\n=== Urban Feeder: Baseline vs Volt-VAr vs Volt-Watt ===")
print(comparison.sort_values("baseline_kW").to_string(index=False))
print(f"\nVolt-Watt outperformed Volt-VAr in {(comparison['voltwatt_kW'] >= comparison['voltvar_kW']).sum()} of {len(comparison)} buses")

comparison.to_csv("results/urban_full_comparison.csv", index=False)