"""Script 19: snapshot at the SimBench study cases, with two more control variants.

Why
  The stored operating point of scripts 11 and 16 has the existing PV at full
  output and the loads at their stored values (1.08 to 2.37 times the largest
  load of the year). Script 17 showed that the year never reaches this point.
  SimBench defines study cases (net.loadcases) with their own scaling factors
  for load and PV. This script repeats the analysis of script 11 at the study
  cases with low load and high PV, so the snapshot uses an operating point that
  planners use.

  It also adds control variants that a reviewer may ask for:
    cosphi     cos phi(P) characteristic of the type in VDE-AR-N 4105:2018 on the
               added unit: cos phi = 1 for P <= 0.5 Pn, then linear to 0.90
               underexcited at P = Pn (reactive power absorbed). No voltage input.
    vvar_all   default IEEE 1547 Volt-VAr on every PV unit (existing and added),
               each unit on its own bus voltage.
    vvar_slim  Volt-VAr on the added unit with an inverter apparent-power limit
               S = Pn and active-power priority: |Q| <= sqrt(Pn^2 - P^2).
               Run only where it can change the result, that is where the PV
               factor of the case is above sqrt(1 - 0.44^2) = 0.898. Below that
               the full 0.44 Pn is available and vvar_slim = vvar exactly.

What is the same as script 11
  Limits (1.05 pu, 100 % current-based), search (binary, 0.1 kW, 2000 kW
  ceiling), the Volt-VAr curve and its iteration, the bus sample (20 buses per
  grid evenly spaced along the electrical distance, all 13 of rural1), the
  derived columns (first limit, effect, r = hc_t / hc_v, gain, penalty, dead
  band, checks). Script 11 is imported, not copied, and not changed.

What is different
  - Loads and existing PV units take the values of the study case.
  - The added unit has nameplate Pn (the searched size) and injects
    P = Pn x f_pv, where f_pv is the PV factor of the case (sum of existing PV
    output at the case / sum of existing PV nameplate). Volt-VAr uses
    Q = ratio(V) x Pn, as in scripts 14 and 15. All capacities are nameplate kW.
  - The nine buses of the time-series study (near, middle, far of rural1,
    semiurb5 and urban6; script 12) are always added, at the study cases and at
    the stored point ("stored", f_pv = 1). The stored rows reproduce script 11
    where both exist (check) and give the stored-point effect at the six buses
    that are not in the script 11 sample. Script 21 compares these rows with
    the year.

Study cases
  By default every case with PV factor >= 0.5 and load factor <= 0.5 (low load,
  high PV) is run: lW (load 0.1, PV 0.8) and lPV (load 0.1, PV 0.95). The
  factors of all cases are printed and written to the summary. --cases
  overrides the choice.

Slack voltage and voltage limit (design note, 26 Oct 2026)
  The first run showed that the SimBench slack voltage of lW and lPV is
  1.055 pu, above the 1.05 pu limit, so every base case violates the limit
  before any PV is added. No capacity result had been computed. Two variants:
    --slack stored  (default, label "lW")    load and PV factors of the case,
                     slack voltage as stored (1.025 pu, as in scripts 11 and 12
                     and in the year), limit 1.05 pu. This is the main test:
                     only the operating point of loads and PV changes, so the
                     snapshot compares with the year at the same voltage headroom.
    --slack case    (label "lW-sb")          the SimBench case as defined: slack
                     1.055 pu, limit 1.10 pu (EN 50160 upper limit).
    --slack both     runs both.

Pre-registered predictions: see docs/predictions_19_21.md (register before the run).

Run from the repository root (file name with underscores: 19_studycase_snapshot.py):
  python scripts/19_studycase_snapshot.py --list-cases          (print the study cases, no search)
  python scripts/19_studycase_snapshot.py --workers 4           (main test, --slack stored)
  python scripts/19_studycase_snapshot.py --workers 4 --slack case --resume   (SimBench slack, 1.10 pu)
  python scripts/19_studycase_snapshot.py --workers 4 --resume
  python scripts/19_studycase_snapshot.py --grids rural1 --per-grid 2 --out test   (quick test)
Outputs: results/studycase_snapshot.csv and results/studycase_summary.md
(--out NAME replaces 'studycase').
Send back: results/studycase_summary.md
"""
import argparse
import copy
import importlib.util
import math
import multiprocessing
import os
import time
import warnings

