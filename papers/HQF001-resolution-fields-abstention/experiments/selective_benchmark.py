#!/usr/bin/env python3
"""HQF001 -- Selective classification benchmark: anisotropic resolution field vs references.

Every number in the manuscript comes from results/results.json written by this script.
Seed is fixed. Runs single-threaded (BLAS threads limited) so that CPU time ~ wall time.

Usage: python3 selective_benchmark.py [--fast] [--resummarise]

v0.2 (2026-10-03, after internal review round 1): every paired comparison is reported with
three 95 % intervals (percentile bootstrap over folds, the predefined one; Student t over
folds; t with the Nadeau-Bengio variance correction), wins/ties/losses and a borderline
flag; each pair has its own seeded generator and the "best reference" comparison is a copy
of the direct one; B = 20000; synth-classcov uses a covariance spectrum for which the
Bayes-error calibration has a solution (v0.1 hit the lower bound: coinciding means);
inner-CV configurations that fail on some inner fold are discarded.

v0.3 (2026-10-03, after internal review round 2; preregistered in PREREGISTRO_HQF001_rejilla_20261003.md):
the field grid is widened from K_m in {20, 40, 80}, alpha in {0.05, 0.2, 0.5} (FIELD_GRID_V02) to
K_m in {20, 40, 80, 160, 320}, alpha in {0.05, 0.2, 0.5, 0.7, 0.9}, because the v0.2 selection sat on the
upper edge of the grid in most folds of several datasets; nominal K_m values that the cap
min(K_m, n_train - 1) makes identical are listed largest first, so that among identical inner
configurations the largest nominal value is kept (on iris, "all 79 inner points" then maps to "all 119
outer points" instead of "80 of 120"); the fraction of folds whose selected hyper-parameter lies on an
edge of its grid is stored ("saturation") and tabulated. References, folds, seeds, inner CV, intervals and
the criterion are unchanged.
"""
import os
os.environ.setdefault("OMP_NUM_THREADS", "1")
os.environ.setdefault("OPENBLAS_NUM_THREADS", "1")
os.environ.setdefault("MKL_NUM_THREADS", "1")

import argparse
import json
import platform
import time
import warnings
import zlib

import numpy as np
import scipy
import sklearn
from scipy.stats import t as t_dist
from scipy.stats import wilcoxon
from sklearn import datasets
from sklearn.decomposition import PCA
from sklearn.discriminant_analysis import (LinearDiscriminantAnalysis,
                                           QuadraticDiscriminantAnalysis)
from sklearn.ensemble import RandomForestClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import RepeatedStratifiedKFold, StratifiedKFold
from sklearn.neighbors import NearestNeighbors
from sklearn.preprocessing import StandardScaler

warnings.filterwarnings("ignore")

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
SEED = 20260930
SCRIPT_VERSION = "v0.3 (2026-10-03)"
CRITERION_TEXT = ("residual gain = AURC of the field lower than that of the best reference (lowest mean AURC "
                  "among the references on that dataset) on a majority (>= n//2 + 1 of n datasets) of datasets, "
                  "with the paired 95% percentile-bootstrap interval over folds excluding zero; "
                  "see CRITERIO_HQF001.md")
COVERAGE_GRID = np.linspace(0.02, 1.0, 50)
BIG = 1e12  # finite stand-in for "infinitely confident"

# ----------------------------------------------------------------------------
# Selective-classification metrics (expected value under uniform tie-breaking)
# ----------------------------------------------------------------------------

def rc_curve(score, correct):
    """Risk-coverage curve. Returns coverage (i/n) and expected selective risk
    when points are accepted in decreasing order of `score`, ties broken
    uniformly at random (expectation taken exactly, block by block)."""
    score = np.asarray(score, float)
    correct = np.asarray(correct, bool)
    order = np.argsort(-score, kind="mergesort")
    s = score[order]
    err = (~correct[order]).astype(float)
    n = len(s)
    change = np.r_[True, s[1:] != s[:-1]]
    block = np.cumsum(change) - 1
    nb = block[-1] + 1
    size = np.bincount(block, minlength=nb).astype(float)
    berr = np.bincount(block, weights=err, minlength=nb)
    rate = berr / size
    start = np.cumsum(size) - size
    prev = np.cumsum(berr) - berr
    i = np.arange(1, n + 1, dtype=float)
    exp_cum = prev[block] + (i - start[block]) * rate[block]
    return i / n, exp_cum / i


def aurc(score, correct):
    _, risk = rc_curve(score, correct)
    return float(risk.mean())


def selective_accuracy(score, correct, coverage):
    _, risk = rc_curve(score, correct)
    k = max(1, int(np.ceil(coverage * len(risk))))
    return float(1.0 - risk[k - 1])


def curve_on_grid(score, correct):
    cov, risk = rc_curve(score, correct)
    idx = np.clip(np.ceil(COVERAGE_GRID * len(risk)).astype(int) - 1, 0, len(risk) - 1)
    return risk[idx]


def finite(x):
    x = np.asarray(x, float).copy()
    x[np.isposinf(x)] = BIG
    x[np.isneginf(x)] = -BIG
    x[np.isnan(x)] = -BIG
    return x

# ----------------------------------------------------------------------------
# Datasets
# ----------------------------------------------------------------------------

def _rand_rot(rng, d):
    q, r = np.linalg.qr(rng.standard_normal((d, d)))
    return q * np.sign(np.diag(r))


def _gauss_bayes_error(rng, means, covs, priors, n=40000):
    """Monte-Carlo Bayes error of a Gaussian mixture classifier (true posteriors)."""
    K = len(means)
    counts = rng.multinomial(n, priors)
    X = np.vstack([rng.multivariate_normal(means[c], covs[c], counts[c]) for c in range(K)])
    logp = np.empty((n, K))
    for c in range(K):
        Ci = np.linalg.inv(covs[c])
        diff = X - means[c]
        logp[:, c] = (np.log(priors[c]) - 0.5 * np.einsum("nd,de,ne->n", diff, Ci, diff)
                      - 0.5 * np.linalg.slogdet(covs[c])[1])
    logp -= logp.max(1, keepdims=True)
    p = np.exp(logp)
    p /= p.sum(1, keepdims=True)
    return float(np.mean(1.0 - p.max(1)))


