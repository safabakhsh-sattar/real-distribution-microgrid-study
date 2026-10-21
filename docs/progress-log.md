# Progress Log

## September 19, 2026
- Full project setup and folder structure
- First Load Flow executed on the base network — all voltages healthy (1.019-1.026 pu)
- Network topology confirmed: 15 buses, 13 lines, 1 transformer, 13 loads, total load 80 kW
- Next: Start Hosting Capacity analysis for PV

## September 23, 2026
- Calculated the electrical distance of each bus to the transformer (calc_distance_to_bus)
- Quantitative confirmation of the hypothesis: buses 4 and 5 (farthest electrical distance) = lowest hosting capacity
- Summarized and critiqued 2 articles related to Volt-VAr Control (papers summary.md)
- Next: Write Volt-VAr control script on SimBench network

## September 24, 2026
- Fixed CSV read/write bug (invalid UTF-8 character from terminal output)
- Successful execution of Volt-VAr Control script (IEEE 1547 standard curve)
- Completed full baseline vs. Volt-VAr comparison:
  - Critical buses (4, 5): ~26-27% improvement (80 → 101-102 kW)
  - Best improvement: bus 12 at 54%
  - Network-wide average improvement: ~45%
  - 7 buses reached the 300 kW search ceiling — need higher ceiling for exact values
- Next: raise search ceiling, write docs/methodology.md, start Week 2

## September 26, 2026
- Added thermal loading (line + transformer) constraints to hosting capacity search
- Converted linear search to binary search (faster, more precise)
- Diagnosed root cause: transformer at 98.8% loading is the binding constraint,
  not line thermal limits or electrical distance
- Key finding: Volt-VAr control can slightly reduce hosting capacity when the
  binding constraint is transformer thermal loading (apparent power increases
  with added Q), reversing its benefit
- Created docs/methodology.md documenting full analysis approach
- Next: implement Volt-Watt control as alternative, compare against Volt-VAr

## September 27, 2026
- Finalized docs/methodology.md with full transformer-bottleneck finding
- Volt-Watt control parked due to numerical oscillation (documented as future work)
- Week 2 core deliverable (Volt-VAr + thermal analysis) closed
- Next: start daily language practice, then revisit Volt-Watt with damping fix

## October 2, 2026
- Completed paper draft: Discussion (updated with confirmed Volt-Watt
  results), Conclusion, and Abstract sections written
- Full paper draft now complete end-to-end (Abstract through References)
- Next: full read-through and revision pass, then decide on next phase
  (submission target, or extend scope to EV/storage)

## October 3, 2026
- Added validation test on second SimBench feeder (1-LV-urban6--0-sw)
- Key finding: binding constraint is topology-dependent — transformer
  dominates in rural (single-transformer) feeder, lines dominate in
  urban (distributed) feeder
- Added Section 3.4 (Validation) to paper-draft.md
- Decision: Volt-VAr/Volt-Watt comparison on urban feeder deferred —
  current finding is sufficient to close this phase
- Next: decide between (a) closing paper draft as-is, (b) extending
  with urban VAr/Watt test, or (c) starting language per user's own timing.

## October 7, 2026
- Recomputed rural no-control baseline under voltage + thermal limits (fair comparison): 80.1–82.0 kW
- Confirmed: Volt-VAr is below no-control at all 13 rural buses (1.0–2.9 kW lower)
- Confirmed: all lines are NAYY 4x150SE, so path length (km) is proportional to path impedance
- Issue found: Volt-Watt equals no-control at every bus (13/13 rural, 53/53 urban).
  Cause: feasibility limit (1.05 pu) is below the IEEE 1547 default Volt-Watt
  activation point (1.06 pu), so Volt-Watt never curtails inside the feasible region
- Correction: 1.05 pu is a conservative planning limit, not the EN 50160 limit (±10%)
- Paper claims on Volt-Watt superiority on hold until sensitivity analysis (scripts/08)

## October 7, 2026 (sensitivity analysis)
- Ran 7-scenario sensitivity on rural feeder (scripts/08_sensitivity_rural.py)
- Self-check passed: NC_1.05 reproduces 02b results within search resolution (≤0.6 kW)
- Findings:
  - Feeder is transformer-bound at ~80-83 kW regardless of control or voltage limit (1.05 / 1.10)
  - Default Volt-VAr reduces HC by 1.4-3.5% at all 13 buses, under both limits
  - Default Volt-Watt is inert: its 1.06 pu activation is reached only above the thermal limit
  - Tuned Volt-Watt (1.03-1.05 pu) raises nameplate HC from ~81 kW to 91-403 kW,
    scaling with distance, while peak delivered power stays at the transformer limit
