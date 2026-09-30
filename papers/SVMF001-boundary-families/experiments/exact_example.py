#!/usr/bin/env python3
"""SVMF001 -- exact computations and simulations for the 'no-gain' proposition.

Model (Gaussian location, hyperplane Bayes rule):  Y uniform on {-1,+1},
  X1 | Y ~ N(Y mu, 1),  X2,...,Xd ~ N(0,1) independent of (X1, Y).
Bayes rule sign(x1), Bayes risk Phi(-mu).  With mu = delta/2 and delta = 3.29 this
is the population behind the 'gauss_linear' dataset of run_comparison.py.

Part A (exact).  Nearest-centroid threshold t = (mean X1 of positives + mean X1 of
negatives)/2 fitted on n points.  Given the class counts (N+, N-), t ~ N(0, s^2)
with s^2 = (1/N+ + 1/N-)/4 and E[R(t)] = Phi(-mu / sqrt(1 + s^2)); if a class is
missing the rule votes and its risk is 1/2.  R_nc(n) is the binomial average.
Part B (exact).  Partition-localised version: M cells of equal probability defined
by a coordinate independent of (X1, Y); cell m fits its own threshold on its N_m ~
Bin(n, 1/M) points.  Expected risk = E[R_nc(N_m)]  (Proposition 2 of the paper).
Part C (Monte Carlo check of A and B).
Part D (simulation, illustration only): kNN-localised nearest-centroid and
kNN-localised linear SVM in d = 2, risk versus k; learning curve of the global
linear SVM in d = 10 (the monotonicity assumption of Proposition 2, checked
empirically for the SVM).
"""
import json
import os
import platform
import time

for _v in ("OMP_NUM_THREADS", "OPENBLAS_NUM_THREADS", "MKL_NUM_THREADS"):
    os.environ.setdefault(_v, "1")

import numpy as np
import scipy
import sklearn
from scipy.stats import binom, norm
from sklearn.neighbors import NearestNeighbors
from sklearn.svm import SVC

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
SEED = 20260930
DELTA = 3.29
MU = DELTA / 2
BAYES = float(norm.cdf(-MU))


# ---------------------------------------------------------------- Part A (exact)

def risk_threshold(t):
    """Risk of the rule 'predict +1 iff x1 > t' (exact)."""
    return 0.5 * (norm.cdf(t - MU) + norm.cdf(-t - MU))


def risk_given_counts(np_, nm):
    """Vectorised: risk 1/2 when a class is missing, Phi(-mu/sqrt(1+s^2)) otherwise."""
    np_, nm = np.asarray(np_, float), np.asarray(nm, float)
    with np.errstate(divide="ignore"):
        s2 = 0.25 * (1.0 / np.where(np_ > 0, np_, np.inf) + 1.0 / np.where(nm > 0, nm, np.inf))
    return np.where((np_ > 0) & (nm > 0), norm.cdf(-MU / np.sqrt(1.0 + s2)), 0.5)


_RNC = {}


def R_nc(n):
    """Exact expected risk of the nearest-centroid threshold with n iid points."""
    n = int(n)
    if n not in _RNC:
        if n == 0:
            _RNC[n] = 0.5
        else:
            ks = np.arange(n + 1)
            _RNC[n] = float(np.sum(binom.pmf(ks, n, 0.5) * risk_given_counts(ks, n - ks)))
    return _RNC[n]


def R_partition(n, M):
    """Exact expected risk of the M-cell partition-localised rule (equal cells)."""
    ks = np.arange(n + 1)
    p = binom.pmf(ks, n, 1.0 / M)
    return float(np.sum(p * np.array([R_nc(k) for k in ks])))


# ---------------------------------------------------------------- Part D helpers

def sample(rng, n, d):
    y = rng.choice([-1, 1], size=n)
    X = rng.normal(size=(n, d))
    X[:, 0] += y * MU
    return X, y


def risk_linear(w, b):
    """Exact risk of sign(w.x + b) under the model (any d)."""
    nw = np.linalg.norm(w)
    if nw == 0:
        return 0.5
    return 0.5 * (norm.cdf(-(w[0] * MU + b) / nw) + norm.cdf((b - w[0] * MU) / nw))