def _calibrate_shift(rng, dirs, covs, priors, target=0.10):
    """Scale the class-mean directions so that the Bayes error is `target`, by bisection on
    [0.05, 20]. Returns (shift, at_bound): at_bound is True when the bisection converged to an
    end of the interval, i.e. there is no solution inside it (for the lower bound: the
    covariances alone already separate the classes better than `target`)."""
    lo0, hi0 = 0.05, 20.0
    lo, hi = lo0, hi0
    for _ in range(40):
        mid = 0.5 * (lo + hi)
        e = _gauss_bayes_error(np.random.default_rng(rng.integers(2**31)), dirs * mid, covs, priors)
        if e > target:
            lo = mid
        else:
            hi = mid
    shift = 0.5 * (lo + hi)
    at_bound = bool(shift - lo0 < 1e-6 or hi0 - shift < 1e-6)
    return shift, at_bound


def make_datasets(seed, fast=False):
    rng = np.random.default_rng(seed)
    D = {}
    X, y = datasets.load_iris(return_X_y=True)
    D["iris"] = dict(X=X, y=y, pca=None, kind="real")
    X, y = datasets.load_wine(return_X_y=True)
    D["wine"] = dict(X=X, y=y, pca=None, kind="real")
    X, y = datasets.load_breast_cancer(return_X_y=True)
    D["breast_cancer"] = dict(X=X, y=y, pca=None, kind="real")
    X, y = datasets.load_digits(return_X_y=True)
    D["digits"] = dict(X=X, y=y, pca=20, kind="real")

    n = 1200
    # S1: informative + redundant features
    X, y = datasets.make_classification(n_samples=n, n_features=10, n_informative=5, n_redundant=3,
                                        n_repeated=0, n_classes=2, n_clusters_per_class=2,
                                        flip_y=0.03, class_sep=0.8, random_state=seed)
    D["synth_informative"] = dict(X=X, y=y, pca=None, kind="synthetic",
                                  note="make_classification(10 features: 5 informative, 3 redundant, 2 noise; 2 clusters/class; flip_y=0.03; class_sep=0.8)")
    # S2: two moons with anisotropic Gaussian noise plus 3 nuisance dimensions
    X, y = datasets.make_moons(n_samples=n, noise=0.0, random_state=seed)
    th = np.deg2rad(30.0)
    R = np.array([[np.cos(th), -np.sin(th)], [np.sin(th), np.cos(th)]])
    Cn = R @ np.diag([0.30 ** 2, 0.06 ** 2]) @ R.T
    X = X + rng.multivariate_normal(np.zeros(2), Cn, n)
    X = np.hstack([X, rng.standard_normal((n, 3))])
    D["moons_aniso"] = dict(X=X, y=y, pca=None, kind="synthetic",
                            note="two moons + anisotropic Gaussian noise (sd 0.30 x 0.06, rotated 30 deg) + 3 nuisance N(0,1) dimensions",
                            noise_cov=Cn.tolist())
    # S3: class-dependent covariance (QDA regime): two random rotations of one covariance spectrum,
    # mean shift calibrated to a 10% Bayes error. v0.1 used the spectrum (2, 1, 0.5, 0.25, 0.1, 0.05),
    # for which the rotated covariances alone separate the classes with a 7.7% Bayes error, so the
    # bisection stopped at its lower bound (shift 0.05: coinciding means). v0.2 uses the less disparate
    # spectrum geomspace(2, 0.25, 6) (about 20% Bayes error with coinciding means), for which the
    # calibration has a solution. The rotations and every other draw are unchanged (same RNG consumption).
    d = 6
    eig = np.geomspace(2.0, 0.25, d)
    Q0, Q1 = _rand_rot(rng, d), _rand_rot(rng, d)
    covs = [Q0 @ np.diag(eig) @ Q0.T, Q1 @ np.diag(eig) @ Q1.T]
    u = rng.standard_normal(d)
    u /= np.linalg.norm(u)
    dirs = np.vstack([np.zeros(d), u])
    priors = np.array([0.5, 0.5])
    scale, at_bound = _calibrate_shift(rng, dirs, covs, priors)
    means = dirs * scale
    counts = rng.multinomial(n, priors)
    X = np.vstack([rng.multivariate_normal(means[c], covs[c], counts[c]) for c in range(2)])
    y = np.repeat(np.arange(2), counts)
    be = _gauss_bayes_error(rng, means, covs, priors)
    D["synth_classcov"] = dict(X=X, y=y, pca=None, kind="synthetic",
                               note="two Gaussians in d=6 with different (rotated) covariances sharing the eigenvalues geomspace(2, 0.25, 6); mean shift chosen by bisection in [0.05, 20] towards a 10% Bayes error (v0.1 used eigenvalues 2, 1, 0.5, 0.25, 0.1, 0.05 and the bisection hit the lower bound: coinciding means, Bayes error 7.7%)",
                               bayes_error=be, shift=scale, shift_at_bound=at_bound)
    # S4: shared covariance, three classes (LDA regime), Bayes error calibrated to 10%
    Q = _rand_rot(rng, d)
    Sig = Q @ np.diag(np.geomspace(2.0, 0.05, d)) @ Q.T
    dirs = rng.standard_normal((3, d))
    dirs -= dirs.mean(0)
    dirs /= np.linalg.norm(dirs, axis=1, keepdims=True)
    priors = np.array([1 / 3, 1 / 3, 1 / 3])
    covs = [Sig, Sig, Sig]
    scale, at_bound = _calibrate_shift(rng, dirs, covs, priors)
    means = dirs * scale
    counts = rng.multinomial(n, priors)
    X = np.vstack([rng.multivariate_normal(means[c], covs[c], counts[c]) for c in range(3)])
    y = np.repeat(np.arange(3), counts)
    be = _gauss_bayes_error(rng, means, covs, priors)
    D["synth_lda"] = dict(X=X, y=y, pca=None, kind="synthetic",
                          note="three Gaussians in d=6 with one shared covariance (eigenvalues geomspace(2, 0.05, 6)); mean shift chosen by bisection in [0.05, 20] towards a 10% Bayes error",
                          bayes_error=be, shift=scale, shift_at_bound=at_bound)
    if fast:
        for k in D:
            X, y = D[k]["X"], D[k]["y"]
            if len(y) > 600:
                idx = np.random.default_rng(seed).choice(len(y), 600, replace=False)
                D[k]["X"], D[k]["y"] = X[idx], y[idx]
    return D

