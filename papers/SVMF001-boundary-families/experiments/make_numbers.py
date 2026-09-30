#!/usr/bin/env python3
"""Turn results/*.json into LaTeX macros (manuscript/numbers.tex) and table bodies
(manuscript/table_*.tex).  No number in main.tex is typed by hand."""
import json
import os

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
OUT = os.path.join(ROOT, "manuscript")
res = json.load(open(os.path.join(ROOT, "results", "results.json")))
ex = json.load(open(os.path.join(ROOT, "results", "exact_example.json")))
post = json.load(open(os.path.join(ROOT, "results", "posthoc_oracle.json")))

METHODS = res["meta"]["methods"]
LOCAL = res["meta"]["local"]
NAMES = list(res["results"].keys())
TAG = {"knn_svm": "Knn", "cell_svm": "Cell", "vb_rbf": "Vb", "llsvm": "Llsvm", "linear": "Lin", "rbf": "Rbf", "best_global": "Best"}
DTAG = {"wine": "Wine", "breast_cancer": "Bc", "digits_parity": "Dig", "gauss_linear": "Gauss", "moons_2scale": "Moons", "checker_2scale": "Check"}
CTAG = {"main": "Main", "noise20": "Noise", "sub25": "Sub"}
PRETTY = {"wine": "wine", "breast_cancer": "breast cancer", "digits_parity": "digits (parity)", "gauss_linear": "Gaussian, linear",
          "moons_2scale": "two-scale moons", "checker_2scale": "two-scale checkerboard"}
MPRETTY = {"linear": "linear SVM", "rbf": "RBF-SVM", "best_global": "best global (inner CV)", "knn_svm": "kNN-SVM",
           "cell_svm": "cell-SVM", "vb_rbf": "VB-RBF-SVM", "llsvm": "LLSVM"}

L = []


def mac(name, val):
    L.append(rf"\newcommand{{\{name}}}{{{val}}}")


def pp(x, sign=True):
    return f"{100*x:+.2f}" if sign else f"{100*x:.2f}"


def cell_diff(d):
    lo, hi = d["diff_ci"]
    mark = {"pos": r"$^{+}$", "neg": r"$^{-}$", "none": ""}[d["sig"]]
    return f"{pp(d['diff_mean'])} [{pp(lo)}, {pp(hi)}]{mark}"


m = res["meta"]
mac("MetaSeed", m["seed"])
mac("MetaPython", m["python"])
mac("MetaNumpy", m["numpy"])
mac("MetaSklearn", m["sklearn"])
mac("MetaScipy", ex["meta"]["scipy"])
mac("MetaSecondsMain", int(round(m["seconds"])))
mac("MetaSecondsExact", int(round(ex["meta"]["seconds"])))
mac("MetaSecondsTotal", int(round(m["seconds"] + ex["meta"]["seconds"])))
mac("NDatasets", len(NAMES))
mac("NMainFolds", m["conditions"]["main"]["repeats"] * m["conditions"]["main"]["folds"])
mac("NMainRepeats", m["conditions"]["main"]["repeats"])
mac("NRobFolds", m["conditions"]["noise20"]["folds"])
mac("NoiseRate", int(round(100 * m["conditions"]["noise20"]["noise"])))
mac("SubFrac", int(round(100 * m["conditions"]["sub25"]["frac"])))
mac("InnerFolds", m["grid"]["inner_folds"])
mac("KnnValCap", m["grid"]["knn_val_cap"])
mac("KnnKs", ", ".join(str(k) for k in m["grid"]["knn_ks"]))
mac("KnnC", m["grid"]["knn_C"])
mac("VbKbw", m["grid"]["vb_kbw"])
mac("VbBetas", ", ".join(str(b) for b in m["grid"]["vb_betas"]))
mac("GammaMults", ", ".join(str(g) for g in m["grid"]["gamma_mults"]))
mac("CRbf", ", ".join(str(c) for c in m["grid"]["C_rbf"]))
mac("CLin", ", ".join(str(c) for c in m["grid"]["C_lin"]))
mac("CellMs", ", ".join(str(c) for c in m["grid"]["cell_Ms"]))
mac("CellCs", ", ".join(str(c) for c in m["grid"]["cell_Cs"]))
mac("LlsvmMs", ", ".join(str(c) for c in m["grid"]["llsvm_Ms"]))
mac("LlsvmCs", ", ".join(str(c) for c in m["grid"]["llsvm_Cs"]))

