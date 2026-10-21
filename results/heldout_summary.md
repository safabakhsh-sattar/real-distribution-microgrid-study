# Multi-feeder snapshot results (script 11)

Voltage limit 1.05 pu, thermal limit 100 % (current-based), search tolerance 0.1 kW, ceiling 2000 kW. 'Equal' means within 0.2 kW. Run time 31.4 min.

## Networks

| code | buses | trafo_kVA | load_kW | existing_pv_kW | load_buses | base_v_max | base_line_% | base_trafo_% | status |
|---|---|---|---|---|---|---|---|---|---|
| 1-LV-rural1--1-sw | 15 | 160 | 81.8 | 468.2 | 13 | 1.0987 | 119.7 | 316.3 | base violation |
| 1-LV-rural2--1-sw | 97 | 250 | 216.8 | 228.7 | 93 | 1.025 | 38.6 | 34.8 | ok |
| 1-LV-rural3--1-sw | 129 | 400 | 481.7 | 242.2 | 118 | 1.025 | 70.6 | 64.6 | ok |
| 1-LV-semiurb4--1-sw | 44 | 400 | 251.3 | 6.5 | 39 | 1.025 | 65.8 | 63.9 | ok |
| 1-LV-semiurb5--1-sw | 111 | 630 | 469.7 | 181.8 | 104 | 1.025 | 36.9 | 42.8 | ok |
| 1-LV-urban6--1-sw | 59 | 630 | 443.8 | 140.0 | 53 | 1.025 | 54.6 | 56.2 | ok |
| 1-LV-rural1--2-sw | 15 | 160 | 181.3 | 468.2 | 13 | 1.0828 | 109.8 | 293.5 | base violation |
| 1-LV-rural2--2-sw | 97 | 250 | 327.2 | 233.5 | 93 | 1.025 | 44.6 | 52.8 | ok |
| 1-LV-rural3--2-sw | 129 | 400 | 552.8 | 252.3 | 118 | 1.025 | 87.8 | 78.7 | ok |
| 1-LV-semiurb4--2-sw | 44 | 400 | 337.3 | 172.2 | 39 | 1.0415 | 117.0 | 36.4 | base violation |
| 1-LV-semiurb5--2-sw | 111 | 630 | 552.3 | 184.7 | 104 | 1.025 | 51.3 | 40.7 | ok |
| 1-LV-urban6--2-sw | 59 | 630 | 620.6 | 171.2 | 53 | 1.025 | 64.0 | 75.8 | ok |

## Hosting capacity (kW) and effect of default Volt-VAr

| code | buses | hc_nc median | hc_nc min-max | hc_vvar median | higher | equal | lower | median change % |
|---|---|---|---|---|---|---|---|---|
| 1-LV-rural2--1-sw | 20 | 168.5 | 76.1-193.8 | 168.4 | 9 | 2 | 9 | 0.0 |
| 1-LV-rural2--2-sw | 20 | 151.9 | 97.7-218.3 | 150.1 | 4 | 6 | 10 | -0.13 |
| 1-LV-rural3--1-sw | 20 | 192.6 | 107.8-293.9 | 194.8 | 4 | 7 | 9 | -0.04 |
| 1-LV-rural3--2-sw | 20 | 194.6 | 117.8-317.4 | 198.3 | 4 | 12 | 4 | 0.0 |
| 1-LV-semiurb4--1-sw | 20 | 207.7 | 195.4-300.0 | 206.3 | 1 | 3 | 16 | -0.88 |
| 1-LV-semiurb5--1-sw | 20 | 256.6 | 173.4-307.8 | 253.8 | 4 | 4 | 12 | -0.66 |
| 1-LV-semiurb5--2-sw | 20 | 222.6 | 123.7-319.9 | 222.6 | 1 | 5 | 14 | -1.03 |
| 1-LV-urban6--1-sw | 20 | 264.8 | 212.7-337.5 | 263.8 | 0 | 10 | 10 | -0.12 |
| 1-LV-urban6--2-sw | 20 | 267.8 | 222.8-339.7 | 267.0 | 0 | 18 | 2 | 0.0 |

## Which limit binds first without control

| code | voltage first | thermal first | both | thermal element: trafo | thermal element: line |
|---|---|---|---|---|---|
| 1-LV-rural2--1-sw | 9 | 11 | 0 | 0 | 20 |
| 1-LV-rural2--2-sw | 5 | 15 | 0 | 1 | 19 |
| 1-LV-rural3--1-sw | 4 | 16 | 0 | 0 | 20 |
| 1-LV-rural3--2-sw | 4 | 16 | 0 | 0 | 20 |
| 1-LV-semiurb4--1-sw | 1 | 19 | 0 | 0 | 20 |
| 1-LV-semiurb5--1-sw | 4 | 16 | 0 | 0 | 20 |
| 1-LV-semiurb5--2-sw | 2 | 18 | 0 | 0 | 20 |
| 1-LV-urban6--1-sw | 0 | 20 | 0 | 0 | 20 |
| 1-LV-urban6--2-sw | 0 | 20 | 0 | 0 | 20 |

