# Volt-VAr over one year, far bus of each feeder (script 14)

Time resolution: hour (8,784 hourly means).
Limits: 1.05 pu voltage, 100 % current-based loading. Volt-VAr: IEEE 1547 default curve, Q = ratio(V) x nameplate.

## Results

| code | bus | step | size_label | size_kW | E_avail_MWh | Q_supplied_kvarh | Q_absorbed_kvarh | hours_volt_nc | hours_therm_nc | hours_volt_vvar | hours_therm_vvar | dLoss_nc_kWh | dLoss_vvar_kWh | deadband_steps |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| 1-LV-rural1--0-sw | 4 | hour | snapshot capacity | 80.1 | 51.98 | 0.0 | 12011.6 | 0.0 | 0.0 | 0.0 | 0.0 | 451.0 | 524.1 | 3925 |
| 1-LV-rural1--0-sw | 4 | hour | time-series capacity | 106.5 | 69.11 | 0.0 | 19128.8 | 0.0 | 0.0 | 0.0 | 0.0 | 790.4 | 932.9 | 3828 |
| 1-LV-rural1--0-sw | 4 | hour | 1.5 x larger capacity | 159.8 | 103.7 | 0.0 | 36759.1 | 266.0 | 0.0 | 0.0 | 0.0 | 1752.8 | 2148.5 | 3667 |
| 1-LV-semiurb5--0-sw | 51 | hour | snapshot capacity | 190.4 | 125.73 | 0.0 | 45705.1 | 273.0 | 0.0 | 3.0 | 0.0 | 2030.7 | 2470.3 | 3258 |
| 1-LV-semiurb5--0-sw | 51 | hour | time-series capacity | 110.5 | 72.97 | 0.0 | 19638.0 | 0.0 | 0.0 | 0.0 | 0.0 | 698.2 | 811.3 | 3423 |
| 1-LV-semiurb5--0-sw | 51 | hour | 1.5 x larger capacity | 285.6 | 188.6 | 0.0 | 84736.2 | 696.0 | 0.0 | 118.0 | 0.0 | 4476.4 | 5775.7 | 3153 |
| 1-LV-urban6--0-sw | 17 | hour | snapshot capacity | 267.9 | 176.79 | 0.0 | 69390.0 | 49.0 | 0.0 | 0.0 | 0.0 | 1810.7 | 2180.4 | 953 |
| 1-LV-urban6--0-sw | 17 | hour | time-series capacity | 224.7 | 148.28 | 0.0 | 53971.0 | 0.0 | 0.0 | 0.0 | 0.0 | 1154.9 | 1377.8 | 978 |
| 1-LV-urban6--0-sw | 17 | hour | 1.5 x larger capacity | 401.8 | 265.15 | 0.0 | 123281.0 | 513.0 | 0.0 | 0.0 | 0.0 | 4685.9 | 5893.5 | 907 |

## Run checks

Failed steps (power flow did not converge): 0. This must be 0.

- rural1: steps 8784, daylight steps 3664, power flows 81452, time 4180.2 s, failed 0
- semiurb5: steps 8784, daylight steps 3854, power flows 128526, time 6343.3 s, failed 0
- urban6: steps 8784, daylight steps 3854, power flows 215659, time 8433.3 s, failed 0

Send this file back: D:\Research\01-active-projects\real-distribution-microgrid-study\results\vvar_annual_hour_summary.md
