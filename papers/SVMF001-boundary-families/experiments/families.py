#!/usr/bin/env python3
"""Small, transparent implementations of the boundary families compared in SVMF001.

Global references
  (a) linear SVM and RBF-SVM (libsvm through scikit-learn), tuned by inner CV.
Locally adaptive families (each contains a global reference as a special case)
  (b) kNN-SVM: for each test point, a linear SVM on its k nearest training points
      (k = 'all' recovers a global linear SVM); pure neighbourhoods vote.
  (b') cell-SVM: hard partition into M k-means cells, one linear SVM per cell
      (M = 1 recovers a global linear SVM).
  (c) variable-bandwidth RBF-SVM: per-point bandwidth from the k-NN radius,
      symmetrised into a positive-definite kernel (beta = 0 recovers the RBF-SVM).
  (d) LLSVM-style mixture: linear SVMs weighted by a soft k-means partition,
      fitted jointly as one linear SVM on expanded features (M = 1 recovers a
      global linear SVM).
All labels are in {-1, +1}.  Nothing here is optimised for speed.
"""
import numpy as np
from sklearn.cluster import KMeans
from sklearn.metrics import pairwise_distances
from sklearn.model_selection import StratifiedKFold
from sklearn.neighbors import NearestNeighbors
from sklearn.svm import SVC

# --------------------------------------------------------------------------
# helpers

def median_gamma(X):
    """Median heuristic: gamma = 1 / median squared pairwise distance."""
    D2 = pairwise_distances(X, metric="sqeuclidean")
    med = np.median(D2[np.triu_indices_from(D2, k=1)])
    return 1.0 / max(med, 1e-12)


def majority(y):
    s = np.sum(y)
    return 1 if s > 0 else (-1 if s < 0 else 1)


def inner_folds(y, n_splits, seed):
    skf = StratifiedKFold(n_splits=n_splits, shuffle=True, random_state=seed)
    return list(skf.split(np.zeros(len(y)), y))


def linear_svm(C):
    return SVC(kernel="linear", C=C)


def fit_linear_or_vote(X, y, C):
    """A linear SVM if both classes are present, else a constant vote."""
    if len(np.unique(y)) < 2:
        lab = int(y[0])
        return lambda Z: np.full(len(Z), lab)
    m = linear_svm(C).fit(X, y)
    return m.predict


# --------------------------------------------------------------------------
# (a) global references

def select(configs, score_fn):
    """Return (best_config, best_score, all_scores); ties go to the FIRST config,
    so grids must list the global special case first."""
    scores = [score_fn(c) for c in configs]
    i = int(np.argmax(scores))  # argmax returns the first maximiser
    return configs[i], float(scores[i]), scores


def cv_score_estimator(make, X, y, folds):
    accs = []
    for tr, va in folds:
        m = make().fit(X[tr], y[tr])
        accs.append(np.mean(m.predict(X[va]) == y[va]))
    return float(np.mean(accs))


def tune_linear(X, y, folds, Cs):
    cfg, sc, _ = select([{"C": C} for C in Cs],
                        lambda c: cv_score_estimator(lambda: linear_svm(c["C"]), X, y, folds))
    return cfg, sc, linear_svm(cfg["C"]).fit(X, y)


def tune_rbf(X, y, folds, Cs, gamma_mults):
    g0 = median_gamma(X)
    configs = [{"C": C, "gamma_mult": gm} for gm in gamma_mults for C in Cs]
    cfg, sc, scores = select(configs, lambda c: cv_score_estimator(
        lambda: SVC(kernel="rbf", C=c["C"], gamma=c["gamma_mult"] * g0), X, y, folds))
    model = SVC(kernel="rbf", C=cfg["C"], gamma=cfg["gamma_mult"] * g0).fit(X, y)
    cfg = dict(cfg, gamma=cfg["gamma_mult"] * g0)
    return cfg, sc, model, {(c["gamma_mult"], c["C"]): s for c, s in zip(configs, scores)}


# --------------------------------------------------------------------------
# (b) kNN-SVM (localised linear SVM), Bottou-Vapnik / SVM-KNN style

def knn_svm_predict_multi(Xtr, ytr, Xte, ks, C):
    """Predictions of the localised linear SVM for every k in `ks` at once.
    ks may contain the string 'all' (global linear SVM with the same C)."""
    out = {}
    num_ks = [k for k in ks if k != "all"]
    if "all" in ks:
        out["all"] = fit_linear_or_vote(Xtr, ytr, C)(Xte)
    if not num_ks:
        return out
    kmax = min(max(num_ks), len(Xtr))
    nn = NearestNeighbors(n_neighbors=kmax).fit(Xtr)
    idx = nn.kneighbors(Xte, return_distance=False)
    for k in num_ks:
        k_eff = min(k, len(Xtr))
        pred = np.empty(len(Xte), dtype=int)
        for i in range(len(Xte)):
            nb = idx[i, :k_eff]
            yl = ytr[nb]
            if np.all(yl == yl[0]):
                pred[i] = yl[0]  # pure neighbourhood: vote (no SVM to fit)
            else:
                m = linear_svm(C).fit(Xtr[nb], yl)  # classes_ = [-1, 1]
                pred[i] = 1 if float(m.coef_[0] @ Xte[i] + m.intercept_[0]) > 0 else -1
        out[k] = pred
    return out


