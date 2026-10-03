#!/usr/bin/env python3
"""Figures for HQF001 from results/*.json (plus a cheap 2-D illustration of the field)."""
import json
import os

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
from matplotlib.patches import Ellipse

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
FIG = os.path.join(ROOT, "figures")
os.makedirs(FIG, exist_ok=True)
res = json.load(open(os.path.join(ROOT, "results", "results.json")))
S = res["summary"]

# validated default palette (dataviz reference instance), slots 1-4 + text tokens
C1, C2, C3, C4 = "#2a78d6", "#eb6834", "#1baf7a", "#eda100"
TXT, TXT2, GRID = "#0b0b0b", "#52514e", "#e6e5e1"
plt.rcParams.update({"font.size": 9, "axes.edgecolor": TXT2, "axes.labelcolor": TXT, "xtick.color": TXT2,
                     "ytick.color": TXT2, "text.color": TXT, "axes.spines.top": False, "axes.spines.right": False,
                     "figure.dpi": 150, "savefig.dpi": 200})
DS_NAME = {"iris": "iris", "wine": "wine", "breast_cancer": "breast-cancer", "digits": "digits",
           "synth_informative": "synth-informative", "moons_aniso": "moons-aniso",
           "synth_classcov": "synth-classcov", "synth_lda": "synth-lda"}


def save(fig, name):
    fig.savefig(os.path.join(FIG, name + ".png"), bbox_inches="tight", facecolor="white")
    fig.savefig(os.path.join(FIG, name + ".pdf"), bbox_inches="tight", facecolor="white")
    plt.close(fig)


# (v0.1 had a forest plot of the paired differences here; it duplicated the table of differences and its
#  symlog axis compressed exactly the range |delta| < 1 where the anisotropic field lives: removed in v0.2.)

# ---- Figure: mean risk-coverage curves on three datasets
grid = np.array(res["meta"]["coverage_grid"])
show = ["digits", "moons_aniso", "synth_classcov"]
fig, axes = plt.subplots(1, 3, figsize=(9.0, 2.9), sharey=False)
for ax, ds in zip(axes, show):
    best = S[ds]["best_reference"]
    for m, label, col, ls in [("Field-aniso", "Field (aniso)", C1, "-"), ("Field-iso", "Field (iso)", C2, "-"),
                              (best, f"best ref.: {best}", C3, "-")]:
        ax.plot(100 * grid, 100 * np.array(S[ds]["methods"][m]["curve_mean"]), color=col, lw=1.8, ls=ls, label=label)
    ax.set_title(DS_NAME[ds], fontsize=9, color=TXT)
    ax.set_xlabel("coverage (%)")
    ax.grid(color=GRID, lw=0.8)
    ax.legend(frameon=False, fontsize=7.5, loc="upper left")
axes[0].set_ylabel("selective risk (%), mean over folds")
save(fig, "fig_rc_curves")

# ---- Figure: illustration of the resolution ellipses on moons-aniso (first two coordinates)
from sklearn.datasets import make_moons
from sklearn.neighbors import NearestNeighbors
from sklearn.preprocessing import StandardScaler
seed = res["meta"]["seed"]
rng = np.random.default_rng(seed)
n = 1200
X, y = make_moons(n_samples=n, noise=0.0, random_state=seed)
th = np.deg2rad(30.0)
R = np.array([[np.cos(th), -np.sin(th)], [np.sin(th), np.cos(th)]])
Cn = R @ np.diag([0.30 ** 2, 0.06 ** 2]) @ R.T
X = X + rng.multivariate_normal(np.zeros(2), Cn, n)
X = np.hstack([X, rng.standard_normal((n, 3))])
Xs = StandardScaler().fit_transform(X)
Km, alpha = 40, 0.2
nn = NearestNeighbors(n_neighbors=Km).fit(Xs)
gx, gy = np.meshgrid(np.linspace(Xs[:, 0].min(), Xs[:, 0].max(), 9), np.linspace(Xs[:, 1].min(), Xs[:, 1].max(), 7))
Q = np.c_[gx.ravel(), gy.ravel(), np.zeros((gx.size, 3))]
_, idx = nn.kneighbors(Q)
fig, ax = plt.subplots(figsize=(5.2, 3.9))
ax.scatter(Xs[y == 0, 0], Xs[y == 0, 1], s=6, color=C1, alpha=0.45, label="class 0", linewidths=0)
ax.scatter(Xs[y == 1, 0], Xs[y == 1, 1], s=6, color=C2, alpha=0.45, label="class 1", linewidths=0)
for q, ii in zip(Q, idx):
    P = Xs[ii][:, :2]
    C = np.cov(P.T)
    Sm = (1 - alpha) * C + alpha * np.trace(C) / 2 * np.eye(2)
    w, V = np.linalg.eigh(Sm)
    ang = np.degrees(np.arctan2(V[1, 1], V[0, 1]))
    e = Ellipse(q[:2], 2 * np.sqrt(w[1]) * 0.6, 2 * np.sqrt(w[0]) * 0.6, angle=ang, fill=False, ec=TXT, lw=0.9)
    ax.add_patch(e)
    ax.plot(q[0], q[1], ".", color=TXT, ms=3)
