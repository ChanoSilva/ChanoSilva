#!/usr/bin/env python3
"""SVMF001 -- controlled comparison of locally adaptive boundary families against
matched global references, with a predefined criterion for 'added value'.

Protocol (fixed before running):
  * binary tasks, features standardised on the training fold (digits: PCA(16) then
    standardisation, fitted on the training fold);
  * main condition: 2 x stratified 5-fold CV (10 outer folds);
    robustness conditions: 1 x 5-fold CV with (noise20) 20% of the TRAINING labels
    flipped, test labels clean, and (sub25) only 25% of the training fold used;
  * every family is tuned by an inner stratified 3-fold CV on the training fold,
    accuracy as the score, ties broken towards the global special case;
  * reference = 'best global' = the global reference (linear or RBF) with the higher
    inner-CV score in that fold (no test data used in the choice);
  * paired differences (family - best global) per outer fold; percentile bootstrap
    95% CI of their mean over folds (B = 2000);
  * predefined criterion of added value for a family: mean paired improvement > 0
    with CI excluding 0 on a MAJORITY of datasets in the main condition; failing
    that, a NAMED regime (dataset group) in which this holds on every dataset of the
    group and no dataset outside the group shows a CI entirely below 0.
Everything is seeded; run with --fast for a reduced smoke test.
"""
import argparse
import json
import os
import platform
import sys
import time

for _v in ("OMP_NUM_THREADS", "OPENBLAS_NUM_THREADS", "MKL_NUM_THREADS"):
    os.environ.setdefault(_v, "1")

import numpy as np
import sklearn
from sklearn.datasets import load_breast_cancer, load_digits, load_wine, make_moons
from sklearn.decomposition import PCA
from sklearn.model_selection import StratifiedKFold
from sklearn.preprocessing import StandardScaler

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import families as F  # noqa: E402

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
SEED = 20260930

# ----------------------------------------------------------------------------
# datasets (all binary, labels in {-1,+1}); subsampling sizes are part of the design

def stratified_subsample(X, y, n, rng):
    if n >= len(y):
        return X, y
    idx = []
    for c in np.unique(y):
        ic = np.flatnonzero(y == c)
        m = int(round(n * len(ic) / len(y)))
        idx.append(rng.choice(ic, size=m, replace=False))
    idx = np.concatenate(idx)
    return X[idx], y[idx]


def ds_wine(rng):
    d = load_wine()
    return d.data, np.where(d.target == 0, 1, -1)


def ds_breast_cancer(rng):
    d = load_breast_cancer()
    return stratified_subsample(d.data, np.where(d.target == 1, 1, -1), 300, rng)


def ds_digits_parity(rng):
    d = load_digits()
    return stratified_subsample(d.data, np.where(d.target % 2 == 0, 1, -1), 400, rng)


def ds_gauss_linear(rng, n=400, d=10, delta=3.29):
    y = rng.choice([-1, 1], size=n)
    X = rng.normal(size=(n, d))
    X[:, 0] += y * delta / 2
    return X, y


def ds_moons_2scale(rng, n_big=100, n_small=300, scale_small=0.25, noise=0.15):
    Xb, yb = make_moons(n_samples=n_big, noise=noise, random_state=int(rng.integers(1 << 31)))
    Xs, ys = make_moons(n_samples=n_small, noise=noise, random_state=int(rng.integers(1 << 31)))
    Xs = Xs * scale_small + np.array([3.5, 0.0])
    X = np.vstack([Xb, Xs])
    y = np.where(np.concatenate([yb, ys]) == 1, 1, -1)
    return X, y


def ds_checker_2scale(rng, n_big=100, n_small=300, side_big=1.0, side_small=0.5):
    Xb = np.column_stack([rng.uniform(-2, 0, n_big), rng.uniform(-1, 1, n_big)])
    Xs = np.column_stack([rng.uniform(0, 2, n_small), rng.uniform(-1, 1, n_small)])
    lb = (np.floor(Xb[:, 0] / side_big) + np.floor(Xb[:, 1] / side_big)) % 2
    ls = (np.floor(Xs[:, 0] / side_small) + np.floor(Xs[:, 1] / side_small)) % 2
    X = np.vstack([Xb, Xs])
    y = np.where(np.concatenate([lb, ls]) == 0, 1, -1)
    return X, y


