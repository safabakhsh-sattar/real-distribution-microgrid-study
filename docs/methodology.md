# Methodology

Technical record of the method used in the hosting-capacity study, including
the decisions taken and the reasons. The paper
([paper-draft.md](paper-draft.md)) presents the final method; this document
also records how it was reached. Sections 1 to 7 describe Study 1 (two
feeders, snapshot); Section 8 describes Study 2a (six networks, snapshot,
script 11) and Section 9 Study 2b (three feeders, one year of profiles,
scripts 12 and 12b).

## 1. Networks and operating point

Source: SimBench dataset, loaded with `simbench.get_simbench_net(code)`.
Power flow: pandapower, Newton-Raphson, balanced single-phase equivalent.

| Item | Rural `1-LV-rural1--0-sw` | Urban `1-LV-urban6--0-sw` |
|---|---|---|
| Buses / lines | 15 buses, 13 lines | 53 load buses |
| Transformer | 1 x 160 kVA | 1 x 630 kVA |
| Loads | 13 loads, 80 kW | 111 loads, 441 kW |
| Existing PV | 4 units, 160.4 kW | 5 units, 57.1 kW |
| Slack voltage | 1.025 pu | 1.025 pu |
| Base-case transformer loading | 52.5% (transformer export 78.9 kW at the HV side; bus balance 80.4 kW; the 1.4 kW difference is network losses) | 67.7% (transformer import 392.2 kW at the HV side; bus balance 383.9 kW; the 8.3 kW difference is network losses) |
| Line type (rural) | all NAYY 4x150SE | not checked |

Operating point: the values stored in the SimBench files (loads and existing
PV as stored). The SimBench study-case scaling factors (for example low load
with high PV, slack 1.055 pu) are **not** applied. Hosting capacity is
therefore the additional PV connectable at one bus on top of the existing
generation, in one snapshot.

Why SimBench: open and reproducible, based on German DSO planning principles,
no confidentiality restrictions.

## 2. Constraints

| Constraint | Value | Note |
|---|---|---|
| Maximum bus voltage | 1.05 pu | Conservative planning limit. **Not** the EN 50160 limit (+/-10%, i.e. 1.10 pu) |
| Voltage sensitivity | 1.10 pu | Evaluated for no control, Volt-VAr and Volt-Watt default |
| Line loading | 100% | `res_line.loading_percent` (current-based) |
| Transformer loading | 100% | `res_trafo.loading_percent` (current-based, pandapower default: larger of HV and LV current relative to rated current; at an LV voltage of about 1.03 pu, 100% corresponds to about 103% of rated apparent power) |

Only the upper voltage limit is enforced because PV injection raises
voltages. A candidate PV size is feasible only if voltage and both thermal
limits hold at the same time.

## 3. Hosting capacity definition and search

- For each load bus, a PV generator (sgen) of size P_n is added to a deep copy of the base network.
- **Nameplate HC** is the largest feasible P_n. **Delivered HC** is the active power actually injected at that size after any curtailment.
- Search: binary search on P_n, tolerance 0.1 kW, upper bound 2000 kW on all networks.
- Assumption: feasibility is monotonic in P_n (larger PV never restores feasibility). Fine for a radial feeder with one added injection.
- An evaluation that raises an exception (non-convergence) counts as infeasible.
- Electrical distance: `calc_distance_to_bus` from the transformer LV bus. It returns **path length in km**, not impedance. On the rural feeder all lines are the same cable type, so path length is proportional to path impedance and is a valid proxy.

## 4. Control scenarios

Only the added PV unit is controlled; existing PV is uncontrolled. Reactive
power is expressed per unit of PV nameplate; no inverter apparent-power limit
is imposed.

| Scenario | Definition |
|---|---|
| NC | Unity power factor |
| VVAR | IEEE 1547-2018 default Volt-VAr: V = (0.92, 0.98, 1.02, 1.08) pu, Q = (+0.44, 0, 0, -0.44) of nameplate |
| VW default | IEEE 1547-2018 default Volt-Watt: curtailment from 1.06 pu, floor 0.2 at 1.10 pu |
| VW adapted | Same shape, curtailment from 1.03 pu, floor 0.2 at 1.05 pu |

**Volt-VAr solution.** Voltage and Q depend on each other, so the power flow
is iterated: run power flow, read the voltage at the PV bus, set Q from the
curve, repeat. Up to 20 iterations, stop when Q changes by less than
0.1 kvar. No convergence means infeasible.

