"""Script 18: out-of-sample test of the screening indicator r (Study 2a).

Why
  The indicator r = hc_t / hc_v and its thresholds (1.00 and 1.05) were derived
  from scenario 0 of the six SimBench 1-LV grids (script 11, 113 buses), and the
  same grids and scenario were used to test the rule. This script tests the same
  rules on scenarios 1 and 2 of the same six grids. These are other operating
  points (other PV and load data), not other networks. Nothing is refitted: the
  rules and thresholds stay as they are.

Why not new networks
  SimBench 1-LV has only six grids (rural1, rural2, rural3, semiurb4, semiurb5,
  urban6), and all six are used in scripts 11 to 17. A test on new networks would
  need LV subnets taken from the SimBench MV grids. That is a separate step.

Pre-registered predictions (registered 21 Oct 2026, before any run of this design)
  P1. Thermal first (r < 1): Volt-VAr is never higher than no control.
  P2. r >= 1.05: Volt-VAr is higher at every bus where the voltage limit binds
      first (hc_v < hc_t).
  P3. Dead band (voltage at the no-control capacity <= 1.02 pu): Volt-VAr is
      unchanged (equal).
  P4. hc_nc = min(hc_v, hc_t) and hc_vvar = min(hc_v_vvar, hc_t_vvar) within
      0.2 kW at every bus.
  The 1.00-1.05 band is expected to be mixed, as in the training sample.
  If a prediction fails, the failure is reported as it is.
  An earlier list of five other networks (rural4, semiurb1, semiurb3, urban2,
  urban4) was replaced on 21 Oct 2026 because those grids do not exist in
  SimBench. That run never started, so no result was seen.

Networks (the six 1-LV grids, scenarios 1 and 2; codes such as 1-LV-rural1--1-sw).
  Scenario 0, used in scripts 11 to 17, is not run here.
  Buses: as in script 11 (--per-grid 20).

Limit of this test
  It is out-of-sample only in operating points. The networks, and the bus
  choice rule, are the same as in the training sample. A pass does not show that
  the indicator holds on other networks.

Method
  The same functions as script 11 are used. script 11 is imported and called with
  the six grids and scenarios 1 and 2. Nothing in script 11 is changed.

Run from the repository root (about 20 to 50 min with --workers 3):
  python scripts\18_heldout_indicator.py --workers 3
Outputs: results/heldout_snapshot.csv and results/heldout_summary.md
Send back: results/heldout_summary.md
"""
import importlib.util
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))

GRIDS = ["rural1", "rural2", "rural3", "semiurb4", "semiurb5", "urban6"]
SCENARIOS = ["1", "2"]


def _load(name, file):
    spec = importlib.util.spec_from_file_location(name, os.path.join(HERE, file))
    mod = importlib.util.module_from_spec(spec)
    sys.modules[name] = mod
    spec.loader.exec_module(mod)
    return mod


s11 = _load("s11", "11_multi_feeder_snapshot.py")


def main():
    extra = sys.argv[1:]                     # e.g. --workers 3
    sys.argv = [sys.argv[0], "--grids", *GRIDS, "--scenarios", *SCENARIOS,
                "--out", "heldout", *extra]
    s11.main()


if __name__ == "__main__":
    main()