- Old headline ("Volt-Watt outperforms Volt-VAr") retired; paper to be rewritten once after final runs
- Next: final rural run at 0.1 kW resolution, urban sensitivity run

## October 7, 2026 (final runs and paper rewrite)
- Reran rural sensitivity at 0.1 kW tolerance and ran urban sensitivity (53 buses, 7 scenarios); urban results match an independent cloud run to 0.0 kW
- Rural: no control 80.1-82.7 kW (1.05 pu), 82.0-83.1 kW (1.10 pu); Volt-VAr -1.5% to -3.6%; Volt-Watt default = no control; Volt-Watt adapted nameplate 91.1-403.5 kW, delivered within 0.1 kW
- Urban: no control 252.5-371.8 kW; Volt-VAr lower at 27/53 buses (max -1.53%), equal at 26; Volt-Watt default = no control at 53/53; adapted nameplate up to 568.7 kW (bus 17), delivered within 0.1 kW
- Correction to the earlier entry: the rural feeder is not transformer-bound at every bus. Buses 4 and 5 are voltage-bound at 1.05 pu (by 3.0 and 2.4 kW)
- Found: SimBench base networks already contain PV (rural 160.4 kW, urban 57.1 kW). HC is additional PV on top of this, in a single snapshot. Added to paper (Section 2.1, limitations)
- Paper rewritten with final results; figures 1 and 2 regenerated from the sensitivity CSVs
- Open: sync docs/methodology.md, direct trafo Q/S check, time-series analysis. Language not started (user will announce)

## October 9, 2026 (direct transformer measurement)
- Added scripts/10_trafo_pqs_rural.py: transformer P, Q, S at the LV terminal with and without Volt-VAr (13 rural buses, 3 cases each); output results/trafo_pqs_rural.csv
- Result: at the same PV size Volt-VAr leaves transformer active power unchanged (0.0 to -0.15 kW) and raises the reactive power it supplies by 6.6-14.8 kvar; loading rises from 98.3-100.0% to 100.7-101.8%, so the no-control size is infeasible at 13/13 buses; at the Volt-VAr limit loading is back at 100% with 1.2-3.0 kW less PV
- Correction: pandapower transformer loading is current-based (default), not apparent-power-based as written earlier; at LV voltage about 1.03 pu, 100% loading is about 103% of rated S. Documents corrected; sensitivity to a power-based criterion not evaluated
- Correction: documents gave the rural search ceiling as 600 kW, scripts use 2000 kW; results unchanged (script 10 reproduces the committed CSV to 0.0 kW)
- Synced: methodology (decision log steps 11-13), paper (Section 3.6, Discussion, Conclusion, limitation 7), README, defense sheet
- Open: time-series analysis, urban line-current check, storage/EV. Language not started (user will announce)

## October 9, 2026 (urban line measurement)
- Added scripts/10b_line_pqs_urban.py: most loaded line P, Q, I and transformer loading at 53 urban buses, 3 cases each; output results/line_pqs_urban.csv; capacity limits reproduce sensitivity_urban.csv to 0.0 kW
- Result: same mechanism as rural. At 27 buses (PV-bus voltage 1.0204-1.0432 pu at the no-control limit) Volt-VAr absorbs 0.7-31.8 kvar, which flows through the limiting line at unchanged active power; line current +0.07 to +5.8 A, loading up to 101.6%. At 26 buses (voltage at most 1.0203 pu, dead band) Q is about 0 and capacity is unchanged
- Transformer stays below 40% in all cases (28-36% without control, up to 39.6% with Volt-VAr); the limiting line is the same with and without Volt-VAr at every bus
- Synced: paper (3.6, Discussion, Conclusion), methodology (step 14), README, defense sheet
- Open: time-series, storage/EV, power-based transformer criterion. Language not started (user will announce)