# datasets table
with open(os.path.join(OUT, "table_datasets.tex"), "w") as fh:
    for d in NAMES:
        info = res["datasets"][d]
        fh.write(f"{PRETTY[d]} & {info['regime']} & {info['n']} & {info['d']} & {res['results'][d]['main']['n_train']} & "
                 f"{res['results'][d]['sub25']['n_train']} & {100*info['pos_frac']:.0f}\\% \\\\\n")
    mac_d = None
for d in NAMES:
    mac(f"N{DTAG[d]}", res["datasets"][d]["n"])
    mac(f"D{DTAG[d]}", res["datasets"][d]["d"])

# accuracy tables and paired-difference tables per condition
for c in m["conditions"]:
    with open(os.path.join(OUT, f"table_acc_{c}.tex"), "w") as fh:
        for d in NAMES:
            s = res["results"][d][c]["summary"]
            fh.write(f"{PRETTY[d]} & " + " & ".join(f"{100*s[mm]['mean_acc']:.1f}" for mm in METHODS) + " \\\\\n")
    with open(os.path.join(OUT, f"table_diff_{c}.tex"), "w") as fh:
        for d in NAMES:
            s = res["results"][d][c]["summary"]
            fh.write(f"{PRETTY[d]} & " + " & ".join(cell_diff(s[mm]) for mm in LOCAL) + " \\\\\n")
    with open(os.path.join(OUT, f"table_localfrac_{c}.tex"), "w") as fh:
        for d in NAMES:
            s = res["results"][d][c]["summary"]
            fh.write(f"{PRETTY[d]} & {s['best_global']['pick_rbf_frac']:.1f} & " + " & ".join(f"{s[mm]['local_frac']:.1f}" for mm in LOCAL) + " \\\\\n")
    for d in NAMES:
        s = res["results"][d][c]["summary"]
        for mm in METHODS:
            mac(f"Acc{CTAG[c]}{DTAG[d]}{TAG[mm]}", f"{100*s[mm]['mean_acc']:.1f}")
        for mm in LOCAL:
            mac(f"Diff{CTAG[c]}{DTAG[d]}{TAG[mm]}", pp(s[mm]["diff_mean"]))
            mac(f"DiffLo{CTAG[c]}{DTAG[d]}{TAG[mm]}", pp(s[mm]["diff_ci"][0]))
            mac(f"DiffHi{CTAG[c]}{DTAG[d]}{TAG[mm]}", pp(s[mm]["diff_ci"][1]))
            mac(f"LocalFrac{CTAG[c]}{DTAG[d]}{TAG[mm]}", f"{100*s[mm]['local_frac']:.0f}")
        mac(f"PickRbf{CTAG[c]}{DTAG[d]}", f"{100*s['best_global']['pick_rbf_frac']:.0f}")

# counts of significant results per family and condition
for c in m["conditions"]:
    for mm in LOCAL:
        sig = [res["results"][d][c]["summary"][mm]["sig"] for d in NAMES]
        mac(f"NPos{CTAG[c]}{TAG[mm]}", sum(s == "pos" for s in sig))
        mac(f"NNeg{CTAG[c]}{TAG[mm]}", sum(s == "neg" for s in sig))
        mac(f"NNone{CTAG[c]}{TAG[mm]}", sum(s == "none" for s in sig))
# the single 'pos' cell(s) in the main condition
pos_cells = [(d, mm) for d in NAMES for mm in LOCAL if res["results"][d]["main"]["summary"][mm]["sig"] == "pos"]
mac("NPosCellsMain", len(pos_cells))
mac("PosCellsMain", "; ".join(f"{MPRETTY[mm]} on {PRETTY[d]}" for d, mm in pos_cells) if pos_cells else "none")
neg_total = sum(res["results"][d]["main"]["summary"][mm]["sig"] == "neg" for d in NAMES for mm in LOCAL)
mac("NNegCellsMain", neg_total)
mac("NCellsMain", len(NAMES) * len(LOCAL))

# criterion
for mm, v in res["criterion"].items():
    mac(f"Crit{TAG[mm]}Pos", v["n_ci_positive"])
    mac(f"Crit{TAG[mm]}Neg", v["n_ci_negative"])
    mac(f"Crit{TAG[mm]}Majority", "met" if v["majority_criterion"] else "not met")
    mac(f"Crit{TAG[mm]}Regimes", ", ".join(v["named_regimes"]) if v["named_regimes"] else "none")
    mac(f"Crit{TAG[mm]}Verdict", "yes" if v["added_value"] else "no")
