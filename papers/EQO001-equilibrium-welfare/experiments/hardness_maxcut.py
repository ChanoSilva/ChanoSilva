#!/usr/bin/env python3
"""E6 (v0.3): brute-force check of the MAX-CUT reduction behind Proposition 'hardness'.

Pointed out in the internal review of v0.2 (round 2, M1).  For a graph G = (V, E, w) with
integer weights, n = |V|, and an integer k >= 1, let
    cut(x) = sum_{ij in E} w_ij (x_i + x_j - 2 x_i x_j),   L(x) = sum_i deg_w(i) x_i,
    q(x, y) = cut(x) + y (k - 1/2 - L(x))                    on [0,1]^{n+1},
and consider the game with n + 2 scalar players on [0,1] (0 < eps < 1):
    u_i = -x_i - eps/2 x_i^2 (i <= n),  u_{n+1} = y - eps/2 y^2,  u_{n+2} = z - eps/2 z^2 + q(x, y).
F = eps * v + const is eps-strongly monotone, x* = (0,...,0,1,1) is the unique equilibrium
(dominant strategies) and Lambda_1(x*) is the whole orthant.  The claim proved in the
manuscript is
    e_{n+2} in Lambda(x*)  <=>  maxcut(G) < k  <=>  Lambda(x*) = Lambda_1(x*).
This script checks the claim by brute force, independently of the proof:
  * maxcut(G) by enumeration of the 2^n cuts;
  * Lambda-membership of every unit vector e_j by the exact face enumeration of the box QP
    (welfare_cone.box_qp_max, 3^(n+2) faces) for e_{n+2} and n <= 4 (the other payoffs are
    separable and concave, maximised at a vertex), and for n = 5, 6 by enumeration of the
    2^(n+1) vertices in (x, y) with z = 1 (justified in the manuscript by multilinearity), with a
    face-enumeration cross-check on a random subsample;
  * equilibrium residual, strong monotonicity constant and the linear test for Lambda_1.
Graphs: all labelled graphs with unit weights on n = 3, 4, 5 nodes; for n = 6 a random sample
of labelled graphs with unit weights and a random sample with weights in {1, 2, 3}; every
threshold k = 1, ..., W_total + 1 (W_total = total weight).

Criteria (evaluated by check_criteria(); no external pre-registration):
  * for every (G, k): [e_{n+2} in Lambda] == [maxcut(G) < k] and [Lambda == Lambda_1] == [maxcut(G) < k];
  * every e_j, j <= n + 1, is in Lambda; Lambda_1 is the orthant; residual of x* <= 1e-12;
  * vertex enumeration and face enumeration agree on the subsample (to 1e-9).
"""
import itertools
import json
import os
import platform
import sys
import time

import numpy as np

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from vi_solver import proj_box, vi_residual  # noqa: E402
from welfare_cone import QuadGame, active_pattern, box_qp_max, cone_constraints, in_Lambda1  # noqa: E402

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
SEED = 20260930
EPS = 0.2
TOL = 1e-8
T0 = time.time()


def build_game(n, W, k, eps=EPS):
    """W: symmetric (n x n) integer weight matrix with zero diagonal.  Variables (x_1..x_n, y, z)."""
    N = n + 2
    deg = W.sum(axis=1)
    H, h = [], []
    for i in range(n):
        Hi = np.zeros((N, N)); Hi[i, i] = eps
        hi = np.zeros(N); hi[i] = -1.0
        H.append(Hi); h.append(hi)
    Hy = np.zeros((N, N)); Hy[n, n] = eps
    hy = np.zeros(N); hy[n] = 1.0
    H.append(Hy); h.append(hy)
    # u_{n+2} = z - eps/2 z^2 + L(x) - 2 sum_{i<j} w_ij x_i x_j + (k - 1/2) y - y L(x)
    Hz = np.zeros((N, N))
    Hz[:n, :n] = 2.0 * W                      # -1/2 v^T H v contributes -2 w_ij x_i x_j over i<j
    Hz[:n, n] = deg; Hz[n, :n] = deg          # -y deg_i x_i
    Hz[n + 1, n + 1] = eps
    hz = np.zeros(N); hz[:n] = deg; hz[n] = k - 0.5; hz[n + 1] = 1.0
    H.append(Hz); h.append(hz)
    return QuadGame(H, h)


