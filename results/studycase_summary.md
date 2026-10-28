# Snapshot at the SimBench study cases (script 19)

Voltage limit 1.05 pu with the stored slack voltage (labels without '-sb', and 'stored'); 1.1 pu (EN 50160) with the SimBench slack voltage of the case (labels ending '-sb'). Thermal limit 100 % (current-based), search 0.1 kW, ceiling 2000 kW, 'equal' within 0.2 kW. Capacities are nameplate kW; the added unit injects Pn x f_pv. Regenerated from the saved CSV.

## Study cases of each network (all cases, the run uses the selected ones)

| grid | case | load_factor | pv_factor | slack_vm | source | loadcases_row |
|---|---|---|---|---|---|---|
| rural1 | hL | 1.0 | 0.0 | 0.965 | simbench.get_absolute_values | pload=1.0; qload=1.0; Wind_p=0.0; PV_p=0.0; RES_p=0.0; Slack_vm=0.965 |
| rural1 | n1 | 1.0 | 0.0 | 0.965 | simbench.get_absolute_values | pload=1.0; qload=1.0; Wind_p=0.0; PV_p=0.0; RES_p=0.0; Slack_vm=0.965 |
| rural1 | hW | 1.0 | 0.8 | 0.965 | simbench.get_absolute_values | pload=1.0; qload=1.0; Wind_p=1.0; PV_p=0.8; RES_p=1.0; Slack_vm=0.965 |
| rural1 | hPV | 1.0 | 0.95 | 0.965 | simbench.get_absolute_values | pload=1.0; qload=1.0; Wind_p=0.85; PV_p=0.95; RES_p=1.0; Slack_vm=0.965 |
| rural1 | lW | 0.1 | 0.8 | 1.055 | simbench.get_absolute_values | pload=0.1; qload=0.122543; Wind_p=1.0; PV_p=0.8; RES_p=1.0; Slack_vm=1.055 |
| rural1 | lPV | 0.1 | 0.95 | 1.055 | simbench.get_absolute_values | pload=0.1; qload=0.122543; Wind_p=0.85; PV_p=0.95; RES_p=1.0; Slack_vm=1.055 |
| rural2 | hL | 1.0 | 0.0 | 0.965 | simbench.get_absolute_values | pload=1.0; qload=1.0; Wind_p=0.0; PV_p=0.0; RES_p=0.0; Slack_vm=0.965 |
| rural2 | n1 | 1.0 | 0.0 | 0.965 | simbench.get_absolute_values | pload=1.0; qload=1.0; Wind_p=0.0; PV_p=0.0; RES_p=0.0; Slack_vm=0.965 |
| rural2 | hW | 1.0 | 0.8 | 0.965 | simbench.get_absolute_values | pload=1.0; qload=1.0; Wind_p=1.0; PV_p=0.8; RES_p=1.0; Slack_vm=0.965 |
| rural2 | hPV | 1.0 | 0.95 | 0.965 | simbench.get_absolute_values | pload=1.0; qload=1.0; Wind_p=0.85; PV_p=0.95; RES_p=1.0; Slack_vm=0.965 |
| rural2 | lW | 0.1 | 0.8 | 1.055 | simbench.get_absolute_values | pload=0.1; qload=0.122543; Wind_p=1.0; PV_p=0.8; RES_p=1.0; Slack_vm=1.055 |
| rural2 | lPV | 0.1 | 0.95 | 1.055 | simbench.get_absolute_values | pload=0.1; qload=0.122543; Wind_p=0.85; PV_p=0.95; RES_p=1.0; Slack_vm=1.055 |
| rural3 | hL | 1.0 | 0.0 | 0.965 | simbench.get_absolute_values | pload=1.0; qload=1.0; Wind_p=0.0; PV_p=0.0; RES_p=0.0; Slack_vm=0.965 |
| rural3 | n1 | 1.0 | 0.0 | 0.965 | simbench.get_absolute_values | pload=1.0; qload=1.0; Wind_p=0.0; PV_p=0.0; RES_p=0.0; Slack_vm=0.965 |
| rural3 | hW | 1.0 | 0.8 | 0.965 | simbench.get_absolute_values | pload=1.0; qload=1.0; Wind_p=1.0; PV_p=0.8; RES_p=1.0; Slack_vm=0.965 |
| rural3 | hPV | 1.0 | 0.95 | 0.965 | simbench.get_absolute_values | pload=1.0; qload=1.0; Wind_p=0.85; PV_p=0.95; RES_p=1.0; Slack_vm=0.965 |
| rural3 | lW | 0.1 | 0.8 | 1.055 | simbench.get_absolute_values | pload=0.1; qload=0.122543; Wind_p=1.0; PV_p=0.8; RES_p=1.0; Slack_vm=1.055 |
| rural3 | lPV | 0.1 | 0.95 | 1.055 | simbench.get_absolute_values | pload=0.1; qload=0.122543; Wind_p=0.85; PV_p=0.95; RES_p=1.0; Slack_vm=1.055 |
| semiurb4 | hL | 1.0 | 0.0 | 0.965 | simbench.get_absolute_values | pload=1.0; qload=1.0; Wind_p=0.0; PV_p=0.0; RES_p=0.0; Slack_vm=0.965 |
| semiurb4 | n1 | 1.0 | 0.0 | 0.965 | simbench.get_absolute_values | pload=1.0; qload=1.0; Wind_p=0.0; PV_p=0.0; RES_p=0.0; Slack_vm=0.965 |
| semiurb4 | hW | 1.0 | 0.8 | 0.965 | simbench.get_absolute_values | pload=1.0; qload=1.0; Wind_p=1.0; PV_p=0.8; RES_p=1.0; Slack_vm=0.965 |
| semiurb4 | hPV | 1.0 | 0.95 | 0.965 | simbench.get_absolute_values | pload=1.0; qload=1.0; Wind_p=0.85; PV_p=0.95; RES_p=1.0; Slack_vm=0.965 |
| semiurb4 | lW | 0.1 | 0.8 | 1.055 | simbench.get_absolute_values | pload=0.1; qload=0.122543; Wind_p=1.0; PV_p=0.8; RES_p=1.0; Slack_vm=1.055 |
| semiurb4 | lPV | 0.1 | 0.95 | 1.055 | simbench.get_absolute_values | pload=0.1; qload=0.122543; Wind_p=0.85; PV_p=0.95; RES_p=1.0; Slack_vm=1.055 |
| semiurb5 | hL | 1.0 | 0.0 | 0.965 | simbench.get_absolute_values | pload=1.0; qload=1.0; Wind_p=0.0; PV_p=0.0; RES_p=0.0; Slack_vm=0.965 |
| semiurb5 | n1 | 1.0 | 0.0 | 0.965 | simbench.get_absolute_values | pload=1.0; qload=1.0; Wind_p=0.0; PV_p=0.0; RES_p=0.0; Slack_vm=0.965 |
| semiurb5 | hW | 1.0 | 0.8 | 0.965 | simbench.get_absolute_values | pload=1.0; qload=1.0; Wind_p=1.0; PV_p=0.8; RES_p=1.0; Slack_vm=0.965 |
| semiurb5 | hPV | 1.0 | 0.95 | 0.965 | simbench.get_absolute_values | pload=1.0; qload=1.0; Wind_p=0.85; PV_p=0.95; RES_p=1.0; Slack_vm=0.965 |
| semiurb5 | lW | 0.1 | 0.8 | 1.055 | simbench.get_absolute_values | pload=0.1; qload=0.122543; Wind_p=1.0; PV_p=0.8; RES_p=1.0; Slack_vm=1.055 |
| semiurb5 | lPV | 0.1 | 0.95 | 1.055 | simbench.get_absolute_values | pload=0.1; qload=0.122543; Wind_p=0.85; PV_p=0.95; RES_p=1.0; Slack_vm=1.055 |
| urban6 | hL | 1.0 | 0.0 | 0.965 | simbench.get_absolute_values | pload=1.0; qload=1.0; Wind_p=0.0; PV_p=0.0; RES_p=0.0; Slack_vm=0.965 |
| urban6 | n1 | 1.0 | 0.0 | 0.965 | simbench.get_absolute_values | pload=1.0; qload=1.0; Wind_p=0.0; PV_p=0.0; RES_p=0.0; Slack_vm=0.965 |
| urban6 | hW | 1.0 | 0.8 | 0.965 | simbench.get_absolute_values | pload=1.0; qload=1.0; Wind_p=1.0; PV_p=0.8; RES_p=1.0; Slack_vm=0.965 |
| urban6 | hPV | 1.0 | 0.95 | 0.965 | simbench.get_absolute_values | pload=1.0; qload=1.0; Wind_p=0.85; PV_p=0.95; RES_p=1.0; Slack_vm=0.965 |
| urban6 | lW | 0.1 | 0.8 | 1.055 | simbench.get_absolute_values | pload=0.1; qload=0.122543; Wind_p=1.0; PV_p=0.8; RES_p=1.0; Slack_vm=1.055 |
| urban6 | lPV | 0.1 | 0.95 | 1.055 | simbench.get_absolute_values | pload=0.1; qload=0.122543; Wind_p=0.85; PV_p=0.95; RES_p=1.0; Slack_vm=1.055 |

