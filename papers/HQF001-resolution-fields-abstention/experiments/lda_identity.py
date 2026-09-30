#!/usr/bin/env python3
"""HQF001 -- numerical verification of Proposition 1 (resolution margin vs LDA posterior margin).

Setting: K Gaussian classes N(mu_c, Sigma) with a shared covariance. The resolution score
with the *exact* metric A = Sigma^-1 is s(x) = d2_(2)(x) - d2_(1)(x), the gap between the two
smallest squared Mahalanobis distances to the class means.

Checks (all with the true parameters, no estimation):
  (i)   K=2, equal priors: s is a strictly increasing function of the posterior margin
        m = |p1 - p2| (m = tanh(s/4)); identical risk-coverage curves (AURC difference 0).
  (ii)  K=2, unequal priors: s is not a function of m; the signed score plus 2 log(pi1/pi2)
        restores the identity.
  (iii) K=3: s equals twice the log-ratio of the two largest posteriors, but is not a
        function of the posterior difference p_(1)-p_(2) nor of the max posterior; an
        explicit pair of points with equal s and different m is reported.
  (iv)  Isotropic local rescaling A(x) = lambda(x) Sigma^-1 changes the ranking (example).
Writes results/results_identity.json and results/tables_identity.md.
"""
import json
import os
import platform
import time

import numpy as np
import scipy
from scipy.stats import spearmanr

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
SEED = 20260930


def rc_curve(score, correct):
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
    return i / n, (prev[block] + (i - start[block]) * rate[block]) / i


def aurc(score, correct):
    return float(rc_curve(score, correct)[1].mean())


def posteriors(X, means, Sigma_inv, priors):
    K = len(means)
    d2 = np.empty((len(X), K))
    for c in range(K):
        diff = X - means[c]
        d2[:, c] = np.einsum("nd,de,ne->n", diff, Sigma_inv, diff)
    logp = np.log(priors)[None, :] - 0.5 * d2
    logp -= logp.max(1, keepdims=True)
    p = np.exp(logp)
    p /= p.sum(1, keepdims=True)
    return d2, p


def resolution_score(d2):
    o = np.sort(d2, 1)
    return o[:, 1] - o[:, 0]


def is_monotone_function(x, y, tol=1e-9):
    """True if y is a (weakly) increasing function of x on the sample, up to tol."""
    o = np.argsort(x, kind="mergesort")
    return bool(np.all(np.diff(y[o]) >= -tol))


def sample(rng, means, Sigma, priors, n):
    counts = rng.multinomial(n, priors)
    X = np.vstack([rng.multivariate_normal(means[c], Sigma, counts[c]) for c in range(len(means))])
    y = np.repeat(np.arange(len(means)), counts)
    return X, y