# ----------------------------------------------------------------------------
# Methods. Each returns a list of (param_dict, pred, score) for its whole grid,
# sharing neighbour computations. Higher score = more confident.
# ----------------------------------------------------------------------------

def msp_output(clf, Xte, classes):
    P = clf.predict_proba(Xte)
    pred = clf.classes_[P.argmax(1)]
    return pred, P.max(1)


def m_knn(Xtr, ytr, Xte, grid):
    classes = np.unique(ytr)
    ks = [k for k in grid["k"] if k < len(ytr)]
    nn = NearestNeighbors(n_neighbors=max(ks)).fit(Xtr)
    dist, idx = nn.kneighbors(Xte)
    lab = ytr[idx]
    out = []
    for k in ks:
        for w in grid["weights"]:
            wt = np.ones((len(Xte), k)) if w == "uniform" else 1.0 / (dist[:, :k] + 1e-9)
            votes = np.zeros((len(Xte), len(classes)))
            for j, c in enumerate(classes):
                votes[:, j] = (wt * (lab[:, :k] == c)).sum(1)
            votes /= votes.sum(1, keepdims=True)
            out.append((dict(k=k, weights=w), classes[votes.argmax(1)], votes.max(1)))
    return out


def m_ncm(Xtr, ytr, Xte, grid):
    classes = np.unique(ytr)
    mu = np.vstack([Xtr[ytr == c].mean(0) for c in classes])
    d2 = ((Xte[:, None, :] - mu[None]) ** 2).sum(-1)
    o = np.sort(d2, 1)
    return [(dict(), classes[d2.argmin(1)], o[:, 1] - o[:, 0])]


def m_lda(Xtr, ytr, Xte, grid):
    out = []
    for sh in grid["shrinkage"]:
        clf = LinearDiscriminantAnalysis(solver="lsqr", shrinkage=sh).fit(Xtr, ytr)
        pred, sc = msp_output(clf, Xte, None)
        out.append((dict(shrinkage=str(sh)), pred, sc))
    return out


def m_qda(Xtr, ytr, Xte, grid):
    out = []
    for r in grid["reg_param"]:
        try:
            clf = QuadraticDiscriminantAnalysis(reg_param=r).fit(Xtr, ytr)
        except np.linalg.LinAlgError:
            continue  # singular class covariance at this regularisation: configuration skipped
        pred, sc = msp_output(clf, Xte, None)
        out.append((dict(reg_param=r), pred, sc))
    return out


def m_logreg(Xtr, ytr, Xte, grid):
    out = []
    for C in grid["C"]:
        clf = LogisticRegression(C=C, max_iter=3000).fit(Xtr, ytr)
        pred, sc = msp_output(clf, Xte, None)
        out.append((dict(C=C), pred, sc))
    return out


def m_rforest(Xtr, ytr, Xte, grid):
    out = []
    for leaf in grid["min_samples_leaf"]:
        clf = RandomForestClassifier(n_estimators=grid["n_estimators"], min_samples_leaf=leaf,
                                     max_features="sqrt", random_state=SEED, n_jobs=1).fit(Xtr, ytr)
        pred, sc = msp_output(clf, Xte, None)
        out.append((dict(min_samples_leaf=leaf), pred, sc))
    return out


def _sym_inv_sqrt(W):
    w, V = np.linalg.eigh(W)
    w = np.clip(w, 1e-12, None)
    return (V / np.sqrt(w)) @ V.T


def m_dann(Xtr, ytr, Xte, grid):
    """Discriminant adaptive nearest neighbours (Hastie & Tibshirani 1996), one iteration.
    Local metric Sigma = W^-1/2 [W^-1/2 B W^-1/2 + eps I] W^-1/2 from K_m Euclidean
    neighbours; then k-NN vote under Sigma among all training points."""
    classes = np.unique(ytr)
    d = Xtr.shape[1]
    cap = {km: min(km, len(ytr) - 1) for km in grid["K_m"]}   # nominal -> effective
    Kms = sorted(set(cap.values()))
    ks = [k for k in grid["k"] if k < len(ytr)]
    nn = NearestNeighbors(n_neighbors=max(Kms)).fit(Xtr)
    _, idx = nn.kneighbors(Xte)
    eps = grid["eps"]
    out = []
    for Km in Kms:
        noms = [km for km in grid["K_m"] if cap[km] == Km]
        # per-test-point transform L such that dist = ||(x - x_i) L||^2
        L = np.empty((len(Xte), d, d))
        for i in range(len(Xte)):
            P = Xtr[idx[i, :Km]]
            lab = ytr[idx[i, :Km]]
            m = P.mean(0)
            W = np.zeros((d, d))
            B = np.zeros((d, d))
            for c in classes:
                Pc = P[lab == c]
                if len(Pc) == 0:
                    continue
                mc = Pc.mean(0)
                Zc = Pc - mc
                W += Zc.T @ Zc
                B += len(Pc) * np.outer(mc - m, mc - m)
            W /= Km
            B /= Km
            W += (1e-3 * np.trace(W) / d + 1e-9) * np.eye(d)
            Wih = _sym_inv_sqrt(W)
            Bs = Wih @ B @ Wih
            Sigma = Wih @ (Bs + eps * np.eye(d)) @ Wih
            ev, V = np.linalg.eigh(Sigma)
            L[i] = V * np.sqrt(np.clip(ev, 0, None))
        # distances under Sigma to all training points, chunked
        D2 = np.empty((len(Xte), len(Xtr)))
        for a in range(0, len(Xte), 48):
            b = min(a + 48, len(Xte))
            Dif = Xtr[None, :, :] - Xte[a:b, None, :]
            T = np.einsum("ntd,nde->nte", Dif, L[a:b])
            D2[a:b] = (T ** 2).sum(-1)
        nn_idx = np.argsort(D2, axis=1)[:, :max(ks)]
        lab = ytr[nn_idx]
        for k in ks:
            votes = np.zeros((len(Xte), len(classes)))
            for j, c in enumerate(classes):
                votes[:, j] = (lab[:, :k] == c).sum(1)
            votes /= k
            for nom in noms:
                out.append((dict(K_m=nom, k=k), classes[votes.argmax(1)], votes.max(1)))
    return out


