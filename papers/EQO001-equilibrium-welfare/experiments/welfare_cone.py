#!/usr/bin/env python3
"""E2-E4: the cone of welfare weights under which a Nash equilibrium is welfare-optimal.

Games: N players, scalar actions x_i in [0, 1], quadratic payoffs
    u_i(x) = -1/2 x^T H_i x + h_i^T x        (H_i symmetric N x N, h_i in R^N),
equilibrium operator F(x) = (-d u_i / d x_i)_i = M x - m with M[i, :] = H_i[i, :], m_i = h_i[i].
Welfare functionals W_lambda = sum_i lambda_i u_i, lambda >= 0.

    Lambda(x*)   = { lambda >= 0 : x* maximises W_lambda over K }              (exact set)
    Lambda_1(x*) = { lambda >= 0 : sum_i lambda_i grad u_i(x*) in N_K(x*) }    (first-order cone)

Theorem (manuscript, Thm 5.1): Lambda is a closed convex cone, Lambda <= Lambda_1 always,
with equality when every u_i is concave on K (jointly).  Without joint concavity the
inclusion can be strict.

E2  Two-player example with exact cone (wedge beta_2 lambda_2 <= lambda_1 <= lambda_2 / beta_1),
    Cournot duopoly (interior equilibrium, cone {0}; boundary equilibrium, cone = a ray),
    and the Nikaido-Isoda modification u_i' = u_i - v_i(x_{-i}) which makes the same
    equilibrium optimal for every lambda >= 0 (Prop. 5.3).
E3  Random jointly concave games (N = 3, 4): predefined criterion = every tested lambda in
    Lambda_1 (vertices and a relative-interior point of Lambda_1 on the simplex, plus grid
    points) is in Lambda, and every grid point outside Lambda_1 is outside Lambda.
E4  Random non-concave games (same monotone F structure): count instances where a lambda in
    Lambda_1 is certified NOT to be in Lambda (a feasible x with W_lambda(x) > W_lambda(x*)).

Lambda-membership is decided exactly (up to floating point) by enumerating the 3^N faces
of the box and solving the stationarity system of W_lambda restricted to each face; the
global maximiser of a quadratic over a box lies in the relative interior of some face and
is stationary for the restriction, so it is among the candidates.
"""
import itertools
import json
import os
import platform
import sys
import time

import numpy as np
import scipy
from scipy.optimize import linprog

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from vi_solver import proj_box, solve_vi, vi_residual  # noqa: E402

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
SEED = 20260930
T0 = time.time()
TOL_BOUNDARY = 1e-9      # x_j* within this of 0 or 1 counts as active
TOL_LIN = 1e-9           # tolerance in the linear (first-order) membership test
TOL_QP = 1e-8            # lambda is in Lambda if W(x*) >= max_K W - TOL_QP
WITNESS_GAP = 1e-6       # a better point must beat W(x*) by this to count as a witness


# ----------------------------------------------------------------------------- games
class QuadGame:
    def __init__(self, H, h):
        self.H = [np.array(Hi, dtype=float) for Hi in H]
        self.h = np.array(h, dtype=float)
        self.N = len(self.H)
        self.M = np.array([self.H[i][i, :] for i in range(self.N)])
        self.m = np.array([self.h[i][i] for i in range(self.N)])
        S = (self.M + self.M.T) / 2
        self.mu = float(np.linalg.eigvalsh(S).min())
        self.L = float(np.linalg.norm(self.M, 2))

    def F(self, x):
        return self.M @ x - self.m

    def payoffs(self, x):
        return np.array([-0.5 * x @ Hi @ x + hi @ x for Hi, hi in zip(self.H, self.h)])

    def grad_matrix(self, x):
        """G[i, j] = d u_i / d x_j at x."""
        return np.array([-Hi @ x + hi for Hi, hi in zip(self.H, self.h)])

    def jointly_concave(self):
        return all(np.linalg.eigvalsh(Hi).min() >= -1e-10 for Hi in self.H)

    def equilibrium(self):
        x0 = np.full(self.N, 0.5)
        x, info = solve_vi(self.F, proj_box, x0, self.mu, self.L, tol=1e-13)
        info["residual"] = vi_residual(self.F, proj_box, x)
        return x, info


