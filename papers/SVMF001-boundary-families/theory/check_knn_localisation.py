#!/usr/bin/env python3
"""SVMF001 -- numerical check of the kNN-localisation results (theory/knn_localisation.tex).

Model (Proposition prop:exact of the manuscript): Y uniform on {-1,+1}, X_1 | Y ~ N(Y mu, 1),
optionally extra coordinates W ~ N(0, I) independent of (X_1, Y).  Bayes rule sign(x_1).

Base rules A:
  nc  : nearest-centroid threshold on X_1 (midpoint of the class means; constant if a class is missing)
  svm : linear SVM (hinge loss, C = 1 fixed, sklearn SVC) ; constant if the local sample is pure
kNN-localised rule: at a query, fit A on the k nearest training points and predict at the query.

Parts
  C   exact constants: Bayes risk, R_nc(n) (exact finite sum), the k-fixed limits
      Rinf_nc(k) = R* + E[(a-1/2)(1-a^k+b^k)]   and   Rinf_vote(k) = R* + E[(2a-1) P(Bin(k,a)<k/2)]
      (a = max(eta, 1-eta), b = 1-a), the first-order constant Q(rho) = 1/(rho v(mu, r_rho)).
  L   Lemma (population local threshold has the Bayes sign): grid check.
  P1  uninformative neighbourhoods (kNN in W only): Monte Carlo vs the exact identity E R = R_A(k)
      (nc: exact R_nc(k); svm on X_1: Monte Carlo learning curve).
  P2  informative neighbourhoods, k fixed: nc in d = 1 (neighbourhood in X_1) for growing n,
      against Rinf_nc(k) and R_nc(n); nc with neighbourhoods in all d = 2, 5 coordinates.
  P3  informative neighbourhoods, k fixed, local linear SVM in d = 1: against Rinf_vote(k);
      check of the deterministic 'majority' lemma when the neighbourhood radius is < r0(k, C).
  P4  informative neighbourhoods, k = rho n (d = 1, nc): excess-risk ratio vs Q(rho) and vs 1/rho.

Risk estimators: excess risk E[|2 eta(X_1) - 1| 1{f(X) != sign(X_1)}] (exact identity R - R* ),
evaluated either by deterministic quadrature over x_1 (d = 1) or at Monte Carlo test points (d > 1),
or exactly given the fitted threshold when the test pair is independent of the selection (P1).
Every reported Monte Carlo number carries its standard error over independent training samples.

Usage:  OMP_NUM_THREADS=1 python check_knn_localisation.py   (writes knn_localisation_results.json)
        python check_knn_localisation.py --macros > ../manuscript/knn_numbers.tex   (adds key 'macros' to the JSON)
        python check_knn_localisation.py --report   (re-prints the report from the JSON)
"""
import json
import os
import platform
import sys
import time

import numpy as np
import scipy
import sklearn
from scipy.integrate import quad
from scipy.optimize import brentq
from scipy.stats import binom, norm, truncnorm
from sklearn.neighbors import NearestNeighbors
from sklearn.svm import SVC

SEED = 20261003
MU_MAIN = 3.29 / 2          # manuscript value (delta = 3.29, Bayes risk 0.0500)
MU_HARD = 0.5               # harder model, Bayes risk 0.3085
HERE = os.path.dirname(os.path.abspath(__file__))
T0 = time.process_time()


# ---------------------------------------------------------------- model helpers
def bayes(mu):
    return float(norm.cdf(-mu))


def eta(x1, mu):
    return 1.0 / (1.0 + np.exp(-2.0 * mu * np.asarray(x1, float)))


def dens(x1, mu):
    return 0.5 * (norm.pdf(x1 - mu) + norm.pdf(x1 + mu))


def risk_t(t, mu):
    """Risk of 'predict +1 iff x1 > t'."""
    return 0.5 * (norm.cdf(t - mu) + norm.cdf(-t - mu))


def risk_lin1(w, b, mu):
    """Exact risk of sign(w x1 + b) (any sign of w); 1/2 if w = 0."""
    w = np.asarray(w, float); b = np.asarray(b, float)
    aw = np.abs(w)
    with np.errstate(divide="ignore", invalid="ignore"):
        r = 0.5 * (norm.cdf(-(w * mu + b) / aw) + norm.cdf((b - w * mu) / aw))
    return np.where(aw > 0, r, 0.5)