def m_field(Xtr, ytr, Xte, grid):
    """Anisotropic resolution field. At each test x: K_m Euclidean neighbours,
    local covariance C(x), shrunk S = (1-a) C + a (tr C / d) I, metric A = S^-1.
    Prototypes: mean of the neighbours of each class (nearest training point of the
    class if the class is absent from the neighbourhood). Score = Mahalanobis
    margin d^2_(2) - d^2_(1) under A. Variants share the same neighbourhoods."""
    classes = np.unique(ytr)
    K = len(classes)
    n_te, d = Xte.shape
    I = np.eye(d)
    cap = {km: min(km, len(ytr) - 1) for km in grid["K_m"]}   # nominal -> effective
    Kms = sorted(set(cap.values()))
    nn = NearestNeighbors(n_neighbors=max(Kms)).fit(Xtr)
    _, idx_all = nn.kneighbors(Xte)
    # nearest training point of each class (fallback prototype)
    fallback = np.empty((n_te, K, d))
    for j, c in enumerate(classes):
        nnc = NearestNeighbors(n_neighbors=1).fit(Xtr[ytr == c])
        _, ic = nnc.kneighbors(Xte)
        fallback[:, j] = Xtr[ytr == c][ic[:, 0]]
    gmu = np.vstack([Xtr[ytr == c].mean(0) for c in classes])  # global prototypes
    out = []
    for Km in Kms:
        # nominal values that the cap makes identical: largest first, so that the inner selection (which
        # keeps the first of equal inner AURCs) keeps the largest nominal K_m (v0.3)
        noms = sorted((km for km in grid["K_m"] if cap[km] == Km), reverse=True)
        idx = idx_all[:, :Km]
        P = Xtr[idx]
        lab = ytr[idx]
        Z = P - P.mean(1, keepdims=True)
        C = np.einsum("nkd,nke->nde", Z, Z) / max(Km - 1, 1)
        tau = np.trace(C, axis1=1, axis2=2) / d + 1e-12
        protos = fallback.copy()
        for j, c in enumerate(classes):
            mask = (lab == c)
            cnt = mask.sum(1)
            has = cnt > 0
            mc = (P * mask[..., None]).sum(1) / np.maximum(cnt, 1)[:, None]
            protos[has, j] = mc[has]
        diff = Xte[:, None, :] - protos            # (n, K, d)
        gdiff = Xte[:, None, :] - gmu[None]         # (n, K, d)

        def margin_pred(S, dif):
            Y = np.linalg.solve(S, dif.transpose(0, 2, 1))
            d2 = np.einsum("nkd,ndk->nk", dif, Y)
            o = np.argsort(d2, 1)
            first = d2[np.arange(n_te), o[:, 0]]
            second = d2[np.arange(n_te), o[:, 1]]
            return classes[o[:, 0]], second - first

        for a in grid["alpha"]:
            S = (1 - a) * C + a * tau[:, None, None] * I
            pred, marg = margin_pred(S, diff)
            logdet = np.linalg.slogdet(S)[1]
            ev = np.linalg.eigvalsh(S)
            kappa = np.log(ev[:, -1]) - np.log(np.clip(ev[:, 0], 1e-300, None))
            gpred, gmarg = margin_pred(S, gdiff)
            for nom in noms:
                out.append((dict(variant="aniso", K_m=nom, alpha=a), pred, marg))
                out.append((dict(variant="vol", K_m=nom, alpha=a), pred, -logdet))
                out.append((dict(variant="anis", K_m=nom, alpha=a), pred, -kappa))
                out.append((dict(variant="aniso_gproto", K_m=nom, alpha=a), gpred, gmarg))
        # isotropic field: A = (tr C / d)^-1 I  (alpha = 1)
        S = tau[:, None, None] * I[None]
        pred_i, marg_i = margin_pred(np.broadcast_to(S, (n_te, d, d)).copy(), diff)
        # local prototypes with the identity metric
        pred_e, marg_e = margin_pred(np.broadcast_to(I, (n_te, d, d)).copy(), diff)
        for nom in noms:
            out.append((dict(variant="iso", K_m=nom, alpha=1.0), pred_i, marg_i))
            out.append((dict(variant="euclid", K_m=nom, alpha=None), pred_e, marg_e))
    return out


# Field grid. v0.2 (the run of the predefined criterion, kept in results/v02/) used FIELD_GRID_V02;
# v0.3 widens it as preregistered in PREREGISTRO_HQF001_rejilla_20261003.md.
FIELD_GRID_V02 = dict(K_m=[20, 40, 80], alpha=[0.05, 0.2, 0.5])
FIELD_GRID = dict(K_m=[20, 40, 80, 160, 320], alpha=[0.05, 0.2, 0.5, 0.7, 0.9])


