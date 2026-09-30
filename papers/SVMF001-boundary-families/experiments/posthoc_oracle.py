#!/usr/bin/env python3
"""POST-HOC sensitivity check (defined AFTER seeing the main results; not part of the
predefined criterion).  Recomputes the paired differences of each local family against
the ORACLE best global reference, i.e. max(linear, RBF) test accuracy in each outer fold
(a reference that uses test data and is therefore optimistic for the references), and
against each fixed global reference.  Reads results/results.json only; no refit."""
import json
import os

import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
res = json.load(open(os.path.join(ROOT, "results", "results.json")))
LOCAL = res["meta"]["local"]
SEED = res["meta"]["seed"]


def ci(diffs, rng, B=2000):
    d = np.asarray(diffs)
    m = np.array([rng.choice(d, size=len(d), replace=True).mean() for _ in range(B)])
    return float(np.percentile(m, 2.5)), float(np.percentile(m, 97.5))


out = {"note": __doc__.strip(), "conditions": {}}
for cname in res["meta"]["conditions"]:
    out["conditions"][cname] = {}
    for d, r in res["results"].items():
        folds = r[cname]["folds"]
        row = {}
        for ref in ["oracle", "linear", "rbf"]:
            if ref == "oracle":
                refacc = np.array([max(f["linear"]["acc"], f["rbf"]["acc"]) for f in folds])
            else:
                refacc = np.array([f[ref]["acc"] for f in folds])
            for m in LOCAL:
                diffs = np.array([f[m]["acc"] for f in folds]) - refacc
                rng = np.random.default_rng([SEED, 4242, sum(map(ord, cname)), sum(map(ord, d)), sum(map(ord, m)), sum(map(ord, ref))])
                lo, hi = ci(diffs, rng)
                row[f"{m}_vs_{ref}"] = {"diff_mean": float(diffs.mean()), "diff_ci": [lo, hi],
                                       "sig": "pos" if lo > 0 else ("neg" if hi < 0 else "none")}
        row["oracle_mean_acc"] = float(np.mean([max(f["linear"]["acc"], f["rbf"]["acc"]) for f in folds]))
        out["conditions"][cname][d] = row

with open(os.path.join(ROOT, "results", "posthoc_oracle.json"), "w") as fh:
    json.dump(out, fh, indent=1)
L = ["# POST-HOC: paired differences against the oracle best global reference (max(linear, RBF) per fold)\n",
     "Defined after seeing the main results; a sensitivity check, not the predefined criterion.\n"]
for cname, rows in out["conditions"].items():
    L.append(f"\n## `{cname}`\n\n| dataset | oracle acc | " + " | ".join(LOCAL) + " |\n|---|---|" + "---|" * len(LOCAL))
    for d, row in rows.items():
        L.append(f"| {d} | {row['oracle_mean_acc']:.3f} | " + " | ".join(
            f"{100*row[m+'_vs_oracle']['diff_mean']:+.2f} [{100*row[m+'_vs_oracle']['diff_ci'][0]:+.2f}, {100*row[m+'_vs_oracle']['diff_ci'][1]:+.2f}] {row[m+'_vs_oracle']['sig']}" for m in LOCAL) + " |")
with open(os.path.join(ROOT, "results", "posthoc_oracle.md"), "w") as fh:
    fh.write("\n".join(L) + "\n")
print("\n".join(L))
