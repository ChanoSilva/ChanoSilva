#!/usr/bin/env python3
"""
Lorentzian chain experiments (E5) for the MRT001 draft.

Model: n points sprinkled uniformly in the causal diamond of 1+1 Minkowski
space, written in null coordinates (u, v) in (0,1)^2 with ds^2 = du dv, so the
proper time between causally related points is tau = sqrt(du * dv).  The
causal order is the product order: p < q  iff  u_p < u_q and v_p < v_q.

Formalisms:  coordinates  -->  causal order  -->  (causal order + counting)

  E5a  Kernel of the order translation.  Monotone reparametrisations of u and
       v (the 1+1 conformal maps) and boosts preserve the order exactly;
       proper times survive boosts but not reparametrisations; a Euclidean
       rotation of the (t,x) plane, which is not conformal, changes the order.
  E5b  Dimension from the order alone: ordering fraction of sprinklings in
       causal diamonds of spacetime dimension 2, 3, 4.
  E5c  Order + number -> proper time: longest-chain length between related
       points against sqrt(n) * tau (Brightwell--Gregory regime), and its
       invariance under conformal reparametrisation.
  E5d  Order + number -> coordinates: positions in the diamond recovered from
       past/future counts and a spectral resolution of the u/v ambiguity.

Usage:   python3 lorentzian_chain.py [--fast]
Outputs: ../results/results_lorentz.json, ../results/tables_lorentz.md,
         ../figures/lorentz_chain.{png,pdf}
"""
import argparse
import bisect
import json
import os
import platform
import sys
import time
from math import gamma

import numpy as np
import scipy
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from scipy.optimize import brentq

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
RESULTS = os.path.join(ROOT, "results")
FIGURES = os.path.join(ROOT, "figures")
os.makedirs(RESULTS, exist_ok=True)
os.makedirs(FIGURES, exist_ok=True)
MASTER_SEED = 20260930


# --------------------------------------------------------------------------
# sprinklings and translations
# --------------------------------------------------------------------------
def sprinkle_diamond_2d(rng, n):
    """n points uniform in the unit square of null coordinates (u, v)."""
    return rng.random((n, 2))


def causal_order_2d(UV):
    """R[p, q] = True iff p < q (product order on null coordinates)."""
    u, v = UV[:, 0], UV[:, 1]
    return (u[:, None] < u[None, :]) & (v[:, None] < v[None, :])


def proper_time_2d(UV):
    du = UV[None, :, 0] - UV[:, None, 0]
    dv = UV[None, :, 1] - UV[:, None, 1]
    return np.sqrt(np.clip(du * dv, 0.0, None))     # meaningful only where p < q


def sprinkle_diamond(rng, n, D):
    """n points uniform in the causal diamond between (t=0,x=0) and (t=1,x=0)
    of (D)-dimensional Minkowski space (D = 1 + d), by rejection sampling."""
    d = D - 1
    pts = []
    while sum(len(b) for b in pts) < n:
        m = 4 * n
        t = rng.random(m)
        x = rng.random((m, d)) - 0.5
        r = np.linalg.norm(x, axis=1)
        ok = r < np.minimum(t, 1.0 - t)
        pts.append(np.column_stack([t[ok], x[ok]]))
    P = np.vstack(pts)[:n]
    return P


def causal_order(P):
    dt = P[None, :, 0] - P[:, None, 0]
    dx = np.linalg.norm(P[None, :, 1:] - P[:, None, 1:], axis=2)
    return dt > dx


def ordering_fraction(R):
    n = R.shape[0]
    return R.sum() / (n * (n - 1) / 2)


def myrheim_meyer_fraction(D):
    """Expected fraction of comparable *unordered* pairs for a uniform
    sprinkling in a causal diamond of D-dimensional Minkowski space:
    2 * Gamma(D+1) Gamma(D/2) / (4 Gamma(3D/2))."""
    return 2 * gamma(D + 1) * gamma(D / 2) / (4 * gamma(1.5 * D))


def mm_dimension(r):
    f = lambda D: myrheim_meyer_fraction(D) - r
    try:
        return float(brentq(f, 1.05, 12.0))
    except ValueError:
        return float("nan")


def random_monotone(rng, k=24):
    """a random strictly increasing bijection of [0,1] (a 1+1 conformal factor):
    piecewise-linear with log-normal slopes, so that it departs strongly from
    the identity"""
    w = rng.lognormal(0.0, 1.2, size=k)
    knots = np.concatenate([[0.0], np.cumsum(w) / w.sum()])
    knots[-1] = 1.0
    xs = np.linspace(0.0, 1.0, k + 1)
    return lambda x: np.interp(x, xs, knots)


