import simbench as sb
import pandapower as pp
import pandas as pd
import copy

VOLTAGE_LIMIT = 1.05
LOADING_LIMIT = 100.0   # Allowed loading percentage of line/transformer
MAX_KW = 1000.0
TOLERANCE_KW = 1.0      #  (Binary search precision) or (Allowed tolerance for binary search )

V1, V2, V3, V4 = 0.92, 0.98, 1.02, 1.08
Q1, Q2, Q3, Q4 = 0.44, 0.0, 0.0, -0.44

def volt_var_q(voltage_pu, inverter_kva):
    if voltage_pu <= V1:
        q_ratio = Q1
    elif voltage_pu <= V2:
        q_ratio = Q1 + (Q2 - Q1) * (voltage_pu - V1) / (V2 - V1)
    elif voltage_pu <= V3:
        q_ratio = Q2
    elif voltage_pu <= V4:
        q_ratio = Q3 + (Q4 - Q3) * (voltage_pu - V3) / (V4 - V3)
    else:
        q_ratio = Q4
    return q_ratio * inverter_kva

def is_feasible(base_net, bus, pv_kw):
    """ Checks whether this PV value is permissible in terms of both voltage and heat"""
    net_test = copy.deepcopy(base_net)
    sgen_idx = pp.create_sgen(net_test, bus=bus, p_mw=pv_kw / 1000, q_mvar=0, name="PV_test")

    for _ in range(10):
        try:
            pp.runpp(net_test)
        except:
            return False
        v_bus = net_test.res_bus.vm_pu.at[bus]
        q_kvar = volt_var_q(v_bus, pv_kw)
        net_test.sgen.at[sgen_idx, "q_mvar"] = q_kvar / 1000

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

df_voltvar = pd.DataFrame(results).sort_values("hosting_capacity_kW")
print("\n=== PV Hosting Capacity WITH Volt-VAr (Voltage + Thermal Limits) ===")
print(df_voltvar.to_string(index=False))

df_baseline = pd.read_csv("results/hosting_capacity_baseline.csv")
comparison = df_baseline.merge(df_voltvar, on="bus", suffixes=("_baseline", "_voltvar"))
comparison["improvement_kW"] = comparison["hosting_capacity_kW_voltvar"] - comparison["hosting_capacity_kW_baseline"]
comparison["improvement_%"] = (comparison["improvement_kW"] / comparison["hosting_capacity_kW_baseline"] * 100).round(1)

print("\n=== Comparing Baseline versus Volt-VAR ===")
print(comparison.to_string(index=False))

comparison.to_csv("results/hosting_capacity_comparison.csv", index=False)