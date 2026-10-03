#!/usr/bin/env python3
"""SPD001 -- Support geometry and nearest neighbours: the isolating comparison.

For a query q and its k nearest training neighbours of class c (Euclidean, after
per-fold standardisation) the script computes

  * the local tangent subspace T_m spanned by the first m right-singular directions
    of the centred neighbourhood,
  * the tangential distance  T = |P_T (q - mu)|  and the orthogonal distance
    O = |(I - P_T)(q - mu)|  (so that |q - mu|^2 = T^2 + O^2),
  * the spatial depth of q with respect to the neighbourhood (Vardi-Zhang / Serfling),

and evaluates the reference classifiers

  kNN   majority vote of the k nearest neighbours (all classes),
  NFL   nearest feature line among the k nearest same-class neighbours (Li-Lu 1999),
  HKNN  K-local hyperplane distance with ridge penalty lambda (Vincent-Bengio 2002),
  LPH   local PCA hull: argmin over classes of the orthogonal distance O_m,
  LCD   local class distance: argmin of the mean distance to the k class neighbours,
  SD    spatial-depth classifier: argmax of the local spatial depth,

against the proposed decomposition classifier

  TOD   conditional logit with shared weights on (log T, log O, log(1 - depth)),

and its ablations TO, TD, OD (one component removed) and T (tangential only;
O-only is LPH and D-only is SD).

Protocol: 5x5 repeated stratified k-fold; identical splits for all methods;
hyper-parameters chosen on each training fold by leave-one-out accuracy over
fixed grids; test accuracy and selective accuracy at 80% coverage per fold;
paired comparison against the best reference per dataset with a percentile
bootstrap over folds and the Nadeau-Bengio corrected t statistic (p-value and
95% interval with the inflated variance).

Protocol v0.3 (internal review round 2, 03/10/2026; preregistered in
../PREREGISTRO_SPD001_ronda2.md before this run, whose SHA-256 is stored in meta):
  * widened grids for every method and ablation: per-class neighbourhood size
    k in {5,10,20,30,50,75} restricted to k <= k_cap, plus k_cap itself when
    k_cap < 75, where k_cap = min_c (n_c - ceil(n_c/5)) - 1 is the largest size
    admissible in every training fold (leave-one-out); k_NN up to 121 (<= n_train-1);
    lambda_rel up to 10^4; tangent dimension m up to 21 (m <= min(k-1, d-1));
  * best reference decided by exact rational arithmetic on the integer counts of
    correct test predictions; exact ties are kept as a set (see compare());
  * one common matrix of bootstrap resampling indices for every comparison, so that
    a pair of methods has a single interval;
  * the E2 rows p=0 and p=10 are the E1 datasets moons and moons_noise10 (identical
    data and folds) and are copied, not recomputed;
  * per-fold counts of correct predictions are stored; NFL, depth and mean distance
    are computed once at the largest k and sliced (prefix minima / cumulative sums).
The v0.2 run (narrower grids) is kept in ../results/v02/.

Everything is seeded (SEED = 20260930).  Usage:
    python3 support_geometry.py            # full run
    python3 support_geometry.py --fast     # reduced run for smoke tests
Outputs: ../results/results.json, ../results/results_regime.json, ../results/tables.md
"""
import argparse
import json
import math
import os
import platform
import sys
import time
import hashlib
from fractions import Fraction

# Single-threaded BLAS: the matrices are tiny and multi-threading only adds CPU time.
for _v in ("OMP_NUM_THREADS", "OPENBLAS_NUM_THREADS", "MKL_NUM_THREADS"):
    os.environ.setdefault(_v, "1")

import numpy as np
import scipy
import sklearn
from scipy.optimize import minimize
from scipy.stats import t as student_t
from sklearn import datasets
from sklearn.model_selection import RepeatedStratifiedKFold

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
RESULTS = os.path.join(ROOT, "results")

SEED = 20260930
EPS = 1e-6                       # floor inside logarithms (standardised units)
# Grids of protocol v0.3 (PREREGISTRO_SPD001_ronda2.md). The neighbourhood and kNN grids
# are restricted per dataset by the class sizes, see dataset_grids().
K_BASE = [5, 10, 20, 30, 50, 75]             # per-class neighbourhood sizes (all class-neighbourhood methods)
M_GRID = [1, 2, 3, 5, 8, 13, 21]             # tangent dimensions (restricted to m <= min(k-1, d-1))
KNN_BASE = [1, 3, 5, 7, 9, 11, 15, 21, 31, 41, 61, 81, 121]
LAMBDA_GRID = [0.0, 0.1, 1.0, 10.0, 100.0, 1000.0, 10000.0]   # HKNN ridge, relative to the local scatter scale
K_COST = {"digits": 50}                     # cost cap on k (digits: d = 64 dominates the CPU time)
PREREG = "PREREGISTRO_SPD001_ronda2.md"
COVERAGE = 0.8                   # coverage for selective accuracy
N_BOOT = 10000
RIDGE = 1e-3                     # L2 penalty on the conditional-logit weights
REFERENCES = ["kNN", "NFL", "HKNN", "LPH", "LCD", "SD"]
PROPOSED = "TOD"
ABLATIONS = ["TO", "TD", "OD"]
SINGLES = ["T"]
LOGIT_MODELS = [PROPOSED] + ABLATIONS
ALL_METHODS = REFERENCES + [PROPOSED] + ABLATIONS + SINGLES
REGIME_P = [0, 2, 5, 10, 20]     # extra noise dimensions for the moons regime scan


