#!/usr/bin/env python3
"""E1: equilibrium versus welfare in nonatomic routing (Pigou, price of anarchy, tolls).

E1a  Pigou's example with c_1 = 1, c_2(x) = x^d, unit demand: Wardrop equilibrium,
     social optimum and their ratio, in closed form and numerically (d = 1, 2, 4, 8, 16).
E1b  Random parallel-link networks with affine costs c_e(x) = a_e x + b_e (a_e > 0,
     b_e >= 0): equilibrium and optimum computed by the projected-gradient VI solver
     on the simplex and, independently, by exact water-filling on the cost level;
     the price of anarchy is checked against the bound 4/3.
E1c  (merged into E1b in v0.3.)  For affine costs the tolled operator c + tau, tau_e = a_e f_e,
     is the same function as grad C = 2 a f + b, so "the equilibrium of the tolled operator" and
     "the optimum" are one solver call; v0.2 ran it twice and the two deviations from the
     water-filling optimum coincided bit for bit (internal review, round 2, m1).  The optimum
     computed by the solver is compared with the water-filling optimum in E1b, which is the
     only content of that check.

Criteria (stated in this docstring and evaluated by check_criteria() below, which writes a
pass/fail flag and the margins into results/results_traffic.json; there is no external
pre-registration record):
  * every VI residual <= 1e-8;
  * solver and water-filling agree to 1e-7 in flow (equilibrium and optimum);
  * PoA <= 4/3 + 1e-9 in every affine instance; Pigou (d = 1) gives 4/3 to 1e-12.
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
            "used_links_eq": int(np.sum(f_eq > 1e-9)),
            "used_links_opt": int(np.sum(f_opt > 1e-9)),
            "equal_cost_spread_eq": float(np.ptp(cost(f_eq)[f_eq > 1e-9])),
            "equal_mcost_spread_opt": float(np.ptp(mcost(f_opt)[f_opt > 1e-9])),
        })
    return rows


def make_figure(out):
    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt
    BLUE, ORANGE, INK, MUTED = "#2a78d6", "#eb6834", "#0b0b0b", "#52514e"
    plt.rcParams.update({"font.size": 9, "axes.edgecolor": MUTED, "axes.labelcolor": INK,
                         "xtick.color": MUTED, "ytick.color": MUTED, "axes.spines.top": False,
                         "axes.spines.right": False})
    # v0.3: the Pigou-vs-d panel was dropped (it plots the closed form of Example 3.7; values in tables_traffic.md)
    fig, ax = plt.subplots(figsize=(3.3, 2.5))
    vals = [r["price_of_anarchy"] for r in out["E1b_affine"]["rows"]]
    ax.hist(vals, bins=np.linspace(1.0, 4 / 3, 21), color=BLUE, edgecolor="#fcfcfb", lw=0.8)
    ax.axvline(4 / 3, color=ORANGE, lw=1.2, ls="--")
    ax.text(4 / 3 - 0.005, ax.get_ylim()[1] * 0.9, "4/3", color=INK, fontsize=8, ha="right")
    ax.set_xlabel("price of anarchy (affine parallel links)"); ax.set_ylabel("instances")
    ax.set_title(f"{len(vals)} random instances, max {max(vals):.3f}", fontsize=8.5, color=INK)
    ax.grid(True, axis="y", color="#e6e5e0", lw=0.5); ax.set_axisbelow(True)
    fig.tight_layout()
    os.makedirs(os.path.join(ROOT, "figures"), exist_ok=True)
    fig.savefig(os.path.join(ROOT, "figures", "fig_poa.png"), dpi=200)
    fig.savefig(os.path.join(ROOT, "figures", "fig_poa.pdf"))
    plt.close(fig)


def check_criteria(out):
    """Evaluate the docstring criteria; returns per-criterion pass flags, values and thresholds."""
    e = out["E1b_affine"]
    pig = {r["d"]: r for r in out["E1a_pigou"]}
    crit = {
        "residuals_le_1e-8": {"value": e["max_residual"], "threshold": 1e-8},
        "solver_vs_waterfill_le_1e-7": {"value": e["max_dev_vs_waterfill"], "threshold": 1e-7},
        "poa_bound_violations_zero": {"value": e["bound_violations"], "threshold": 0},
        "pigou_d1_poa_minus_4_3_le_1e-12": {"value": abs(pig[1]["price_of_anarchy"] - 4.0 / 3.0), "threshold": 1e-12},
    }
    for v in crit.values():
        v["pass"] = bool(v["value"] <= v["threshold"])
    crit["all_pass"] = all(v["pass"] for v in crit.values())
    for k, v in crit.items():
        if k != "all_pass" and not v["pass"]:
            print(f"CRITERION FAILED: {k}: {v}")
    return crit


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
        "max_iterations": int(max(max(r["iterations_eq"], r["iterations_opt"]) for r in rows)),
        "max_equal_cost_spread_eq": float(max(r["equal_cost_spread_eq"] for r in rows)),
        "n_poa_equals_one": int(np.sum(np.abs(poa - 1.0) < 1e-9)),
        "fraction_poa_equals_one": float(np.mean(np.abs(poa - 1.0) < 1e-9)),
        "argmax_instance": rows[int(np.argmax(poa))],
        "rows": rows,
    }
    out["criteria"] = check_criteria(out)
    out["meta"]["seconds"] = time.time() - T0
    os.makedirs(os.path.join(ROOT, "results"), exist_ok=True)
    with open(os.path.join(ROOT, "results", "results_traffic.json"), "w") as fh:
        json.dump(out, fh, indent=1)
    make_figure(out)

    # Markdown summary
    L = ["# E1: traffic (Pigou, affine price of anarchy, marginal-cost tolls)", "",
         f"Seed {SEED}; {out['meta']['seconds']:.1f} s.", "",
         "## E1a Pigou, c_1 = 1, c_2 = x^d", "",
         "| d | optimum flow on link 2 | optimum cost | PoA |", "|---|---|---|---|"]
    for r in out["E1a_pigou"]:
        L.append(f"| {r['d']} | {r['optimum_flow'][1]:.6f} | {r['optimum_cost']:.6f} | {r['price_of_anarchy']:.6f} |")
    e = out["E1b_affine"]
    L += ["", "## E1b random affine parallel links (E1c merged here in v0.3)", "",
          f"- instances: {e['instances']}", f"- PoA max {e['poa_max']:.6f}, mean {e['poa_mean']:.6f}, median {e['poa_median']:.6f}",
          f"- bound violations (PoA > 4/3): {e['bound_violations']}",
          f"- max VI residual: {e['max_residual']:.2e}",
          f"- max |solver - water-filling|: {e['max_dev_vs_waterfill']:.2e}",
          f"- max iterations: {e['max_iterations']}",
          f"- fraction of instances with PoA > 1.01: {e['fraction_poa_above_1p01']:.3f}; > 1.10: {e['fraction_poa_above_1p10']:.3f}",
          f"- instances with PoA = 1 exactly (equilibrium = optimum): {e['n_poa_equals_one']}/{e['instances']}", "",
          "## Criteria", ""]
    for k, v in out["criteria"].items():
        L.append(f"- {k}: {'PASS' if (v if k == 'all_pass' else v['pass']) else 'FAIL'}" +
                 ("" if k == "all_pass" else f" (value {v['value']:.3g}, threshold {v['threshold']:.3g})"))
    with open(os.path.join(ROOT, "results", "tables_traffic.md"), "w") as fh:
        fh.write("\n".join(L) + "\n")
    print("\n".join(L))


if __name__ == "__main__":
    main()