# Case lPV: script 11 tables on the sample (113 buses)


## Networks

| code | case | f_pv | slack_vm | v_limit | load_kW | existing_pv_kW | base_v_max | base_line_% | base_trafo_% | status |
|---|---|---|---|---|---|---|---|---|---|---|
| 1-LV-rural1--0-sw | lPV | 0.95 | 1.025 | 1.05 | 8.0 | 152.4 | 1.0385 | 46.7 | 86.9 | ok |
| 1-LV-rural2--0-sw | lPV | 0.95 | 1.025 | 1.05 | 20.2 | 138.1 | 1.0422 | 26.6 | 45.7 | ok |
| 1-LV-rural3--0-sw | lPV | 0.95 | 1.025 | 1.05 | 33.1 | 180.9 | 1.0405 | 20.2 | 36.0 | ok |
| 1-LV-semiurb4--0-sw | lPV | 0.95 | 1.025 | 1.05 | 24.3 | 6.2 | 1.025 | 6.3 | 5.6 | ok |
| 1-LV-semiurb5--0-sw | lPV | 0.95 | 1.025 | 1.05 | 40.9 | 130.3 | 1.037 | 20.6 | 14.1 | ok |
| 1-LV-urban6--0-sw | lPV | 0.95 | 1.025 | 1.05 | 44.1 | 54.3 | 1.025 | 8.9 | 3.7 | ok |