def random_game(rng, N, concave, mu_target=0.5, h_loc=1.0, h_scale=1.5):
    H = []
    for _ in range(N):
        B = rng.normal(size=(N, N)) / np.sqrt(N)
        H.append(B @ B.T if concave else (B + B.T) / 2)
    h = rng.normal(loc=h_loc, scale=h_scale, size=(N, N))
    M = np.array([H[i][i, :] for i in range(N)])
    lam_min = np.linalg.eigvalsh((M + M.T) / 2).min()
    d = max(0.0, mu_target - lam_min)
    for i in range(N):
        H[i][i, i] += d          # keeps H_i PSD in the concave case; makes F strongly monotone
    return QuadGame(H, h)


# ----------------------------------------------------------------------------- exact box QP
_FACE_CACHE = {}


def faces(N):
    if N not in _FACE_CACHE:
        out = []
        for pat in itertools.product((0, 1, 2), repeat=N):
            pat = np.array(pat)
            free = np.where(pat == 2)[0]
            fixed = np.where(pat != 2)[0]
            out.append((free, fixed, pat[fixed].astype(float)))
        _FACE_CACHE[N] = out
    return _FACE_CACHE[N]


def box_qp_max(Hq, hq):
    """Global maximum of -1/2 x^T Hq x + hq^T x over [0,1]^N by face enumeration."""
    N = len(hq)
    best_val, best_x = -np.inf, None
    for free, fixed, xb in faces(N):
        x = np.zeros(N)
        x[fixed] = xb
        if len(free):
            A = Hq[np.ix_(free, free)]
            rhs = hq[free] - Hq[np.ix_(free, fixed)] @ xb
            try:
                xf = np.linalg.solve(A, rhs)
            except np.linalg.LinAlgError:
                xf = np.linalg.lstsq(A, rhs, rcond=None)[0]
            if np.any(xf < -1e-9) or np.any(xf > 1 + 1e-9):
                continue
            x[free] = np.clip(xf, 0.0, 1.0)
        val = -0.5 * x @ Hq @ x + hq @ x
        if val > best_val:
            best_val, best_x = val, x
    return best_val, best_x


def pga_max(Hq, hq, rng, starts=6, iters=20000):
    """Projected gradient ascent (independent cross-check, valid for concave W)."""
    L = max(np.abs(np.linalg.eigvalsh(Hq)).max(), 1e-12)
    best = -np.inf
    for s in range(starts):
        x = rng.random(len(hq)) if s else np.full(len(hq), 0.5)
        for _ in range(iters):
            x = proj_box(x + (1.0 / L) * (-Hq @ x + hq))
        best = max(best, -0.5 * x @ Hq @ x + hq @ x)
    return best


def in_Lambda(game, xstar, lam, return_witness=False):
    Hq = sum(l * Hi for l, Hi in zip(lam, game.H))
    hq = sum(l * hi for l, hi in zip(lam, game.h))
    wmax, xmax = box_qp_max(Hq, hq)
    wstar = -0.5 * xstar @ Hq @ xstar + hq @ xstar
    member = wstar >= wmax - TOL_QP
    if return_witness:
        return member, float(wmax - wstar), xmax
    return member


# ----------------------------------------------------------------------------- first-order cone
def active_pattern(xstar):
    """-1: at lower bound, +1: at upper bound, 0: interior."""
    pat = np.zeros(len(xstar), dtype=int)
    pat[xstar <= TOL_BOUNDARY] = -1
    pat[xstar >= 1 - TOL_BOUNDARY] = 1
    return pat


