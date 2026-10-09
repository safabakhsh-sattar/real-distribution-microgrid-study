# Methodology

Technical record of the method used in the hosting-capacity study, including
the decisions taken and the reasons. The paper
([paper-draft.md](paper-draft.md)) presents the final method; this document
also records how it was reached.

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
| Base-case transformer loading | 52.5% (net export 78.9 kW) | 67.7% (net import 392.2 kW) |
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
- Search: binary search on P_n, tolerance 0.1 kW, upper bound 2000 kW on both feeders.
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

## 6. Verification checks performed

- The rural no-control result at 1.05 pu from script 08 reproduces the script 02b baseline within the 1 kW resolution of 02b (all differences are below 1 kW).
- Urban results from script 08b (7 scenarios, 53 buses, 371 rows) were reproduced in an independent run in a separate environment with a maximum difference of 0.0 kW.
- Script 10 (rural) reproduces the no-control and Volt-VAr capacity limits of `sensitivity_rural.csv` at all 13 buses with 0.0 kW difference, and its printed tables from a second computer are identical to the first run.
- Script 10b (urban) reproduces the no-control and Volt-VAr capacity limits of `sensitivity_urban.csv` at all 53 buses with 0.0 kW difference.
- At 1.10 pu, Volt-VAr results equal those at 1.05 pu at every bus on both feeders. This is consistent with thermal-limited behaviour.
- Volt-Watt default equals no control at every bus at both limits (13 of 13 rural, 53 of 53 urban), as expected when the curve is not activated.

## 7. Known limitations and open items

1. Single snapshot at the stored SimBench operating point; study cases and annual profiles are not evaluated.
2. Existing PV is uncontrolled; network-wide control is not modelled.
3. No inverter apparent-power limit; no P-priority or Q-priority.
4. Balanced single-phase model; phase imbalance not modelled.
5. Two feeders only.
6. The cause of the Volt-VAr reduction was measured on both feeders. Rural (script 10): active power through the transformer unchanged, reactive power supplied to the LV network up by 6.6–14.8 kvar, loading up by 1.0–1.8 percentage points at the same PV size. Urban (script 10b): active power through the limiting line unchanged, the absorbed reactive power (up to 31.8 kvar) flows through it, and Volt-VAr is inactive at the 26 buses whose voltage stays at or near the dead band (at most 1.0203 pu).
7. Scripts 03 to 06 use the earlier Volt-Watt implementation (damped iteration, first no-control baseline). The paper uses scripts 08 and 08b.
8. Transformer loading is current-based; a criterion on apparent power would be stricter by about 3% at the LV voltage found at the limit. The effect on the HC values has not been evaluated.

## 8. Reproducibility

Script order, outputs and requirements are listed in the repository
[README](../README.md). All results are produced from the open SimBench data
with the scripts in `scripts/`; no proprietary data is used.