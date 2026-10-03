#!/usr/bin/env python3
"""Figures for the manuscript, from results/fragility.json and results/scaling.json.
Palette: a validated brand-neutral set (ordinal blue ramp for the size of f; categorical
blue / orange / aqua for exact / greedy upper bound / certificate lower bound)."""
import json
import os

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
RES = os.path.join(ROOT, "results")
FIG = os.path.join(ROOT, "figures")
os.makedirs(FIG, exist_ok=True)
fra = json.load(open(os.path.join(RES, "fragility.json")))
sca = json.load(open(os.path.join(RES, "scaling.json")))

RAMP = ["#86b6ef", "#5598e7", "#2a78d6", "#1c5cab", "#104281", "#0d366b"]   # ordinal, steps 250..700
BLUE, ORANGE, AQUA = "#2a78d6", "#eb6834", "#1baf7a"
TEXT, MUTED, GRID = "#0b0b0b", "#52514e", "#d9d8d3"
plt.rcParams.update({"font.size": 9, "axes.edgecolor": MUTED, "axes.labelcolor": TEXT, "xtick.color": TEXT,
                     "ytick.color": TEXT, "axes.spines.top": False, "axes.spines.right": False,
                     "pdf.fonttype": 42})

def panel_distribution(ax, fam):
    """Stacked distribution of the exact signed fragility number (ANY, rule C) against n."""
    cols = []
    for a in fra["aggregates"]:
        if a["family"] != fam:
            continue
        d = a["f_any_signed_C_dist"]
        cols.append((a["n"], [d[str(k)] for k in range(1, 6)] + [d["6"] + d["7"] + d["notfound"]], a["instances"]))
    for a in sca["exact"]:
        if a["family"] != fam or a["n"] < 18:
            continue
        d = a["f_C_dist"]
        cols.append((a["n"], [d[str(k)] for k in range(1, 6)] + [d["6"] + d["notfound"]], a["instances"]))
    cols.sort()
    x = np.arange(len(cols))
    bottom = np.zeros(len(cols))
    for k in range(6):
        vals = np.array([c[1][k] / c[2] for c in cols])
        lab = f"$f={k+1}$" if k < 5 else r"$f\geq 6$ / not found"
        ax.bar(x, vals, bottom=bottom, width=0.62, color=RAMP[k], edgecolor="white", linewidth=1.2, label=lab)
        bottom += vals
    ax.set_xticks(x)
    ax.set_xticklabels([str(c[0]) for c in cols])
    ax.set_xlabel("$n$")
    ax.set_title(f"family {fam}", loc="left", fontsize=9, color=TEXT)
    ax.set_ylim(0, 1)
    ax.yaxis.grid(True, color=GRID, linewidth=0.8)
    ax.set_axisbelow(True)


def panel_bracket(ax, fam):
    """Bracket of the fragility number at large n: greedy upper bound, certificate lower bound, exact."""
    ex = [a for a in sca["exact"] if a["family"] == fam]
    n_ex = [a["n"] for a in ex]
    med_ex = [a["f_C_median"] for a in ex]
    # greedy and certificate at all n (exact records carry greedy too)
    rows = {}
    for r in sca["records_exact"] + sca["records_greedy"]:
        if r["family"] != fam:
            continue
        rows.setdefault(r["n"], {"g": [], "k": []})
        rows[r["n"]]["g"].append(r["g_onestep_C"] if r["g_onestep_C"] is not None else np.nan)
        rows[r["n"]]["k"].append(r["kstar"] + 1)
    ns = sorted(rows)
    g_med = [np.nanmedian(rows[n]["g"]) for n in ns]
    g_q1 = [np.nanpercentile(rows[n]["g"], 25) for n in ns]
    g_q3 = [np.nanpercentile(rows[n]["g"], 75) for n in ns]
    k_med = [np.median(rows[n]["k"]) for n in ns]
    ax.fill_between(ns, g_q1, g_q3, color=ORANGE, alpha=0.12, linewidth=0)
    ax.plot(ns, g_med, color=ORANGE, linewidth=2, marker="o", markersize=5, markeredgecolor="white",
            markeredgewidth=1.2, label="one-step greedy (upper bound), median and IQR")
    ax.plot(ns, k_med, color=AQUA, linewidth=2, marker="s", markersize=5, markeredgecolor="white",
            markeredgewidth=1.2, label=r"certificate $k^\ast+1$ (lower bound), median")
    ax.plot(n_ex, med_ex, color=BLUE, linewidth=2, marker="D", markersize=5, markeredgecolor="white",
            markeredgewidth=1.2, label=r"exact $f$ (search capped at $|R|\leq 6$), median")
    ax.set_xscale("log")
    ax.set_xticks([10, 20, 50, 100, 200, 400])
    ax.set_xticklabels(["10", "20", "50", "100", "200", "400"])
    ax.set_xlabel("$n$")
    ax.set_title(f"family {fam}", loc="left", fontsize=9, color=TEXT)
    ax.yaxis.grid(True, color=GRID, linewidth=0.8)
    ax.set_axisbelow(True)


# ------------------------------------------------------------------ Figure 1: distribution of f vs n
fig, axes = plt.subplots(1, 2, figsize=(7.2, 2.9), sharey=True)
for ax, fam in zip(axes, ["A", "B"]):
    panel_distribution(ax, fam)
axes[0].set_ylabel("fraction of instances")
axes[1].legend(frameon=False, fontsize=7.5, loc="upper left", bbox_to_anchor=(1.0, 1.0))
fig.tight_layout()
fig.savefig(os.path.join(FIG, "fig_fragility_distribution.pdf"))
fig.savefig(os.path.join(FIG, "fig_fragility_distribution.png"), dpi=200)
plt.close(fig)

# ------------------------------------------------------------------ Figure 2: bracket at large n
fig, axes = plt.subplots(1, 2, figsize=(7.2, 2.9), sharey=True)
for ax, fam in zip(axes, ["A", "B"]):
    panel_bracket(ax, fam)
axes[0].set_ylabel("number of removed observations")
axes[0].legend(frameon=False, fontsize=7.5, loc="upper left")
fig.tight_layout()
fig.savefig(os.path.join(FIG, "fig_bracket.pdf"))
fig.savefig(os.path.join(FIG, "fig_bracket.png"), dpi=200)
plt.close(fig)

# ------------------------------------------------------------------ Figure 3 (manuscript): both in one 2 x 2 figure
fig, axes = plt.subplots(2, 2, figsize=(7.2, 5.4))
for ax, fam in zip(axes[0], ["A", "B"]):
    panel_distribution(ax, fam)
axes[0, 1].sharey(axes[0, 0])
axes[0, 0].set_ylabel("fraction of instances")
axes[0, 1].legend(frameon=False, fontsize=7, loc="upper left", bbox_to_anchor=(1.0, 1.0))
for ax, fam in zip(axes[1], ["A", "B"]):
    panel_bracket(ax, fam)
axes[1, 1].sharey(axes[1, 0])
axes[1, 0].set_ylabel("number of removed observations")
axes[1, 0].legend(frameon=False, fontsize=7, loc="upper left")
for ax, lab in zip(axes.ravel(), "abcd"):
    ax.text(-0.12, 1.04, f"({lab})", transform=ax.transAxes, fontsize=9, fontweight="bold", color=TEXT)
fig.tight_layout()
fig.savefig(os.path.join(FIG, "fig_combined.pdf"))
fig.savefig(os.path.join(FIG, "fig_combined.png"), dpi=200)
plt.close(fig)
print("figures written")