**Volt-Watt solution.** The delivered power satisfies
P = P_n * r(V(P)), where r is the curtailment ratio. It is solved by
bisection on P. Voltage rises with P and r falls with voltage, so the residual
P_n * r(V(P)) - P is strictly decreasing in P and the root is unique.

## 5. History of the method (decision log)

The sequence below is kept deliberately, because several early results were
wrong or misleading and were corrected.

| Step | What was done | What went wrong or was learned | Decision |
|---|---|---|---|
| 1 | Voltage-only baseline, linear search in 1 kW steps | Slow; HC 80 kW (buses 4, 5) to 286 kW (bus 7) | Keep as the voltage-only reference (Section 3.1 of the paper) |
| 2 | Volt-VAr with a fixed upper bound | Several buses returned the search bound itself (100/300/1000 kW) - no real limit found | Treat bound hits as artifacts; add a second constraint |
| 3 | Added thermal limits (lines and transformer) | Transformer became the binding element on the rural feeder (script 03b printed 98.8% transformer vs 82% most loaded line) | Always enforce voltage and thermal together |
| 4 | Linear search replaced by binary search | About 10 power flows per bus instead of up to 1000 | Binary search with tolerance (1 kW, later 0.1 kW) |
| 5 | Volt-Watt by plain iteration | Oscillated between full output and the 20% floor | First fix: damping (alpha = 0.3) |
| 6 | Compared VAr and Watt against the voltage-only baseline | Unfair: baseline ignored thermal limits | Recompute no-control baseline with voltage + thermal (script 02b) |
| 7 | Fair comparison | Volt-Watt equalled no control at every bus | Cause: 1.05 pu feasibility limit is below the 1.06 pu Volt-Watt activation, so it never curtails inside the feasible region. The "Volt-Watt superiority" claim was withdrawn |
| 8 | Voltage limit labelled "EN 50160" | Incorrect: EN 50160 allows +/-10% | 1.05 pu is a planning limit; 1.10 pu added as sensitivity |
| 9 | Sensitivity analysis (scripts 08, 08b) | Needed a Volt-Watt that works when the curve is active, and a nameplate vs delivered distinction | Volt-Watt equilibrium by bisection; report both nameplate and delivered capacity; add the adapted curve |
| 10 | Checked what the SimBench base nets contain | The nets already include PV (rural 160.4 kW, urban 57.1 kW) | State the operating point explicitly; HC is additional PV; single-snapshot limitation added |
| 11 | Measured transformer P, Q and S with and without Volt-VAr (script 10, rural) | Active power unchanged; reactive power supplied to the LV network up by 6.6–14.8 kvar; loading above 100% at the no-control size at all 13 buses | Volt-VAr reduction attributed to added reactive flow (rural); urban measured in step 14 |
| 12 | Checked how pandapower computes transformer loading | Default is current-based, not apparent-power-based as written earlier; at 100% loading S is about 103% of rating (LV voltage about 1.03 pu) | Definition corrected in all documents; sensitivity to a power-based criterion left open |
| 13 | Compared documented search ceiling with the scripts | Documents said 600 kW (rural); the scripts use 2000 kW. Script 10 (2000 kW) reproduces the committed rural CSV to 0.0 kW | Documents corrected to 2000 kW on both feeders |
| 14 | Measured limiting-line current with and without Volt-VAr (script 10b, urban) | The 26 equal-capacity buses have a PV-bus voltage of at most 1.0203 pu at the no-control limit (dead band, Q about 0); at the 27 lower buses the absorbed Q (0.7–31.8 kvar) flows through the limiting line at unchanged P and its current rises | Same mechanism confirmed on the urban feeder; the 27/26 split explained |
| 15 | Ran the six-network snapshot study (script 11, 113 buses) to test the hypothesis "Volt-VAr helps only where the voltage limit binds first" | Thermal first at 89 buses, voltage first at 24; Volt-VAr higher at 0 of 89 and 21 of 24 respectively; the thermal element is the transformer only on rural1 and a line on the other five networks | Hypothesis supported in this sample; the "shared transformer bottleneck" claim is restricted to rural1 |
| 16 | First summary of script 11 reported a "gain" at buses where the voltage limit does not bind | There hc_v is several hundred kW or more and the Volt-VAr iteration may not converge (urban6 bus 54), so hc_v_vvar is a numerical limit | Gain reported only for voltage-first buses; `--summarize-only` added to rebuild the summary from the saved CSV; hc_vvar itself unaffected |
| 17 | Looked for a simple indicator | r = hc_t / hc_v separates the outcomes (0 of 89 for r < 1; 19 of 19 for r >= 1.05); the threshold follows from min(hc_v (1+g), hc_t (1-p)) > hc_v, i.e. r > 1/(1-p) | Reported as sample-specific, not a general constant |
| 18 | Time-series capacity (script 12) by a critical-step method | A full check of rural1 bus 4 at 106.6 kW found 1 violating step of 14,278: the result had been rounded up | Result rounded down (106.5 kW); full check then 0 violations |
| 19 | Planned run time for script 12 was "about one hour" | Measured 244 min in one process (rural1 69, semiurb5 90, urban6 85 min) | Docstring corrected; `--resume` and `--workers` documented |
| 20 | Compared snapshot and time-series capacity | The ratio is above 1 where a line or the transformer binds (1.23-2.15) and below 1 at voltage-limited far buses of semiurb5 and urban6 (0.58-0.85) | Script 12b added to show PV factor and load at the binding step; explanation stated as consistent with the data, not a formal decomposition |

