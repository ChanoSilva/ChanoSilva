#!/usr/bin/env python3
"""
Formalism-chain experiments for the MRT001 draft
"Foundational Geometry: invariants across formalisms and structures
preceding a geometric description".

Finite Euclidean configurations are studied through four formalisms linked
by translations

    coordinates --> metric (distance matrix) --> ordinal (ranking of the
    pairwise distances) --> relational (Tarski betweenness and congruence)

and the experiments measure, on random instances, what each translation keeps
and what it destroys.  Every number quoted in the manuscript is produced here.

Experiments
  E1  Generic triviality of the relational primitives on finite samples
      (exact integer arithmetic).
  E2  Recovery of the configuration up to similarity from ordinal data only,
      as a function of the sample size n (non-metric MDS + Procrustes).
  E2b Invariance check: a monotone distortion of the metric changes the
      metric-MDS reconstruction but not the ordinal one.
  E3  Finite non-uniqueness of the ordinal formalism: explicit examples, and
      the number of distinct ordinal patterns realised by four points in
      dimensions 1, 2 and 3.
  E4  Formalism depth of standard geometric quantities: which quantities
      survive rigid motions, similarities and monotone distortions.

Usage:   python3 formalism_chain.py [--fast]
Outputs: ../results/results.json, ../results/tables.md,
         ../figures/ordinal_recovery.{png,pdf}
"""
import argparse
import itertools
import json
import os
import platform
import sys
import time
import warnings
from collections import Counter

import numpy as np
import scipy
import sklearn
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from scipy.sparse.csgraph import minimum_spanning_tree
from scipy.spatial import procrustes
from scipy.spatial.distance import pdist, squareform
from sklearn.manifold import MDS

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
RESULTS = os.path.join(ROOT, "results")
FIGURES = os.path.join(ROOT, "figures")
os.makedirs(RESULTS, exist_ok=True)
os.makedirs(FIGURES, exist_ok=True)

MASTER_SEED = 20260930
GRID = 2 ** 30          # integer coordinate range for exact relational tests


# --------------------------------------------------------------------------
# Translations between formalisms
# --------------------------------------------------------------------------
def tau_metric(X):
    """coordinates -> distance matrix"""
    return squareform(pdist(X))


def tau_ordinal(D):
    """metric -> ordinal pattern.

    Returns (rank_matrix, pattern).  rank_matrix has zero diagonal and the
    rank (1..m) of every off-diagonal distance; pattern is the tuple of pair
    indices sorted by increasing distance, i.e. the total order on pairs.
    """
    n = D.shape[0]
    iu = np.triu_indices(n, 1)
    vals = D[iu]
    order = np.argsort(vals, kind="stable")
    ranks = np.empty_like(order)
    ranks[order] = np.arange(1, len(vals) + 1)
    R = np.zeros_like(D)
    R[iu] = ranks
    R = R + R.T
    return R, tuple(order.tolist())


