# real-distribution-microgrid-study
Investigation of the Hosting Capacity of Renewable Resources, Electric Vehicles, and Storage in a Real Distribution Network, with a focus on Microgrids, Voltage, and Losses.

## Feeder / Data Source
Actual low-pressure distribution network from the SimBench dataset (joint research project of the University of Kassel, Fraunhofer IEE, RWTH Aachen, and TU Dortmund University, Germany), model: `1-LV-rural1--0-sw`
This network is built upon the principles of real planning and operation of German electricity distribution operators and includes real load/generation time series—not a hypothetical standard model like the IEEE 33-bus.

Why this network?
- Open and fully reproducible data (no confidentiality restrictions)
- Directly relevant to German distribution network infrastructure — aligned with the PhD application path
- Verifiable by any other researcher

## Project Structure
```
data/       Raw and processed network data
scripts/    Python scripts (analysis, simulation)
results/    Outputs: charts, tables, reports
papers/     Summaries of related papers
docs/       Methodology documentation and weekly reviews
```

 ## Current Status
Full hosting capacity analysis complete on primary feeder (rural):
Baseline, Volt-VAr, and Volt-Watt under voltage + thermal constraints.
Validated on a second feeder (urban) — confirmed that the binding
constraint (transformer vs. line) is topology-dependent. Paper draft
complete end-to-end (Abstract through Validation). See docs/paper-draft.md.
