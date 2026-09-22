import simbench as sb
import pandapower as pp
import pandas as pd
import numpy as np
import copy

# --- Settings ---
VOLTAGE_LIMIT = 1.05
STEP_KW = 1.0
MAX_KW = 300.0

# Standard Volt-VAr curve according to IEEE 1547-2018 (points V1-V4 and Q1-Q4)
# Voltage unit: per-unit | Reactive power unit: relative to the inverter's rated capacity (pu)
V1, V2, V3, V4 = 0.92, 0.98, 1.02, 1.08
Q1, Q2, Q3, Q4 = 0.44, 0.0, 0.0, -0.44  # +Q = تزریق راکتیو (ساپورت ولتاژ), -Q = جذب راکتیو

def volt_var_q(voltage_pu, inverter_kva):
    """Calculation of reactive power based on current voltage, according to the Volt-VAr curve"""
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

# ---Base network loading---
base_net = sb.get_simbench_net("1-LV-rural1--0-sw")
load_buses = base_net.load.bus.unique()

results = []

for bus in load_buses:
    hosting_capacity = 0.0
    pv_kw = 0.0

    while pv_kw < MAX_KW:
        pv_kw += STEP_KW

        net_test = copy.deepcopy(base_net)
        # First, we add with q=0, then in the repetition loop, we correct Q according to the current voltage.
        sgen_idx = pp.create_sgen(net_test, bus=bus, p_mw=pv_kw / 1000, q_mvar=0, name="PV_test")

        # Iteration loop for Volt-VAr convergence (because Q depends on voltage and voltage depends on Q)
        converged = True
        for _ in range(10):  # Maximum 10 iterations for convergence
            try:
                pp.runpp(net_test)
            except:
                converged = False
                break
            v_bus = net_test.res_bus.vm_pu.at[bus]
            q_new_kvar = volt_var_q(v_bus, pv_kw)  # Assumption: Inverter capacity = pv_kw
            net_test.sgen.at[sgen_idx, "q_mvar"] = q_new_kvar / 1000

        if not converged:
            break

        max_voltage = net_test.res_bus.vm_pu.max()
        if max_voltage > VOLTAGE_LIMIT:
            break

        hosting_capacity = pv_kw

    results.append({"bus": bus, "hosting_capacity_kW": hosting_capacity})
    print(f"Bus {bus} completed — Capacity: {hosting_capacity} kW")

df_voltvar = pd.DataFrame(results).sort_values("hosting_capacity_kW")

print("\n=== PV Hosting Capacity WITH Volt-VAr Control ===")
print(df_voltvar.to_string(index=False))

# --- Comparison with baseline (uncontrolled) ---
df_baseline = pd.read_csv("results/hosting_capacity_baseline.csv")
comparison = df_baseline.merge(df_voltvar, on="bus", suffixes=("_baseline", "_voltvar"))
comparison["improvement_kW"] = comparison["hosting_capacity_kW_voltvar"] - comparison["hosting_capacity_kW_baseline"]
comparison["improvement_%"] = (comparison["improvement_kW"] / comparison["hosting_capacity_kW_baseline"] * 100).round(1)

print("\n=== Comparing Baseline versus Volt-VAr ===")
print(comparison.to_string(index=False))

comparison.to_csv("results/hosting_capacity_comparison.csv", index=False)