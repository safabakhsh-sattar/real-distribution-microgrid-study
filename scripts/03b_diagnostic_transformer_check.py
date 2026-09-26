import simbench as sb
import pandapower as pp
import copy

base_net = sb.get_simbench_net("1-LV-rural1--0-sw")
bus = 7
pv_kw = 80.0

net_test = copy.deepcopy(base_net)
pp.create_sgen(net_test, bus=bus, p_mw=pv_kw / 1000, q_mvar=0, name="PV_test")
pp.runpp(net_test)

print("=== Loading of Lines (Percentage) ===")
print(net_test.res_line[["loading_percent"]].sort_values("loading_percent", ascending=False).head(5))

print("\n=== Transformer Loading (Percentage) ===")
print(net_test.res_trafo[["loading_percent"]])

print("\n=== Nominal capacity of lines (Amperes) ===")
print(net_test.line[["max_i_ka", "length_km"]])