def q_direct(W, k, x, y):
    n = len(x)
    cut = sum(W[i, j] * (x[i] + x[j] - 2 * x[i] * x[j]) for i in range(n) for j in range(i + 1, n))
    return cut + y * (k - 0.5 - W.sum(axis=1) @ x)


def maxcut(W):
    n = W.shape[0]
    best = 0
    for s in itertools.product((0, 1), repeat=n):
        s = np.array(s)
        best = max(best, int(sum(W[i, j] for i in range(n) for j in range(i + 1, n) if s[i] != s[j])))
    return best


def max_payoff_vertices(game, j):
    """max over the box of u_j when u_j is multilinear in (x, y) and separable concave in z (z = 1)."""
    N = len(game.h)
    Hj, hj = game.H[j], game.h[j]
    best = -np.inf
    for v in itertools.product((0.0, 1.0), repeat=N - 1):
        x = np.array(v + (1.0,))
        best = max(best, -0.5 * x @ Hj @ x + hj @ x)
    return best


def check_instance(n, W, k, use_faces):
    g = build_game(n, W, k)
    N = n + 2
    xs = np.zeros(N); xs[n] = xs[n + 1] = 1.0
    res = vi_residual(g.F, proj_box, xs)
    pat = active_pattern(xs)
    A_eq, A_ub = cone_constraints(g.grad_matrix(xs), pat)
    L1_orthant = all(in_Lambda1(np.eye(N)[j], A_eq, A_ub) for j in range(N))
    inL = []
    for j in range(N):
        wstar = -0.5 * xs @ g.H[j] @ xs + g.h[j] @ xs
        wmax = box_qp_max(g.H[j], g.h[j])[0] if (use_faces and j == N - 1) else max_payoff_vertices(g, j)
        inL.append(bool(wstar >= wmax - TOL))
    # sanity: the payoff formula of player n+2 equals q + z - eps/2 z^2 at random points
    rng = np.random.default_rng(n * 1000 + k)
    for _ in range(3):
        v = rng.random(N)
        direct = v[-1] - EPS / 2 * v[-1] ** 2 + q_direct(W, k, v[:n], v[n])
        assert abs(g.payoffs(v)[N - 1] - direct) < 1e-9
    return {"residual": float(res), "mu": float(g.mu), "L1_orthant": bool(L1_orthant), "in_Lambda": inL}


def graphs_all(n):
    pairs = [(i, j) for i in range(n) for j in range(i + 1, n)]
    for mask in range(1 << len(pairs)):
        W = np.zeros((n, n), dtype=int)
        for b, (i, j) in enumerate(pairs):
            if mask >> b & 1:
                W[i, j] = W[j, i] = 1
        yield W


def graphs_random(rng, n, count, weights):
    pairs = [(i, j) for i in range(n) for j in range(i + 1, n)]
    for _ in range(count):
        W = np.zeros((n, n), dtype=int)
        for (i, j) in pairs:
            if rng.random() < 0.5:
                W[i, j] = W[j, i] = int(rng.choice(weights))
        yield W


