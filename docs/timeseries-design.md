# Time-series study: design (draft, 9 Oct 2026)

Status: plan only. No time-series results exist yet. The numbers in Section 1
come from the SimBench profile data, read with `simbench.get_absolute_values`.

## 1. What the data check showed

Both feeders come with one year of profiles: 35,136 steps of 15 minutes
(2016, a leap year). Loads and PV have profiles; storage is empty.

| | Rural `1-LV-rural1--0-sw` | Urban `1-LV-urban6--0-sw` |
|---|---|---|
| Loads: stored sum / annual peak in the profile | 80.0 / 74.4 kW | 441.0 / 186.1 kW |
| Existing PV: stored nameplate / annual peak in the profile | 160.4 / 92.4 kW | 57.1 / 33.3 kW |
| PV profile maximum (fraction of nameplate) | 0.59 to 0.60 | 0.59 to 0.63 |
| PV full-load hours per year | 622 to 676 | 622 to 676 |
| Highest net export in the profile | 69.4 kW (27 Jul, 13:15) | 5.7 kW |
| Net flow in the stored snapshot | 80.4 kW export | 383.9 kW import |

What this means for Study 1:

1. The stored snapshot is not an hour that occurs in the year. On the urban
   feeder it has all loads at their rating at once (441 kW, against a
   profile peak of 186 kW). On the rural feeder it has all existing PV at
   100% of nameplate, while the profile never exceeds about 60%.
2. A PV unit added in a time-series study injects at most about 0.6 times its
   nameplate. So nameplate hosting capacity from the snapshot and from a
   time-series study differ by construction.
3. The nameplate-versus-delivered question (does a larger nameplate under a
   tuned Volt-Watt curve give more annual energy?) can only be answered with
   time series. Curtailment happens in few hours, and the cost of a
   curtailed hour is small compared with the benefit of the other hours.

Hypothesis, not a result: because of point 2, the time-series capacity may be
well above the snapshot capacity (roughly 1.5 to 2 times). This must be tested
before anything is claimed.

## 2. Questions

- Q1. How does the time-series hosting capacity (largest nameplate with no
  violation in any step of the year, no control) compare with the snapshot
  value of Study 1?
- Q2. With the tuned Volt-Watt curve (1.03 to 1.05 pu), does a larger nameplate
  give more annual energy, and how much of it is curtailed?
- Q3 (optional). Does the default Volt-VAr curve change the time-series
  capacity?

## 3. Method (draft)

- Profiles from `get_absolute_values(net, profiles_instead_of_study_cases=True)`.
  Existing PV is uncontrolled. The added PV uses the PV profile of the existing
  units (same weather), scaled to its nameplate.
- Each step: set loads and existing PV, add the new PV at P_n times its
  profile, apply the control rule, run the power flow. Constraints as in
  Study 1: 1.05 pu, line and transformer loading at most 100% (current-based).
- Capacity search: binary search on P_n using a reduced set of critical steps
  (the 500 steps with the highest net injection, about 1.4% of the year), then
  a check of the result on all 35,136 steps.
- Energy: E = sum of delivered power times 0.25 h. Curtailed energy is the
  profile energy minus E.
- Speed: one power flow takes about 28 ms (rural) and 32 ms (urban) in the
  cloud workspace without numba. A full year is 16 to 19 minutes per size, so
  an exhaustive search on the full year is not possible. Hourly aggregation
  (8,784 steps, about 4 minutes) is the fallback.

## 4. Scope of the first pass

- Rural feeder only, three buses: one far from the transformer (bus 4), one
  near (bus 7) and one in between, chosen from the distance table.
- Scenarios: no control and Volt-Watt adapted. Volt-Watt default only if time
  allows.
- Output per bus: snapshot capacity, time-series capacity, annual energy and
  curtailed share for the adapted Volt-Watt curve at three nameplate sizes
  (snapshot capacity, time-series capacity, in between).
- Planned script: `scripts/11_timeseries_rural.py`; results in
  `results/timeseries_rural.csv`.

## 5. Decisions needed before coding

1. Resolution: 15 minutes (as stored) or hourly for the first pass.
2. Which three buses.
3. Whether the urban feeder follows in the same week or after the rural result.

## 6. Risks and limits

- A time-series capacity much larger than the snapshot makes some Study 1
  statements conditional on the operating point. They must be reported that
  way, and limitation 1 of the paper becomes more important.
- One weather year, and the PV profiles of different units are almost
  identical.
- Balanced single-phase model, no inverter apparent-power limit (as in
  Study 1).