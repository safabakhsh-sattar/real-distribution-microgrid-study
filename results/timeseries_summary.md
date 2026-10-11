# Time-series study results (script 12)

Limits 1.05 pu and 100 % (current-based). Q1 uses 15-minute steps: critical set 100, verification set 1500 worst + 500 random daylight steps. Q2 uses hourly means of daylight hours. Tuned Volt-Watt 1.03 to 1.05 pu, floor 0.2. Run time 244.2 min.

## Q1: snapshot vs time-series hosting capacity (kW, no control)

| code | bus | z_ohm | hc_snapshot | hc_ts | ratio_ts_snapshot | binding_time | binding_f | limit | refine_rounds | unresolved_violations | capped |
|---|---|---|---|---|---|---|---|---|---|---|---|
| 1-LV-rural1--0-sw | 7 | 0.0051 | 82.0 | 175.7 | 2.14 | 20 May 12:00 | 0.569 | trafo | 0 | 0 | False |
| 1-LV-rural1--0-sw | 11 | 0.052 | 82.3 | 176.7 | 2.15 | 20 May 12:00 | 0.569 | trafo | 0 | 0 | False |
| 1-LV-rural1--0-sw | 4 | 0.2453 | 80.1 | 106.5 | 1.33 | 27 Jul 12:00 | 0.531 | voltage | 0 | 0 | False |
| 1-LV-semiurb5--0-sw | 74 | 0.0131 | 324.3 | 397.4 | 1.23 | 24 May 11:00 | 0.587 | line | 0 | 0 | False |
| 1-LV-semiurb5--0-sw | 72 | 0.1929 | 290.2 | 246.5 | 0.85 | 24 Jul 11:00 | 0.57 | voltage | 0 | 0 | False |
| 1-LV-semiurb5--0-sw | 51 | 0.3889 | 190.4 | 110.5 | 0.58 | 24 Jul 11:00 | 0.57 | voltage | 0 | 0 | False |
| 1-LV-urban6--0-sw | 54 | 0.014 | 265.5 | 439.3 | 1.65 | 24 May 11:00 | 0.582 | line | 1 | 0 | False |
| 1-LV-urban6--0-sw | 50 | 0.096 | 266.7 | 442.6 | 1.66 | 24 May 11:00 | 0.582 | line | 1 | 0 | False |
| 1-LV-urban6--0-sw | 17 | 0.2589 | 267.9 | 224.7 | 0.84 | 24 Jul 11:00 | 0.567 | voltage | 0 | 0 | False |

Ratio time-series / snapshot per feeder:

| code | median_ratio | min_ratio | max_ratio |
|---|---|---|---|
| 1-LV-rural1--0-sw | 2.14 | 1.33 | 2.15 |
| 1-LV-semiurb5--0-sw | 0.85 | 0.58 | 1.23 |
| 1-LV-urban6--0-sw | 1.65 | 0.84 | 1.66 |

## Q2: annual energy with the tuned Volt-Watt curve (far bus)

| code | bus | label | size_kW | E_avail_MWh | E_vw_MWh | curtailed_% | full_load_h_vw | volt_h_nc | therm_h_nc | volt_h_vw | therm_h_vw | dLoss_nc_kWh | dLoss_vw_kWh |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| 1-LV-rural1--0-sw | 4 | snapshot capacity | 80.1 | 51.98 | 47.6 | 8.42 | 594.0 | 0 | 0 | 0 | 0 | 451.0 | 328.0 |
| 1-LV-rural1--0-sw | 4 | time-series capacity | 106.5 | 69.11 | 59.99 | 13.19 | 563.0 | 0 | 0 | 0 | 0 | 790.0 | 496.0 |
| 1-LV-rural1--0-sw | 4 | 1.5 x larger capacity | 159.8 | 103.7 | 80.99 | 21.9 | 507.0 | 266 | 0 | 0 | 0 | 1753.0 | 843.0 |
| 1-LV-semiurb5--0-sw | 51 | snapshot capacity | 190.4 | 125.73 | 98.23 | 21.88 | 516.0 | 273 | 0 | 0 | 0 | 2031.0 | 947.0 |
| 1-LV-semiurb5--0-sw | 51 | time-series capacity | 110.5 | 72.97 | 64.67 | 11.38 | 585.0 | 0 | 0 | 0 | 0 | 698.0 | 449.0 |
| 1-LV-semiurb5--0-sw | 51 | 1.5 x larger capacity | 285.6 | 188.6 | 128.42 | 31.91 | 450.0 | 696 | 0 | 0 | 0 | 4476.0 | 1521.0 |
| 1-LV-urban6--0-sw | 17 | snapshot capacity | 267.9 | 176.79 | 149.16 | 15.63 | 557.0 | 49 | 0 | 0 | 0 | 1811.0 | 930.0 |
| 1-LV-urban6--0-sw | 17 | time-series capacity | 224.7 | 148.28 | 131.06 | 11.62 | 583.0 | 0 | 0 | 0 | 0 | 1155.0 | 668.0 |
| 1-LV-urban6--0-sw | 17 | 1.5 x larger capacity | 401.8 | 265.15 | 194.88 | 26.5 | 485.0 | 513 | 0 | 0 | 0 | 4686.0 | 1738.0 |

## Marginal energy of a larger nameplate

| code | from kW | to kW | extra energy kWh per extra kW | average full-load h at lower size | violation hours at larger size (volt/therm, with VW) |
|---|---|---|---|---|---|
| 1-LV-rural1--0-sw | 80.1 | 106.5 | 469.0 | 594.0 | 0/0 |
| 1-LV-rural1--0-sw | 106.5 | 159.8 | 394.0 | 563.0 | 0/0 |
| 1-LV-semiurb5--0-sw | 110.5 | 190.4 | 420.0 | 585.0 | 0/0 |
| 1-LV-semiurb5--0-sw | 190.4 | 285.6 | 317.0 | 516.0 | 0/0 |
| 1-LV-urban6--0-sw | 224.7 | 267.9 | 419.0 | 583.0 | 0/0 |
| 1-LV-urban6--0-sw | 267.9 | 401.8 | 341.0 | 557.0 | 0/0 |