import numpy as np
import pandapower as pp
import pandas as pd
import simbench as sb

warnings.filterwarnings("ignore")

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)


def _load(name, file):
    spec = importlib.util.spec_from_file_location(name, os.path.join(HERE, file))
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


s11 = _load("s11", "11_multi_feeder_snapshot.py")     # limits, curve, search constants, pick_buses, summary
ts = _load("ts12", "12_timeseries.py")                # pick_buses (near, middle, far)

GRIDS = s11.GRIDS
TS_GRIDS = ["rural1", "semiurb5", "urban6"]
Q_MAX = 0.44
F_SLIM = math.sqrt(1 - Q_MAX ** 2)                    # 0.898: above this P, S = Pn limits Q
MAX_IT = {"vvar": 20, "vvar_slim": 20, "vvar_all": 30}
SB_SUFFIX = "-sb"          # label suffix: SimBench slack voltage of the case
V_LIMIT_SB = 1.10          # EN 50160 upper limit, used with the SimBench slack voltage


def parse_label(label):
    """'lW' -> ('lW', False); 'lW-sb' -> ('lW', True); 'stored' -> ('stored', False)."""
    if label.endswith(SB_SUFFIX):
        return label[:-len(SB_SUFFIX)], True
    return label, False


def v_limit_of(label):
    return V_LIMIT_SB if parse_label(label)[1] else s11.V_LIMIT


def limits_ok(net, check_v, check_t, v_lim):
    if check_v and net.res_bus.vm_pu.max() > v_lim:
        return False
    if check_t and (net.res_line.loading_percent.max() > s11.LOADING_LIMIT or
                    net.res_trafo.loading_percent.max() > s11.LOADING_LIMIT):
        return False
    return True


# ---------------------------------------------------------------- study cases
def _is_pv(net):
    return net.sgen.type.fillna("").str.contains("PV", case=False).to_numpy()


def case_values(net, case):
    """Absolute load P, Q, sgen P and slack voltage of a study case.
    First the simbench API (get_absolute_values with study cases); if that does
    not give the case, the factors of net.loadcases are applied by hand."""
    try:
        av = sb.get_absolute_values(net, profiles_instead_of_study_cases=False)
        lp, lq, sp = av[("load", "p_mw")], av[("load", "q_mvar")], av[("sgen", "p_mw")]
        if case in lp.index and case in sp.index:
            vm = None
            key = ("ext_grid", "vm_pu")
            if key in av and case in av[key].index:
                vm = float(np.asarray(av[key].loc[case]).ravel()[0])
            out = dict(
                lp=lp.loc[case].reindex(net.load.index).to_numpy(float),
                lq=lq.loc[case].reindex(net.load.index).to_numpy(float),
                sp=sp.loc[case].reindex(net.sgen.index).to_numpy(float),
                vm=vm, source="simbench.get_absolute_values")
            if not any(np.isnan(out[k]).any() for k in ("lp", "lq", "sp")):
                return out                     # otherwise: columns did not match, use the factors
    except Exception:
        pass
    row = net.loadcases.loc[case]
    typ = net.sgen.type.fillna("").str.lower()
    fac = np.where(typ.str.contains("pv"), row["PV_p"],
                   np.where(typ.str.contains("wind"), row["Wind_p"], row["RES_p"]))
    return dict(lp=net.load.p_mw.to_numpy(float) * row["pload"],
                lq=net.load.q_mvar.to_numpy(float) * row["qload"],
                sp=net.sgen.p_mw.to_numpy(float) * fac,
                vm=float(row["Slack_vm"]) if "Slack_vm" in row.index else None,
                source="net.loadcases factors")


