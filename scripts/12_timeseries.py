"""Script 12: time-series study on three SimBench feeders.

Questions
  Q1  How does the hosting capacity found with one year of SimBench profiles
      (no control) compare with the snapshot hosting capacity of Study 1?
  Q2  With the tuned Volt-Watt curve (1.03 to 1.05 pu), does a larger nameplate
      deliver more annual energy, how much is curtailed, and what happens to
      the limits and to the losses?

Feeders: rural1, semiurb5, urban6 (scenario 0). Three buses per feeder (near,
middle, far along the electrical distance from the transformer) for Q1; the far
bus for Q2.

Method
  Profiles: sb.get_absolute_values (15-minute steps, leap year 2016, 35,136 steps).
  The added PV follows the average profile of the existing PV units, scaled to
  its nameplate. Existing PV is uncontrolled. Limits as in scripts 08 to 11:
  1.05 pu and 100 % (current-based) at every step.

  Q1 (15-minute steps, no control). Only daylight steps matter (the added PV
  is zero at night). Steps are ranked by net feeder injection plus a share of
  the added PV; the worst k_crit steps form a critical set. The capacity is
  found by bisection on the critical set. It is then checked on a larger
  verification set (the worst k_verify steps and k_rand random daylight steps).
  Any violating step found is added to the critical set and the search is
  repeated, until the capacity holds on the verification set. A step that
  already violates a limit without the added PV is excluded and counted.
  --verify-full checks the final capacity on every daylight step (slow).

  Q2 (hourly means, daylight hours). For three sizes (snapshot capacity,
  time-series capacity, and 1.5 times the larger of the two) one pass gives:
  energy available, energy delivered with the tuned Volt-Watt curve
  (equilibrium by bisection), curtailed energy, hours with a violated limit
  (voltage, thermal) without control and with Volt-Watt, and the change of
  network losses against the case without the added PV.

Run from the repository root:
  python scripts/12_timeseries.py --workers 3
  python scripts/12_timeseries.py --workers 3 --resume
  python scripts/12_timeseries.py --grids rural1 --k-crit 30 --k-verify 100 --k-rand 100 --energy-stride 40 --out test
Outputs: results/timeseries_hc.csv, results/timeseries_energy.csv,
results/timeseries_summary.md   (--out NAME replaces 'timeseries')
Run time (full run, three feeders, one process, Windows PC): 244 min. Use --workers to run feeders in parallel.
"""
import argparse
import copy
import math
import multiprocessing
import os
import time
import warnings

import numpy as np
import pandapower as pp
import pandapower.topology as top
import pandas as pd
import simbench as sb

warnings.filterwarnings("ignore")

V_LIMIT = 1.05
LOADING_LIMIT = 100.0
MAX_KW = 2000.0
TOL_KW = 0.1
VW1, VW2, VW_FLOOR = 1.03, 1.05, 0.2
DAY_F = 0.001
GRIDS = ["rural1", "semiurb5", "urban6"]
START = pd.Timestamp("2016-01-01 00:00")


def limits_ok(net):
    return (net.res_bus.vm_pu.max() <= V_LIMIT and
            net.res_line.loading_percent.max() <= LOADING_LIMIT and
            net.res_trafo.loading_percent.max() <= LOADING_LIMIT)


def vw_ratio(v):
    if v <= VW1:
        return 1.0
    if v >= VW2:
        return VW_FLOOR
    return 1.0 + (VW_FLOOR - 1.0) * (v - VW1) / (VW2 - VW1)


