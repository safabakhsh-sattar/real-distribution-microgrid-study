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

## Current Status
Baseline hosting capacity established (critical buses: 4, 5 at 80 kW).
Volt-VAr control (IEEE 1547) implemented and validated — critical bus
capacity increased to ~101–102 kW (~26–27% improvement); network-wide
average improvement ~45%. Some buses reached the 300 kW search ceiling
and require a higher limit for exact values. Literature review: 2 papers
critically summarized.