def case_factors(net, case):
    pv = _is_pv(net)
    if case == "stored":
        return dict(case="stored", load_factor=1.0, pv_factor=1.0,
                    slack_vm=float(net.ext_grid.vm_pu.iloc[0]), source="stored values")
    cv = case_values(net, case)
    load0 = net.load.p_mw.sum()
    pv0 = net.sgen.p_mw.to_numpy(float)[pv].sum()
    lc = net.loadcases.loc[case]                       # raw factors, for comparison
    return dict(case=case,
                load_factor=round(float(cv["lp"].sum() / load0), 4) if load0 > 0 else float("nan"),
                pv_factor=round(float(cv["sp"][pv].sum() / pv0), 4) if pv0 > 0 else float("nan"),
                slack_vm=cv["vm"] if cv["vm"] is not None else float(net.ext_grid.vm_pu.iloc[0]),
                source=cv["source"],
                loadcases_row="; ".join(f"{k}={v}" for k, v in lc.items()))


def apply_case(net, label):
    """Return (net at the operating point, f_pv, PV units [(sgen index, bus, nameplate kW)]).
    The slack voltage of the case is used only for labels ending in '-sb'."""
    case, sb_slack = parse_label(label)
    net = copy.deepcopy(net)
    pv = _is_pv(net)
    units = [(int(i), int(b), float(p) * 1000)
             for i, b, p, is_pv in zip(net.sgen.index, net.sgen.bus, net.sgen.p_mw, pv) if is_pv]
    if case == "stored":
        return net, 1.0, units
    cv = case_values(net, case)
    pv0 = net.sgen.p_mw.to_numpy(float)[pv].sum()
    f_pv = float(cv["sp"][pv].sum() / pv0)
    net.load["p_mw"] = cv["lp"]
    net.load["q_mvar"] = cv["lq"]
    net.sgen["p_mw"] = cv["sp"]
    if sb_slack:
        if cv["vm"] is None:
            raise RuntimeError(f"{label}: no slack voltage for case {case}")
        net.ext_grid["vm_pu"] = cv["vm"]
    return net, f_pv, units


# ---------------------------------------------------------------- controls
def cosphi_q_kvar(p_kw, pn_kw):
    """cos phi(P), VDE-AR-N 4105:2018 type: 1.00 up to 0.5 Pn, linear to 0.90
    underexcited at Pn. Negative = absorbed (same sign as Volt-VAr at high voltage)."""
    x = p_kw / pn_kw if pn_kw > 0 else 0.0
    if x <= 0.5:
        return 0.0
    cphi = 1.0 - 0.2 * (min(x, 1.0) - 0.5)
    return -p_kw * math.tan(math.acos(cphi))


def solve(net, idx, bus, kw, control, f_pv, units):
    """Set the added unit (nameplate kw, output kw * f_pv) and the control, run the power flow.
    For control 'vvar' with f_pv = 1 this is the same sequence as script 11 solve()."""
    p = kw * f_pv
    net.sgen.at[idx, "p_mw"] = p / 1000
    net.sgen.at[idx, "q_mvar"] = 0.0
    if control == "vvar_all":
        for i, _, _ in units:
            net.sgen.at[i, "q_mvar"] = 0.0
    if control == "none":
        pp.runpp(net)
        return
    if control == "cosphi":
        net.sgen.at[idx, "q_mvar"] = cosphi_q_kvar(p, kw) / 1000
        pp.runpp(net)
        return
    ctrl = [(idx, bus, kw)] + (units if control == "vvar_all" else [])
    q_prev = {i: 0.0 for i, _, _ in ctrl}
    for _ in range(MAX_IT[control]):
        pp.runpp(net)
        diff = 0.0
        for i, b, pn in ctrl:
            q = s11.vvar_q_ratio(net.res_bus.vm_pu.at[b]) * pn
            if control == "vvar_slim":
                lim = math.sqrt(max(pn ** 2 - p ** 2, 0.0))
                q = max(-lim, min(lim, q))
            net.sgen.at[i, "q_mvar"] = q / 1000
            diff = max(diff, abs(q - q_prev[i]))
            q_prev[i] = q
        if diff < 0.1:
            break
    else:
        raise RuntimeError(f"{control} did not converge")
    pp.runpp(net)