## Hosting capacity (kW) and effect of default Volt-VAr

| code | buses | hc_nc median | hc_nc min-max | hc_vvar median | higher | equal | lower | median change % |
|---|---|---|---|---|---|---|---|---|
| 1-LV-rural1--0-sw [lPV] | 13 | 23.2 | 23.1-23.3 | 22.9 | 0 | 4 | 9 | -1.29 |
| 1-LV-rural2--0-sw [lPV] | 20 | 71.8 | 11.4-150.8 | 98.7 | 18 | 0 | 2 | 29.53 |
| 1-LV-rural3--0-sw [lPV] | 20 | 83.2 | 16.6-200.6 | 106.4 | 17 | 0 | 3 | 20.92 |
| 1-LV-semiurb4--0-sw [lPV] | 20 | 171.0 | 94.2-216.6 | 201.8 | 11 | 0 | 9 | 18.72 |
| 1-LV-semiurb5--0-sw [lPV] | 20 | 140.0 | 45.6-232.9 | 188.2 | 15 | 0 | 5 | 30.59 |
| 1-LV-urban6--0-sw [lPV] | 20 | 265.6 | 142.7-280.9 | 265.6 | 7 | 0 | 13 | -0.62 |

## Which limit binds first without control

| code | voltage first | thermal first | both | thermal element: trafo | thermal element: line |
|---|---|---|---|---|---|
| 1-LV-rural1--0-sw [lPV] | 0 | 13 | 0 | 13 | 0 |
| 1-LV-rural2--0-sw [lPV] | 18 | 2 | 0 | 20 | 0 |
| 1-LV-rural3--0-sw [lPV] | 17 | 3 | 0 | 0 | 20 |
| 1-LV-semiurb4--0-sw [lPV] | 12 | 8 | 0 | 0 | 20 |
| 1-LV-semiurb5--0-sw [lPV] | 15 | 5 | 0 | 0 | 20 |
| 1-LV-urban6--0-sw [lPV] | 7 | 13 | 0 | 0 | 20 |

## Hypothesis test: effect of Volt-VAr by first limit, per network

