#!/usr/bin/env python3
"""Coverage of the percentile bootstrap interval used by run_comparison.bootstrap_ci
(95 %, B = 2000 resamples of the per-fold paired differences) when the n per-fold
differences are i.i.d. normal with mean zero -- the most favourable case, since outer
cross-validation folds are in fact positively dependent (Nadeau and Bengio 2003).

Added in the second round of internal review (03/10/2026, referee 2, finding M4): the
"expected by chance" counts of the manuscript were two-sided (0.05 N) and compared with
one-sided counts, and assumed nominal coverage.  This script estimates, for n = 10 (main
condition) and n = 5 (robustness conditions), the probability that the interval lies
entirely above zero under no true difference, and the binomial tail probabilities of the
observed counts.  It reproduces the referee's own check (scratchpad coverage.py: 85.0 %
for n = 5, 89.9 % for n = 10 with B = 1000) with the protocol's B = 2000.

Writes results/bootstrap_coverage.json.  About 15 s on one core.  Both tails are averaged (the null is symmetric)."""
import json
import os
import time

import numpy as np
from scipy.stats import binom

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
SEED = 20261003
R, B, CHUNK = 20000, 2000, 200


def simulate(n, rng):
    lo_all, hi_all = [], []
    for _ in range(R // CHUNK):
        x = rng.standard_normal((CHUNK, n))
        idx = rng.integers(0, n, size=(CHUNK, B, n))
        means = np.take_along_axis(np.broadcast_to(x[:, None, :], (CHUNK, B, n)), idx, axis=2).mean(axis=2)
        lo_all.append(np.percentile(means, 2.5, axis=1))
        hi_all.append(np.percentile(means, 97.5, axis=1))
    lo, hi = np.concatenate(lo_all), np.concatenate(hi_all)
    return {"n": n, "replications": R, "B": B,
            "coverage": float(np.mean((lo <= 0) & (hi >= 0))),
            "p_above": float(np.mean(lo > 0)), "p_below": float(np.mean(hi < 0)),
            # by the symmetry of N(0, 1) both tails have the same probability; average them
            "p_one_sided": float(0.5 * (np.mean(lo > 0) + np.mean(hi < 0)))}


def main():
    t0 = time.time()
    rng = np.random.default_rng(SEED)
    out = {"meta": {"seed": SEED, "what": "percentile bootstrap 95% CI of a mean of n i.i.d. N(0,1) fold differences"},
           "sim": {str(n): simulate(n, rng) for n in (10, 5)}}
    res = json.load(open(os.path.join(ROOT, "results", "results.json")))
    names, local = list(res["results"].keys()), res["meta"]["local"]
    n_main = len(names) * len(local)
    n_rob = 2 * n_main
    pos_main = sum(res["results"][d]["main"]["summary"][m]["sig"] == "pos" for d in names for m in local)
    pos_rob = sum(res["results"][d][c]["summary"][m]["sig"] == "pos" for c in ("noise20", "sub25") for d in names for m in local)
    p10, p5 = out["sim"]["10"]["p_one_sided"], out["sim"]["5"]["p_one_sided"]
    out["counts"] = {
        "n_main": n_main, "n_robust": n_rob, "pos_main": pos_main, "pos_robust": pos_rob,
        "expected_above_main_nominal": 0.025 * n_main, "expected_above_robust_nominal": 0.025 * n_rob,
        "expected_above_main_sim": p10 * n_main, "expected_above_robust_sim": p5 * n_rob,
        "p_at_least_obs_main_nominal": float(binom.sf(pos_main - 1, n_main, 0.025)),
        "p_at_least_obs_main_sim": float(binom.sf(pos_main - 1, n_main, p10)),
        "p_at_least_obs_robust_nominal": float(binom.sf(pos_rob - 1, n_rob, 0.025)),
        "p_at_least_obs_robust_sim": float(binom.sf(pos_rob - 1, n_rob, p5)),
    }
    out["meta"]["seconds"] = time.time() - t0
    with open(os.path.join(ROOT, "results", "bootstrap_coverage.json"), "w") as fh:
        json.dump(out, fh, indent=1)
    print(json.dumps(out, indent=1))


if __name__ == "__main__":
    main()