## Hypothesis test: effect of Volt-VAr by first limit, per network

| code | first limit | buses | higher | equal | lower | median change % |
|---|---|---|---|---|---|---|
| 1-LV-rural2--1-sw | thermal | 11 | 0 | 2 | 9 | -1.23 |
| 1-LV-rural2--1-sw | voltage | 9 | 9 | 0 | 0 | 21.43 |
| 1-LV-rural2--2-sw | thermal | 15 | 0 | 6 | 9 | -0.47 |
| 1-LV-rural2--2-sw | voltage | 5 | 4 | 0 | 1 | 11.8 |
| 1-LV-rural3--1-sw | thermal | 16 | 0 | 7 | 9 | -0.21 |
| 1-LV-rural3--1-sw | voltage | 4 | 4 | 0 | 0 | 18.26 |
| 1-LV-rural3--2-sw | thermal | 16 | 0 | 12 | 4 | 0.0 |
| 1-LV-rural3--2-sw | voltage | 4 | 4 | 0 | 0 | 15.26 |
| 1-LV-semiurb4--1-sw | thermal | 19 | 0 | 3 | 16 | -0.91 |
| 1-LV-semiurb4--1-sw | voltage | 1 | 1 | 0 | 0 | 1.23 |
| 1-LV-semiurb5--1-sw | thermal | 16 | 0 | 4 | 12 | -1.23 |
| 1-LV-semiurb5--1-sw | voltage | 4 | 4 | 0 | 0 | 7.42 |
| 1-LV-semiurb5--2-sw | thermal | 18 | 0 | 5 | 13 | -1.03 |
| 1-LV-semiurb5--2-sw | voltage | 2 | 1 | 0 | 1 | 0.12 |
| 1-LV-urban6--1-sw | thermal | 20 | 0 | 10 | 10 | -0.12 |
| 1-LV-urban6--2-sw | thermal | 20 | 0 | 18 | 2 | 0.0 |

## Hypothesis test: all networks together

| first limit | buses | higher | equal | lower | median change % | min change % | max change % |
|---|---|---|---|---|---|---|---|
| thermal | 151 | 0 | 67 | 84 | -0.25 | -4.41 | 0.0 |
| voltage | 29 | 27 | 0 | 2 | 14.13 | -2.5 | 32.02 |

## Volt-VAr split: gain on the voltage limit, penalty on the thermal limit

Gain is shown only where the voltage limit binds first. Elsewhere hc_v is very large (PV of several hundred kW or more) and the Volt-VAr iteration may not converge, so hc_v_vvar there is a numerical limit, not a physical one.

| code | voltage-first buses | median gain % (voltage-first buses) | median penalty % (all buses) | max penalty % (all buses) | hc_vvar = min(parts) |
|---|---|---|---|---|---|
| 1-LV-rural2--1-sw | 9 | 30.9 | 2.6 | 16.9 | 20/20 |
| 1-LV-rural2--2-sw | 5 | 24.3 | 0.8 | 13.1 | 20/20 |
| 1-LV-rural3--1-sw | 4 | 18.4 | 0.4 | 7.1 | 20/20 |
| 1-LV-rural3--2-sw | 4 | 18.7 | 0.0 | 6.3 | 20/20 |
| 1-LV-semiurb4--1-sw | 1 | 24.8 | 1.0 | 2.5 | 20/20 |
| 1-LV-semiurb5--1-sw | 4 | 30.8 | 1.5 | 3.9 | 20/20 |
| 1-LV-semiurb5--2-sw | 2 | 31.1 | 1.1 | 3.5 | 20/20 |
| 1-LV-urban6--1-sw | 0 | - | 0.1 | 1.6 | 20/20 |
| 1-LV-urban6--2-sw | 0 | - | 0.0 | 0.8 | 20/20 |

## Screening indicator: effect of Volt-VAr by ratio r = hc_t / hc_v

| ratio hc_t / hc_v | buses | higher | equal | lower | median change % |
|---|---|---|---|---|---|
| < 1 (thermal first) | 151 | 0 | 67 | 84 | -0.25 |
| 1.00-1.05 | 5 | 3 | 0 | 2 | 0.19 |
| 1.05-1.10 | 3 | 3 | 0 | 0 | 2.75 |
| 1.10-1.25 | 8 | 8 | 0 | 0 | 10.88 |
| 1.25-1.50 | 8 | 8 | 0 | 0 | 20.54 |
| >= 1.50 | 5 | 5 | 0 | 0 | 20.68 |

## Dead-band check (PV-bus voltage at the no-control capacity)

- PV bus inside the dead band (<= 1.02 pu): 61 buses, effect equal in 61
- PV bus above the dead band: 119 buses, equal in 6, higher in 27, lower in 86

## Checks

- hc_nc equals min(hc_v, hc_t) within 0.2 kW: 180 of 180 buses
- hc_vvar equals min(hc_v_vvar, hc_t_vvar) within 0.2 kW: 180 of 180 buses
- buses where at least one search reached the 2000 kW ceiling (that limit never binds below it): 14