| code | first limit | buses | higher | equal | lower | median change % |
|---|---|---|---|---|---|---|
| 1-LV-rural1--0-sw [lPV] | thermal | 13 | 0 | 4 | 9 | -1.29 |
| 1-LV-rural2--0-sw [lPV] | thermal | 2 | 0 | 0 | 2 | -1.73 |
| 1-LV-rural2--0-sw [lPV] | voltage | 18 | 18 | 0 | 0 | 32.81 |
| 1-LV-rural3--0-sw [lPV] | thermal | 3 | 0 | 0 | 3 | -1.1 |
| 1-LV-rural3--0-sw [lPV] | voltage | 17 | 17 | 0 | 0 | 22.22 |
| 1-LV-semiurb4--0-sw [lPV] | thermal | 8 | 0 | 0 | 8 | -1.5 |
| 1-LV-semiurb4--0-sw [lPV] | voltage | 12 | 11 | 0 | 1 | 27.85 |
| 1-LV-semiurb5--0-sw [lPV] | thermal | 5 | 0 | 0 | 5 | -1.08 |
| 1-LV-semiurb5--0-sw [lPV] | voltage | 15 | 15 | 0 | 0 | 32.8 |
| 1-LV-urban6--0-sw [lPV] | thermal | 13 | 0 | 0 | 13 | -1.01 |
| 1-LV-urban6--0-sw [lPV] | voltage | 7 | 7 | 0 | 0 | 33.36 |

## Hypothesis test: all networks together

| first limit | buses | higher | equal | lower | median change % | min change % | max change % |
|---|---|---|---|---|---|---|---|
| thermal | 44 | 0 | 4 | 40 | -1.29 | -2.5 | -0.34 |
| voltage | 69 | 68 | 0 | 1 | 28.53 | -0.84 | 61.67 |

## Volt-VAr split: gain on the voltage limit, penalty on the thermal limit

Gain is shown only where the voltage limit binds first. Elsewhere hc_v is very large (PV of several hundred kW or more) and the Volt-VAr iteration may not converge, so hc_v_vvar there is a numerical limit, not a physical one.

| code | voltage-first buses | median gain % (voltage-first buses) | median penalty % (all buses) | max penalty % (all buses) | hc_vvar = min(parts) |
|---|---|---|---|---|---|
| 1-LV-rural1--0-sw [lPV] | 0 | - | 1.3 | 1.3 | 13/13 |
| 1-LV-rural2--0-sw [lPV] | 18 | 36.0 | 4.5 | 10.5 | 20/20 |
| 1-LV-rural3--0-sw [lPV] | 17 | 23.8 | 5.0 | 11.8 | 20/20 |
| 1-LV-semiurb4--0-sw [lPV] | 12 | 30.3 | 3.0 | 6.6 | 20/20 |
| 1-LV-semiurb5--0-sw [lPV] | 15 | 33.5 | 4.3 | 8.8 | 20/20 |
| 1-LV-urban6--0-sw [lPV] | 7 | 41.2 | 1.7 | 5.6 | 20/20 |

## Screening indicator: effect of Volt-VAr by ratio r = hc_t / hc_v

| ratio hc_t / hc_v | buses | higher | equal | lower | median change % |
|---|---|---|---|---|---|
| < 1 (thermal first) | 44 | 0 | 4 | 40 | -1.29 |
| 1.00-1.05 | 2 | 1 | 0 | 1 | 0.12 |
| 1.05-1.10 | 1 | 1 | 0 | 0 | 3.44 |
| 1.10-1.25 | 7 | 7 | 0 | 0 | 17.96 |
| 1.25-1.50 | 11 | 11 | 0 | 0 | 34.67 |
| >= 1.50 | 48 | 48 | 0 | 0 | 28.51 |

## Dead-band check (PV-bus voltage at the no-control capacity)

- PV bus inside the dead band (<= 1.02 pu): 0 buses, effect equal in 0
- PV bus above the dead band: 113 buses, equal in 4, higher in 68, lower in 41

## Checks

- hc_nc equals min(hc_v, hc_t) within 0.2 kW: 113 of 113 buses
- hc_vvar equals min(hc_v_vvar, hc_t_vvar) within 0.2 kW: 113 of 113 buses
- buses where at least one search reached the 2000 kW ceiling (that limit never binds below it): 1

## Case lPV: rules P1 to P4 of script 18

| rule | result |
|---|---|
| P1: r < 1, Volt-VAr never higher | 44 of 44 |
| P2: r >= 1.05 and voltage first, Volt-VAr higher | 67 of 67 |
| P3: dead band at hc_nc, Volt-VAr equal | 0 of 0 |
| P4: hc_nc and hc_vvar = min of their parts | 113 of 113 |
| voltage-first buses: higher / equal / lower | 68 / 0 / 1 |

## Case lPV: control variants by first limit

Change relative to no control at the same case (nameplate kW).

