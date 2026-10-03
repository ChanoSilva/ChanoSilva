#!/usr/bin/env python3
"""E5: commodity-weight cones in two-commodity nonatomic routing (Open question 2 of v0.1).

Network: commodities k = 1, 2 with unit demand; commodity 1 has a private edge (cost
a_0 f + b_0) and the shared edge (cost a_s f + b_s), commodity 2 a private edge (a_1 f + b_1)
and the same shared edge.  Variables y = (f_B, f_D) in [0,1]^2 = flow of each commodity on
the shared edge; path flows are determined by edge flows, so the Wardrop equilibrium f* is
unique when a_0, a_1, a_s > 0 and the cone does not depend on a path-flow representative.
C_k(y) = sum_{p in P_k} f_p c_p(f) is the cost borne by commodity k: a quadratic in y with
indefinite Hessian (cross term a_s f_B f_D), so Theorem 5.1(c) does not apply.

    Lambda(f*)   = { lambda >= 0 : f* minimises lambda_1 C_1 + lambda_2 C_2 over [0,1]^2 }
    Lambda_1(f*) = { lambda >= 0 : -sum_k lambda_k grad C_k(f*) in N_K(f*) }

E5a Fixed instance a_0 = 1, b_0 = 2, a_1 = 1/4, b_1 = 0, a_s = 1, b_s = 0 (manuscript,
    Example 'routing cone').  Hand calculation: f* = (1, 0), Lambda_1 = R^2_+ but
    Lambda = { lambda_2 <= 40 lambda_1 }; for lambda = (0, 1) the point (0, 1/5) lowers C_2
    from 1/4 to 1/5.  Hence Lambda != Lambda_1 even for affine separable costs.
E5b Random instances (a ~ U(0.05, 1); b = 0 w.p. 1/2, else U(0, 1)): how often the direction
    grid meets Lambda_1, how often Lambda_1 is the whole orthant, and how often a direction in
    Lambda_1 carries a certified witness (W_lambda improves by > 1e-6) that it is not in
    Lambda.  Descriptive only.

Criteria (stated here and evaluated by check_criteria(), which writes pass/fail flags into
results/results_commodity.json; no external pre-registration record):
  * every equilibrium residual <= 1e-8;
  * E5a: all tested directions lie in Lambda_1; the bisected boundary lambda_1 (at lambda_2 = 1)
    equals 1/40 to 1e-6; the witness gap for lambda = (0, 1) equals 1/20 to 1e-9;
  * E5b: no direction certified in Lambda (QP gap <= 1e-11) lies outside Lambda_1 (Theorem 5.1(b)).
    Directions that the exact test accepts only within its 1e-8 tolerance while violating the
    linear test by more than 1e-9 are recorded separately as tolerance-level disagreements.
"""
import json
import os
import platform
import sys
import time

import numpy as np

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from vi_solver import proj_box, solve_vi, vi_residual  # noqa: E402
from welfare_cone import QuadGame, active_pattern, cone_constraints, in_Lambda, in_Lambda1  # noqa: E402

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
SEED = 20260930
T0 = time.time()
WITNESS_GAP = 1e-6


class TwoCommodity:
    """Costs as quadratics C_k(y) = 1/2 y^T Q_k y + q_k^T y + r_k in y = (f_B, f_D)."""

    def __init__(self, a0, b0, a1, b1, a_s, b_s):
        self.par = dict(a0=a0, b0=b0, a1=a1, b1=b1, a_s=a_s, b_s=b_s)
        self.Q = [np.array([[2 * (a0 + a_s), a_s], [a_s, 0.0]]), np.array([[0.0, a_s], [a_s, 2 * (a1 + a_s)]])]
        self.q = [np.array([-2 * a0 - b0 + b_s, 0.0]), np.array([0.0, -2 * a1 - b1 + b_s])]
        self.r = [a0 + b0, a1 + b1]
        J = np.array([[a_s + a0, a_s], [a_s, a_s + a1]])          # Jacobian of the reduced operator
        self.mu, self.L = float(np.linalg.eigvalsh(J).min()), float(np.linalg.norm(J, 2))
        self.game = QuadGame(self.Q, [-qk for qk in self.q])       # u_k = -C_k (constants dropped)

    def costs(self, y):
        return np.array([0.5 * y @ Qk @ y + qk @ y + rk for Qk, qk, rk in zip(self.Q, self.q, self.r)])

    def costs_direct(self, y):
        p = self.par
        fB, fD = y
        cs = p["a_s"] * (fB + fD) + p["b_s"]
        return np.array([(1 - fB) * (p["a0"] * (1 - fB) + p["b0"]) + fB * cs,
                         (1 - fD) * (p["a1"] * (1 - fD) + p["b1"]) + fD * cs])

    def F(self, y):
        """Reduced Wardrop operator: cost of the shared path minus cost of the private path."""
        p = self.par
        cs = p["a_s"] * (y[0] + y[1]) + p["b_s"]
        return np.array([cs - (p["a0"] * (1 - y[0]) + p["b0"]), cs - (p["a1"] * (1 - y[1]) + p["b1"])])

    def equilibrium(self):
        y, info = solve_vi(self.F, proj_box, np.array([0.5, 0.5]), self.mu, self.L, tol=1e-13)
        info["residual"] = vi_residual(self.F, proj_box, y)
        return y, info


