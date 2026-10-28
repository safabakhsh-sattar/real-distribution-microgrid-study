# Time-series hosting capacity with Volt-VAr and cos phi(P), nine buses (script 20)

Search of scripts 12 and 15 (critical-step method, same sets, 15-minute steps, one
weather year). Change relative to the no-control time-series capacity of script 12.

## Per bus

| code | bus | position | control | hc_ts_nc | hc_ts_ctrl | delta_pct | limit_at_capacity | binding_time | unresolved_violations | nonconverged_at_or_below_capacity | verify_set | source |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| 1-LV-rural1--0-sw | 7 | near | cosphi | 175.7 | 170.8 | -2.79 | trafo | 20 May 12:00 | 0 | 0 | all daylight steps | script 20 |
| 1-LV-rural1--0-sw | 11 | middle | cosphi | 176.7 | 171.7 | -2.83 | trafo | 20 May 12:00 | 0 | 0 | all daylight steps | script 20 |
| 1-LV-rural1--0-sw | 4 | far | cosphi | 106.5 | 115.2 | 8.17 | voltage | 27 Jul 13:00 | 0 | 0 | all daylight steps | script 20 |
| 1-LV-semiurb5--0-sw | 74 | near | cosphi | 397.4 | 387.8 | -2.42 | line | 24 May 11:00 | 0 | 0 | all daylight steps | script 20 |
| 1-LV-semiurb5--0-sw | 72 | middle | cosphi | 246.5 | 298.6 | 21.14 | voltage | 01 Aug 10:45 | 0 | 0 | all daylight steps | script 20 |
| 1-LV-semiurb5--0-sw | 51 | far | cosphi | 110.5 | 129.2 | 16.92 | voltage | 24 Jul 10:15 | 0 | 0 | all daylight steps | script 20 |
| 1-LV-urban6--0-sw | 54 | near | cosphi | 439.3 | 430.0 | -2.12 | line | 24 May 11:00 | 0 | 0 | all daylight steps | script 20 |
| 1-LV-urban6--0-sw | 50 | middle | cosphi | 442.6 | 432.4 | -2.3 | line | 24 May 11:00 | 0 | 0 | all daylight steps | script 20 |
| 1-LV-urban6--0-sw | 17 | far | cosphi | 224.7 | 252.3 | 12.28 | voltage | 29 May 09:15 | 0 | 0 | all daylight steps | script 20 |
| 1-LV-rural1--0-sw | 7 | near | vvar | 175.7 | 170.8 | -2.79 | trafo | 20 May 12:00 | 0 | 0 | all daylight steps | script 20 |
| 1-LV-rural1--0-sw | 11 | middle | vvar | 176.7 | 169.7 | -3.96 | trafo | 20 May 12:00 | 0 | 0 | all daylight steps | script 20 |
| 1-LV-rural1--0-sw | 4 | far | vvar | 106.5 | 165.1 | 55.02 | trafo | - | 0 | 0 | all daylight steps | script 15 (reused) |
| 1-LV-semiurb5--0-sw | 74 | near | vvar | 397.4 | 393.7 | -0.93 | line | 24 May 11:00 | 0 | 0 | all daylight steps | script 20 |
| 1-LV-semiurb5--0-sw | 72 | middle | vvar | 246.5 | 381.2 | 54.65 | line | 24 May 11:00 | 0 | 0 | all daylight steps | script 20 |
| 1-LV-semiurb5--0-sw | 51 | far | vvar | 110.5 | 174.1 | 57.56 | voltage | - | 0 | 0 | all daylight steps | script 15 (reused) |
| 1-LV-urban6--0-sw | 54 | near | vvar | 439.3 | 436.6 | -0.61 | line | 24 May 11:00 | 0 | 0 | all daylight steps | script 20 |
| 1-LV-urban6--0-sw | 50 | middle | vvar | 442.6 | 429.6 | -2.94 | line | 24 May 11:00 | 0 | 0 | all daylight steps | script 20 |
| 1-LV-urban6--0-sw | 17 | far | vvar | 224.7 | 390.8 | 73.92 | voltage | - | 0 | 0 | all daylight steps | script 15 (reused) |

## Summary

| control | buses | higher (> +0.2 kW) | equal | lower (< -0.2 kW) | median change % | min % | max % |
|---|---|---|---|---|---|---|---|
| cosphi | 9 | 4 | 0 | 5 | -2.12 | -2.83 | 21.14 |
| vvar | 9 | 4 | 0 | 5 | -0.61 | -3.96 | 73.92 |

## Run checks

Unresolved violations (must be 0): 0.
Non-converged at or below the capacity (must be 0): 0.
Total time: 249.7 min.

Send this file back: results\year_controls_summary.md
