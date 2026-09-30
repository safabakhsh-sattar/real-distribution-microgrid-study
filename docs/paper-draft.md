# PV Hosting Capacity Enhancement in Real Distribution Networks:
# A Comparative Study of Volt-VAr and Volt-Watt Control Under Combined
# Voltage and Thermal Constraints

## Abstract
[Write last — 150-200 words summarizing problem, method, key result]

## 1. Introduction
Increasing penetration of rooftop photovoltaic (PV) systems in low-voltage
(LV) distribution networks is often constrained by voltage rise, a
phenomenon extensively studied under the term "hosting capacity" (HC).
Smart inverter functions — particularly Volt-VAr and Volt-Watt control
per IEEE 1547-2018 — have been proposed to mitigate this constraint.

However, most existing studies (e.g., Alfouly et al., 2025) evaluate
control strategies under voltage constraints alone, using simplified
single-feeder test systems, without quantifying hosting capacity in
kW or considering thermal loading of network equipment. Similarly,
Chathurangi et al. (2021) compare Volt-VAr and Volt-Watt performance
across feeder types but do not examine the interaction between reactive
power support and transformer thermal limits.

This study addresses this gap by: (1) quantifying hosting capacity on a
real multi-bus LV feeder (SimBench 1-LV-rural1) under combined voltage
AND thermal constraints, and (2) comparing Volt-VAr and Volt-Watt control
to identify which strategy performs better once the binding constraint
shifts from voltage to transformer thermal loading.

## 2. Methodology
### 2.1 Network Model
The study uses the SimBench dataset (Meinecke et al., University of
Kassel, Fraunhofer IEE, RWTH Aachen, TU Dortmund), specifically the
`1-LV-rural1--0-sw` model: a real German low-voltage rural feeder with
15 buses, 13 lines, 1 transformer, and 13 loads (total 80 kW). Unlike
standard synthetic test systems (e.g., IEEE 33-bus), SimBench networks
are derived from real German DSO planning principles. Power flow
calculations use pandapower's Newton-Raphson solver.

### 2.2 Baseline Hosting Capacity (Voltage-Only)
For each load bus, a PV generator (sgen) was incrementally added in 1 kW
steps. After each increment, a power flow was solved; the search stopped
when the maximum network voltage exceeded 1.05 pu (EN 50160 upper limit).
The last feasible value was recorded as that bus's baseline hosting
capacity. Electrical distance from each bus to the transformer was
computed via pandapower's topology module (calc_distance_to_bus) to test
the hypothesis that capacity decreases with distance.

### 2.3 Volt-VAr Control
Reactive power support followed the IEEE 1547-2018 default Volt-VAr
curve, defined by voltage breakpoints V1=0.92, V2=0.98, V3=1.02,
V4=1.08 pu, with corresponding reactive power ratios Q1=+0.44,
Q2=Q3=0.0, Q4=-0.44 (per unit of inverter rating). Since voltage and
reactive power are mutually dependent, each power flow was solved
iteratively (up to 10 iterations) until convergence.

### 2.4 Volt-Watt Control
Active power curtailment followed the IEEE 1547-2018 Volt-Watt curve,
with breakpoints VW1=1.06, VW2=1.10 pu and power ratios PW1=1.0
(no curtailment) to PW2=0.2 (80% curtailment). The initial direct
iterative implementation exhibited a numerical oscillation between two
states (full output / 20% output) rather than convergence. This was
resolved using a damping factor (α=0.3): at each iteration, the injected
power was updated as P_new = P_old + α × (P_target − P_old), and the
iteration count was increased to 30 to allow convergence under damping.

### 2.5 Thermal Constraints
Beyond the voltage limit, each candidate PV capacity was additionally
checked against line and transformer thermal loading, using
pandapower's res_line.loading_percent and res_trafo.loading_percent,
with a 100% limit. A capacity was accepted only if both voltage and
thermal constraints were simultaneously satisfied.

### 2.6 Search Algorithm
The initial linear search (1 kW steps up to 1000 kW) was computationally
expensive. It was replaced with a binary search (1 kW tolerance),
reducing the number of power-flow evaluations per bus from up to 1000
to approximately 10, without loss of accuracy.

## 3. Results

### 3.1 Baseline Hosting Capacity (Voltage-Only)
Hosting capacity ranged from 80 kW (buses 4, 5) to 286 kW (bus 7),
strongly correlated with electrical distance to the transformer
(calc_distance_to_bus), confirming the expected inverse relationship
between distance and capacity.

### 3.2 Effect of Thermal Constraints
Adding transformer and line loading limits (100%) revealed the true
binding constraint: the single shared transformer, reaching 98.8%
loading at only 80 kW of PV injection — far below the voltage-only
estimates. This collapsed all bus-level capacities to a narrow band
(78–82 kW), independent of electrical distance.

### 3.3 Volt-VAr vs. Volt-Watt Comparison

| Bus | Baseline (kW) | Volt-VAr (kW) | Volt-Watt (kW) |
|---|---|---|---|
| 4 | 80 | 78.1 | 80.1 |
| 5 | 80 | 78.1 | 80.1 |
| 0 | 115 | 79.1 | 82.0 |
| 2 | 121 | 79.1 | 82.0 |
| 13 | 130 | 79.1 | 82.0 |
| 12 | 133 | 79.1 | 82.0 |
| 9 | 179 | 80.1 | 82.0 |
| 11 | 180 | 80.1 | 82.0 |
| 6 | 183 | 80.1 | 82.0 |
| 8 | 196 | 80.1 | 82.0 |
| 10 | 229 | 80.1 | 82.0 |
| 1 | 242 | 80.1 | 82.0 |
| 7 | 286 | 80.1 | 81.1 |

Volt-Watt matched or outperformed Volt-VAr at every single bus.

## 4. Discussion
The consistent underperformance of Volt-VAr relative to Volt-Watt under
thermal constraints is explained by apparent power: S = √(P² + Q²).
Reactive power injected to support voltage adds to S without contributing
useful active energy delivery, pushing the transformer toward its thermal
limit sooner. Volt-Watt, by curtailing active power directly, avoids this
penalty entirely.

This finding qualifies prior literature that treats Volt-VAr as a
generally superior or default strategy (as implied in Alfouly et al.,
2025): its advantage holds only while voltage remains the binding
constraint. In transformer-limited networks — common in real single-
transformer LV feeders — Volt-Watt is the more effective choice.

## 5. Conclusion
[Summarize contribution: quantitative HC + thermal constraints + strategy
comparison on a real German LV network, with actionable guidance:
check the binding constraint before choosing a smart inverter strategy]

## 6. Future Work
- Time-series hosting capacity using SimBench's annual load/generation profiles
- Combined PV + EV hosting capacity
- Validation on additional SimBench feeders (urban/semi-urban)

## References
[1] Alfouly et al. (2025). A novel inverter control strategy for maximum
    hosting capacity photovoltaic systems using power factor.
[2] Chathurangi et al. (2021). Comparative evaluation of solar PV hosting
    capacity enhancement using Volt-VAr and Volt-Watt control strategies.

    git add docs/paper-draft.md
git commit -m "Add first paper draft skeleton with results"
git push