def cone_constraints(G, pat):
    """Lambda_1 = {lam >= 0 : A_eq lam = 0, A_ub lam <= 0}. Columns of G^T are G[:, j]."""
    A_eq = [G[:, j] for j in range(len(pat)) if pat[j] == 0]
    A_ub = [G[:, j] for j in range(len(pat)) if pat[j] == -1] + \
           [-G[:, j] for j in range(len(pat)) if pat[j] == 1]
    N = G.shape[0]
    A_eq = np.array(A_eq) if A_eq else np.zeros((0, N))
    A_ub = np.array(A_ub) if A_ub else np.zeros((0, N))
    return A_eq, A_ub


def in_Lambda1(lam, A_eq, A_ub):
    ok = np.all(lam >= -TOL_LIN)
    if A_eq.shape[0]:
        ok &= np.all(np.abs(A_eq @ lam) <= TOL_LIN * (1 + np.abs(A_eq).sum()))
    if A_ub.shape[0]:
        ok &= np.all(A_ub @ lam <= TOL_LIN * (1 + np.abs(A_ub).sum()))
    return bool(ok)


def _lp(c, A_ub, b_ub, A_eq, b_eq, N, extra_ub=None, extra_eq=None, bounds=None):
    Aub = A_ub if A_ub.shape[0] else None
    bub = b_ub if A_ub.shape[0] else None
    if extra_ub is not None:
        Aub = np.vstack([Aub, extra_ub[0]]) if Aub is not None else np.atleast_2d(extra_ub[0])
        bub = np.concatenate([bub, extra_ub[1]]) if bub is not None else np.atleast_1d(extra_ub[1])
    Aeq = A_eq if A_eq.shape[0] else None
    beq = b_eq if A_eq.shape[0] else None
    if extra_eq is not None:
        Aeq = np.vstack([Aeq, extra_eq[0]]) if Aeq is not None else np.atleast_2d(extra_eq[0])
        beq = np.concatenate([beq, extra_eq[1]]) if beq is not None else np.atleast_1d(extra_eq[1])
    return linprog(c, A_ub=Aub, b_ub=bub, A_eq=Aeq, b_eq=beq,
                   bounds=bounds if bounds is not None else [(0, None)] * N, method="highs")


def cone_geometry(G, pat, rng, n_vertex_draws=12):
    """Nontriviality, dimension, vertices of Lambda_1 on the simplex, relative-interior point."""
    N = G.shape[0]
    A_eq, A_ub = cone_constraints(G, pat)
    ones = np.ones((1, N))
    b_eq = np.zeros(A_eq.shape[0])
    b_ub = np.zeros(A_ub.shape[0])
    # nontrivial?
    r = _lp(-np.ones(N), A_ub, b_ub, A_eq, b_eq, N, extra_ub=(ones, [1.0]))
    nontrivial = r.status == 0 and -r.fun > 0.5
    if not nontrivial:
        return {"nontrivial": False, "dim": 0, "vertices": [], "relint": None,
                "n_interior": int(np.sum(pat == 0)), "A_eq": A_eq, "A_ub": A_ub}
    # implicit equalities among inequality rows (A_ub rows and lam_i >= 0)
    ineq_rows = [row for row in A_ub] + [-np.eye(N)[i] for i in range(N)]
    implicit = []
    for row in ineq_rows:
        r = _lp(row, A_ub, b_ub, A_eq, b_eq, N, extra_ub=(ones, [1.0]))   # minimise row.lam (= -slack)
        if r.status == 0 and -r.fun <= 1e-9:
            implicit.append(row)
    E = np.vstack([A_eq] + [np.atleast_2d(x) for x in implicit]) if (A_eq.shape[0] or implicit) else np.zeros((0, N))
    dim = N - (np.linalg.matrix_rank(E, tol=1e-9) if E.shape[0] else 0)
    # vertices of Lambda_1 on the simplex
    verts = []
    for _ in range(n_vertex_draws):
        c = rng.normal(size=N)
        r = _lp(c, A_ub, b_ub, A_eq, b_eq, N, extra_eq=(ones, [1.0]))
        if r.status == 0:
            v = np.round(r.x, 10)
            if not any(np.allclose(v, w, atol=1e-8) for w in verts):
                verts.append(v)
    relint = np.mean(verts, axis=0) if verts else None
    return {"nontrivial": True, "dim": int(dim), "vertices": verts, "relint": relint,
            "n_interior": int(np.sum(pat == 0)), "A_eq": A_eq, "A_ub": A_ub}


