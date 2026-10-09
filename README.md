# real-distribution-microgrid-study

PV hosting capacity of real low-voltage distribution feeders under combined
voltage and thermal constraints, and the effect of smart-inverter control
(Volt-VAr, Volt-Watt) on deliverable capacity.

The long-term scope of the repository is hosting capacity of renewables,
electric vehicles and storage in real distribution networks, with a focus on
microgrids, voltage and losses. The first completed study (below) covers PV
hosting capacity and inverter control.

## Key findings

Two real German LV feeders from SimBench, voltage limit 1.05 pu (1.10 pu as
sensitivity), thermal limit 100% for lines and transformer, binary search with
0.1 kW tolerance.

| | Rural (`1-LV-rural1--0-sw`) | Urban (`1-LV-urban6--0-sw`) |
|---|---|---|
| Binding constraint | Transformer (160 kVA) | Line (transformer only 35.7%, line 99.8%) |
| No-control hosting capacity | 80.1 to 82.7 kW | 252.5 to 371.8 kW |
| Volt-VAr, IEEE 1547-2018 default | Lower at 13 of 13 buses (-1.5% to -3.6%) | Lower at 27 of 53 buses (up to -1.5%), equal at 26, never higher |
| Volt-Watt, IEEE 1547-2018 default | Identical to no control (13 of 13) | Identical to no control (53 of 53) |
| Volt-Watt tuned to 1.03-1.05 pu | Nameplate 91.1 to 403.5 kW, delivered power within 0.1 kW of no control | Nameplate up to 568.7 kW, delivered power within 0.1 kW of no control |

Conclusion: when a thermal limit binds, standard local voltage-control curves
do not raise deliverable PV capacity. A tuned Volt-Watt curve raises the
installed (nameplate) size but not the active power delivered, so nameplate
capacity alone can overstate the benefit by up to a factor of five.

Why Volt-VAr lowers capacity (measured at the binding element, scripts 10
and 10b): for the same PV size, Volt-VAr leaves the active power unchanged but
adds reactive flow, 6.6 to 14.8 kvar through the rural transformer and up to
31.8 kvar through the limiting urban line, lifting its current-based loading
above 100%. Urban buses whose voltage stays in the Volt-VAr dead band
(0.98 to 1.02 pu), 26 of 53, are unaffected.

Full write-up: [docs/paper-draft.md](docs/paper-draft.md)

## Figures

![Rural feeder](results/fig1_rural_comparison.png)
![Urban feeder](results/fig2_urban_comparison.png)
![Distance vs capacity](results/fig3_distance_vs_capacity.png)

## Feeder / Data Source

Real low-voltage distribution networks from the SimBench dataset (joint
research project of the University of Kassel, Fraunhofer IEE, RWTH Aachen and
TU Dortmund University, Germany). The networks follow the planning and
operation principles of German distribution operators; they are not
hypothetical test systems such as the IEEE 33-bus.

| Feeder | Transformer | Loads | Existing PV in the model |
|---|---|---|---|
| Rural, 15 buses | 160 kVA | 13 loads, 80 kW | 4 units, 160.4 kW |
| Urban, 53 load buses | 630 kVA | 111 loads, 441 kW | 5 units, 57.1 kW |

Hosting capacity is the **additional** PV that can be connected at one bus on
top of the existing generation, in a single deterministic snapshot (stored
SimBench values; no time series).

Why this data?
- Open and fully reproducible (no confidentiality restrictions)
- Directly relevant to German distribution network infrastructure
- Verifiable by any other researcher

## Method in brief

- pandapower Newton-Raphson power flow; one PV generator added per load bus
- Constraints: maximum voltage 1.05 pu (conservative planning limit, not the EN 50160 limit of +/-10%); line and transformer loading at most 100% (current-based, pandapower default)
- Largest feasible PV size found by binary search (0.1 kW tolerance)
- Scenarios: no control, Volt-VAr (IEEE 1547-2018 default), Volt-Watt default (1.06-1.10 pu) and Volt-Watt adapted (1.03-1.05 pu)
- Volt-Watt delivered power solved as the unique equilibrium by bisection
- Two capacities reported: nameplate (installed size) and delivered (active power actually injected)

