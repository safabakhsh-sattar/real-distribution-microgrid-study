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