# Registry: name -> (function, grid, filter on params, group)
def build_methods(fast):
    ks = [3, 5, 7, 11, 15, 21, 31]
    M = {
        "kNN": (m_knn, dict(k=ks, weights=["uniform", "distance"]), None, "reference"),
        "NCM": (m_ncm, dict(), None, "reference"),
        "LDA": (m_lda, dict(shrinkage=[None, "auto"]), None, "reference"),
        "QDA": (m_qda, dict(reg_param=[0.01, 0.1, 0.5]), None, "reference"),
        "LogReg": (m_logreg, dict(C=[0.1, 1.0, 10.0]), None, "reference"),
        "RForest": (m_rforest, dict(n_estimators=100 if not fast else 50, min_samples_leaf=[1, 5]), None, "reference"),
        "DANN": (m_dann, dict(K_m=[50, 100], k=[5, 11, 21], eps=1.0), None, "reference"),
    }
    fgrid = dict(FIELD_GRID)
    for v, label in [("aniso", "Field-aniso"), ("iso", "Field-iso"), ("euclid", "Field-euclid"),
                     ("vol", "Field-vol"), ("anis", "Field-anis"), ("aniso_gproto", "Field-aniso-gproto")]:
        M[label] = (m_field, fgrid, v, "field")
    return M

# ----------------------------------------------------------------------------
# Tuning by inner CV on AURC, evaluation on the outer test fold
# ----------------------------------------------------------------------------

def run_grid(fn, grid, Xtr, ytr, Xte):
    return fn(Xtr, ytr, Xte, grid)


def evaluate_fold(Xtr, ytr, Xte, yte, methods, inner_seed):
    """Returns dict method -> metrics. Shared computation: each base function is
    run once per (inner) split for its whole grid; field variants are filtered."""
    inner = StratifiedKFold(n_splits=3, shuffle=True, random_state=inner_seed)
    splits = list(inner.split(Xtr, ytr))
    # group methods by base function
    by_fn = {}
    for name, (fn, grid, filt, group) in methods.items():
        by_fn.setdefault(id(fn), (fn, grid, []))[2].append((name, filt))
    results = {}
    for fn, grid, members in by_fn.values():
        # inner CV
        inner_scores = {}  # (name, key) -> list of aurc
        for tr, va in splits:
            outs = run_grid(fn, grid, Xtr[tr], ytr[tr], Xtr[va])
            for params, pred, score in outs:
                for name, filt in members:
                    if filt is not None and params.get("variant") != filt:
                        continue
                    key = json.dumps(params, sort_keys=True)
                    inner_scores.setdefault((name, key), []).append(aurc(finite(score), pred == ytr[va]))
        best = {}
        dropped = {}   # configurations that failed on some inner fold (e.g. QDA LinAlgError): not comparable
        for (name, key), vals in inner_scores.items():
            if len(vals) < len(splits):
                dropped[name] = dropped.get(name, 0) + 1
                continue
            m = float(np.mean(vals))
            if name not in best or m < best[name][1]:
                best[name] = (key, m)
        for name, _ in members:
            assert name in best, f"{name}: no configuration completed all {len(splits)} inner folds"
        # outer fit with the full training fold
        outs = run_grid(fn, grid, Xtr, ytr, Xte)
        for params, pred, score in outs:
            key = json.dumps(params, sort_keys=True)
            for name, filt in members:
                if best[name][0] != key:
                    continue
                sc = finite(score)
                corr = pred == yte
                results[name] = dict(
                    aurc=aurc(sc, corr),
                    acc=float(corr.mean()),
                    acc90=selective_accuracy(sc, corr, 0.90),
                    acc80=selective_accuracy(sc, corr, 0.80),
                    params=json.loads(key),
                    inner_aurc=best[name][1],
                    inner_configs_dropped=dropped.get(name, 0),
                    curve=curve_on_grid(sc, corr).tolist(),
                )
    missing = [m for m in methods if m not in results]
    assert not missing, f"no outer result for {missing}"
    return results

# ----------------------------------------------------------------------------
# Statistics
# ----------------------------------------------------------------------------

BOOT_B = 20000       # bootstrap replicates (v0.1: 2000)
BORDERLINE = 0.0002  # an interval end closer than this to zero (0.02 in AURC x 100) is flagged as borderline


def pair_rng(key):
    """One generator per comparison, seeded by the master seed and a CRC of the pair's name, so that
    the interval of a pair never depends on which other pairs were evaluated before it. (Python's
    hash() is salted per process and is not used.)"""
    return np.random.default_rng([SEED, zlib.crc32(key.encode("utf-8"))])


def pair_stats(diff, key, B=BOOT_B, rho=0.25, labels=("first better", "second better")):
    """Paired per-fold differences `diff` (first minus second; negative favours the first).
    Returns the mean; three 95 % intervals: percentile bootstrap over folds (the predefined one),
    Student t over folds (n-1 d.f.) and the t interval with the Nadeau-Bengio corrected variance
    (1/n + rho) s^2 with rho = n_test/n_train; wins/ties/losses over folds; a two-sided Wilcoxon
    signed-rank p-value (descriptive); a verdict under each interval; and a borderline flag when an
    end of the bootstrap or t interval is within BORDERLINE of zero."""
    diff = np.asarray(diff, float)
    n = len(diff)
    mean = float(diff.mean())
    idx = pair_rng(key).integers(0, n, size=(B, n))
    bm = diff[idx].mean(1)
    lo, hi = float(np.percentile(bm, 2.5)), float(np.percentile(bm, 97.5))
    sd = float(diff.std(ddof=1))
    q = float(t_dist.ppf(0.975, n - 1))
    t_lo, t_hi = mean - q * sd / np.sqrt(n), mean + q * sd / np.sqrt(n)
    nb_lo, nb_hi = mean - q * sd * np.sqrt(1.0 / n + rho), mean + q * sd * np.sqrt(1.0 / n + rho)
    try:
        p = float(wilcoxon(diff, zero_method="wilcox").pvalue) if np.any(diff != 0) else 1.0
    except ValueError:
        p = float("nan")

    def verdict(a, b):
        return labels[0] if b < 0 else labels[1] if a > 0 else "inconclusive"

    return dict(mean_diff=mean, ci_lo=lo, ci_hi=hi, t_lo=float(t_lo), t_hi=float(t_hi),
                nb_lo=float(nb_lo), nb_hi=float(nb_hi), wilcoxon_p=p,
                wins=int((diff < 0).sum()), ties=int((diff == 0).sum()), losses=int((diff > 0).sum()),
                verdict=verdict(lo, hi), verdict_t=verdict(t_lo, t_hi), verdict_nb=verdict(nb_lo, nb_hi),
                borderline=bool(min(abs(lo), abs(hi), abs(t_lo), abs(t_hi)) < BORDERLINE))