def eta(x1):
    """P(Y = +1 | X1 = x1)."""
    return 1.0 / (1.0 + np.exp(-2.0 * MU * x1))


def cond_risk(x1, pred):
    e = eta(x1)
    return np.where(pred == 1, 1.0 - e, e)


def knn_centroid_risk(rng, n, ks, n_test, reps):
    """kNN-localised nearest-centroid threshold in d = 2; exact conditional risk
    averaged over test points (k = n is the global rule)."""
    out = {k: [] for k in ks}
    for _ in range(reps):
        X, y = sample(rng, n, 2)
        Xt, _ = sample(rng, n_test, 2)
        nn = NearestNeighbors(n_neighbors=max(ks)).fit(X)
        idx = nn.kneighbors(Xt, return_distance=False)
        for k in ks:
            nb = idx[:, :k]
            yl = y[nb]
            x1 = X[nb, 0]
            pos = yl == 1
            npos = pos.sum(1)
            with np.errstate(invalid="ignore", divide="ignore"):
                mpos = np.where(npos > 0, (x1 * pos).sum(1) / np.maximum(npos, 1), np.nan)
                mneg = np.where(k - npos > 0, (x1 * ~pos).sum(1) / np.maximum(k - npos, 1), np.nan)
            t = 0.5 * (mpos + mneg)
            pred = np.where(Xt[:, 0] > t, 1, -1)
            pure = (npos == 0) | (npos == k)
            pred[pure] = np.where(npos[pure] > 0, 1, -1)
            out[k].append(float(np.mean(cond_risk(Xt[:, 0], pred))))
    return {k: {"mean": float(np.mean(v)), "se": float(np.std(v, ddof=1) / np.sqrt(len(v)))} for k, v in out.items()}


def knn_svm_risk(rng, n, ks, n_test, reps, C=1.0):
    """kNN-localised linear SVM (C fixed) in d = 2; k = 'all' is the global linear SVM."""
    out = {k: [] for k in ks}
    for _ in range(reps):
        X, y = sample(rng, n, 2)
        Xt, _ = sample(rng, n_test, 2)
        num = [k for k in ks if k != "all"]
        if "all" in ks:
            m = SVC(kernel="linear", C=C).fit(X, y)
            out["all"].append(float(risk_linear(m.coef_[0], m.intercept_[0])))
        nn = NearestNeighbors(n_neighbors=max(num)).fit(X)
        idx = nn.kneighbors(Xt, return_distance=False)
        for k in num:
            pred = np.empty(n_test, dtype=int)
            for i in range(n_test):
                nb = idx[i, :k]
                yl = y[nb]
                if np.all(yl == yl[0]):
                    pred[i] = yl[0]
                else:
                    m = SVC(kernel="linear", C=C).fit(X[nb], yl)
                    pred[i] = 1 if float(m.coef_[0] @ Xt[i] + m.intercept_[0]) > 0 else -1
            out[k].append(float(np.mean(cond_risk(Xt[:, 0], pred))))
    return {str(k): {"mean": float(np.mean(v)), "se": float(np.std(v, ddof=1) / np.sqrt(len(v)))} for k, v in out.items()}


def svm_learning_curve(rng, ns, d, reps, C=1.0):
    out = {}
    for n in ns:
        r = []
        for _ in range(reps):
            X, y = sample(rng, n, d)
            m = SVC(kernel="linear", C=C).fit(X, y)
            r.append(risk_linear(m.coef_[0], m.intercept_[0]))
        out[n] = {"mean": float(np.mean(r)), "se": float(np.std(r, ddof=1) / np.sqrt(reps))}
    return out