# ----------------------------------------------------------------------------
# datasets
# ----------------------------------------------------------------------------
def make_datasets(seed, fast=False):
    """Return an ordered dict name -> (X, y, description)."""
    rng = np.random.default_rng(seed)
    out = {}
    X, y = datasets.load_iris(return_X_y=True)
    out["iris"] = (X, y, "Fisher iris, 150 x 4, 3 classes")
    X, y = datasets.load_wine(return_X_y=True)
    out["wine"] = (X, y, "UCI wine, 178 x 13, 3 classes")
    X, y = datasets.load_breast_cancer(return_X_y=True)
    out["breast_cancer"] = (X, y, "Wisconsin diagnostic breast cancer, 569 x 30, 2 classes")
    X, y = datasets.load_digits(return_X_y=True)
    per = 50 if fast else 100
    keep = np.concatenate([rng.choice(np.flatnonzero(y == c), per, replace=False) for c in range(10)])
    keep.sort()
    out["digits"] = (X[keep], y[keep], f"sklearn digits, stratified subsample {per} per class, 64 pixels, 10 classes")
    n = 600
    X, t = datasets.make_swiss_roll(n_samples=n, noise=1.0, random_state=seed)
    y = np.digitize(t, np.quantile(t, [1 / 3, 2 / 3]))
    out["swiss_roll"] = (X, y, "make_swiss_roll(600, noise=1.0); 3 classes = terciles of the roll parameter t")
    Xm, ym = datasets.make_moons(n_samples=n, noise=0.3, random_state=seed)
    noise_dims = rng.standard_normal((n, max(REGIME_P)))
    out["moons"] = (Xm, ym, "make_moons(600, noise=0.3), 2-d")
    out["moons_noise10"] = (np.hstack([Xm, noise_dims[:, :10]]), ym,
                            "moons + 10 independent N(0,1) coordinates (12-d)")

    def sphere(m, radius):
        v = rng.standard_normal((m, 3))
        v /= np.linalg.norm(v, axis=1, keepdims=True)
        return radius * v

    Xs = np.vstack([sphere(300, 1.0), sphere(300, 1.5)]) + 0.2 * rng.standard_normal((n, 3))
    ys = np.repeat([0, 1], 300)
    out["spheres"] = (Xs, ys, "two nested spheres in R^3 (radii 1 and 1.5, 300 points each) + N(0, 0.2^2 I) noise")
    regime = {p: (np.hstack([Xm, noise_dims[:, :p]]) if p > 0 else Xm, ym,
                  f"moons + {p} noise coordinates") for p in REGIME_P}
    return out, regime


def dataset_grids(y, n_splits, name=None):
    """Grids of protocol v0.3 for one dataset. k_cap is the largest per-class
    neighbourhood admissible in every training fold with leave-one-out features:
    min over classes of (n_c - ceil(n_c / n_splits)) - 1. The k grid is K_BASE cut at
    k_cap, plus k_cap itself when k_cap < max(K_BASE) (the whole class but the point)."""
    counts = np.bincount(np.searchsorted(np.unique(y), y))
    k_cap = int(min(c - math.ceil(c / n_splits) for c in counts)) - 1
    k_top = min(k_cap, K_COST.get(name, k_cap))
    k_grid = [k for k in K_BASE if k <= k_top]
    if k_top == k_cap and k_cap < max(K_BASE):
        k_grid.append(k_cap)
    n_train_min = len(y) - math.ceil(len(y) / n_splits)
    knn_grid = [k for k in KNN_BASE if k <= n_train_min - 1]
    return dict(k_grid=k_grid, k_cap=k_cap, k_cost=K_COST.get(name), knn_grid=knn_grid, m_grid=list(M_GRID),
                lambda_grid=list(LAMBDA_GRID))


# ----------------------------------------------------------------------------
# local geometry of a set of queries with respect to a labelled training set
# ----------------------------------------------------------------------------
def sqdist(A, B):
    a2 = (A * A).sum(1)[:, None]
    b2 = (B * B).sum(1)[None, :]
    D = a2 + b2 - 2.0 * (A @ B.T)
    np.maximum(D, 0.0, out=D)
    return D


RANK_TOL = 1e-10                 # relative threshold on squared singular values (numerical rank)


def spectral_coordinates(V, r):
    """Squared singular values s_j^2 of the centred neighbourhood V (nq, k, d), in
    decreasing order, and the squared coordinates t_j^2 = (u_j . r)^2 of the residual on
    the right singular directions, from the eigen-decomposition of the smaller Gram
    matrix (V V^T if k <= d, V^T V otherwise). Directions whose squared singular value is
    below RANK_TOL * s_1^2 are treated as null (s_j^2 = t_j^2 = 0), so that sums over
    j give the projection on the span of the neighbourhood (numerical rank), also for
    non-generic neighbourhoods. Returns arrays of shape (nq, min(k, d))."""
    nq, k, d = V.shape
    if k <= d:
        ev, W = np.linalg.eigh(V @ V.transpose(0, 2, 1))           # ascending
        ev, W = ev[:, ::-1], W[:, :, ::-1]
        g = np.einsum("nkd,nd->nk", V, r)                           # V r
        proj2 = np.einsum("nkj,nk->nj", W, g) ** 2                  # (w_j . V r)^2 = s_j^2 t_j^2
    else:
        ev, U = np.linalg.eigh(V.transpose(0, 2, 1) @ V)
        ev, U = ev[:, ::-1], U[:, :, ::-1]
        proj2 = None
        t = np.einsum("nd,ndj->nj", r, U)
    ev = np.maximum(ev, 0.0)
    pos = ev > RANK_TOL * ev[:, :1]
    s2 = np.where(pos, ev, 0.0)
    if proj2 is not None:
        t2 = np.where(pos, proj2 / np.where(pos, ev, 1.0), 0.0)
    else:
        t2 = np.where(pos, t * t, 0.0)
    return s2, t2