class Searcher:
    """Binary search as script 11, with a log of power flows that did not converge."""

    def __init__(self, net, idx, bus, f_pv, units, v_lim):
        self.net, self.idx, self.bus, self.f_pv, self.units = net, idx, bus, f_pv, units
        self.v_lim = v_lim
        self.nonconv = []                     # (control, size) of each non-converged check

    def feasible(self, kw, control, check_v, check_t):
        try:
            solve(self.net, self.idx, self.bus, kw, control, self.f_pv, self.units)
            return limits_ok(self.net, check_v, check_t, self.v_lim)
        except Exception:
            self.nonconv.append((control, kw))
            return False

    def hc(self, control, check_v=True, check_t=True):
        lo, hi = 0.0, s11.MAX_KW
        while hi - lo > s11.TOL_KW:
            mid = (lo + hi) / 2
            if self.feasible(mid, control, check_v, check_t):
                lo = mid
            else:
                hi = mid
        return round(lo, 1)

    def hc_near(self, control, check_v, check_t, guess):
        """Same boundary as hc(), starting from a guess (as script 11 hosting_capacity_near)."""
        step, tol, top_ = 1.3, s11.TOL_KW, s11.MAX_KW
        f = lambda kw: self.feasible(kw, control, check_v, check_t)
        guess = min(max(guess, 1.0), top_)
        if f(guess):
            lo, hi = guess, guess * step
            while hi < top_ and f(hi):
                lo, hi = hi, hi * step
            hi = min(hi, top_)
        else:
            hi, lo = guess, guess / step
            while lo > tol and not f(lo):
                hi, lo = lo, lo / step
            if lo <= tol:
                lo = 0.0
        while hi - lo > tol:
            mid = (lo + hi) / 2
            if f(mid):
                lo = mid
            else:
                hi = mid
        return round(lo, 1)

    def nonconv_at_or_below(self, control, cap):
        return sum(1 for c, kw in self.nonconv if c == control and kw <= cap)


# ---------------------------------------------------------------- per bus
_BASE, _CASE = {}, {}


def get_base(code):
    if code not in _BASE:
        _BASE[code] = sb.get_simbench_net(code)
    return _BASE[code]


def get_case(code, case):
    key = (code, case)
    if key not in _CASE:
        _CASE[key] = apply_case(get_base(code), case)
    return _CASE[key]


def effect_of(delta):
    if delta > s11.EQUAL_TOL_KW:
        return "higher"
    if delta < -s11.EQUAL_TOL_KW:
        return "lower"
    return "equal"