DATASETS = {
    # name: (loader, regime, needs_pca)
    "wine": (ds_wine, "real", False),
    "breast_cancer": (ds_breast_cancer, "real", False),
    "digits_parity": (ds_digits_parity, "real", True),
    "gauss_linear": (ds_gauss_linear, "linear", False),
    "moons_2scale": (ds_moons_2scale, "multiscale", False),
    "checker_2scale": (ds_checker_2scale, "multiscale", False),
}
REGIMES = {"real": ["wine", "breast_cancer", "digits_parity"],
           "linear": ["gauss_linear"],
           "multiscale": ["moons_2scale", "checker_2scale"]}

METHODS = ["linear", "rbf", "best_global", "knn_svm", "cell_svm", "vb_rbf", "llsvm"]
LOCAL = ["knn_svm", "cell_svm", "vb_rbf", "llsvm"]

GRID = {
    "C_lin": [0.01, 0.1, 1.0, 10.0],
    "C_rbf": [0.1, 1.0, 10.0],
    "gamma_mults": [0.1, 0.3, 1.0, 3.0, 10.0],
    "knn_ks": [20, 50, 100],
    "knn_C": 1.0,
    "knn_val_cap": 40,
    "cell_Ms": [1, 2, 4, 8],
    "cell_Cs": [0.1, 1.0, 10.0],
    "vb_betas": [0.0, 0.5, 1.0],
    "vb_kbw": 10,
    "llsvm_Ms": [1, 2, 4, 8],
    "llsvm_Cs": [0.01, 0.1, 1.0, 10.0],
    "inner_folds": 3,
}

CONDITIONS = {
    "main": {"repeats": 2, "folds": 5, "noise": 0.0, "frac": 1.0},
    "noise20": {"repeats": 1, "folds": 5, "noise": 0.2, "frac": 1.0},
    "sub25": {"repeats": 1, "folds": 5, "noise": 0.0, "frac": 0.25},
}


# ----------------------------------------------------------------------------

def preprocess(Xtr, Xte, needs_pca, seed):
    if needs_pca:
        pca = PCA(n_components=16, random_state=seed).fit(Xtr)
        Xtr, Xte = pca.transform(Xtr), pca.transform(Xte)
    sc = StandardScaler().fit(Xtr)
    return sc.transform(Xtr), sc.transform(Xte)


def apply_condition(Xtr, ytr, cond, rng):
    if cond["frac"] < 1.0:
        n_keep = max(40, int(round(cond["frac"] * len(ytr))))
        Xtr, ytr = stratified_subsample(Xtr, ytr, n_keep, rng)
    if cond["noise"] > 0:
        ytr = ytr.copy()
        flip = rng.random(len(ytr)) < cond["noise"]
        ytr[flip] = -ytr[flip]
    return Xtr, ytr


def run_fold(Xtr, ytr, Xte, yte, seed, grid):
    folds = F.inner_folds(ytr, grid["inner_folds"], seed)
    out = {}
    ks = [k for k in grid["knn_ks"] if k < min(len(tr) for tr, _ in folds)]

    cfg, sc, m = F.tune_linear(Xtr, ytr, folds, grid["C_lin"])
    out["linear"] = {"acc": float(np.mean(m.predict(Xte) == yte)), "inner": sc, "cfg": cfg}
    cfg, sc, m, rbf_scores = F.tune_rbf(Xtr, ytr, folds, grid["C_rbf"], grid["gamma_mults"])
    out["rbf"] = {"acc": float(np.mean(m.predict(Xte) == yte)), "inner": sc, "cfg": cfg}
    pick = "rbf" if out["rbf"]["inner"] > out["linear"]["inner"] else "linear"
    out["best_global"] = {"acc": out[pick]["acc"], "inner": out[pick]["inner"], "cfg": {"pick": pick}}

    cfg, sc = F.tune_knn_svm(Xtr, ytr, folds, ks, grid["knn_C"], grid["knn_val_cap"], seed)
    pred = F.knn_svm_predict_multi(Xtr, ytr, Xte, [cfg["k"]], cfg["C"])[cfg["k"]]
    out["knn_svm"] = {"acc": float(np.mean(pred == yte)), "inner": sc, "cfg": cfg}

    cfg, sc, m = F.tune_cell_svm(Xtr, ytr, folds, grid["cell_Ms"], grid["cell_Cs"], seed)
    out["cell_svm"] = {"acc": float(np.mean(m.predict(Xte) == yte)), "inner": sc, "cfg": cfg}

    cfg, sc, m = F.tune_vbrbf(Xtr, ytr, folds, grid["C_rbf"], grid["gamma_mults"], grid["vb_betas"], grid["vb_kbw"], rbf_scores)
    out["vb_rbf"] = {"acc": float(np.mean(m.predict(Xte) == yte)), "inner": sc, "cfg": cfg}

    cfg, sc, m = F.tune_llsvm(Xtr, ytr, folds, grid["llsvm_Ms"], grid["llsvm_Cs"], seed)
    out["llsvm"] = {"acc": float(np.mean(m.predict(Xte) == yte)), "inner": sc, "cfg": cfg}
    return out