def analyse(net, n_dirs=91):
    ys, info = net.equilibrium()
    pat = active_pattern(ys)
    G = net.game.grad_matrix(ys)
    A_eq, A_ub = cone_constraints(G, pat)
    thetas = np.linspace(0.0, np.pi / 2, n_dirs)
    rec, best, max_tol_viol = [], None, 0.0
    for th in thetas:
        lam = np.array([np.cos(th), np.sin(th)])
        l1 = in_Lambda1(lam, A_eq, A_ub)
        ll, gap, xw = in_Lambda(net.game, ys, lam, return_witness=True)
        rec.append((float(np.degrees(th)), bool(l1), bool(ll), float(gap)))
        if ll and not l1:                      # size of the first-order violation behind the disagreement
            v_eq = float(np.abs(A_eq @ lam).max()) if A_eq.shape[0] else 0.0
            v_ub = float(max(0.0, (A_ub @ lam).max())) if A_ub.shape[0] else 0.0
            max_tol_viol = max(max_tol_viol, v_eq, v_ub)
        if l1 and not ll and gap > WITNESS_GAP and (best is None or gap > best["gap"]):
            best = {"lambda": lam.tolist(), "gap": float(gap), "better_y": xw.tolist()}
    return {"y_star": ys.tolist(), "residual": info["residual"], "iterations": info["iterations"],
            "pattern": pat.tolist(), "costs_at_eq": net.costs(ys).tolist(), "G": G.tolist(),
            "n_dirs": n_dirs, "dirs_in_L1": sum(r[1] for r in rec), "dirs_in_L": sum(r[2] for r in rec),
            "dirs_in_L_not_L1": sum(r[2] and not r[1] for r in rec),           # tolerance-level disagreements
            "violations": sum((r[3] <= 1e-11) and not r[1] for r in rec),     # certified in Lambda but outside Lambda_1
            "max_tolerance_disagreement_violation": max_tol_viol,
            "dirs_in_L1_not_L": sum(r[1] and not r[2] for r in rec),
            "witness": best, "records": rec}


def fixed_instance():
    net = TwoCommodity(a0=1.0, b0=2.0, a1=0.25, b1=0.0, a_s=1.0, b_s=0.0)
    for y in (np.array([0.3, 0.7]), np.array([1.0, 0.0]), np.array([0.0, 0.2])):
        assert np.allclose(net.costs(y), net.costs_direct(y))
    out = analyse(net)
    ys = np.array(out["y_star"])
    lo, hi = 0.0, 1.0                              # boundary of Lambda on the slice lambda_2 = 1
    for _ in range(60):
        mid = 0.5 * (lo + hi)
        if in_Lambda(net.game, ys, np.array([mid, 1.0])):
            hi = mid
        else:
            lo = mid
    m, gap, yw = in_Lambda(net.game, ys, np.array([0.0, 1.0]), return_witness=True)
    m11, gap11, _ = in_Lambda(net.game, ys, np.array([1.0, 1.0]), return_witness=True)
    hess = [Qk.tolist() for Qk in net.Q]
    out.update({"parameters": net.par, "mu": net.mu, "L": net.L, "hessians": hess,
                "hessian_dets": [float(np.linalg.det(Qk)) for Qk in net.Q],
                "boundary_lambda1_at_lambda2_1": hi, "boundary_ratio_predicted": 1.0 / 40.0,
                "witness_lambda_0_1": {"in_Lambda": bool(m), "gap": float(gap), "better_y": yw.tolist(),
                                       "costs_at_better_y": net.costs(yw).tolist()},
                "utilitarian_in_Lambda": bool(m11), "utilitarian_gap": float(gap11)})
    return out