## October 10, 2026 (central question and six-network snapshot)
- Central question set: when does the default Volt-VAr curve help or hurt PV hosting capacity in LV feeders, and can a simple indicator predict it?
- Added scripts/11_multi_feeder_snapshot.py: six SimBench networks, 113 buses, six capacities per bus (voltage only, thermal only, both, with and without Volt-VAr); hypothesis written in the script before the run; run time 57 min; reproduces script 10 at the rural buses to 0.0 kW
- Result: thermal limit first at 89 of 113 buses, voltage first at 24. Volt-VAr higher at 0 of 89 (thermal first) and at 21 of 24 (voltage first, median +17.6%). hc_vvar = min(hc_v_vvar, hc_t_vvar) at 113 of 113 buses
- Screening indicator r = hc_t / hc_v: 0 of 89 gained for r < 1, 19 of 19 for r >= 1.05, mixed between 1.00 and 1.05. Dead band: 20 of 20 unchanged. Thermal element: transformer on rural1 only (13 of 13), line on the other five networks (100 of 100)
- Correction: the first summary reported a "gain" at buses where the voltage limit does not bind (Volt-VAr iteration does not converge at PV sizes of roughly 600-1000 kW); gain now reported only for voltage-first buses, `--summarize-only` added; hc_vvar unaffected
- Consequence: the "shared transformer bottleneck" claim of Study 1 is restricted to rural1

## October 11, 2026 (time series, three feeders)
- Added scripts/12_timeseries.py: one year of 15-minute SimBench profiles on rural1, semiurb5 and urban6; capacity by a critical-step method with a verification set; energy, curtailment, violation hours and losses with the tuned Volt-Watt curve at the far bus; run time 244 min in one process (the estimate of about one hour was wrong)
- Correction during development: a first version rounded the capacity up and a full check of rural1 bus 4 found 1 violating step of 14,278 at 106.6 kW; result now rounded down (106.5 kW, 0 violations)
- Result: time-series capacity is 1.23 to 2.15 times the snapshot value at line- or transformer-limited buses and 0.58 to 0.85 times at voltage-limited buses of semiurb5 and urban6 (1.33 on rural1 bus 4). Sizing by the snapshot gave 273 h (semiurb5 bus 51) and 49 h (urban6 bus 17) per year above 1.05 pu
- Tuned Volt-Watt: no hourly violation in nine cases, curtailment 8% to 32%, extra energy per extra kW 61% to 79% of the average, added losses 27% to 66% lower than without control
- Open: Volt-VAr over the year was not simulated

## October 11, 2026 (paper restructured, figures, documents)
- Paper rewritten around the central question: new title, abstract, contributions; Methods 2.6 and 2.7; Results 3.7 and 3.8; Discussion, Limitations, Conclusion and Future Work revised
- Added scripts/12b_binding_conditions.py (load and PV factor at the binding step, makes Table 11 reproducible) and scripts/13_figures_study2.py (figures 4 to 6)
- Synced: methodology (decision-log steps 15-20, new Sections 8 and 9), README (key findings, script table, limitations, status), weekly reviews
- Open: own reading of the new paper and oral drill; Volt-VAr over the year; inverter apparent-power limit; storage and EV after week 8

## October 21, 2026 (Volt-VAr over the year, checks, paper and weekly review)
- Added scripts/14_vvar_annual.py (hourly, far buses): almost all voltage-violation hours removed at the snapshot sizes; added losses 16.2% to 29.0% higher with Volt-VAr in all nine cases; 0 failed power flows
- Added scripts/15_vvar_timeseries_hc.py (15-minute steps, far buses, every daylight step checked at the final capacity): Volt-VAr capacity over the year 165.1 kW (rural1, +55.0%), 174.1 kW (semiurb5, +57.6%), 390.8 kW (urban6, +73.9%); 0 unresolved violations; no non-converged power flow at or below capacity
- Added scripts/16_vvar_snapshot_check.py: the Volt-VAr code reproduces the script 11 values at the three far buses (match: True); the snapshot-to-year gap is not a coding error
- Added scripts/17_snapshot_condition.py: the highest year PV is 57.6% to 58.6% of the snapshot PV; no quarter hour reaches 90% of it; stored loads are 1.08 to 2.37 times the year's peak
- Finding: the snapshot indicator r did not predict the year sign at two of three far buses (urban6 r = 0.885, year +73.9%; rural1 snapshot -1.5%, year +55.0%). Reported as a limitation; the indicator stays a snapshot result
- Paper updated (abstract, contributions, Sections 2.7, 3.9, discussion, limitations, conclusion); committed and pushed (commit 0e10167)
- Week 6 review written to docs/weekly-reviews.md (commit 25c6cac)
- Synced: README, methodology (Section 9, decision log steps 21-24, verification checks, limitations), this log, and the time-series design note (marked superseded)
- Open: Week 7 checklist (commit these documents); defense sheet in Week 8