def tau_relational_exact(P):
    """metric -> Tarski primitives restricted to the sample, computed exactly.

    P holds integer coordinates (shape (n, d), entries below 2**30, d <= 3),
    so squared distances and 2x2 minors fit in int64 without overflow.

    Betweenness  B(a,b,c):  b lies strictly between a and c on a line
                            (equivalently d(a,b) + d(b,c) = d(a,c) with
                            a, b, c distinct).
    Congruence   ab == cd:  d(a,b) = d(c,d) for distinct unordered pairs.

    Returns (number of unordered triples {a,c} with some b strictly between
    them, number of unordered pairs of distinct point-pairs at equal distance).
    """
    P = np.asarray(P, dtype=np.int64)
    n, d = P.shape
    diff = P[:, None, :] - P[None, :, :]               # diff[i,j] = P[i]-P[j]
    D2 = (diff ** 2).sum(-1)
    vals = D2[np.triu_indices(n, 1)]
    _, counts = np.unique(vals, return_counts=True)
    congruent = int((counts * (counts - 1) // 2).sum())
    # A[a,b,c] = P[a]-P[b],  C[a,b,c] = P[c]-P[b]
    A = diff[:, :, None, :]
    C = diff.transpose(1, 0, 2)[None, :, :, :]
    coll = np.ones((n, n, n), dtype=bool)                # all 2x2 minors vanish
    for i in range(d):
        for j in range(i + 1, d):
            minor = A[..., i] * C[..., j] - A[..., j] * C[..., i]
            coll &= (minor == 0)
    dot = (A * C).sum(-1)                                # < 0 iff b strictly between
    idx = np.arange(n)
    distinct_ac = np.ones((n, n, n), dtype=bool)
    distinct_ac[idx, :, idx] = False                     # exclude a == c
    between = int(np.count_nonzero(coll & (dot < 0) & distinct_ac)) // 2
    return between, congruent


# --------------------------------------------------------------------------
# Helpers
# --------------------------------------------------------------------------
def random_config(rng, n, d):
    """uniform sample in the unit cube (a bounded connected open set)"""
    return rng.random((n, d))


def random_rigid(rng, d):
    A = rng.standard_normal((d, d))
    Q, _ = np.linalg.qr(A)
    if rng.random() < 0.5:                      # allow reflections
        Q[:, 0] = -Q[:, 0]
    t = rng.standard_normal(d) * 5.0
    return Q, t


def _mds(nonmetric, d, seed, n_init):
    return MDS(n_components=d, metric_mds=not nonmetric, metric="precomputed",
               init="random", n_init=n_init, max_iter=2000, eps=1e-9,
               random_state=seed, n_jobs=1, normalized_stress="auto")


def nonmetric_embedding(R, d, rng, n_init=4):
    """ordinal -> coordinates (non-metric MDS on the rank matrix)"""
    return _mds(True, d, int(rng.integers(0, 2**31 - 1)), n_init).fit_transform(R)


def metric_embedding(D, d, rng, n_init=4):
    return _mds(False, d, int(rng.integers(0, 2**31 - 1)), n_init).fit_transform(D)


def affine_dimension(D, tol=1e-6):
    """rank of the Gram matrix obtained by double centring (classical MDS)"""
    n = D.shape[0]
    J = np.eye(n) - np.ones((n, n)) / n
    G = -0.5 * J @ (D ** 2) @ J
    w = np.linalg.eigvalsh(G)
    w = w / max(abs(w).max(), 1e-300)
    return int(np.count_nonzero(w > tol))


def knn_graph(D, k):
    n = D.shape[0]
    edges = set()
    for i in range(n):
        order = np.argsort(D[i], kind="stable")
        for j in order[1:k + 1]:
            edges.add((i, int(j)))
    return frozenset(edges)


def mst_edges(D):
    T = minimum_spanning_tree(D).tocoo()
    return frozenset(tuple(sorted((int(i), int(j)))) for i, j in zip(T.row, T.col))


def rng_graph(D):
    """relative neighbourhood graph: ij is an edge iff no k has
    max(d(i,k), d(j,k)) < d(i,j)  (comparisons only)"""
    n = D.shape[0]
    edges = set()
    for i in range(n):
        for j in range(i + 1, n):
            m = np.maximum(D[i], D[j])
            m[[i, j]] = np.inf
            if not np.any(m < D[i, j]):
                edges.add((i, j))
    return frozenset(edges)


def gabriel_graph(D):
    """Gabriel graph: ij is an edge iff no k has d(i,k)^2 + d(j,k)^2 < d(i,j)^2
    (an additive, hence metric-level, condition)"""
    n = D.shape[0]
    edges = set()
    for i in range(n):
        for j in range(i + 1, n):
            s = D[i] ** 2 + D[j] ** 2
            s[[i, j]] = np.inf
            if not np.any(s < D[i, j] ** 2):
                edges.add((i, j))
    return frozenset(edges)


def diameter_pair(D):
    n = D.shape[0]
    iu = np.triu_indices(n, 1)
    k = int(np.argmax(D[iu]))
    return (int(iu[0][k]), int(iu[1][k]))


# --------------------------------------------------------------------------
# E1  generic triviality of the relational primitives (exact arithmetic)
# --------------------------------------------------------------------------
def experiment_E1(rng, fast):
    N = 200 if fast else 500
    settings = [(n, d) for d in (2, 3) for n in (5, 10, 20, 50)]
    out = []
    for n, d in settings:
        nb = nc = 0
        for _ in range(N):
            P = rng.integers(0, GRID, size=(n, d), dtype=np.int64)
            b, c = tau_relational_exact(P)
            nb += b
            nc += c
        out.append({"n": n, "d": d, "configurations": N,
                    "betweenness_instances": nb, "congruence_instances": nc})
    controls = []                                # integer grids: both relations rich
    for k in (3, 4, 5):
        pts = np.array(list(itertools.product(range(k), repeat=2)), dtype=np.int64)
        b, c = tau_relational_exact(pts)
        controls.append({"grid": f"{k}x{k}", "n": k * k,
                         "betweenness_instances": b, "congruence_instances": c})
    return {"random": out, "controls": controls, "coordinate_range": GRID,
            "arithmetic": "exact int64"}


# --------------------------------------------------------------------------
# E2  ordinal recovery as a function of n
# --------------------------------------------------------------------------
def experiment_E2(rng, fast):
    plan = ([(2, [8, 16, 32, 64, 128], 10), (3, [8, 16, 32, 64], 5)] if fast else
            [(2, [8, 16, 32, 64, 128, 256], 30), (3, [8, 16, 32, 64, 128], 15)])
    rows, raw = [], {}
    for d, sizes, reps in plan:
        for n in sizes:
            disp = []
            t0 = time.time()
            for _ in range(reps):
                X = random_config(rng, n, d)
                R, _ = tau_ordinal(tau_metric(X))
                Y = nonmetric_embedding(R, d, rng)
                disp.append(float(procrustes(X, Y)[2]))
            disp = np.array(disp)
            raw[f"d={d},n={n}"] = disp.tolist()
            rows.append({"d": d, "n": n, "repetitions": reps,
                         "median_disparity": float(np.median(disp)),
                         "q1": float(np.percentile(disp, 25)),
                         "q3": float(np.percentile(disp, 75)),
                         "max": float(disp.max()),
                         "seconds": round(time.time() - t0, 1)})
            print(f"  E2 d={d} n={n:4d}  median disparity {np.median(disp):.3e}  "
                  f"(q1 {np.percentile(disp, 25):.3e}, q3 {np.percentile(disp, 75):.3e})",
                  file=sys.stderr)
    # E2b: invariance under a monotone distortion of the metric (d = 2, n = 64)
    d, n = 2, 64
    reps_b = 10 if fast else 20
    same_ord, d_true, d_dist, d_ord = [], [], [], []
    for _ in range(reps_b):
        X = random_config(rng, n, d)
        D = tau_metric(X)
        p = float(rng.uniform(2.0, 4.0))
        Dp = D ** p                              # monotone distortion, same ranks
        R, pat = tau_ordinal(D)
        Rp, patp = tau_ordinal(Dp)
        same_ord.append(pat == patp)
        seed = int(rng.integers(0, 2**31 - 1))
        Y_true = metric_embedding(D, d, np.random.default_rng(seed))
        Y_dist = metric_embedding(Dp, d, np.random.default_rng(seed))
        Z1 = nonmetric_embedding(R, d, np.random.default_rng(seed))
        Z2 = nonmetric_embedding(Rp, d, np.random.default_rng(seed))
        d_true.append(float(procrustes(X, Y_true)[2]))
        d_dist.append(float(procrustes(X, Y_dist)[2]))
        d_ord.append(float(procrustes(Z1, Z2)[2]))
    e2b = {"n": n, "repetitions": reps_b,
           "ordinal_pattern_preserved_by_distortion": int(sum(same_ord)),
           "metric_mds_on_true_metric_median_disparity_to_X": float(np.median(d_true)),
           "metric_mds_on_distorted_metric_median_disparity_to_X": float(np.median(d_dist)),
           "metric_mds_on_distorted_metric_min_disparity_to_X": float(np.min(d_dist)),
           "nonmetric_mds_true_vs_distorted_median_disparity": float(np.median(d_ord)),
           "nonmetric_mds_true_vs_distorted_max_disparity": float(np.max(d_ord))}
    return {"recovery": rows, "raw": raw, "distortion": e2b}


# --------------------------------------------------------------------------
# E3  finite non-uniqueness of the ordinal formalism
# --------------------------------------------------------------------------
def experiment_E3(rng, fast):
    ex = []
    for pts in ([0.0, 1.0, 3.0], [0.0, 1.0, 2.5]):          # collinear examples
        D = tau_metric(np.array(pts)[:, None])
        _, pat = tau_ordinal(D)
        ex.append({"points": pts, "ordinal_pattern": pat,
                   "distances": sorted(D[np.triu_indices(3, 1)].tolist())})
    tri = []
    for a, b, c in ((3.0, 4.0, 5.0), (3.0, 4.0, 6.0)):        # planar examples
        x = (b * b - a * a + c * c) / (2 * c)                   # A=(0,0), B=(c,0)
        y = np.sqrt(max(b * b - x * x, 0.0))
        X = np.array([[0.0, 0.0], [c, 0.0], [x, y]])
        D = tau_metric(X)
        _, pat = tau_ordinal(D)
        ang = []
        for i, j, k in ((0, 1, 2), (1, 0, 2), (2, 0, 1)):
            cosv = (D[i, j] ** 2 + D[i, k] ** 2 - D[j, k] ** 2) / (2 * D[i, j] * D[i, k])
            ang.append(float(np.degrees(np.arccos(cosv))))
        tri.append({"sides": [a, b, c], "ordinal_pattern": pat, "angles_deg": ang})
    N = 50_000 if fast else 300_000
    counts = {}
    for d in (1, 2, 3):
        seen = Counter()
        for _ in range(N):
            _, pat = tau_ordinal(tau_metric(random_config(rng, 4, d)))
            seen[pat] += 1
        counts[f"d={d}"] = {"samples": N, "distinct_patterns_observed": len(seen),
                            "upper_bound_6_factorial": 720,
                            "least_frequent_pattern_count": min(seen.values())}
    return {"collinear_example": ex, "triangle_example": tri, "n4_patterns": counts}


# --------------------------------------------------------------------------
# E4  formalism depth of geometric quantities
# --------------------------------------------------------------------------
def experiment_E4(rng, fast):
    trials = 100 if fast else 300
    n, d, k = 30, 2, 3
    names = ["centroid", "diameter_value", "affine_dimension", "gabriel_graph",
             "diameter_pair", "knn_graph_k3", "mst_edges", "rng_graph"]
    ok = {t: {q: 0 for q in names} for t in ("rigid", "similarity", "monotone")}

    def quantities(D):
        return {"diameter_value": D.max(),
                "affine_dimension": affine_dimension(D),
                "diameter_pair": diameter_pair(D),
                "knn_graph_k3": knn_graph(D, k),
                "mst_edges": mst_edges(D),
                "rng_graph": rng_graph(D),
                "gabriel_graph": gabriel_graph(D)}

    for _ in range(trials):
        X = random_config(rng, n, d)
        D = tau_metric(X)
        base = quantities(D)
        base["centroid"] = X.mean(0)
        Q, t = random_rigid(rng, d)
        s = float(rng.uniform(0.1, 10.0))
        p = float(rng.uniform(0.3, 3.0))
        Xr = X @ Q.T + t
        variants = {"rigid": (Xr, tau_metric(Xr)),
                    "similarity": (s * Xr, tau_metric(s * Xr)),
                    "monotone": (None, D ** p)}
        for tname, (X2, D2) in variants.items():
            cur = quantities(D2)
            if X2 is not None:
                cur["centroid"] = X2.mean(0)
            for q in names:
                if q not in cur:
                    continue                    # centroid undefined for a bare metric
                a, b = base[q], cur[q]
                if isinstance(a, np.ndarray):
                    same = np.allclose(a, b, rtol=1e-9, atol=1e-9)
                elif isinstance(a, (float, np.floating)):
                    same = abs(a - b) <= 1e-9 * max(1.0, abs(a))
                else:
                    same = (a == b)
                ok[tname][q] += int(same)
    table = []
    for q in names:
        row = {"quantity": q}
        for tname in ("rigid", "similarity", "monotone"):
            row[tname] = None if (q == "centroid" and tname == "monotone") \
                else ok[tname][q] / trials
        table.append(row)
    return {"trials": trials, "n": n, "d": d, "k": k, "table": table}


# --------------------------------------------------------------------------
# Figure and tables
# --------------------------------------------------------------------------
def make_figure(e2):
    rows = e2["recovery"]
    fig, ax = plt.subplots(figsize=(4.8, 3.2), dpi=150)
    colours = {2: ("#08519c", "#9ecae1"), 3: ("#a63603", "#fdae6b")}
    for d in (2, 3):
        sel = [r for r in rows if r["d"] == d]
        if not sel:
            continue
        ns = [r["n"] for r in sel]
        ax.fill_between(ns, [r["q1"] for r in sel], [r["q3"] for r in sel],
                        color=colours[d][1], alpha=0.6)
        ax.plot(ns, [r["median_disparity"] for r in sel], "o-",
                color=colours[d][0], label=f"$d={d}$ (median, IQR)")
    ax.set_xscale("log", base=2)
    ax.set_yscale("log")
    ax.set_xlabel("sample size $n$")
    ax.set_ylabel("Procrustes disparity")
    ax.set_title("Recovery from ordinal data only", fontsize=10)
    ax.grid(True, which="both", lw=0.3, alpha=0.5)
    ax.legend(frameon=False, fontsize=8)
    fig.tight_layout()
    fig.savefig(os.path.join(FIGURES, "ordinal_recovery.png"))
    fig.savefig(os.path.join(FIGURES, "ordinal_recovery.pdf"))
    plt.close(fig)


def write_tables(res):
    L = ["# Result tables (generated by experiments/formalism_chain.py)\n",
         f"seed = {MASTER_SEED}; fast = {res['meta']['fast']}; "
         f"runtime = {res['meta']['seconds']} s\n",
         "\n## E1 Relational primitives on random samples (exact integer arithmetic)\n",
         "| n | d | configurations | betweenness instances | congruence instances |",
         "|---|---|---|---|---|"]
    for r in res["E1"]["random"]:
        L.append(f"| {r['n']} | {r['d']} | {r['configurations']} | "
                 f"{r['betweenness_instances']} | {r['congruence_instances']} |")
    L += ["\nControls (integer grids):\n",
          "| grid | n | betweenness instances | congruence instances |",
          "|---|---|---|---|"]
    for r in res["E1"]["controls"]:
        L.append(f"| {r['grid']} | {r['n']} | {r['betweenness_instances']} | "
                 f"{r['congruence_instances']} |")
    L += ["\n## E2 Ordinal recovery (non-metric MDS on ranks, Procrustes disparity)\n",
          "| d | n | repetitions | median | Q1 | Q3 | max |",
          "|---|---|---|---|---|---|---|"]
    for r in res["E2"]["recovery"]:
        L.append(f"| {r['d']} | {r['n']} | {r['repetitions']} | {r['median_disparity']:.2e} | "
                 f"{r['q1']:.2e} | {r['q3']:.2e} | {r['max']:.2e} |")
    b = res["E2"]["distortion"]
    L.append(f"\n### E2b Monotone distortion (n = {b['n']}, {b['repetitions']} repetitions)\n")
    for k_, v in b.items():
        if k_ not in ("n", "repetitions"):
            L.append(f"- {k_}: {v}")
    L.append("\n## E3 Ordinal non-uniqueness\n")
    for e in res["E3"]["collinear_example"]:
        L.append(f"- points {e['points']}: pattern {e['ordinal_pattern']}, distances {e['distances']}")
    for e in res["E3"]["triangle_example"]:
        L.append(f"- triangle sides {e['sides']}: pattern {e['ordinal_pattern']}, "
                 f"angles {[round(a, 2) for a in e['angles_deg']]}")
    for k_, v in res["E3"]["n4_patterns"].items():
        L.append(f"- n=4, {k_}: {v['distinct_patterns_observed']} distinct ordinal patterns "
                 f"observed in {v['samples']} samples (bound 720); least frequent pattern "
                 f"seen {v['least_frequent_pattern_count']} times")
    L += ["\n## E4 Formalism depth (fraction of trials in which the quantity is preserved)\n",
          "| quantity | rigid motion | similarity | monotone distortion |",
          "|---|---|---|---|"]
    for r in res["E4"]["table"]:
        f = lambda v: "n/a" if v is None else f"{v:.2f}"
        L.append(f"| {r['quantity']} | {f(r['rigid'])} | {f(r['similarity'])} | {f(r['monotone'])} |")
    with open(os.path.join(RESULTS, "tables.md"), "w") as fh:
        fh.write("\n".join(L) + "\n")


def main():
    warnings.filterwarnings("ignore", category=FutureWarning)
    ap = argparse.ArgumentParser()
    ap.add_argument("--fast", action="store_true", help="smaller sample sizes")
    args = ap.parse_args()
    rng = np.random.default_rng(MASTER_SEED)
    t0 = time.time()
    res = {"meta": {"seed": MASTER_SEED, "fast": args.fast,
                    "python": platform.python_version(),
                    "numpy": np.__version__, "scipy": scipy.__version__,
                    "sklearn": sklearn.__version__,
                    "matplotlib": matplotlib.__version__}}
    for name, fn in (("E1", experiment_E1), ("E2", experiment_E2),
                     ("E3", experiment_E3), ("E4", experiment_E4)):
        print(f"{name} ...", file=sys.stderr)
        res[name] = fn(rng, args.fast)
    res["meta"]["seconds"] = round(time.time() - t0, 1)
    with open(os.path.join(RESULTS, "results.json"), "w") as fh:
        json.dump(res, fh, indent=2)
    make_figure(res["E2"])
    write_tables(res)
    print(f"done in {res['meta']['seconds']} s", file=sys.stderr)


if __name__ == "__main__":
    main()