ax.set_xlabel("standardised coordinate 1")
ax.set_ylabel("standardised coordinate 2")
ax.set_title(f"moons-aniso: neighbourhood ellipses ($K_m={Km}$, $\\alpha={alpha}$), 2-D projection", fontsize=9)
ax.legend(frameon=False, fontsize=8, loc="upper left", bbox_to_anchor=(1.01, 1.0), markerscale=2.5)
ax.set_aspect("equal")
save(fig, "fig_field_moons")

# ---- Figure: Proposition 3.1 illustration (K=2 identity and K=3 non-identity), from the true model
d = 5
rng = np.random.default_rng(seed)
q, r = np.linalg.qr(rng.standard_normal((d, d)))
Sigma = q @ np.diag(np.geomspace(2.0, 0.1, d)) @ q.T
Si = np.linalg.inv(Sigma)


def post(Xp, means, priors):
    d2 = np.stack([np.einsum("nd,de,ne->n", Xp - mu, Si, Xp - mu) for mu in means], 1)
    lp = np.log(priors)[None] - 0.5 * d2
    lp -= lp.max(1, keepdims=True)
    p = np.exp(lp)
    p /= p.sum(1, keepdims=True)
    return d2, p


fig, axes = plt.subplots(1, 2, figsize=(7.6, 3.0))
means = np.vstack([np.zeros(d), 1.6 * rng.standard_normal(d) / np.sqrt(d)])
Xp = np.vstack([rng.multivariate_normal(mu, Sigma, 800) for mu in means])
d2, p = post(Xp, means, np.array([0.5, 0.5]))
s = np.sort(d2, 1)[:, 1] - np.sort(d2, 1)[:, 0]
m = np.abs(p[:, 0] - p[:, 1])
axes[0].scatter(s, m, s=5, color=C1, alpha=0.5, linewidths=0, label="sample points")
ss = np.linspace(0, s.max(), 200)
axes[0].plot(ss, np.tanh(ss / 4), color=TXT, lw=1.2, label=r"$m=\tanh(s/4)$")
axes[0].set_xlabel(r"resolution margin $s$ (metric $\Sigma^{-1}$)")
axes[0].set_ylabel(r"LDA posterior margin $m$")
axes[0].set_title("K = 2, equal priors: monotone", fontsize=9)
axes[0].legend(frameon=False, fontsize=8)
axes[0].grid(color=GRID, lw=0.8)
means3 = np.vstack([np.zeros(d), rng.standard_normal(d), rng.standard_normal(d)]) * 0.6
Xp = np.vstack([rng.multivariate_normal(mu, Sigma, 600) for mu in means3])
d2, p = post(Xp, means3, np.ones(3) / 3)
s = np.sort(d2, 1)[:, 1] - np.sort(d2, 1)[:, 0]
ps = -np.sort(-p, 1)
axes[1].scatter(s, ps[:, 0] - ps[:, 1], s=5, color=C1, alpha=0.5, linewidths=0, label=r"$p_{(1)}-p_{(2)}$")
axes[1].scatter(s, ps[:, 0], s=5, color=C2, alpha=0.5, linewidths=0, label=r"$p_{(1)}$ (MSP)")
axes[1].set_xlabel(r"resolution margin $s$ (metric $\Sigma^{-1}$)")
axes[1].set_ylabel("posterior-based score")
axes[1].set_title("K = 3: not a function of $s$", fontsize=9)
axes[1].legend(frameon=False, fontsize=8, loc="lower right")
axes[1].grid(color=GRID, lw=0.8)
save(fig, "fig_identity")
print("figures written to", FIG)
