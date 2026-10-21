# real-distribution-microgrid-study

PV hosting capacity of real low-voltage distribution feeders under combined
voltage and thermal constraints, and the effect of smart-inverter control
(Volt-VAr, Volt-Watt) on deliverable capacity.

Central question: **when does the default Volt-VAr curve help or hurt PV
hosting capacity in low-voltage feeders, and can a simple indicator predict
it?**

The long-term scope of the repository is hosting capacity of renewables,
electric vehicles and storage in real distribution networks, with a focus on
microgrids, voltage and losses. The studies so far cover PV hosting capacity
and inverter control: Study 1 (two feeders), Study 2a (six networks, snapshot)
and Study 2b (three feeders, one year of profiles).

## Key findings

### Study 1: two feeders in detail

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

### Study 2a: six networks, 113 buses (snapshot, script 11)

- Without control the thermal limit binds first at 89 of 113 buses and the voltage limit at 24. The thermal element is the transformer on rural1 only and a line on the other five networks.
- Volt-VAr acts as a gain on the voltage limit and a penalty on the thermal limit; the capacity is the smaller of the two (113 of 113 buses).
- In the snapshot, where the thermal limit binds first, Volt-VAr never raised capacity (0 of 89; median -0.9%, worst -3.6%). Where the voltage limit binds first it raised capacity at 21 of 24 buses (median +17.6%, up to +31.6%).
- Snapshot screening indicator r = hc_t / hc_v from two searches without control: no gain for r < 1 (0 of 89), gain at all 19 buses with r >= 1.05, mixed between 1.00 and 1.05. The threshold is specific to this sample.
- Buses inside the Volt-VAr dead band at the uncontrolled capacity (<= 1.02 pu) are unchanged (20 of 20).
- Held-out test (script 18): on scenarios 1 and 2 of the same six networks (180 buses, nine cases, predictions written before the run) the rules held: no gain for r < 1 (0 of 151), gain at all 24 buses with r >= 1.05, dead band unchanged (61 of 61). These are new operating points, not new networks; SimBench 1-LV has no further grids.

### Study 2b: one year of profiles, three feeders (scripts 12, 12b)

- Time-series capacity (no control, 15-minute steps) is 1.23 to 2.15 times the snapshot capacity at line- or transformer-limited buses and 0.58 to 0.85 times at the voltage-limited buses of semiurb5 and urban6 (1.33 at the voltage-limited far bus of rural1). The sign of the bias depends on the binding limit.
- Sizing the far bus by the snapshot capacity gave 273 hours per year above 1.05 pu at semiurb5 bus 51 and 49 hours at urban6 bus 17 (hourly means).
- The tuned Volt-Watt curve (1.03-1.05 pu) removed every hourly violation in the nine cases but curtailed 8% to 32% of the available energy at the sizes studied. Each extra kW of nameplate delivered 61% to 79% of the average annual energy per kW.
- Volt-VAr over the year at the far bus of each feeder (script 15, every daylight step verified): capacity rose from 106.5 to 165.1 kW at rural1 (+55.0%), from 110.5 to 174.1 kW at semiurb5 (+57.6%) and from 224.7 to 390.8 kW at urban6 (+73.9%).
- The snapshot predicted a small penalty at rural1 and urban6, so the snapshot indicator did not hold over the year at two of the three far buses. Scripts 16 and 17 show that the code is not the cause: the year's PV peaks at about 58% of the snapshot PV.
- Hourly voltage violations at the snapshot sizes fell to 3 hours or fewer at the far buses (script 14).

Full write-up: [docs/paper-draft.md](docs/paper-draft.md)

## Figures

![Rural feeder](results/fig1_rural_comparison.png)
![Urban feeder](results/fig2_urban_comparison.png)
![Distance vs capacity](results/fig3_distance_vs_capacity.png)
![Volt-VAr effect vs indicator r](results/fig4_effect_vs_ratio.png)
![Snapshot vs time series](results/fig5_snapshot_vs_timeseries.png)
![Energy and curtailment](results/fig6_energy_curtailment.png)

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