def _as_ablation(c):
    """Re-label a field-vs-reference comparison as an ablation entry (first = field, second = reference)."""
    out = dict(c)
    for k in ("verdict", "verdict_t", "verdict_nb"):
        out[k] = {"field better": "first better", "field worse": "second better"}.get(c[k], c[k])
    return out


ABLATION_PAIRS = [("Field-aniso", "Field-iso"), ("Field-aniso", "Field-euclid"), ("Field-iso", "Field-euclid"),
                  ("Field-aniso", "Field-vol"), ("Field-aniso", "Field-anis"), ("Field-aniso", "Field-aniso-gproto"),
                  ("Field-euclid", "NCM")]


def summarise(per_fold, methods, B=BOOT_B, n_splits=5, curves_from=None):
    """per_fold: dict dataset -> list of fold dicts (method -> metrics).
    curves_from: an earlier summary whose mean curves are reused when per-fold curves are absent."""
    refs = [m for m, v in methods.items() if v[3] == "reference"]
    rho = 1.0 / (n_splits - 1)   # n_test / n_train of a K-fold split (Nadeau-Bengio correction)
    summary = {}
    for ds, folds in per_fold.items():
        S = {"n_folds": len(folds), "methods": {}, "best_reference": None, "comparisons": {}}
        means = {}
        for m in methods:
            a = np.array([f[m]["aurc"] for f in folds])
            acc = np.array([f[m]["acc"] for f in folds])
            a90 = np.array([f[m]["acc90"] for f in folds])
            a80 = np.array([f[m]["acc80"] for f in folds])
            if curves_from is None:
                curve_mean = np.array([f[m]["curve"] for f in folds]).mean(0).tolist()
            else:
                curve_mean = curves_from[ds]["methods"][m]["curve_mean"]
            params = [json.dumps(f[m]["params"], sort_keys=True) for f in folds]
            uniq, cnt = np.unique(params, return_counts=True)
            S["methods"][m] = dict(
                aurc_mean=float(a.mean()), aurc_sd=float(a.std(ddof=1)),
                acc_mean=float(acc.mean()), acc_sd=float(acc.std(ddof=1)),
                acc90_mean=float(a90.mean()), acc80_mean=float(a80.mean()),
                error_rate=float(1 - acc.mean()),
                curve_mean=curve_mean,
                selected_params={str(u): int(c) for u, c in zip(uniq, cnt)},
                inner_configs_dropped=int(sum(f[m].get("inner_configs_dropped", 0) for f in folds)),
            )
            means[m] = float(a.mean())
        best_ref = min(refs, key=lambda m: means[m])
        S["best_reference"] = best_ref
        # each field variant vs every reference; "__best__" is a copy of the direct comparison with the
        # best reference (v0.1 resampled it separately, giving two intervals for the same pair)
        for m in methods:
            if methods[m][3] != "field":
                continue
            comp = {}
            for r in refs:
                diff = np.array([f[m]["aurc"] - f[r]["aurc"] for f in folds])
                comp[r] = dict(reference=r, **pair_stats(diff, f"{ds}|{m}|{r}", B, rho, ("field better", "field worse")))
            comp["__best__"] = dict(comp[best_ref])
            S["comparisons"][m] = comp
        # ablations; a pair whose second member is a reference copies the comparison above
        abl = {}
        for a_, b_ in ABLATION_PAIRS:
            if b_ in refs:
                abl[f"{a_} - {b_}"] = _as_ablation(S["comparisons"][a_][b_])
            else:
                diff = np.array([f[a_]["aurc"] - f[b_]["aurc"] for f in folds])
                abl[f"{a_} - {b_}"] = pair_stats(diff, f"{ds}|{a_}|{b_}", B, rho)
        S["ablations"] = abl
        summary[ds] = S
    # predefined criterion (bootstrap interval), plus the same count under the t and Nadeau-Bengio intervals
    crit = {}
    n_ds = len(summary)
    maj = n_ds // 2 + 1
    for m in methods:
        if methods[m][3] != "field":
            continue
        cb = {ds: summary[ds]["comparisons"][m]["__best__"] for ds in summary}

        def count(vkey):
            return dict(better=[ds for ds in cb if cb[ds][vkey] == "field better"],
                        worse=[ds for ds in cb if cb[ds][vkey] == "field worse"],
                        inconclusive=[ds for ds in cb if cb[ds][vkey] == "inconclusive"])

        c0 = count("verdict")
        crit[m] = dict(**c0, n_datasets=n_ds, majority_needed=maj, criterion_met=len(c0["better"]) >= maj,
                       t=count("verdict_t"), nb=count("verdict_nb"),
                       borderline=[ds for ds in cb if cb[ds]["borderline"]])
    return summary, crit

# ----------------------------------------------------------------------------
# Markdown report
# ----------------------------------------------------------------------------