def analyse_bus(task):
    code, case, bus, dist, in_sample, position = task      # case is the label, e.g. lW or lW-sb
    base, f_pv, units = get_case(code, case)
    net = copy.deepcopy(base)
    idx = pp.create_sgen(net, bus=bus, p_mw=0.0, q_mvar=0.0)
    v_lim = v_limit_of(case)
    S = Searcher(net, idx, bus, f_pv, units, v_lim)

    hc_v = S.hc("none", True, False)
    hc_t = S.hc("none", False, True)
    hc_nc = S.hc("none")
    hc_vv = S.hc("vvar")
    hc_v_vv = S.hc_near("vvar", True, False, hc_v)
    hc_t_vv = S.hc_near("vvar", False, True, hc_t)
    hc_cp = S.hc("cosphi")
    hc_all = S.hc("vvar_all")
    hc_slim = S.hc("vvar_slim") if f_pv > F_SLIM else hc_vv

    solve(net, idx, bus, hc_t, "none", f_pv, units)
    t_el = ("trafo" if net.res_trafo.loading_percent.max() >= net.res_line.loading_percent.max()
            else "line")
    solve(net, idx, bus, hc_nc, "none", f_pv, units)
    v_pv = round(float(net.res_bus.vm_pu.at[bus]), 4)

    first = ("both" if abs(hc_v - hc_t) <= s11.EQUAL_TOL_KW
             else ("voltage" if hc_v < hc_t else "thermal"))
    pct = lambda x: round(100 * (x - hc_nc) / hc_nc, 2) if hc_nc > 0 else float("nan")
    delta = round(hc_vv - hc_nc, 1)
    return {
        "code": code, "case": case, "bus": int(bus), "z_ohm": round(dist, 4),
        "in_sample": in_sample, "position": position, "f_pv": round(f_pv, 4),
        "slack_vm": round(float(base.ext_grid.vm_pu.iloc[0]), 4), "v_limit": v_lim,
        "hc_v": hc_v, "hc_t": hc_t, "hc_nc": hc_nc, "hc_vvar": hc_vv,
        "hc_v_vvar": hc_v_vv, "hc_t_vvar": hc_t_vv,
        "delta_kW": delta, "delta_pct": pct(hc_vv),
        "first_limit": first, "effect": effect_of(delta), "thermal_element": t_el,
        "v_pv_nc": v_pv,
        "ratio_t_v": round(hc_t / hc_v, 3) if hc_v > 0 else float("nan"),
        "gain_pct": round(100 * (hc_v_vv - hc_v) / hc_v, 2) if hc_v > 0 else float("nan"),
        "penalty_pct": round(100 * (hc_t - hc_t_vv) / hc_t, 2) if hc_t > 0 else float("nan"),
        "vvar_is_min": abs(hc_vv - min(hc_v_vv, hc_t_vv)) <= s11.EQUAL_TOL_KW,
        "nc_is_min": abs(hc_nc - min(hc_v, hc_t)) <= s11.EQUAL_TOL_KW,
        "hc_cosphi": hc_cp, "cosphi_pct": pct(hc_cp), "cosphi_effect": effect_of(round(hc_cp - hc_nc, 1)),
        "hc_vvar_all": hc_all, "vvar_all_pct": pct(hc_all),
        "vvar_all_effect": effect_of(round(hc_all - hc_nc, 1)),
        "hc_vvar_slim": hc_slim, "slim_run": f_pv > F_SLIM,
        "nonconv_vvar_at_or_below": S.nonconv_at_or_below("vvar", hc_vv),
        "nonconv_vvar_all_at_or_below": S.nonconv_at_or_below("vvar_all", hc_all),
        "nonconv_total": len(S.nonconv),
        "capped": max(hc_v, hc_t, hc_nc, hc_vv, hc_v_vv, hc_t_vv, hc_cp, hc_all) >= s11.MAX_KW - 0.5,
    }


def network_info(code, case):
    net, f_pv, _ = get_case(code, case)
    pp.runpp(net)
    v_max = float(net.res_bus.vm_pu.max())
    l_max = float(net.res_line.loading_percent.max())
    t_max = float(net.res_trafo.loading_percent.max())
    v_lim = v_limit_of(case)
    why = [w for w, bad in (("voltage", v_max > v_lim), ("line", l_max > s11.LOADING_LIMIT),
                            ("trafo", t_max > s11.LOADING_LIMIT)) if bad]
    return {"code": code, "case": case, "f_pv": round(f_pv, 3),
            "slack_vm": round(float(net.ext_grid.vm_pu.iloc[0]), 4), "v_limit": v_lim,
            "load_kW": round(float(net.load.p_mw.sum()) * 1000, 1),
            "existing_pv_kW": round(float(net.sgen.p_mw.sum()) * 1000, 1),
            "base_v_max": round(v_max, 4), "base_line_%": round(l_max, 1),
            "base_trafo_%": round(t_max, 1),
            "status": "ok" if not why else "base violation: " + ", ".join(why)}


# ---------------------------------------------------------------- summary
md_table = s11.md_table
BINS = [-1, 1.0, 1.05, 1.10, 1.25, 1.5, float("inf")]
LABELS = ["< 1 (thermal first)", "1.00-1.05", "1.05-1.10", "1.10-1.25", "1.25-1.50", ">= 1.50"]