def bootstrap_ci(diffs, B, rng):
    diffs = np.asarray(diffs)
    means = np.array([rng.choice(diffs, size=len(diffs), replace=True).mean() for _ in range(B)])
    return float(np.percentile(means, 2.5)), float(np.percentile(means, 97.5))


def summarise(fold_records, rng, B=2000):
    """fold_records: list of dicts method -> {acc,...} for one (dataset, condition)."""
    summ = {}
    for meth in METHODS:
        accs = np.array([r[meth]["acc"] for r in fold_records])
        summ[meth] = {"mean_acc": float(accs.mean()), "sd_acc": float(accs.std(ddof=1)) if len(accs) > 1 else 0.0,
                      "accs": accs.tolist()}
        if meth in LOCAL:
            diffs = np.array([r[meth]["acc"] - r["best_global"]["acc"] for r in fold_records])
            lo, hi = bootstrap_ci(diffs, B, rng)
            summ[meth].update({"diff_mean": float(diffs.mean()), "diff_ci": [lo, hi],
                               "diffs": diffs.tolist(), "wins": int((diffs > 0).sum()),
                               "losses": int((diffs < 0).sum()),
                               "sig": "pos" if lo > 0 else ("neg" if hi < 0 else "none")})
    summ["best_global"]["pick_rbf_frac"] = float(np.mean([r["best_global"]["cfg"]["pick"] == "rbf" for r in fold_records]))
    # how often did inner CV choose a genuinely local configuration?
    summ["knn_svm"]["local_frac"] = float(np.mean([r["knn_svm"]["cfg"]["k"] != "all" for r in fold_records]))
    summ["cell_svm"]["local_frac"] = float(np.mean([r["cell_svm"]["cfg"]["M"] > 1 for r in fold_records]))
    summ["vb_rbf"]["local_frac"] = float(np.mean([r["vb_rbf"]["cfg"]["beta"] > 0 for r in fold_records]))
    summ["llsvm"]["local_frac"] = float(np.mean([r["llsvm"]["cfg"]["M"] > 1 for r in fold_records]))
    return summ


def evaluate_criterion(results_main):
    names = list(results_main.keys())
    verdict = {}
    for meth in LOCAL:
        sig = {n: results_main[n][meth]["sig"] for n in names}
        n_pos = sum(s == "pos" for s in sig.values())
        n_neg = sum(s == "neg" for s in sig.values())
        majority = n_pos > len(names) / 2
        regimes = []
        for reg, members in REGIMES.items():
            members = [n for n in members if n in names]
            if not members:
                continue
            in_pos = all(sig[n] == "pos" for n in members)
            out_neg = any(sig[n] == "neg" for n in names if n not in members)
            if in_pos and not out_neg:
                regimes.append(reg)
        verdict[meth] = {"n_datasets": len(names), "n_ci_positive": n_pos, "n_ci_negative": n_neg,
                         "majority_criterion": bool(majority), "named_regimes": regimes,
                         "added_value": bool(majority or regimes), "sig": sig}
    return verdict