def simplex_grid(N, k):
    pts = []
    for comp in itertools.product(range(k + 1), repeat=N - 1):
        if sum(comp) <= k:
            pts.append(np.array(list(comp) + [k - sum(comp)], dtype=float) / k)
    return pts


# ----------------------------------------------------------------------------- E3 / E4 driver
def run_random(rng, N, n_instances, concave, grid_k, pga_check=0):
    rows = []
    agg = {"instances": 0, "nontrivial": 0, "dims": {}, "boundary_coord_fraction": [],
           "tested_in_L1": 0, "tested_in_L1_in_L": 0, "grid_out_L1": 0, "grid_out_L1_out_L": 0,
           "grid_in_L1": 0, "grid_in_L1_in_L": 0, "witness_instances": 0, "witnesses": 0,
           "max_residual": 0.0, "max_iterations": 0, "all_concave": True, "any_indefinite_H": 0,
           "pga_checks": 0, "pga_max_abs_diff": 0.0, "min_mu": np.inf, "max_L": 0.0}
    grid = simplex_grid(N, grid_k)
    for k in range(n_instances):
        g = random_game(rng, N, concave)
        xs, info = g.equilibrium()
        pat = active_pattern(xs)
        G = g.grad_matrix(xs)
        geo = cone_geometry(G, pat, rng)
        agg["instances"] += 1
        agg["max_residual"] = max(agg["max_residual"], info["residual"])
        agg["max_iterations"] = max(agg["max_iterations"], info["iterations"])
        agg["min_mu"] = min(agg["min_mu"], g.mu)
        agg["max_L"] = max(agg["max_L"], g.L)
        agg["boundary_coord_fraction"].append(float(np.mean(pat != 0)))
        jc = g.jointly_concave()
        agg["all_concave"] &= jc
        agg["any_indefinite_H"] += int(not jc)
        row = {"instance": k, "x_star": xs.tolist(), "pattern": pat.tolist(), "mu": g.mu, "L": g.L,
               "iterations": info["iterations"], "residual": info["residual"],
               "jointly_concave": bool(jc), "cone_nontrivial": geo["nontrivial"], "cone_dim": geo["dim"],
               "tested": 0, "tested_in_L": 0, "witness": None}
        if geo["nontrivial"]:
            agg["nontrivial"] += 1
            agg["dims"][geo["dim"]] = agg["dims"].get(geo["dim"], 0) + 1
            tests = list(geo["vertices"]) + ([geo["relint"]] if geo["relint"] is not None else [])
            best_gap = 0.0
            for lam in tests:
                assert in_Lambda1(lam, geo["A_eq"], geo["A_ub"])
                member, gap, xw = in_Lambda(g, xs, lam, return_witness=True)
                row["tested"] += 1
                agg["tested_in_L1"] += 1
                if member:
                    row["tested_in_L"] += 1
                    agg["tested_in_L1_in_L"] += 1
                elif gap > WITNESS_GAP:
                    agg["witnesses"] += 1
                    if gap > best_gap:
                        best_gap = gap
                        row["witness"] = {"lambda": lam.tolist(), "better_x": xw.tolist(), "gap": gap}
            if row["witness"] is not None:
                agg["witness_instances"] += 1
            if pga_check and k < pga_check and geo["relint"] is not None:
                lam = geo["relint"]
                Hq = sum(l * Hi for l, Hi in zip(lam, g.H))
                hq = sum(l * hi for l, hi in zip(lam, g.h))
                v_face, _ = box_qp_max(Hq, hq)
                v_pga = pga_max(Hq, hq, rng)
                agg["pga_checks"] += 1
                agg["pga_max_abs_diff"] = max(agg["pga_max_abs_diff"], abs(v_face - v_pga))
        # grid
        for lam in grid:
            l1 = in_Lambda1(lam, geo["A_eq"], geo["A_ub"])
            ll = in_Lambda(g, xs, lam)
            if l1:
                agg["grid_in_L1"] += 1
                agg["grid_in_L1_in_L"] += int(ll)
            else:
                agg["grid_out_L1"] += 1
                agg["grid_out_L1_out_L"] += int(not ll)
        rows.append(row)
    agg["boundary_coord_fraction"] = float(np.mean(agg["boundary_coord_fraction"]))
    agg["dims"] = {str(k): v for k, v in sorted(agg["dims"].items())}
    agg["grid_points_per_instance"] = len(grid)
    agg["N"] = N
    agg["concave"] = concave
    agg["min_mu"] = float(agg["min_mu"])
    return agg, rows


