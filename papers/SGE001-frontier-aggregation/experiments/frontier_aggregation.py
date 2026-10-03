#!/usr/bin/env python3
"""SGE001 -- Moment-based aggregation of production frontiers
(research line "dynamic aggregation of production frontiers").

Controlled simulation of first-, second- and third-order moment-based
aggregation of a common concave frontier over heterogeneous production units,
in the smooth regime and at capacity (threshold) crossings, with a two-level
hierarchy and a rank-decision experiment.  Every number in the manuscript is
produced here (seed fixed) and injected by make_numbers.py.

Experiments
  E0  self-test of the analytic derivatives against central differences
  E1  dispersion sweep, smooth frontiers (Cobb-Douglas, CES) x input laws (LN, SU)
  E1b idiosyncratic efficiency terms: the covariance floor
  E1c small-dispersion exponent of the second-order error against N (finite-N effect)
  E2  capacity frontier min(f, c): threshold proximity x dispersion
  E3  two-level hierarchy (units -> firms -> sector): pooled vs bottom-up
  E4  decision experiment: rank reversals between two sectors
  E5  a scalar calibration of the second-order term, tested out of sample
  E6  closed-form examples of the manuscript (arithmetic check)

Usage: python3 frontier_aggregation.py [--fast]

Random numbers: one independent generator per experiment, spawned from
np.random.SeedSequence(SEED) (reference run v0.2; the v0.1 run shared one stream).
"""
import argparse
import datetime
import hashlib
import json
import math
import os
import platform
import time

import numpy as np
import scipy
from scipy.stats import norm
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import matplotlib.ticker

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
RES = os.path.join(ROOT, "results")
FIG = os.path.join(ROOT, "figures")
SEED = 20260930

# categorical palette (fixed order, colour-blind checked): order 1, order 2, order 3, bound, reference
C1, C2, C3, CB, CR = "#2a78d6", "#eb6834", "#1baf7a", "#4a3aa7", "#7a7a7a"
plt.rcParams.update({"font.size": 9, "axes.grid": True, "grid.alpha": 0.25, "grid.linewidth": 0.5,
                     "axes.spines.top": False, "axes.spines.right": False, "lines.linewidth": 1.6,
                     "legend.frameon": False, "figure.dpi": 150})


# --------------------------------------------------------------------------- frontiers
class CobbDouglas:
    """f(x) = A prod_j x_j^{a_j}, sum a_j < 1 (decreasing returns, strictly concave on R_+^d)."""
    name = "CD"

    def __init__(self, A=1.0, alpha=(0.3, 0.5)):
        self.A = float(A)
        self.al = np.asarray(alpha, float)
        a = self.al
        self.C = np.outer(a, a) - np.diag(a)                       # Hessian coefficients
        d = len(a)
        self.K3 = np.empty((d, d, d))                              # third-derivative coefficients
        for j in range(d):
            for k in range(d):
                for l in range(d):
                    self.K3[j, k, l] = self.C[j, k] * (a[l] - (j == l) - (k == l))

    def f(self, X):                      # X: (..., d) -> (...)
        return self.A * np.prod(X ** self.al, axis=-1)

    def grad(self, x):                   # x: (..., d) -> (..., d)
        return self.f(x)[..., None] * self.al / x

    def hess(self, x):                   # (..., d, d)
        fx = self.f(x)
        return fx[..., None, None] * self.C / (x[..., :, None] * x[..., None, :])

    def third(self, x):                  # (..., d, d, d)
        fx = self.f(x)
        return fx[..., None, None, None] * self.K3 / (x[..., :, None, None] * x[..., None, :, None] * x[..., None, None, :])

    def box_bounds(self, lo, hi):
        """Rigorous upper bounds M2, M3 for sup over the box [lo, hi] of the operator norms of
        D^2 f and D^3 f: each entry |coef| A prod_m x_m^{a_m - e_m} is monotone in every coordinate,
        so its sup sits at an explicit corner; the Frobenius norm of the entrywise sups dominates
        the operator norm.  lo, hi: (..., d)."""
        a = self.al
        d = len(a)
        lo = np.asarray(lo, float)
        hi = np.asarray(hi, float)

        def sup_entry(coef, idx):
            e = np.zeros(d)
            for m in idx:
                e[m] += 1
            val = abs(coef) * self.A * np.ones(lo.shape[:-1])
            for m in range(d):
                p = a[m] - e[m]
                val = val * (hi[..., m] ** p if p > 0 else lo[..., m] ** p)
            return val

        S2 = sum(sup_entry(self.C[j, k], (j, k)) ** 2 for j in range(d) for k in range(d))
        S3 = sum(sup_entry(self.K3[j, k, l], (j, k, l)) ** 2
                 for j in range(d) for k in range(d) for l in range(d))
        return np.sqrt(S2), np.sqrt(S3)


class CES:
    """f(x) = A (sum_j a_j x_j^rho)^{nu/rho}, rho < 1, rho != 0, 0 < nu < 1."""
    name = "CES"

    def __init__(self, A=1.0, a=(0.4, 0.6), rho=-1.0, nu=0.8):
        self.A, self.a, self.rho, self.nu = float(A), np.asarray(a, float), float(rho), float(nu)

    def _S(self, x):
        return np.sum(self.a * x ** self.rho, axis=-1)

    def f(self, X):
        return self.A * self._S(X) ** (self.nu / self.rho)

    def grad(self, x):
        S = self._S(x)
        g = self.a * x ** (self.rho - 1)
        return self.A * self.nu * g * S[..., None] ** (self.nu / self.rho - 1)

    def hess(self, x):
        rho, nu = self.rho, self.nu
        S = self._S(x)
        g = self.a * x ** (rho - 1)
        h = self.a * (rho - 1) * x ** (rho - 2)
        p = nu / rho - 1
        d = x.shape[-1]
        H = (np.eye(d) * h[..., :, None]) * S[..., None, None] ** p \
            + (nu - rho) * g[..., :, None] * g[..., None, :] * S[..., None, None] ** (p - 1)
        return self.A * nu * H

    def third(self, x):
        rho, nu = self.rho, self.nu
        S = self._S(x)
        g = self.a * x ** (rho - 1)
        h = self.a * (rho - 1) * x ** (rho - 2)
        q = self.a * (rho - 1) * (rho - 2) * x ** (rho - 3)
        p = nu / rho - 1
        d = x.shape[-1]
        I = np.eye(d)
        I3 = np.zeros((d, d, d))
        for j in range(d):
            I3[j, j, j] = 1.0
        Sp = S[..., None, None, None]
        T = I3 * q[..., :, None, None] * Sp ** p
        pair = (I[:, :] * h[..., :, None])[..., :, :, None] * g[..., None, None, :] \
            + (I[:, :] * h[..., :, None])[..., :, None, :] * g[..., None, :, None] \
            + (I[:, :] * h[..., :, None])[..., None, :, :] * g[..., :, None, None]
        T = T + (nu - rho) * pair * Sp ** (p - 1)
        T = T + (nu - rho) * (nu - 2 * rho) * g[..., :, None, None] * g[..., None, :, None] * g[..., None, None, :] * Sp ** (p - 2)
        return self.A * nu * T


def selftest(front, rng):
    """Central differences of f, grad, hess against the analytic grad, hess, third."""
    worst = {"grad": 0.0, "hess": 0.0, "third": 0.0}
    for _ in range(20):
        x = np.exp(rng.uniform(-0.7, 0.7, size=2))
        eps = 1e-5
        d = len(x)
        g = front.grad(x)
        H = front.hess(x)
        T = front.third(x)
        for j in range(d):
            e = np.zeros(d)
            e[j] = eps * x[j]
            gd = (front.f(x + e) - front.f(x - e)) / (2 * e[j])
            worst["grad"] = max(worst["grad"], abs(gd - g[j]) / abs(g[j]))
            Hd = (front.grad(x + e) - front.grad(x - e)) / (2 * e[j])
            worst["hess"] = max(worst["hess"], np.max(np.abs(Hd - H[:, j]) / np.abs(H[:, j])))
            Td = (front.hess(x + e) - front.hess(x - e)) / (2 * e[j])
            worst["third"] = max(worst["third"], np.max(np.abs(Td - T[:, :, j]) / np.maximum(np.abs(T[:, :, j]), 1e-12)))
    return worst


# --------------------------------------------------------------------------- inputs
CORR = 0.5
CHOL = np.linalg.cholesky(np.array([[1.0, CORR], [CORR, 1.0]]))


