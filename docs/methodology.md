# Methodology

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

## 4. Critical Finding: Thermal Limits Dominate Under Reactive Support
Initial voltage-only search showed large, unrealistic capacities
(>1000 kW) at buses electrically close to the transformer. Diagnostic
inspection (scripts/03b_diagnostic_transformer_check.py) revealed the
transformer reaching 98.8% loading while lines stayed below 85% —
confirming the transformer, not the lines, as the binding constraint
in this single-transformer topology.

Re-running with combined voltage (1.05 pu) AND thermal (100% loading,
lines + transformer) constraints showed hosting capacity converging to
~78–80 kW across nearly all buses, regardless of electrical distance —
because the transformer is a shared bottleneck for the whole feeder.

Notably, Volt-VAr capacity at critical buses (4, 5) came out slightly
*below* the baseline (78.1 vs 80 kW). This is because transformer
thermal loading depends on apparent power (S = √(P²+Q²)); injecting
reactive power to solve the voltage constraint increases S and reaches
the thermal limit sooner. This is the project's core finding: Volt-VAr
is effective only when voltage is the binding constraint; when the
binding constraint shifts to transformer thermal capacity, reactive
power injection can reduce, not increase, hosting capacity.