# ----------------------------------------------------------------------------

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--fast", action="store_true")
    ap.add_argument("--datasets", nargs="*", default=None)
    args = ap.parse_args()
    t0 = time.time()
    grid = dict(GRID)
    conds = {k: dict(v) for k, v in CONDITIONS.items()}
    if args.fast:
        conds = {"main": {"repeats": 1, "folds": 3, "noise": 0.0, "frac": 1.0}}
        grid["gamma_mults"] = [0.3, 1.0, 3.0]
        grid["C_rbf"] = [1.0, 10.0]
        grid["C_lin"] = [0.1, 1.0]
    names = args.datasets or list(DATASETS.keys())

    records, timing = {}, {}
    for dname in names:
        loader, regime, needs_pca = DATASETS[dname]
        rng = np.random.default_rng([SEED, sum(map(ord, dname))])
        X, y = loader(rng)
        X, y = np.asarray(X, float), np.asarray(y, int)
        records[dname] = {"n": int(len(y)), "d": int(X.shape[1]), "regime": regime,
                          "pos_frac": float(np.mean(y == 1)), "conditions": {}}
        td = time.time()
        for cname, cond in conds.items():
            fold_recs = []
            for rep in range(cond["repeats"]):
                fseed = SEED + 100 * rep + 7 * sum(map(ord, cname))
                skf = StratifiedKFold(n_splits=cond["folds"], shuffle=True, random_state=fseed)
                for fi, (tr, te) in enumerate(skf.split(X, y)):
                    Xtr, Xte = preprocess(X[tr], X[te], needs_pca, fseed + fi)
                    ytr, yte = y[tr], y[te]
                    crng = np.random.default_rng([SEED, rep, fi, sum(map(ord, cname)), sum(map(ord, dname))])
                    Xtr, ytr = apply_condition(Xtr, ytr, cond, crng)
                    rec = run_fold(Xtr, ytr, Xte, yte, fseed + fi, grid)
                    rec["n_train"] = int(len(ytr))
                    fold_recs.append(rec)
            srng = np.random.default_rng([SEED, 999, sum(map(ord, cname)), sum(map(ord, dname))])
            records[dname]["conditions"][cname] = {"summary": summarise(fold_recs, srng),
                                                   "folds": fold_recs, "n_train": fold_recs[0]["n_train"]}
        timing[dname] = time.time() - td
        print(f"{dname}: {timing[dname]:.1f}s", flush=True)

    main_summ = {d: records[d]["conditions"]["main"]["summary"] for d in names}
    criterion = evaluate_criterion(main_summ)

    # robustness: accuracy drop (main -> condition) per method, and paired diffs there
    robustness = {}
    for cname in conds:
        if cname == "main":
            continue
        robustness[cname] = {}
        for d in names:
            s_main, s_c = records[d]["conditions"]["main"]["summary"], records[d]["conditions"][cname]["summary"]
            robustness[cname][d] = {m: {"acc": s_c[m]["mean_acc"], "drop": s_main[m]["mean_acc"] - s_c[m]["mean_acc"],
                                        **({"diff_mean": s_c[m]["diff_mean"], "diff_ci": s_c[m]["diff_ci"], "sig": s_c[m]["sig"]} if m in LOCAL else {})}
                                    for m in METHODS}

    seconds = time.time() - t0
    out = {"meta": {"seed": SEED, "fast": args.fast, "seconds": seconds, "timing": timing,
                    "python": platform.python_version(), "numpy": np.__version__, "sklearn": sklearn.__version__,
                    "grid": grid, "conditions": conds, "methods": METHODS, "local": LOCAL, "regimes": REGIMES},
           "datasets": {d: {k: v for k, v in records[d].items() if k != "conditions"} for d in names},
           "results": {d: {c: {"summary": records[d]["conditions"][c]["summary"],
                               "n_train": records[d]["conditions"][c]["n_train"],
                               "folds": [{m: {"acc": r[m]["acc"], "cfg": r[m]["cfg"], "inner": r[m]["inner"]} for m in METHODS}
                                         for r in records[d]["conditions"][c]["folds"]]}
                           for c in conds} for d in names},
           "criterion": criterion, "robustness": robustness}
    os.makedirs(os.path.join(ROOT, "results"), exist_ok=True)
    fn = "results_fast.json" if args.fast else "results.json"
    with open(os.path.join(ROOT, "results", fn), "w") as fh:
        json.dump(out, fh, indent=1)
    write_markdown(out, os.path.join(ROOT, "results", "tables_fast.md" if args.fast else "tables.md"))
    if not args.fast:
        make_figures(out, records, names)
    print(f"total {seconds:.1f}s -> results/{fn}")


