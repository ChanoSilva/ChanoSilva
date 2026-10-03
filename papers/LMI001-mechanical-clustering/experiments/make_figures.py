#!/usr/bin/env python3
"""Figures for LMI001 from results/*.json (no computation beyond re-plotting)."""
import json
import os
import sys

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
from scipy.spatial.distance import pdist, squareform

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import mechanical as M  # noqa: E402

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
RES = os.path.join(ROOT, "results")
FIG = os.path.join(ROOT, "figures")
os.makedirs(FIG, exist_ok=True)

# categorical palette (validated reference palette; slots 1, 2, 3, 7 for print legibility)
C = {"relax": "#2a78d6", "lloyd+relax": "#eb6834", "lloyd": "#1baf7a", "lloyd_naive": "#4a3aa7"}
LABEL = {"relax": "spring relaxation (single-particle descent)",
         "lloyd+relax": "kernel k-means: Lloyd, then single-move polish",
         "lloyd": "kernel k-means: Lloyd (canonical kernel)",
         "lloyd_naive": "Lloyd on the naively shifted kernel (control)"}
MARK = {"relax": "o", "lloyd+relax": "s", "lloyd": "D", "lloyd_naive": "^"}
POTS = ["hooke", "hooke_lift", "rest", "tension", "gauss", "log"]
POT_TEX = {"hooke": "$d^2$", "hooke_lift": "$d^2$, lifted", "rest": "$(d-r)^2$", "tension": "$d$",
           "gauss": "$1-e^{-d^2/2\\ell^2}$", "log": "$\\log(1+d^2/\\ell^2)$"}
POT_SHORT = {"hooke": "$d^2$", "hooke_lift": "lift", "rest": "rest", "tension": "$d$",
             "gauss": "sat.", "log": "log"}
FLOOR = 1e-12

plt.rcParams.update({"font.size": 8, "axes.spines.top": False, "axes.spines.right": False,
                     "axes.edgecolor": "#9a9a9a", "axes.labelcolor": "#0b0b0b", "xtick.color": "#52514e",
                     "ytick.color": "#52514e", "grid.color": "#e6e6e3", "grid.linewidth": 0.6,
                     "legend.frameon": False})


def fig_energies():
    res = json.load(open(os.path.join(RES, "results_relaxation.json")))
    cfgs = res["configs"]
    datasets = []
    for c in cfgs:
        if c["dataset"] not in datasets:
            datasets.append(c["dataset"])
    # one row of five panels plus a legend row, drawn at the final print width (6.3 in, included at
    # \linewidth), so that every font is >= 8 pt at print size (round-2 review, m6)
    fig = plt.figure(figsize=(6.3, 2.75))
    gs = fig.add_gridspec(2, len(datasets), height_ratios=[1, 0.12], hspace=0.5, wspace=0.12)
    axes = [fig.add_subplot(gs[0, 0])]
    for j in range(1, len(datasets)):
        axes.append(fig.add_subplot(gs[0, j], sharey=axes[0]))
    methods = ["relax", "lloyd+relax", "lloyd", "lloyd_naive"]
    off = np.linspace(-0.27, 0.27, len(methods))
    for ax, d in zip(axes, datasets):
        ax.set_facecolor("#fcfcfb")
        ax.grid(True, axis="y")
        ax.set_axisbelow(True)
        for j, m in enumerate(methods):
            xs, med, best = [], [], []
            for i, p in enumerate(POTS):
                c = next(c for c in cfgs if c["dataset"] == d and c["potential"] == p)
                s = c["summary"][m]
                xs.append(i + off[j])
                med.append(max(s["median_rel_excess"], FLOOR))
                best.append(max(s["best_rel_excess"], FLOOR))
            ax.scatter(xs, med, s=14, marker=MARK[m], color=C[m], linewidths=0.7, zorder=3,
                       label=LABEL[m] if d == datasets[0] else None)
            ax.scatter(xs, best, s=14, marker=MARK[m], facecolors="none", edgecolors=C[m],
                       linewidths=0.7, zorder=3)
        ax.set_yscale("log")
        ax.set_ylim(FLOOR * 0.5, 5)
        ax.set_xticks(range(len(POTS)))
        ax.set_xticklabels([POT_SHORT[p] for p in POTS], rotation=90, fontsize=8)
        ax.tick_params(axis="y", labelsize=8)
        ax.set_title(d, loc="left", fontsize=8)
        if ax is not axes[0]:
            plt.setp(ax.get_yticklabels(), visible=False)
    axes[0].set_ylabel("rel. excess over $E^*$", fontsize=8)
    axes[0].set_yticks([1e-12, 1e-9, 1e-6, 1e-3, 1])
    axes[0].set_yticklabels([r"$\leq 10^{-12}$", r"$10^{-9}$", r"$10^{-6}$", r"$10^{-3}$", "1"])
    lax = fig.add_subplot(gs[1, :])
    lax.axis("off")
    handles, labels = axes[0].get_legend_handles_labels()
    short = {"relax": "spring relaxation (single-particle descent)", "lloyd+relax": "Lloyd, then single-move polish",
             "lloyd": "Lloyd (canonical kernel)", "lloyd_naive": "Lloyd, naively shifted kernel (control)"}
    lax.legend(handles, [short[m] for m in methods], loc="upper center", ncol=2, fontsize=8, handletextpad=0.3,
               columnspacing=1.5, borderaxespad=0.0)
    fig.subplots_adjust(left=0.135, right=0.995, top=0.93, bottom=0.02)
    for ext in ("png", "pdf"):
        fig.savefig(os.path.join(FIG, f"energies.{ext}"), dpi=200, bbox_inches="tight", pad_inches=0.02)
    plt.close(fig)


def fig_partitions():
    res = json.load(open(os.path.join(RES, "results_relaxation.json")))
    cfgs = res["configs"]
    n_syn = res["configs"][0]["n"]
    datasets = M.load_datasets(M.MASTER_SEED, n_synthetic=n_syn, n_digits=n_syn)
    show = ["blobs", "moons", "circles"]
    pots = ["hooke", "gauss"]
    cols = ["#2a78d6", "#eb6834", "#1baf7a"]
    fig, axes = plt.subplots(len(pots), len(show), figsize=(8.2, 5.2))
    for r, p in enumerate(pots):
        for cidx, d in enumerate(show):
            ax = axes[r, cidx]
            X = datasets[d][0]
            c = next(c for c in cfgs if c["dataset"] == d and c["potential"] == p)
            lab = np.array(c["best_labels"]["relax"])
            for kk in np.unique(lab):
                ax.scatter(X[lab == kk, 0], X[lab == kk, 1], s=9, color=cols[kk % 3], linewidths=0,
                           alpha=0.9)
            ax.set_aspect("equal")
            ax.set_xticks([])
            ax.set_yticks([])
            for sp in ax.spines.values():
                sp.set_visible(False)
            ax.set_title(f"{d}, springs {POT_TEX[p]}:  $E^*$ = {c['E_best']:.4g}", loc="left", fontsize=8)
    fig.suptitle("Best partitions found by spring relaxation; each equals a kernel k-means optimum of the same value",
                 fontsize=9, x=0.02, ha="left")
    fig.tight_layout(rect=(0, 0, 1, 0.95))
    for ext in ("png", "pdf"):
        fig.savefig(os.path.join(FIG, f"partitions.{ext}"), dpi=200)
    plt.close(fig)


if __name__ == "__main__":
    fig_energies()
    fig_partitions()
    print("wrote figures/energies.* and figures/partitions.*")