# ----------------------------------------------------------------------------- E2 examples
def two_player_example(rng, beta1=0.5, beta2=0.5, alpha=2.0, n_angles=181):
    H = [np.diag([1.0, 0.0]), np.diag([0.0, 1.0])]
    h = [np.array([alpha, -beta1]), np.array([-beta2, alpha])]
    g = QuadGame(H, h)
    xs, info = g.equilibrium()
    pat = active_pattern(xs)
    G = g.grad_matrix(xs)
    A_eq, A_ub = cone_constraints(G, pat)
    thetas = np.linspace(0, np.pi / 2, n_angles)
    rec = []
    for th in thetas:
        lam = np.array([np.cos(th), np.sin(th)])
        pred = (lam[0] >= beta2 * lam[1] - 1e-12) and (lam[1] >= beta1 * lam[0] - 1e-12)   # closed form
        l1 = in_Lambda1(lam, A_eq, A_ub)
        ll = in_Lambda(g, xs, lam)
        rec.append((float(th), bool(pred), bool(l1), bool(ll)))
    agree = sum(1 for r in rec if r[1] == r[2] == r[3])
    lam_w = np.array([1.0, 3.0])
    member, gap, xw = in_Lambda(g, xs, lam_w, return_witness=True)
    return {"beta1": beta1, "beta2": beta2, "alpha": alpha, "x_star": xs.tolist(), "F_at_x_star": g.F(xs).tolist(),
            "residual": info["residual"], "mu": g.mu, "L": g.L,
            "boundary_angles_deg": [float(np.degrees(np.arctan(beta1))), float(np.degrees(np.arctan(1 / beta2)))],
            "angles_tested": n_angles, "agreement": agree,
            "in_cone_count": sum(1 for r in rec if r[3]),
            "witness_lambda": lam_w.tolist(), "witness_member": bool(member), "witness_gap": gap,
            "witness_better_x": xw.tolist(), "records": rec}