def run():
    rng = np.random.default_rng(SEED)
    families = [("all_unit", 3, list(graphs_all(3)), True), ("all_unit", 4, list(graphs_all(4)), True),
                ("all_unit", 5, list(graphs_all(5)), False),
                ("sample_unit", 6, list(graphs_random(rng, 6, 300, [1])), False),
                ("sample_w123", 6, list(graphs_random(rng, 6, 300, [1, 2, 3])), False)]
    summary, mism, checks, max_res, min_mu, all_L1, others_in = [], 0, 0, 0.0, np.inf, True, True
    for name, n, graphs, use_faces in families:
        fam = {"family": name, "n": n, "graphs": len(graphs), "pairs_checked": 0, "member_cases": 0,
               "nonmember_cases": 0, "mismatches": 0, "exact_method": "faces" if use_faces else "vertices"}
        for W in graphs:
            mc = maxcut(W)
            for k in range(1, int(W.sum() // 2) + 2):
                r = check_instance(n, W, k, use_faces)
                pred = mc < k
                got = r["in_Lambda"][-1]
                eq_L1 = all(r["in_Lambda"]) and r["L1_orthant"]
                bad = (got != pred) or (eq_L1 != pred)
                fam["pairs_checked"] += 1; fam["mismatches"] += int(bad)
                fam["member_cases"] += int(got); fam["nonmember_cases"] += int(not got)
                mism += int(bad); checks += 1
                max_res = max(max_res, r["residual"]); min_mu = min(min_mu, r["mu"])
                all_L1 &= r["L1_orthant"]; others_in &= all(r["in_Lambda"][:-1])
        summary.append(fam)
        print(fam, f"{time.time() - T0:.1f}s")
    # cross-check vertex enumeration against face enumeration on a subsample (n = 5, 6)
    xc_rng = np.random.default_rng(SEED + 1)
    xc_max, xc_n = 0.0, 0
    for n in (5, 6):
        for W in graphs_random(xc_rng, n, 6, [1, 2, 3]):
            for k in (1, max(1, maxcut(W)), maxcut(W) + 1):
                g = build_game(n, W, k)
                j = n + 1
                xc_max = max(xc_max, abs(box_qp_max(g.H[j], g.h[j])[0] - max_payoff_vertices(g, j)))
                xc_n += 1
    return {"families": summary, "total_pairs": checks, "total_mismatches": mism, "max_residual": max_res,
            "min_mu": min_mu, "eps": EPS, "L1_orthant_always": bool(all_L1),
            "other_unit_vectors_always_in_Lambda": bool(others_in),
            "crosscheck_vertices_vs_faces": {"cases": xc_n, "max_abs_diff": xc_max}}


def check_criteria(out):
    crit = {
        "membership_iff_maxcut_lt_k": (out["total_mismatches"] == 0, out["total_mismatches"]),
        "other_unit_vectors_in_Lambda": (out["other_unit_vectors_always_in_Lambda"], out["other_unit_vectors_always_in_Lambda"]),
        "Lambda1_orthant": (out["L1_orthant_always"], out["L1_orthant_always"]),
        "residual_le_1e-12": (out["max_residual"] <= 1e-12, out["max_residual"]),
        "vertices_vs_faces_le_1e-9": (out["crosscheck_vertices_vs_faces"]["max_abs_diff"] <= 1e-9,
                                      out["crosscheck_vertices_vs_faces"]["max_abs_diff"]),
    }
    crit = {k: {"pass": bool(v[0]), "value": v[1]} for k, v in crit.items()}
    crit["all_pass"] = all(v["pass"] for v in crit.values())
    for k, v in crit.items():
        if k != "all_pass" and not v["pass"]:
            print(f"CRITERION FAILED: {k}: {v}")
    return crit


def main():
    out = {"meta": {"seed": SEED, "python": platform.python_version(), "numpy": np.__version__}}
    out.update(run())
    out["criteria"] = check_criteria(out)
    out["meta"]["seconds"] = time.time() - T0
    with open(os.path.join(ROOT, "results", "results_hardness.json"), "w") as fh:
        json.dump(out, fh, indent=1)
    L = ["# E6: brute-force check of the MAX-CUT reduction (Proposition 'hardness')", "",
         f"Seed {SEED}; eps = {EPS}; {out['meta']['seconds']:.1f} s.", "",
         "| family | n | graphs | (G, k) pairs | e_N in Lambda | e_N not in Lambda | mismatches | exact max by |",
         "|---|---|---|---|---|---|---|---|"]
    for f in out["families"]:
        L.append(f"| {f['family']} | {f['n']} | {f['graphs']} | {f['pairs_checked']} | {f['member_cases']} | "
                 f"{f['nonmember_cases']} | {f['mismatches']} | {f['exact_method']} |")
    L += ["", f"- total pairs {out['total_pairs']}, mismatches {out['total_mismatches']}; max residual of x* "
          f"{out['max_residual']:.1e}; strong-monotonicity constant {out['min_mu']}",
          f"- vertex vs face enumeration cross-check: {out['crosscheck_vertices_vs_faces']}", "", "## Criteria", ""]
    for k, v in out["criteria"].items():
        L.append(f"- {k}: {'PASS' if (v if k == 'all_pass' else v['pass']) else 'FAIL'}" +
                 ("" if k == "all_pass" else f" (value {v['value']})"))
    with open(os.path.join(ROOT, "results", "tables_hardness.md"), "w") as fh:
        fh.write("\n".join(L) + "\n")
    print("\n".join(L))


if __name__ == "__main__":
    main()
