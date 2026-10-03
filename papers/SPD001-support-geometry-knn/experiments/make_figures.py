#!/usr/bin/env python3
"""Figures for SPD001 from results/*.json (and one schematic computed from the moons data).

  figures/decomposition.{pdf,png}  the (tangential, orthogonal, depth) decomposition on make_moons
  figures/forest.{pdf,png}         paired differences with bootstrap CIs: TOD - best reference, ablations
  figures/regime.{pdf,png}         moons regime scan: accuracy against the number of noise coordinates
"""
import json
import os
import sys

for _v in ("OMP_NUM_THREADS", "OPENBLAS_NUM_THREADS", "MKL_NUM_THREADS"):
    os.environ.setdefault(_v, "1")

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import support_geometry as sg  # noqa: E402

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
FIG = os.path.join(ROOT, "figures")
os.makedirs(FIG, exist_ok=True)

# validated categorical palette (fixed order, never cycled)
BLUE, ORANGE, AQUA, YELLOW, MAGENTA, GREEN, VIOLET, RED = (
    "#2a78d6", "#eb6834", "#1baf7a", "#eda100", "#e87ba4", "#008300", "#4a3aa7", "#e34948")
INK, INK2, GRID = "#0b0b0b", "#52514e", "#d9d8d3"
plt.rcParams.update({"font.size": 9, "axes.edgecolor": INK2, "axes.labelcolor": INK, "xtick.color": INK2,
                     "ytick.color": INK2, "axes.spines.top": False, "axes.spines.right": False,
                     "grid.color": GRID, "grid.linewidth": 0.6, "legend.frameon": False})

res = json.load(open(os.path.join(ROOT, "results", "results.json")))
reg = json.load(open(os.path.join(ROOT, "results", "results_regime.json")))
LABEL = {"iris": "iris", "wine": "wine", "breast_cancer": "breast cancer", "digits": "digits",
         "swiss_roll": "swiss roll", "moons": "moons", "moons_noise10": "moons + 10 noise dims", "spheres": "spheres"}


def save(fig, name):
    fig.savefig(os.path.join(FIG, name + ".pdf"), bbox_inches="tight")
    fig.savefig(os.path.join(FIG, name + ".png"), bbox_inches="tight", dpi=200)
    plt.close(fig)