class LocalGeometry:
    """For every query and every class: the k nearest same-class training points,
    their centred SVD, the squared projections of q - mu on the singular directions,
    the nearest-feature-line distance, the mean neighbour distance and the spatial depth.

    exclude_self=True is used when the queries are the training points themselves
    (leave-one-out features): a point is never its own neighbour.
    """

    def __init__(self, Xtr, ytr, classes, k_grid, Xq, exclude_self=False):
        self.nq, self.d = Xq.shape
        self.C = len(classes)
        self.k_grid = list(k_grid)
        D2 = sqdist(Xq, Xtr)
        if exclude_self:
            D2[np.arange(self.nq), np.arange(self.nq)] = np.inf
        self.D2 = D2
        kmax = max(k_grid)
        order = {}
        for ci, c in enumerate(classes):
            idx = np.flatnonzero(ytr == c)
            if exclude_self:
                assert len(idx) > kmax, "class too small for the neighbourhood grid"
            else:
                assert len(idx) >= kmax, "class too small for the neighbourhood grid"
            Dc = D2[:, idx]
            part = np.argpartition(Dc, kmax - 1, axis=1)[:, :kmax]
            sub = np.take_along_axis(Dc, part, axis=1)
            srt = np.argsort(sub, axis=1, kind="stable")
            order[ci] = idx[np.take_along_axis(part, srt, axis=1)]
        self.geo = {}
        triu_mask = np.triu(np.ones((kmax, kmax), dtype=bool), 1)        # pairs i < j
        per_class = []
        for ci in range(self.C):
            Xn = Xtr[order[ci]]                       # (nq, kmax, d), sorted by distance
            A = Xq[:, None, :] - Xn                   # q - x_i
            G = A @ A.transpose(0, 2, 1)              # (q - x_i).(q - x_j)
            a2 = np.einsum("nkk->nk", G).copy()
            num = a2[:, :, None] - G                  # (q - x_i).(x_j - x_i)
            den = a2[:, :, None] + a2[:, None, :] - 2.0 * G   # |x_j - x_i|^2
            with np.errstate(divide="ignore", invalid="ignore"):
                dl2 = np.where(den > 1e-18, a2[:, :, None] - num * num / den, a2[:, :, None])
            del num, den, G
            dl2 = np.where(triu_mask[None], dl2, np.inf)
            # line distance over all pairs among the first k neighbours = prefix minimum over
            # the column-wise minima (pair (i, j), i < j, enters as soon as k > j)
            nfl_prefix = np.minimum.accumulate(dl2.min(1), axis=1)   # (nq, kmax); entry j: pairs within the first j+1
            del dl2
            norms = np.sqrt(a2)
            U = A / np.where(norms > 0, norms, 1.0)[:, :, None]
            cumU = np.cumsum(U, axis=1)
            cumN = np.cumsum(norms, axis=1)
            per_class.append((Xn, nfl_prefix, cumU, cumN))
        for k in k_grid:
            kp = min(k, self.d)
            t2 = np.zeros((self.nq, self.C, kp))
            s2 = np.zeros((self.nq, self.C, kp))
            r2 = np.zeros((self.nq, self.C))
            nfl2 = np.zeros((self.nq, self.C))
            lcd = np.zeros((self.nq, self.C))
            depth = np.zeros((self.nq, self.C))
            for ci in range(self.C):
                Xn_full, nfl_prefix, cumU, cumN = per_class[ci]
                Xn = Xn_full[:, :k]                       # (nq, k, d)
                mu = Xn.mean(1)
                V = Xn - mu[:, None, :]                   # centred neighbourhood
                r = Xq - mu                               # residual q - mu
                sv2, tt2 = spectral_coordinates(V, r)
                t2[:, ci, :] = tt2
                s2[:, ci, :] = sv2
                r2[:, ci] = (r * r).sum(1)
                nfl2[:, ci] = np.maximum(nfl_prefix[:, k - 1], 0.0)
                depth[:, ci] = 1.0 - np.linalg.norm(cumU[:, k - 1], axis=1) / k
                lcd[:, ci] = cumN[:, k - 1] / k
            self.geo[k] = dict(t2=t2, s2=s2, r2=r2, nfl2=nfl2, lcd=lcd, depth=depth,
                               rank=min(k - 1, self.d), rank_num=(s2 > 0).sum(2))


# derived scores ("smaller is better" unless stated)
def score_T2(L, k, m):
    return L.geo[k]["t2"][:, :, :m].sum(2)


def score_O2(L, k, m):
    return np.maximum(L.geo[k]["r2"] - score_T2(L, k, m), 0.0)


def score_hull2(L, k):
    """Squared distance to the affine hull of the neighbourhood: |r|^2 minus the squared
    projection on the span of the directions with non-zero singular value."""
    g = L.geo[k]
    return np.maximum(g["r2"] - g["t2"].sum(2), 0.0)