def cournot_examples(rng):
    out = {}
    # interior: a = 1, c = 0, K = [0,1]^2 -> q* = (1/3, 1/3)
    a = 1.0
    H = [np.array([[2.0, 1.0], [1.0, 0.0]]), np.array([[0.0, 1.0], [1.0, 2.0]])]
    h = [np.array([a, 0.0]), np.array([0.0, a])]
    g = QuadGame(H, h)
    xs, info = g.equilibrium()
    pat = active_pattern(xs)
    G = g.grad_matrix(xs)
    geo = cone_geometry(G, pat, rng)
    grid = simplex_grid(2, 60)
    n_in = sum(in_Lambda(g, xs, lam) for lam in grid)
    coll = np.array([0.25, 0.25])
    out["interior"] = {"a": a, "x_star": xs.tolist(), "residual": info["residual"], "pattern": pat.tolist(),
                       "G": G.tolist(), "cone_nontrivial": geo["nontrivial"], "grid_points": len(grid),
                       "grid_points_in_Lambda": int(n_in),
                       "payoffs_at_equilibrium": g.payoffs(xs).tolist(),
                       "payoffs_at_collusion": g.payoffs(coll).tolist(),
                       "jointly_concave": bool(g.jointly_concave())}
    # boundary: a = 4 -> q* = (1, 1)
    a = 4.0
    h = [np.array([a, 0.0]), np.array([0.0, a])]
    g = QuadGame(H, h)
    xs, info = g.equilibrium()
    pat = active_pattern(xs)
    G = g.grad_matrix(xs)
    geo = cone_geometry(G, pat, rng)
    grid = simplex_grid(2, 60)
    in_l1 = [in_Lambda1(lam, geo["A_eq"], geo["A_ub"]) for lam in grid]
    in_l = [in_Lambda(g, xs, lam) for lam in grid]
    out["boundary"] = {"a": a, "x_star": xs.tolist(), "residual": info["residual"], "pattern": pat.tolist(),
                       "F_at_x_star": g.F(xs).tolist(), "G": G.tolist(),
                       "cone_nontrivial": geo["nontrivial"], "cone_dim": geo["dim"],
                       "vertices": [v.tolist() for v in geo["vertices"]],
                       "grid_points": len(grid), "grid_in_L1": int(sum(in_l1)), "grid_in_L": int(sum(in_l)),
                       "agreement": int(sum(a == b for a, b in zip(in_l1, in_l))),
                       "relint_in_Lambda": bool(in_Lambda(g, xs, geo["relint"])) if geo["relint"] is not None else None,
                       "jointly_concave": bool(g.jointly_concave())}
    # Nikaido-Isoda modification of the interior Cournot game: u_i' = u_i - v_i(x_{-i})
    a = 1.0
    def u(q):
        return np.array([q[0] * (a - q[0] - q[1]), q[1] * (a - q[0] - q[1])])
    def v(q):   # best-response values, best response clipped to [0, 1]
        b0 = np.clip((a - q[1]) / 2, 0, 1); b1 = np.clip((a - q[0]) / 2, 0, 1)
        return np.array([b0 * (a - b0 - q[1]), b1 * (a - q[0] - b1)])
    n = 401
    xs_ = np.array([1 / 3, 1 / 3])
    gridx = np.linspace(0, 1, n)
    X, Y = np.meshgrid(gridx, gridx, indexing="ij")
    Q = np.stack([X.ravel(), Y.ravel()])
    U = np.array([Q[0] * (a - Q[0] - Q[1]), Q[1] * (a - Q[0] - Q[1])])
    B0 = np.clip((a - Q[1]) / 2, 0, 1); B1 = np.clip((a - Q[0]) / 2, 0, 1)
    V = np.array([B0 * (a - B0 - Q[1]), B1 * (a - Q[0] - B1)])
    Up = U - V                       # u' on the grid, <= 0 everywhere, = 0 at Nash
    lam_grid = simplex_grid(2, 60)
    worst = -np.inf
    for lam in lam_grid:
        worst = max(worst, float(np.max(lam @ Up)))
    out["nikaido_isoda"] = {"a": a, "x_star": xs_.tolist(), "u_prime_at_x_star": (u(xs_) - v(xs_)).tolist(),
                            "grid_x": n, "lambda_directions": len(lam_grid),
                            "max_W_prime_over_grid_all_lambda": worst,
                            "max_u_prime_over_grid": Up.max(axis=1).tolist(),
                            "x_star_optimal_for_all_lambda": bool(worst <= 1e-12)}
    return out