Study 2a and 2b use further SimBench networks: rural2, rural3, semiurb4,
semiurb5 (111 buses, 630 kVA) and urban6, scenario 0.

Hosting capacity is the **additional** PV that can be connected at one bus on
top of the existing generation. Studies 1 and 2a use a single deterministic
snapshot (stored SimBench values); Study 2b uses one year of 15-minute SimBench
profiles.

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
| 14 | `scripts/11_multi_feeder_snapshot.py` | Study 2a: six networks, 113 buses, six capacities per bus (about 1 h; `--workers`, `--resume`, `--summarize-only`) | `multi_feeder_snapshot.csv`, `multi_feeder_summary.md` |
| 15 | `scripts/12_timeseries.py` | Study 2b: time-series capacity and annual energy, three feeders (244 min in one process; `--workers`, `--resume`) | `timeseries_hc.csv`, `timeseries_energy.csv`, `timeseries_summary.md` |
| 16 | `scripts/12b_binding_conditions.py` | Load and PV factor at the binding step (about 1 min) | `binding_conditions.csv`, `binding_conditions.md` |
| 17 | `scripts/13_figures_study2.py` | Figures 4 to 6 | `fig4`, `fig5`, `fig6` (.png) |
| 18 | `scripts/14_vvar_annual.py` | Volt-VAr over one year at the far buses, hourly means (about 2.5 h with `--workers 3`) | `vvar_annual_hour_summary.md` |
| 19 | `scripts/15_vvar_timeseries_hc.py` | Volt-VAr time-series capacity at the far buses, 15-minute steps, all daylight steps verified (about 7 h in one process; `--workers`, `--sampled` for a quick test) | `vvar_timeseries_hc.csv`, `vvar_timeseries_summary.md` |
| 20 | `scripts/16_vvar_snapshot_check.py` | Checks the Volt-VAr code against the script 11 snapshot values (a few minutes) | `snapshot_vvar_check.csv` |
| 21 | `scripts/17_snapshot_condition.py` | Compares the year's PV and load with the stored operating point (no power flow) | `snapshot_condition.csv` |
| 22 | `scripts/18_heldout_indicator.py` | Held-out test of r: scenarios 1 and 2 of the six 1-LV networks, 180 buses in nine cases (about 30 min with `--workers 3`) | `heldout_summary.md`, `heldout_snapshot.csv` |

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

- Studies 1 and 2a are single snapshots; scenarios 1 and 2 of the six networks were used only for the held-out test (script 18), and other SimBench study cases are not evaluated
- Study 2a: 113 buses of six networks (all buses of rural1, 20 evenly spaced buses of each other network); counts are sample counts, the indicator threshold is sample-specific, and the held-out test used other operating points of the same networks, not other networks
- Study 2b: three feeders, three buses per feeder, one weather year, one fleet-average PV profile; energy, violation hours and losses use hourly means; the capacity search is a critical-step method with a verification set
- Volt-VAr over the year was simulated at the far bus of each feeder only; the indicator was not tested over the year at other buses
- Existing PV units are uncontrolled; only the added unit applies Volt-VAr or Volt-Watt
- No inverter apparent-power limit is imposed
- Balanced single-phase equivalent (no phase imbalance)
- Transformer loading is current-based (pandapower default); a criterion on apparent power would be about 3% stricter, effect not evaluated

## Current Status

Study 1 (two feeders), Study 2a (six networks, snapshot) and Study 2b (three
feeders, one year of profiles) are complete and written up in
[docs/paper-draft.md](docs/paper-draft.md), organised around the central
question above. Earlier statements that Volt-Watt outperforms Volt-VAr have
been withdrawn: the default Volt-Watt curve is inactive within the feasible
region.

Next steps:
- Volt-VAr over the year at the near and middle buses of each feeder, to test the indicator with profiles
- Inverter apparent-power limit (P-priority and Q-priority); other SimBench study cases; a held-out test on networks other than the six used here (for example LV subnets of the SimBench MV grids)
- Storage and EV flexibility to lift the thermal ceiling