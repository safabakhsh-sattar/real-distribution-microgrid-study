# Snapshot against year: stored point and study cases (script 21)

## Check: stored rows of script 19 against script 11

Buses in both: 7. Largest difference: hc_nc 0.0 kW, hc_vvar 0.0 kW (must be 0.0, or within 0.1 kW of search tolerance).

## Volt-VAr: snapshot effect and rule of r against the year, nine buses

| grid | bus | position | point | f_pv | snapshot hc_nc | r | rule | snapshot Volt-VAr % | snapshot sign | year Volt-VAr % | year sign | sign agrees | rule agrees |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| rural1 | 7 | near | lPV | 0.95 | 23.1 | 0.155 | no gain expected | -0.87 | lower | -2.79 | lower | True | True |
| rural1 | 7 | near | lW | 0.8 | 57.4 | 0.274 | no gain expected | -1.22 | lower | -2.79 | lower | True | True |
| rural1 | 7 | near | stored | 1.0 | 82.0 | 0.286 | no gain expected | -2.07 | lower | -2.79 | lower | True | True |
| rural1 | 11 | middle | lPV | 0.95 | 23.2 | 0.267 | no gain expected | -1.29 | lower | -3.96 | lower | True | True |
| rural1 | 11 | middle | lW | 0.8 | 57.7 | 0.469 | no gain expected | -1.56 | lower | -3.96 | lower | True | True |
| rural1 | 11 | middle | stored | 1.0 | 82.3 | 0.456 | no gain expected | -2.67 | lower | -3.96 | lower | True | True |
| rural1 | 4 | far | lPV | 0.95 | 23.3 | 0.693 | no gain expected | -1.72 | lower | 55.02 | higher | False | False |
| rural1 | 4 | far | lW | 0.8 | 47.4 | 1.23 | gain expected | 19.83 | higher | 55.02 | higher | True | True |
| rural1 | 4 | far | stored | 1.0 | 80.1 | 1.037 | mixed band | -1.5 | lower | 55.02 | higher | False | - |
| semiurb5 | 74 | near | lPV | 0.95 | 216.2 | 0.366 | no gain expected | -0.51 | lower | -0.93 | lower | True | True |
| semiurb5 | 74 | near | lW | 0.8 | 269.3 | 0.312 | no gain expected | -0.67 | lower | -0.93 | lower | True | True |
| semiurb5 | 74 | near | stored | 1.0 | 324.3 | 0.162 | no gain expected | 0.0 | equal | -0.93 | lower | False | True |
| semiurb5 | 72 | middle | lPV | 0.95 | 101.1 | 2.213 | gain expected | 33.93 | higher | 54.65 | higher | True | True |
| semiurb5 | 72 | middle | lW | 0.8 | 144.9 | 1.921 | gain expected | 48.72 | higher | 54.65 | higher | True | True |
| semiurb5 | 72 | middle | stored | 1.0 | 290.2 | 0.803 | no gain expected | -2.14 | lower | 54.65 | higher | False | False |
| semiurb5 | 51 | far | lPV | 0.95 | 45.6 | 5.044 | gain expected | 27.63 | higher | 57.56 | higher | True | True |
| semiurb5 | 51 | far | lW | 0.8 | 65.2 | 4.362 | gain expected | 34.82 | higher | 57.56 | higher | True | True |
| semiurb5 | 51 | far | stored | 1.0 | 190.4 | 1.24 | gain expected | 18.75 | higher | 57.56 | higher | True | True |
| urban6 | 54 | near | lPV | 0.95 | 269.8 | 0.204 | no gain expected | -0.37 | lower | -0.61 | lower | True | True |
| urban6 | 54 | near | lW | 0.8 | 320.4 | 0.204 | no gain expected | -0.5 | lower | -0.61 | lower | True | True |
| urban6 | 54 | near | stored | 1.0 | 265.5 | 0.133 | no gain expected | 0.0 | equal | -0.61 | lower | False | True |
| urban6 | 50 | middle | lPV | 0.95 | 269.8 | 0.823 | no gain expected | -1.7 | lower | -2.94 | lower | True | True |
| urban6 | 50 | middle | lW | 0.8 | 321.2 | 0.82 | no gain expected | -2.12 | lower | -2.94 | lower | True | True |
| urban6 | 50 | middle | stored | 1.0 | 266.7 | 0.452 | no gain expected | -0.11 | lower | -2.94 | lower | True | True |
| urban6 | 17 | far | lPV | 0.95 | 142.7 | 1.969 | gain expected | 33.36 | higher | 73.92 | higher | True | True |
| urban6 | 17 | far | lW | 0.8 | 170.3 | 1.959 | gain expected | 42.51 | higher | 73.92 | higher | True | True |
| urban6 | 17 | far | stored | 1.0 | 267.9 | 0.885 | no gain expected | -1.53 | lower | 73.92 | higher | False | False |