Details: [docs/methodology.md](docs/methodology.md) and Section 2 of the paper draft.

## Reproducing the results

Requirements: Python 3, `pandapower`, `simbench`, `pandas`, `numpy`, `matplotlib`.
Run from the repository root.

| Order | Script | Purpose | Output in `results/` |
|---|---|---|---|
| 1 | `scripts/01_load_flow_baseline.py` | Base load flow and topology check | (console) |
| 2 | `scripts/02_hosting_capacity.py` | Voltage-only baseline and distance to transformer | `hosting_capacity_baseline.csv` |
| 3 | `scripts/02b_rural_baseline_thermal.py` | Rural no-control baseline, voltage + thermal | `rural_baseline_thermal.csv` |
| 4 | `scripts/03_volt_var_control.py` | Volt-VAr, rural | `hosting_capacity_comparison.csv` |
| 5 | `scripts/04_volt_watt_control.py` | Volt-Watt (first version, damped iteration), rural | `hosting_capacity_full_comparison.csv` |
| 6 | `scripts/05_validation_second_feeder.py` | Urban baseline, voltage + thermal | `validation_urban_feeder.csv` |
| 7 | `scripts/06_urban_feeder_full_comparison.py` | Urban Volt-VAr and Volt-Watt (first version) | `urban_full_comparison.csv` |
| 8 | `scripts/08_sensitivity_rural.py` | Final rural analysis, 7 scenarios | `sensitivity_rural.csv` |
| 9 | `scripts/08b_sensitivity_urban.py` | Final urban analysis, 7 scenarios (about 15-30 min) | `sensitivity_urban.csv` |
| 10 | `scripts/09_print_tables.py` | Compact tables from the two sensitivity CSVs | (console) |
| 11 | `scripts/10_trafo_pqs_rural.py` | Transformer P, Q, S with and without Volt-VAr, rural (about 1-2 min) | `trafo_pqs_rural.csv` |
| 12 | `scripts/10b_line_pqs_urban.py` | Limiting-line P, Q, I with and without Volt-VAr, urban (about 5-15 min) | `line_pqs_urban.csv` |
| 13 | `scripts/07_generate_figures.py` | Figures 1 to 3 | `fig1`, `fig2`, `fig3` (.png) |

`scripts/03b_diagnostic_transformer_check.py` is the diagnostic that revealed
the transformer bottleneck. Scripts 03 to 06 are earlier steps whose
Volt-Watt implementation was superseded by scripts 08 and 08b; the paper's
results come from 08 and 08b.

## Project Structure
```
data/       Raw and processed network data
scripts/    Python scripts (analysis, simulation, figures)
results/    Outputs: CSV tables and figures
papers/     Summaries of related papers
docs/       Paper draft, methodology, progress log, weekly reviews
```

## Limitations

- Single snapshot; SimBench study cases and annual profiles are not evaluated
- Existing PV units are uncontrolled; only the added unit applies Volt-VAr or Volt-Watt
- No inverter apparent-power limit is imposed
- Balanced single-phase equivalent (no phase imbalance)
- Two feeders only
- Transformer loading is current-based (pandapower default); a criterion on apparent power would be about 3% stricter, effect not evaluated

## Current Status

Study 1 (PV hosting capacity and inverter control on two feeders) is complete
and written up in [docs/paper-draft.md](docs/paper-draft.md). Earlier
statements that Volt-Watt outperforms Volt-VAr have been withdrawn: the
default Volt-Watt curve is inactive within the feasible region.

Next steps:
- Time-series analysis (SimBench profiles and study cases) to test whether the nameplate gain yields more annual energy
- Storage and EV flexibility to lift the transformer ceiling
- Sensitivity to a power-based transformer loading criterion