def rules_table(g):
    """The four rules of script 18 (P1 to P4) on one set of buses."""
    vf = g[g.first_limit == "voltage"]
    dead = g[g.v_pv_nc <= s11.DEADBAND_UPPER + 0.0005]
    p1 = g[g.ratio_t_v < 1.0]
    p2 = g[(g.ratio_t_v >= 1.05) & (g.first_limit == "voltage")]
    return [
        {"rule": "P1: r < 1, Volt-VAr never higher",
         "result": f"{int((p1.effect != 'higher').sum())} of {len(p1)}"},
        {"rule": "P2: r >= 1.05 and voltage first, Volt-VAr higher",
         "result": f"{int((p2.effect == 'higher').sum())} of {len(p2)}"},
        {"rule": "P3: dead band at hc_nc, Volt-VAr equal",
         "result": f"{int((dead.effect == 'equal').sum())} of {len(dead)}"},
        {"rule": "P4: hc_nc and hc_vvar = min of their parts",
         "result": f"{int((g.nc_is_min & g.vvar_is_min).sum())} of {len(g)}"},
        {"rule": "voltage-first buses: higher / equal / lower",
         "result": f"{int((vf.effect == 'higher').sum())} / {int((vf.effect == 'equal').sum())} / "
                   f"{int((vf.effect == 'lower').sum())}"},
    ]


def variant_table(g):
    rows = []
    for fl, h in g.groupby("first_limit"):
        for name, eff, pct in (("Volt-VAr (added unit)", "effect", "delta_pct"),
                               ("cos phi(P) (added unit)", "cosphi_effect", "cosphi_pct"),
                               ("Volt-VAr (all PV units)", "vvar_all_effect", "vvar_all_pct")):
            e = h[eff].value_counts()
            rows.append({"first limit": fl, "control": name, "buses": len(h),
                         "higher": int(e.get("higher", 0)), "equal": int(e.get("equal", 0)),
                         "lower": int(e.get("lower", 0)),
                         "median change %": round(h[pct].median(), 2),
                         "min %": round(h[pct].min(), 2), "max %": round(h[pct].max(), 2)})
    return pd.DataFrame(rows)


