import simbench as sb
import pandapower as pp
import pandas as pd
import copy

VOLTAGE_LIMIT = 1.05
LOADING_LIMIT = 100.0
MAX_KW = 500.0
TOLERANCE_KW = 1.0

def is_feasible(base_net, bus, pv_kw):
    net_test = copy.deepcopy(base_net)
    sgen_idx = pp.create_sgen(net_test, bus=bus, p_mw=pv_kw / 1000, q_mvar=0)
    try:
        pp.runpp(net_test)
    except:
        return False
    if net_test.res_bus.vm_pu.max() > VOLTAGE_LIMIT:
        return False
    if len(net_test.res_line) and net_test.res_line.loading_percent.max() > LOADING_LIMIT:
        return False
    if len(net_test.res_trafo) and net_test.res_trafo.loading_percent.max() > LOADING_LIMIT:
        return False
    return True

# Second feeder: urban (unlike the first feeder, which was rural)
base_net = sb.get_simbench_net("1-LV-urban6--0-sw")
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

df = pd.DataFrame(results).sort_values("hosting_capacity_kW")
print("=== Urban Feeder Hosting Capacity (Voltage + Thermal) ===")
print(df.to_string(index=False))
print(f"\nTransformer loading at min capacity bus:")

# Check transformer loading at minimum capacity
min_bus = int(df.iloc[0]["bus"])
min_cap = df.iloc[0]["hosting_capacity_kW"]
net_check = copy.deepcopy(base_net)
pp.create_sgen(net_check, bus=min_bus, p_mw=min_cap/1000, q_mvar=0)
pp.runpp(net_check)
print(f"Bus {min_bus}: Trafo loading = {net_check.res_trafo.loading_percent.values[0]:.1f}%, "
      f"Max line loading = {net_check.res_line.loading_percent.max():.1f}%")

df.to_csv("results/validation_urban_feeder.csv", index=False)