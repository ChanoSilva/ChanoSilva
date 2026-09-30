#!/usr/bin/env python3
"""
E2c: direct measurements of the ordinal kernel class (the set of configurations
with the same ranking of pairwise distances as a given X), complementing the
solver-based reconstruction of E2.

  (a) Inradius.  Let g(X) be the minimal gap between consecutive sorted
      pairwise distances.  Moving every point by at most eps changes every
      distance by at most 2 eps and every difference of distances by at most
      4 eps, so eps < g/4 keeps the ranking; when the two pairs realising g are
      disjoint, displacing their four endpoints by g/4 along the pair
      directions closes the gap.  The script checks both statements
      numerically and records the distribution of g(X) against n.
  (b) Anisotropy.  A random walk constrained to the class (proposals are
      accepted iff the ranking is unchanged) records the farthest member
      found, measured by the similarity-invariant Procrustes disparity from
      X.  This is a lower bound on the class radius at X in that metric.

Usage:   python3 ordinal_class.py [--fast]
Outputs: ../results/results_class.json, ../results/tables_class.md,
         ../figures/ordinal_class.{png,pdf}
"""
import argparse
import json
import os
import platform
import sys
import time

import numpy as np
import scipy
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from scipy.spatial import procrustes
from scipy.spatial.distance import pdist

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
RESULTS = os.path.join(ROOT, "results")
FIGURES = os.path.join(ROOT, "figures")
MASTER_SEED = 20260930


def pattern(X):
    return np.argsort(pdist(X), kind="stable")


def min_gap(X):
    """minimal gap between consecutive sorted distances, the two pairs
    realising it, and whether those pairs are disjoint"""
    n = len(X)
    iu = np.triu_indices(n, 1)
    dv = pdist(X)
    order = np.argsort(dv, kind="stable")
    sd = dv[order]
    gaps = np.diff(sd)
    k = int(np.argmin(gaps))
    p_small = (int(iu[0][order[k]]), int(iu[1][order[k]]))
    p_large = (int(iu[0][order[k + 1]]), int(iu[1][order[k + 1]]))
    disjoint = len(set(p_small) | set(p_large)) == 4
    return float(gaps[k]), p_small, p_large, disjoint


def check_inradius(X, rng, trials=20):
    """(i) random Euclidean perturbations of every point below g/4 keep the pattern;
    (ii) for disjoint extremal pairs, the explicit displacement by g/4 (times
    1 + 1e-6) along the pair directions changes it."""
    g, ps, pl, disjoint = min_gap(X)
    P = pattern(X)
    eps = 0.999 * g / 4
    kept = 0
    n, d = X.shape
    for _ in range(trials):
        # displacement of every point by a vector of Euclidean norm < eps,
        # uniform in the ball (direction uniform on the sphere, radius eps*U^(1/d))
        direc = rng.standard_normal((n, d))
        direc /= np.linalg.norm(direc, axis=1, keepdims=True)
        radius = eps * rng.random(n) ** (1.0 / d)
        step = direc * radius[:, None]
        kept += int(np.array_equal(pattern(X + step), P))
    changed = None
    if disjoint:
        Y = X.copy()
        # overshoot g/4 by a margin safely above double-precision rounding of
        # distances of order one (relative 1e-6, or absolute 1e-12 if larger)
        e = g / 4 + max(1e-6 * g / 4, 1e-12)
        a, b = ps                                             # grow the smaller distance
        u = (X[b] - X[a]) / np.linalg.norm(X[b] - X[a])
        Y[a] -= e * u
        Y[b] += e * u
        c, d = pl                                             # shrink the larger one
        w = (X[d] - X[c]) / np.linalg.norm(X[d] - X[c])
        Y[c] += e * w
        Y[d] -= e * w
        changed = not np.array_equal(pattern(Y), P)
    return {"gap": g, "disjoint": disjoint, "kept": kept, "trials": trials, "changed": changed}