# --------------------------------------------------------------------------
# E5a  kernel of the order translation
# --------------------------------------------------------------------------
def experiment_E5a(rng, fast):
    n = 300
    trials = 50 if fast else 200
    out = {"n": n, "trials": trials}
    pres_conf, tau_change_conf = 0, []
    pres_boost, tau_change_boost = 0, []
    changed_rot = []
    for _ in range(trials):
        UV = sprinkle_diamond_2d(rng, n)
        R = causal_order_2d(UV)
        T = proper_time_2d(UV)
        rel = R
        # conformal reparametrisation u -> f(u), v -> g(v)
        f, g = random_monotone(rng), random_monotone(rng)
        UV2 = np.column_stack([f(UV[:, 0]), g(UV[:, 1])])
        R2 = causal_order_2d(UV2)
        pres_conf += int(np.array_equal(R, R2))
        T2 = proper_time_2d(UV2)
        tau_change_conf.append(float(np.median(np.abs(T2[rel] - T[rel]) / T[rel])))
        # boost u -> lam u, v -> v / lam
        lam = float(rng.uniform(0.5, 2.0))
        UV3 = np.column_stack([lam * UV[:, 0], UV[:, 1] / lam])
        R3 = causal_order_2d(UV3)
        pres_boost += int(np.array_equal(R, R3))
        T3 = proper_time_2d(UV3)
        tau_change_boost.append(float(np.max(np.abs(T3[rel] - T[rel]) / T[rel])))
        # Euclidean rotation of the (t, x) plane: not a conformal map
        theta = float(np.radians(rng.uniform(5.0, 30.0)))
        t = (UV[:, 0] + UV[:, 1]) / 2
        x = (UV[:, 1] - UV[:, 0]) / 2
        t4 = np.cos(theta) * t - np.sin(theta) * x
        x4 = np.sin(theta) * t + np.cos(theta) * x
        UV4 = np.column_stack([t4 - x4, t4 + x4])
        R4 = causal_order_2d(UV4)
        rel_before = R | R.T
        rel_after = R4 | R4.T
        pairs = n * (n - 1) / 2
        changed_rot.append(float(np.count_nonzero(rel_before != rel_after) / 2 / pairs))
    out.update({
        "conformal_order_preserved": pres_conf,
        "conformal_median_relative_tau_change": float(np.median(tau_change_conf)),
        "boost_order_preserved": pres_boost,
        "boost_max_relative_tau_change": float(np.max(tau_change_boost)),
        "rotation_median_fraction_of_pairs_changed": float(np.median(changed_rot)),
        "rotation_min_fraction_of_pairs_changed": float(np.min(changed_rot)),
    })
    return out


# --------------------------------------------------------------------------
# E5b  dimension from the order alone
# --------------------------------------------------------------------------
def experiment_E5b(rng, fast):
    n = 400
    reps = 20 if fast else 60
    rows = []
    for D in (2, 3, 4):
        fr, dims = [], []
        for _ in range(reps):
            P = sprinkle_diamond(rng, n, D)
            r = ordering_fraction(causal_order(P))
            fr.append(float(r))
            dims.append(mm_dimension(r))
        rows.append({"D": D, "n": n, "repetitions": reps,
                     "ordering_fraction_mean": float(np.mean(fr)),
                     "ordering_fraction_sd": float(np.std(fr, ddof=1)),
                     "expected_fraction": myrheim_meyer_fraction(D),
                     "dimension_estimate_mean": float(np.nanmean(dims)),
                     "dimension_estimate_sd": float(np.nanstd(dims, ddof=1))})
    return rows


# --------------------------------------------------------------------------
# E5c  order + number -> proper time (longest chains)
# --------------------------------------------------------------------------
def lis_length(seq):
    """length of the longest strictly increasing subsequence"""
    tails = []
    for x in seq:
        i = bisect.bisect_left(tails, x)
        if i == len(tails):
            tails.append(x)
        else:
            tails[i] = x
    return len(tails)