# ----------------------------------------------------------------------------- figures
def make_figures(ex2, aggs):
    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt
    BLUE, ORANGE, GRAY, INK, MUTED = "#2a78d6", "#eb6834", "#b8b7b1", "#0b0b0b", "#52514e"
    plt.rcParams.update({"font.size": 9, "axes.edgecolor": MUTED, "axes.labelcolor": INK,
                         "xtick.color": MUTED, "ytick.color": MUTED, "axes.spines.top": False,
                         "axes.spines.right": False})
    figdir = os.path.join(ROOT, "figures")
    os.makedirs(figdir, exist_ok=True)

    # Figure 1: the exact wedge in the two-player example
    fig, ax = plt.subplots(figsize=(3.6, 3.6))
    r = 1.0
    for th, pred, l1, ll in ex2["records"]:
        ax.plot([0, r * np.cos(th)], [0, r * np.sin(th)], color=BLUE if ll else GRAY,
                lw=0.9 if ll else 0.5, alpha=0.9 if ll else 0.6, solid_capstyle="round")
    b1, b2 = ex2["beta1"], ex2["beta2"]
    for slope, lab in ((b1, r"$\lambda_2=\beta_1\lambda_1$"), (1 / b2, r"$\lambda_1=\beta_2\lambda_2$")):
        t = np.linspace(0, 1.15, 2)
        ax.plot(t / np.sqrt(1 + slope**2), slope * t / np.sqrt(1 + slope**2), color=ORANGE, lw=1.6)
    ax.text(0.98, 0.42, r"$\lambda_2=\beta_1\lambda_1$", color=INK, fontsize=8, ha="right")
    ax.text(0.30, 1.02, r"$\lambda_1=\beta_2\lambda_2$", color=INK, fontsize=8)
    ax.text(0.62, 0.62, r"$\Lambda(x^*)$", color=INK, fontsize=10, ha="center")
    ax.set_xlim(0, 1.2); ax.set_ylim(0, 1.2); ax.set_aspect("equal")
    ax.set_xlabel(r"$\lambda_1$"); ax.set_ylabel(r"$\lambda_2$")
    ax.set_title(r"Welfare-weight cone, $\beta_1=\beta_2=1/2$", fontsize=9, color=INK)
    ax.grid(True, color="#e6e5e0", lw=0.5)
    fig.tight_layout()
    fig.savefig(os.path.join(figdir, "fig_cone_2player.png"), dpi=200)
    fig.savefig(os.path.join(figdir, "fig_cone_2player.pdf"))
    plt.close(fig)

    # Figure 2: dimension of Lambda_1 across random games (concave vs non-concave)
    fig, axes = plt.subplots(1, 2, figsize=(6.4, 2.6), sharey=False)
    for ax, N in zip(axes, (3, 4)):
        a_c = next(a for a in aggs if a["N"] == N and a["concave"])
        a_n = next(a for a in aggs if a["N"] == N and not a["concave"])
        dims = list(range(0, N + 1))
        def counts(a):
            c = [a["instances"] - a["nontrivial"]] + [a["dims"].get(str(d), 0) for d in range(1, N + 1)]
            return np.array(c) / a["instances"]
        w = 0.38
        ax.bar(np.array(dims) - w / 2, counts(a_c), width=w, color=BLUE, label="jointly concave")
        ax.bar(np.array(dims) + w / 2, counts(a_n), width=w, color=ORANGE, label="non-concave")
        ax.set_xticks(dims); ax.set_xlabel(r"$\dim\Lambda_1(x^*)$ (0 = trivial cone)")
        ax.set_title(f"N = {N} players, {a_c['instances']} + {a_n['instances']} games", fontsize=9, color=INK)
        ax.grid(True, axis="y", color="#e6e5e0", lw=0.5)
        ax.set_axisbelow(True)
    axes[0].set_ylabel("fraction of instances")
    axes[0].legend(frameon=False, fontsize=8)
    fig.tight_layout()
    fig.savefig(os.path.join(figdir, "fig_cone_dims.png"), dpi=200)
    fig.savefig(os.path.join(figdir, "fig_cone_dims.pdf"))
    plt.close(fig)