def score_hknn2(L, k, lam):
    """Penalised local-hyperplane distance: sum_j lam t_j^2/(s_j^2+lam) + O_hull^2."""
    g = L.geo[k]
    if lam == 0.0:
        return score_hull2(L, k)
    return (lam * g["t2"] / (g["s2"] + lam)).sum(2) + score_hull2(L, k)


def logit_features(L, k, m, which):
    cols = []
    if "T" in which:
        cols.append(0.5 * np.log(score_T2(L, k, m) + EPS ** 2))
    if "O" in which:
        cols.append(0.5 * np.log(score_O2(L, k, m) + EPS ** 2))
    if "D" in which:
        cols.append(np.log(1.0 - L.geo[k]["depth"] + EPS))
    return np.stack(cols, axis=2)          # (nq, C, p)


def fit_clogit(F, y, ridge=RIDGE):
    """Conditional logit P(c|q) = softmax_c(-F[q,c,:].w), shared w, ridge penalty."""
    n, C, p = F.shape
    rows = np.arange(n)

    def obj(w):
        S = -F @ w
        S = S - S.max(1, keepdims=True)
        lse = np.log(np.exp(S).sum(1))
        ll = S[rows, y] - lse
        P = np.exp(S - lse[:, None])
        P[rows, y] -= 1.0
        grad = -np.einsum("nc,ncp->p", P, F) / n + 2.0 * ridge * w
        return -ll.mean() + ridge * (w @ w), grad

    res = minimize(obj, np.ones(p), jac=True, method="L-BFGS-B")
    return res.x


def clogit_predict(F, w):
    S = -F @ w
    S = S - S.max(1, keepdims=True)
    P = np.exp(S)
    P /= P.sum(1, keepdims=True)
    return P.argmax(1), P.max(1), P


def relative_margin(score):
    """Confidence of an argmin-of-score classifier: (s2 - s1)/(s1 + s2)."""
    part = np.partition(score, 1, axis=1)
    s1, s2 = part[:, 0], part[:, 1]
    return (s2 - s1) / (s1 + s2 + 1e-12)


def selective_accuracy(correct, confidence, coverage=COVERAGE):
    n = len(correct)
    keep = int(math.ceil(coverage * n))
    idx = np.argsort(-confidence, kind="stable")[:keep]
    return float(correct[idx].mean())


def result_entry(corr, conf, loo, params, **extra):
    """Per-fold record: accuracy, selective accuracy and the integer counts behind them."""
    keep = int(math.ceil(COVERAGE * len(corr)))
    idx = np.argsort(-conf, kind="stable")[:keep]
    out = dict(acc=float(corr.mean()), sel=float(corr[idx].mean()), n_correct=int(corr.sum()),
               n_test=int(len(corr)), sel_correct=int(corr[idx].sum()), sel_n=keep, loo=loo, params=params)
    out.update(extra)
    return out


def m_candidates(k, d):
    return [m for m in M_GRID if m <= min(k - 1, d - 1)]