def svm_partition_curve(rng, n, Ms, d, reps, C=1.0):
    """Monte Carlo: partition-localised linear SVM (cells by an independent coordinate),
    exact risk of each cell rule averaged with the cell probabilities."""
    out = {}
    for M in Ms:
        r = []
        for _ in range(reps):
            X, y = sample(rng, n, d)
            z = rng.integers(M, size=n)  # cell label independent of (X, Y)
            tot = 0.0
            for m_ in range(M):
                sel = z == m_
                if sel.sum() == 0 or len(np.unique(y[sel])) < 2:
                    tot += 0.5 / M
                else:
                    m = SVC(kernel="linear", C=C).fit(X[sel], y[sel])
                    tot += risk_linear(m.coef_[0], m.intercept_[0]) / M
            r.append(tot)
        out[M] = {"mean": float(np.mean(r)), "se": float(np.std(r, ddof=1) / np.sqrt(reps))}
    return out


# ---------------------------------------------------------------- main

def main():
    t0 = time.time()
    rng = np.random.default_rng(SEED)
    res = {"meta": {"seed": SEED, "delta": DELTA, "mu": MU, "bayes": BAYES,
                    "python": platform.python_version(), "numpy": np.__version__,
                    "scipy": scipy.__version__, "sklearn": sklearn.__version__}}

    # A: exact learning curve of the nearest-centroid threshold
    ns = [10, 20, 40, 80, 160, 320, 640, 1280]
    res["A_learning_curve"] = {n: {"risk": R_nc(n), "excess": R_nc(n) - BAYES} for n in ns}
    # strict monotonicity check on a fine grid (a proof is in the paper; this is a sanity check)
    curve = np.array([R_nc(n) for n in range(2, 1001)])
    res["A_monotone_check"] = {"range": [2, 1000], "strictly_decreasing": bool(np.all(np.diff(curve) < 0))}

    # B: exact partition-localised risk, n = 320 (training size of gauss_linear in the main protocol)
    n0, Ms = 320, [1, 2, 4, 8, 16, 32]
    res["B_partition"] = {"n": n0, "rows": {M: {"risk": R_partition(n0, M), "excess": R_partition(n0, M) - BAYES,
                                             "excess_ratio_vs_global": (R_partition(n0, M) - BAYES) / (R_nc(n0) - BAYES)} for M in Ms}}
    res["B_partition_vs_n"] = {n: {M: R_partition(n, M) - BAYES for M in [1, 4, 16]} for n in [40, 80, 160, 320, 640, 1280]}

    # C: Monte Carlo check of A and B (exact risk of each fitted rule, averaged over samples)
    reps = 2000
    mc_glob, mc_part = [], []
    for _ in range(reps):
        X, y = sample(rng, n0, 2)
        def fit_t(Xs, ys):
            if np.all(ys == ys[0]):
                return None, int(ys[0])
            return 0.5 * (Xs[ys == 1, 0].mean() + Xs[ys == -1, 0].mean()), None
        t, v = fit_t(X, y)
        mc_glob.append(risk_threshold(t) if t is not None else 0.5)
        u = rng.random(n0)  # independent partition coordinate, 4 equal cells
        tot = 0.0
        for c in range(4):
            sel = (u >= c / 4) & (u < (c + 1) / 4)
            if sel.sum() == 0:
                tot += 0.5 / 4
                continue
            t, v = fit_t(X[sel], y[sel])
            tot += (risk_threshold(t) if t is not None else 0.5) / 4
        mc_part.append(tot)
    res["C_montecarlo"] = {"reps": reps, "n": n0,
                           "global": {"mean": float(np.mean(mc_glob)), "se": float(np.std(mc_glob, ddof=1) / np.sqrt(reps)), "exact": R_nc(n0)},
                           "partition_M4": {"mean": float(np.mean(mc_part)), "se": float(np.std(mc_part, ddof=1) / np.sqrt(reps)), "exact": R_partition(n0, 4)}}

    # D1: kNN-localised nearest centroid (d = 2), exact conditional risk on test points
    ks = [5, 10, 20, 40, 80, 160, 320]
    res["D1_knn_centroid"] = {"n": n0, "d": 2, "reps": 200, "n_test": 1000,
                              "rows": knn_centroid_risk(rng, n0, ks, 1000, 200)}
    # D2: kNN-localised linear SVM (d = 2), C = 1
    res["D2_knn_svm"] = {"n": n0, "d": 2, "reps": 16, "n_test": 125, "C": 1.0,
                         "rows": knn_svm_risk(rng, n0, [10, 20, 40, 80, 160, "all"], 125, 16)}
    # D3: learning curve of the global linear SVM in d = 10 (monotonicity assumption)
    res["D3_svm_learning_curve"] = {"d": 10, "reps": 200, "C": 1.0,
                                    "rows": svm_learning_curve(rng, [20, 40, 80, 160, 320, 640], 10, 200)}
    # D4: partition-localised linear SVM by an independent cell label, d = 10, n = 320
    res["D4_svm_partition"] = {"d": 10, "n": n0, "reps": 200, "C": 1.0,
                               "rows": svm_partition_curve(rng, n0, [1, 2, 4, 8], 10, 200)}

    # E: the prefactor in Lemma 2.2 is needed -- a five-point witness (no randomness) for which the
    # prefactor-free matrix exp(-|x_i-x_j|^2/(a_i+a_j)) has a negative eigenvalue while K_a does not
    Xw = np.array([[0.841], [-0.144], [1.31], [-1.189], [-0.159]])
    aw = np.array([65.85, 0.0658, 0.0789, 0.0897, 153.0])
    D2 = (Xw - Xw.T) ** 2
    S = aw[:, None] + aw[None, :]
    prefree = np.exp(-D2 / S)
    full = (2 * np.sqrt(np.outer(aw, aw)) / S) ** 0.5 * prefree
    res["E_prefactor_witness"] = {"x": Xw.ravel().tolist(), "a": aw.tolist(), "d": 1,
                                  "min_eig_prefactor_free": float(np.linalg.eigvalsh(prefree).min()),
                                  "min_eig_full_kernel": float(np.linalg.eigvalsh(full).min())}

    res["meta"]["seconds"] = time.time() - t0
    os.makedirs(os.path.join(ROOT, "results"), exist_ok=True)
    with open(os.path.join(ROOT, "results", "exact_example.json"), "w") as fh:
        json.dump(res, fh, indent=1, default=str)

    # markdown
    L = ["# SVMF001 -- exact example (Gaussian location model, mu = %.3f, Bayes risk %.4f)\n" % (MU, BAYES)]
    L.append("## A. Exact learning curve of the nearest-centroid threshold\n\n| n | risk | excess |\n|---|---|---|")
    for n, r in res["A_learning_curve"].items():
        L.append(f"| {n} | {r['risk']:.5f} | {r['excess']:.5f} |")
    L.append(f"\nStrictly decreasing on n = 2..1000: {res['A_monotone_check']['strictly_decreasing']}\n")
    L.append(f"## B. Partition-localised rule, n = {n0} (exact)\n\n| M | risk | excess | excess ratio vs M=1 |\n|---|---|---|---|")
    for M, r in res["B_partition"]["rows"].items():
        L.append(f"| {M} | {r['risk']:.5f} | {r['excess']:.5f} | {r['excess_ratio_vs_global']:.2f} |")
    c = res["C_montecarlo"]
    L.append(f"\n## C. Monte Carlo check ({reps} samples)\n\n- global: {c['global']['mean']:.5f} +- {c['global']['se']:.5f} (exact {c['global']['exact']:.5f})")
    L.append(f"- partition M=4: {c['partition_M4']['mean']:.5f} +- {c['partition_M4']['se']:.5f} (exact {c['partition_M4']['exact']:.5f})\n")
    L.append("## D1. kNN-localised nearest centroid, d = 2 (simulation)\n\n| k | risk | se |\n|---|---|---|")
    for k, r in res["D1_knn_centroid"]["rows"].items():
        L.append(f"| {k} | {r['mean']:.5f} | {r['se']:.5f} |")
    L.append("\n## D2. kNN-localised linear SVM, d = 2 (simulation)\n\n| k | risk | se |\n|---|---|---|")
    for k, r in res["D2_knn_svm"]["rows"].items():
        L.append(f"| {k} | {r['mean']:.5f} | {r['se']:.5f} |")
    L.append("\n## D3. Learning curve of the global linear SVM, d = 10 (simulation)\n\n| n | risk | se |\n|---|---|---|")
    for n, r in res["D3_svm_learning_curve"]["rows"].items():
        L.append(f"| {n} | {r['mean']:.5f} | {r['se']:.5f} |")
    L.append("\n## D4. Partition-localised linear SVM (independent cells), d = 10, n = 320 (simulation)\n\n| M | risk | se |\n|---|---|---|")
    for M, r in res["D4_svm_partition"]["rows"].items():
        L.append(f"| {M} | {r['mean']:.5f} | {r['se']:.5f} |")
    w = res["E_prefactor_witness"]
    L.append(f"\n## E. Prefactor witness (d = 1, five points)\n\nx = {w['x']}, a = {w['a']}: min eigenvalue of the prefactor-free matrix {w['min_eig_prefactor_free']:.3f}; of K_a {w['min_eig_full_kernel']:.3f}\n")
    with open(os.path.join(ROOT, "results", "exact_example.md"), "w") as fh:
        fh.write("\n".join(L) + "\n")

    # figure
    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt
    fig, axes = plt.subplots(1, 3, figsize=(12.5, 3.5))
    ax = axes[0]
    for M, col in zip([1, 4, 16], ["#1b6ca8", "#c0392b", "#7a4fa3"]):
        xs = sorted(res["B_partition_vs_n"].keys())
        ax.plot(xs, [res["B_partition_vs_n"][n][M] for n in xs], "o-", color=col, label=f"M = {M} cells")
    ax.set_xscale("log"); ax.set_yscale("log")
    ax.set_xlabel("n"); ax.set_ylabel("excess risk (exact)"); ax.set_title("partition-localised nearest centroid")
    ax.legend(fontsize=8)
    ax = axes[1]
    r1 = res["D1_knn_centroid"]["rows"]
    ax.errorbar(list(r1.keys()), [r1[k]["mean"] - BAYES for k in r1], yerr=[r1[k]["se"] for k in r1], fmt="o-", color="#1b6ca8", label="kNN nearest centroid")
    r2 = res["D2_knn_svm"]["rows"]
    kk = [k for k in r2 if k != "all"]
    ax.errorbar([int(k) for k in kk], [r2[k]["mean"] - BAYES for k in kk], yerr=[r2[k]["se"] for k in kk], fmt="s-", color="#c0392b", label="kNN linear SVM")
    ax.axhline(r2["all"]["mean"] - BAYES, color="#c0392b", ls="--", lw=1, label="global linear SVM")
    ax.set_xscale("log"); ax.set_yscale("log")
    ax.set_xlabel("k (local sample size)"); ax.set_ylabel("excess risk"); ax.set_title("kNN-localised rules, d = 2, n = 320")
    ax.legend(fontsize=8)
    ax = axes[2]
    r3 = res["D3_svm_learning_curve"]["rows"]
    ax.errorbar(list(r3.keys()), [r3[n]["mean"] - BAYES for n in r3], yerr=[r3[n]["se"] for n in r3], fmt="s-", color="#c0392b", label="linear SVM, d = 10 (MC)")
    xs = sorted(res["A_learning_curve"].keys())
    ax.plot(xs, [res["A_learning_curve"][n]["excess"] for n in xs], "o-", color="#1b6ca8", label="nearest centroid (exact)")
    ax.set_xscale("log"); ax.set_yscale("log")
    ax.set_xlabel("n"); ax.set_ylabel("excess risk"); ax.set_title("learning curves")
    ax.legend(fontsize=8)
    fig.tight_layout()
    os.makedirs(os.path.join(ROOT, "figures"), exist_ok=True)
    fig.savefig(os.path.join(ROOT, "figures", "fig_exact.png"), dpi=160)
    fig.savefig(os.path.join(ROOT, "figures", "fig_exact.pdf"))
    print(f"exact example done in {res['meta']['seconds']:.1f}s")


if __name__ == "__main__":
    main()