def base_noise(rng, T, N, law):
    """Common random numbers: standard shocks (T, N, d), reused across the dispersion sweep."""
    if law == "LN":
        return rng.standard_normal((T, N, 2)) @ CHOL.T
    if law == "SU":                       # symmetric uniform marginals (Gaussian copula), antithetic
        Z = rng.standard_normal((T, N // 2, 2)) @ CHOL.T
        W = math.sqrt(3.0) * (2.0 * norm.cdf(Z) - 1.0)
        return np.concatenate([W, -W], axis=1)
    raise ValueError(law)


def inputs(xbar, sigma, Z, law):
    """xbar: (d,) or (T, d); Z: (T, N, d); returns X: (T, N, d)."""
    xbar = np.asarray(xbar, float)
    if xbar.ndim == 1:
        xbar = xbar[None, None, :]
    else:
        xbar = xbar[:, None, :]
    if law == "LN":
        return xbar * np.exp(sigma * Z - 0.5 * sigma ** 2)
    return xbar * (1.0 + sigma * Z)


# --------------------------------------------------------------------------- aggregation
def moments(X):
    """X: (T, N, d) -> mean (T,d), covariance (T,d,d), third central moment tensor (T,d,d,d),
    s2 = tr Sigma (T,), m3 = mean ||x_i - xbar||^3 (T,)."""
    N = X.shape[1]
    xb = X.mean(axis=1)
    Hc = X - xb[:, None, :]
    Sig = np.einsum("tni,tnj->tij", Hc, Hc) / N
    mu3 = np.einsum("tni,tnj,tnk->tijk", Hc, Hc, Hc) / N
    s2 = np.einsum("tii->t", Sig)
    m3 = np.mean(np.sum(Hc ** 2, axis=2) ** 1.5, axis=1)
    return xb, Sig, mu3, s2, m3


def boot_median_ci(a, rng, B=1000, level=0.95):
    """Percentile bootstrap interval (over replications) for the median of a."""
    a = np.asarray(a, float)
    n = len(a)
    idx = rng.integers(0, n, size=(B, n))
    meds = np.median(a[idx], axis=1)
    lo, hi = np.quantile(meds, [(1 - level) / 2, 1 - (1 - level) / 2])
    return [float(lo), float(hi)]


def wilson(k, n, z=1.959963984540054):
    """Wilson 95% interval for a proportion with k successes out of n."""
    if n == 0:
        return [0.0, 0.0]
    c = (k + z * z / 2) / (n + z * z)
    h = z / (n + z * z) * math.sqrt(k * (n - k) / n + z * z / 4)
    return [max(0.0, c - h), min(1.0, c + h)]


def aggregate(front, X, cap=None, bounds=True, branch_at_equality="below"):
    """Exact aggregate and its order-1/2/3 moment approximations, per population (T of them).
    cap: capacity c (scalar or (T,)).  At f(xbar) = c (up to a relative tolerance 1e-12) the
    one-sided Hessian convention is fixed explicitly by branch_at_equality ("below", the
    manuscript's convention, or "above"); without the tolerance the branch would be decided by
    floating-point rounding in the symmetric design.  Returns a dict of arrays of length T."""
    T, N, d = X.shape
    xb, Sig, mu3, s2, m3 = moments(X)
    u = front.f(X)                                   # (T, N) individual smooth outputs
    fb = front.f(xb)                                 # (T,)
    Hf = front.hess(xb)
    D3f = front.third(xb)
    Q2f = 0.5 * N * np.einsum("tij,tij->t", Hf, Sig)   # second-order term of the smooth frontier
    out = {"N": N, "xbar": xb, "s2": s2, "m3": m3, "Q2f": Q2f}
    if cap is None:
        Y = u.sum(axis=1)
        Y1 = N * fb
        H, D3 = Hf, D3f
        Tu = np.zeros(T)
        below = np.ones(T, bool)
    else:
        cap = np.broadcast_to(np.asarray(cap, float), (T,))
        Y = np.minimum(u, cap[:, None]).sum(axis=1)
        tol = 1e-12 * cap
        if branch_at_equality == "below":
            below = fb <= cap + tol
        elif branch_at_equality == "above":
            below = fb < cap - tol
        else:
            raise ValueError(branch_at_equality)
        Y1 = N * np.where(below, fb, cap)
        H = Hf * below[:, None, None]
        D3 = D3f * below[:, None, None, None]
        P = np.maximum(u - cap[:, None], 0).sum(axis=1)
        Q = np.maximum(cap[:, None] - u, 0).sum(axis=1)
        Tu = np.minimum(P, Q) / N
        out["frac_above"] = (u > cap[:, None]).mean(axis=1)
    Q2 = 0.5 * N * np.einsum("tij,tij->t", H, Sig)
    Y2 = Y1 + Q2
    Y3 = Y2 + N / 6.0 * np.einsum("tijk,tijk->t", D3, mu3)
    out.update({"Y": Y, "Y1": Y1, "Y2": Y2, "Y3": Y3, "Q2": Q2, "Tu": Tu, "below": below, "fb": fb,
                "E1": Y - Y1, "E2": Y - Y2, "E3": Y - Y3})
    if bounds and hasattr(front, "box_bounds"):
        # global box bound (crude) and segmentwise bound (sup over each segment [xbar, x_i],
        # contained in the coordinate box spanned by xbar and x_i); both are rigorous.
        M2, M3 = front.box_bounds(X.min(axis=1), X.max(axis=1))
        lo = np.minimum(X, xb[:, None, :])
        hi = np.maximum(X, xb[:, None, :])
        M2i, M3i = front.box_bounds(lo, hi)                       # (T, N)
        hn2 = np.sum((X - xb[:, None, :]) ** 2, axis=2)
        out["M2box"], out["M3box"] = M2, M3
        out["B1box"] = 0.5 * N * M2 * s2
        out["B2box"] = N * M3 * m3 / 6.0
        out["B1"] = 0.5 * np.sum(M2i * hn2, axis=1)               # |E1(f)| <= B1 (remainder-bound proposition, (a))
        out["B2"] = np.sum(M3i * hn2 ** 1.5, axis=1) / 6.0        # |E2(f)| <= B2 (remainder-bound proposition, (c))
        # |E2(f_c) + N T_u| <= |E2(f)| + |E1(f)| + |Q2f| 1{f(xbar) > c}   (capacity proposition)
        out["B2cap"] = out["B2"] + out["B1"] + np.abs(Q2f) * (~below)
    return out


def q(a, p):
    return float(np.quantile(a, p))


# --------------------------------------------------------------------------- E1
def run_E1(rng, fast, brng):
    N, R = (2000, 20) if not fast else (1000, 6)
    xbar = np.array([2.0, 1.0])
    grids = {"LN": np.logspace(-2, 0, 17), "SU": np.logspace(-2, math.log10(0.5), 15)}
    fronts = {"CD": CobbDouglas(), "CES": CES()}
    rows = []
    store = {}                                   # per-replication errors at sigma <= 0.05, for exponent SEs
    for fname, front in fronts.items():
        for law, sig_grid in grids.items():
            Z = base_noise(rng, R, N, law)
            for s in sig_grid:
                X = inputs(xbar, s, Z, law)
                A = aggregate(front, X, bounds=(fname == "CD"))
                e1, e2, e3 = (np.abs(A["E1"] / A["Y"]), np.abs(A["E2"] / A["Y"]), np.abs(A["E3"] / A["Y"]))
                if s <= 0.05 + 1e-12:
                    store.setdefault(f"{fname}-{law}", []).append((float(s), e1, e2, e3))
                r21 = np.abs(A["E1"]) / np.abs(A["E2"])
                r32 = np.abs(A["E2"]) / np.abs(A["E3"])
                row = {"frontier": fname, "law": law, "sigma": float(s), "N": N, "reps": R,
                       "e1_med": q(e1, .5), "e1_max": float(e1.max()), "e1_ci": boot_median_ci(e1, brng),
                       "e2_med": q(e2, .5), "e2_max": float(e2.max()), "e2_ci": boot_median_ci(e2, brng),
                       "e3_med": q(e3, .5), "e3_max": float(e3.max()), "e3_ci": boot_median_ci(e3, brng),
                       "r21_min": float(r21.min()), "r21_med": q(r21, .5),
                       "r32_min": float(r32.min()), "r32_med": q(r32, .5),
                       "cv_K": float(np.median(np.sqrt(np.var(X[:, :, 0], axis=1)) / X[:, :, 0].mean(axis=1)))}
                if fname == "CD":
                    row.update({"bound2_rel_med": q(A["B2"] / A["Y"], .5),
                                "bound2box_rel_med": q(A["B2box"] / A["Y"], .5),
                                "bound1_rel_med": q(A["B1"] / A["Y"], .5),
                                "bound2box_holds": int(np.all(np.abs(A["E2"]) <= A["B2box"])),
                                "bound2_holds": int(np.all(np.abs(A["E2"]) <= A["B2"])),
                                "bound1_holds": int(np.all(np.abs(A["E1"]) <= A["B1"])),
                                "ratio_E2_over_B2_med": q(np.abs(A["E2"]) / A["B2"], .5),
                                "ratio_E2_over_B2_max": float(np.max(np.abs(A["E2"]) / A["B2"])),
                                # observable certificate of improvement: 2 B2 < |Q2| in every replication
                                # (then |E2| <= B2 < |Q2| - B2 <= |E1|); Q2 and B2 are functions of the moments
                                "cert_obs_holds_all": int(np.all(2.0 * A["B2"] < np.abs(A["Q2"]))),
                                "cert_obs_frac": float(np.mean(2.0 * A["B2"] < np.abs(A["Q2"])))})
                rows.append(row)
    # small-dispersion exponents from the median curves (least squares on sigma <= 0.05)
    summary = {}
    for fname in fronts:
        for law in grids:
            sel = [r for r in rows if r["frontier"] == fname and r["law"] == law]
            lo = [r for r in sel if r["sigma"] <= 0.05 + 1e-12]
            ls = np.log([r["sigma"] for r in lo])
            slopes = {k: float(np.polyfit(ls, np.log([r[k] for r in lo]), 1)[0]) for k in ("e1_med", "e2_med", "e3_med")}
            # bootstrap standard errors of the exponents: resample replications, recompute the median curve, refit
            st = store[f"{fname}-{law}"]
            Rr = len(st[0][1])
            bs = {1: [], 2: [], 3: []}
            for _ in range(500):
                idx = brng.integers(0, Rr, size=Rr)
                for k in (1, 2, 3):
                    med = [np.median(t[k][idx]) for t in st]
                    bs[k].append(np.polyfit(ls, np.log(med), 1)[0])
            slope_se = {k: float(np.std(bs[k], ddof=1)) for k in (1, 2, 3)}
            # certified-improvement criterion C1: min over reps of |E1|/|E2| >= 5, uniformly in sigma <= sigma*
            ok = [r["sigma"] for r in sel if r["r21_min"] >= 5.0]
            largest_ok = 0.0
            first_fail = None
            for r in sel:                       # largest sigma such that the criterion holds for all smaller sigma
                if r["r21_min"] >= 5.0:
                    largest_ok = r["sigma"]
                else:
                    first_fail = r["sigma"]
                    break
            cert_largest = 0.0
            if fname == "CD":
                for r in sel:                   # largest sigma such that 2 B2 < |Q2| in all reps for all smaller sigma
                    if r["cert_obs_holds_all"]:
                        cert_largest = r["sigma"]
                    else:
                        break
            summary[f"{fname}-{law}"] = {"slope_e1": slopes["e1_med"], "slope_e2": slopes["e2_med"],
                                         "slope_e3": slopes["e3_med"],
                                         "slope_e1_se": slope_se[1], "slope_e2_se": slope_se[2], "slope_e3_se": slope_se[3],
                                         "ci_halfwidth_rel_max": float(max((r[f"e{k}_ci"][1] - r[f"e{k}_ci"][0]) / (2 * r[f"e{k}_med"])
                                                                           for r in sel for k in (1, 2, 3))),
                                         "C1_holds_whole_grid": int(len(ok) == len(sel)),
                                         "C1_largest_sigma_uniform": float(largest_ok),
                                         "C1_first_failing_sigma": first_fail,
                                         "sigma_max_grid": float(sel[-1]["sigma"]),
                                         "r21_min_over_grid": float(min(r["r21_min"] for r in sel)),
                                         "r21_at_sigma_max": float(sel[-1]["r21_min"]),
                                         "r21_min_sigma_le_0p2": float(min(r["r21_min"] for r in sel if r["sigma"] <= 0.2 + 1e-12)),
                                         "r32_min_over_grid": float(min(r["r32_min"] for r in sel)),
                                         "r32_min_sigma_le_0p2": float(min(r["r32_min"] for r in sel if r["sigma"] <= 0.2 + 1e-12)),
                                         "r32_med_below_1_cells": int(sum(r["r32_med"] < 1.0 for r in sel)),
                                         "cells": len(sel),
                                         "bound2_holds_all": (int(all(r["bound2_holds"] for r in sel)) if fname == "CD" else None),
                                         "bound2box_holds_all": (int(all(r["bound2box_holds"] for r in sel)) if fname == "CD" else None),
                                         # v0.1 test (medians, uses the true E1: not observable from moments); kept as a diagnostic only
                                         "sigma_largest_bound2_le_e1_median_nonobservable": (float(max([r["sigma"] for r in sel if r["bound2_rel_med"] < r["e1_med"]] or [0.0])) if fname == "CD" else None),
                                         # observable certificate 2 B2 < |Q2| in every replication (B2)
                                         "sigma_largest_cert_observable": (float(cert_largest) if fname == "CD" else None),
                                         "ratio_E2_over_B2_max": (float(max(r["ratio_E2_over_B2_max"] for r in sel)) if fname == "CD" else None),
                                         "ratio_E2_over_B2_med_min": (float(min(r["ratio_E2_over_B2_med"] for r in sel)) if fname == "CD" else None),
                                         "ratio_B2box_over_B2_max": (float(max(r["bound2box_rel_med"] / r["bound2_rel_med"] for r in sel)) if fname == "CD" else None)}
    return {"rows": rows, "summary": summary, "xbar": xbar.tolist(), "corr": CORR}


def run_E1b(rng, fast):
    """Efficiency terms theta_i ~ U(0.5, 1) independent of inputs: y_i = theta_i f(x_i)."""
    N, R = (2000, 20) if not fast else (1000, 6)
    xbar = np.array([2.0, 1.0])
    front = CobbDouglas()
    Z = base_noise(rng, R, N, "LN")
    theta = rng.uniform(0.5, 1.0, size=(R, N))
    rows = []
    for s in np.logspace(-2, 0, 9):
        X = inputs(xbar, s, Z, "LN")
        A = aggregate(front, X, bounds=False)
        u = front.f(X)
        Yth = (theta * u).sum(axis=1)
        thbar = theta.mean(axis=1)
        e2_theta = np.abs(Yth - thbar * A["Y2"]) / Yth
        e2 = np.abs(A["E2"] / A["Y"])
        cov_term = np.abs(((theta - thbar[:, None]) * u).sum(axis=1)) / Yth
        floor_pred = np.std(theta, axis=1) * np.std(u, axis=1) / (thbar * u.mean(axis=1) * math.sqrt(N))
        cv_u = np.std(u, axis=1) / u.mean(axis=1)
        rows.append({"sigma": float(s), "e2_med": q(e2, .5), "e2_theta_med": q(e2_theta, .5),
                     "cov_term_med": q(cov_term, .5), "floor_pred_med": q(floor_pred, .5), "cv_u_med": q(cv_u, .5),
                     "cov_dominates": int(q(cov_term, .5) > q(e2, .5))})
    summ = {"sd_over_mean_theta": float(np.median(np.std(theta, axis=1) / theta.mean(axis=1))),
            "largest_sigma_cov_dominates": float(max([r["sigma"] for r in rows if r["cov_dominates"]] or [0.0])),
            "ratio_cov_over_e2_smallest_sigma": rows[0]["cov_term_med"] / rows[0]["e2_med"],
            "ratio_cov_over_pred_max": float(max(r["cov_term_med"] / r["floor_pred_med"] for r in rows)),
            "ratio_cov_over_pred_min": float(min(r["cov_term_med"] / r["floor_pred_med"] for r in rows))}
    return {"rows": rows, "N": N, "reps": R, "theta_law": "U(0.5,1)", "summary": summ}


def run_E1c(rng, fast):
    """Finite-N effect on the second-order exponent (Cobb-Douglas, LN): the sample third central
    moment of N units has an O(sigma^3 N^{-1/2}) fluctuation, so at fixed N the fitted exponent of
    |e2| on sigma <= 0.05 lies between 3 (noise) and 4 (population skewness)."""
    Ns = [200, 2000, 20000] if not fast else [200, 2000]
    R = 6
    xbar = np.array([2.0, 1.0])
    front = CobbDouglas()
    grid = [float(s) for s in np.logspace(-2, 0, 17) if s <= 0.05 + 1e-12]
    rows = []
    for N in Ns:
        Z = base_noise(rng, R, N, "LN")
        meds = {1: [], 2: [], 3: []}
        for s in grid:
            A = aggregate(front, inputs(xbar, s, Z, "LN"), bounds=False)
            for k in (1, 2, 3):
                meds[k].append(q(np.abs(A[f"E{k}"] / A["Y"]), .5))
        ls = np.log(grid)
        rows.append({"N": N, "reps": R, "sigma_grid": grid,
                     "slope_e1": float(np.polyfit(ls, np.log(meds[1]), 1)[0]),
                     "slope_e2": float(np.polyfit(ls, np.log(meds[2]), 1)[0]),
                     "slope_e3": float(np.polyfit(ls, np.log(meds[3]), 1)[0])})
    return {"rows": rows}


# --------------------------------------------------------------------------- E2
def run_E2(rng, fast, brng):
    N, R = (2000, 20) if not fast else (1000, 6)
    xbar = np.array([2.0, 1.0])
    front = CobbDouglas()
    fb = float(front.f(xbar))
    deltas = [-0.3, -0.1, -0.03, 0.0, 0.03, 0.1, 0.3]
    sig_grid = np.logspace(-2, 0, 13)
    rows = []
    for law in ("LN", "SU"):
        Z = base_noise(rng, R, N, law)
        grid = sig_grid if law == "LN" else sig_grid[sig_grid <= 0.5]
        for delta in deltas:
            cap = fb / (1.0 + delta)                    # f(xbar) = c (1 + delta)
            for s in grid:
                X = inputs(xbar, s, Z, law)
                Ac = aggregate(front, X, cap=cap)
                As = aggregate(front, X, bounds=False)
                e1, e2 = np.abs(Ac["E1"] / Ac["Y"]), np.abs(Ac["E2"] / Ac["Y"])
                e2s = np.abs(As["E2"] / As["Y"])
                NTu = N * Ac["Tu"]
                two_sided = np.abs(Ac["E2"] + NTu) <= Ac["B2cap"]
                lower = NTu - Ac["B2cap"]
                below = Ac["below"]
                r21 = np.abs(Ac["E1"]) / np.abs(Ac["E2"])
                # exact identity (capacity proposition, eq. (1)): E2(f_c) = -N Tu + E2(f) + Q2 1{f(xbar) > c} - N[(ubar-c)_+ - (f(xbar)-c)_+]
                ubar = As["Y"] / N
                rhs = -NTu + As["E2"] + As["Q2"] * (~below) - N * (np.maximum(ubar - cap, 0) - np.maximum(Ac["fb"] - cap, 0))
                id_gap = float(np.max(np.abs(Ac["E2"] - rhs) / Ac["Y"]))
                # crossing-corollary constant: Tu / (sigma tau_z) with z_i = (x_i - xbar)/sigma, g = grad f(xbar);
                # and the shifted version tau_z(b), b = (f(xbar) - c)/sigma, for designs with f(xbar) != c (LN)
                xb = Ac["xbar"]
                g = front.grad(xb)                                            # (T, d)
                gz = np.einsum("td,tnd->tn", g, (X - xb[:, None, :]) / s)     # (T, N)
                tau_z = 0.5 * np.mean(np.abs(gz), axis=1)
                b = (Ac["fb"] - cap) / s
                tau_zb = np.minimum(np.mean(np.maximum(gz + b[:, None], 0), axis=1), np.mean(np.maximum(-(gz + b[:, None]), 0), axis=1))
                with np.errstate(divide="ignore", invalid="ignore"):
                    tau_ratio = Ac["Tu"] / (s * tau_z)
                    taub_ratio = np.where(tau_zb > 0, Ac["Tu"] / (s * tau_zb), np.nan)
                row = {"law": law, "delta": delta, "sigma": float(s), "cap": cap,
                       "e1_med": q(e1, .5), "e2_med": q(e2, .5), "e2_smooth_med": q(e2s, .5),
                       "e1_ci": boot_median_ci(e1, brng), "e2_ci": boot_median_ci(e2, brng),
                       "r21_min": float(np.min(r21)),
                       "r21_med": q(r21, .5),
                       "r21_min_below_branch": (float(np.min(r21[below])) if np.any(below) else None),
                       "r21_min_above_branch": (float(np.min(r21[~below])) if np.any(~below) else None),
                       "frac_reps_mean_above": float(np.mean(~below)),
                       "fxbar_minus_c_rel_med": q(np.abs(Ac["fb"] - cap) / cap, .5),
                       "fxbar_minus_c_rel_max": float(np.max(np.abs(Ac["fb"] - cap) / cap)),
                       "NTu_rel_med": q(NTu / Ac["Y"], .5),
                       "E2_over_minusNTu_med": (float(np.nanmedian(-Ac["E2"] / np.where(NTu > 0, NTu, np.nan))) if np.any(NTu > 0) else None),
                       "Tu_over_sigma_tau_med": q(tau_ratio, .5),
                       "Tu_over_sigma_tau_ci": boot_median_ci(tau_ratio, brng),
                       "Tu_over_sigma_taub_med": (float(np.nanmedian(taub_ratio)) if np.any(np.isfinite(taub_ratio)) else None),
                       "identity_rel_gap_max": id_gap,
                       "two_sided_bound_holds": int(np.all(two_sided)),
                       "lower_bound_informative": int(np.all(lower > 0)),
                       "frac_above_med": q(Ac["frac_above"], .5),
                       "crossing_all_reps": int(np.all((Ac["frac_above"] > 0) & (Ac["frac_above"] < 1)))}
                if delta == 0.0:                 # alternative convention at f(xbar) = c: "above" branch (Y2 = Y1 there)
                    Aa = aggregate(front, X, cap=cap, bounds=False, branch_at_equality="above")
                    row["r21_min_alt_branch_above"] = float(np.min(np.abs(Aa["E1"]) / np.abs(Aa["E2"])))
                    row["frac_reps_mean_above_alt"] = float(np.mean(~Aa["below"]))
                rows.append(row)
    # exponents at delta = 0 and delta = -0.3 (LN), sigma <= 0.05
    summ = {}
    for law in ("LN", "SU"):
        for delta in (0.0, -0.3, -0.03):
            sel = [r for r in rows if r["law"] == law and r["delta"] == delta and r["sigma"] <= 0.05 + 1e-12]
            ls = np.log([r["sigma"] for r in sel])
            summ[f"{law}-delta{delta}"] = {
                "slope_e2_capped": float(np.polyfit(ls, np.log([r["e2_med"] for r in sel]), 1)[0]),
                "slope_e2_smooth": float(np.polyfit(ls, np.log([r["e2_smooth_med"] for r in sel]), 1)[0]),
                "r21_min": float(min(r["r21_min"] for r in [x for x in rows if x["law"] == law and x["delta"] == delta])),
                "r21_min_small_sigma": float(min(r["r21_min"] for r in sel))}
    summ["two_sided_bound_holds_all"] = int(all(r["two_sided_bound_holds"] for r in rows))
    summ["n_cells"] = len(rows)
    inf = [r for r in rows if r["lower_bound_informative"]]
    summ["n_cells_lower_bound_informative"] = len(inf)
    summ["crossing_cells"] = len([r for r in rows if r["crossing_all_reps"]])
    d0 = [r for r in rows if r["law"] == "LN" and r["delta"] == 0.0]
    summ["LN_delta0_ratio_range"] = [min(r["E2_over_minusNTu_med"] for r in d0), max(r["E2_over_minusNTu_med"] for r in d0)]
    summ["LN_delta0_ratio_smallest_sigma"] = d0[0]["E2_over_minusNTu_med"]
    summ["LN_delta0_e2_smallest_sigma"] = d0[0]["e2_med"]
    summ["LN_delta0_e2smooth_smallest_sigma"] = d0[0]["e2_smooth_med"]
    summ["LN_delta0_amplification_smallest_sigma"] = d0[0]["e2_med"] / d0[0]["e2_smooth_med"]
    summ["LN_delta0_r21_smallest_sigma"] = d0[0]["r21_med"]
    summ["LN_delta0_r21_min_below_smallest_sigma"] = d0[0]["r21_min_below_branch"]
    summ["LN_delta0_frac_reps_mean_above_range"] = [min(r["frac_reps_mean_above"] for r in d0), max(r["frac_reps_mean_above"] for r in d0)]
    summ["LN_delta0_fxbar_minus_c_rel_max"] = max(r["fxbar_minus_c_rel_max"] for r in d0)
    summ["LN_delta0_lower_informative_largest_sigma"] = float(max([r["sigma"] for r in d0 if r["lower_bound_informative"]] or [0.0]))
    s0 = [r for r in rows if r["law"] == "SU" and r["delta"] == 0.0]
    summ["SU_delta0_r21_min_below_smallest_sigma"] = s0[0]["r21_min_below_branch"]
    summ["SU_delta0_frac_reps_mean_above_range"] = [min(r["frac_reps_mean_above"] for r in s0), max(r["frac_reps_mean_above"] for r in s0)]
    summ["SU_delta0_r21_min_alt_branch_above"] = float(min(r["r21_min_alt_branch_above"] for r in s0))
    summ["SU_delta0_frac_reps_mean_above_alt_range"] = [min(r["frac_reps_mean_above_alt"] for r in s0), max(r["frac_reps_mean_above_alt"] for r in s0)]
    summ["SU_delta0_tau_ratio_smallest_sigma"] = s0[0]["Tu_over_sigma_tau_med"]
    summ["SU_delta0_tau_ratio_smallest_sigma_ci"] = s0[0]["Tu_over_sigma_tau_ci"]
    summ["LN_delta0_tau_ratio_smallest_sigma"] = d0[0]["Tu_over_sigma_tau_med"]
    summ["LN_delta0_taub_ratio_smallest_sigma"] = d0[0]["Tu_over_sigma_taub_med"]
    summ["tau_ratio_delta0"] = {law: [[r["sigma"], r["Tu_over_sigma_tau_med"], r["Tu_over_sigma_taub_med"]] for r in rows if r["law"] == law and r["delta"] == 0.0] for law in ("LN", "SU")}
    summ["identity_rel_gap_max"] = float(max(r["identity_rel_gap_max"] for r in rows))
    summ["sigma_min"] = float(sig_grid[0])
    return {"rows": rows, "summary": summ, "N": N, "reps": R, "deltas": deltas, "f_xbar": fb}


# --------------------------------------------------------------------------- E3
def run_E3(rng, fast, brng):
    G, n, R = (40, 50, 20) if not fast else (20, 50, 6)
    N = G * n
    xbar = np.array([2.0, 1.0])
    front = CobbDouglas()
    grid = [0.05, 0.1, 0.2, 0.4]
    ZB = rng.standard_normal((R, G, 2)) @ CHOL.T              # between-firm shocks
    ZW = rng.standard_normal((R, G, n, 2)) @ CHOL.T           # within-firm shocks
    rows = []
    lemma_gap = 0.0
    for sB in grid:
        for sW in grid:
            for capped in (False, True):
                mB = xbar * np.exp(sB * ZB - 0.5 * sB ** 2)                  # (R, G, d) firm means
                X = mB[:, :, None, :] * np.exp(sW * ZW - 0.5 * sW ** 2)     # (R, G, n, d)
                Xflat = X.reshape(R, N, 2)
                cap = None
                if capped:
                    cap = float(front.f(xbar))                                # sector-level capacity
                pooled = aggregate(front, Xflat, cap=cap)
                firm = aggregate(front, X.reshape(R * G, n, 2), cap=cap)
                for k in ("Y", "Y1", "Y2", "E1", "E2", "B2", "Tu"):
                    firm[k] = firm[k].reshape(R, G)
                Y = pooled["Y"]
                hier1 = firm["Y1"].sum(axis=1)
                hier2 = firm["Y2"].sum(axis=1)
                assert np.allclose(firm["Y"].sum(axis=1), Y)
                # Lemma: top-down two-stage second order == pooled second order (smooth case)
                if not capped:
                    xb_f = firm["xbar"].reshape(R, G, 2)
                    xb = pooled["xbar"]
                    SigB = np.einsum("rgi,rgj->rij", xb_f - xb[:, None, :], xb_f - xb[:, None, :]) / G
                    _, SigW_all, _, _, _ = moments(X.reshape(R * G, n, 2))
                    SigW = SigW_all.reshape(R, G, 2, 2).mean(axis=1)
                    Hb = front.hess(xb)
                    topdown = N * (front.f(xb) + 0.5 * np.einsum("rij,rij->r", Hb, SigB + SigW))
                    lemma_gap = max(lemma_gap, float(np.max(np.abs(topdown - pooled["Y2"]) / Y)))
                row = {"sigma_B": sB, "sigma_W": sW, "capped": int(capped),
                       "pooled1_med": q(np.abs(pooled["E1"] / Y), .5), "pooled2_med": q(np.abs(pooled["E2"] / Y), .5),
                       "pooled2_ci": boot_median_ci(np.abs(pooled["E2"] / Y), brng), "hier2_ci": boot_median_ci(np.abs((Y - hier2) / Y), brng),
                       "hier1_med": q(np.abs((Y - hier1) / Y), .5), "hier2_med": q(np.abs((Y - hier2) / Y), .5),
                       "pooled2_max": float(np.max(np.abs(pooled["E2"] / Y))), "hier2_max": float(np.max(np.abs((Y - hier2) / Y))),
                       "gain_hier_over_pooled_med": q(np.abs(pooled["E2"]) / np.abs(Y - hier2), .5)}
                if not capped:
                    row.update({"bound_pooled_rel_med": q(pooled["B2"] / Y, .5),
                                "bound_hier_rel_med": q(firm["B2"].sum(axis=1) / Y, .5),
                                "bound_hier_holds": int(np.all(np.abs(Y - hier2) <= firm["B2"].sum(axis=1))),
                                "bound_pooled_holds": int(np.all(np.abs(pooled["E2"]) <= pooled["B2"]))})
                else:
                    strad = ((firm["Tu"] > 0)).mean(axis=1)
                    row.update({"frac_firms_straddling_med": q(strad, .5),
                                "NTu_pooled_rel_med": q(N * pooled["Tu"] / Y, .5),
                                "sum_nTu_firms_rel_med": q(n * firm["Tu"].sum(axis=1) / Y, .5),
                                "share_hier_error_from_nonstraddling_max": float(np.max(
                                    np.abs((firm["E2"] * (firm["Tu"] == 0)).sum(axis=1)) / np.abs(firm["E2"].sum(axis=1))))})
                rows.append(row)
    sm = [r for r in rows if not r["capped"]]
    summ = {"lemma_topdown_equals_pooled_max_rel_gap": lemma_gap,
            "smooth_hier2_better_cells": int(sum(r["hier2_med"] < r["pooled2_med"] for r in sm)),
            "smooth_cells": len(sm),
            "smooth_bounds_hold_all": int(all(r["bound_hier_holds"] and r["bound_pooled_holds"] for r in sm)),
            "smooth_gain_min": float(min(r["gain_hier_over_pooled_med"] for r in sm)),
            "smooth_gain_max": float(max(r["gain_hier_over_pooled_med"] for r in sm)),
            "G": G, "n": n, "N": N, "reps": R}
    cp = [r for r in rows if r["capped"]]
    summ["capped_hier2_over_pooled2_min"] = float(min(r["hier2_med"] / r["pooled2_med"] for r in cp))
    summ["capped_hier2_over_pooled2_max"] = float(max(r["hier2_med"] / r["pooled2_med"] for r in cp))
    summ["capped_share_from_nonstraddling_max"] = float(max(r["share_hier_error_from_nonstraddling_max"] for r in cp))
    summ["capped_frac_firms_straddling_min"] = float(min(r["frac_firms_straddling_med"] for r in cp))
    summ["capped_frac_firms_straddling_max"] = float(max(r["frac_firms_straddling_med"] for r in cp))
    return {"rows": rows, "summary": summ}


# --------------------------------------------------------------------------- E4
def run_E4(rng, fast):
    N, trials = (500, 1000) if not fast else (500, 200)
    xbarA = np.array([2.0, 1.0])
    front = CobbDouglas()
    deg = float(front.al.sum())
    fA = float(front.f(xbarA))
    sig_grid = [0.02, 0.05, 0.1, 0.2, 0.4, 0.8]
    prox = [None, 0.5, 0.2, 0.1, 0.05, 0.0]
    gmax = 0.05
    rows = []
    for s in sig_grid:
        ZA = base_noise(rng, trials, N, "LN")
        ZB = base_noise(rng, trials, N, "LN")
        gamma = rng.uniform(-gmax, gmax, size=trials)
        xbarB = xbarA[None, :] * (1.0 + gamma)[:, None] ** (1.0 / deg)   # f(xbarB) = (1+gamma) f(xbarA)
        XA = inputs(xbarA, s, ZA, "LN")
        XB = inputs(xbarB, s / 2.0, ZB, "LN")
        for p in prox:
            cap = None if p is None else fA * (1.0 + p)
            A = aggregate(front, XA, cap=cap)
            B = aggregate(front, XB, cap=cap)
            true = np.sign(A["Y"] - B["Y"])
            row = {"sigma": s, "prox": (p if p is not None else "none"), "trials": trials,
                   "fracA_mean_below_cap": float(np.mean(A["below"])), "fracB_mean_below_cap": float(np.mean(B["below"]))}
            for k in (1, 2, 3):
                appr = np.sign(A[f"Y{k}"] - B[f"Y{k}"])
                nrev = int(np.sum(appr != true))
                row[f"rev{k}"] = nrev / trials
                row[f"rev{k}_ci"] = wilson(nrev, trials)            # Wilson 95% interval
            if p is None:
                margin = np.abs(A["Y2"] - B["Y2"]) > (A["B2"] + B["B2"])
                row["certified_frac"] = float(margin.mean())
                row["certified_reversals"] = int(np.sum(margin & (np.sign(A["Y2"] - B["Y2"]) != true)))
                margin1 = np.abs(A["Y1"] - B["Y1"]) > (A["B1"] + B["B1"])
                row["certified1_frac"] = float(margin1.mean())
                row["certified1_reversals"] = int(np.sum(margin1 & (np.sign(A["Y1"] - B["Y1"]) != true)))
            rows.append(row)
    # criterion C2: in every cell with rev1 >= 2%, rev2 <= rev1 / 5
    elig = [r for r in rows if r["rev1"] >= 0.02]
    fail = [r for r in elig if r["rev2"] > r["rev1"] / 5.0]
    # robustness of the per-cell verdict with Wilson intervals: clear failure if the lower limit of rev2 exceeds the
    # upper limit of rev1/5; clear pass if the upper limit of rev2 is below the lower limit of rev1/5; else borderline
    def verdict(r):
        if r["rev2_ci"][0] > r["rev1_ci"][1] / 5.0:
            return "fail"
        if r["rev2_ci"][1] < r["rev1_ci"][0] / 5.0:
            return "pass"
        return "borderline"
    for r in elig:
        r["C2_verdict"] = verdict(r)
    cell = lambda r: [r["prox"], r["sigma"]]
    summ = {"C2_eligible_cells": len(elig), "C2_failing_cells": len(fail),
            "C2_passing_cells": [cell(r) for r in elig if r not in fail],
            "C2_fail_clear_cells": [cell(r) for r in elig if r["C2_verdict"] == "fail"],
            "C2_borderline_cells": [cell(r) for r in elig if r["C2_verdict"] == "borderline"],
            "C2_pass_clear_cells": [cell(r) for r in elig if r["C2_verdict"] == "pass"],
            "C2_fail_clear_capped": len([r for r in elig if r["C2_verdict"] == "fail" and r["prox"] != "none"]),
            "C2_borderline_capped": len([r for r in elig if r["C2_verdict"] == "borderline" and r["prox"] != "none"]),
            "C2_borderline_smooth": len([r for r in elig if r["C2_verdict"] == "borderline" and r["prox"] == "none"]),
            "C2_pass_clear_capped": len([r for r in elig if r["C2_verdict"] == "pass" and r["prox"] != "none"]),
            "C2_pass_clear_smooth": len([r for r in elig if r["C2_verdict"] == "pass" and r["prox"] == "none"]),
            "C2_eligible_smooth_cells": len([r for r in elig if r["prox"] == "none"]),
            "C2_eligible_capped_cells": len([r for r in elig if r["prox"] != "none"]),
            "C2_failing_smooth_cells": len([r for r in fail if r["prox"] == "none"]),
            "C2_failing_capped_cells": len([r for r in fail if r["prox"] != "none"]),
            "C2_holds": int(len(fail) == 0),
            "certified_reversals_total": int(sum(r["certified_reversals"] for r in rows if r["prox"] == "none")),
            "certified1_reversals_total": int(sum(r["certified1_reversals"] for r in rows if r["prox"] == "none")),
            "certified_frac_min": float(min(r["certified_frac"] for r in rows if r["prox"] == "none")),
            "certified_frac_max": float(max(r["certified_frac"] for r in rows if r["prox"] == "none")),
            "smooth_rev1_max": float(max(r["rev1"] for r in rows if r["prox"] == "none")),
            "smooth_rev2_max": float(max(r["rev2"] for r in rows if r["prox"] == "none")),
            "capped0_rev1_max": float(max(r["rev1"] for r in rows if r["prox"] == 0.0)),
            "capped0_rev2_max": float(max(r["rev2"] for r in rows if r["prox"] == 0.0)),
            "capped0_rev2_min": float(min(r["rev2"] for r in rows if r["prox"] == 0.0)),
            "N": N, "trials": trials, "gamma_max": gmax}
    return {"rows": rows, "summary": summ}


# --------------------------------------------------------------------------- E5
def run_E5(rng, fast):
    """Scalar calibration Yhat = Y1 + lambda * Q2 fitted by least squares on a training design,
    global and per proximity regime, evaluated out of sample (new seeds, off-grid sigma, and the
    symmetric law).  Criterion C1 (factor >= 5 over order 1, uniformly, min over reps)."""
    N, R = (2000, 10) if not fast else (1000, 4)
    xbar = np.array([2.0, 1.0])
    front = CobbDouglas()
    fb = float(front.f(xbar))
    regimes = {"smooth": None, "below": -0.1, "at": 0.0, "above": 0.1}
    train_sig = [0.05, 0.1, 0.2, 0.4]
    test_sig = [0.03, 0.07, 0.15, 0.3, 0.6]

    def design(sigmas, law, Rr):
        Z = base_noise(rng, Rr, N, law)
        recs = []
        for reg, delta in regimes.items():
            cap = None if delta is None else fb / (1.0 + delta)
            for s in sigmas:
                X = inputs(xbar, s, Z, law)
                A = aggregate(front, X, cap=cap, bounds=False)
                recs.append({"regime": reg, "sigma": s, "law": law, "E1": A["E1"], "Q2": A["Q2"], "Y": A["Y"], "below": A["below"]})
        return recs

    train = design(train_sig, "LN", R)
    # least squares lambda: minimise sum (E1 - lambda Q2)^2
    def fit(recs):
        num = sum(float(np.sum(r["E1"] * r["Q2"])) for r in recs)
        den = sum(float(np.sum(r["Q2"] ** 2)) for r in recs)
        return num / den if den > 0 else None      # None: Q2 == 0 identically (above capacity)
    lam_global = fit(train)
    lam_reg = {reg: fit([r for r in train if r["regime"] == reg]) for reg in regimes}
    lam_reg_eval = {k: (v if v is not None else 1.0) for k, v in lam_reg.items()}
    results = {"lambda_global": lam_global, "lambda_regime": lam_reg, "N": N, "reps": R,
               "regimes_with_Q2_identically_zero": [k for k, v in lam_reg.items() if v is None],
               "train_sigma": train_sig, "test_sigma": test_sig, "rows": []}
    for law in ("LN", "SU"):
        test = design([s for s in test_sig if law == "LN" or s <= 0.5], law, R)
        for r in test:
            e1 = np.abs(r["E1"])
            below = r["below"]
            row = {"law": law, "regime": r["regime"], "sigma": r["sigma"],
                   "e1_med": q(e1 / r["Y"], .5), "frac_reps_mean_above": float(np.mean(~below))}
            for name, lam in (("order2", 1.0), ("global", lam_global), ("regime", lam_reg_eval[r["regime"]])):
                e = np.abs(r["E1"] - lam * r["Q2"])
                row[f"{name}_med"] = q(e / r["Y"], .5)
                row[f"{name}_ratio_min"] = float(np.min(e1 / e))
                # restricted to replications in the "below" branch (in the "above" branch Q2 = 0 and the ratio is 1 by construction)
                row[f"{name}_ratio_min_below"] = (float(np.min((e1 / e)[below])) if np.any(below) else None)
            results["rows"].append(row)
    summ = {}
    for name in ("order2", "global", "regime"):
        for law in ("LN", "SU"):
            for reg in regimes:
                sel = [r for r in results["rows"] if r["law"] == law and r["regime"] == reg]
                summ[f"{name}-{law}-{reg}"] = float(min(r[f"{name}_ratio_min"] for r in sel))
            sel = [r for r in results["rows"] if r["law"] == law and r["regime"] == "at"]
            vals = [r[f"{name}_ratio_min_below"] for r in sel if r[f"{name}_ratio_min_below"] is not None]
            summ[f"{name}-{law}-at-below"] = (float(min(vals)) if vals else None)
            summ[f"{name}-{law}-at-frac-above"] = [min(r["frac_reps_mean_above"] for r in sel), max(r["frac_reps_mean_above"] for r in sel)]
        # "above" is excluded from the C1 verdict: Q2 == 0 there, nothing to recalibrate (and e1 = 0 when no unit crosses)
        summ[f"{name}-C1-holds-excl-above"] = int(all(summ[f"{name}-{law}-{reg}"] >= 5.0 for law in ("LN", "SU") for reg in ("smooth", "below", "at")))
        summ[f"{name}-C1-holds-all"] = int(all(summ[f"{name}-{law}-{reg}"] >= 5.0 for law in ("LN", "SU") for reg in regimes))
        summ[f"{name}-C1-holds-smooth"] = int(all(summ[f"{name}-{law}-smooth"] >= 5.0 for law in ("LN", "SU")))
        summ[f"{name}-C1-fails-threshold"] = int(any(summ[f"{name}-{law}-{reg}"] < 5.0 for law in ("LN", "SU") for reg in ("below", "at", "above")))
    results["summary"] = summ
    return results


# --------------------------------------------------------------------------- E6
def run_E6():
    """Closed-form examples used in the manuscript (margin-condition section, reversal example)."""
    out = {}
    # kinked frontier min(x, 1): A all at 1 - eps, B half at 1 - s, half at 1 + s (mean 1)
    eps, s = 0.05, 0.2
    out["kink"] = {"eps": eps, "sigma": s, "YA_per_unit": 1 - eps, "YB_per_unit": 1 - s / 2,
                   "YB_approx_per_unit_all_orders": 1.0, "truth_A_gt_B": bool(1 - eps > 1 - s / 2),
                   "approx_B_gt_A": True, "reversal": bool((1 - eps > 1 - s / 2))}
    # smooth frontier sqrt(x): A all at 1; B half at 1+d+s, half at 1+d-s
    d, s2 = 0.01, 0.3
    YB = 0.5 * (math.sqrt(1 + d + s2) + math.sqrt(1 + d - s2))
    Y1B = math.sqrt(1 + d)
    Y2B = Y1B - 0.125 * (1 + d) ** (-1.5) * s2 ** 2
    out["sqrt"] = {"delta": d, "sigma": s2, "YA": 1.0, "YB": YB, "Y1B": Y1B, "Y2B": Y2B,
                   "order1_reversal": bool((Y1B > 1.0) != (YB > 1.0)), "order2_reversal": bool((Y2B > 1.0) != (YB > 1.0))}
    return out


# --------------------------------------------------------------------------- figures
def fig_E1(E1):
    """Cobb-Douglas panels only (the CES curves are visually identical up to the constants; Table 1 has their numbers)."""
    fig, axes = plt.subplots(1, 2, figsize=(7.2, 2.9), sharey=True)
    for ax, key in zip(axes.ravel(), ("CD-LN", "CD-SU")):
        fname, law = key.split("-")
        sel = [r for r in E1["rows"] if r["frontier"] == fname and r["law"] == law]
        sg = [r["sigma"] for r in sel]
        ax.loglog(sg, [r["e1_med"] for r in sel], color=C1, marker="o", ms=3, label="order 1 (representative unit)")
        ax.loglog(sg, [r["e2_med"] for r in sel], color=C2, marker="s", ms=3, label="order 2 (Hessian $\\cdot$ covariance)")
        ax.loglog(sg, [r["e3_med"] for r in sel], color=C3, marker="^", ms=3, label="order 3")
        if fname == "CD":
            ax.loglog(sg, [r["bound2_rel_med"] for r in sel], color=CB, ls="--", label="certified bound $B_2/Y$ on order 2")
        ax.set_title(f"{'Cobb–Douglas' if fname == 'CD' else 'CES'} frontier, {'log-normal' if law == 'LN' else 'symmetric'} inputs", fontsize=9)
        ax.set_xlabel("dispersion $\\sigma$")
        ax.set_ylim(1e-13, 3)
    axes[0].set_ylabel("median relative aggregation error")
    h, l = axes[0].get_legend_handles_labels()
    fig.legend(h, l, loc="lower center", ncol=4, fontsize=7, bbox_to_anchor=(0.5, -0.02))
    fig.tight_layout(rect=(0, 0.08, 1, 1))
    for ext in ("png", "pdf"):
        fig.savefig(os.path.join(FIG, f"dispersion_sweep.{ext}"), bbox_inches="tight")
    plt.close(fig)


def fig_E2E3(E2, E3):
    """One 2x2 figure: top row E2 (capacity threshold), bottom row E3 (hierarchy)."""
    fig, axes = plt.subplots(2, 2, figsize=(7.2, 5.4))
    ax = axes[0, 0]
    cols = {-0.3: "#c6dbef", -0.1: "#6baed6", -0.03: "#2171b5", 0.0: "#08306b"}
    for delta, col in cols.items():
        sel = [r for r in E2["rows"] if r["law"] == "LN" and r["delta"] == delta]
        ax.loglog([r["sigma"] for r in sel], [r["e2_med"] for r in sel], color=col, marker="o", ms=3,
                  label=f"capacity, $\\delta={delta:+.2f}$")
    sel = [r for r in E2["rows"] if r["law"] == "LN" and r["delta"] == 0.0]
    ax.loglog([r["sigma"] for r in sel], [r["e2_smooth_med"] for r in sel], color=CR, ls="--", label="no capacity (smooth)")
    ax.set_xlabel("dispersion $\\sigma$")
    ax.set_ylabel("median $|E_2|/Y$ (order 2)")
    ax.set_title("E2: second-order error at a capacity threshold", fontsize=9)
    ax.legend(fontsize=7)
    ax = axes[0, 1]
    for delta, col in cols.items():
        sel = [r for r in E2["rows"] if r["law"] == "LN" and r["delta"] == delta and r["E2_over_minusNTu_med"] is not None]
        ax.semilogx([r["sigma"] for r in sel], [r["E2_over_minusNTu_med"] for r in sel], color=col, marker="o", ms=3,
                    label=f"$\\delta={delta:+.2f}$")
    ax.axhline(1.0, color=CR, ls="--", lw=1)
    ax.set_xlabel("dispersion $\\sigma$")
    ax.set_ylabel("$-E_2 / (N\\,T_u)$")
    ax.set_ylim(-0.6, 1.6)                 # one point of delta = -0.30 (sigma ~ 0.15) lies below: N Tu is then smaller than E2(f); said in the caption
    ax.set_title("E2: error against the crossing term $N T_u$", fontsize=9)
    ax.legend(fontsize=7)
    grid = sorted({r["sigma_B"] for r in E3["rows"]})
    shades = ["#c6dbef", "#6baed6", "#2171b5", "#08306b"]
    axes[1, 1].sharey(axes[1, 0])
    for ax, capped in zip(axes[1], (0, 1)):
        for sB, col in zip(grid, shades):
            sel = [r for r in E3["rows"] if r["capped"] == capped and r["sigma_B"] == sB]
            ax.loglog([r["sigma_W"] for r in sel], [r["pooled2_med"] for r in sel], color=col, marker="o", ms=3, ls="-",
                      label=f"pooled, $\\sigma_B={sB}$")
            ax.loglog([r["sigma_W"] for r in sel], [r["hier2_med"] for r in sel], color=col, marker="s", ms=3, ls=":",
                      label=f"bottom-up, $\\sigma_B={sB}$")
        ax.set_xlabel("within-firm dispersion $\\sigma_W$")
        ax.set_title("E3: smooth frontier" if not capped else "E3: capacity at the sector mean output", fontsize=9)
        ax.set_xticks(grid)
        ax.set_xticklabels([str(g) for g in grid])
        ax.xaxis.set_minor_formatter(matplotlib.ticker.NullFormatter())
    axes[1, 0].set_ylabel("median $|E_2|/Y$")
    h, l = axes[1, 1].get_legend_handles_labels()
    fig.legend(h, l, loc="lower center", ncol=4, fontsize=7, bbox_to_anchor=(0.5, -0.01))
    fig.tight_layout(rect=(0, 0.06, 1, 1))
    for ext in ("png", "pdf"):
        fig.savefig(os.path.join(FIG, f"threshold_hierarchy.{ext}"), bbox_inches="tight")
    plt.close(fig)


def fig_E4(E4):
    prox = ["none", 0.1, 0.0]
    fig, axes = plt.subplots(1, 3, figsize=(7.2, 2.6), sharex=True, sharey=True)
    axes = np.array([axes])
    for ax, p in zip(axes.ravel(), prox):
        sel = [r for r in E4["rows"] if r["prox"] == p]
        sg = [r["sigma"] for r in sel]
        ax.semilogx(sg, [100 * r["rev1"] for r in sel], color=C1, marker="o", ms=3, label="order 1")
        ax.semilogx(sg, [100 * r["rev2"] for r in sel], color=C2, marker="s", ms=3, label="order 2")
        ax.semilogx(sg, [100 * r["rev3"] for r in sel], color=C3, marker="^", ms=3, label="order 3")
        ax.set_title("no capacity" if p == "none" else f"capacity at $+{100*p:.0f}\\%$ of mean output", fontsize=8)
    sg_all = sorted({r["sigma"] for r in E4["rows"]})
    for ax in axes.ravel():
        ax.set_xticks(sg_all)
        ax.set_xticklabels([str(v) for v in sg_all])
        ax.xaxis.set_minor_formatter(matplotlib.ticker.NullFormatter())
    for ax in axes[-1]:
        ax.set_xlabel("dispersion $\\sigma$ (sector A; B has $\\sigma/2$)")
    for ax in axes[:, 0]:
        ax.set_ylabel("rank reversals (%)")
    axes[0, 0].legend(fontsize=7)
    fig.tight_layout()
    for ext in ("png", "pdf"):
        fig.savefig(os.path.join(FIG, f"decision.{ext}"), bbox_inches="tight")
    plt.close(fig)


# --------------------------------------------------------------------------- tables
def write_tables(res):
    L = ["# SGE001 tables (generated by experiments/frontier_aggregation.py)", "",
         f"seed = {res['meta']['seed']}; fast = {res['meta']['fast']}; runtime = {res['meta']['seconds']:.1f} s", ""]
    L += ["## E0 derivative self-test (max relative deviation from central differences)", ""]
    for k, v in res["E0"].items():
        L.append(f"- {k}: grad {v['grad']:.1e}, hess {v['hess']:.1e}, third {v['third']:.1e}")
    L += ["", "## E1 dispersion sweep (median relative errors over reps with bootstrap 95% CI; r21 = |E1|/|E2| min over reps; cert = all reps satisfy 2 B2 < |Q2|)", "",
          "| frontier | law | sigma | e1 | e2 | e2 CI | e3 | r21 min | r32 min | bound2 (rel) | E2/B2 max | cert |", "|---|---|---|---|---|---|---|---|---|---|---|---|"]
    for r in res["E1"]["rows"]:
        L.append(f"| {r['frontier']} | {r['law']} | {r['sigma']:.3g} | {r['e1_med']:.2e} | {r['e2_med']:.2e} | [{r['e2_ci'][0]:.2e}, {r['e2_ci'][1]:.2e}] | {r['e3_med']:.2e} | "
                 f"{r['r21_min']:.1f} | {r['r32_min']:.1f} | {r.get('bound2_rel_med', float('nan')):.2e} | {r.get('ratio_E2_over_B2_max', float('nan')):.3f} | {r.get('cert_obs_holds_all', '--')} |")
    L += ["", "### E1 summary", ""]
    for k, v in res["E1"]["summary"].items():
        L.append(f"- {k}: " + ", ".join(f"{a}={b:.3g}" if isinstance(b, float) else f"{a}={b}" for a, b in v.items()))
    L += ["", "## E1b efficiency terms", "", "| sigma | e2 (no theta) | e2 (with theta) | covariance term | predicted floor |", "|---|---|---|---|---|"]
    for r in res["E1b"]["rows"]:
        L.append(f"| {r['sigma']:.3g} | {r['e2_med']:.2e} | {r['e2_theta_med']:.2e} | {r['cov_term_med']:.2e} | {r['floor_pred_med']:.2e} |")
    L += ["", "### E1b summary", ""] + [f"- {k}: {v}" for k, v in res["E1b"]["summary"].items()]
    L += ["", "## E1c finite-N effect on the exponents (CD, LN, 6 reps, fit on sigma <= 0.05)", "", "| N | slope e1 | slope e2 | slope e3 |", "|---|---|---|---|"]
    for r in res["E1c"]["rows"]:
        L.append(f"| {r['N']} | {r['slope_e1']:.2f} | {r['slope_e2']:.2f} | {r['slope_e3']:.2f} |")
    L += ["", "## E2 capacity threshold (both laws; 'below branch' = min ratio over reps with f(xbar) <= c; tau = Tu/(sigma tau_z); tau(b) = shifted version)", "",
          "| law | delta | sigma | e1 | e2 capped | e2 CI | e2 smooth | r21 min | r21 min below | reps mean above | N Tu / Y | -E2/(N Tu) | tau | tau(b) | two-sided bound | lower informative | frac above |",
          "|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|"]
    fmt = lambda v, f="%.3f": (f % v) if v is not None else "--"
    for r in res["E2"]["rows"]:
        L.append(f"| {r['law']} | {r['delta']:+.2f} | {r['sigma']:.3g} | {r['e1_med']:.2e} | {r['e2_med']:.2e} | [{r['e2_ci'][0]:.2e}, {r['e2_ci'][1]:.2e}] | {r['e2_smooth_med']:.2e} | {r['r21_min']:.3f} | "
                 f"{fmt(r['r21_min_below_branch'])} | {r['frac_reps_mean_above']:.2f} | {r['NTu_rel_med']:.2e} | {fmt(r['E2_over_minusNTu_med'])} | {fmt(r['Tu_over_sigma_tau_med'])} | {fmt(r['Tu_over_sigma_taub_med'])} | "
                 f"{r['two_sided_bound_holds']} | {r['lower_bound_informative']} | {r['frac_above_med']:.3f} |")
    L += ["", "### E2 summary", ""]
    for k, v in res["E2"]["summary"].items():
        L.append(f"- {k}: {v}")
    L += ["", "## E3 hierarchy (median relative errors, bootstrap 95% CI for the second-order medians)", "", "| capped | sigma_B | sigma_W | pooled1 | pooled2 | pooled2 CI | bottom-up1 | bottom-up2 | bottom-up2 CI | gain (pooled2/bu2) | straddling firms |", "|---|---|---|---|---|---|---|---|---|---|---|"]
    for r in res["E3"]["rows"]:
        L.append(f"| {r['capped']} | {r['sigma_B']} | {r['sigma_W']} | {r['pooled1_med']:.2e} | {r['pooled2_med']:.2e} | [{r['pooled2_ci'][0]:.2e}, {r['pooled2_ci'][1]:.2e}] | {r['hier1_med']:.2e} | {r['hier2_med']:.2e} | "
                 f"[{r['hier2_ci'][0]:.2e}, {r['hier2_ci'][1]:.2e}] | {r['gain_hier_over_pooled_med']:.2f} | {r.get('frac_firms_straddling_med', float('nan')):.2f} |")
    L += ["", "### E3 summary", ""]
    for k, v in res["E3"]["summary"].items():
        L.append(f"- {k}: {v}")
    L += ["", "## E4 rank reversals (%, Wilson 95% intervals; C2 verdict for eligible cells: fail / pass / borderline)", "", "| prox | sigma | order 1 | CI | order 2 | CI | order 3 | CI | certified frac | certified reversals | mean A below cap | C2 |", "|---|---|---|---|---|---|---|---|---|---|---|---|"]
    ci = lambda c: f"[{100*c[0]:.1f}, {100*c[1]:.1f}]"
    for r in res["E4"]["rows"]:
        L.append(f"| {r['prox']} | {r['sigma']} | {100*r['rev1']:.1f} | {ci(r['rev1_ci'])} | {100*r['rev2']:.1f} | {ci(r['rev2_ci'])} | {100*r['rev3']:.1f} | {ci(r['rev3_ci'])} | "
                 f"{r.get('certified_frac', float('nan')):.2f} | {r.get('certified_reversals', '--')} | {r['fracA_mean_below_cap']:.2f} | {r.get('C2_verdict', '--')} |")
    L += ["", "### E4 summary", ""]
    for k, v in res["E4"]["summary"].items():
        L.append(f"- {k}: {v}")
    L += ["", "## E5 calibration", "", f"lambda_global = {res['E5']['lambda_global']:.4f}; lambda_regime = " +
          ", ".join(f"{k}: {v:.4f}" if v is not None else f"{k}: undefined (Q2 = 0)" for k, v in res["E5"]["lambda_regime"].items()), "",
          "| law | regime | sigma | e1 | order2 | global | regime | min ratio order2 | min ratio global | min ratio regime | reps mean above | min ratio order2 (below branch) |", "|---|---|---|---|---|---|---|---|---|---|---|---|"]
    for r in res["E5"]["rows"]:
        L.append(f"| {r['law']} | {r['regime']} | {r['sigma']} | {r['e1_med']:.2e} | {r['order2_med']:.2e} | {r['global_med']:.2e} | {r['regime_med']:.2e} | "
                 f"{r['order2_ratio_min']:.2f} | {r['global_ratio_min']:.2f} | {r['regime_ratio_min']:.2f} | {r['frac_reps_mean_above']:.2f} | {fmt(r['order2_ratio_min_below'], '%.2f')} |")
    L += ["", "### E5 summary", ""]
    for k, v in res["E5"]["summary"].items():
        L.append(f"- {k}: {v}")
    L += ["", "## E6 closed-form examples", "", json.dumps(res["E6"], indent=1)]
    with open(os.path.join(RES, "tables.md"), "w") as fh:
        fh.write("\n".join(L) + "\n")


# --------------------------------------------------------------------------- main
def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--fast", action="store_true")
    args = ap.parse_args()
    os.makedirs(RES, exist_ok=True)
    os.makedirs(FIG, exist_ok=True)
    t0 = time.time()
    c0 = time.process_time()
    # one independent generator per experiment (and one for the bootstrap), spawned from the master seed
    names = ["E0", "E1", "E1b", "E1c", "E2", "E3", "E4", "E5", "boot"]
    gens = dict(zip(names, (np.random.default_rng(s) for s in np.random.SeedSequence(SEED).spawn(len(names)))))
    brng = gens["boot"]
    with open(os.path.abspath(__file__), "rb") as fh:
        script_sha = hashlib.sha256(fh.read()).hexdigest()
    res = {"meta": {"seed": SEED, "fast": args.fast, "python": platform.python_version(),
                    "numpy": np.__version__, "scipy": scipy.__version__, "matplotlib": matplotlib.__version__,
                    "rng": "SeedSequence(SEED).spawn, one generator per experiment", "script_sha256": script_sha,
                    "date_utc": datetime.datetime.now(datetime.timezone.utc).strftime("%Y-%m-%d %H:%M")}}
    res["E0"] = {"CD": selftest(CobbDouglas(), gens["E0"]), "CES": selftest(CES(), gens["E0"])}
    for k, v in res["E0"].items():
        assert v["grad"] < 1e-6 and v["hess"] < 1e-6 and v["third"] < 1e-4, (k, v)
    print("E0 ok", res["E0"], flush=True)
    res["E1"] = run_E1(gens["E1"], args.fast, brng); print("E1 done", time.time() - t0, flush=True)
    res["E1b"] = run_E1b(gens["E1b"], args.fast); print("E1b done", time.time() - t0, flush=True)
    res["E1c"] = run_E1c(gens["E1c"], args.fast); print("E1c done", time.time() - t0, flush=True)
    res["E2"] = run_E2(gens["E2"], args.fast, brng); print("E2 done", time.time() - t0, flush=True)
    res["E3"] = run_E3(gens["E3"], args.fast, brng); print("E3 done", time.time() - t0, flush=True)
    res["E4"] = run_E4(gens["E4"], args.fast); print("E4 done", time.time() - t0, flush=True)
    res["E5"] = run_E5(gens["E5"], args.fast); print("E5 done", time.time() - t0, flush=True)
    res["E6"] = run_E6()
    res["meta"]["seconds"] = time.time() - t0
    res["meta"]["cpu_seconds"] = time.process_time() - c0
    with open(os.path.join(RES, "results.json"), "w") as fh:
        json.dump(res, fh, indent=1, default=float)
    write_tables(res)
    fig_E1(res["E1"]); fig_E2E3(res["E2"], res["E3"]); fig_E4(res["E4"])
    print(f"total {time.time() - t0:.1f} s; wrote results/results.json, results/tables.md, figures/")


if __name__ == "__main__":
    main()