# ---------------------------------------------------------------- schematic
def schematic():
    data, _ = sg.make_datasets(sg.SEED)
    X, y, _ = data["moons"]
    X = (X - X.mean(0)) / X.std(0)
    k = 10
    # deterministic choice of the query: the grid point nearest the origin whose tangential
    # and orthogonal components with respect to BOTH classes are visible (between 0.3 and 0.9)
    best = None
    for gx in np.linspace(-1.5, 1.5, 61):
        for gy in np.linspace(-1.5, 1.5, 61):
            qq = np.array([gx, gy])
            ok = True
            for c in (0, 1):
                idx = np.flatnonzero(y == c)
                Xn = X[idx[np.argsort(((X[idx] - qq) ** 2).sum(1))[:k]]]
                mu = Xn.mean(0)
                u = np.linalg.svd(Xn - mu, full_matrices=False)[2][0]
                r = qq - mu
                T = abs(r @ u)
                O = np.sqrt(max(r @ r - T * T, 0.0))
                if not (0.3 <= T <= 0.9 and 0.3 <= O <= 0.9):
                    ok = False
            if ok and (best is None or gx * gx + gy * gy < best[0]):
                best = (gx * gx + gy * gy, qq)
    q = best[1]
    fig, axes = plt.subplots(1, 2, figsize=(7.2, 3.3))
    for ax, c, col, title in ((axes[0], 1, ORANGE, "components w.r.t. class 1"),
                              (axes[1], 0, BLUE, "components w.r.t. class 0")):
        for cc, ccol in ((0, BLUE), (1, ORANGE)):
            ax.scatter(*X[y == cc].T, s=6, color=ccol, alpha=0.18, linewidths=0)
        idx = np.flatnonzero(y == c)
        nb = idx[np.argsort(((X[idx] - q) ** 2).sum(1))[:k]]
        Xn = X[nb]
        mu = Xn.mean(0)
        V = Xn - mu
        u = np.linalg.svd(V, full_matrices=False)[2][0]
        r = q - mu
        t = (r @ u) * u
        o = r - t
        ax.scatter(*Xn.T, s=22, facecolor="none", edgecolor=col, linewidths=1.0, zorder=3)
        span = np.linspace(-1.1, 1.1, 2)
        ax.plot(mu[0] + span * u[0], mu[1] + span * u[1], color=col, lw=1.2, zorder=2)
        ax.plot([mu[0], mu[0] + t[0]], [mu[1], mu[1] + t[1]], color=INK, lw=1.6, zorder=4)
        ax.plot([mu[0] + t[0], q[0]], [mu[1] + t[1], q[1]], color=INK, lw=1.6, ls="--", zorder=4)
        for xi in Xn:
            uv = (xi - q) / np.linalg.norm(xi - q)
            ax.plot([q[0], q[0] + 0.3 * uv[0]], [q[1], q[1] + 0.3 * uv[1]], color=INK2, lw=0.6, zorder=3)
        ax.scatter(*mu, s=36, color=col, edgecolor=INK, zorder=5, marker="s")
        ax.scatter(*q, s=46, color=INK, zorder=6, marker="*")
        U = (Xn - q) / np.linalg.norm(Xn - q, axis=1, keepdims=True)
        depth = 1 - np.linalg.norm(U.mean(0))
        ax.text(0.02, 0.97, f"$T={np.linalg.norm(t):.2f}$, $O={np.linalg.norm(o):.2f}$, depth $={depth:.2f}$",
                transform=ax.transAxes, va="top", fontsize=8.5, color=INK)
        ax.set_title(title, fontsize=9.5, color=INK)
        ax.set_aspect("equal")
        ax.set_xlim(-2.2, 2.4)
        ax.set_ylim(-2.1, 2.1)
        ax.set_xticks([])
        ax.set_yticks([])
        for s in ("left", "bottom"):
            ax.spines[s].set_visible(False)
    axes[0].text(q[0] + 0.12, q[1] - 0.25, "$q$", fontsize=9)
    axes[1].text(q[0] + 0.12, q[1] - 0.25, "$q$", fontsize=9)
    save(fig, "decomposition")


# ---------------------------------------------------------------- forest plot
def nb_interval(a, b, n_splits):
    """95% interval of the mean fold-level difference a - b with the Nadeau-Bengio variance
    (same formula as make_numbers.py), in accuracy points."""
    import math
    from scipy.stats import t as student_t
    d = np.asarray(a, float) - np.asarray(b, float)
    J = len(d)
    half = student_t.ppf(0.975, J - 1) * math.sqrt((1.0 / J + 1.0 / (n_splits - 1)) * d.var(ddof=1))
    return 100 * (d.mean() - half), 100 * (d.mean() + half)


