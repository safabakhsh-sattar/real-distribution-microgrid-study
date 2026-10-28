# Predictions for scripts 19 to 21 (register before the first full run)

Registered on: 11:20 , 26 Oct 2026 (date and time, before any full run of scripts 19 and 20)

The predictions come from the gain-penalty model of Section 3.7 and from the
operating points of Section 3.8. They are fixed now. If one fails, the failure
is reported as it is. Nothing is refitted after the run.

## Design note (26 Oct 2026, before any capacity result)

The first run of script 19 showed that the SimBench slack voltage of the
study cases lW and lPV is 1.055 pu. This is above the 1.05 pu limit, so every
base case violated the limit and no capacity was computed. The design was
changed before any result was seen:

- Main test (label lW, lPV): load and PV factors of the case, slack voltage as
  stored (1.025 pu, as in the year), limit 1.05 pu.
- Second variant (label lW-sb, lPV-sb): the SimBench case as defined, slack
  1.055 pu, limit 1.10 pu (EN 50160). No prediction; reported as it is.

## Script 19: snapshot at the study cases (low load, high PV), main test

- **P5.** On the sample buses (113 per case), the rules of script 18 hold at
  each study case: P1 (r < 1: Volt-VAr never higher), P2 (r >= 1.05 and voltage
  first: Volt-VAr higher), P3 (dead band: equal), P4 (min rule).
- **P6.** Inverter limit S = Pn with active-power priority: if the PV factor of
  the case is at most 0.898, the limit changes no result. This follows from
  sqrt(1 - f^2) >= 0.44.
- **P7.** Volt-VAr on all PV units: at thermal-first buses the median change is
  at most the median change with one controlled unit (more reactive current
  through the binding element). At voltage-first buses the median change is
  at least the median change with one controlled unit.

## Scripts 20 and 21: one year at nine buses

- **P8.** Over the year, Volt-VAr is higher than no control at the four buses
  where the year capacity without control is voltage-limited (rural1 bus 4,
  semiurb5 buses 72 and 51, urban6 bus 17). It is not higher at the five buses
  where the year capacity is limited by a line or the transformer (rural1 buses
  7 and 11, semiurb5 bus 74, urban6 buses 54 and 50).
- **P9.** At the study case, the sign of the snapshot Volt-VAr effect agrees
  with the year sign at more of the nine buses than at the stored point.
- **P10.** Over the year, cos phi(P) raises the capacity less than Volt-VAr at
  each of the four voltage-limited buses. Reason: the PV factor stays at or
  below 0.59, so cos phi stays at or above 0.98.

## What the predictions do not cover

- Unbalanced three-phase operation (SimBench LV data give no phase allocation).
- Networks other than the six SimBench 1-LV grids.