| first limit | control | buses | higher | equal | lower | median change % | min % | max % |
|---|---|---|---|---|---|---|---|---|
| thermal | Volt-VAr (added unit) | 44 | 0 | 4 | 40 | -1.29 | -2.5 | -0.34 |
| thermal | cos phi(P) (added unit) | 44 | 0 | 0 | 44 | -9.81 | -11.87 | -3.86 |
| thermal | Volt-VAr (all PV units) | 44 | 0 | 0 | 44 | -1.78 | -12.02 | -0.34 |
| voltage | Volt-VAr (added unit) | 69 | 68 | 0 | 1 | 28.53 | -0.84 | 61.67 |
| voltage | cos phi(P) (added unit) | 69 | 66 | 0 | 3 | 55.19 | -9.62 | 168.39 |
| voltage | Volt-VAr (all PV units) | 69 | 68 | 0 | 1 | 42.3 | -0.94 | 115.8 |

## Case lPV: inverter apparent-power limit (S = Pn, P priority)

PV factor 0.950 is above 0.898: the limit can bind and was searched. Reactive power is limited to sqrt(Pn^2 - P^2).

| first limit | buses | changed vs unlimited Volt-VAr | median change %, unlimited Volt-VAr | median change %, S = Pn | higher than no control, S = Pn |
|---|---|---|---|---|---|
| thermal | 44 | 0 | -1.29 | -1.29 | 0 |
| voltage | 69 | 0 | 28.53 | 28.53 | 68 |

# Case lW: script 11 tables on the sample (113 buses)


## Networks

| code | case | f_pv | slack_vm | v_limit | load_kW | existing_pv_kW | base_v_max | base_line_% | base_trafo_% | status |
|---|---|---|---|---|---|---|---|---|---|---|
| 1-LV-rural1--0-sw | lW | 0.8 | 1.025 | 1.05 | 8.0 | 128.3 | 1.0362 | 39.2 | 72.6 | ok |
| 1-LV-rural2--0-sw | lW | 0.8 | 1.025 | 1.05 | 20.2 | 116.3 | 1.0386 | 22.3 | 37.4 | ok |
| 1-LV-rural3--0-sw | lW | 0.8 | 1.025 | 1.05 | 33.1 | 152.3 | 1.0371 | 16.5 | 29.2 | ok |
| 1-LV-semiurb4--0-sw | lW | 0.8 | 1.025 | 1.05 | 24.3 | 5.2 | 1.025 | 6.3 | 5.8 | ok |
| 1-LV-semiurb5--0-sw | lW | 0.8 | 1.025 | 1.05 | 40.9 | 109.7 | 1.0343 | 17.2 | 11.0 | ok |
| 1-LV-urban6--0-sw | lW | 0.8 | 1.025 | 1.05 | 44.1 | 45.7 | 1.025 | 7.1 | 3.3 | ok |

## Hosting capacity (kW) and effect of default Volt-VAr

| code | buses | hc_nc median | hc_nc min-max | hc_vvar median | higher | equal | lower | median change % |
|---|---|---|---|---|---|---|---|---|
| 1-LV-rural1--0-sw [lW] | 13 | 57.7 | 47.4-57.9 | 56.8 | 2 | 0 | 11 | -1.56 |
| 1-LV-rural2--0-sw [lW] | 20 | 91.1 | 19.7-206.5 | 134.9 | 18 | 0 | 2 | 36.65 |
| 1-LV-rural3--0-sw [lW] | 20 | 108.4 | 26.6-240.2 | 147.9 | 16 | 0 | 4 | 25.82 |
| 1-LV-semiurb4--0-sw [lW] | 20 | 203.6 | 112.7-257.1 | 238.8 | 11 | 0 | 9 | 17.59 |
| 1-LV-semiurb5--0-sw [lW] | 20 | 183.0 | 65.2-284.7 | 258.8 | 15 | 0 | 5 | 35.39 |
| 1-LV-urban6--0-sw [lW] | 20 | 316.7 | 170.3-333.6 | 314.9 | 7 | 0 | 13 | -0.74 |

## Which limit binds first without control

| code | voltage first | thermal first | both | thermal element: trafo | thermal element: line |
|---|---|---|---|---|---|
| 1-LV-rural1--0-sw [lW] | 2 | 11 | 0 | 13 | 0 |
| 1-LV-rural2--0-sw [lW] | 18 | 2 | 0 | 16 | 4 |
| 1-LV-rural3--0-sw [lW] | 17 | 3 | 0 | 0 | 20 |
| 1-LV-semiurb4--0-sw [lW] | 12 | 8 | 0 | 0 | 20 |
| 1-LV-semiurb5--0-sw [lW] | 15 | 5 | 0 | 0 | 20 |
| 1-LV-urban6--0-sw [lW] | 7 | 13 | 0 | 0 | 20 |