def tune_knn_svm(X, y, folds, ks, C, val_cap=50, seed=0):
    """Inner CV for k; to bound the number of per-point fits, each inner validation
    set is subsampled (without replacement, seeded) to at most `val_cap` points."""
    ks = ["all"] + [k for k in ks if k != "all"]  # ties favour the global case
    scores = {k: [] for k in ks}
    rng = np.random.default_rng(seed)
    for tr, va in folds:
        if len(va) > val_cap:
            va = np.sort(rng.choice(va, size=val_cap, replace=False))
        preds = knn_svm_predict_multi(X[tr], y[tr], X[va], ks, C)
        for k in ks:
            scores[k].append(np.mean(preds[k] == y[va]))
    mean_scores = [float(np.mean(scores[k])) for k in ks]
    i = int(np.argmax(mean_scores))
    return {"k": ks[i], "C": C}, mean_scores[i]


# --------------------------------------------------------------------------
# (b') cell-SVM: hard k-means partition, one linear SVM per cell

def kmeans_partition(X, M, seed):
    """(centres, labels) of a k-means partition with M cells (M = 1: one cell)."""
    if M == 1:
        return X.mean(0, keepdims=True), np.zeros(len(X), dtype=int)
    km = KMeans(n_clusters=M, n_init=1, random_state=seed).fit(X)
    return km.cluster_centers_, km.labels_


class CellSVM:
    def __init__(self, M, C, seed=0, partition=None):
        self.M, self.C, self.seed, self.partition = M, C, seed, partition

    def fit(self, X, y):
        self.centres_, cells = self.partition if self.partition is not None else kmeans_partition(X, self.M, self.seed)
        self.global_vote_ = majority(y)
        self.models_ = []
        for m in range(len(self.centres_)):
            sel = cells == m
            if sel.sum() == 0:
                v = self.global_vote_
                self.models_.append(lambda Z, v=v: np.full(len(Z), v))
            else:
                self.models_.append(fit_linear_or_vote(X[sel], y[sel], self.C))
        return self

    def predict(self, Z):
        cell = np.argmin(pairwise_distances(Z, self.centres_, metric="sqeuclidean"), axis=1)
        pred = np.empty(len(Z), dtype=int)
        for m in range(len(self.centres_)):
            sel = cell == m
            if sel.any():
                pred[sel] = self.models_[m](Z[sel])
        return pred


def tune_partition_family(Model, X, y, folds, Ms, Cs, seed):
    """Inner CV over (M, C) for CellSVM / LLSVM; the k-means partition of each inner
    training fold is computed once per M and shared across C. M = 1 is listed first."""
    configs, scores = [], []
    for M in Ms:
        parts = [kmeans_partition(X[tr], M, seed) for tr, _ in folds]
        for C in Cs:
            accs = []
            for (tr, va), part in zip(folds, parts):
                m = Model(M, C, seed, partition=part).fit(X[tr], y[tr])
                accs.append(np.mean(m.predict(X[va]) == y[va]))
            configs.append({"M": M, "C": C})
            scores.append(float(np.mean(accs)))
    i = int(np.argmax(scores))
    cfg = configs[i]
    return cfg, scores[i], Model(cfg["M"], cfg["C"], seed).fit(X, y)


def tune_cell_svm(X, y, folds, Ms, Cs, seed):
    return tune_partition_family(CellSVM, X, y, folds, Ms, Cs, seed)


# --------------------------------------------------------------------------
# (c) variable-bandwidth RBF kernel

def knn_radius(Xref, Xq, k, exclude_self):
    nn = NearestNeighbors(n_neighbors=k + (1 if exclude_self else 0)).fit(Xref)
    d, _ = nn.kneighbors(Xq)
    return d[:, -1]


def vb_kernel(X, aX, Z, aZ, d):
    """K(x,z) = (2 sqrt(a_x a_z)/(a_x+a_z))^{d/2} exp(-|x-z|^2/(a_x+a_z)).
    This is the normalised L2 inner product of the Gaussians exp(-|u-x|^2/a_x)
    and exp(-|u-z|^2/a_z), hence positive definite for any bandwidth map a(.)."""
    D2 = pairwise_distances(X, Z, metric="sqeuclidean")
    S = aX[:, None] + aZ[None, :]
    logpre = 0.5 * d * (np.log(2.0) + 0.5 * (np.log(aX)[:, None] + np.log(aZ)[None, :]) - np.log(S))
    return np.exp(logpre - D2 / S)


