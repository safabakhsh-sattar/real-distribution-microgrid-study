# PV Hosting Capacity Enhancement in Real Distribution Networks:
# A Comparative Study of Volt-VAr and Volt-Watt Control Under Combined
# Voltage and Thermal Constraints

## Abstract
Rising residential PV adoption is constrained by distribution network
hosting capacity (HC), commonly limited by voltage rise. Smart inverter
functions such as Volt-VAr and Volt-Watt control (IEEE 1547-2018) have
been proposed to increase HC, but most studies evaluate these strategies
under voltage constraints alone, without considering thermal limits of
network equipment. This study quantifies HC on a real German low-voltage
feeder (SimBench 1-LV-rural1, 15 buses) using pandapower, under combined
voltage (1.05 pu) and thermal (line and transformer loading) constraints,
and compares baseline, Volt-VAr, and Volt-Watt control via binary search.
Results show that once the shared transformer becomes the binding
constraint, bus-level HC collapses to a narrow band (~78-82 kW)
independent of electrical distance, and Volt-VAr control can slightly
reduce HC relative to no control due to the apparent-power penalty of
reactive injection (S=√(P²+Q²)). Volt-Watt control, which curtails active
power directly, matched or outperformed Volt-VAr at every bus. These
findings indicate that the choice between Volt-VAr and Volt-Watt should
depend on which constraint — voltage or thermal — is binding in the
target network, rather than defaulting to Volt-VAr as common in prior
literature.

## 1. Introduction

Increasing penetration of rooftop photovoltaic (PV) systems in low-voltage
(LV) distribution networks is often constrained by voltage rise, a
phenomenon extensively studied under the term "hosting capacity" (HC).
Smart inverter functions — particularly Volt-VAr and Volt-Watt control
per IEEE 1547-2018 — have been proposed to mitigate this constraint.

However, most existing studies (e.g., Alfouly et al., 2025) evaluate
control strategies under voltage constraints alone, using simplified
single-feeder test systems, without quantifying hosting capacity in
kW or considering thermal loading of network equipment.
Transformer thermal limitations have been independently recognized as a
critical HC constraint: Ame-Oko and Lavrova (2024) address this via
battery storage dispatch, while Qamar et al. (2023), in a comprehensive
review, note that DSOs in several countries (e.g., Portugal <25%, Spain <50% and Italy <65% of the MV/LV transformer rating) impose hard limits on DG capacity as a fraction of transformer rating confirming the practical relevance of this constraint.Dissanayake
et al. (2022) combine voltage control with dynamic line rating on a
real Sri Lankan network but test only a single 25-node topology. However, 
none of these studies directly compare Volt-VAr and Volt-Watt control under 
simultaneous voltage and thermal constraints across multiple real network 
topologies - the specific gap this study addresses.
Similarly, Chathurangi et al. (2021) compare Volt-VAr and Volt-Watt performance
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

### 2.7 Mathematical Formulation

**Power Flow Constraints.** For each bus i, the AC power balance equations
solved by pandapower's Newton-Raphson method are:

P_i = V_i * Σ_k V_k * (G_ik*cos(θ_ik) + B_ik*sin(θ_ik))
Q_i = V_i * Σ_k V_k * (G_ik*sin(θ_ik) - B_ik*cos(θ_ik))

where V_i is voltage magnitude, θ_ik is the voltage angle difference
between buses i and k, and G_ik, B_ik are the real and imaginary parts
of the bus admittance matrix.

**Hosting Capacity Optimization Problem.** For each bus i, the hosting
capacity HC_i is formulated as:

HC_i = max P_PV
subject to:
  V_min ≤ V_j ≤ V_max,  ∀j ∈ buses
  L_l ≤ L_max,          ∀l ∈ lines
  L_t ≤ L_max,          ∀t ∈ transformers

where V_max = 1.05 pu (EN 50160), L_max = 100% (thermal rating), and
L_l, L_t are line and transformer loading percentages, each computed as:

L = |S| / S_rated × 100%,   S = √(P² + Q²)

**Volt-VAr Control Law.** Reactive power output Q as a function of
measured voltage V follows a piecewise-linear curve:

Q(V) = Q1,                                    V ≤ V1
Q(V) = Q1 + (Q2-Q1)(V-V1)/(V2-V1),            V1 < V ≤ V2
Q(V) = Q2,                                    V2 < V ≤ V3
Q(V) = Q3 + (Q4-Q3)(V-V3)/(V4-V3),            V3 < V ≤ V4
Q(V) = Q4,                                    V > V4

with (V1,V2,V3,V4) = (0.92, 0.98, 1.02, 1.08) pu and
(Q1,Q2,Q3,Q4) = (+0.44, 0, 0, -0.44) per unit of inverter rating S_rated.

**Volt-Watt Control Law.** Active power ratio as a function of voltage:

P_ratio(V) = 1.0,                              V ≤ VW1
P_ratio(V) = PW1 + (PW2-PW1)(V-VW1)/(VW2-VW1), VW1 < V ≤ VW2
P_ratio(V) = PW2,                              V > VW2

with (VW1, VW2) = (1.06, 1.10) pu and (PW1, PW2) = (1.0, 0.2).

**Apparent Power Penalty (Key Mechanism).** The core finding of this
study follows directly from the thermal constraint definition. For a
fixed active power injection P, any nonzero reactive power Q increases
apparent power:

S = √(P² + Q²) > P   when Q ≠ 0

Since thermal loading L is proportional to S, Volt-VAr's reactive
injection (|Q| > 0) necessarily increases L relative to Volt-Watt's
pure active-power curtailment (Q = 0), explaining the consistent
underperformance of Volt-VAr once thermal constraints bind.

**Damping for Numerical Stability.** To resolve oscillation in the
iterative Volt-Watt loop, the active power update uses exponential
smoothing:

P_t = P_{t-1} + α(P_target - P_{t-1}),   α = 0.3

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

### 3.4 Validation on a Second Feeder Topology

To test whether the transformer-bottleneck finding generalizes, the
voltage+thermal baseline analysis was repeated on a second SimBench
feeder with different topology: `1-LV-urban6--0-sw` (urban, 53 buses).

Results diverged sharply from the rural feeder: the transformer reached
only 35.7% loading at the critical bus's hosting capacity, while line
loading reached 99.8% — the binding constraint shifted from the
transformer to individual line segments. Hosting capacity varied widely
by bus (252–371 kW) rather than collapsing to a narrow shared band,
consistent with line-level (rather than network-wide) constraints.

This confirms that the binding constraint — transformer vs. line — is
topology-dependent: single-transformer rural feeders with concentrated
load tend toward transformer-bound capacity, while more distributed
urban feeders with longer line runs tend toward line-bound capacity.
Control strategy selection (Volt-VAr vs. Volt-Watt) should therefore
account for network topology, not only constraint type in isolation.

Full Volt-VAr and Volt-Watt comparison on the urban feeder confirmed the
rural finding with full consistency: Volt-Watt matched or outperformed
Volt-VAr at all 53 buses (100%), compared to 13/13 (100%) on the rural
feeder. Notably, in buses where voltage never exceeded the Volt-Watt
activation threshold (1.06 pu), Volt-Watt capacity equaled the
uncontrolled baseline exactly, while Volt-VAr still underperformed the
baseline — confirming that reactive power injection carries an apparent-
power cost even when voltage support is not strictly necessary.

## 4. Discussion
Results confirm that once thermal constraints (particularly transformer
loading) become binding, apparent power — not just active power —
determines the true hosting capacity limit: S = √(P² + Q²). Volt-VAr
control, by injecting reactive power to resolve voltage violations,
increases S and reaches the transformer's thermal limit sooner than a
strategy that leaves Q untouched. This explains why Volt-VAr capacity at
critical buses (4, 5) fell slightly below the uncontrolled baseline
(78.1 vs 80 kW).