## Hypothesis test: effect of Volt-VAr by first limit, per network

| code | first limit | buses | higher | equal | lower | median change % |
|---|---|---|---|---|---|---|
| 1-LV-rural1--0-sw [lW] | thermal | 11 | 0 | 0 | 11 | -1.56 |
| 1-LV-rural1--0-sw [lW] | voltage | 2 | 2 | 0 | 0 | 19.33 |
| 1-LV-rural2--0-sw [lW] | thermal | 2 | 0 | 0 | 2 | -2.12 |
| 1-LV-rural2--0-sw [lW] | voltage | 18 | 18 | 0 | 0 | 39.52 |
| 1-LV-rural3--0-sw [lW] | thermal | 3 | 0 | 0 | 3 | -1.33 |
| 1-LV-rural3--0-sw [lW] | voltage | 17 | 16 | 0 | 1 | 27.72 |
| 1-LV-semiurb4--0-sw [lW] | thermal | 8 | 0 | 0 | 8 | -1.86 |
| 1-LV-semiurb4--0-sw [lW] | voltage | 12 | 11 | 0 | 1 | 33.83 |
| 1-LV-semiurb5--0-sw [lW] | thermal | 5 | 0 | 0 | 5 | -1.3 |
| 1-LV-semiurb5--0-sw [lW] | voltage | 15 | 15 | 0 | 0 | 39.37 |
| 1-LV-urban6--0-sw [lW] | thermal | 13 | 0 | 0 | 13 | -1.31 |
| 1-LV-urban6--0-sw [lW] | voltage | 7 | 7 | 0 | 0 | 31.77 |

## Hypothesis test: all networks together

| first limit | buses | higher | equal | lower | median change % | min change % | max change % |
|---|---|---|---|---|---|---|---|
| thermal | 42 | 0 | 0 | 42 | -1.48 | -3.04 | -0.37 |
| voltage | 71 | 69 | 0 | 2 | 32.98 | -1.89 | 60.66 |

## Volt-VAr split: gain on the voltage limit, penalty on the thermal limit

Gain is shown only where the voltage limit binds first. Elsewhere hc_v is very large (PV of several hundred kW or more) and the Volt-VAr iteration may not converge, so hc_v_vvar there is a numerical limit, not a physical one.

| code | voltage-first buses | median gain % (voltage-first buses) | median penalty % (all buses) | max penalty % (all buses) | hc_vvar = min(parts) |
|---|---|---|---|---|---|
| 1-LV-rural1--0-sw [lW] | 2 | 33.8 | 1.6 | 2.6 | 13/13 |
| 1-LV-rural2--0-sw [lW] | 18 | 46.7 | 5.6 | 14.5 | 20/20 |
| 1-LV-rural3--0-sw [lW] | 17 | 29.7 | 6.1 | 15.3 | 20/20 |
| 1-LV-semiurb4--0-sw [lW] | 12 | 38.4 | 3.7 | 8.0 | 20/20 |
| 1-LV-semiurb5--0-sw [lW] | 15 | 43.9 | 5.1 | 10.4 | 20/20 |
| 1-LV-urban6--0-sw [lW] | 7 | 53.7 | 2.1 | 6.6 | 20/20 |

## Screening indicator: effect of Volt-VAr by ratio r = hc_t / hc_v

| ratio hc_t / hc_v | buses | higher | equal | lower | median change % |
|---|---|---|---|---|---|
| < 1 (thermal first) | 42 | 0 | 0 | 42 | -1.48 |
| 1.00-1.05 | 2 | 0 | 0 | 2 | -1.79 |
| 1.05-1.10 | 3 | 3 | 0 | 0 | 3.41 |
| 1.10-1.25 | 7 | 7 | 0 | 0 | 18.07 |
| 1.25-1.50 | 11 | 11 | 0 | 0 | 31.7 |
| >= 1.50 | 48 | 48 | 0 | 0 | 37.61 |

## Dead-band check (PV-bus voltage at the no-control capacity)

- PV bus inside the dead band (<= 1.02 pu): 0 buses, effect equal in 0
- PV bus above the dead band: 113 buses, equal in 0, higher in 69, lower in 44

## Checks

