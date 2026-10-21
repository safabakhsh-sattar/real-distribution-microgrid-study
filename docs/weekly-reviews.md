# Weekly Reviews

## Week 1 (19–25 Sep 2026)
- Evaluation: Much better than expected, ahead of schedule
- Done: fresh identity/repo, baseline Load Flow, electrical distance,
  2 papers summarized, Volt-VAr Control (~3 weeks ahead of plan)
- Weakness: daily language practice never started
- Week 2 plan: fix CSV bug + complete comparison, write docs/methodology.md,
  start language for real (even 10-15 min/day)
- Next review: Friday, 2 Oct 2026, 8:00 PM

## Week 2 (26 Sep – 2 Oct 2026)
- Evaluation: Again much better than expected; the work of weeks 2-7 of the
  original plan was done in two weeks
- Done: CSV bug fixed, baseline hosting capacity + electrical distance,
  finding "the transformer is a shared bottleneck", Volt-VAr (voltage +
  thermal limits), Volt-Watt (numerical oscillation fixed with damping),
  full three-way comparison, docs/methodology.md complete,
  docs/paper-draft.md started (Introduction + Methodology)
- Weakness: language still not started (followed up by Sattar separately)
- Warning: this pace is not sustainable. From now on the focus moves from
  producing new results to consolidating and finishing the paper
- Week 3 plan: complete Discussion / Conclusion / Abstract in the paper
  draft, review the whole draft, start language for real,
  (optional) look at EV or time-series analysis
- Next review: Friday, 9 Oct 2026, 8:00 PM (held earlier, 9 Oct, 2:30 PM)

## Week 3 (3–9 Oct 2026)
- Evaluation (Sattar): "I don't know"
- Load on energy and family time: light
- Done: paper draft complete and rewritten around the final results (the
  claim that Volt-Watt is better was dropped); 7-scenario sensitivity study
  on the rural and urban feeders (53 buses); scripts 10 and 10b (direct
  measurement of why Volt-VAr can lower hosting capacity, on both feeders);
  figures, README, methodology with decision log, summary of 5 papers,
  references, defense sheet, PhD target-group note; line-by-line lessons on
  the scripts started
- Weakness: language not started until the night of 9 Oct; Sattar's own
  reading of the paper and the defense sheet is behind
- Week 4 plan: see below
- Next review: Friday, 16 Oct 2026, 8:00 PM

## Week 4 (10–16 Oct 2026)
- Evaluation (Sattar): much better than expected
- Load on energy and family time: light
- Done: central question set (when does default Volt-VAr help or hurt hosting
  capacity, and can a simple indicator predict it); six-network snapshot study
  (113 buses, script 11) with a tested hypothesis (Volt-VAr never higher where
  the thermal limit binds first, 0 of 89; higher at 21 of 24 voltage-first
  buses) and a screening indicator r = hc_t / hc_v; time-series study on three
  feeders (script 12) with annual energy, curtailment, violation hours and
  losses; binding-step conditions (script 12b); figures 4 to 6 (script 13);
  paper rewritten around the central question; README, methodology and
  progress log synced
- Weakness: Volt-VAr over the year is not tested; Sattar's own reading of the
  new paper and the oral drill of the defense questions are still ahead;
  language practice to be reviewed separately
- Week 5 plan: Volt-VAr over the year at the same feeders, to test the
  indicator r and the gain and penalty split with profiles; update the paper
  with the result or the limitation. Reading, oral drill and language stay
  with Sattar
- Next review: Friday, 23 Oct 2026, 8:00 PM

## Week 5 review (17–23 Oct 2026)
- Evaluation (Sattar): [to fill]
- Load on energy and family time: [to fill]
- Done: rural1 energy check (matches Table 12, bus 4); two methodology lines added; check_* files removed; Section 2.1 net-flow labels corrected; Section 2.7 answers drafted; script 14 (Volt-VAr over the year, hourly, 8,784 h per case) ran on all three feeders with 0 failed power flows (runtime: rural1 70 min, semiurb5 106 min, urban6 141 min)
- Result: Volt-VAr removes almost all voltage-violation hours at snapshot and 1.5x capacity. Exception: semiurb5 at 1.5x (285.6 kW) still has 118 h above 1.05 pu. No thermal violations. Volt-VAr increases losses in all cases.
- Weakness: indicator r not yet tested on the annual results; paper not yet updated with the annual result; quarter-hour run not done
- Week 6 plan: test indicator r on the annual results; update the paper with the annual result or its limitation (semiurb5 at 1.5x); quarter-hour run (optional); reading, oral drill and language stay with Sattar
- Next review: Friday, 30 Oct 2026, 8:00 PM

## Week 6

Goal: Volt-VAr over the year at the far buses (time-series capacity), checked against the snapshot indicator r.

Done:
- Script 15 (Volt-VAr time-series capacity, far buses): rural1 106.5 -> 165.1 kW (+55.0%), semiurb5 110.5 -> 174.1 kW (+57.6%), urban6 224.7 -> 390.8 kW (+73.9%). Every daylight step verified, 0 unresolved violations, 0 non-converged power flows at or below capacity.
- Script 16: the Volt-VAr code reproduces the script 11 snapshot values at all three buses (match: True).
- Script 17: the year's highest PV is 58% of the snapshot PV at all three feeders, and the stored loads are 1.08 to 2.37 times the year's peak load.
- Script 14 losses checked against results/vvar_annual_hour_summary.md: Volt-VAr adds 16.2% to 29.0% losses in all nine cases.
- Paper updated (abstract, contributions, Sections 2.7, 3.9, discussion, limitations, conclusion), committed and pushed.

Finding:
- The snapshot indicator r did not predict the year-based sign at two of three far buses: urban6 (r = 0.885, no gain expected) gained 73.9% over the year, and rural1 (snapshot effect -1.5%) gained 55.0%. The indicator holds for the snapshot only.

Decision:
- The snapshot result stays in the paper as the main result. The year result is reported as a limitation of the indicator.

Weakness:
- Year-based Volt-VAr was run only at the far bus of each feeder, not at the other buses.
- The snapshot-to-year explanation (PV peaks at about 58% of nameplate) fits the data but is not a formal decomposition.

Week 7 plan: close the project checklist. Make README, methodology, progress log and weekly reviews consistent with the paper, check table and figure numbers, and commit everything.

Week 8 plan: build the defense sheet from the final paper.

Next review: Friday 6 Nov 2026, 20:00.