def longest_chain(UV, order_u, p, q):
    """number of links of the longest chain from p to q (p < q) using only
    the order: interior points sorted by u, LIS in v."""
    u, v = UV[:, 0], UV[:, 1]
    lo = np.searchsorted(u[order_u], u[p], side="right")
    hi = np.searchsorted(u[order_u], u[q], side="left")
    idx = order_u[lo:hi]
    inside = idx[(v[idx] > v[p]) & (v[idx] < v[q])]
    return lis_length(v[inside].tolist()) + 1


def experiment_E5c(rng, fast):
    plan = [(250, 8), (500, 8), (1000, 6), (2000, 4)] if not fast else [(250, 3), (500, 3), (1000, 2)]
    pairs_per_config = 600 if fast else 1500
    rows = []
    for n, reps in plan:
        Ls, taus, taus_dist, ratios = [], [], [], []
        t0 = time.time()
        for _ in range(reps):
            UV = sprinkle_diamond_2d(rng, n)
            R = causal_order_2d(UV)
            T = proper_time_2d(UV)
            f, g = random_monotone(rng), random_monotone(rng)
            UV2 = np.column_stack([f(UV[:, 0]), g(UV[:, 1])])
            T2 = proper_time_2d(UV2)
            order_u = np.argsort(UV[:, 0], kind="stable")
            order_u2 = np.argsort(UV2[:, 0], kind="stable")
            ps, qs = np.nonzero(R)
            sel = rng.choice(len(ps), size=min(pairs_per_config, len(ps)), replace=False)
            for k in sel:
                p, q = int(ps[k]), int(qs[k])
                L = longest_chain(UV, order_u, p, q)
                L2 = longest_chain(UV2, order_u2, p, q)
                assert L == L2                       # order-invariant by construction
                Ls.append(L)
                taus.append(T[p, q])
                taus_dist.append(T2[p, q])
        Ls, taus, taus_dist = map(np.array, (Ls, taus, taus_dist))
        x = np.sqrt(n) * taus
        slope = float((x * Ls).sum() / (x * x).sum())          # L ~ slope * sqrt(n) tau
        tau_hat = Ls / (2.0 * np.sqrt(n))
        rel_err = np.abs(tau_hat - taus) / taus
        rel_err_dist = np.abs(tau_hat - taus_dist) / taus_dist
        big = taus > 0.25                                       # pairs with ~ n/16 interior pts
        rows.append({"n": n, "repetitions": reps, "pairs": int(len(Ls)),
                     "corr_L_tau": float(np.corrcoef(Ls, taus)[0, 1]),
                     "corr_L_tau_distorted": float(np.corrcoef(Ls, taus_dist)[0, 1]),
                     "slope_L_vs_sqrtn_tau": slope,
                     "median_rel_err_tau_hat": float(np.median(rel_err)),
                     "median_rel_err_tau_hat_tau_gt_quarter": float(np.median(rel_err[big])),
                     "median_rel_err_vs_distorted_tau_gt_quarter": float(np.median(rel_err_dist[big])),
                     "seconds": round(time.time() - t0, 1)})
        print(f"  E5c n={n}: corr {rows[-1]['corr_L_tau']:.3f} (distorted {rows[-1]['corr_L_tau_distorted']:.3f}), "
              f"slope {slope:.3f}, med rel err {np.median(rel_err):.3f}", file=sys.stderr)
    return rows


# --------------------------------------------------------------------------
# E5d  order + number -> coordinates
# --------------------------------------------------------------------------
def reconstruct_from_counts(R):
    """Estimate (u, v) for every point from |past|, |future| and the order.

    Uniform density gives |past| ~ (n-1) u v and |future| ~ (n-1)(1-u)(1-v),
    hence s = u + v and p = u v, and {u, v} as the roots of x^2 - s x + p.
    Which root is u is a per-point sign.  A comparable pair must satisfy
    (u_r - u_q)(v_r - v_q) > 0 and an unrelated pair < 0; whenever exactly
    one of the two relative orientations satisfies the constraint the pair
    votes "same" or "opposite", and the votes are resolved globally by the
    leading eigenvector of the vote matrix (Z2 synchronisation).  The global swap u <-> v (parity) is unresolvable
    from the order and is fixed against the truth by the caller.
    """
    n = R.shape[0]
    past = R.sum(0).astype(float)
    fut = R.sum(1).astype(float)
    p = past / (n - 1)
    s = 1.0 - (fut - past) / (n - 1)
    disc = np.clip(s * s - 4 * p, 0.0, None)
    big = (s + np.sqrt(disc)) / 2
    small = (s - np.sqrt(disc)) / 2
    rel = R | R.T                                    # comparable pairs
    inc = ~rel
    np.fill_diagonal(inc, False)
    # sign of the product of coordinate differences under each orientation:
    #   same orientation:     (u_r-u_q)(v_r-v_q) = (b_r-b_q)(s_r-s_q)
    #   opposite orientation: (u_r-u_q)(v_r-v_q) = (b_r-s_q)(s_r-b_q)
    # a comparable pair needs a positive product, an unrelated pair a negative one
    same_prod = (big[:, None] - big[None, :]) * (small[:, None] - small[None, :])
    diff_prod = (big[:, None] - small[None, :]) * (small[:, None] - big[None, :])
    same_ok = np.where(rel, same_prod > 0, same_prod < 0)
    diff_ok = np.where(rel, diff_prod > 0, diff_prod < 0)
    off = ~np.eye(n, dtype=bool)
    W = np.zeros((n, n))
    W[off & same_ok & ~diff_ok] = 1.0
    W[off & diff_ok & ~same_ok] = -1.0
    w, V = np.linalg.eigh(W)
    sigma = np.sign(V[:, -1])
    sigma[sigma == 0] = 1.0
    u = np.where(sigma > 0, big, small)
    v = np.where(sigma > 0, small, big)
    return np.column_stack([u, v])