def class_walk(X, rng, steps):
    """random walk inside the ordinal class of X; returns the largest
    Procrustes disparity from X among visited configurations and the
    acceptance rate"""
    P = pattern(X)
    Y = X.copy()
    sigma = 1e-3
    best = 0.0
    accepted = 0
    for t in range(steps):
        prop = Y + sigma * rng.standard_normal(X.shape)
        if np.array_equal(pattern(prop), P):
            Y = prop
            accepted += 1
            d = procrustes(X, Y)[2]
            if d > best:
                best = float(d)
            sigma *= 1.05                                     # adapt towards ~30% acceptance
        else:
            sigma *= 0.98
    return best, accepted / steps


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--fast", action="store_true")
    args = ap.parse_args()
    rng = np.random.default_rng(MASTER_SEED + 2)
    os.makedirs(RESULTS, exist_ok=True)
    os.makedirs(FIGURES, exist_ok=True)
    plan = ([(8, 10, 2000), (16, 10, 2000), (32, 10, 1500), (64, 6, 1000)] if args.fast else
            [(8, 20, 8000), (16, 20, 8000), (32, 20, 6000), (64, 20, 4000), (128, 20, 3000), (256, 12, 1500)])
    d = 2
    rows, raw = [], {}
    t_all = time.time()
    for n, reps, steps in plan:
        gaps, disj, kept_all, changed_all, radii, acc = [], 0, 0, [0, 0], [], []
        t0 = time.time()
        for _ in range(reps):
            X = rng.random((n, d))
            chk = check_inradius(X, rng)
            gaps.append(chk["gap"])
            disj += int(chk["disjoint"])
            kept_all += chk["kept"]
            if chk["changed"] is not None:
                changed_all[0] += int(chk["changed"]); changed_all[1] += 1
            r, a = class_walk(X, rng, steps)
            radii.append(r); acc.append(a)
        gaps, radii = np.array(gaps), np.array(radii)
        raw[n] = {"gaps": gaps.tolist(), "radii": radii.tolist()}
        rows.append({"n": n, "configurations": reps, "walk_steps": steps,
                     "gap_median": float(np.median(gaps)), "gap_q1": float(np.percentile(gaps, 25)),
                     "gap_q3": float(np.percentile(gaps, 75)),
                     "disjoint_extremal_pairs": disj,
                     "perturbations_below_quarter_gap_kept": kept_all,
                     "perturbations_total": reps * 20,
                     "quarter_gap_displacement_changed": changed_all[0],
                     "quarter_gap_displacement_tested": changed_all[1],
                     "walk_radius_median": float(np.median(radii)),
                     "walk_radius_q1": float(np.percentile(radii, 25)),
                     "walk_radius_q3": float(np.percentile(radii, 75)),
                     "walk_acceptance_mean": float(np.mean(acc)),
                     "seconds": round(time.time() - t0, 1)})
        print(f"  n={n:4d} gap median {np.median(gaps):.2e}  walk radius median {np.median(radii):.2e}  "
              f"kept {kept_all}/{reps*20}  changed {changed_all[0]}/{changed_all[1]}", file=sys.stderr)
    # log-log slopes
    ns = np.array([r["n"] for r in rows], dtype=float)
    slope_gap = float(np.polyfit(np.log(ns), np.log([r["gap_median"] for r in rows]), 1)[0])
    slope_rad = float(np.polyfit(np.log(ns), np.log([r["walk_radius_median"] for r in rows]), 1)[0])
    res = {"meta": {"seed": MASTER_SEED + 2, "fast": args.fast, "python": platform.python_version(),
                    "numpy": np.__version__, "scipy": scipy.__version__,
                    "seconds": round(time.time() - t_all, 1)},
           "rows": rows, "raw": raw, "slope_gap": slope_gap, "slope_walk_radius": slope_rad}
    with open(os.path.join(RESULTS, "results_class.json"), "w") as fh:
        json.dump(res, fh, indent=2)
    # figure
    fig, ax = plt.subplots(figsize=(4.8, 3.2), dpi=150)
    ax.plot(ns, [r["gap_median"] for r in rows], "o-", color="#08519c", label=f"minimal gap $g$ (slope {slope_gap:.1f})")
    ax.fill_between(ns, [r["gap_q1"] for r in rows], [r["gap_q3"] for r in rows], color="#9ecae1", alpha=0.6)
    ax.plot(ns, [r["walk_radius_median"] for r in rows], "s--", color="#a63603", label=f"walk radius (slope {slope_rad:.1f})")
    ax.fill_between(ns, [r["walk_radius_q1"] for r in rows], [r["walk_radius_q3"] for r in rows], color="#fdae6b", alpha=0.6)
    ax.set_xscale("log", base=2); ax.set_yscale("log")
    ax.set_xlabel("sample size $n$"); ax.set_title("E2c: size of the ordinal class", fontsize=10)
    ax.grid(True, which="both", lw=0.3, alpha=0.5); ax.legend(frameon=False, fontsize=8)
    fig.tight_layout()
    fig.savefig(os.path.join(FIGURES, "ordinal_class.png")); fig.savefig(os.path.join(FIGURES, "ordinal_class.pdf"))
    plt.close(fig)
    # tables
    L = ["# E2c tables (generated by experiments/ordinal_class.py)\n",
         f"seed = {MASTER_SEED + 2}; fast = {args.fast}; runtime = {res['meta']['seconds']} s\n",
         f"log-log slope of median gap vs n: {slope_gap:.2f}; of median walk radius vs n: {slope_rad:.2f}\n",
         "| n | configs | median gap g | Q1 | Q3 | disjoint pairs | kept below g/4 | changed at g/4 | walk steps | median walk radius | Q1 | Q3 | acceptance |",
         "|---|---|---|---|---|---|---|---|---|---|---|---|---|"]
    for r in rows:
        L.append(f"| {r['n']} | {r['configurations']} | {r['gap_median']:.2e} | {r['gap_q1']:.2e} | {r['gap_q3']:.2e} | "
                 f"{r['disjoint_extremal_pairs']}/{r['configurations']} | {r['perturbations_below_quarter_gap_kept']}/{r['perturbations_total']} | "
                 f"{r['quarter_gap_displacement_changed']}/{r['quarter_gap_displacement_tested']} | {r['walk_steps']} | "
                 f"{r['walk_radius_median']:.2e} | {r['walk_radius_q1']:.2e} | {r['walk_radius_q3']:.2e} | {r['walk_acceptance_mean']:.2f} |")
    with open(os.path.join(RESULTS, "tables_class.md"), "w") as fh:
        fh.write("\n".join(L) + "\n")
    print(f"done in {res['meta']['seconds']} s", file=sys.stderr)


if __name__ == "__main__":
    main()