with open(os.path.join(OUT, "table_criterion.tex"), "w") as fh:
    for mm in LOCAL:
        v = res["criterion"][mm]
        fh.write(f"{MPRETTY[mm]} & {v['n_ci_positive']}/{v['n_datasets']} & {v['n_ci_negative']}/{v['n_datasets']} & "
                 f"{'met' if v['majority_criterion'] else 'not met'} & {', '.join(v['named_regimes']) if v['named_regimes'] else 'none'} & "
                 f"{'yes (by the letter; see text)' if v['added_value'] else 'no'} \\\\\n")

# robustness: mean accuracy drop per method averaged over datasets
for c in ["noise20", "sub25"]:
    for mm in METHODS:
        drops = [res["robustness"][c][d][mm]["drop"] for d in NAMES]
        mac(f"Drop{CTAG[c]}{TAG[mm]}", f"{100*sum(drops)/len(drops):.1f}")
with open(os.path.join(OUT, "table_drop.tex"), "w") as fh:
    for mm in METHODS:
        row = [MPRETTY[mm]]
        for c in ["noise20", "sub25"]:
            drops = [res["robustness"][c][d][mm]["drop"] for d in NAMES]
            accs = [res["robustness"][c][d][mm]["acc"] for d in NAMES]
            row += [f"{100*sum(accs)/len(accs):.1f}", f"{100*sum(drops)/len(drops):.1f}"]
        accs_main = [res["results"][d]["main"]["summary"][mm]["mean_acc"] for d in NAMES]
        fh.write(f"{row[0]} & {100*sum(accs_main)/len(accs_main):.1f} & " + " & ".join(row[1:]) + " \\\\\n")

# post-hoc oracle table (main) and macros
with open(os.path.join(OUT, "table_posthoc_main.tex"), "w") as fh:
    for d in NAMES:
        r = post["conditions"]["main"][d]
        fh.write(f"{PRETTY[d]} & {100*r['oracle_mean_acc']:.1f} & " + " & ".join(cell_diff(r[f'{mm}_vs_oracle']) for mm in LOCAL) + " \\\\\n")
for c in m["conditions"]:
    for d in NAMES:
        for mm in LOCAL:
            r = post["conditions"][c][d][f"{mm}_vs_oracle"]
            mac(f"Post{CTAG[c]}{DTAG[d]}{TAG[mm]}", pp(r["diff_mean"]))
            mac(f"PostLo{CTAG[c]}{DTAG[d]}{TAG[mm]}", pp(r["diff_ci"][0]))
            mac(f"PostHi{CTAG[c]}{DTAG[d]}{TAG[mm]}", pp(r["diff_ci"][1]))
    for mm in LOCAL:
        sig = [post["conditions"][c][d][f"{mm}_vs_oracle"]["sig"] for d in NAMES]
        mac(f"PostNPos{CTAG[c]}{TAG[mm]}", sum(s == "pos" for s in sig))
        mac(f"PostNNeg{CTAG[c]}{TAG[mm]}", sum(s == "neg" for s in sig))
post_pos_total = sum(post["conditions"][c][d][f"{mm}_vs_oracle"]["sig"] == "pos" for c in m["conditions"] for d in NAMES for mm in LOCAL)
mac("PostNPosAll", post_pos_total)
mac("PostNCellsAll", len(m["conditions"]) * len(NAMES) * len(LOCAL))

# ---------------------------------------------------------------- exact example
e = ex
mac("ExDelta", e["meta"]["delta"])
mac("ExMu", f"{e['meta']['mu']:.3f}")
mac("ExBayes", f"{e['meta']['bayes']:.4f}")
mac("ExMonotone", "strictly decreasing" if e["A_monotone_check"]["strictly_decreasing"] else "NOT strictly decreasing")
mac("ExMonotoneMax", e["A_monotone_check"]["range"][1])
mac("ExPartN", e["B_partition"]["n"])
for n, r in e["A_learning_curve"].items():
    mac(f"ExRnc{n}", f"{r['risk']:.5f}")
    mac(f"ExExc{n}", f"{1e4*r['excess']:.1f}")  # in units of 1e-4
