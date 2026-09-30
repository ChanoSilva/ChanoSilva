#!/usr/bin/env python3
"""E1: equilibrium versus welfare in nonatomic routing (Pigou, price of anarchy, tolls).

E1a  Pigou's example with c_1 = 1, c_2(x) = x^d, unit demand: Wardrop equilibrium,
     social optimum and their ratio, in closed form and numerically (d = 1, 2, 4, 8, 16).
E1b  Random parallel-link networks with affine costs c_e(x) = a_e x + b_e (a_e > 0,
     b_e >= 0): equilibrium and optimum computed by the projected-gradient VI solver
     on the simplex and, independently, by exact water-filling on the cost level;
     the price of anarchy is checked against the bound 4/3.
E1c  Marginal-cost tolls tau_e(f) = f_e c_e'(f_e) = a_e f_e: the equilibrium of the
     tolled operator c + tau = grad C is compared with the social optimum.

Predefined criteria (stated before the run):
  * every VI residual <= 1e-8;
  * solver and water-filling agree to 1e-7 in flow;
  * PoA <= 4/3 + 1e-9 in every affine instance; Pigou (d = 1) gives exactly 4/3;
  * tolled equilibrium equals the optimum to 1e-7 in every instance.
"""
import json
import os
import platform
import sys
import time

import numpy as np

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from vi_solver import proj_simplex, solve_vi, vi_residual  # noqa: E402

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
SEED = 20260930
T0 = time.time()


# ----------------------------------------------------------------------------- Pigou
def pigou(d):
    """Two parallel links, c_1 = 1, c_2(x) = x^d, unit demand (closed form)."""
    # Equilibrium: everybody on link 2 (cost 1 <= 1). Social cost 1.
    eq_flow = np.array([0.0, 1.0])
    eq_cost = 1.0
    # Optimum: minimise (1 - x) + x^{d+1} over x in [0, 1]; x = (d+1)^{-1/d}.
    x = (d + 1.0) ** (-1.0 / d)
    opt_flow = np.array([1.0 - x, x])
    opt_cost = 1.0 - x + x ** (d + 1)
    # Numerical check by dense search over x (independent of the calculus).
    grid = np.linspace(0.0, 1.0, 200001)
    num_opt = float(np.min(1.0 - grid + grid ** (d + 1)))
    return {"d": d, "equilibrium_flow": eq_flow.tolist(), "equilibrium_cost": eq_cost,
            "optimum_flow": opt_flow.tolist(), "optimum_cost": float(opt_cost),
            "optimum_cost_grid_search": num_opt,
            "price_of_anarchy": float(eq_cost / opt_cost)}


# ----------------------------------------------------------------------------- affine parallel links
def water_fill(a, b, demand=1.0):
    """Exact Wardrop equilibrium for parallel affine links c_e = a_e x + b_e, a_e > 0.

    Finds the common cost level c with sum_e max(0, (c - b_e)/a_e) = demand by
    bisection (the left side is continuous and strictly increasing once positive).
    """
    lo, hi = float(np.min(b)), float(np.max(b) + demand * np.max(a) + 1.0)
    for _ in range(200):
        mid = 0.5 * (lo + hi)
        tot = np.sum(np.maximum(0.0, (mid - b) / a))
        if tot < demand:
            lo = mid
        else:
            hi = mid
    c = 0.5 * (lo + hi)
    f = np.maximum(0.0, (c - b) / a)
    return f / f.sum() * demand, c


def run_affine_instances(rng, n_instances=200):
    rows = []
    for k in range(n_instances):
        m = int(rng.integers(2, 6))                      # 2..5 links
        a = rng.uniform(0.05, 1.0, size=m)
        b = rng.uniform(0.0, 1.0, size=m) * (rng.random(m) < 0.5)   # half the links free at zero flow
        cost = lambda f, a=a, b=b: a * f + b               # equilibrium operator F(f) = c(f)
        mcost = lambda f, a=a, b=b: 2 * a * f + b          # grad C, C(f) = sum f_e c_e(f_e)
        mu, L = float(np.min(a)), float(np.max(a))
        x0 = np.full(m, 1.0 / m)
        f_eq, info_eq = solve_vi(cost, proj_simplex, x0, mu, L)
        f_opt, info_opt = solve_vi(mcost, proj_simplex, x0, 2 * mu, 2 * L)
        f_toll, info_toll = solve_vi(lambda f: cost(f) + a * f, proj_simplex, x0, 2 * mu, 2 * L)
        f_eq_wf, _ = water_fill(a, b)
        f_opt_wf, _ = water_fill(2 * a, b)
        C = lambda f: float(np.sum(f * (a * f + b)))
        rows.append({
            "instance": k, "links": m, "a": a.tolist(), "b": b.tolist(),
            "equilibrium_cost": C(f_eq), "optimum_cost": C(f_opt),
            "price_of_anarchy": C(f_eq) / C(f_opt),
            "residual_eq": vi_residual(cost, proj_simplex, f_eq),
            "residual_opt": vi_residual(mcost, proj_simplex, f_opt),
            "iterations_eq": info_eq["iterations"], "iterations_opt": info_opt["iterations"],
            "contraction_factor_eq": info_eq["contraction_factor"],
            "dev_eq_vs_waterfill": float(np.max(np.abs(f_eq - f_eq_wf))),
            "dev_opt_vs_waterfill": float(np.max(np.abs(f_opt - f_opt_wf))),
            "dev_tolled_vs_opt": float(np.max(np.abs(f_toll - f_opt))),
            "used_links_eq": int(np.sum(f_eq > 1e-9)),
            "used_links_opt": int(np.sum(f_opt > 1e-9)),
            "equal_cost_spread_eq": float(np.ptp(cost(f_eq)[f_eq > 1e-9])),
            "equal_mcost_spread_opt": float(np.ptp(mcost(f_opt)[f_opt > 1e-9])),
        })
    return rows


