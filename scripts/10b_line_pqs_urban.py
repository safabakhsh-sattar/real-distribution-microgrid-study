"""Script 10b: line current, P, Q and S with and without Volt-VAr (urban feeder).

Companion to script 10 (rural, transformer). On the urban feeder the binding
element is a LINE (transformer only about 36% loaded at the critical bus), so the
quantity to measure is the most loaded line, not the transformer.

Question: default Volt-VAr lowers the hosting capacity at 27 of 53 urban buses and
leaves it unchanged at 26. Does the same mechanism as on the rural feeder (extra
reactive flow at unchanged active power raises the current of the limiting
element) explain this, and what distinguishes the two groups of buses?

Three cases per load bus (1.05 pu voltage limit, 100% thermal limits):
  A  NC    at the no-control hosting capacity
  B  VVAR  at the SAME nameplate size as A
  C  VVAR  at its own hosting capacity

For each case the most loaded line is identified and its flows are taken at the
end with the larger current (the end that sets the loading). Signs follow
pandapower's load reference at that line end: positive = into the line.
Line loading in pandapower is current-based (I / I_max).

Run from the repository root:  python scripts/10b_line_pqs_urban.py
Takes roughly 10-20 minutes. Output: results/line_pqs_urban.csv
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
    """PV output, most loaded line (at its higher-current end) and transformer loading."""
    sg = net.sgen.index.max()                      # the PV unit added last
    li = net.res_line.loading_percent.idxmax()
    r = net.res_line.loc[li]
    if r.i_from_ka >= r.i_to_ka:
        end, p, q, v, i = "from", r.p_from_mw, r.q_from_mvar, r.vm_from_pu, r.i_from_ka
    else:
        end, p, q, v, i = "to", r.p_to_mw, r.q_to_mvar, r.vm_to_pu, r.i_to_ka
    p, q = p * 1000, q * 1000
    return {
        "case": case,
        "bus": bus,
        "nameplate_kW": size_kw,
        "pv_P_kW": round(net.res_sgen.p_mw.at[sg] * 1000, 2),
        "pv_Q_kvar": round(net.res_sgen.q_mvar.at[sg] * 1000, 2),
        "v_pv_pu": round(net.res_bus.vm_pu.at[bus], 4),
        "v_max_pu": round(net.res_bus.vm_pu.max(), 4),
        "line": int(li),
        "line_end": end,
        "line_P_kW": round(p, 2),
        "line_Q_kvar": round(q, 2),
        "line_S_kVA": round(math.hypot(p, q), 2),
        "line_I_A": round(i * 1000, 2),
        "line_V_pu": round(v, 4),
        "line_loading_pct": round(r.loading_percent, 2),
        "trafo_loading_pct": round(net.res_trafo.loading_percent.max(), 2),
    }


base = sb.get_simbench_net("1-LV-urban6--0-sw")
buses = sorted(base.load.bus.unique())

rows = []
for n, bus in enumerate(buses, 1):
    print(f"bus {bus} ({n}/{len(buses)})", flush=True)
    hc_nc = hosting_capacity(base, bus, run_no_control)
    hc_vv = hosting_capacity(base, bus, run_volt_var)
    rows.append(measure(run_no_control(base, bus, hc_nc), bus, "A_NC_at_NC_limit", hc_nc))
    rows.append(measure(run_volt_var(base, bus, hc_nc), bus, "B_VVAR_same_size", hc_nc))
    rows.append(measure(run_volt_var(base, bus, hc_vv), bus, "C_VVAR_at_VVAR_limit", hc_vv))

df = pd.DataFrame(rows)
df.to_csv("results/line_pqs_urban.csv", index=False, encoding="utf-8")

a = df[df.case == "A_NC_at_NC_limit"].set_index("bus")
b = df[df.case == "B_VVAR_same_size"].set_index("bus")
c = df[df.case == "C_VVAR_at_VVAR_limit"].set_index("bus")
cmp = pd.DataFrame({
    "HC_NC_kW": a.nameplate_kW,
    "HC_VVAR_kW": c.nameplate_kW,
    "v_pv_A": a.v_pv_pu,
    "pvQ_B_kvar": b.pv_Q_kvar,
    "line_A": a.line,
    "line_B": b.line,
    "dP_kW": (b.line_P_kW - a.line_P_kW).round(2),
    "dQ_kvar": (b.line_Q_kvar - a.line_Q_kvar).round(2),
    "dI_A": (b.line_I_A - a.line_I_A).round(2),
    "load_A_%": a.line_loading_pct,
    "load_B_%": b.line_loading_pct,
    "trafo_A_%": a.trafo_loading_pct,
})
cmp["group"] = (cmp.HC_VVAR_kW < cmp.HC_NC_kW).map({True: "lower", False: "equal"})

pd.set_option("display.width", 250)
print("\n=== Per bus: Volt-VAr off (A) vs on (B) at the same PV size ===")
print(cmp.to_string())

print("\n=== Summary by group (lower = Volt-VAr HC below no control; equal = same) ===")
for name, g in cmp.groupby("group"):
    print(f"\n{name}: {len(g)} buses")
    print(g[["v_pv_A", "pvQ_B_kvar", "dP_kW", "dQ_kvar", "dI_A", "load_A_%", "load_B_%",
             "trafo_A_%"]].describe().loc[["min", "50%", "max"]].round(3).to_string())
    print("same limiting line in A and B:", int((g.line_A == g.line_B).sum()), "of", len(g))
    print("B infeasible at the no-control size (line loading > 100):",
          int((g["load_B_%"] > 100).sum()), "of", len(g))