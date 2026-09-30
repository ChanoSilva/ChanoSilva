#!/usr/bin/env python3
"""Minimal projected-gradient solver for finite-dimensional variational inequalities.

VI(F, K): find x* in K with <F(x*), x - x*> >= 0 for all x in K.

The fixed points of T(x) = Pi_K(x - gamma F(x)) are exactly the solutions of VI(F, K)
(projection characterisation).  When F is mu-strongly monotone and L-Lipschitz, T is a
contraction for 0 < gamma < 2 mu / L^2 with factor sqrt(1 - 2 gamma mu + gamma^2 L^2);
the choice gamma = mu / L^2 gives sqrt(1 - mu^2 / L^2).  This is the classical argument
reproduced in the manuscript (Theorem on strong monotonicity).
"""
import numpy as np


# ----------------------------------------------------------------------------- projections
def proj_box(y, lo=0.0, hi=1.0):
    """Euclidean projection onto the box [lo, hi]^n (lo, hi scalars or arrays)."""
    return np.minimum(np.maximum(y, lo), hi)


def proj_simplex(y, total=1.0):
    """Euclidean projection onto {x >= 0, sum x = total} (sort-based, exact)."""
    y = np.asarray(y, dtype=float)
    u = np.sort(y)[::-1]
    css = np.cumsum(u) - total
    idx = np.arange(1, len(y) + 1)
    cond = u - css / idx > 0
    rho = idx[cond][-1]
    theta = css[rho - 1] / rho
    return np.maximum(y - theta, 0.0)


# ----------------------------------------------------------------------------- solver
def solve_vi(F, proj, x0, mu, L, tol=1e-12, max_iter=200000, gamma=None):
    """Projected-gradient (Picard) iteration x <- proj(x - gamma F(x)).

    Returns (x, info) where info records iterations, the final fixed-point residual
    ||x - proj(x - F(x))|| (the natural-map residual with unit step) and the
    contraction factor guaranteed by the theory.
    """
    if gamma is None:
        gamma = mu / (L * L)
    q = np.sqrt(max(0.0, 1.0 - 2.0 * gamma * mu + gamma * gamma * L * L))
    x = np.array(x0, dtype=float)
    it = 0
    for it in range(1, max_iter + 1):
        x_new = proj(x - gamma * F(x))
        step = np.linalg.norm(x_new - x)
        x = x_new
        if step <= tol:
            break
    res = np.linalg.norm(x - proj(x - F(x)))
    return x, {"iterations": it, "residual": float(res), "gamma": float(gamma),
               "contraction_factor": float(q), "last_step": float(step)}


def vi_residual(F, proj, x):
    """Natural-map residual ||x - proj(x - F(x))||; zero iff x solves VI(F, K)."""
    return float(np.linalg.norm(x - proj(x - F(x))))
