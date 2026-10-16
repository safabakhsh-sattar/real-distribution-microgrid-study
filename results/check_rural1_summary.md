# Time-series study results (script 12)

Limits 1.05 pu and 100 % (current-based). Q1 uses 15-minute steps: critical set 100, verification set 1500 worst + 500 random daylight steps. Q2 uses hourly means of daylight hours. Tuned Volt-Watt 1.03 to 1.05 pu, floor 0.2. Run time 4.4 min.

## Q1: snapshot vs time-series hosting capacity (kW, no control)

| code | bus | z_ohm | hc_snapshot | hc_ts | ratio_ts_snapshot | binding_time | binding_f | limit | refine_rounds | unresolved_violations | capped |
|---|---|---|---|---|---|---|---|---|---|---|---|
| 1-LV-rural1--0-sw | 7 | 0.0051 | 82.0 | 175.7 | 2.14 | 20 May 12:00 | 0.569 | trafo | 0 | 0 | False |
| 1-LV-rural1--0-sw | 11 | 0.052 | 82.3 | 176.7 | 2.15 | 20 May 12:00 | 0.569 | trafo | 0 | 0 | False |
| 1-LV-rural1--0-sw | 4 | 0.2453 | 80.1 | 106.5 | 1.33 | 27 Jul 12:00 | 0.531 | voltage | 0 | 0 | False |

Ratio time-series / snapshot per feeder:

| code | median_ratio | min_ratio | max_ratio |
|---|---|---|---|
| 1-LV-rural1--0-sw | 2.14 | 1.33 | 2.15 |