def write_markdown(res, path):
    L = ["# HQF001 -- selective classification benchmark (generated by experiments/selective_benchmark.py)", ""]
    m = res["meta"]
    L.append(f"seed = {m['seed']}; fast = {m['fast']}; repeats x folds = {m['n_repeats']} x {m['n_splits']}; "
             f"CPU time = {m['cpu_seconds']:.1f} s; wall = {m['wall_seconds']:.1f} s")
    L.append("")
    L.append("## Datasets")
    L.append("")
    L.append("| dataset | n | d (after preprocessing) | classes | note |")
    L.append("|---|---|---|---|---|")
    for ds, info in res["datasets"].items():
        extra = ("" if info.get("bayes_error") is None else
                 f" Bayes error {100*info['bayes_error']:.2f}%; shift {info.get('shift')}; calibration at bound: {info.get('shift_at_bound')}.")
        L.append(f"| {ds} | {info['n']} | {info['d_used']} | {info['n_classes']} | {info.get('note', '')}{extra} |")
    L.append("")
    methods = list(res["methods_order"])
    L.append("## AURC x 100 (mean +- sd over folds; lower is better). The error rate x 100 (= AURC of a random ordering) is in the accuracy table below")
    L.append("")
    L.append("| dataset | " + " | ".join(methods) + " | best ref |")
    L.append("|---|" + "---|" * (len(methods) + 1))
    for ds, S in res["summary"].items():
        cells = []
        for mth in methods:
            v = S["methods"][mth]
            cells.append(f"{100*v['aurc_mean']:.2f} +- {100*v['aurc_sd']:.2f}")
        L.append(f"| {ds} | " + " | ".join(cells) + f" | {S['best_reference']} |")
    L.append("")
    L.append("## Accuracy x 100 at full coverage / 90% / 80% coverage")
    L.append("")
    L.append("| dataset | " + " | ".join(methods) + " |")
    L.append("|---|" + "---|" * len(methods))
    for ds, S in res["summary"].items():
        cells = []
        for mth in methods:
            v = S["methods"][mth]
            cells.append(f"{100*v['acc_mean']:.1f} / {100*v['acc90_mean']:.1f} / {100*v['acc80_mean']:.1f}")
        L.append(f"| {ds} | " + " | ".join(cells) + " |")
    L.append("")
    def cell(c):
        return (f"{100*c['mean_diff']:+.2f} boot[{100*c['ci_lo']:+.2f}, {100*c['ci_hi']:+.2f}] "
                f"t[{100*c['t_lo']:+.2f}, {100*c['t_hi']:+.2f}] NB[{100*c['nb_lo']:+.2f}, {100*c['nb_hi']:+.2f}] "
                f"W/T/L {c['wins']}/{c['ties']}/{c['losses']} p_W={c['wilcoxon_p']:.3f} "
                f"({c['verdict']}; t: {c['verdict_t']}; NB: {c['verdict_nb']}{'; BORDERLINE' if c['borderline'] else ''})")

    L.append("## Geometry-only scores: error rate x 100 of the variant's own tuned classifier (= expected AURC of a random ordering) and its AURC x 100")
    L.append("")
    L.append("| dataset | margin err | margin AURC | volume err | volume AURC | anisotropy err | anisotropy AURC |")
    L.append("|---|---|---|---|---|---|---|")
    for ds, S in res["summary"].items():
        cells = []
        for mth in ["Field-aniso", "Field-vol", "Field-anis"]:
            v = S["methods"][mth]
            cells.append(f"{100*v['error_rate']:.1f} | {100*v['aurc_mean']:.2f}")
        L.append(f"| {ds} | " + " | ".join(cells) + " |")
    L.append("")
    L.append("## Field variants vs best reference: paired difference of AURC x 100 (field - reference); 95% intervals: percentile bootstrap over folds (boot, predefined), Student t over folds (t), Nadeau-Bengio corrected t (NB); wins/ties/losses over folds; Wilcoxon p (descriptive)")
    L.append("")
    fields = [mm for mm in methods if mm.startswith("Field")]
    L.append("| dataset | best ref | " + " | ".join(fields) + " |")
    L.append("|---|---|" + "---|" * len(fields))
    for ds, S in res["summary"].items():
        L.append(f"| {ds} | {S['best_reference']} | " + " | ".join(cell(S["comparisons"][f]["__best__"]) for f in fields) + " |")
    L.append("")
    L.append("## Field-aniso vs each reference separately (same format)")
    L.append("")
    refs = [mm for mm in methods if not mm.startswith("Field")]
    L.append("| dataset | " + " | ".join(refs) + " |")
    L.append("|---|" + "---|" * len(refs))
    for ds, S in res["summary"].items():
        L.append(f"| {ds} | " + " | ".join(cell(S["comparisons"]["Field-aniso"][r]) for r in refs) + " |")
    L.append("")
    L.append("## Predefined criterion (better AURC than the best reference on a majority of datasets, paired 95% bootstrap CI excluding 0), and the same count under the t and Nadeau-Bengio intervals")
    L.append("")
    for f, c in res["criterion"].items():
        L.append(f"- {f}: better on {len(c['better'])}/{c['n_datasets']} {c['better']}; worse on {len(c['worse'])} {c['worse']}; "
                 f"inconclusive on {len(c['inconclusive'])} {c['inconclusive']}; criterion met: {c['criterion_met']}")
        L.append(f"  - t interval: better {len(c['t']['better'])} {c['t']['better']}; worse {len(c['t']['worse'])} {c['t']['worse']}; inconclusive {len(c['t']['inconclusive'])} {c['t']['inconclusive']}")
        L.append(f"  - Nadeau-Bengio: better {len(c['nb']['better'])} {c['nb']['better']}; worse {len(c['nb']['worse'])} {c['nb']['worse']}; inconclusive {len(c['nb']['inconclusive'])} {c['nb']['inconclusive']}")
        L.append(f"  - borderline (an end of the bootstrap or t interval within 0.02 of zero): {c['borderline']}")
    L.append("")
    L.append("## Ablations (paired difference of AURC x 100, first minus second; same format)")
    L.append("")
    keys = list(next(iter(res["summary"].values()))["ablations"].keys())
    L.append("| dataset | " + " | ".join(keys) + " |")
    L.append("|---|" + "---|" * len(keys))
    for ds, S in res["summary"].items():
        L.append(f"| {ds} | " + " | ".join(cell(S["ablations"][k]) for k in keys) + " |")
    L.append("")
    L.append("## Selected hyper-parameters (counts over folds)")
    L.append("")
    for ds, S in res["summary"].items():
        L.append(f"- **{ds}**")
        for mth in methods:
            L.append(f"  - {mth}: {S['methods'][mth]['selected_params']}")
    with open(path, "w") as fh:
        fh.write("\n".join(L) + "\n")