with open(os.path.join(OUT, "table_exact_curve.tex"), "w") as fh:
    for n, r in e["A_learning_curve"].items():
        fh.write(f"{n} & {r['risk']:.5f} & {1e4*r['excess']:.1f} \\\\\n")
with open(os.path.join(OUT, "table_exact_partition.tex"), "w") as fh:
    for M, r in e["B_partition"]["rows"].items():
        fh.write(f"{M} & {r['risk']:.5f} & {1e4*r['excess']:.1f} & {r['excess_ratio_vs_global']:.2f} \\\\\n")
for M, r in e["B_partition"]["rows"].items():
    mac(f"ExPartRisk{M}", f"{r['risk']:.5f}")
    mac(f"ExPartExc{M}", f"{1e4*r['excess']:.1f}")
    mac(f"ExPartRatio{M}", f"{r['excess_ratio_vs_global']:.2f}")
c = e["C_montecarlo"]
mac("ExMcReps", c["reps"])
mac("ExMcGlobal", f"{c['global']['mean']:.5f}")
mac("ExMcGlobalSe", f"{c['global']['se']:.5f}")
mac("ExMcGlobalExact", f"{c['global']['exact']:.5f}")
mac("ExMcPart", f"{c['partition_M4']['mean']:.5f}")
mac("ExMcPartSe", f"{c['partition_M4']['se']:.5f}")
mac("ExMcPartExact", f"{c['partition_M4']['exact']:.5f}")
d1 = e["D1_knn_centroid"]
mac("ExDoneReps", d1["reps"])
mac("ExDoneTest", d1["n_test"])
with open(os.path.join(OUT, "table_exact_knn.tex"), "w") as fh:
    for k, r in d1["rows"].items():
        fh.write(f"{k} & {r['mean']:.4f} & {r['se']:.4f} \\\\\n")
for k, r in d1["rows"].items():
    mac(f"ExKnnC{k}", f"{r['mean']:.4f}")
worst_k = max(d1["rows"], key=lambda k: d1["rows"][k]["mean"])
mac("ExKnnCWorstK", worst_k)
mac("ExKnnCWorst", f"{d1['rows'][worst_k]['mean']:.4f}")
d2 = e["D2_knn_svm"]
mac("ExDtwoReps", d2["reps"])
mac("ExDtwoTest", d2["n_test"])
with open(os.path.join(OUT, "table_exact_knnsvm.tex"), "w") as fh:
    for k, r in d2["rows"].items():
        fh.write(f"{'global' if k == 'all' else k} & {r['mean']:.4f} & {r['se']:.4f} \\\\\n")
for k, r in d2["rows"].items():
    mac(f"ExKnnS{'All' if k == 'all' else k}", f"{r['mean']:.4f}")
    mac(f"ExKnnSSe{'All' if k == 'all' else k}", f"{r['se']:.4f}")
d3 = e["D3_svm_learning_curve"]
mac("ExDthreeReps", d3["reps"])
with open(os.path.join(OUT, "table_exact_svmcurve.tex"), "w") as fh:
    for n, r in d3["rows"].items():
        fh.write(f"{n} & {r['mean']:.4f} & {r['se']:.4f} \\\\\n")
for n, r in d3["rows"].items():
    mac(f"ExSvmCurve{n}", f"{r['mean']:.4f}")
    mac(f"ExSvmCurveSe{n}", f"{r['se']:.4f}")
vals = [d3["rows"][n]["mean"] for n in d3["rows"]]
mac("ExSvmCurveMonotone", "decreasing at every step" if all(b < a for a, b in zip(vals, vals[1:])) else "NOT monotone")
d4 = e["D4_svm_partition"]
mac("ExDfourReps", d4["reps"])
with open(os.path.join(OUT, "table_exact_svmpart.tex"), "w") as fh:
    for M, r in d4["rows"].items():
        fh.write(f"{M} & {r['mean']:.4f} & {r['se']:.4f} \\\\\n")
for M, r in d4["rows"].items():
    mac(f"ExSvmPart{M}", f"{r['mean']:.4f}")
    mac(f"ExSvmPartSe{M}", f"{r['se']:.4f}")

with open(os.path.join(OUT, "numbers.tex"), "w") as fh:
    fh.write("% generated by experiments/make_numbers.py -- do not edit\n" + "\n".join(L) + "\n")
print(f"wrote {len(L)} macros and table bodies to {OUT}")