def sample(rng, n, d, mu):
    y = rng.choice([-1, 1], size=n)
    X = rng.normal(size=(n, d))
    X[:, 0] += y * mu
    return X, y


_RNC = {}


def R_nc(n, mu):
    """Exact learning curve of the nearest-centroid threshold (Prop. prop:exact (ii))."""
    key = (int(n), float(mu))
    if key not in _RNC:
        n = int(n)
        if n == 0:
            _RNC[key] = 0.5
        else:
            ks = np.arange(n + 1)
            a = ks.astype(float); b = (n - ks).astype(float)
            with np.errstate(divide="ignore"):
                s2 = 0.25 * (1.0 / np.where(a > 0, a, np.inf) + 1.0 / np.where(b > 0, b, np.inf))
            r = np.where((a > 0) & (b > 0), norm.cdf(-mu / np.sqrt(1.0 + s2)), 0.5)
            _RNC[key] = float(np.sum(binom.pmf(ks, n, 0.5) * r))
    return _RNC[key]


def _integrate_even(g, mu):
    """E[g(X_1)] for g even in x1 (the integrands below are), X_1 ~ mixture."""
    val, _ = quad(lambda x: 2.0 * dens(x, mu) * g(x), 0.0, np.inf, limit=400, epsabs=1e-13, epsrel=1e-11)
    return val


def Rinf_nc(k, mu):
    def g(x):
        e = float(eta(x, mu)); a = max(e, 1 - e); b = 1 - a
        return (a - 0.5) * (1.0 - a ** k + b ** k)
    return bayes(mu) + _integrate_even(g, mu)