def main():
    rng = np.random.default_rng(SEED)
    out = {"meta": {"seed": SEED, "python": platform.python_version(), "numpy": np.__version__}}
    out["E1a_pigou"] = [pigou(d) for d in (1, 2, 4, 8, 16)]
    rows = run_affine_instances(rng)
    poa = np.array([r["price_of_anarchy"] for r in rows])
    out["E1b_affine"] = {
        "instances": len(rows),
        "poa_max": float(poa.max()), "poa_mean": float(poa.mean()), "poa_median": float(np.median(poa)),
        "poa_min": float(poa.min()),
        "fraction_poa_above_1p01": float(np.mean(poa > 1.01)),
        "fraction_poa_above_1p10": float(np.mean(poa > 1.10)),
        "bound_violations": int(np.sum(poa > 4.0 / 3.0 + 1e-9)),
        "max_residual": float(max(max(r["residual_eq"], r["residual_opt"]) for r in rows)),
        "max_dev_vs_waterfill": float(max(max(r["dev_eq_vs_waterfill"], r["dev_opt_vs_waterfill"]) for r in rows)),
        "max_dev_tolled_vs_opt": float(max(r["dev_tolled_vs_opt"] for r in rows)),
        "max_iterations": int(max(max(r["iterations_eq"], r["iterations_opt"]) for r in rows)),
        "max_equal_cost_spread_eq": float(max(r["equal_cost_spread_eq"] for r in rows)),
        "fraction_eq_equals_opt_flow": float(np.mean([r["dev_tolled_vs_opt"] < 1e-7 and
                                                       abs(r["price_of_anarchy"] - 1) < 1e-9 for r in rows])),
        "argmax_instance": rows[int(np.argmax(poa))],
        "rows": rows,
    }
    out["meta"]["seconds"] = time.time() - T0
    os.makedirs(os.path.join(ROOT, "results"), exist_ok=True)
    with open(os.path.join(ROOT, "results", "results_traffic.json"), "w") as fh:
        json.dump(out, fh, indent=1)

    # Markdown summary
    L = ["# E1: traffic (Pigou, affine price of anarchy, marginal-cost tolls)", "",
         f"Seed {SEED}; {out['meta']['seconds']:.1f} s.", "",
         "## E1a Pigou, c_1 = 1, c_2 = x^d", "",
         "| d | optimum flow on link 2 | optimum cost | PoA |", "|---|---|---|---|"]
    for r in out["E1a_pigou"]:
        L.append(f"| {r['d']} | {r['optimum_flow'][1]:.6f} | {r['optimum_cost']:.6f} | {r['price_of_anarchy']:.6f} |")
    e = out["E1b_affine"]
    L += ["", "## E1b/E1c random affine parallel links", "",
          f"- instances: {e['instances']}", f"- PoA max {e['poa_max']:.6f}, mean {e['poa_mean']:.6f}, median {e['poa_median']:.6f}",
          f"- bound violations (PoA > 4/3): {e['bound_violations']}",
          f"- max VI residual: {e['max_residual']:.2e}",
          f"- max |solver - water-filling|: {e['max_dev_vs_waterfill']:.2e}",
          f"- max |tolled equilibrium - optimum|: {e['max_dev_tolled_vs_opt']:.2e}",
          f"- max iterations: {e['max_iterations']}",
          f"- fraction of instances with PoA > 1.01: {e['fraction_poa_above_1p01']:.3f}; > 1.10: {e['fraction_poa_above_1p10']:.3f}"]
    with open(os.path.join(ROOT, "results", "tables_traffic.md"), "w") as fh:
        fh.write("\n".join(L) + "\n")
    print("\n".join(L))


if __name__ == "__main__":
    main()