## 6. Verification checks performed

- The rural no-control result at 1.05 pu from script 08 reproduces the script 02b baseline within the 1 kW resolution of 02b (all differences are below 1 kW).
- Urban results from script 08b (7 scenarios, 53 buses, 371 rows) were reproduced in an independent run in a separate environment with a maximum difference of 0.0 kW.
- Script 10 (rural) reproduces the no-control and Volt-VAr capacity limits of `sensitivity_rural.csv` at all 13 buses with 0.0 kW difference, and its printed tables from a second computer are identical to the first run.
- Script 10b (urban) reproduces the no-control and Volt-VAr capacity limits of `sensitivity_urban.csv` at all 53 buses with 0.0 kW difference.
- At 1.10 pu, Volt-VAr results equal those at 1.05 pu at every bus on both feeders. This is consistent with thermal-limited behaviour.
- Volt-Watt default equals no control at every bus at both limits (13 of 13 rural, 53 of 53 urban), as expected when the curve is not activated.
- Script 11 reproduces the no-control and Volt-VAr capacities of script 10 at the 13 rural buses with 0.0 kW difference.
- Script 11: hc_nc = min(hc_v, hc_t) and hc_vvar = min(hc_v_vvar, hc_t_vvar), each within 0.2 kW, at 113 of 113 buses. At 7 buses at least one search reached the 2000 kW ceiling.
- Script 12: for rural1 bus 4 the capacity of 106.5 kW was checked on all 14,278 daylight steps with 0 violations (the earlier rounded-up value 106.6 kW had 1). For all nine buses the capacity holds on the verification set (0 unresolved violations, none at the 2000 kW ceiling).
- Script 12b asserts that the binding time stamps of `timeseries_hc.csv` match the profile index.

## 7. Known limitations and open items

1. Study 1 and Study 2a are single snapshots at the stored SimBench operating point; study cases are not evaluated. Study 2b uses annual profiles on three feeders only (three buses per feeder for capacity, the far bus for energy).
2. Existing PV is uncontrolled; network-wide control is not modelled.
3. No inverter apparent-power limit; no P-priority or Q-priority.
4. Balanced single-phase model; phase imbalance not modelled.
5. Study 1: two feeders. Study 2a: 113 buses of six networks (all 13 buses of rural1, 20 evenly spaced buses of each other network), scenario 0 only; the counts are sample counts, not probabilities, and the indicator was not tested on other networks.
6. The cause of the Volt-VAr reduction was measured on both feeders. Rural (script 10): active power through the transformer unchanged, reactive power supplied to the LV network up by 6.6–14.8 kvar, loading up by 1.0–1.8 percentage points at the same PV size. Urban (script 10b): active power through the limiting line unchanged, the absorbed reactive power (up to 31.8 kvar) flows through it, and Volt-VAr is inactive at the 26 buses whose voltage stays at or near the dead band (at most 1.0203 pu).
7. Scripts 03 to 06 use the earlier Volt-Watt implementation (damped iteration, first no-control baseline). The paper uses scripts 08 and 08b.
8. Transformer loading is current-based; a criterion on apparent power would be stricter by about 3% at the LV voltage found at the limit. The effect on the HC values has not been evaluated.
9. Time series (Study 2b): one weather year (2016); one fleet-average PV profile for the added unit; hourly means for energy, violation hours and losses (15-minute peaks are hidden); the capacity search is a critical-step method with a verification set, validated on the full year for one bus only; steps that already violate a limit without the added PV are excluded.
10. Volt-VAr was not simulated in the time series; the central question is answered with snapshots.
11. The explanation of the snapshot-to-time-series ratio (PV factor and load at the binding step) is consistent with the numbers but is not a formal decomposition.
12. Absolute energy values depend on the SimBench PV profile (about 650-660 kWh per kW of nameplate) and should be read as relative.

