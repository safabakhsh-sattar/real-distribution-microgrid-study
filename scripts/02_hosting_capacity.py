import simbench as sb
import pandapower as pp
import pandas as pd
import copy

# --- Settings ---
VOLTAGE_LIMIT = 1.05  # Voltage limit (pu)
STEP_KW = 1.0
MAX_KW = 300.0

# --- Base network loading (only once) ---
base_net = sb.get_simbench_net("1-LV-rural1--0-sw")

results = []
load_buses = base_net.load.bus.unique()

for bus in load_buses:
    hosting_capacity = 0.0
    pv_kw = 0.0

    while pv_kw < MAX_KW:
        pv_kw += STEP_KW

        # Fast copy into memory, without re-reading from the file
        net_test = copy.deepcopy(base_net)
        pp.create_sgen(net_test, bus=bus, p_mw=pv_kw / 1000, q_mvar=0, name="PV_test")

        try:
            pp.runpp(net_test)
            max_voltage = net_test.res_bus.vm_pu.max()
        except:
            break

        if max_voltage > VOLTAGE_LIMIT:
            break

        hosting_capacity = pv_kw

    results.append({"bus": bus, "hosting_capacity_kW": hosting_capacity})
    print(f"Bus {bus} completed — Capacity: {hosting_capacity} kW")  # For viewing progress

df = pd.DataFrame(results).sort_values("hosting_capacity_kW")

print("\n=== PV Hosting Capacity for Each Bus ===")
print(df.to_string(index=False))
print(f"\n Minimum Network Capacity (Critical Bus): {df.iloc[0]['bus']} with {df.iloc[0]['hosting_capacity_kW']} kW")


# فاصله الکتریکی هر باس تا ترانس (بر حسب امپدانس خط)
import pandapower.topology as top

dist = top.calc_distance_to_bus(base_net, base_net.trafo.lv_bus.iloc[0])
print(dist.sort_values(ascending=False))