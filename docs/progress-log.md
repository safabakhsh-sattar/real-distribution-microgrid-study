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