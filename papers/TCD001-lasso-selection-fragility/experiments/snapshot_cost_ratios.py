#!/usr/bin/env python3
"""
Archive the wall-clock cost ratios (heuristic time / exhaustive-search time) of a complete run
(fragility.json for E3, scaling.json for E4) into results/cost_ratios_run_<tag>.json, so that
make_numbers.py can report how much these ratios change between complete runs of the same code with
the same seeds on the same shared machine (round-2 finding M2(v): they depend on machine load).

Usage: python3 snapshot_cost_ratios.py <tag> "<label>" [<directory with fragility.json and scaling.json>]
The directory defaults to results/.  To archive the current reference run, call it BEFORE re-running
the experiments; it does not recompute anything.  Archived in v0.3:
  cost_ratios_run_v02.json      the v0.2 reference run (03/10/2026 04:08-04:09 UTC);
  cost_ratios_run_referee.json  the complete repetition made by the round-2 internal referee
                                (03/10/2026 09:46-09:48 UTC; same code plus a fit counter, same seeds).
The current run (results/*.json) is the third.
"""
import json
import os
import sys

import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
RES = os.path.join(os.path.dirname(HERE), "results")


def main():
    tag, label = sys.argv[1], sys.argv[2]
    src = sys.argv[3] if len(sys.argv) > 3 else RES
    fra = json.load(open(os.path.join(src, "fragility.json")))
    sca = json.load(open(os.path.join(src, "scaling.json")))
    e3 = {k: v["median_cost_ratio"] for k, v in fra["verdict"].items()}
    e4 = {}
    for a in sca["exact"]:
        e4[f"{a['family']}_{a['n']}_onestep"] = a["cost_ratio_onestep_median"]
        e4[f"{a['family']}_{a['n']}_amip"] = a["cost_ratio_amip_median"]
    for fam in sca["meta"]["families"]:
        big = [r for r in sca["records_exact"] if r["family"] == fam and r["n"] >= 22 and r["t_C"] > 0]
        e4[f"{fam}_ge22_all_onestep"] = float(np.median([r["t_onestep_C"] / r["t_C"] for r in big]))
    out = dict(label=label, source_seconds=dict(fragility=fra["meta"]["seconds"], scaling=sca["meta"]["seconds"]),
               e3_median_cost_ratio=e3, e4_median_cost_ratio=e4)
    with open(os.path.join(RES, f"cost_ratios_run_{tag}.json"), "w") as fh:
        json.dump(out, fh, indent=1)
    print(f"archived {len(e3)} E3 and {len(e4)} E4 cost ratios ({label})")


if __name__ == "__main__":
    main()