# ----------------------------------------------------------------------------
# one outer fold
# ----------------------------------------------------------------------------
def run_fold(Xtr, ytr, Xte, yte, classes, grids):
    mu, sd = Xtr.mean(0), Xtr.std(0)
    sd = np.where(sd > 0, sd, 1.0)
    Xtr = (Xtr - mu) / sd
    Xte = (Xte - mu) / sd
    d = Xtr.shape[1]
    ntr = len(ytr)
    cidx = {c: i for i, c in enumerate(classes)}
    ytr_i = np.array([cidx[c] for c in ytr])
    yte_i = np.array([cidx[c] for c in yte])
    C = len(classes)

    K_GRID = grids["k_grid"]
    KNN_GRID = grids["knn_grid"]
    Ltr = LocalGeometry(Xtr, ytr, classes, K_GRID, Xtr, exclude_self=True)

    class _Dist:                                   # test-to-training distances for kNN
        D2 = sqdist(Xte, Xtr)
    out = {}
    chosen = {}                                    # selections, evaluated on the test fold at the end

    # ---- kNN (majority vote; ties broken towards the class of the nearest neighbour)
    def knn_scores(L, k):
        nb = np.argpartition(L.D2, k - 1, axis=1)[:, :k]
        dn = np.take_along_axis(L.D2, nb, axis=1)
        srt = np.argsort(dn, axis=1, kind="stable")
        nb = np.take_along_axis(nb, srt, axis=1)
        lab = ytr_i[nb]
        counts = (lab[:, :, None] == np.arange(C)).sum(1).astype(float)
        counts[np.arange(len(lab)), lab[:, 0]] += 0.5
        pred = counts.argmax(1)
        frac = np.floor(counts.max(1)) / k
        conf = frac + 1e-6 / (1.0 + np.sqrt(np.take_along_axis(L.D2, nb, axis=1)).mean(1))
        return pred, conf

    best = None
    for k in [k for k in KNN_GRID if k < ntr]:
        acc = float((knn_scores(Ltr, k)[0] == ytr_i).mean())
        if best is None or acc > best[0]:
            best = (acc, k)
    pred, conf = knn_scores(_Dist, best[1])
    corr = (pred == yte_i)
    out["kNN"] = result_entry(corr, conf, best[0], {"k": best[1]})

    # ---- HKNN scale: median over training points of the mean squared singular value
    #      of the true-class neighbourhood (leave-one-out)
    scale = {}
    for k in K_GRID:
        rk = Ltr.geo[k]["rank"]
        s2 = Ltr.geo[k]["s2"][np.arange(ntr), ytr_i, :rk]          # null directions count as 0
        scale[k] = float(np.median(s2.mean(1)))

    # ---- argmin-of-score reference classifiers
    def candidates(name):
        if name == "NFL":
            return [((k,), lambda L, k=k: L.geo[k]["nfl2"]) for k in K_GRID]
        if name == "HKNN":
            return [((k, lam), lambda L, k=k, lam=lam: score_hknn2(L, k, lam * scale[k]))
                    for k in K_GRID for lam in LAMBDA_GRID]
        if name == "LPH":
            return [((k, m), lambda L, k=k, m=m: score_O2(L, k, m)) for k in K_GRID for m in m_candidates(k, d)]
        if name == "LCD":
            return [((k,), lambda L, k=k: L.geo[k]["lcd"]) for k in K_GRID]
        if name == "SD":
            return [((k,), lambda L, k=k: 1.0 - L.geo[k]["depth"]) for k in K_GRID]
        if name == "T":
            return [((k, m), lambda L, k=k, m=m: score_T2(L, k, m)) for k in K_GRID for m in m_candidates(k, d)]
        raise ValueError(name)

    param_names = {"NFL": ["k"], "HKNN": ["k", "lambda_rel"], "LPH": ["k", "m"], "LCD": ["k"],
                   "SD": ["k"], "T": ["k", "m"]}
    for name in ["NFL", "HKNN", "LPH", "LCD", "SD", "T"]:
        best = None
        for params, fn in candidates(name):
            acc = float((fn(Ltr).argmin(1) == ytr_i).mean())
            if best is None or acc > best[0]:
                best = (acc, params, fn)
        chosen[name] = best

    # ---- conditional-logit decomposition models
    for name in LOGIT_MODELS:
        which = name
        best = None
        for k in K_GRID:
            ms = m_candidates(k, d) if ("T" in which or "O" in which) else [1]
            for m in ms:
                Ftr = logit_features(Ltr, k, m, which)
                fm = Ftr.mean((0, 1))
                fs = Ftr.std((0, 1))
                fs = np.where(fs > 0, fs, 1.0)
                Fz = (Ftr - fm) / fs
                w = fit_clogit(Fz, ytr_i)
                acc = float((clogit_predict(Fz, w)[0] == ytr_i).mean())
                if best is None or acc > best[0]:
                    best = (acc, (k, m), fm, fs, w)
        chosen[name] = best

    # ---- test fold: local geometry only at the neighbourhood sizes actually selected
    needed = sorted({b[1][0] for nm, b in chosen.items()})
    Lte = LocalGeometry(Xtr, ytr, classes, needed, Xte)
    for name in ["NFL", "HKNN", "LPH", "LCD", "SD", "T"]:
        acc0, params, fn = chosen[name]
        sc = fn(Lte)
        corr = (sc.argmin(1) == yte_i)
        out[name] = result_entry(corr, relative_margin(sc), acc0, dict(zip(param_names[name], params)))
    for name in LOGIT_MODELS:
        acc0, (k, m), fm, fs, w = chosen[name]
        Fte = (logit_features(Lte, k, m, name) - fm) / fs
        pred, conf, _ = clogit_predict(Fte, w)
        corr = (pred == yte_i)
        out[name] = result_entry(corr, conf, acc0, {"k": k, "m": m}, weights={f: float(x) for f, x in zip(name, w)})
    return out


# ----------------------------------------------------------------------------
# statistics
# ----------------------------------------------------------------------------
_BOOT_IDX = {}


def boot_indices(J, n_boot=None):
    """One common matrix of bootstrap resampling indices (n_boot x J) for every paired
    comparison with J folds, seeded with the master seed: a given pair of methods on a
    given dataset therefore has a single interval, whatever the order of the comparisons."""
    n_boot = N_BOOT if n_boot is None else n_boot
    key = (J, n_boot)
    if key not in _BOOT_IDX:
        _BOOT_IDX[key] = np.random.default_rng(SEED).integers(0, J, size=(n_boot, J))
    return _BOOT_IDX[key]


def paired_stats(a, b, n_test_over_n_train):
    """Fold-level paired differences a - b: mean, percentile bootstrap CI (common
    resampling indices), Nadeau-Bengio corrected t, two-sided p and 95% interval."""
    dlt = np.asarray(a, float) - np.asarray(b, float)
    J = len(dlt)
    boot = dlt[boot_indices(J)].mean(1)
    lo, hi = np.percentile(boot, [2.5, 97.5])
    var = dlt.var(ddof=1)
    nb_se = math.sqrt((1.0 / J + n_test_over_n_train) * var)     # Nadeau-Bengio standard error
    if var > 0:
        tstat = dlt.mean() / nb_se
        p = float(2 * student_t.sf(abs(tstat), J - 1))
    else:
        tstat, p = (float("inf") if dlt.mean() > 0 else (float("-inf") if dlt.mean() < 0 else 0.0)), (0.0 if dlt.mean() != 0 else 1.0)
    half = float(student_t.ppf(0.975, J - 1) * nb_se)              # 95% interval with the NB variance
    return dict(mean=float(dlt.mean()), ci_low=float(lo), ci_high=float(hi), wins=int((dlt > 0).sum()),
                losses=int((dlt < 0).sum()), ties=int((dlt == 0).sum()), nb_t=float(tstat), nb_p=p,
                nb_lo=float(dlt.mean() - half), nb_hi=float(dlt.mean() + half))


