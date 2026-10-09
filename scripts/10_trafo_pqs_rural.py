"""Script 10: direct measurement of transformer P, Q and S with and without Volt-VAr.

Question: script 08 shows that default Volt-VAr LOWERS the hosting capacity on the
rural feeder (13 of 13 buses). The proposed reason is that the inverter absorbs
reactive power, the transformer must then carry that reactive power on top of the
active power, its apparent power S = sqrt(P^2 + Q^2) rises, and the 100% thermal
limit is reached at a smaller PV size. This script measures P, Q and S at the
transformer to test that explanation directly.

Note on the loading figure: pandapower's default trafo_loading="current" gives
loading_percent = max(I_hv/I_n_hv, I_lv/I_n_lv) x 100, i.e. it is CURRENT-based, not
apparent-power-based. Because I = S / (sqrt(3) V), a loading of 100% at an LV
voltage of about 1.03 pu corresponds to S of about 103% of the nameplate rating.
Both numbers are reported below (S_over_Sn_pct and trafo_loading_pct).

Three cases per load bus (1.05 pu voltage limit, 100% thermal limits):
  A  NC    at the no-control hosting capacity        (reference: at its limit)
  B  VVAR  at the SAME nameplate size as A           (what Volt-VAr does to the same PV)
  C  VVAR  at its own hosting capacity                (new limit, smaller PV)

Run from the repository root:  python scripts/10_trafo_pqs_rural.py
Output: results/trafo_pqs_rural.csv
"""
import copy
import math

import pandapower as pp
import pandas as pd
import simbench as sb

LOADING_LIMIT = 100.0
V_LIMIT = 1.05
MAX_KW = 2000.0
TOL_KW = 0.1


def thermal_ok(net):
    return (net.res_line.loading_percent.max() <= LOADING_LIMIT and
            net.res_trafo.loading_percent.max() <= LOADING_LIMIT)


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
    return net


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
    return net


def hosting_capacity(base, bus, runner):
    lo, hi = 0.0, MAX_KW
    while hi - lo > TOL_KW:
        mid = (lo + hi) / 2
        try:
            net = runner(base, bus, mid)
            ok = net.res_bus.vm_pu.max() <= V_LIMIT and thermal_ok(net)
        except Exception:
            ok = False
        if ok:
            lo = mid
        else:
            hi = mid
    return round(lo, 1)


def measure(net, bus, case, size_kw):
    """Collect PV output and transformer flows (LV side) from a solved network."""
    sg = net.sgen.index.max()                      # the PV unit added last
    pv_p = net.res_sgen.p_mw.at[sg] * 1000
    pv_q = net.res_sgen.q_mvar.at[sg] * 1000
    tr = net.res_trafo.iloc[0]
    sn_kva = net.trafo.sn_mva.iloc[0] * 1000
    # Signs follow pandapower's load reference at the LV terminal (positive = into the
    # transformer): positive P = export from the LV network towards the grid, negative Q =
    # reactive power supplied by the transformer to the LV network.
    p_lv = tr.p_lv_mw * 1000
    q_lv = tr.q_lv_mvar * 1000
    s_lv = math.hypot(p_lv, q_lv)
    return {
        "case": case,
        "bus": bus,
        "nameplate_kW": size_kw,
        "pv_P_kW": round(pv_p, 2),
        "pv_Q_kvar": round(pv_q, 2),
        "v_pv_pu": round(net.res_bus.vm_pu.at[bus], 4),
        "v_max_pu": round(net.res_bus.vm_pu.max(), 4),
        "trafo_P_kW": round(p_lv, 2),
        "trafo_Q_kvar": round(q_lv, 2),
        "trafo_S_kVA": round(s_lv, 2),
        "S_over_Sn_pct": round(100 * s_lv / sn_kva, 2),
        "trafo_loading_pct": round(tr.loading_percent, 2),
        "line_max_loading_pct": round(net.res_line.loading_percent.max(), 2),
    }


base = sb.get_simbench_net("1-LV-rural1--0-sw")
buses = sorted(base.load.bus.unique())

rows = []
for bus in buses:
    hc_nc = hosting_capacity(base, bus, run_no_control)
    hc_vv = hosting_capacity(base, bus, run_volt_var)
    rows.append(measure(run_no_control(base, bus, hc_nc), bus, "A_NC_at_NC_limit", hc_nc))
    rows.append(measure(run_volt_var(base, bus, hc_nc), bus, "B_VVAR_same_size", hc_nc))
    rows.append(measure(run_volt_var(base, bus, hc_vv), bus, "C_VVAR_at_VVAR_limit", hc_vv))

df = pd.DataFrame(rows)
df.to_csv("results/trafo_pqs_rural.csv", index=False, encoding="utf-8")

pd.set_option("display.width", 250)
cols = ["bus", "case", "nameplate_kW", "pv_P_kW", "pv_Q_kvar", "v_pv_pu",
        "trafo_P_kW", "trafo_Q_kvar", "trafo_S_kVA", "trafo_loading_pct",
        "line_max_loading_pct"]
print(df[cols].to_string(index=False))

# Compact test of the explanation: change from A to B (same PV size, Volt-VAr switched on)
a = df[df.case == "A_NC_at_NC_limit"].set_index("bus")
b = df[df.case == "B_VVAR_same_size"].set_index("bus")
c = df[df.case == "C_VVAR_at_VVAR_limit"].set_index("bus")
cmp = pd.DataFrame({
    "size_kW": a.nameplate_kW,
    "dP_kW": (b.trafo_P_kW - a.trafo_P_kW).round(2),
    "dQ_kvar": (b.trafo_Q_kvar - a.trafo_Q_kvar).round(2),
    "dS_kVA": (b.trafo_S_kVA - a.trafo_S_kVA).round(2),
    "loading_A_%": a.trafo_loading_pct,
    "loading_B_%": b.trafo_loading_pct,
    "VVAR_limit_kW": c.nameplate_kW,
})
print("\n=== Same PV size: Volt-VAr off (A) vs on (B) ===")
print(cmp.to_string())