def random_instances(rng, n_instances=200):
    rows, agg = [], {"instances": 0, "corner_equilibria": 0, "dirs_in_L1_any": 0, "L1_full_orthant": 0,
                     "witness_instances": 0, "violations_L_not_L1": 0, "tolerance_disagreements": 0,
                     "max_tolerance_disagreement_violation": 0.0, "max_residual": 0.0, "max_iterations": 0}
    for k in range(n_instances):
        a0, a1, a_s = rng.uniform(0.05, 1.0, size=3)
        b0, b1, b_s = rng.uniform(0.0, 1.0, size=3) * (rng.random(3) < 0.5)
        net = TwoCommodity(a0, b0, a1, b1, a_s, b_s)
        r = analyse(net)
        agg["instances"] += 1
        agg["corner_equilibria"] += int(np.all(np.array(r["pattern"]) != 0))
        agg["dirs_in_L1_any"] += int(r["dirs_in_L1"] > 0)
        agg["L1_full_orthant"] += int(r["dirs_in_L1"] == r["n_dirs"])
        agg["witness_instances"] += int(r["witness"] is not None)
        agg["violations_L_not_L1"] += r["violations"]
        agg["tolerance_disagreements"] += r["dirs_in_L_not_L1"]
        agg["max_tolerance_disagreement_violation"] = max(agg["max_tolerance_disagreement_violation"],
                                                          r["max_tolerance_disagreement_violation"])
        agg["max_residual"] = max(agg["max_residual"], r["residual"])
        agg["max_iterations"] = max(agg["max_iterations"], r["iterations"])
        r.pop("records")
        rows.append({"instance": k, "parameters": net.par, **r})
    return agg, rows


def check_criteria(out):
    fx, ag = out["E5a_fixed"], out["E5b_random"]
    crit = {
        "residuals_le_1e-8": (max(fx["residual"], ag["max_residual"]) <= 1e-8, max(fx["residual"], ag["max_residual"])),
        "E5a_all_directions_in_Lambda1": (fx["dirs_in_L1"] == fx["n_dirs"], f"{fx['dirs_in_L1']}/{fx['n_dirs']}"),
        "E5a_boundary_ratio_1_40_to_1e-6": (abs(fx["boundary_lambda1_at_lambda2_1"] - 1 / 40) <= 1e-6,
                                            fx["boundary_lambda1_at_lambda2_1"]),
        "E5a_witness_gap_1_20_to_1e-9": (not fx["witness_lambda_0_1"]["in_Lambda"]
                                         and abs(fx["witness_lambda_0_1"]["gap"] - 0.05) <= 1e-9,
                                         fx["witness_lambda_0_1"]["gap"]),
        "E5b_no_direction_in_L_outside_L1": (ag["violations_L_not_L1"] == 0, ag["violations_L_not_L1"]),
    }
    crit = {k: {"pass": bool(v[0]), "value": v[1]} for k, v in crit.items()}
    crit["all_pass"] = all(v["pass"] for v in crit.values())
    for k, v in crit.items():
        if k != "all_pass" and not v["pass"]:
            print(f"CRITERION FAILED: {k}: {v}")
    return crit


def main():
    rng = np.random.default_rng(SEED)
    out = {"meta": {"seed": SEED, "python": platform.python_version(), "numpy": np.__version__}}
    out["E5a_fixed"] = fixed_instance()
    agg, rows = random_instances(rng)
    out["E5b_random"] = agg
    out["E5b_rows"] = rows
    out["criteria"] = check_criteria(out)
    out["meta"]["seconds"] = time.time() - T0
    os.makedirs(os.path.join(ROOT, "results"), exist_ok=True)
    with open(os.path.join(ROOT, "results", "results_commodity.json"), "w") as fh:
        json.dump(out, fh, indent=1)
    fx = out["E5a_fixed"]
    L = ["# E5: commodity-weight cones in two-commodity routing", "", f"Seed {SEED}; {out['meta']['seconds']:.1f} s.", "",
         "## E5a fixed instance (a0=1, b0=2, a1=1/4, b1=0, a_s=1, b_s=0)",
         f"- f* = {fx['y_star']} (shared-edge flows of commodities 1, 2), residual {fx['residual']:.1e}, "
         f"C(f*) = {fx['costs_at_eq']}, Hessian determinants {fx['hessian_dets']}",
         f"- directions in Lambda_1: {fx['dirs_in_L1']}/{fx['n_dirs']}; in Lambda: {fx['dirs_in_L']}/{fx['n_dirs']}",
         f"- boundary of Lambda on lambda_2 = 1: lambda_1 = {fx['boundary_lambda1_at_lambda2_1']:.8f} (predicted 1/40 = 0.025)",
         f"- lambda = (0, 1): in Lambda {fx['witness_lambda_0_1']['in_Lambda']}, gap {fx['witness_lambda_0_1']['gap']:.6f}, "
         f"better y = {fx['witness_lambda_0_1']['better_y']}, costs there {fx['witness_lambda_0_1']['costs_at_better_y']}",
         f"- lambda = (1, 1) in Lambda: {fx['utilitarian_in_Lambda']}", "",
         "## E5b random instances", ""]
    for k, v in agg.items():
        L.append(f"- {k}: {v}")
    L += ["", "## Criteria", ""]
    for k, v in out["criteria"].items():
        L.append(f"- {k}: {'PASS' if (v if k == 'all_pass' else v['pass']) else 'FAIL'}" +
                 ("" if k == "all_pass" else f" (value {v['value']})"))
    with open(os.path.join(ROOT, "results", "tables_commodity.md"), "w") as fh:
        fh.write("\n".join(L) + "\n")
    print("\n".join(L))


if __name__ == "__main__":
    main()