## 8. Study 2a: six-network snapshot (script 11)

- Networks: rural1, rural2, rural3, semiurb4, semiurb5, urban6, scenario 0 (`-sw`). The base case of all six satisfies both limits (otherwise the network would be skipped and reported).
- Buses: all 13 load buses of rural1; 20 load buses of each other network, evenly spaced by electrical distance (`calc_distance_to_bus` with impedance weight) from the transformer. 113 buses.
- Per bus six capacities: hc_v, hc_t, hc_nc, hc_vvar, hc_v_vvar, hc_t_vvar (voltage only, thermal only, both; without control and with Volt-VAr). Search and Volt-VAr model as in Sections 3 and 4. The two Volt-VAr split searches use a warm bracket (start from the no-control value, step 1.3) to save power flows; this changes the cost, not the result.
- Derived: first limit (voltage / thermal / both, 0.2 kW), effect (higher / equal / lower, 0.2 kW), thermal element, PV-bus voltage at hc_nc, r = hc_t / hc_v, gain (voltage-first buses only), penalty.
- Flags: `--grids`, `--scenarios`, `--workers`, `--per-grid` (default 20), `--out`, `--resume`, `--summarize-only`.
- Outputs: `results/multi_feeder_snapshot.csv`, `results/multi_feeder_summary.md`. Run time 57 min on a Windows PC.
- Hypothesis (set in the script before the run): Volt-VAr helps when the voltage limit binds first and does not help, or lowers the capacity, when a thermal limit binds first.

## 9. Study 2b: time series (scripts 12 and 12b)

- Feeders: rural1, semiurb5, urban6 (scenario 0); three load buses each (near, middle, far by impedance distance); the far bus for energy.
- Profiles: `simbench.get_absolute_values` (35,136 steps of 15 minutes, leap year 2016). The added PV follows f(t) = sum of the existing PV profiles / sum of their nameplates (maximum 0.576 on rural1, 0.587 on semiurb5, 0.582 on urban6). Existing PV uncontrolled.Daylight steps (f > 0.001): 14,278 on rural1, 15,035 on semiurb5 and urban6.The verification set has 1,947 to 1,955 unique steps (the 1,500 worst and 500 random steps, duplicates removed).
- Q1, capacity without control on 15-minute steps: rank daylight steps by net feeder injection plus a share of the added PV; critical set of the worst 100; bisection on the critical set; verification set of the worst 1500 and 500 random daylight steps; violators are added to the critical set and the search repeats (up to 8 rounds); result rounded down to 0.1 kW. Base-violating steps are excluded and counted. `--verify-full` checks all daylight steps.
- Q2, energy on hourly means of daylight hours at three sizes (snapshot capacity, time-series capacity, 1.5 times the larger): available energy, delivered energy with the tuned Volt-Watt curve (1.03-1.05 pu, floor 0.2; equilibrium by bisection per hour), curtailed share, full-load hours, hours with a violated limit (counted only if not already violated without the added PV), added losses (with minus without the added PV), marginal energy per extra kW.
- Flags (script 12): `--grids`, `--workers`, `--k-crit 100`, `--k-verify 1500`, `--k-rand 500`, `--energy-stride 1`, `--skip-energy`, `--verify-full`, `--resume`, `--out`.
- Outputs: `results/timeseries_hc.csv`, `results/timeseries_energy.csv`, `results/timeseries_summary.md`. Run time 244 min in one process on a Windows PC (rural1 69, semiurb5 90, urban6 85 min).
- Script 12b: `results/binding_conditions.csv` and `.md` (stored load, profile peak, load and PV factor at each binding step). About 1 minute.
- Figures 4 to 6: script 13 (`scripts/13_figures_study2.py`).

## 10. Reproducibility

Script order, outputs and requirements are listed in the repository
[README](../README.md). All results are produced from the open SimBench data
with the scripts in `scripts/`; no proprietary data is used.