import simbench as sb
import pandapower as pp

# Network loading
net = sb.get_simbench_net("1-LV-rural1--0-sw")

# Running Load Flow
pp.runpp(net)

# Resulting voltages
print("=== Bus Voltages (per-unit) ===")
print(net.res_bus.vm_pu)

# Network topology
print("\n=== Network Topology ===")
print("Number of buses:", len(net.bus))
print("Number of lines:", len(net.line))
print("Number of transformers:", len(net.trafo))
print("Number of loads:", len(net.load))
print("Total load (kW):", net.load.p_mw.sum() * 1000)