def evaluate_dataset(name, X, y, n_splits, n_repeats, log):
    classes = np.unique(y)
    grids = dataset_grids(y, n_splits, name.split("_p")[0] if name.startswith("moons_p") else name)
    rskf = RepeatedStratifiedKFold(n_splits=n_splits, n_repeats=n_repeats, random_state=SEED)
    folds = []
    t0 = time.time()
    c0 = time.process_time()
    for tr, te in rskf.split(X, y):
        folds.append(run_fold(X[tr], y[tr], X[te], y[te], classes, grids))
    wall = time.time() - t0
    cpu = time.process_time() - c0
    per_method = {}
    for mth in ALL_METHODS:
        per_method[mth] = {key: [f[mth][key] for f in folds]
                           for key in ("acc", "sel", "n_correct", "n_test", "sel_correct", "sel_n", "loo", "params")}
        if mth in LOGIT_MODELS:
            per_method[mth]["weights"] = [f[mth]["weights"] for f in folds]
    log(f"  {name}: {len(folds)} folds in {wall:.1f}s wall / {cpu:.1f}s cpu; grids k={grids['k_grid']} "
        f"kNN<={max(grids['knn_grid'])}; "
        + ", ".join(f"{m}={np.mean(per_method[m]['acc']):.3f}" for m in ALL_METHODS))
    return dict(n=int(len(y)), d=int(X.shape[1]), classes=int(len(classes)),
                class_counts=[int(v) for v in np.bincount(np.searchsorted(classes, y))],
                folds=len(folds), n_splits=n_splits, n_repeats=n_repeats, grids=grids,
                seconds_wall=wall, seconds_cpu=cpu, methods=per_method)


def exact_mean(correct, ntest):
    """Mean accuracy over folds in exact rational arithmetic on the integer counts."""
    return sum(Fraction(int(c), int(n)) for c, n in zip(correct, ntest)) / len(correct)


def best_set(r, metric="acc"):
    """References with the highest mean (exact ties kept): list in REFERENCES order."""
    ck, nk = ("n_correct", "n_test") if metric == "acc" else ("sel_correct", "sel_n")
    ex = {m: exact_mean(r["methods"][m][ck], r["methods"][m][nk]) for m in REFERENCES}
    top = max(ex.values())
    return [m for m in REFERENCES if ex[m] == top]


def compare(res, criterion_datasets):
    """Paired comparisons and the predefined criterion.

    Tie rule (protocol v0.3): the best reference is decided on the exact mean accuracy
    (rational arithmetic on the integer counts of correct predictions); when several
    references tie exactly, all of them are kept. A significant win then requires an
    interval above zero against every tied reference and a significant loss an interval
    below zero against every tied reference; the representative shown in the tables
    ('best_reference') is the tied reference with the highest bootstrap upper limit,
    i.e. the one least favourable to a loss and most conservative for the bound on a gain."""
    comp = {}
    for name, r in res.items():
        acc = {m: np.array(r["methods"][m]["acc"]) for m in ALL_METHODS}
        ratio = 1.0 / (r["n_splits"] - 1)          # n_test / n_train for k-fold
        means = {m: float(acc[m].mean()) for m in ALL_METHODS}
        vs_each = {m: paired_stats(acc[PROPOSED], acc[m], ratio) for m in REFERENCES}
        tied = best_set(r, "acc")
        best_ref = max(tied, key=lambda m: (vs_each[m]["ci_high"], -REFERENCES.index(m)))
        entry = dict(best_reference=best_ref, best_reference_tied=tied,
                     win_vs_all_tied=all(vs_each[m]["ci_low"] > 0 for m in tied),
                     loss_vs_all_tied=all(vs_each[m]["ci_high"] < 0 for m in tied),
                     win_vs_all_tied_nb=all(vs_each[m]["nb_lo"] > 0 for m in tied),
                     loss_vs_all_tied_nb=all(vs_each[m]["nb_hi"] < 0 for m in tied),
                     means=means,
                     total_correct={m: int(sum(r["methods"][m]["n_correct"])) for m in ALL_METHODS},
                     sds={m: float(acc[m].std(ddof=1)) for m in ALL_METHODS},
                     vs_best=vs_each[best_ref],
                     vs_each=vs_each,
                     ablation={m: paired_stats(acc[PROPOSED], acc[m], ratio) for m in ABLATIONS + SINGLES})
        sel = {m: np.array(r["methods"][m]["sel"]) for m in ALL_METHODS}
        entry["sel_means"] = {m: float(sel[m].mean()) for m in ALL_METHODS}
        sel_each = {m: paired_stats(sel[PROPOSED], sel[m], ratio) for m in REFERENCES}
        entry["sel_vs_each"] = sel_each
        entry["sel_vs_best"] = sel_each[best_ref]
        tied_sel = best_set(r, "sel")
        entry["sel_best_reference_by_sel_tied"] = tied_sel
        entry["sel_best_reference_by_sel"] = max(tied_sel, key=lambda m: (sel_each[m]["ci_high"], -REFERENCES.index(m)))
        entry["sel_vs_best_by_sel"] = sel_each[entry["sel_best_reference_by_sel"]]
        # modal hyper-parameters and mean weights of the proposed model
        entry["params_mode"] = {}
        for m in ALL_METHODS:
            ps = [json.dumps(p, sort_keys=True) for p in r["methods"][m]["params"]]
            # deterministic mode: ties broken towards the smallest parameter values
            cnt = {s: ps.count(s) for s in set(ps)}
            top = max(cnt.values())
            tiedp = [json.loads(s) for s, v in cnt.items() if v == top]
            entry["params_mode"][m] = min(tiedp, key=lambda p: tuple(p[kk] for kk in sorted(p)))
        entry["weights_mean"] = {m: {f: float(np.mean([w[f] for w in r["methods"][m]["weights"]]))
                                     for f in m} for m in LOGIT_MODELS}
        comp[name] = entry
    n_ds = len(criterion_datasets)
    wins = [nm for nm in criterion_datasets if comp[nm]["win_vs_all_tied"]]
    losses = [nm for nm in criterion_datasets if comp[nm]["loss_vs_all_tied"]]
    needed = n_ds // 2 + 1
    verdict = dict(datasets=criterion_datasets, n_datasets=n_ds, required_wins=needed,
                   significant_wins=wins, significant_losses=losses,
                   adds_information=len(wins) >= needed)
    return comp, verdict