- hc_nc equals min(hc_v, hc_t) within 0.2 kW: 113 of 113 buses
- hc_vvar equals min(hc_v_vvar, hc_t_vvar) within 0.2 kW: 113 of 113 buses
- buses where at least one search reached the 2000 kW ceiling (that limit never binds below it): 1

## Case lW: rules P1 to P4 of script 18

| rule | result |
|---|---|
| P1: r < 1, Volt-VAr never higher | 42 of 42 |
| P2: r >= 1.05 and voltage first, Volt-VAr higher | 69 of 69 |
| P3: dead band at hc_nc, Volt-VAr equal | 0 of 0 |
| P4: hc_nc and hc_vvar = min of their parts | 113 of 113 |
| voltage-first buses: higher / equal / lower | 69 / 0 / 2 |

## Case lW: control variants by first limit

Change relative to no control at the same case (nameplate kW).

| first limit | control | buses | higher | equal | lower | median change % | min % | max % |
|---|---|---|---|---|---|---|---|---|
| thermal | Volt-VAr (added unit) | 42 | 0 | 0 | 42 | -1.48 | -3.04 | -0.37 |
| thermal | cos phi(P) (added unit) | 42 | 0 | 0 | 42 | -6.99 | -8.28 | -3.8 |
| thermal | Volt-VAr (all PV units) | 42 | 0 | 0 | 42 | -2.13 | -7.25 | -0.37 |
| voltage | Volt-VAr (added unit) | 71 | 69 | 0 | 2 | 32.98 | -1.89 | 60.66 |
| voltage | cos phi(P) (added unit) | 71 | 67 | 0 | 4 | 45.61 | -6.5 | 99.68 |
| voltage | Volt-VAr (all PV units) | 71 | 69 | 0 | 2 | 44.53 | -1.93 | 101.26 |

## Case lW: inverter apparent-power limit (S = Pn, P priority)

PV factor 0.800 is at or below 0.898: with S = Pn the full 0.44 Pn of reactive power is available (sqrt(1 - f^2) >= 0.44), so the limit does not change any result at this case (not searched).

## The nine buses of the time-series study (input for script 21)