def forest():
    comp = res["comparison"]
    data = res["datasets"]
    names = list(data.keys())
    # drawn at its printed size (0.7 of the text width, about 4.4 in) so that the fonts stay legible
    fig, axes = plt.subplots(1, 2, figsize=(4.7, 2.3), sharey=True)
    ypos = np.arange(len(names))[::-1]
    ax = axes[0]
    for yy, nm in zip(ypos, names):
        s = comp[nm]["vs_best"]
        sig = s["ci_low"] > 0 or s["ci_high"] < 0
        lo, hi = nb_interval(data[nm]["methods"]["TOD"]["acc"], data[nm]["methods"][comp[nm]["best_reference"]]["acc"],
                             data[nm]["n_splits"])
        ax.plot([lo, hi], [yy, yy], color=INK2, lw=0.6, alpha=0.7, zorder=1)      # thin: NB interval
        ax.plot([100 * s["ci_low"], 100 * s["ci_high"]], [yy, yy], color=INK if sig else INK2, lw=1.8, zorder=2)
        ax.plot(100 * s["mean"], yy, "o", color=INK if sig else INK2, ms=5, zorder=3)
    ax.axvline(0, color=GRID, lw=1, zorder=0)
    ax.set_yticks(ypos)
    ax.set_yticklabels([f"{LABEL[n]} ({'/'.join(comp[n].get('best_reference_tied', [comp[n]['best_reference']]))})" for n in names], fontsize=6.5)
    ax.set_xlabel("TOD $-$ best ref., points", fontsize=7)
    ax.tick_params(axis="x", labelsize=6.5)
    ax.grid(axis="x")
    ax.set_title("primary comparison", fontsize=8)
    ax = axes[1]
    cols = {"TO": BLUE, "TD": ORANGE, "OD": AQUA}
    lab = {"TO": "TOD $-$ TO (depth removed)", "TD": "TOD $-$ TD (orthogonal removed)",
           "OD": "TOD $-$ OD (tangential removed)"}
    off = {"TO": 0.22, "TD": 0.0, "OD": -0.22}
    for m in ("TO", "TD", "OD"):
        for yy, nm in zip(ypos, names):
            s = comp[nm]["ablation"][m]
            lo, hi = nb_interval(data[nm]["methods"]["TOD"]["acc"], data[nm]["methods"][m]["acc"], data[nm]["n_splits"])
            ax.plot([lo, hi], [yy + off[m]] * 2, color=cols[m], lw=0.6, alpha=0.5, zorder=1)   # thin: NB interval
            ax.plot([100 * s["ci_low"], 100 * s["ci_high"]], [yy + off[m]] * 2, color=cols[m], lw=1.6, zorder=2)
            ax.plot(100 * s["mean"], yy + off[m], "o", color=cols[m], ms=3.5, zorder=3)
        ax.plot([], [], "o-", color=cols[m], ms=3.5, lw=1.6, label=lab[m])
    ax.plot([], [], "-", color=INK2, lw=0.6, label="thin: Nadeau$-$Bengio interval")
    ax.axvline(0, color=GRID, lw=1, zorder=0)
    ax.grid(axis="x")
    ax.set_xlabel("TOD $-$ reduced model, points", fontsize=7)
    ax.tick_params(axis="x", labelsize=6.5)
    ax.set_title("ablations", fontsize=8)
    fig.legend(*ax.get_legend_handles_labels(), fontsize=6.5, loc="upper center", bbox_to_anchor=(0.55, 0.0), ncol=2)
    save(fig, "forest")


# ---------------------------------------------------------------- regime scan
def regime():
    names = sorted(reg["datasets"].keys(), key=lambda n: reg["datasets"][n]["p"])
    ps = [reg["datasets"][n]["p"] for n in names]
    methods = [("kNN", BLUE), ("HKNN", ORANGE), ("LPH", AQUA), ("SD", YELLOW), ("LCD", MAGENTA), ("TOD", INK)]
    fig, ax = plt.subplots(figsize=(4.6, 3.2))
    for m, col in methods:
        acc = [100 * reg["comparison"][n]["means"][m] for n in names]
        ax.plot(ps, acc, marker="o", color=col, lw=1.6 if m == "TOD" else 1.2, ms=4, label=m,
                ls="--" if m == "TOD" else "-")
    ax.set_xlabel("number of added noise coordinates $p$ (moons, noise 0.3)")
    ax.set_ylabel("accuracy (%)")
    ax.set_xticks(ps)
    ax.set_xlim(-0.5, 20.5)
    ax.grid(axis="y")
    ax.legend(fontsize=7.5, ncol=2, loc="lower left")
    save(fig, "regime")


if __name__ == "__main__":
    schematic()
    forest()
    regime()
    print("figures written to", FIG)