# ----------------------------------------------------------------------------
# markdown tables
# ----------------------------------------------------------------------------
def fmt_ci(s):
    return f"{100 * s['mean']:+.2f} [{100 * s['ci_low']:+.2f}, {100 * s['ci_high']:+.2f}]"


def write_tables(res, comp, verdict, regime, regime_comp, meta, path):
    L = []
    L.append("# SPD001 -- results (generated by experiments/support_geometry.py)\n")
    L.append(f"Protocol {meta['protocol']}; seed {meta['seed']}; {meta['n_splits']}x{meta['n_repeats']} repeated stratified k-fold; "
             f"total {meta['seconds_wall']:.0f} s wall, {meta['seconds_cpu']:.0f} s CPU.\n")
    L.append("## E1: accuracy (mean over folds, %)\n")
    L.append("| dataset | n | d | C | " + " | ".join(ALL_METHODS) + " | best ref |")
    L.append("|---|---|---|---|" + "---|" * len(ALL_METHODS) + "---|")
    for name, r in res.items():
        c = comp[name]
        L.append(f"| {name} | {r['n']} | {r['d']} | {r['classes']} | "
                 + " | ".join(f"{100 * c['means'][m]:.2f}" for m in ALL_METHODS) + f" | {c['best_reference']} |")
    L.append("\n## E1: TOD minus best reference (accuracy points; percentile bootstrap 95% CI over folds; Nadeau-Bengio p)\n")
    L.append("| dataset | best ref | delta [CI] | wins/losses/ties | NB p |")
    L.append("|---|---|---|---|---|")
    for name in res:
        c = comp[name]
        s = c["vs_best"]
        L.append(f"| {name} | {'/'.join(c['best_reference_tied'])} | {fmt_ci(s)} | {s['wins']}/{s['losses']}/{s['ties']} | {s['nb_p']:.3f} |")
    L.append(f"\nPredefined criterion: TOD 'adds information' iff CI > 0 (against every exactly tied best reference) on at least {verdict['required_wins']} of "
             f"{verdict['n_datasets']} datasets. Significant wins: {verdict['significant_wins']}; "
             f"significant losses: {verdict['significant_losses']}. **Verdict: adds_information = {verdict['adds_information']}**\n")
    L.append("\n## E1: TOD minus each reference (accuracy points, mean [CI])\n")
    L.append("| dataset | " + " | ".join(REFERENCES) + " |")
    L.append("|---|" + "---|" * len(REFERENCES))
    for name in res:
        L.append(f"| {name} | " + " | ".join(fmt_ci(comp[name]["vs_each"][m]) for m in REFERENCES) + " |")
    L.append("\n## E1: ablations, TOD minus reduced model (accuracy points, mean [CI])\n")
    L.append("| dataset | " + " | ".join(f"TOD - {m}" for m in ABLATIONS + SINGLES + ["LPH (O)", "SD (D)"]) + " |")
    L.append("|---|" + "---|" * (len(ABLATIONS) + len(SINGLES) + 2))
    for name in res:
        c = comp[name]
        cells = [fmt_ci(c["ablation"][m]) for m in ABLATIONS + SINGLES] + [fmt_ci(c["vs_each"]["LPH"]), fmt_ci(c["vs_each"]["SD"])]
        L.append(f"| {name} | " + " | ".join(cells) + " |")
    L.append("\n## E1: selective accuracy at 80% coverage (mean over folds, %)\n")
    L.append("| dataset | " + " | ".join(ALL_METHODS) + " | TOD - best ref (by acc) |")
    L.append("|---|" + "---|" * len(ALL_METHODS) + "---|")
    for name in res:
        c = comp[name]
        L.append(f"| {name} | " + " | ".join(f"{100 * c['sel_means'][m]:.2f}" for m in ALL_METHODS)
                 + f" | {fmt_ci(c['sel_vs_best'])} |")
    L.append("\n## E1: modal hyper-parameters and mean fitted weights (TOD: log T, log O, log(1-depth))\n")
    L.append("| dataset | kNN k | HKNN (k, lambda_rel) | LPH (k, m) | TOD (k, m) | TOD weights (T, O, D) |")
    L.append("|---|---|---|---|---|---|")
    for name in res:
        c = comp[name]
        w = c["weights_mean"]["TOD"]
        L.append(f"| {name} | {c['params_mode']['kNN']['k']} | ({c['params_mode']['HKNN']['k']}, {c['params_mode']['HKNN']['lambda_rel']}) | "
                 f"({c['params_mode']['LPH']['k']}, {c['params_mode']['LPH']['m']}) | ({c['params_mode']['TOD']['k']}, {c['params_mode']['TOD']['m']}) | "
                 f"({w['T']:.2f}, {w['O']:.2f}, {w['D']:.2f}) |")
    L.append("\n## E2: moons regime scan, accuracy (%) against the number of noise coordinates\n")
    L.append("| p | " + " | ".join(ALL_METHODS) + " | best ref | TOD - best ref |")
    L.append("|---|" + "---|" * len(ALL_METHODS) + "---|---|")
    for name in regime:
        c = regime_comp[name]
        L.append(f"| {name.split('_p')[-1]} | " + " | ".join(f"{100 * c['means'][m]:.2f}" for m in ALL_METHODS)
                 + f" | {c['best_reference']} | {fmt_ci(c['vs_best'])} |")
    with open(path, "w") as fh:
        fh.write("\n".join(L) + "\n")


