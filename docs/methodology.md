Methodology

## 1. Network Model
Source: SimBench dataset, model `1-LV-rural1--0-sw` (real German LV rural
feeder: 15 buses, 13 lines, 1 transformer, 13 loads, 80 kW total load).
Tool: pandapower (Newton-Raphson power flow).

## 2. Baseline Hosting Capacity
Single-bus PV injection, incremented until voltage exceeds 1.05 pu
(EN 50160 limit). No reactive power control. Result: critical buses
identified via electrical distance to transformer (calc_distance_to_bus) —
buses 4 and 5 (farthest) show lowest capacity (80 kW), confirming the
inverse relationship between electrical distance and hosting capacity.

## 3. Volt-VAr Control (IEEE 1547-2018)
Reactive power support curve with breakpoints V1=0.92, V2=0.98, V3=1.02,
V4=1.08 pu and Q1=+0.44, Q4=-0.44 (per unit of inverter rating).
Iterative power flow (10 iterations) for convergence between voltage and Q.

## 4. Adding Thermal Constraints
Initial voltage-only search showed unrealistic capacities (>1000 kW) at
buses electrically close to the transformer. Diagnostic inspection
(scripts/03b_diagnostic_transformer_check.py) revealed the transformer
reaching 98.8% loading while lines stayed below 85% — confirming the
transformer, not the lines, as the binding constraint in this
single-transformer topology.

## 5. Key Finding: Transformer as Shared Bottleneck
With combined voltage AND thermal constraints, hosting capacity converges
to ~78-80 kW across nearly all buses, regardless of electrical distance —
because all buses share a single transformer as a common constraint point.

Notably, Volt-VAr capacity at critical buses (4, 5) came out slightly
*below* the baseline (78.1 vs 80 kW). This is because transformer thermal
loading depends on apparent power (S = √(P²+Q²)); injecting reactive power
to solve the voltage constraint increases S and reaches the thermal limit
sooner. This is the project's core finding: Volt-VAr is effective only
when voltage is the binding constraint; when the binding constraint shifts
to transformer thermal capacity, reactive power injection can reduce, not
increase, hosting capacity.

## 6. Future Work (Parked)
Volt-Watt control was attempted as an alternative (reducing active power
instead of injecting reactive power, avoiding the apparent-power penalty
above). Initial implementation showed numerical oscillation in the
iterative loop between voltage and power output — a known challenge in
coupled power-flow/local-control simulations, typically resolved via a
damping factor. This remains unresolved and is parked for a future
session, not abandoned.