def experiment_E5d(rng, fast):
    plan = [(250, 10), (500, 10), (1000, 6), (2000, 4)] if not fast else [(250, 3), (500, 3), (1000, 2)]
    rows = []
    for n, reps in plan:
        rmse, viol = [], []
        for _ in range(reps):
            UV = sprinkle_diamond_2d(rng, n)
            R = causal_order_2d(UV)
            est = reconstruct_from_counts(R)
            e1 = np.sqrt(((est - UV) ** 2).sum(1).mean())
            e2 = np.sqrt(((est[:, ::-1] - UV) ** 2).sum(1).mean())
            rmse.append(float(min(e1, e2)))
            R_est = causal_order_2d(est)
            pairs = n * (n - 1) / 2
            viol.append(float(np.count_nonzero((R | R.T) != (R_est | R_est.T)) / 2 / pairs))
        rows.append({"n": n, "repetitions": reps,
                     "rmse_median": float(np.median(rmse)), "rmse_max": float(np.max(rmse)),
                     "rmse_times_sqrt_n": float(np.median(rmse) * np.sqrt(n)),
                     "order_disagreement_median": float(np.median(viol))})
        print(f"  E5d n={n}: median RMSE {np.median(rmse):.4f} (x sqrt n = {np.median(rmse)*np.sqrt(n):.3f}), "
              f"order disagreement {np.median(viol):.4f}", file=sys.stderr)
    return rows


# --------------------------------------------------------------------------
def make_figure(res, rng):
    fig, axes = plt.subplots(1, 2, figsize=(8.0, 3.2), dpi=150)
    # left: one sprinkling, true positions vs reconstruction from order + number
    n = 500
    UV = sprinkle_diamond_2d(rng, n)
    est = reconstruct_from_counts(causal_order_2d(UV))
    if np.sqrt(((est[:, ::-1] - UV) ** 2).sum(1).mean()) < np.sqrt(((est - UV) ** 2).sum(1).mean()):
        est = est[:, ::-1]
    ax = axes[0]
    for (u0, v0), (u1, v1) in zip(UV, est):                 # displacement segments
        ax.plot([u0, u1], [v0, v1], color="#bdbdbd", lw=0.5, zorder=1)
    ax.scatter(UV[:, 0], UV[:, 1], s=7, color="#08519c", label="sprinkled points", zorder=2)
    ax.scatter(est[:, 0], est[:, 1], s=9, color="#e6550d", marker="x", lw=0.7,
               label="recovered from order + counts", zorder=3)
    ax.set_xlabel("$u$"); ax.set_ylabel("$v$"); ax.set_aspect("equal")
    ax.set_xlim(-0.02, 1.02); ax.set_ylim(-0.02, 1.02)
    ax.set_title(f"E5d: coordinates from the order, $n={n}$", fontsize=9)
    ax.legend(frameon=False, fontsize=7, loc="upper center", bbox_to_anchor=(0.5, -0.16), ncol=2)
    # right: chain length vs sqrt(n) tau (E5c summary)
    ax = axes[1]
    rows = res["E5c"]
    ax.plot([r["n"] for r in rows], [r["median_rel_err_tau_hat_tau_gt_quarter"] for r in rows], "o-",
            color="#08519c", label=r"median rel. error of $\hat\tau=L/(2\sqrt{n})$, $\tau>1/4$")
    ax.plot([r["n"] for r in rows], [abs(r["slope_L_vs_sqrtn_tau"] - 2) / 2 for r in rows], "s--",
            color="#e6550d", label=r"$|\mathrm{slope}-2|/2$")
    ax.set_xscale("log", base=2); ax.set_yscale("log")
    ax.set_xlabel("sample size $n$"); ax.set_ylabel("relative deviation")
    ax.set_title("E5c: proper time from longest chains", fontsize=9)
    ax.grid(True, which="both", lw=0.3, alpha=0.5)
    ax.legend(frameon=False, fontsize=7)
    fig.tight_layout()
    fig.savefig(os.path.join(FIGURES, "lorentz_chain.png"))
    fig.savefig(os.path.join(FIGURES, "lorentz_chain.pdf"))
    plt.close(fig)