def Rinf_vote(k, mu):
    assert k % 2 == 1
    def g(x):
        e = float(eta(x, mu)); a = max(e, 1 - e)
        return (2 * a - 1) * binom.cdf((k - 1) // 2, k, a)
    return bayes(mu) + _integrate_even(g, mu)


def heuristic_Q(rho, mu):
    """First-order excess-ratio constant for k = rho n, d = 1 (heuristic, Remark in the tex)."""
    if rho >= 1:
        return {"r": float("inf"), "v": 1.0, "Q": 1.0}
    r = brentq(lambda r: norm.cdf(r - mu) + norm.cdf(r + mu) - 1.0 - rho, 1e-9, 50)
    v = float(truncnorm(a=-r - mu, b=r - mu, loc=mu, scale=1.0).var())
    return {"r": float(r), "v": v, "Q": 1.0 / (rho * v)}


def make_grid(mu, fine=1.0, n_fine=10000, n_coarse=4000):
    """Midpoint quadrature nodes/weights on [-L, L], L = mu + 7, finer on [-fine, fine]."""
    L = mu + 7.0
    e_f = np.linspace(-fine, fine, n_fine + 1)
    e_l = np.linspace(-L, -fine, n_coarse // 2 + 1)
    e_r = np.linspace(fine, L, n_coarse // 2 + 1)
    nodes, wts = [], []
    for e in (e_l, e_f, e_r):
        nodes.append(0.5 * (e[1:] + e[:-1])); wts.append(np.diff(e))
    x = np.concatenate(nodes); w = np.concatenate(wts) * dens(np.concatenate(nodes), mu)
    return x, w


# ---------------------------------------------------------------- 1-D kNN machinery
def knn_block_start(xs, q, k):
    """xs sorted (n,), queries q (G,): start index lo of the contiguous block of the k nearest."""
    n = len(xs)
    lo = np.zeros(len(q), dtype=np.int64)
    hi = np.full(len(q), n - k, dtype=np.int64)
    while True:
        act = lo < hi
        if not act.any():
            return lo
        mid = (lo + hi) // 2
        midc = np.where(act, mid, 0)
        right = act & ((q - xs[midc]) > (xs[np.minimum(midc + k, n - 1)] - q))
        lo = np.where(right, mid + 1, lo)
        hi = np.where(act & ~right, mid, hi)


def loc_nc_pred_1d(xs, ys, q, k):
    """kNN-localised nearest-centroid threshold, neighbourhood in X_1 (d = 1). Returns predictions."""
    lo = knn_block_start(xs, q, k)
    if k <= 64:
        idx = lo[:, None] + np.arange(k)[None, :]
        D = xs[idx] - q[:, None]                     # offsets (exact, no cancellation)
        pos = ys[idx] == 1
        npos = pos.sum(1); nneg = k - npos
        sp = (D * pos).sum(1); sn = (D * ~pos).sum(1)
    else:
        pos = (ys == 1).astype(float)
        P = np.concatenate([[0.0], np.cumsum(pos)])
        xc = xs - np.median(xs)
        PX = np.concatenate([[0.0], np.cumsum(xc * pos)])
        SX = np.concatenate([[0.0], np.cumsum(xc)])
        npos = np.rint(P[lo + k] - P[lo]).astype(int); nneg = k - npos
        qc = q - np.median(xs)
        sp = (PX[lo + k] - PX[lo]) - npos * qc
        sn = (SX[lo + k] - SX[lo]) - (PX[lo + k] - PX[lo]) - nneg * qc
    mixed = (npos > 0) & (nneg > 0)
    S = 0.5 * (sp / np.maximum(npos, 1) + sn / np.maximum(nneg, 1))   # t_hat - query
    pred = np.where(mixed, np.where(S < 0, 1, -1), np.where(npos > 0, 1, -1))
    return pred, mixed


def excess_on_grid(pred, x, w, mu):
    wrong = pred != np.where(x > 0, 1, -1)
    return float(np.sum(w * np.abs(2 * eta(x, mu) - 1) * wrong))


def mean_se(v):
    v = np.asarray(v, float)
    return float(v.mean()), float(v.std(ddof=1) / np.sqrt(len(v)))


# ---------------------------------------------------------------- parts
def part_C():
    out = {}
    for mu in (MU_MAIN, MU_HARD):
        d = {"bayes": bayes(mu)}
        d["Rinf_nc"] = {str(k): Rinf_nc(k, mu) for k in (1, 2, 3, 4, 5, 10, 20, 50, 100, 1000)}
        d["Rinf_vote"] = {str(k): Rinf_vote(k, mu) for k in (1, 3, 5, 9, 21, 51)}
        d["Q"] = {str(r): heuristic_Q(r, mu) for r in (0.125, 0.25, 0.5, 0.75)}
        d["R_nc"] = {str(n): R_nc(n, mu) for n in (20, 80, 320, 2000, 20000)}
        out[f"{mu:.3f}"] = d
    return out


def part_L():
    """sign(x - t_r(x)) = sign(x) for the population local threshold on symmetric windows."""
    worst = np.inf; checked = 0
    for mu in (MU_MAIN, MU_HARD):
        for x in np.linspace(-4, 4, 161):
            if abs(x) < 1e-12:
                continue
            for r in (0.01, 0.1, 0.5, 1.0, 2.0, 5.0):
                mp = truncnorm(a=(x - r) - mu, b=(x + r) - mu, loc=mu).mean()
                mm = truncnorm(a=(x - r) + mu, b=(x + r) + mu, loc=-mu).mean()
                gap = np.sign(x) * (x - 0.5 * (mp + mm))
                worst = min(worst, gap / abs(x)); checked += 1
    return {"n_checked": checked, "min_signed_gap_over_abs_x": float(worst), "all_correct_sign": bool(worst > 0)}


def part_P1(rng):
    """Uninformative neighbourhoods: kNN in W (W in R^2 independent of (X_1, Y))."""
    rows = []
    reps, n_test = 1000, 100
    for mu in (MU_MAIN, MU_HARD):
        Rs = bayes(mu)
        for n in (80, 320):
            ks = sorted({1, 5, 20, n // 4, n})
            acc = {k: [] for k in ks}
            for _ in range(reps):
                X, y = sample(rng, n, 3, mu)
                Wt = rng.normal(size=(n_test, 2))
                idx = NearestNeighbors(n_neighbors=n).fit(X[:, 1:]).kneighbors(Wt, return_distance=False)
                for k in ks:
                    nb = idx[:, :k]; x1 = X[nb, 0]; pos = y[nb] == 1
                    npos = pos.sum(1); nneg = k - npos
                    with np.errstate(invalid="ignore", divide="ignore"):
                        t = 0.5 * ((x1 * pos).sum(1) / npos + (x1 * ~pos).sum(1) / nneg)
                    r = np.where((npos > 0) & (nneg > 0), risk_t(t, mu), 0.5)
                    acc[k].append(float(r.mean()))
            for k in ks:
                m, se = mean_se(acc[k])
                ex = R_nc(k, mu)
                rows.append({"mu": mu, "n": n, "k": k, "mc": m, "se": se, "exact_R_nc_k": ex,
                             "z": (m - ex) / se if se > 0 else 0.0,
                             "excess_ratio_exact": (ex - Rs) / (R_nc(n, mu) - Rs)})
    # linear SVM on X_1 only (C = 1), kNN in W ; against a Monte Carlo learning curve
    svm_rows = []
    mu, n = MU_MAIN, 320
    for k in (10, 40):
        loc = []
        for _ in range(600):          # many training sets: the per-fit risk is heavy-tailed
            X, y = sample(rng, n, 3, mu)
            Wt = rng.normal(size=(10, 2))
            idx = NearestNeighbors(n_neighbors=k).fit(X[:, 1:]).kneighbors(Wt, return_distance=False)
            rr = []
            for i in range(len(Wt)):
                nb = idx[i]
                if np.all(y[nb] == y[nb][0]):
                    rr.append(0.5)
                else:
                    m = SVC(kernel="linear", C=1.0).fit(X[nb, :1], y[nb])
                    rr.append(float(risk_lin1(m.coef_[0, 0], m.intercept_[0], mu)))
            loc.append(np.mean(rr))
        curve = []
        for _ in range(8000):
            X, y = sample(rng, k, 1, mu)
            if np.all(y == y[0]):
                curve.append(0.5)
            else:
                m = SVC(kernel="linear", C=1.0).fit(X, y)
                curve.append(float(risk_lin1(m.coef_[0, 0], m.intercept_[0], mu)))
        lm, ls = mean_se(loc); cm, cs = mean_se(curve)
        svm_rows.append({"mu": mu, "n": n, "k": k, "localised_mc": lm, "localised_se": ls,
                         "curve_mc": cm, "curve_se": cs, "z": (lm - cm) / np.hypot(ls, cs)})
    gl = []
    for _ in range(1000):
        X, y = sample(rng, n, 1, mu)
        m = SVC(kernel="linear", C=1.0).fit(X, y)
        gl.append(float(risk_lin1(m.coef_[0, 0], m.intercept_[0], mu)))
    gm, gs = mean_se(gl)
    return {"nc": rows, "svm": svm_rows, "svm_global_n320": {"mc": gm, "se": gs},
            "reps": reps, "n_test": n_test}


def part_P2(rng):
    """Informative neighbourhoods, k fixed, nc rule."""
    rows = []
    for mu in (MU_MAIN, MU_HARD):
        Rs = bayes(mu)
        x, w = make_grid(mu, fine=1.0, n_fine=2000, n_coarse=4000)
        for n in (320, 2000, 20000):
            reps = 200
            ks = (1, 2, 3, 5, 10, 20)
            acc = {k: [] for k in ks}
            for _ in range(reps):
                X, y = sample(rng, n, 1, mu)
                o = np.argsort(X[:, 0]); xs = X[o, 0]; ys = y[o]
                for k in ks:
                    pred, _ = loc_nc_pred_1d(xs, ys, x, k)
                    acc[k].append(excess_on_grid(pred, x, w, mu))
            for k in ks:
                m, se = mean_se(acc[k])
                rows.append({"mu": mu, "d": 1, "n": n, "k": k, "risk_mc": Rs + m, "se": se,
                             "Rinf_nc_k": Rinf_nc(k, mu), "R_nc_n": R_nc(n, mu),
                             "excess_ratio_vs_global": m / (R_nc(n, mu) - Rs)})
    # neighbourhoods in all d coordinates (W irrelevant), nc on X_1, Monte Carlo test points
    rows_d = []
    mu = MU_MAIN; Rs = bayes(mu)
    for d in (2, 5):
        for n in (320, 2000):
            acc = {k: [] for k in (3, 10)}
            for _ in range(100):
                X, y = sample(rng, n, d, mu)
                Xt, _ = sample(rng, 1000, d, mu)
                idx = NearestNeighbors(n_neighbors=10).fit(X).kneighbors(Xt, return_distance=False)
                for k in acc:
                    nb = idx[:, :k]; D = X[nb, 0] - Xt[:, :1]; pos = y[nb] == 1
                    npos = pos.sum(1); nneg = k - npos
                    S = 0.5 * ((D * pos).sum(1) / np.maximum(npos, 1) + (D * ~pos).sum(1) / np.maximum(nneg, 1))
                    mixed = (npos > 0) & (nneg > 0)
                    pred = np.where(mixed, np.where(S < 0, 1, -1), np.where(npos > 0, 1, -1))
                    wrong = pred != np.where(Xt[:, 0] > 0, 1, -1)
                    acc[k].append(float(np.mean(np.abs(2 * eta(Xt[:, 0], mu) - 1) * wrong)))
            for k in acc:
                m, se = mean_se(acc[k])
                rows_d.append({"mu": mu, "d": d, "n": n, "k": k, "risk_mc": Rs + m, "se": se,
                               "Rinf_nc_k": Rinf_nc(k, mu), "R_nc_n": R_nc(n, mu)})
    return {"d1": rows, "dall": rows_d}


def part_P3(rng):
    """Informative neighbourhoods, k fixed, local linear SVM (C = 1) in d = 1."""
    mu, C = MU_MAIN, 1.0
    Rs = bayes(mu)
    rows = []
    lemma_checked = 0; lemma_ok = 0
    for n in (320, 2000):
        for k in (1, 3, 5, 9):
            r0 = 1.0 / (k * np.sqrt(2 * C * k))      # Lemma lem:majority
            acc, frac_vote = [], []
            for _ in range(25):
                X, y = sample(rng, n, 1, mu)
                Xt, _ = sample(rng, 400, 1, mu)
                dist, idx = NearestNeighbors(n_neighbors=k).fit(X).kneighbors(Xt)
                pred = np.empty(len(Xt), dtype=int); agree = 0
                for i in range(len(Xt)):
                    nb = idx[i]; yl = y[nb]
                    vote = 1 if yl.sum() > 0 else -1
                    if np.all(yl == yl[0]):
                        pred[i] = yl[0]
                    else:
                        m = SVC(kernel="linear", C=C).fit(X[nb], yl)
                        pred[i] = 1 if float(m.decision_function(Xt[i:i + 1])[0]) > 0 else -1
                        if dist[i, -1] < r0:
                            lemma_checked += 1; lemma_ok += int(pred[i] == vote)
                    agree += int(pred[i] == vote)
                wrong = pred != np.where(Xt[:, 0] > 0, 1, -1)
                acc.append(float(np.mean(np.abs(2 * eta(Xt[:, 0], mu) - 1) * wrong)))
                frac_vote.append(agree / len(Xt))
            m, se = mean_se(acc)
            rows.append({"mu": mu, "n": n, "k": k, "C": C, "risk_mc": Rs + m, "se": se,
                         "Rinf_vote_k": Rinf_vote(k, mu), "frac_pred_equals_vote": float(np.mean(frac_vote)),
                         "r0": r0})
    gl = {}
    for n in (320, 2000):
        v = []
        for _ in range(300):
            X, y = sample(rng, n, 1, mu)
            m = SVC(kernel="linear", C=C).fit(X, y)
            v.append(float(risk_lin1(m.coef_[0, 0], m.intercept_[0], mu)))
        gm, gs = mean_se(v)
        gl[str(n)] = {"mc": gm, "se": gs}
    return {"rows": rows, "global_svm": gl, "lemma_queries_checked": lemma_checked,
            "lemma_queries_majority": lemma_ok}


def part_P4(rng):
    """Informative neighbourhoods, k = rho n, nc rule (d = 1): excess ratio vs Q(rho)."""
    rows = []
    for mu in (MU_MAIN, MU_HARD):
        Rs = bayes(mu)
        x, w = make_grid(mu, fine=1.0, n_fine=10000, n_coarse=4000)
        for n in (2000, 8000, 32000):
            for rho in (0.25, 0.5, 1.0):
                k = int(round(rho * n))
                acc = []
                for _ in range(600):
                    X, y = sample(rng, n, 1, mu)
                    o = np.argsort(X[:, 0])
                    pred, _ = loc_nc_pred_1d(X[o, 0], y[o], x, k)
                    acc.append(excess_on_grid(pred, x, w, mu))
                m, se = mean_se(acc)
                g = R_nc(n, mu) - Rs
                rows.append({"mu": mu, "n": n, "rho": rho, "k": k, "excess_mc": m, "se": se,
                             "global_excess_exact": g, "ratio": m / g, "ratio_se": se / g,
                             "Q_heuristic": heuristic_Q(rho, mu)["Q"], "thinning_1_over_rho": 1.0 / rho})
    return rows


def fmt_report(res):
    L = []
    L.append("SVMF001 -- check_knn_localisation.py   (seed %d)" % SEED)
    for mu_s, d in res["constants"].items():
        L.append(f"\n[C] mu = {mu_s}: Bayes risk {d['bayes']:.5f}")
        L.append("    k-fixed limit, local nearest centroid  Rinf_nc(k): " +
                 ", ".join(f"k={k}: {v:.5f}" for k, v in d["Rinf_nc"].items()))
        L.append("    k-fixed limit, local linear SVM = vote Rinf_vote(k): " +
                 ", ".join(f"k={k}: {v:.5f}" for k, v in d["Rinf_vote"].items()))
        L.append("    exact global R_nc(n): " + ", ".join(f"n={k}: {v:.6f}" for k, v in d["R_nc"].items()))
        L.append("    heuristic Q(rho) = 1/(rho v): " +
                 ", ".join(f"rho={k}: r={v['r']:.3f} v={v['v']:.4f} Q={v['Q']:.3f}" for k, v in d["Q"].items()))
    l = res["lemma_population_sign"]
    L.append(f"\n[L] population local threshold has the Bayes sign at {l['n_checked']} (x, r) pairs: "
             f"{l['all_correct_sign']} (min sign(x)(x - t_r(x))/|x| = {l['min_signed_gap_over_abs_x']:.3e})")
    L.append("\n[P1] uninformative neighbourhoods (kNN in W), nearest centroid: MC vs exact R_nc(k)")
    for r in res["P1"]["nc"]:
        L.append(f"    mu={r['mu']:.3f} n={r['n']:4d} k={r['k']:4d}: MC {r['mc']:.6f} +- {r['se']:.6f}  exact {r['exact_R_nc_k']:.6f}"
                 f"  z={r['z']:+.2f}  excess ratio vs k=n {r['excess_ratio_exact']:.3f}")
    L.append("    linear SVM on X_1 (C=1): localised (kNN in W) vs learning curve at k (both MC)")
    for r in res["P1"]["svm"]:
        L.append(f"    n={r['n']} k={r['k']}: localised {r['localised_mc']:.5f} +- {r['localised_se']:.5f}"
                 f"  curve {r['curve_mc']:.5f} +- {r['curve_se']:.5f}  z={r['z']:+.2f}")
    g = res["P1"]["svm_global_n320"]
    L.append(f"    global linear SVM on X_1, n=320: {g['mc']:.5f} +- {g['se']:.5f}")
    L.append("\n[P2] informative neighbourhoods (kNN in X_1, d=1), k fixed, nearest centroid")
    for r in res["P2"]["d1"]:
        L.append(f"    mu={r['mu']:.3f} n={r['n']:6d} k={r['k']:3d}: risk {r['risk_mc']:.5f} +- {r['se']:.5f}"
                 f"  limit Rinf_nc {r['Rinf_nc_k']:.5f}  global R_nc(n) {r['R_nc_n']:.6f}")
    L.append("    neighbourhoods in all d coordinates (nc on X_1)")
    for r in res["P2"]["dall"]:
        L.append(f"    d={r['d']} n={r['n']:5d} k={r['k']:3d}: risk {r['risk_mc']:.5f} +- {r['se']:.5f}"
                 f"  limit Rinf_nc {r['Rinf_nc_k']:.5f}  global R_nc(n) {r['R_nc_n']:.6f}")
    L.append("\n[P3] informative neighbourhoods (d=1), k fixed, local linear SVM C=1")
    for r in res["P3"]["rows"]:
        L.append(f"    n={r['n']:5d} k={r['k']}: risk {r['risk_mc']:.5f} +- {r['se']:.5f}  limit Rinf_vote {r['Rinf_vote_k']:.5f}"
                 f"  P(pred = local majority) {r['frac_pred_equals_vote']:.4f}")
    for n, g in res["P3"]["global_svm"].items():
        L.append(f"    global linear SVM d=1 n={n}: {g['mc']:.5f} +- {g['se']:.5f}")
    L.append(f"    majority lemma (radius < r0): {res['P3']['lemma_queries_majority']} of "
             f"{res['P3']['lemma_queries_checked']} mixed queries predicted the majority")
    L.append("\n[P4] informative neighbourhoods (d=1), k = rho n, nearest centroid: excess ratio vs global")
    for r in res["P4"]:
        L.append(f"    mu={r['mu']:.3f} n={r['n']:5d} rho={r['rho']:.2f}: excess {r['excess_mc']:.3e} +- {r['se']:.1e}"
                 f"  ratio {r['ratio']:.3f} +- {r['ratio_se']:.3f}  Q(rho) {r['Q_heuristic']:.3f}  1/rho {r['thinning_1_over_rho']:.2f}")
    L.append(f"\nCPU seconds: {res['meta']['cpu_seconds']:.1f}")
    return "\n".join(L)


def _sig(x, sig=3):
    """Format with `sig` significant digits, no exponent (for ratios)."""
    if x == 0:
        return "0"
    from math import floor, log10
    dec = max(0, sig - 1 - int(floor(log10(abs(x)))))
    return f"{x:.{dec}f}"


def _thou(n):
    s = f"{int(n):,}"
    return s.replace(",", "\\,")


def make_macros(res):
    """Macro name -> LaTeX string, all derived from the results dict (no typed numbers)."""
    M = {}
    mm = f"{res['meta']['mu_main']:.3f}"; mh = f"{res['meta']['mu_hard']:.3f}"
    cm, ch = res["constants"][mm], res["constants"][mh]
    M["KLSeed"] = str(res["meta"]["seed"])
    M["KLCpu"] = f"{res['meta']['cpu_seconds']:.0f}"
    M["KLMuHard"] = f"{res['meta']['mu_hard']:g}"
    nc = res["P1"]["nc"]
    row = {(r["mu"], r["n"], r["k"]): r for r in nc}
    mu0 = res["meta"]["mu_main"]
    for k, name in ((5, "Five"), (20, "Twenty"), (80, "Eighty")):
        M[f"KLSelRatio{name}"] = _sig(row[(mu0, 320, k)]["excess_ratio_exact"])
    M["KLSelReps"] = _thou(res["P1"]["reps"])
    sel = [r for r in nc if 1 < r["k"] <= r["n"]]
    M["KLSelNRows"] = str(len(sel))
    M["KLSelMaxZ"] = f"{max(abs(r['z']) for r in sel):.1f}"
    s40 = [r for r in res["P1"]["svm"] if r["k"] == 40][0]
    M["KLSelSvmLoc"] = f"{s40['localised_mc']:.5f}"; M["KLSelSvmLocSe"] = f"{s40['localised_se']:.5f}"
    M["KLSelSvmCurve"] = f"{s40['curve_mc']:.5f}"; M["KLSelSvmCurveSe"] = f"{s40['curve_se']:.5f}"
    for k, name in ((1, "One"), (3, "Three"), (5, "Five"), (10, "Ten"), (20, "Twenty")):
        M[f"KLLimNc{name}"] = f"{cm['Rinf_nc'][str(k)]:.4f}"
        M[f"KLLimNc{name}Hard"] = f"{ch['Rinf_nc'][str(k)]:.4f}"
    for k, name in ((3, "Three"), (9, "Nine")):
        M[f"KLLimVote{name}"] = f"{cm['Rinf_vote'][str(k)]:.4f}"
    d1 = res["P2"]["d1"]
    nbig = max(r["n"] for r in d1)
    M["KLPtwoNBig"] = _thou(nbig)
    M["KLPtwoMaxZ"] = f"{max(abs(r['risk_mc'] - r['Rinf_nc_k']) / r['se'] for r in d1 if r['n'] == nbig and r['k'] <= 5):.1f}"
    M["KLPtwoMaxDiff"] = f"{max(abs(r['risk_mc'] - r['Rinf_nc_k']) for r in d1 if r['n'] == nbig):.4f}"
    M["KLPtwoNRows"] = str(len(d1))
    M["KLPtwoMinGap"] = f"{min(r['risk_mc'] - r['R_nc_n'] for r in d1):.3f}"
    M["KLPtwoReps"] = "200"
    dall = [r for r in res["P2"]["dall"] if r["n"] == 2000]
    M["KLPtwoDallMin"] = f"{min(r['risk_mc'] for r in dall):.3f}"
    M["KLPtwoDallMax"] = f"{max(r['risk_mc'] for r in dall):.3f}"
    p3 = res["P3"]
    assert p3["lemma_queries_checked"] == p3["lemma_queries_majority"]
    M["KLMajChecked"] = _thou(p3["lemma_queries_checked"])
    r3 = [r for r in p3["rows"] if r["n"] == 2000 and r["k"] == 3][0]
    M["KLPthreeKThree"] = f"{r3['risk_mc']:.4f}"; M["KLPthreeKThreeSe"] = f"{r3['se']:.4f}"
    g = p3["global_svm"]["2000"]
    M["KLPthreeGlobal"] = f"{g['mc']:.5f}"; M["KLPthreeGlobalSe"] = f"{g['se']:.5f}"
    M["KLQHalf"] = f"{cm['Q']['0.5']['Q']:.2f}"; M["KLQHalfHard"] = f"{ch['Q']['0.5']['Q']:.1f}"
    M["KLQQuarter"] = f"{cm['Q']['0.25']['Q']:.1f}"
    M["KLQQuarterHard"] = f"{ch['Q']['0.25']['Q']:.1f}"
    p4 = res["P4"]
    nb4 = max(r["n"] for r in p4)
    M["KLPfourNBig"] = _thou(nb4)
    def r4(mu, n, rho):
        return [r for r in p4 if r["mu"] == mu and r["n"] == n and r["rho"] == rho][0]
    a = r4(mu0, nb4, 0.5); M["KLRatioHalfMain"] = f"{a['ratio']:.2f}"; M["KLRatioHalfMainSe"] = f"{a['ratio_se']:.2f}"
    a = r4(res["meta"]["mu_hard"], nb4, 0.5); M["KLRatioHalfHard"] = f"{a['ratio']:.1f}"; M["KLRatioHalfHardSe"] = f"{a['ratio_se']:.1f}"
    for n, tag in ((2000, "A"), (8000, "B"), (nb4, "C")):
        a = r4(mu0, n, 0.25)
        M[f"KLRatioQuarterMain{tag}"] = f"{a['ratio']:.0f}\\pm{a['ratio_se']:.0f}"
    a = r4(res["meta"]["mu_hard"], nb4, 0.25)
    M["KLRatioQuarterHardC"] = f"{a['ratio']:.0f}\\pm{a['ratio_se']:.0f}"
    return M


def write_macros():
    path = os.path.join(HERE, "knn_localisation_results.json")
    with open(path) as f:
        res = json.load(f)
    M = make_macros(res)
    res["macros"] = M
    with open(path, "w") as f:
        json.dump(res, f, indent=1)
    lines = ["% generated by theory/check_knn_localisation.py --macros from knn_localisation_results.json"]
    lines += [f"\\newcommand{{\\{k}}}{{{v}}}" for k, v in M.items()]
    print("\n".join(lines))


def main():
    rng = np.random.default_rng(SEED)
    res = {"meta": {"seed": SEED, "mu_main": MU_MAIN, "mu_hard": MU_HARD, "python": platform.python_version(),
                    "numpy": np.__version__, "scipy": scipy.__version__, "sklearn": sklearn.__version__}}
    res["constants"] = part_C()
    res["lemma_population_sign"] = part_L()
    res["P1"] = part_P1(rng)
    res["P2"] = part_P2(rng)
    res["P3"] = part_P3(rng)
    res["P4"] = part_P4(rng)
    res["meta"]["cpu_seconds"] = time.process_time() - T0
    with open(os.path.join(HERE, "knn_localisation_results.json"), "w") as f:
        json.dump(res, f, indent=1)
    print(fmt_report(res))


if __name__ == "__main__":
    if "--macros" in sys.argv:
        write_macros()
    elif "--report" in sys.argv:
        with open(os.path.join(HERE, "knn_localisation_results.json")) as f:
            print(fmt_report(json.load(f)))
    else:
        main()