class VBRBF:
    """RBF-SVM with per-point bandwidth a(x) = a0 (r_k(x)/median r_k)^(2 beta)."""

    def __init__(self, gamma, beta, C, k_bw=10):
        self.gamma, self.beta, self.C, self.k_bw = gamma, beta, C, k_bw

    def bandwidths(self, Xq, exclude_self):
        if self.beta == 0:
            return np.full(len(Xq), 1.0 / (2 * self.gamma))
        r = knn_radius(self.Xtr_, Xq, self.k_bw, exclude_self)
        return (1.0 / (2 * self.gamma)) * (np.maximum(r, 1e-12) / self.rmed_) ** (2 * self.beta)

    def fit(self, X, y):
        self.Xtr_, self.d_ = X, X.shape[1]
        if self.beta != 0:
            rtr = knn_radius(X, X, self.k_bw, exclude_self=True)
            self.rmed_ = max(np.median(rtr), 1e-12)
        self.atr_ = self.bandwidths(X, exclude_self=True)
        K = vb_kernel(X, self.atr_, X, self.atr_, self.d_)
        self.svm_ = SVC(kernel="precomputed", C=self.C).fit(K, y)
        return self

    def predict(self, Z):
        aZ = self.bandwidths(Z, exclude_self=False)
        K = vb_kernel(Z, aZ, self.Xtr_, self.atr_, self.d_)
        return self.svm_.predict(K)


def tune_vbrbf(X, y, folds, Cs, gamma_mults, betas, k_bw, rbf_scores=None):
    """Inner CV over (beta, gamma, C).  With beta = 0 the model IS the RBF-SVM with the
    same (gamma, C), so its inner scores are taken from `rbf_scores` (same folds)
    when given; beta = 0 is listed first so that ties favour the global reference."""
    g0 = median_gamma(X)
    configs = [{"beta": b, "gamma_mult": gm, "C": C} for b in betas for gm in gamma_mults for C in Cs]
    # cache the Gram matrices per fold and (beta, gamma), then sweep C
    cache = {}

    def score(c):
        if c["beta"] == 0 and rbf_scores is not None and (c["gamma_mult"], c["C"]) in rbf_scores:
            return rbf_scores[(c["gamma_mult"], c["C"])]
        accs = []
        for fi, (tr, va) in enumerate(folds):
            key = (fi, c["beta"], c["gamma_mult"])
            if key not in cache:
                m = VBRBF(c["gamma_mult"] * g0, c["beta"], 1.0, k_bw)
                m.Xtr_, m.d_ = X[tr], X.shape[1]
                if c["beta"] != 0:
                    rtr = knn_radius(X[tr], X[tr], k_bw, exclude_self=True)
                    m.rmed_ = max(np.median(rtr), 1e-12)
                atr = m.bandwidths(X[tr], exclude_self=True)
                ava = m.bandwidths(X[va], exclude_self=False)
                cache[key] = (vb_kernel(X[tr], atr, X[tr], atr, X.shape[1]),
                              vb_kernel(X[va], ava, X[tr], atr, X.shape[1]))
            Ktr, Kva = cache[key]
            svm = SVC(kernel="precomputed", C=c["C"]).fit(Ktr, y[tr])
            accs.append(np.mean(svm.predict(Kva) == y[va]))
        return float(np.mean(accs))

    cfg, sc, _ = select(configs, score)
    model = VBRBF(cfg["gamma_mult"] * g0, cfg["beta"], cfg["C"], k_bw).fit(X, y)
    return dict(cfg, gamma=cfg["gamma_mult"] * g0), sc, model


# --------------------------------------------------------------------------
# (d) LLSVM-style mixture of local linear SVMs (soft partition)

class LLSVM:
    """f(x) = sum_m w_m(x) (<beta_m, x> + b_m), w = softmax(-|x-c_m|^2 / (2 s^2)),
    fitted as ONE linear SVM on the features [w_m(x) x, w_m(x)]_m."""

    def __init__(self, M, C, seed=0, partition=None):
        self.M, self.C, self.seed, self.partition = M, C, seed, partition

    def weights(self, X):
        if self.M == 1:
            return np.ones((len(X), 1))
        D2 = pairwise_distances(X, self.centres_, metric="sqeuclidean")
        L = -D2 / (2 * self.s2_)
        L -= L.max(1, keepdims=True)
        W = np.exp(L)
        return W / W.sum(1, keepdims=True)

    def features(self, X):
        W = self.weights(X)
        return np.hstack([np.hstack([W[:, [m]] * X, W[:, [m]]]) for m in range(W.shape[1])])

    def fit(self, X, y):
        if self.M > 1:
            self.centres_ = (self.partition if self.partition is not None else kmeans_partition(X, self.M, self.seed))[0]
            d2 = pairwise_distances(X, self.centres_, metric="sqeuclidean").min(1)
            self.s2_ = max(np.mean(d2), 1e-12)
        self.svm_ = linear_svm(self.C).fit(self.features(X), y)
        return self

    def predict(self, Z):
        return self.svm_.predict(self.features(Z))


def tune_llsvm(X, y, folds, Ms, Cs, seed):
    return tune_partition_family(LLSVM, X, y, folds, Ms, Cs, seed)
