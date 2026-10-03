#!/usr/bin/env python3
"""Decision regions on the two 2-D multiscale sets (figure only).  Refits, on the
first outer training fold of the main condition, the configuration that the inner CV
selected there (read from results/results.json); it does not change any number."""
import json
import os
import sys

for _v in ("OMP_NUM_THREADS", "OPENBLAS_NUM_THREADS", "MKL_NUM_THREADS"):
    os.environ.setdefault(_v, "1")
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
from sklearn.model_selection import StratifiedKFold

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import families as F  # noqa: E402
import run_comparison as R  # noqa: E402

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
res = json.load(open(os.path.join(ROOT, "results", "results.json")))
SEED = res["meta"]["seed"]

fig, axes = plt.subplots(2, 4, figsize=(7.5, 4.0))
for row, d in enumerate(["moons_2scale", "checker_2scale"]):
    loader, _, _ = R.DATASETS[d]
    rng = np.random.default_rng([SEED, sum(map(ord, d))])
    X, y = loader(rng)
    skf = StratifiedKFold(n_splits=5, shuffle=True, random_state=SEED + 7 * sum(map(ord, "main")))
    tr, te = next(iter(skf.split(X, y)))
    Xtr, Xte = R.preprocess(X[tr], X[te], False, SEED)
    ytr = y[tr]
    f0 = res["results"][d]["main"]["folds"][0]
    xx, yy = np.meshgrid(np.linspace(Xtr[:, 0].min() - .3, Xtr[:, 0].max() + .3, 220),
                         np.linspace(Xtr[:, 1].min() - .3, Xtr[:, 1].max() + .3, 160))
    G = np.column_stack([xx.ravel(), yy.ravel()])
    c = {m: f0[m]["cfg"] for m in f0}
    models = {
        "RBF-SVM": (F.SVC(kernel="rbf", C=c["rbf"]["C"], gamma=c["rbf"]["gamma"]).fit(Xtr, ytr).predict,
                    f"$C$={c['rbf']['C']:g}, $\\gamma$={c['rbf']['gamma']:.2f}"),
        "kNN-SVM": (lambda Z: F.knn_svm_predict_multi(Xtr, ytr, Z, [c["knn_svm"]["k"]], c["knn_svm"]["C"])[c["knn_svm"]["k"]],
                    f"$k$={c['knn_svm']['k']}, $C$={c['knn_svm']['C']:g}"),
        "VB-RBF-SVM": (F.VBRBF(c["vb_rbf"]["gamma"], c["vb_rbf"]["beta"], c["vb_rbf"]["C"], res["meta"]["grid"]["vb_kbw"]).fit(Xtr, ytr).predict,
                       f"$\\beta$={c['vb_rbf']['beta']:g}, $C$={c['vb_rbf']['C']:g}, $\\gamma$={c['vb_rbf']['gamma']:.2f}"),
        "LLSVM": (F.LLSVM(c["llsvm"]["M"], c["llsvm"]["C"], SEED).fit(Xtr, ytr).predict,
                  f"$M$={c['llsvm']['M']}, $C$={c['llsvm']['C']:g}"),
    }
    for col, (mname, (pred, lab)) in enumerate(models.items()):
        ax = axes[row, col]
        Z = pred(G).reshape(xx.shape)
        ax.contourf(xx, yy, Z, levels=[-2, 0, 2], colors=["#f4d6d6", "#d6e4f4"], alpha=0.9)
        ax.scatter(Xtr[:, 0], Xtr[:, 1], c=np.where(ytr == 1, "#1b6ca8", "#c0392b"), s=4)
        ax.set_title(f"{mname}\n{lab}", fontsize=8)
        ax.set_xticks([]); ax.set_yticks([])
        if col == 0:
            ax.set_ylabel(R.PRETTY[d], fontsize=9)
fig.tight_layout()
fig.savefig(os.path.join(ROOT, "figures", "fig_regions.png"), dpi=150)
fig.savefig(os.path.join(ROOT, "figures", "fig_regions.pdf"))
print("wrote figures/fig_regions.{png,pdf}")
