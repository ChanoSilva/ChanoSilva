#!/usr/bin/env python3
"""HQF001 v0.3 (R2-M3): post hoc scan of the covariance spectra that synth-classcov could have used.

For spectra geomspace(2, lam, 6) (and the v0.1 spectrum) the script computes the Monte-Carlo Bayes error
of the two rotated Gaussians at the lower end (0.05) of the mean-shift search interval, with the same
rotations and mean direction as selective_benchmark.make_datasets (same RNG consumption). The 10 %
calibration has an interior solution iff that error exceeds 10 %. No classifier is run. The four candidate
spectra actually tried in round 1 were not recorded; this scan documents the family a posteriori.
Writes results/results_spectrum.json."""
import json
import os
import sys
import time

import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
sys.path.insert(0, HERE)
import selective_benchmark as sb  # noqa: E402


def rng_before_synth_classcov():
    """Generator state of make_datasets right before synth-classcov (moons noise and nuisance draws consumed)."""
    rng = np.random.default_rng(sb.SEED)
    n = 1200
    th = np.deg2rad(30.0)
    R = np.array([[np.cos(th), -np.sin(th)], [np.sin(th), np.cos(th)]])
    rng.multivariate_normal(np.zeros(2), R @ np.diag([0.30 ** 2, 0.06 ** 2]) @ R.T, n)
    rng.standard_normal((n, 3))
    return rng


def main():
    t0 = time.process_time()
    spectra = [("v0.1", [2, 1, 0.5, 0.25, 0.1, 0.05])] + [(f"geom_{lam}", np.geomspace(2, lam, 6).tolist())
                                                        for lam in [0.05, 0.1, 0.15, 0.2, 0.25, 0.3]]
    rows = []
    for name, eig in spectra:
        rng = rng_before_synth_classcov()
        d = 6
        Q0, Q1 = sb._rand_rot(rng, d), sb._rand_rot(rng, d)
        covs = [Q0 @ np.diag(eig) @ Q0.T, Q1 @ np.diag(eig) @ Q1.T]
        u = rng.standard_normal(d)
        u /= np.linalg.norm(u)
        dirs = np.vstack([np.zeros(d), u])
        e = sb._gauss_bayes_error(np.random.default_rng(1), dirs * 0.05, covs, np.array([0.5, 0.5]))
        rows.append(dict(name=name, eigenvalues=[float(v) for v in eig], lam_min=float(min(eig)),
                         bayes_error_at_lower_bound=float(e), interior_solution=bool(e > 0.10)))
        print(f"{name:8s} lam_min={min(eig):.3f} Bayes error at shift 0.05: {100 * e:.1f}% interior solution: {e > 0.10}")
    out = dict(meta=dict(seed=sb.SEED, cpu_seconds=time.process_time() - t0, chosen="geom_0.25",
                         note="post hoc; the four candidates tried in round 1 were not recorded"), spectra=rows)
    with open(os.path.join(ROOT, "results", "results_spectrum.json"), "w") as fh:
        json.dump(out, fh, indent=1)


if __name__ == "__main__":
    main()