def write_markdown(out, path):
    L = ["# SVMF001 -- results (seed %d)\n" % out["meta"]["seed"]]
    for cname in out["meta"]["conditions"]:
        L.append(f"\n## Condition `{cname}`: mean accuracy per fold set\n")
        L.append("| dataset | n_train | " + " | ".join(METHODS) + " |")
        L.append("|---|---|" + "---|" * len(METHODS))
        for d, r in out["results"].items():
            s = r[cname]["summary"]
            L.append(f"| {d} | {r[cname]['n_train']} | " + " | ".join(f"{s[m]['mean_acc']:.3f}" for m in METHODS) + " |")
        L.append(f"\n### Paired difference vs best global (mean [95% bootstrap CI]), `{cname}`\n")
        L.append("| dataset | " + " | ".join(LOCAL) + " |")
        L.append("|---|" + "---|" * len(LOCAL))
        for d, r in out["results"].items():
            s = r[cname]["summary"]
            L.append(f"| {d} | " + " | ".join(f"{100*s[m]['diff_mean']:+.2f} [{100*s[m]['diff_ci'][0]:+.2f}, {100*s[m]['diff_ci'][1]:+.2f}] {s[m]['sig']}" for m in LOCAL) + " |")
        L.append(f"\n### Fraction of folds in which inner CV selected a local configuration, `{cname}`\n")
        L.append("| dataset | best_global picks RBF | " + " | ".join(LOCAL) + " |")
        L.append("|---|---|" + "---|" * len(LOCAL))
        for d, r in out["results"].items():
            s = r[cname]["summary"]
            L.append(f"| {d} | {s['best_global']['pick_rbf_frac']:.2f} | " + " | ".join(f"{s[m]['local_frac']:.2f}" for m in LOCAL) + " |")
    L.append("\n## Predefined criterion (main condition)\n")
    for m, v in out["criterion"].items():
        L.append(f"- **{m}**: CI>0 on {v['n_ci_positive']}/{v['n_datasets']} datasets, CI<0 on {v['n_ci_negative']}; "
                 f"majority criterion {'met' if v['majority_criterion'] else 'not met'}; named regimes {v['named_regimes'] or 'none'}; "
                 f"added value: **{'yes' if v['added_value'] else 'no'}**")
    with open(path, "w") as fh:
        fh.write("\n".join(L) + "\n")


def make_figures(out, records, names):
    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt
    figdir = os.path.join(ROOT, "figures")
    os.makedirs(figdir, exist_ok=True)
    conds = list(out["meta"]["conditions"].keys())
    fig, axes = plt.subplots(1, len(conds), figsize=(4.2 * len(conds), 3.6), sharey=True)
    axes = np.atleast_1d(axes)
    colors = {"knn_svm": "#1b6ca8", "cell_svm": "#7a4fa3", "vb_rbf": "#c0392b", "llsvm": "#2e8b57"}
    for ax, cname in zip(axes, conds):
        for j, d in enumerate(names):
            s = out["results"][d][cname]["summary"]
            for i, m in enumerate(LOCAL):
                y = j + (i - 1.5) * 0.18
                lo, hi = s[m]["diff_ci"]
                ax.plot([100 * lo, 100 * hi], [y, y], color=colors[m], lw=1.4)
                ax.plot(100 * s[m]["diff_mean"], y, "o", color=colors[m], ms=4, label=m if j == 0 else None)
        ax.axvline(0, color="k", lw=0.8)
        ax.set_yticks(range(len(names)))
        ax.set_yticklabels(names)
        ax.set_title(cname)
        ax.set_xlabel("accuracy difference vs best global (pp)")
        ax.invert_yaxis()
    axes[0].legend(fontsize=8, loc="lower left")
    fig.tight_layout()
    fig.savefig(os.path.join(figdir, "fig_paired.png"), dpi=160)
    fig.savefig(os.path.join(figdir, "fig_paired.pdf"))
    plt.close(fig)

    # the decision-region figure is produced by make_region_figure.py from results.json


if __name__ == "__main__":
    main()