def write_summary(path, factors, info, df, seconds):
    out = ["# Snapshot at the SimBench study cases (script 19)", "",
           f"Voltage limit {s11.V_LIMIT} pu with the stored slack voltage (labels without '-sb', and "
           f"'stored'); {V_LIMIT_SB} pu (EN 50160) with the SimBench slack voltage of the case "
           f"(labels ending '-sb'). Thermal limit {s11.LOADING_LIMIT:.0f} % (current-based), search "
           f"{s11.TOL_KW} kW, ceiling {s11.MAX_KW:.0f} kW, 'equal' within {s11.EQUAL_TOL_KW} kW. "
           "Capacities are nameplate kW; the added unit injects Pn x f_pv. "
           + (f"Run time {seconds / 60:.1f} min." if seconds else "Regenerated from the saved CSV."),
           "", "## Study cases of each network (all cases, the run uses the selected ones)", "",
           md_table(pd.DataFrame(factors))]
    for case, g_all in df.groupby("case"):
        g = g_all[g_all.in_sample]
        if g.empty:
            continue
        tmp = path + ".tmp"
        d = g.copy()
        d["code"] = d.code + " [" + case + "]"
        s11.write_summary(tmp, [i for i in info if i["case"] == case], d)
        body = open(tmp, encoding="utf-8").read().split("\n")
        os.remove(tmp)
        text = "\n".join(ln for ln in body[1:] if not ln.startswith("Voltage limit"))
        out += ["", f"# Case {case}: script 11 tables on the sample ({len(g)} buses)", text,
                f"## Case {case}: rules P1 to P4 of script 18", "",
                md_table(pd.DataFrame(rules_table(g))),
                "", f"## Case {case}: control variants by first limit", "",
                "Change relative to no control at the same case (nameplate kW).", "",
                md_table(variant_table(g))]
        slim_run = bool(g.slim_run.any())
        out += ["", f"## Case {case}: inverter apparent-power limit (S = Pn, P priority)", "",
                (f"PV factor {g.f_pv.iloc[0]:.3f} is above {F_SLIM:.3f}: the limit can bind and was "
                 f"searched. Buses where it changed Volt-VAr: "
                 f"{int((abs(g.hc_vvar_slim - g.hc_vvar) > s11.EQUAL_TOL_KW).sum())} of {len(g)}.")
                if slim_run else
                (f"PV factor {g.f_pv.iloc[0]:.3f} is at or below {F_SLIM:.3f}: with S = Pn the full "
                 f"0.44 Pn of reactive power is available (sqrt(1 - f^2) >= 0.44), so the limit "
                 f"does not change any result at this case (not searched).")]
    ts_rows = df[df.position != ""]
    if not ts_rows.empty:
        cols = ["code", "case", "bus", "position", "f_pv", "hc_nc", "first_limit", "ratio_t_v",
                "hc_vvar", "delta_pct", "effect", "hc_cosphi", "cosphi_pct", "hc_vvar_all",
                "vvar_all_pct"]
        out += ["", "## The nine buses of the time-series study (input for script 21)", "",
                md_table(ts_rows.sort_values(["code", "position", "case"])[cols])]
    out += ["", "## Checks", "",
            f"- Volt-VAr power flows that did not converge at or below the Volt-VAr capacity "
            f"(must be 0): {int(df.nonconv_vvar_at_or_below.sum())}",
            f"- Same for Volt-VAr on all PV units (must be 0): {int(df.nonconv_vvar_all_at_or_below.sum())}",
            f"- Non-converged checks above the capacity (expected, no effect): "
            f"{int(df.nonconv_total.sum() - df.nonconv_vvar_at_or_below.sum() - df.nonconv_vvar_all_at_or_below.sum())}",
            f"- Buses with a search at the {s11.MAX_KW:.0f} kW ceiling: {int(df.capped.sum())}",
            "- Stored rows (case 'stored') must equal script 11 where the bus is in both; script 21 checks this.",
            "", "Send this file back: " + os.path.relpath(path, ROOT)]
    with open(path, "w", encoding="utf-8") as f:
        f.write("\n".join(out) + "\n")