# ----------------------------------------------------------------------------- main
def main():
    if "--figures-only" in sys.argv:      # rebuild the figures from the saved results
        saved = json.load(open(os.path.join(ROOT, "results", "results_welfare.json")))
        make_figures(two_player_example(np.random.default_rng(SEED)), saved["E3_E4_summary"])
        print("figures rebuilt from results/results_welfare.json")
        return
    rng = np.random.default_rng(SEED)
    out = {"meta": {"seed": SEED, "python": platform.python_version(), "numpy": np.__version__,
                    "scipy": scipy.__version__}}
    ex2 = two_player_example(rng)
    out["E2_two_player"] = dict(ex2)
    out["E2_cournot"] = cournot_examples(rng)
    aggs, allrows = [], {}
    for N, concave, grid_k, n_inst in ((3, True, 12, 100), (4, True, 8, 100), (3, False, 12, 100), (4, False, 8, 100)):
        agg, rows = run_random(rng, N, n_inst, concave, grid_k, pga_check=25 if concave else 0)
        aggs.append(agg)
        allrows[f"N{N}_{'concave' if concave else 'nonconcave'}"] = rows
        print(f"N={N} concave={concave}: {agg}")
    out["E3_E4_summary"] = aggs
    out["E3_E4_rows"] = allrows
    # a few explicit witnesses of strict inclusion for the manuscript
    wit = []
    for key, rows in allrows.items():
        if "nonconcave" in key:
            for r in rows:
                if r["witness"] is not None:
                    wit.append({"game": key, "instance": r["instance"], **r["witness"], "x_star": r["x_star"]})
    out["E4_witness_examples"] = wit[:5]
    out["meta"]["seconds"] = time.time() - T0
    with open(os.path.join(ROOT, "results", "results_welfare.json"), "w") as fh:
        json.dump(out, fh, indent=1)
    make_figures(ex2, aggs)

    L = ["# E2-E4: welfare-weight cones", "", f"Seed {SEED}; {out['meta']['seconds']:.1f} s.", "",
         "## E2 two-player example",
         f"- x* = {ex2['x_star']}, F(x*) = {ex2['F_at_x_star']}, residual {ex2['residual']:.1e}",
         f"- boundary angles (deg): {ex2['boundary_angles_deg']}",
         f"- {ex2['agreement']}/{ex2['angles_tested']} directions: closed form = first-order cone = exact QP; "
         f"{ex2['in_cone_count']} directions inside",
         f"- witness lambda = {ex2['witness_lambda']}: member {ex2['witness_member']}, gap {ex2['witness_gap']:.4f}, "
         f"better x = {ex2['witness_better_x']}", "",
         "## E2 Cournot",
         f"- interior: x* = {out['E2_cournot']['interior']['x_star']}, cone nontrivial: "
         f"{out['E2_cournot']['interior']['cone_nontrivial']}, grid points in Lambda: "
         f"{out['E2_cournot']['interior']['grid_points_in_Lambda']}/{out['E2_cournot']['interior']['grid_points']}",
         f"- boundary: x* = {out['E2_cournot']['boundary']['x_star']}, cone dim {out['E2_cournot']['boundary']['cone_dim']}, "
         f"vertices {out['E2_cournot']['boundary']['vertices']}, grid agreement "
         f"{out['E2_cournot']['boundary']['agreement']}/{out['E2_cournot']['boundary']['grid_points']}",
         f"- Nikaido-Isoda: x* optimal for all lambda: {out['E2_cournot']['nikaido_isoda']['x_star_optimal_for_all_lambda']} "
         f"(max W' over grid {out['E2_cournot']['nikaido_isoda']['max_W_prime_over_grid_all_lambda']:.2e})", "",
         "## E3/E4 random games", "",
         "| N | concave | instances | nontrivial | dims | tested in L1 | of which in L | grid out L1 | out L | grid in L1 | in L | witness inst. | max resid |",
         "|---|---|---|---|---|---|---|---|---|---|---|---|---|"]
    for a in aggs:
        L.append(f"| {a['N']} | {a['concave']} | {a['instances']} | {a['nontrivial']} | {a['dims']} | {a['tested_in_L1']} | "
                 f"{a['tested_in_L1_in_L']} | {a['grid_out_L1']} | {a['grid_out_L1_out_L']} | {a['grid_in_L1']} | "
                 f"{a['grid_in_L1_in_L']} | {a['witness_instances']} | {a['max_residual']:.1e} |")
    with open(os.path.join(ROOT, "results", "tables_welfare.md"), "w") as fh:
        fh.write("\n".join(L) + "\n")
    print("\n".join(L))


if __name__ == "__main__":
    main()