## Volt-VAr: agreement with the year per operating point

| operating point | buses | snapshot sign = year sign | rule of r correct (outside mixed band) |
|---|---|---|---|
| lPV | 9 | 8 of 9 | 8 of 9 |
| lW | 9 | 9 of 9 | 9 of 9 |
| stored | 9 | 4 of 9 | 6 of 8 |

## cos phi(P): snapshot effect against the year, nine buses

| grid | bus | position | point | snapshot cos phi % | snapshot sign | year cos phi % | year sign | sign agrees |
|---|---|---|---|---|---|---|---|---|
| rural1 | 7 | near | lPV | -3.9 | lower | -2.79 | lower | True |
| rural1 | 7 | near | lW | -3.83 | lower | -2.79 | lower | True |
| rural1 | 7 | near | stored | -14.76 | lower | -2.79 | lower | True |
| rural1 | 11 | middle | lPV | -3.88 | lower | -2.83 | lower | True |
| rural1 | 11 | middle | lW | -3.81 | lower | -2.83 | lower | True |
| rural1 | 11 | middle | stored | -14.82 | lower | -2.83 | lower | True |
| rural1 | 4 | far | lPV | -3.86 | lower | 8.17 | higher | False |
| rural1 | 4 | far | lW | 18.14 | higher | 8.17 | higher | True |
| rural1 | 4 | far | stored | -11.74 | lower | 8.17 | higher | False |
| semiurb5 | 74 | near | lPV | -9.48 | lower | -2.42 | lower | True |
| semiurb5 | 74 | near | lW | -6.87 | lower | -2.42 | lower | True |
| semiurb5 | 74 | near | stored | -22.97 | lower | -2.42 | lower | True |
| semiurb5 | 72 | middle | lPV | 98.22 | higher | 21.14 | higher | True |
| semiurb5 | 72 | middle | lW | 77.43 | higher | 21.14 | higher | True |
| semiurb5 | 72 | middle | stored | -19.26 | lower | 21.14 | higher | False |
| semiurb5 | 51 | far | lPV | 75.88 | higher | 16.92 | higher | True |
| semiurb5 | 51 | far | lW | 52.15 | higher | 16.92 | higher | True |
| semiurb5 | 51 | far | stored | 5.93 | higher | 16.92 | higher | True |
| urban6 | 54 | near | lPV | -10.16 | lower | -2.12 | lower | True |
| urban6 | 54 | near | lW | -6.96 | lower | -2.12 | lower | True |
| urban6 | 54 | near | stored | -12.62 | lower | -2.12 | lower | True |
| urban6 | 50 | middle | lPV | -10.49 | lower | -2.3 | lower | True |
| urban6 | 50 | middle | lW | -7.29 | lower | -2.3 | lower | True |
| urban6 | 50 | middle | stored | -13.16 | lower | -2.3 | lower | True |
| urban6 | 17 | far | lPV | 74.14 | higher | 12.28 | higher | True |
| urban6 | 17 | far | lW | 66.35 | higher | 12.28 | higher | True |
| urban6 | 17 | far | stored | -13.66 | lower | 12.28 | higher | False |

Agreement of the sign per operating point: lPV: 8 of 9; lW: 9 of 9; stored: 6 of 9

## Year: Volt-VAr against cos phi(P)

| code | bus | year cos phi % | year Volt-VAr % | year no control kW | year limit (no control) |
|---|---|---|---|---|---|
| 1-LV-rural1--0-sw | 4 | 8.17 | 55.02 | 106.5 | voltage |
| 1-LV-rural1--0-sw | 7 | -2.79 | -2.79 | 175.7 | trafo |
| 1-LV-rural1--0-sw | 11 | -2.83 | -3.96 | 176.7 | trafo |
| 1-LV-semiurb5--0-sw | 51 | 16.92 | 57.56 | 110.5 | voltage |
| 1-LV-semiurb5--0-sw | 72 | 21.14 | 54.65 | 246.5 | voltage |
| 1-LV-semiurb5--0-sw | 74 | -2.42 | -0.93 | 397.4 | line |
| 1-LV-urban6--0-sw | 17 | 12.28 | 73.92 | 224.7 | voltage |
| 1-LV-urban6--0-sw | 50 | -2.3 | -2.94 | 442.6 | line |
| 1-LV-urban6--0-sw | 54 | -2.12 | -0.61 | 439.3 | line |

Send this file back: results/snapshot_vs_year_summary.md
