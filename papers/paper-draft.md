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
[Summarize from docs/methodology.md — network model, baseline search,
Volt-VAr curve (IEEE 1547), Volt-Watt curve, thermal constraint check,
binary search algorithm, damping factor for numerical stability]

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

    