def write_tables(res):
    L = ["# Lorentzian chain tables (generated by experiments/lorentzian_chain.py)\n",
         f"seed = {MASTER_SEED}; fast = {res['meta']['fast']}; runtime = {res['meta']['seconds']} s\n",
         "\n## E5a Kernel of the order translation\n"]
    for k, v in res["E5a"].items():
        L.append(f"- {k}: {v}")
    L += ["\n## E5b Ordering fraction and dimension estimate\n",
          "| D | n | reps | ordering fraction (mean +- sd) | expected | dimension estimate (mean +- sd) |",
          "|---|---|---|---|---|---|"]
    for r in res["E5b"]:
        L.append(f"| {r['D']} | {r['n']} | {r['repetitions']} | {r['ordering_fraction_mean']:.4f} +- "
                 f"{r['ordering_fraction_sd']:.4f} | {r['expected_fraction']:.4f} | "
                 f"{r['dimension_estimate_mean']:.3f} +- {r['dimension_estimate_sd']:.3f} |")
    L += ["\n## E5c Longest chains versus proper time\n",
          "| n | pairs | corr(L, tau) | corr(L, tau distorted) | slope L/(sqrt(n) tau) | median rel err | median rel err (tau>1/4) | median rel err vs distorted (tau>1/4) |",
          "|---|---|---|---|---|---|---|---|"]
    for r in res["E5c"]:
        L.append(f"| {r['n']} | {r['pairs']} | {r['corr_L_tau']:.4f} | {r['corr_L_tau_distorted']:.4f} | "
                 f"{r['slope_L_vs_sqrtn_tau']:.3f} | {r['median_rel_err_tau_hat']:.3f} | "
                 f"{r['median_rel_err_tau_hat_tau_gt_quarter']:.3f} | {r['median_rel_err_vs_distorted_tau_gt_quarter']:.3f} |")
    L += ["\n## E5d Coordinates from order + number\n",
          "| n | reps | median RMSE | max RMSE | median RMSE x sqrt(n) | order disagreement |",
          "|---|---|---|---|---|---|"]
    for r in res["E5d"]:
        L.append(f"| {r['n']} | {r['repetitions']} | {r['rmse_median']:.4f} | {r['rmse_max']:.4f} | "
                 f"{r['rmse_times_sqrt_n']:.3f} | {r['order_disagreement_median']:.4f} |")
    with open(os.path.join(RESULTS, "tables_lorentz.md"), "w") as fh:
        fh.write("\n".join(L) + "\n")


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--fast", action="store_true")
    args = ap.parse_args()
    rng = np.random.default_rng(MASTER_SEED + 1)
    t0 = time.time()
    res = {"meta": {"seed": MASTER_SEED + 1, "fast": args.fast,
                    "python": platform.python_version(), "numpy": np.__version__,
                    "scipy": scipy.__version__}}
    for name, fn in (("E5a", experiment_E5a), ("E5b", experiment_E5b),
                     ("E5c", experiment_E5c), ("E5d", experiment_E5d)):
        print(f"{name} ...", file=sys.stderr)
        res[name] = fn(rng, args.fast)
    res["meta"]["seconds"] = round(time.time() - t0, 1)
    with open(os.path.join(RESULTS, "results_lorentz.json"), "w") as fh:
        json.dump(res, fh, indent=2)
    make_figure(res, np.random.default_rng(7))
    write_tables(res)
    print(f"done in {res['meta']['seconds']} s", file=sys.stderr)


if __name__ == "__main__":
    main()