def main():
    t0 = time.process_time()
    rng = np.random.default_rng(SEED)
    d, n = 5, 4000
    q, r = np.linalg.qr(rng.standard_normal((d, d)))
    Sigma = q @ np.diag(np.geomspace(2.0, 0.1, d)) @ q.T
    Sigma_inv = np.linalg.inv(Sigma)
    out = {"meta": dict(seed=SEED, d=d, n=n, python=platform.python_version(),
                        numpy=np.__version__, scipy=scipy.__version__)}

    # (i) K = 2, equal priors
    means = np.vstack([np.zeros(d), 1.6 * rng.standard_normal(d) / np.sqrt(d)])
    priors = np.array([0.5, 0.5])
    X, y = sample(rng, means, Sigma, priors, n)
    d2, p = posteriors(X, means, Sigma_inv, priors)
    s = resolution_score(d2)
    m = np.abs(p[:, 0] - p[:, 1])
    pred_s = d2.argmin(1)
    pred_p = p.argmax(1)
    corr = pred_p == y
    out["K2_equal_priors"] = dict(
        predictions_agree=bool(np.all(pred_s == pred_p)),
        spearman_s_m=float(spearmanr(s, m).correlation),
        max_abs_m_minus_tanh=float(np.max(np.abs(m - np.tanh(s / 4)))),
        monotone=is_monotone_function(s, m),
        aurc_s=aurc(s, corr), aurc_m=aurc(m, corr),
        aurc_abs_diff=abs(aurc(s, corr) - aurc(m, corr)),
        error_rate=float(1 - corr.mean()),
    )

    # (ii) K = 2, unequal priors
    priors2 = np.array([0.8, 0.2])
    X, y = sample(rng, means, Sigma, priors2, n)
    d2, p = posteriors(X, means, Sigma_inv, priors2)
    s = resolution_score(d2)
    m = np.abs(p[:, 0] - p[:, 1])
    corr = p.argmax(1) == y
    corr_s = d2.argmin(1) == y
    signed = d2[:, 1] - d2[:, 0]  # positive favours class 0
    corrected = np.abs(signed + 2 * np.log(priors2[0] / priors2[1]))
    out["K2_unequal_priors"] = dict(
        priors=priors2.tolist(),
        predictions_agree=bool(np.all(d2.argmin(1) == p.argmax(1))),
        frac_predictions_differ=float(np.mean(d2.argmin(1) != p.argmax(1))),
        spearman_s_m=float(spearmanr(s, m).correlation),
        monotone=is_monotone_function(s, m),
        aurc_s_with_own_predictions=aurc(s, corr_s), aurc_m=aurc(m, corr),
        corrected_monotone=is_monotone_function(corrected, m),
        corrected_max_abs_m_minus_tanh=float(np.max(np.abs(m - np.tanh(corrected / 4)))),
        aurc_corrected=aurc(corrected, corr),
    )

    # (iii) K = 3, equal priors: explicit counterexample and sample statistics
    mu = np.array([[0.0, 0.0], [2.0, 0.0], [1.0, 2.0]])
    I2 = np.eye(2)
    pts = np.array([[0.75, 0.0], [0.75, 0.5]])
    d2c, pc = posteriors(pts, mu, I2, np.ones(3) / 3)
    sc = resolution_score(d2c)
    ps = -np.sort(-pc, 1)
    out["K3_counterexample"] = dict(
        means=mu.tolist(), points=pts.tolist(), d2=d2c.tolist(),
        score_s=sc.tolist(), posteriors=pc.tolist(),
        top2_diff=(ps[:, 0] - ps[:, 1]).tolist(), max_posterior=ps[:, 0].tolist(),
        two_log_ratio=(2 * (np.log(ps[:, 0]) - np.log(ps[:, 1]))).tolist(),
        nearest_two_are_classes_1_2=[bool(set(np.argsort(r)[:2]) == {0, 1}) for r in d2c],
    )
    means3 = np.vstack([np.zeros(d), rng.standard_normal(d), rng.standard_normal(d)]) * 0.6
    priors3 = np.ones(3) / 3
    X, y = sample(rng, means3, Sigma, priors3, n)
    d2, p = posteriors(X, means3, Sigma_inv, priors3)
    s = resolution_score(d2)
    ps = -np.sort(-p, 1)
    top2 = ps[:, 0] - ps[:, 1]
    msp = ps[:, 0]
    lr = 2 * (np.log(ps[:, 0]) - np.log(ps[:, 1]))
    corr = p.argmax(1) == y
    out["K3_sample"] = dict(
        predictions_agree=bool(np.all(d2.argmin(1) == p.argmax(1))),
        max_abs_s_minus_two_log_ratio=float(np.max(np.abs(s - lr))),
        monotone_in_log_ratio=is_monotone_function(s, lr),
        monotone_in_top2_diff=is_monotone_function(s, top2),
        monotone_in_msp=is_monotone_function(s, msp),
        spearman_s_top2=float(spearmanr(s, top2).correlation),
        spearman_s_msp=float(spearmanr(s, msp).correlation),
        aurc_s=aurc(s, corr), aurc_top2=aurc(top2, corr), aurc_msp=aurc(msp, corr),
        error_rate=float(1 - corr.mean()),
    )

    # (iv) isotropic local rescaling changes the ranking
    # two points in the K=2 problem with s1 < s2 but lambda1 s1 > lambda2 s2
    X, y = sample(rng, means, Sigma, priors, 200)
    d2, p = posteriors(X, means, Sigma_inv, priors)
    s = resolution_score(d2)
    i, j = np.argsort(s)[[50, 60]]
    lam = np.ones(len(s))
    lam[i] = 1.5 * s[j] / s[i]
    out["iso_rescaling_example"] = dict(
        s_i=float(s[i]), s_j=float(s[j]), lambda_i=float(lam[i]), lambda_j=1.0,
        rescaled_i=float(lam[i] * s[i]), rescaled_j=float(s[j]),
        ranking_flipped=bool((s[i] < s[j]) and (lam[i] * s[i] > s[j])),
    )
    out["meta"]["cpu_seconds"] = time.process_time() - t0

    os.makedirs(os.path.join(ROOT, "results"), exist_ok=True)
    with open(os.path.join(ROOT, "results", "results_identity.json"), "w") as fh:
        json.dump(out, fh, indent=1)
    L = ["# Verification of Proposition 1 (generated by experiments/lda_identity.py)", ""]
    for k, v in out.items():
        L.append(f"## {k}")
        L.append("")
        for kk, vv in v.items():
            L.append(f"- {kk}: {vv}")
        L.append("")
    with open(os.path.join(ROOT, "results", "tables_identity.md"), "w") as fh:
        fh.write("\n".join(L))
    print(json.dumps(out, indent=1))


if __name__ == "__main__":
    main()