| code | case | bus | position | f_pv | hc_nc | first_limit | ratio_t_v | hc_vvar | delta_pct | effect | hc_cosphi | cosphi_pct | hc_vvar_all | vvar_all_pct |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| 1-LV-rural1--0-sw | lPV | 4 | far | 0.95 | 23.3 | thermal | 0.693 | 22.9 | -1.72 | lower | 22.4 | -3.86 | 20.5 | -12.02 |
| 1-LV-rural1--0-sw | lW | 4 | far | 0.8 | 47.4 | voltage | 1.23 | 56.8 | 19.83 | higher | 56.0 | 18.14 | 53.6 | 13.08 |
| 1-LV-rural1--0-sw | stored | 4 | far | 1.0 | 80.1 | voltage | 1.037 | 78.9 | -1.5 | lower | 70.7 | -11.74 | 76.1 | -4.99 |
| 1-LV-rural1--0-sw | lPV | 11 | middle | 0.95 | 23.2 | thermal | 0.267 | 22.9 | -1.29 | lower | 22.3 | -3.88 | 20.5 | -11.64 |
| 1-LV-rural1--0-sw | lW | 11 | middle | 0.8 | 57.7 | thermal | 0.469 | 56.8 | -1.56 | lower | 55.5 | -3.81 | 53.8 | -6.76 |
| 1-LV-rural1--0-sw | stored | 11 | middle | 1.0 | 82.3 | thermal | 0.456 | 80.1 | -2.67 | lower | 70.1 | -14.82 | 77.1 | -6.32 |
| 1-LV-rural1--0-sw | lPV | 7 | near | 0.95 | 23.1 | thermal | 0.155 | 22.9 | -0.87 | equal | 22.2 | -3.9 | 20.5 | -11.26 |
| 1-LV-rural1--0-sw | lW | 7 | near | 0.8 | 57.4 | thermal | 0.274 | 56.7 | -1.22 | lower | 55.2 | -3.83 | 53.8 | -6.27 |
| 1-LV-rural1--0-sw | stored | 7 | near | 1.0 | 82.0 | thermal | 0.286 | 80.3 | -2.07 | lower | 69.9 | -14.76 | 77.6 | -5.37 |
| 1-LV-semiurb5--0-sw | lPV | 51 | far | 0.95 | 45.6 | voltage | 5.044 | 58.2 | 27.63 | higher | 80.2 | 75.88 | 74.4 | 63.16 |
| 1-LV-semiurb5--0-sw | lW | 51 | far | 0.8 | 65.2 | voltage | 4.362 | 87.9 | 34.82 | higher | 99.2 | 52.15 | 107.8 | 65.34 |
| 1-LV-semiurb5--0-sw | stored | 51 | far | 1.0 | 190.4 | voltage | 1.24 | 226.1 | 18.75 | higher | 201.7 | 5.93 | 224.3 | 17.8 |
| 1-LV-semiurb5--0-sw | lPV | 72 | middle | 0.95 | 101.1 | voltage | 2.213 | 135.4 | 33.93 | higher | 200.4 | 98.22 | 181.5 | 79.53 |
| 1-LV-semiurb5--0-sw | lW | 72 | middle | 0.8 | 144.9 | voltage | 1.921 | 215.5 | 48.72 | higher | 257.1 | 77.43 | 260.3 | 79.64 |
| 1-LV-semiurb5--0-sw | stored | 72 | middle | 1.0 | 290.2 | thermal | 0.803 | 284.0 | -2.14 | lower | 234.3 | -19.26 | 283.3 | -2.38 |
| 1-LV-semiurb5--0-sw | lPV | 74 | near | 0.95 | 216.2 | thermal | 0.366 | 215.1 | -0.51 | lower | 195.7 | -9.48 | 214.1 | -0.97 |
| 1-LV-semiurb5--0-sw | lW | 74 | near | 0.8 | 269.3 | thermal | 0.312 | 267.5 | -0.67 | lower | 250.8 | -6.87 | 266.5 | -1.04 |
| 1-LV-semiurb5--0-sw | stored | 74 | near | 1.0 | 324.3 | thermal | 0.162 | 324.3 | 0.0 | equal | 249.8 | -22.97 | 324.3 | 0.0 |
| 1-LV-urban6--0-sw | lPV | 17 | far | 0.95 | 142.7 | voltage | 1.969 | 190.3 | 33.36 | higher | 248.5 | 74.14 | 190.9 | 33.78 |
| 1-LV-urban6--0-sw | lW | 17 | far | 0.8 | 170.3 | voltage | 1.959 | 242.7 | 42.51 | higher | 283.3 | 66.35 | 243.1 | 42.75 |
| 1-LV-urban6--0-sw | stored | 17 | far | 1.0 | 267.9 | thermal | 0.885 | 263.8 | -1.53 | lower | 231.3 | -13.66 | 263.8 | -1.53 |
| 1-LV-urban6--0-sw | lPV | 50 | middle | 0.95 | 269.8 | thermal | 0.823 | 265.2 | -1.7 | lower | 241.5 | -10.49 | 265.1 | -1.74 |
| 1-LV-urban6--0-sw | lW | 50 | middle | 0.8 | 321.2 | thermal | 0.82 | 314.4 | -2.12 | lower | 297.8 | -7.29 | 314.3 | -2.15 |
| 1-LV-urban6--0-sw | stored | 50 | middle | 1.0 | 266.7 | thermal | 0.452 | 266.4 | -0.11 | lower | 231.6 | -13.16 | 266.4 | -0.11 |
| 1-LV-urban6--0-sw | lPV | 54 | near | 0.95 | 269.8 | thermal | 0.204 | 268.8 | -0.37 | lower | 242.4 | -10.16 | 268.7 | -0.41 |
| 1-LV-urban6--0-sw | lW | 54 | near | 0.8 | 320.4 | thermal | 0.204 | 318.8 | -0.5 | lower | 298.1 | -6.96 | 318.8 | -0.5 |
| 1-LV-urban6--0-sw | stored | 54 | near | 1.0 | 265.5 | thermal | 0.133 | 265.5 | 0.0 | equal | 232.0 | -12.62 | 265.5 | 0.0 |

## Checks

- Volt-VAr power flows that did not converge at or below the Volt-VAr capacity (must be 0): 0
- Same for Volt-VAr on all PV units (must be 0): 0
- Non-converged checks above the capacity (expected, no effect): 1063
- Buses with a search at the 2000 kW ceiling: 4
- thermal_element, v_pv_nc and hc_vvar_slim recomputed with the fixed solve() (--recheck): 239 of 239 rows; S-limit power flows not converged at or below its capacity (must be 0): 0
- Stored rows (case 'stored') must equal script 11 where the bus is in both; script 21 checks this.

Send this file back: results\studycase_summary.md
