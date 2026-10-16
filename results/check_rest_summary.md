# Time-series study results (script 12)

Limits 1.05 pu and 100 % (current-based). Q1 uses 15-minute steps: critical set 100, verification set 1500 worst + 500 random daylight steps. Q2 uses hourly means of daylight hours. Tuned Volt-Watt 1.03 to 1.05 pu, floor 0.2. Run time 15.8 min.

## Q1: snapshot vs time-series hosting capacity (kW, no control)

| code | bus | z_ohm | hc_snapshot | hc_ts | ratio_ts_snapshot | binding_time | binding_f | limit | refine_rounds | unresolved_violations | capped |
|---|---|---|---|---|---|---|---|---|---|---|---|
| 1-LV-semiurb5--0-sw | 74 | 0.0131 | 324.3 | 397.4 | 1.23 | 24 May 11:00 | 0.587 | line | 0 | 0 | False |
| 1-LV-semiurb5--0-sw | 72 | 0.1929 | 290.2 | 246.5 | 0.85 | 24 Jul 11:00 | 0.57 | voltage | 0 | 0 | False |
| 1-LV-semiurb5--0-sw | 51 | 0.3889 | 190.4 | 110.5 | 0.58 | 24 Jul 11:00 | 0.57 | voltage | 0 | 0 | False |
| 1-LV-urban6--0-sw | 54 | 0.014 | 265.5 | 439.3 | 1.65 | 24 May 11:00 | 0.582 | line | 1 | 0 | False |
| 1-LV-urban6--0-sw | 50 | 0.096 | 266.7 | 442.6 | 1.66 | 24 May 11:00 | 0.582 | line | 1 | 0 | False |
| 1-LV-urban6--0-sw | 17 | 0.2589 | 267.9 | 224.7 | 0.84 | 24 Jul 11:00 | 0.567 | voltage | 0 | 0 | False |

Ratio time-series / snapshot per feeder:

| code | median_ratio | min_ratio | max_ratio |
|---|---|---|---|
| 1-LV-semiurb5--0-sw | 0.85 | 0.58 | 1.23 |
| 1-LV-urban6--0-sw | 1.65 | 0.84 | 1.66 |