# ----------------------------------------------------------------------------
def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--fast", action="store_true")
    ap.add_argument("--profile", default=None,
                    help="time one fold of the named dataset with the v0.3 grids (no output files, no accuracies)")
    args = ap.parse_args()
    global N_BOOT
    n_splits, n_repeats = (3, 1) if args.fast else (5, 5)
    if args.fast:
        N_BOOT = 1000
    data, regime_data = make_datasets(SEED, fast=args.fast)
    if args.profile:
        X, y, _ = data[args.profile] if args.profile in data else regime_data[int(args.profile.split("_p")[-1])]
        grids = dataset_grids(y, 5, args.profile)
        tr, te = next(RepeatedStratifiedKFold(n_splits=5, n_repeats=1, random_state=SEED).split(X, y))
        c0 = time.process_time()
        run_fold(X[tr], y[tr], X[te], y[te], np.unique(y), grids)
        print(f"{args.profile}: grids {grids}; one fold {time.process_time() - c0:.2f}s cpu")
        return
    os.makedirs(RESULTS, exist_ok=True)
    t0 = time.time()
    c0 = time.process_time()
    prereg_path = os.path.join(ROOT, PREREG)
    prereg_sha = hashlib.sha256(open(prereg_path, "rb").read()).hexdigest() if os.path.exists(prereg_path) else None

    def log(msg):
        print(msg, flush=True)

    log(f"SPD001 run (protocol v0.3): seed={SEED} splits={n_splits} repeats={n_repeats} fast={args.fast} "
        f"prereg_sha256={prereg_sha}")
    res = {}
    for name, (X, y, desc) in data.items():
        res[name] = evaluate_dataset(name, X, y, n_splits, n_repeats, log)
        res[name]["description"] = desc
    comp, verdict = compare(res, list(res.keys()))
    log("E2: moons regime scan (p = 0 and p = 10 are the E1 datasets moons and moons_noise10)")
    regime = {}
    reuse = {0: "moons", 10: "moons_noise10"}
    for p, (X, y, desc) in regime_data.items():
        nm = f"moons_p{p}"
        if p in reuse and reuse[p] in res:
            X1, y1, _ = data[reuse[p]]
            assert np.array_equal(X1, X) and np.array_equal(y1, y)
            regime[nm] = json.loads(json.dumps(res[reuse[p]]))
            regime[nm]["reused_from"] = reuse[p]
            log(f"  {nm}: identical to {reuse[p]} (same data and folds), copied")
        else:
            regime[nm] = evaluate_dataset(nm, X, y, n_splits, n_repeats, log)
        regime[nm]["description"] = desc
        regime[nm]["p"] = p
    regime_comp, _ = compare(regime, list(regime.keys()))
    meta = dict(seed=SEED, protocol="v0.3", preregistration=PREREG, preregistration_sha256=prereg_sha,
                n_splits=n_splits, n_repeats=n_repeats, fast=args.fast,
                k_base=K_BASE, m_grid=M_GRID, knn_base=KNN_BASE, lambda_grid=LAMBDA_GRID,
                coverage=COVERAGE, n_boot=N_BOOT, ridge=RIDGE, eps=EPS,
                python=platform.python_version(), numpy=np.__version__, scipy=scipy.__version__,
                sklearn=sklearn.__version__, seconds_wall=time.time() - t0,
                seconds_cpu=time.process_time() - c0, cpu_count=os.cpu_count())
    with open(os.path.join(RESULTS, "results.json"), "w") as fh:
        json.dump(dict(meta=meta, datasets=res, comparison=comp, verdict=verdict), fh, indent=1)
    with open(os.path.join(RESULTS, "results_regime.json"), "w") as fh:
        json.dump(dict(meta=meta, datasets=regime, comparison=regime_comp), fh, indent=1)
    write_tables(res, comp, verdict, regime, regime_comp, meta, os.path.join(RESULTS, "tables.md"))
    log(f"verdict: {verdict}")
    log(f"done in {meta['seconds_wall']:.0f}s wall / {meta['seconds_cpu']:.0f}s cpu")


if __name__ == "__main__":
    main()
