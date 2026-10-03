#!/usr/bin/env python3
"""E7 (v0.3): a three-commodity network whose commodity-weight cone is not polyhedral.

Answers the expectation of Open question 8.2 of v0.2 (internal review, round 2, M2).
Commodities k = 1, 2, 3 with unit demand; commodity k chooses between a private edge and one
shared edge of cost f (a_s = 1).  Private costs: f/4, f/4 and the constant 2.  With
y = (y_1, y_2, y_3) in [0,1]^3 the flows on the shared edge and S = y_1 + y_2 + y_3,
    C_1 = (1 - y_1)^2 / 4 + y_1 S,   C_2 = (1 - y_2)^2 / 4 + y_2 S,   C_3 = 2 (1 - y_3) + y_3 S.
Proved in the manuscript (Example 'three commodities'):
  * y* = (0, 0, 1) is the unique Wardrop equilibrium and Lambda_1(y*) = R^3_+;
  * Lambda(y*) = { lambda >= 0 : lambda_3 + m(lambda_1, lambda_2) >= 0 }, where
    m = min over [0,1]^2 of P(u, w) = l1 (u^2 - 2u)/4 + l2 (w^2 - 2w)/4 + (u + w)(l1 u + l2 w);
  * on the slice lambda_2 = 1 and for 2/3 < lambda_1 < 3/2 the boundary is
    lambda_3 = psi(lambda_1) = lambda_1 (lambda_1 + 1) / (4 (4 - lambda_1)(4 lambda_1 - 1)),
    a rational, non-affine (strictly convex) function, so Lambda(y*) is not polyhedral;
  * lambda = (1, 1, 1/20) is in Lambda_1 but not in Lambda: y = (1/9, 1/9, 0) improves by 1/180.
This script checks all of it numerically, with the exact face enumeration of the box QP
(27 faces) and independently of the closed forms.

Criteria (evaluated by check_criteria(); no external pre-registration):
  * equilibrium residual <= 1e-8 and solver output = (0, 0, 1) to 1e-9;
  * every tested direction lies in Lambda_1 (linear test);
  * bisected boundary on lambda_2 = 1 within 1e-7 of psi on the grid of lambda_1 in [0.7, 1.45];
  * the description {lambda_3 + m >= 0} (m by face enumeration on [0,1]^2) agrees with the
    exact 3-d test at every grid point farther than 1e-6 from the boundary;
  * witness gap 1/180 to 1e-9 at y = (1/9, 1/9, 0).
"""
import json
import os
import platform
import sys
import time

import numpy as np

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from vi_solver import proj_box, solve_vi, vi_residual  # noqa: E402
from welfare_cone import active_pattern, box_qp_max, cone_constraints, in_Lambda1  # noqa: E402

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
SEED = 20260930
T0 = time.time()
TOL = 1e-8

A_PRIV = np.array([0.25, 0.25, 0.0])
B_PRIV = np.array([0.0, 0.0, 2.0])
A_S = 1.0


def costs(y):
    S = y.sum()
    return (1 - y) * (A_PRIV * (1 - y) + B_PRIV) + y * A_S * S


def quad_form():
    """C_k(y) = 1/2 y^T Q_k y + q_k^T y + r_k."""
    Q, q, r = [], [], []
    for k in range(3):
        Qk = np.zeros((3, 3)); Qk[k, :] += A_S; Qk[:, k] += A_S; Qk[k, k] += 2 * A_PRIV[k]
        qk = np.zeros(3); qk[k] = -2 * A_PRIV[k] - B_PRIV[k]
        Q.append(Qk); q.append(qk); r.append(A_PRIV[k] + B_PRIV[k])
    return Q, q, r


Q, q, r = quad_form()


def F(y):
    """Reduced Wardrop operator: shared-path cost minus private-path cost."""
    return A_S * y.sum() - (A_PRIV * (1 - y) + B_PRIV)


