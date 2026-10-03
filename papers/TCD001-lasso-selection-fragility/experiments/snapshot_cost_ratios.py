#!/usr/bin/env python3
"""
Archive the wall-clock cost ratios (heuristic time / exhaustive-search time) of the current
results/fragility.json (E3) and results/scaling.json (E4) into results/cost_ratios_previous_run.json,
so that make_numbers.py can report how much these ratios change between two complete reference runs
of the same code with the same seeds (round-2 finding M2(v): they depend on machine load).

Usage: python3 snapshot_cost_ratios.py "<label of the run being archived>"
Run it BEFORE re-running the experiments; it does not recompute anything.
"""
import json
import os
import sys

import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
RES = os.path.join(os.path.dirname(HERE), "results")


def main():
    label = sys.argv[1] if len(sys.argv) > 1 else "previous run"
    fra = json.load(open(os.path.join(RES, "fragility.json")))
    sca = json.load(open(os.path.join(RES, "scaling.json")))
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
    with open(os.path.join(RES, "cost_ratios_previous_run.json"), "w") as fh:
        json.dump(out, fh, indent=1)
    print(f"archived {len(e3)} E3 and {len(e4)} E4 cost ratios ({label})")


if __name__ == "__main__":
    main()