class Data:
    """Network and one year of profiles."""

    def __init__(self, code):
        net = sb.get_simbench_net(code)
        prof = sb.get_absolute_values(net, profiles_instead_of_study_cases=True)
        assert len(net.gen) == 0 and len(net.storage) == 0, "gen or storage present"
        self.code, self.net = code, net
        self.lp = prof[("load", "p_mw")].reindex(columns=net.load.index).to_numpy(float)
        self.lq = prof[("load", "q_mvar")].reindex(columns=net.load.index).to_numpy(float)
        self.sp = prof[("sgen", "p_mw")].reindex(columns=net.sgen.index).to_numpy(float)
        self.sg_index = net.sgen.index.to_numpy()
        pv = net.sgen.type.fillna("").str.contains("PV", case=False).to_numpy()
        self.f = self.sp[:, pv].sum(1) / net.sgen.p_mw.to_numpy()[pv].sum()
        self.N = self.sp.sum(1) - self.lp.sum(1)            # net injection, MW
        T = len(self.f)
        assert T % 4 == 0
        hmean = lambda a: a.reshape(T // 4, 4, -1).mean(1)
        self.h_lp, self.h_lq, self.h_sp = hmean(self.lp), hmean(self.lq), hmean(self.sp)
        self.h_f = self.f.reshape(T // 4, 4).mean(1)


class Case:
    """A copy of the network with one added PV unit at a bus."""

    def __init__(self, D, bus):
        self.D, self.bus = D, bus
        self.net = copy.deepcopy(D.net)
        self.idx = pp.create_sgen(self.net, bus=bus, p_mw=0.0, q_mvar=0.0)

    def set_state(self, t, hourly):
        D = self.D
        if hourly:
            lp, lq, sp = D.h_lp[t], D.h_lq[t], D.h_sp[t]
        else:
            lp, lq, sp = D.lp[t], D.lq[t], D.sp[t]
        self.net.load["p_mw"] = lp
        self.net.load["q_mvar"] = lq
        self.net.sgen.loc[D.sg_index, "p_mw"] = sp

    def run_p(self, p_kw, t, hourly=False):
        """Set the state of step t, inject p_kw at the added unit, run the power flow."""
        self.set_state(t, hourly)
        self.net.sgen.at[self.idx, "p_mw"] = p_kw / 1000
        pp.runpp(self.net)

    def run_size(self, size_kw, t, hourly=False):
        f = self.D.h_f[t] if hourly else self.D.f[t]
        self.run_p(size_kw * f, t, hourly)

    def losses_kw(self):
        return 1000 * (self.net.res_line.pl_mw.sum() + self.net.res_trafo.pl_mw.sum())

    def flags(self):
        """(voltage limit violated, thermal limit violated)"""
        n = self.net
        return (bool(n.res_bus.vm_pu.max() > V_LIMIT),
                bool(n.res_line.loading_percent.max() > LOADING_LIMIT or
                     n.res_trafo.loading_percent.max() > LOADING_LIMIT))


def snapshot_hc(D, bus):
    """Snapshot capacity as in Study 1: stored operating point, no control."""
    net = copy.deepcopy(D.net)
    idx = pp.create_sgen(net, bus=bus, p_mw=0.0, q_mvar=0.0)
    lo, hi = 0.0, MAX_KW
    while hi - lo > TOL_KW:
        mid = (lo + hi) / 2
        net.sgen.at[idx, "p_mw"] = mid / 1000
        try:
            pp.runpp(net)
            ok = limits_ok(net)
        except Exception:
            ok = False
        if ok:
            lo = mid
        else:
            hi = mid
    return round(lo, 1)


def feasible_on(case, kw, steps):
    """True if no limit is violated on any of the steps, else (False, first violating step)."""
    for t in steps:
        try:
            case.run_size(kw, t)
            ok = limits_ok(case.net)
        except Exception:
            ok = False
        if not ok:
            return False, t
    return True, None


def bisect_ts(case, C, hi0):
    lo, hi = 0.0, hi0
    last = None
    while hi - lo > TOL_KW:
        mid = (lo + hi) / 2
        ok, t = feasible_on(case, mid, C)
        if ok:
            lo = mid
        else:
            hi = mid
            last = t
            C.remove(t)
            C.insert(0, t)
    return math.floor(lo * 10) / 10, last      # round down: stays on the feasible side


def hc_timeseries(case, C0, V, skip):
    C = [t for t in C0 if t not in skip]
    hi0, rounds, n_checked = MAX_KW, 0, 0
    while True:
        hc, crit = bisect_ts(case, C, hi0)
        Cset, viol = set(C), []
        for t in V:
            if t in skip or t in Cset:
                continue
            n_checked += 1
            ok, _ = feasible_on(case, hc, [t])
            if not ok:
                viol.append(t)
                if len(viol) >= 10:
                    break
        if not viol or rounds >= 8:
            return hc, crit, rounds, n_checked, len(viol)
        C += viol
        hi0 = hc + TOL_KW
        rounds += 1


def limiting_element(case, kw, t):
    """What is violated at step t just above the capacity?"""
    try:
        case.run_size(kw * 1.02 + 0.2, t)
    except Exception:
        return "no convergence"
    n = case.net
    if n.res_bus.vm_pu.max() > V_LIMIT:
        return "voltage"
    if n.res_trafo.loading_percent.max() > LOADING_LIMIT:
        return "trafo"
    if n.res_line.loading_percent.max() > LOADING_LIMIT:
        return "line"
    return "none"


def vw_output(case, p_av, t):
    """Delivered power (kW) with the tuned Volt-Watt curve: P = p_av * ratio(v(P))."""
    lo, hi = 0.0, p_av
    while hi - lo > TOL_KW:
        mid = (lo + hi) / 2
        case.run_p(mid, t, hourly=True)
        if mid <= p_av * vw_ratio(case.net.res_bus.vm_pu.at[case.bus]):
            lo = mid
        else:
            hi = mid
    return lo


def base_hours(case, hours):
    """Losses and violation flags without the added PV."""
    loss, fv, ft = [], [], []
    for h in hours:
        case.run_p(0.0, h, hourly=True)
        loss.append(case.losses_kw())
        v, th = case.flags()
        fv.append(v)
        ft.append(th)
    return np.array(loss), np.array(fv), np.array(ft)


def energy_pass(case, size, hours, base, scale):
    D = case.D
    b_loss, b_v, b_t = base
    r = dict(E_avail=0.0, E_vw=0.0, vh_nc=0, th_nc=0, vh_vw=0, th_vw=0, dL_nc=0.0, dL_vw=0.0)
    for k, h in enumerate(hours):
        p_av = size * D.h_f[h]
        case.run_p(p_av, h, hourly=True)
        v0 = case.net.res_bus.vm_pu.at[case.bus]
        fv, ft = case.flags()
        loss = case.losses_kw()
        r["E_avail"] += p_av
        r["vh_nc"] += fv and not b_v[k]
        r["th_nc"] += ft and not b_t[k]
        r["dL_nc"] += loss - b_loss[k]
        if v0 <= VW1:
            p_out, fv2, ft2, loss2 = p_av, fv, ft, loss
        else:
            p_out = vw_output(case, p_av, h)
            case.run_p(p_out, h, hourly=True)
            fv2, ft2 = case.flags()
            loss2 = case.losses_kw()
        r["E_vw"] += p_out
        r["vh_vw"] += fv2 and not b_v[k]
        r["th_vw"] += ft2 and not b_t[k]
        r["dL_vw"] += loss2 - b_loss[k]
    for key in ("E_avail", "E_vw", "dL_nc", "dL_vw", "vh_nc", "th_nc", "vh_vw", "th_vw"):
        r[key] *= scale
    return r


def pick_buses(net, k=3):
    buses = sorted(int(b) for b in net.load.bus.unique())
    g = top.create_nxgraph(net, calc_branch_impedances=True, respect_switches=True)
    dist = top.calc_distance_to_bus(net, int(net.ext_grid.bus.iloc[0]), weight="weight", g=g)
    pairs = sorted((float(dist.loc[b]), b) for b in buses)
    sel = np.unique(np.linspace(0, len(pairs) - 1, k).round().astype(int))
    return [(pairs[i][1], pairs[i][0]) for i in sel]


def stamp(t):
    return (START + pd.Timedelta(minutes=15 * int(t))).strftime("%d %b %H:%M")


def run_feeder(job):
    grid, a = job
    t0 = time.time()
    code = f"1-LV-{grid}--0-sw"
    D = Data(code)
    picks = pick_buses(D.net)
    snap = {b: snapshot_hc(D, b) for b, _ in picks}
    p_ref = float(np.median(list(snap.values()))) / 1000

    day = np.where(D.f > DAY_F)[0]
    score = D.N + p_ref * D.f
    order = day[np.argsort(-score[day])]
    C0 = [int(t) for t in order[:a["k_crit"]]]
    rng = np.random.default_rng(0)
    rand = rng.choice(day, size=min(a["k_rand"], len(day)), replace=False)
    V = list(dict.fromkeys([int(t) for t in order[:a["k_verify"]]] + [int(t) for t in rand]))

    probe = Case(D, picks[0][0])
    skip = set()
    for t in set(C0) | set(V):
        try:
            probe.run_p(0.0, t)
            if not limits_ok(probe.net):
                skip.add(t)
        except Exception:
            skip.add(t)
    print(f"{code}: {len(day)} daylight steps, critical {len(C0)}, verification {len(V)}, "
          f"skipped (base violation) {len(skip)}", flush=True)

    hc_rows, en_rows = [], []
    for b, z in picks:
        case = Case(D, b)
        hc, crit, rounds, nchk, nviol = hc_timeseries(case, C0, V, skip)
        capped = hc >= MAX_KW - 0.5
        row = {
            "code": code, "bus": b, "z_ohm": round(z, 4),
            "hc_snapshot": snap[b], "hc_ts": hc,
            "ratio_ts_snapshot": round(hc / snap[b], 2) if snap[b] > 0 else float("nan"),
            "binding_time": stamp(crit) if crit is not None else "-",
            "binding_f": round(float(D.f[crit]), 3) if crit is not None else float("nan"),
            "limit": limiting_element(case, hc, crit) if crit is not None else "none",
            "refine_rounds": rounds, "verify_steps": nchk,
            "unresolved_violations": nviol, "capped": capped,
            "full_check_violations": "", "full_check_steps": "",
        }
        if a["verify_full"] and not capped:
            bad = 0
            steps = [int(t) for t in day if int(t) not in skip]
            for t in steps:
                ok, _ = feasible_on(case, hc, [t])
                bad += (not ok)
            row["full_check_violations"], row["full_check_steps"] = bad, len(steps)
        hc_rows.append(row)
        print(f"{code}: bus {b}  snapshot {snap[b]} kW, time-series {hc} kW, "
              f"{(time.time() - t0) / 60:.1f} min", flush=True)

    if not a["skip_energy"]:
        far = picks[-1][0]
        far_row = [r for r in hc_rows if r["bus"] == far][0]
        s_snap, s_ts = far_row["hc_snapshot"], far_row["hc_ts"]
        big = round(1.5 * max(s_snap, s_ts), 1)
        sizes = [("snapshot capacity", s_snap), ("time-series capacity", s_ts),
                 ("1.5 x larger capacity", big)]
        stride = a["energy_stride"]
        hours = [int(h) for h in np.where(D.h_f > DAY_F)[0]][::stride]
        case = Case(D, far)
        base = base_hours(case, hours)
        for label, size in sizes:
            r = energy_pass(case, size, hours, base, stride)
            en_rows.append({
                "code": code, "bus": far, "label": label, "size_kW": size,
                "E_avail_MWh": round(r["E_avail"] / 1000, 2),
                "E_vw_MWh": round(r["E_vw"] / 1000, 2),
                "curtailed_%": round(100 * (1 - r["E_vw"] / r["E_avail"]), 2) if r["E_avail"] else 0.0,
                "full_load_h_vw": round(r["E_vw"] / size, 0) if size else 0.0,
                "volt_h_nc": int(r["vh_nc"]), "therm_h_nc": int(r["th_nc"]),
                "volt_h_vw": int(r["vh_vw"]), "therm_h_vw": int(r["th_vw"]),
                "dLoss_nc_kWh": round(r["dL_nc"], 0), "dLoss_vw_kWh": round(r["dL_vw"], 0),
            })
            print(f"{code}: energy pass {label} ({size} kW), {(time.time() - t0) / 60:.1f} min",
                  flush=True)
    return grid, hc_rows, en_rows, round(time.time() - t0, 1), len(skip)


def md_table(df):
    cols = list(df.columns)
    lines = ["| " + " | ".join(str(c) for c in cols) + " |", "|" + "---|" * len(cols)]
    for _, r in df.iterrows():
        lines.append("| " + " | ".join(str(r[c]) for c in cols) + " |")
    return "\n".join(lines)


def write_summary(path, hc, en, a, seconds):
    out = ["# Time-series study results (script 12)", ""]
    out.append(f"Limits {V_LIMIT} pu and {LOADING_LIMIT:.0f} % (current-based). Q1 uses 15-minute "
               f"steps: critical set {a['k_crit']}, verification set {a['k_verify']} worst + "
               f"{a['k_rand']} random daylight steps. Q2 uses hourly means of daylight hours"
               + (f" (every {a['energy_stride']}th hour)" if a["energy_stride"] > 1 else "")
               + f". Tuned Volt-Watt {VW1} to {VW2} pu, floor {VW_FLOOR}. "
               + (f"Run time {seconds / 60:.1f} min." if seconds else ""))
    if not hc.empty:
        t = hc[["code", "bus", "z_ohm", "hc_snapshot", "hc_ts", "ratio_ts_snapshot", "binding_time",
                "binding_f", "limit", "refine_rounds", "unresolved_violations", "capped"]]
        out += ["", "## Q1: snapshot vs time-series hosting capacity (kW, no control)", "",
                md_table(t)]
        if (hc.full_check_steps != "").any():
            f = hc[hc.full_check_steps != ""][["code", "bus", "hc_ts", "full_check_steps",
                                                 "full_check_violations"]]
            out += ["", "## Full check on every daylight step", "", md_table(f)]
        g = hc.groupby("code").agg(median_ratio=("ratio_ts_snapshot", "median"),
                                   min_ratio=("ratio_ts_snapshot", "min"),
                                   max_ratio=("ratio_ts_snapshot", "max")).round(2).reset_index()
        out += ["", "Ratio time-series / snapshot per feeder:", "", md_table(g)]
    if not en.empty:
        out += ["", "## Q2: annual energy with the tuned Volt-Watt curve (far bus)", "",
                md_table(en)]
        rows = []
        for code, g in en.groupby("code"):
            g = g.sort_values("size_kW").reset_index(drop=True)
            for i in range(1, len(g)):
                dP = g.size_kW[i] - g.size_kW[i - 1]
                dE = (g.E_vw_MWh[i] - g.E_vw_MWh[i - 1]) * 1000
                rows.append({
                    "code": code, "from kW": g.size_kW[i - 1], "to kW": g.size_kW[i],
                    "extra energy kWh per extra kW": round(dE / dP, 0) if dP > 0 else "-",
                    "average full-load h at lower size": g.full_load_h_vw[i - 1],
                    "violation hours at larger size (volt/therm, with VW)":
                        f"{g.volt_h_vw[i]}/{g.therm_h_vw[i]}",
                })
        if rows:
            out += ["", "## Marginal energy of a larger nameplate", "", md_table(pd.DataFrame(rows))]
    with open(path, "w", encoding="utf-8") as f:
        f.write("\n".join(out) + "\n")


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--grids", nargs="+", default=GRIDS, choices=GRIDS)
    ap.add_argument("--workers", type=int, default=1)
    ap.add_argument("--k-crit", type=int, default=100)
    ap.add_argument("--k-verify", type=int, default=1500)
    ap.add_argument("--k-rand", type=int, default=500)
    ap.add_argument("--energy-stride", type=int, default=1)
    ap.add_argument("--skip-energy", action="store_true")
    ap.add_argument("--verify-full", action="store_true")
    ap.add_argument("--resume", action="store_true")
    ap.add_argument("--out", default="timeseries")
    args = ap.parse_args()
    a = dict(k_crit=args.k_crit, k_verify=args.k_verify, k_rand=args.k_rand,
             energy_stride=args.energy_stride, skip_energy=args.skip_energy,
             verify_full=args.verify_full)

    os.makedirs("results", exist_ok=True)
    p_hc, p_en = f"results/{args.out}_hc.csv", f"results/{args.out}_energy.csv"
    p_md = f"results/{args.out}_summary.md"
    hc = pd.read_csv(p_hc) if args.resume and os.path.exists(p_hc) else pd.DataFrame()
    en = pd.read_csv(p_en) if args.resume and os.path.exists(p_en) else pd.DataFrame()
    done = {c.split("--")[0].replace("1-LV-", "") for c in hc.code.unique()} if len(hc) else set()
    jobs = [(g, a) for g in args.grids if g not in done]
    print(f"feeders to run: {[j[0] for j in jobs]}, workers = {args.workers}", flush=True)

    t0 = time.time()
    hc_new, en_new = [], []

    def save():
        h = pd.concat([hc, pd.DataFrame(hc_new)], ignore_index=True)
        e = pd.concat([en, pd.DataFrame(en_new)], ignore_index=True)
        h.to_csv(p_hc, index=False, encoding="utf-8")
        e.to_csv(p_en, index=False, encoding="utf-8")
        return h, e

    if args.workers > 1 and len(jobs) > 1:
        ctx = multiprocessing.get_context("spawn")
        with ctx.Pool(min(args.workers, len(jobs))) as pool:
            for grid, h_rows, e_rows, sec, n_skip in pool.imap_unordered(run_feeder, jobs):
                hc_new += h_rows
                en_new += e_rows
                save()
                print(f"== {grid} finished in {sec / 60:.1f} min", flush=True)
    else:
        for job in jobs:
            grid, h_rows, e_rows, sec, n_skip = run_feeder(job)
            hc_new += h_rows
            en_new += e_rows
            save()
            print(f"== {grid} finished in {sec / 60:.1f} min", flush=True)

    h, e = save()
    write_summary(p_md, h, e, a, time.time() - t0)
    print(f"\nDone. Send me this file: {p_md}")
    print(f"Per-bus tables: {p_hc} and {p_en}")


if __name__ == "__main__":
    main()