def gap(lam, ys):
    """max over the box of Phi(y*) - Phi(y), Phi = sum lam_k C_k, by exact face enumeration."""
    Hq = sum(l * Qk for l, Qk in zip(lam, Q))
    hq = -sum(l * qk for l, qk in zip(lam, q))
    wmax, x = box_qp_max(Hq, hq)                      # max of -Phi up to the constants r
    wst = -0.5 * ys @ Hq @ ys + hq @ ys
    return float(wmax - wst), x


def in_Lambda(lam, ys):
    return gap(lam, ys)[0] <= TOL


def m_face(l1, l2):
    """min over [0,1]^2 of P(u, w), by face enumeration (independent of the closed form)."""
    H = np.array([[2 * l1 * (A_PRIV[0] + A_S), A_S * (l1 + l2)], [A_S * (l1 + l2), 2 * l2 * (A_PRIV[1] + A_S)]])
    g = np.array([2 * l1 * A_PRIV[0], 2 * l2 * A_PRIV[1]])
    wmax, x = box_qp_max(H, g)                         # max of -P
    return -wmax, x


def psi(l1):
    return l1 * (l1 + 1) / (4 * (4 - l1) * (4 * l1 - 1))


def main():
    out = {"meta": {"seed": SEED, "python": platform.python_version(), "numpy": np.__version__}}
    for y in (np.array([0.3, 0.6, 0.2]), np.array([0.0, 0.0, 1.0])):
        assert np.allclose(costs(y), [0.5 * y @ Qk @ y + qk @ y + rk for Qk, qk, rk in zip(Q, q, r)])
    J = np.diag(A_PRIV) + A_S * np.ones((3, 3))
    mu, L = float(np.linalg.eigvalsh(J).min()), float(np.linalg.norm(J, 2))
    ys, info = solve_vi(F, proj_box, np.full(3, 0.5), mu, L, tol=1e-14)
    res = vi_residual(F, proj_box, ys)
    ys_exact = np.array([0.0, 0.0, 1.0])
    G = np.array([-(Qk @ ys_exact + qk) for Qk, qk in zip(Q, q)])     # gradients of u_k = -C_k
    A_eq, A_ub = cone_constraints(G, active_pattern(ys_exact))
    rng = np.random.default_rng(SEED)
    dirs = rng.dirichlet(np.ones(3), size=200)
    L1_all = all(in_Lambda1(d, A_eq, A_ub) for d in dirs) and all(in_Lambda1(e, A_eq, A_ub) for e in np.eye(3))
    # boundary on the slice lambda_2 = 1
    grid = np.linspace(0.7, 1.45, 16)
    bnd = []
    for l1 in grid:
        lo, hi = 0.0, 1.0
        for _ in range(50):
            mid = 0.5 * (lo + hi)
            if in_Lambda(np.array([l1, 1.0, mid]), ys_exact):
                hi = mid
            else:
                lo = mid
        bnd.append(hi)
    bnd = np.array(bnd)
    ps = np.array([psi(l1) for l1 in grid])
    competitors = [gap(np.array([l1, 1.0, b - 1e-4]), ys_exact)[1].tolist() for l1, b in zip(grid[::5], bnd[::5])]
    # full description vs exact test on a grid of the slice lambda_2 = 1 and of lambda_3 = 1
    mism, tested, skipped = 0, 0, 0
    for l1 in np.linspace(0.0, 3.0, 31):
        for l3 in np.linspace(0.0, 0.3, 31):
            lam = np.array([l1, 1.0, l3])
            mval = m_face(l1, 1.0)[0]
            if abs(l3 + mval) < 1e-6:
                skipped += 1
                continue
            tested += 1
            mism += int(in_Lambda(lam, ys_exact) != (l3 + mval >= 0))
    for l1 in np.linspace(0.0, 30.0, 31):
        for l2 in np.linspace(0.0, 30.0, 31):
            lam = np.array([l1, l2, 1.0])
            mval = m_face(l1, l2)[0]
            if abs(1.0 + mval) < 1e-6:
                skipped += 1
                continue
            tested += 1
            mism += int(in_Lambda(lam, ys_exact) != (1.0 + mval >= 0))
    wg, wx = gap(np.array([1.0, 1.0, 0.05]), ys_exact)
    out["E7"] = {"a_private": A_PRIV.tolist(), "b_private": B_PRIV.tolist(), "a_shared": A_S,
                 "y_star_solver": ys.tolist(), "residual": float(res), "iterations": info["iterations"],
                 "mu": mu, "L": L, "costs_at_eq": costs(ys_exact).tolist(), "grad_u": G.tolist(),
                 "L1_orthant_all_tested": bool(L1_all), "L1_tested_dirs": len(dirs) + 3,
                 "slice_grid": grid.tolist(), "boundary_bisected": bnd.tolist(), "psi": ps.tolist(),
                 "max_abs_boundary_minus_psi": float(np.max(np.abs(bnd - ps))),
                 "psi_second_differences": np.diff(ps, 2).tolist(),
                 "psi_second_differences_all_positive": bool(np.all(np.diff(ps, 2) > 0)),
                 "competitor_points": competitors,
                 "description_tests": tested, "description_mismatches": mism, "description_skipped_near_boundary": skipped,
                 "witness_lambda": [1.0, 1.0, 0.05], "witness_gap": wg, "witness_y": wx.tolist(),
                 "psi_at_1": psi(1.0)}
    e = out["E7"]
    crit = {
        "residual_le_1e-8": (e["residual"] <= 1e-8 and np.allclose(ys, ys_exact, atol=1e-9), e["residual"]),
        "Lambda1_orthant": (e["L1_orthant_all_tested"], e["L1_tested_dirs"]),
        "boundary_vs_psi_le_1e-7": (e["max_abs_boundary_minus_psi"] <= 1e-7, e["max_abs_boundary_minus_psi"]),
        "description_mismatches_zero": (mism == 0, f"{mism}/{tested}"),
        "witness_gap_1_180_to_1e-9": (abs(wg - 1 / 180) <= 1e-9, wg),
    }
    out["criteria"] = {k: {"pass": bool(v[0]), "value": v[1]} for k, v in crit.items()}
    out["criteria"]["all_pass"] = all(v["pass"] for v in out["criteria"].values())
    for k, v in out["criteria"].items():
        if k != "all_pass" and not v["pass"]:
            print(f"CRITERION FAILED: {k}: {v}")
    out["meta"]["seconds"] = time.time() - T0
    with open(os.path.join(ROOT, "results", "results_three_commodity.json"), "w") as fh:
        json.dump(out, fh, indent=1)
    Lm = ["# E7: three commodities, non-polyhedral commodity-weight cone", "", f"{out['meta']['seconds']:.1f} s.", "",
          f"- y* (solver) = {e['y_star_solver']}, residual {e['residual']:.1e}, costs at y* {e['costs_at_eq']}",
          f"- Lambda_1 = orthant on all {e['L1_tested_dirs']} tested directions: {e['L1_orthant_all_tested']}",
          f"- slice lambda_2 = 1, lambda_1 in [0.7, 1.45] (16 points): max |bisected boundary - psi| = "
          f"{e['max_abs_boundary_minus_psi']:.1e}; psi second differences all positive: {e['psi_second_differences_all_positive']}",
          f"- competitor points (face y_3 = 0): {np.round(np.array(e['competitor_points']), 4).tolist()}",
          f"- description {{lambda_3 + m >= 0}} vs exact test: {mism} mismatches in {tested} grid points "
          f"({skipped} skipped within 1e-6 of the boundary)",
          f"- witness lambda = (1, 1, 1/20): gap {wg:.10f} (1/180 = {1/180:.10f}) at y = {np.round(wx, 6).tolist()}",
          "", "## Criteria", ""]
    for k, v in out["criteria"].items():
        Lm.append(f"- {k}: {'PASS' if (v if k == 'all_pass' else v['pass']) else 'FAIL'}" +
                  ("" if k == "all_pass" else f" (value {v['value']})"))
    with open(os.path.join(ROOT, "results", "tables_three_commodity.md"), "w") as fh:
        fh.write("\n".join(Lm) + "\n")
    print("\n".join(Lm))


if __name__ == "__main__":
    main()