# ---------------------------------------------------------------- main
def all_factors(grids):
    rows = []
    for g in grids:
        net = get_base(s11.sb_code(g, "0"))
        for case in list(net.loadcases.index):
            r = case_factors(net, case)
            r["grid"] = g
            rows.append(r)
    return pd.DataFrame(rows)[["grid", "case", "load_factor", "pv_factor", "slack_vm", "source",
                               "loadcases_row"]]


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--grids", nargs="+", default=GRIDS, choices=GRIDS)
    ap.add_argument("--cases", nargs="+", default=None,
                    help="study cases to run (default: PV factor >= 0.5 and load factor <= 0.5)")
    ap.add_argument("--slack", choices=["stored", "case", "both"], default="stored",
                    help="stored: slack as stored, limit 1.05 pu (main test); case: SimBench slack "
                         "of the case, limit 1.10 pu; both: run both")
    ap.add_argument("--per-grid", type=int, default=20)
    ap.add_argument("--workers", type=int, default=1)
    ap.add_argument("--out", default="studycase")
    ap.add_argument("--resume", action="store_true")
    ap.add_argument("--list-cases", action="store_true")
    ap.add_argument("--summarize-only", action="store_true")
    args = ap.parse_args()

    os.makedirs(os.path.join(ROOT, "results"), exist_ok=True)
    p_csv = os.path.join(ROOT, "results", f"{args.out}_snapshot.csv")
    p_md = os.path.join(ROOT, "results", f"{args.out}_summary.md")

    fac = all_factors(args.grids)
    print(md_table(fac), flush=True)
    if args.list_cases:
        return
    if args.cases:
        cases = args.cases
    else:
        sel = fac[(fac.pv_factor >= 0.5) & (fac.load_factor <= 0.5)]
        cases = sorted(sel.case.unique())
        if not cases:
            raise SystemExit("No study case with PV factor >= 0.5 and load factor <= 0.5. Use --cases.")
    labels = []
    for c in cases:
        if args.slack in ("stored", "both"):
            labels.append(c)
        if args.slack in ("case", "both"):
            labels.append(c + SB_SUFFIX)
    print(f"selected study cases: {cases}; operating points: {labels}", flush=True)

    if args.summarize_only:
        df = pd.read_csv(p_csv, keep_default_na=False, na_values=[""])
        df["position"] = df.position.fillna("")
        run_labels = [c for c in df.case.unique() if c != "stored"]
        info = [network_info(s11.sb_code(g, "0"), c) for c in run_labels for g in args.grids]
        write_summary(p_md, fac.to_dict("records"), info, df, None)
        print(f"Summary rebuilt: {p_md}")
        return

    done = set()
    old = pd.DataFrame()
    if args.resume and os.path.exists(p_csv):
        old = pd.read_csv(p_csv, keep_default_na=False, na_values=[""])
        old["position"] = old.position.fillna("")
        done = set(zip(old.code, old.case, old.bus))

    info, tasks = [], []
    for case in labels + ["stored"]:
        for g in args.grids:
            code = s11.sb_code(g, "0")
            base = get_base(code)
            ts_buses = {}
            if g in TS_GRIDS:
                picks = ts.pick_buses(base)
                ts_buses = {b: pos for (b, _), pos in zip(picks, ["near", "middle", "far"])}
            if case == "stored":
                sample = []                              # stored point: only the nine buses
            else:
                inf = network_info(code, case)
                info.append(inf)
                if inf["status"] != "ok":
                    print(f"{code} [{case}]: {inf['status']} (v max {inf['base_v_max']} pu, "
                          f"slack {inf['slack_vm']} pu, limit {inf['v_limit']} pu), skipped", flush=True)
                    continue
                sample = s11.pick_buses(base, args.per_grid)
            in_s = {b for b, _ in sample}
            dist = dict(sample)
            if ts_buses:
                for b, d in s11.pick_buses(base, 0):
                    if b in ts_buses:
                        dist.setdefault(b, d)
            for b in sorted(set(in_s) | set(ts_buses)):
                if (code, case, b) in done:
                    continue
                tasks.append((code, case, int(b), float(dist[b]), b in in_s, ts_buses.get(b, "")))
    print(f"{len(tasks)} bus runs, workers = {args.workers}", flush=True)

    t0, new = time.time(), []

    def save():
        d = pd.concat([old, pd.DataFrame(new)], ignore_index=True)
        if not d.empty:
            d = d.sort_values(["case", "code", "bus"]).reset_index(drop=True)
            d.to_csv(p_csv, index=False, encoding="utf-8")
        return d

    if args.workers > 1:
        ctx = multiprocessing.get_context("spawn")
        with ctx.Pool(args.workers) as pool:
            for k, row in enumerate(pool.imap_unordered(analyse_bus, tasks, chunksize=1), 1):
                new.append(row)
                if k % 10 == 0 or k == len(tasks):
                    print(f"{k}/{len(tasks)}, {(time.time() - t0) / 60:.1f} min", flush=True)
                    save()
    else:
        for k, task in enumerate(tasks, 1):
            new.append(analyse_bus(task))
            if k % 10 == 0 or k == len(tasks):
                print(f"{k}/{len(tasks)} ({task[0]} {task[1]}), {(time.time() - t0) / 60:.1f} min",
                      flush=True)
                save()

    df = save()
    df["position"] = df.position.fillna("")
    write_summary(p_md, fac.to_dict("records"), info, df, time.time() - t0)
    print(f"\nDone. Send me this file: {p_md}")


if __name__ == "__main__":
    multiprocessing.freeze_support()
    main()