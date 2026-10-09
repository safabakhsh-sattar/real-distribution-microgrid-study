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