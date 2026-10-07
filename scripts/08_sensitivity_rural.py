import simbench as sb
import pandapower as pp
import pandas as pd
import copy

LOADING_LIMIT = 100.0
MAX_KW = 2000.0
TOL_KW = 0.1

def thermal_ok(net):
    return (net.res_line.loading_percent.max() <= LOADING_LIMIT and
            net.res_trafo.loading_percent.max() <= LOADING_LIMIT)

def vw_ratio(v, vw1, vw2, pw2=0.2):
    if v <= vw1:
        return 1.0
    if v >= vw2:
        return pw2
    return 1.0 + (pw2 - 1.0) * (v - vw1) / (vw2 - vw1)

def vvar_q_ratio(v):
    V1, V2, V3, V4 = 0.92, 0.98, 1.02, 1.08
    if v <= V1:
        return 0.44
    if v <= V2:
        return 0.44 * (V2 - v) / (V2 - V1)
    if v <= V3:
        return 0.0
    if v <= V4:
        return -0.44 * (v - V3) / (V4 - V3)
    return -0.44

def run_no_control(base, bus, kw):
    net = copy.deepcopy(base)
    pp.create_sgen(net, bus=bus, p_mw=kw / 1000, q_mvar=0)
    pp.runpp(net)
    return net, kw

def run_volt_var(base, bus, kw):
    net = copy.deepcopy(base)
    idx = pp.create_sgen(net, bus=bus, p_mw=kw / 1000, q_mvar=0)
    q_prev = 0.0
    for _ in range(20):
        pp.runpp(net)
        q = vvar_q_ratio(net.res_bus.vm_pu.at[bus]) * kw
        net.sgen.at[idx, "q_mvar"] = q / 1000
        if abs(q - q_prev) < 0.1:
            break
        q_prev = q
    else:
        raise RuntimeError("Volt-VAr did not converge")
    pp.runpp(net)
    return net, kw

def make_volt_watt(vw1, vw2):
    def run(base, bus, kw):
        net = copy.deepcopy(base)
        idx = pp.create_sgen(net, bus=bus, p_mw=0.0, q_mvar=0)

        def residual(p):
            net.sgen.at[idx, "p_mw"] = p / 1000
            pp.runpp(net)
            return kw * vw_ratio(net.res_bus.vm_pu.at[bus], vw1, vw2) - p

        if residual(kw) >= 0:
            return net, kw          # no curtailment needed at full output
        lo, hi = 0.0, kw
        while hi - lo > 0.1:
            mid = (lo + hi) / 2
            if residual(mid) > 0:
                lo = mid
            else:
                hi = mid
        residual(lo)                # leave the network at the equilibrium point
        return net, lo
    return run

def hosting_capacity(base, bus, runner, v_limit):
    lo, hi, delivered = 0.0, MAX_KW, 0.0
    while hi - lo > TOL_KW:
        mid = (lo + hi) / 2
        try:
            net, p = runner(base, bus, mid)
            ok = net.res_bus.vm_pu.max() <= v_limit and thermal_ok(net)
        except Exception:
            ok = False
        if ok:
            lo, delivered = mid, p
        else:
            hi = mid
    return round(lo, 1), round(delivered, 1)

scenarios = {
    "NC_1.05":         (run_no_control, 1.05),
    "VVAR_1.05":       (run_volt_var, 1.05),
    "VW_default_1.05": (make_volt_watt(1.06, 1.10), 1.05),
    "VW_adapted_1.05": (make_volt_watt(1.03, 1.05), 1.05),
    "NC_1.10":         (run_no_control, 1.10),
    "VVAR_1.10":       (run_volt_var, 1.10),
    "VW_default_1.10": (make_volt_watt(1.06, 1.10), 1.10),
}

base = sb.get_simbench_net("1-LV-rural1--0-sw")
buses = sorted(base.load.bus.unique())
rows = []
for name, (runner, vlim) in scenarios.items():
    print(f"Running {name} ...")
    for bus in buses:
        hc, p = hosting_capacity(base, bus, runner, vlim)
        rows.append({"scenario": name, "bus": bus, "nameplate_kW": hc, "delivered_kW": p})

df = pd.DataFrame(rows)
df.to_csv("results/sensitivity_rural.csv", index=False, encoding="utf-8")
print("\n=== Nameplate hosting capacity (kW) ===")
print(df.pivot(index="bus", columns="scenario", values="nameplate_kW").to_string())
print("\n=== Delivered active power at that nameplate (kW) ===")
print(df.pivot(index="bus", columns="scenario", values="delivered_kW").to_string())