# ----------------------------------------------------------------------------

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--fast", action="store_true")
    ap.add_argument("--resummarise", action="store_true",
                    help="recompute summary/criterion from the per-fold results already in results/results.json")
    args = ap.parse_args()
    if args.resummarise:
        path = os.path.join(ROOT, "results", "results.json")
        old = json.load(open(path))
        methods = build_methods(False)
        per_fold = {ds: [{m: dict(f[m]) for m in f} for f in folds] for ds, folds in old["per_fold"].items()}
        summary, crit = summarise(per_fold, methods, n_splits=old["meta"]["n_splits"], curves_from=old["summary"])
        old["summary"], old["criterion"] = summary, crit
        old["meta"]["bootstrap_B"] = BOOT_B
        old["meta"]["nb_rho"] = 1.0 / (old["meta"]["n_splits"] - 1)
        old["meta"]["resummarised"] = f"summary and criterion recomputed from the stored per-fold results by {SCRIPT_VERSION}"
        with open(path, "w") as fh:
            json.dump(old, fh, indent=1)
        write_markdown(old, os.path.join(ROOT, "results", "tables.md"))
        for f, c in crit.items():
            print(f"criterion {f}: better {c['better']} worse {c['worse']} inconclusive {c['inconclusive']} -> met={c['criterion_met']}")
        return
    t0w, t0c = time.time(), time.process_time()
    n_repeats = 2 if args.fast else 3
    n_splits = 5
    D = make_datasets(SEED, fast=args.fast)
    methods = build_methods(args.fast)
    per_fold = {}
    ds_info = {}
    for ds, info in D.items():
        X, y = info["X"], info["y"]
        tds = time.time()
        rskf = RepeatedStratifiedKFold(n_splits=n_splits, n_repeats=n_repeats, random_state=SEED)
        folds = []
        d_used = None
        for fi, (tr, te) in enumerate(rskf.split(X, y)):
            sc = StandardScaler().fit(X[tr])
            Xtr, Xte = sc.transform(X[tr]), sc.transform(X[te])
            if info["pca"]:
                p = PCA(n_components=info["pca"], random_state=SEED).fit(Xtr)
                Xtr, Xte = p.transform(Xtr), p.transform(Xte)
            d_used = Xtr.shape[1]
            folds.append(evaluate_fold(Xtr, y[tr], Xte, y[te], methods, inner_seed=SEED + fi))
        per_fold[ds] = folds
        ds_info[ds] = dict(n=int(len(y)), d_raw=int(X.shape[1]), d_used=int(d_used), n_classes=int(len(np.unique(y))),
                           kind=info["kind"], note=info.get("note", "PCA to 20 components" if info["pca"] else ""),
                           bayes_error=info.get("bayes_error"), shift=info.get("shift"),
                           shift_at_bound=info.get("shift_at_bound"), seconds=time.time() - tds)
        print(f"[{ds}] done in {time.time() - tds:.1f} s; mean AURC x100: " +
              ", ".join(f"{m}={100*np.mean([f[m]['aurc'] for f in folds]):.2f}" for m in methods), flush=True)
    summary, crit = summarise(per_fold, methods, n_splits=n_splits)
    res = dict(
        meta=dict(seed=SEED, script_version=SCRIPT_VERSION, criterion=CRITERION_TEXT,
                  fast=args.fast, n_repeats=n_repeats, n_splits=n_splits, inner_splits=3,
                  bootstrap_B=BOOT_B, nb_rho=1.0 / (n_splits - 1),
                  intervals="percentile bootstrap over folds (predefined); Student t over folds; Nadeau-Bengio corrected t",
                  coverage_grid=COVERAGE_GRID.tolist(),
                  python=platform.python_version(), numpy=np.__version__, scipy=scipy.__version__,
                  sklearn=sklearn.__version__, cpu_seconds=time.process_time() - t0c,
                  wall_seconds=time.time() - t0w),
        datasets=ds_info,
        methods_order=list(methods.keys()),
        method_groups={m: v[3] for m, v in methods.items()},
        grids={m: {k: (v if not isinstance(v, list) else v) for k, v in methods[m][1].items()} for m in methods},
        summary=summary,
        criterion=crit,
        per_fold={ds: [{m: {k: v for k, v in f[m].items() if k != "curve"} for m in f} for f in folds]
                  for ds, folds in per_fold.items()},
    )
    os.makedirs(os.path.join(ROOT, "results"), exist_ok=True)
    suffix = "_fast" if args.fast else ""
    with open(os.path.join(ROOT, "results", f"results{suffix}.json"), "w") as fh:
        json.dump(res, fh, indent=1)
    write_markdown(res, os.path.join(ROOT, "results", f"tables{suffix}.md"))
    print(f"total CPU {res['meta']['cpu_seconds']:.1f} s, wall {res['meta']['wall_seconds']:.1f} s")
    for f, c in crit.items():
        print(f"criterion {f}: better {c['better']} worse {c['worse']} inconclusive {c['inconclusive']} -> met={c['criterion_met']}")


if __name__ == "__main__":
    main()
