# Multi-feeder snapshot results (script 11)

Voltage limit 1.05 pu, thermal limit 100 % (current-based), search tolerance 0.1 kW, ceiling 2000 kW. 'Equal' means within 0.2 kW. Regenerated from the saved CSV.

## Networks

| code | buses | trafo_kVA | load_kW | existing_pv_kW | load_buses | base_v_max | base_line_% | base_trafo_% | status |
|---|---|---|---|---|---|---|---|---|---|
| 1-LV-rural1--0-sw | 15 | 160 | 80.0 | 160.4 | 13 | 1.0265 | 41.0 | 52.5 | ok |
| 1-LV-rural2--0-sw | 97 | 250 | 202.0 | 145.4 | 93 | 1.025 | 48.5 | 39.6 | ok |
| 1-LV-rural3--0-sw | 129 | 400 | 331.0 | 190.4 | 118 | 1.025 | 30.9 | 48.6 | ok |
| 1-LV-semiurb4--0-sw | 44 | 400 | 243.0 | 6.5 | 39 | 1.025 | 63.1 | 64.8 | ok |
| 1-LV-semiurb5--0-sw | 111 | 630 | 409.0 | 137.1 | 104 | 1.025 | 45.1 | 50.7 | ok |
| 1-LV-urban6--0-sw | 59 | 630 | 441.0 | 57.1 | 53 | 1.025 | 56.6 | 67.7 | ok |

## Hosting capacity (kW) and effect of default Volt-VAr

| code | buses | hc_nc median | hc_nc min-max | hc_vvar median | higher | equal | lower | median change % |
|---|---|---|---|---|---|---|---|---|
| 1-LV-rural1--0-sw | 13 | 82.3 | 80.1-82.7 | 80.1 | 0 | 0 | 13 | -2.67 |
| 1-LV-rural2--0-sw | 20 | 172.3 | 81.7-263.3 | 181.9 | 8 | 1 | 11 | -0.33 |
| 1-LV-rural3--0-sw | 20 | 196.0 | 98.4-239.2 | 196.1 | 8 | 4 | 8 | -0.02 |
| 1-LV-semiurb4--0-sw | 20 | 207.8 | 196.1-295.8 | 206.4 | 1 | 3 | 16 | -0.82 |
| 1-LV-semiurb5--0-sw | 20 | 265.0 | 190.4-324.3 | 262.6 | 4 | 3 | 13 | -0.69 |
| 1-LV-urban6--0-sw | 20 | 281.6 | 255.4-371.8 | 281.6 | 0 | 10 | 10 | -0.04 |

## Which limit binds first without control

| code | voltage first | thermal first | both | thermal element: trafo | thermal element: line |
|---|---|---|---|---|---|
| 1-LV-rural1--0-sw | 2 | 11 | 0 | 13 | 0 |
| 1-LV-rural2--0-sw | 9 | 11 | 0 | 0 | 20 |
| 1-LV-rural3--0-sw | 8 | 12 | 0 | 0 | 20 |
| 1-LV-semiurb4--0-sw | 1 | 19 | 0 | 0 | 20 |
| 1-LV-semiurb5--0-sw | 4 | 16 | 0 | 0 | 20 |
| 1-LV-urban6--0-sw | 0 | 20 | 0 | 0 | 20 |

## Hypothesis test: effect of Volt-VAr by first limit, per network

| code | first limit | buses | higher | equal | lower | median change % |
|---|---|---|---|---|---|---|
| 1-LV-rural1--0-sw | thermal | 11 | 0 | 0 | 11 | -2.67 |
| 1-LV-rural1--0-sw | voltage | 2 | 0 | 0 | 2 | -1.8 |
| 1-LV-rural2--0-sw | thermal | 11 | 0 | 1 | 10 | -1.03 |
| 1-LV-rural2--0-sw | voltage | 9 | 8 | 0 | 1 | 20.56 |
| 1-LV-rural3--0-sw | thermal | 12 | 0 | 4 | 8 | -1.03 |
| 1-LV-rural3--0-sw | voltage | 8 | 8 | 0 | 0 | 17.64 |
| 1-LV-semiurb4--0-sw | thermal | 19 | 0 | 3 | 16 | -0.87 |
| 1-LV-semiurb4--0-sw | voltage | 1 | 1 | 0 | 0 | 0.87 |
| 1-LV-semiurb5--0-sw | thermal | 16 | 0 | 3 | 13 | -1.36 |
| 1-LV-semiurb5--0-sw | voltage | 4 | 4 | 0 | 0 | 11.38 |
| 1-LV-urban6--0-sw | thermal | 20 | 0 | 10 | 10 | -0.04 |

## Hypothesis test: all networks together

| first limit | buses | higher | equal | lower | median change % | min change % | max change % |
|---|---|---|---|---|---|---|---|
| thermal | 89 | 0 | 21 | 68 | -0.9 | -3.64 | 0.0 |
| voltage | 24 | 21 | 0 | 3 | 17.64 | -2.11 | 31.56 |

## Volt-VAr split: gain on the voltage limit, penalty on the thermal limit

Gain is shown only where the voltage limit binds first. Elsewhere hc_v is very large (PV of several hundred kW or more) and the Volt-VAr iteration may not converge, so hc_v_vvar there is a numerical limit, not a physical one.

| code | voltage-first buses | median gain % (voltage-first buses) | median penalty % (all buses) | max penalty % (all buses) | hc_vvar = min(parts) |
|---|---|---|---|---|---|
| 1-LV-rural1--0-sw | 2 | 26.3 | 2.9 | 5.0 | 13/13 |
| 1-LV-rural2--0-sw | 9 | 30.6 | 2.4 | 11.6 | 20/20 |
| 1-LV-rural3--0-sw | 8 | 21.4 | 1.6 | 8.4 | 20/20 |
| 1-LV-semiurb4--0-sw | 1 | 24.8 | 0.9 | 2.4 | 20/20 |
| 1-LV-semiurb5--0-sw | 4 | 30.6 | 1.4 | 4.2 | 20/20 |
| 1-LV-urban6--0-sw | 0 | - | 0.0 | 1.5 | 20/20 |

## Screening indicator: effect of Volt-VAr by ratio r = hc_t / hc_v

| ratio hc_t / hc_v | buses | higher | equal | lower | median change % |
|---|---|---|---|---|---|
| < 1 (thermal first) | 89 | 0 | 21 | 68 | -0.9 |
| 1.00-1.05 | 5 | 2 | 0 | 3 | -1.5 |
| 1.05-1.10 | 3 | 3 | 0 | 0 | 4.6 |
| 1.10-1.25 | 4 | 4 | 0 | 0 | 11.64 |
| 1.25-1.50 | 6 | 6 | 0 | 0 | 21.4 |
| >= 1.50 | 6 | 6 | 0 | 0 | 18.78 |

## Dead-band check (PV-bus voltage at the no-control capacity)

- PV bus inside the dead band (<= 1.02 pu): 20 buses, effect equal in 20
- PV bus above the dead band: 93 buses, equal in 1, higher in 21, lower in 71

## Checks

- hc_nc equals min(hc_v, hc_t) within 0.2 kW: 113 of 113 buses
- hc_vvar equals min(hc_v_vvar, hc_t_vvar) within 0.2 kW: 113 of 113 buses
- buses where at least one search reached the 2000 kW ceiling (that limit never binds below it): 7