Volt-Watt control, which curtails active power directly instead of
injecting reactive power, avoids this apparent-power penalty. The
three-way comparison confirms this: Volt-Watt matched or outperformed
Volt-VAr at every single bus in the network (Table 1), with the largest
relative advantage at buses closest to the transformer (e.g., bus 7:
81.1 kW under Volt-Watt vs 80.1 kW under Volt-VAr).

This finding qualifies prior literature that treats Volt-VAr as a
generally preferred strategy for hosting capacity enhancement (e.g.,
Alfouly et al., 2025, which evaluated PF vs Volt-VAr control but did not
consider thermal constraints). The present study shows that strategy
effectiveness is conditional on which constraint — voltage or thermal
loading — is binding. In networks with limited transformer headroom, a
common condition in real single-transformer LV feeders such as the one
studied here, Volt-Watt is the more robust choice.

A secondary methodological finding concerns numerical stability: the
initial Volt-Watt implementation exhibited sustained oscillation between
two states (full output and maximum curtailment) rather than converging,
a known risk in iterative coupled power-flow/local-control simulations.
Introducing a damping factor (α=0.3) resolved this, underscoring the
importance of verifying convergence — not just final output — when
implementing local control loops in power flow studies.

## 5. Conclusion
This study quantified PV hosting capacity on a real German LV distribution
feeder (SimBench 1-LV-rural1) under combined voltage and thermal
constraints, and compared Volt-VAr and Volt-Watt smart inverter control
strategies.This result held with full consistency (100% of buses) across two
structurally different feeder topologies — rural (transformer-bound)
and urban (line-bound) — indicating the finding is not an artifact of a
single network but a general property of thermal-constrained hosting
capacity.Three contributions emerge:

1. Electrical distance to the transformer strongly predicts hosting
   capacity under voltage-only constraints, but this relationship
   collapses once thermal limits are enforced — the shared transformer
   becomes a network-wide bottleneck independent of bus location.
2. Volt-VAr control can be counterproductive under thermal constraints,
   slightly reducing hosting capacity relative to no control, due to the
   apparent-power penalty of reactive injection.
3. Volt-Watt control consistently matches or outperforms Volt-VAr once
   the transformer is the binding constraint, making it the more reliable
   strategy for this common real-world network configuration.
   

Practically, these results suggest that DSOs and researchers should first
identify which constraint — voltage or thermal — is binding in a given
network before selecting a smart inverter control strategy, rather than
defaulting to Volt-VAr as is common practice in the literature.

## 6. Future Work
- Time-series hosting capacity using SimBench's annual load/generation profiles
- Combined PV + EV hosting capacity
- Validation on additional SimBench feeders (urban/semi-urban)

## References
[1] Alfouly et al. (2025). A novel inverter control strategy for maximum
    hosting capacity photovoltaic systems using power factor.
[2] Chathurangi et al. (2021). Comparative evaluation of solar PV hosting
    capacity enhancement using Volt-VAr and Volt-Watt control strategies.
[3] Ame-Oko, O. Lavrova, "Mitigation of limitation imposed on hosting capacity in low voltage networks by their distribution transformer loading and degradation considerations," IET Energy Systems Integration, 2024. doi:10.1049/esi2.12143

[4] Qamar, A. Arshad, K. Mahmoud, M. Lehtonen, "Hosting capacity in distribution grids: A review of definitions, performance indices, determination methodologies, and enhancement techniques," Energy Science & Engineering, 2023. doi:10.1002/ese3.1389

[5] Dissanayake, A. Wijethunge, J. Wijayakulasooriya, J. Ekanayake, "Optimizing PV-Hosting Capacity with the Integrated Employment of Dynamic Line Rating and Voltage Regulation," Energies, vol. 15, no. 22, 8537, 2022. doi:10.3390/en15228537   

 