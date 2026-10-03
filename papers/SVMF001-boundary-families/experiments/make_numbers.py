#!/usr/bin/env python3
"""Turn results/*.json into LaTeX macros (manuscript/numbers.tex) and table bodies
(manuscript/table_*.tex).  No number in main.tex is typed by hand.

v0.2 (03/10/2026): merged accuracy+difference tables with two-line cells (no \\resizebox),
grid-saturation table and macros (referee B1), nested comparison of each family against
its own fixed global member taken from posthoc_oracle.json (referee M3)."""
import glob
import json
import os
import re

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
PRETTY = {"wine": "wine", "breast_cancer": "breast cancer", "digits_parity": "digits (parity)", "gauss_linear": "Gaussian (linear)",
          "moons_2scale": "two-scale moons", "checker_2scale": "two-scale checkerboard"}
MPRETTY = {"linear": "linear SVM", "rbf": "RBF-SVM", "best_global": "best global (inner CV)", "knn_svm": "kNN-SVM",
           "cell_svm": "cell-SVM", "vb_rbf": "VB-RBF-SVM", "llsvm": "LLSVM"}
# the fixed global member of each local family (referee M3); kNN-SVM's member is the linear
# SVM with C = 1 fixed, which posthoc_oracle.json approximates by the tuned linear SVM
OWN_MEMBER = {"knn_svm": "linear", "cell_svm": "linear", "vb_rbf": "rbf", "llsvm": "linear"}
REGIMES = res["meta"]["regimes"]

L = []
_DIG = ["Zero", "One", "Two", "Three", "Four", "Five", "Six", "Seven", "Eight", "Nine"]


def W(n):
    """Spell the digits of n so that it can be part of a LaTeX macro name (320 -> ThreeTwoZero)."""
    return "".join(_DIG[int(ch)] for ch in str(n))


def mac(name, val):
    assert not any(ch.isdigit() for ch in name), name
    L.append(rf"\newcommand{{\{name}}}{{{val}}}")


def pp(x, sign=True):
    return f"{100*x:+.2f}" if sign else f"{100*x:.2f}"


def cell_diff(d):
    lo, hi = d["diff_ci"]
    mark = {"pos": r"$^{+}$", "neg": r"$^{-}$", "none": ""}[d["sig"]]
    return f"{pp(d['diff_mean'])} [{pp(lo)}, {pp(hi)}]{mark}"


SHORT = {"wine": "wine", "breast_cancer": "breast cancer", "digits_parity": "digits", "gauss_linear": "Gaussian",
         "moons_2scale": "moons", "checker_2scale": "checkerboard"}  # short labels for the wide merged tables


def two_line(d):
    """(line 1, line 2) of a two-line cell: bold mean when the interval excludes zero, then the interval."""
    lo, hi = d["diff_ci"]
    m = pp(d["diff_mean"])
    if d["sig"] != "none":
        m = rf"\textbf{{{m}}}"
    return m, f"[{pp(lo)},\,{pp(hi)}]"


def write_two_line_table(path, rows):
    """rows: list of (label, [fixed cells], [two-line dicts]) -> body with two lines per row."""
    with open(path, "w") as fh:
        for i, (label, fixed, cells) in enumerate(rows):
            if i:
                fh.write("\\addlinespace[1.5pt]\n")
            tl = [two_line(c) for c in cells]
            fh.write(f"{label} & " + " & ".join(fixed + [t[0] for t in tl]) + " \\\\\n")
            fh.write("& " + " & ".join([""] * len(fixed) + [t[1] for t in tl]) + " \\\\\n")


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
mac("NoiseProb", m["conditions"]["noise20"]["noise"])
mac("SubFrac", int(round(100 * m["conditions"]["sub25"]["frac"])))
mac("InnerFolds", m["grid"]["inner_folds"])
mac("KnnValCap", m["grid"]["knn_val_cap"])


def glist(vals):
    return ", ".join(f"{v:g}" if isinstance(v, float) else str(v) for v in vals)


mac("KnnKs", glist(m["grid"]["knn_ks"]))
mac("KnnC", f"{m['grid']['knn_C']:g}")
mac("VbKbw", m["grid"]["vb_kbw"])
mac("VbBetas", glist(m["grid"]["vb_betas"]))
mac("GammaMults", glist(m["grid"]["gamma_mults"]))
mac("GammaMultMax", f"{max(m['grid']['gamma_mults']):g}")
mac("CRbf", glist(m["grid"]["C_rbf"]))
mac("CRbfMax", f"{max(m['grid']['C_rbf']):g}")
mac("CLin", glist(m["grid"]["C_lin"]))
mac("CellMs", glist(m["grid"]["cell_Ms"]))
mac("CellMMax", max(m["grid"]["cell_Ms"]))
mac("CellCs", glist(m["grid"]["cell_Cs"]))
mac("LlsvmMs", glist(m["grid"]["llsvm_Ms"]))
mac("LlsvmCs", glist(m["grid"]["llsvm_Cs"]))
mac("KnnKMin", min(m["grid"]["knn_ks"]))

# datasets table
with open(os.path.join(OUT, "table_datasets.tex"), "w") as fh:
    for d in NAMES:
        info = res["datasets"][d]
        fh.write(f"{PRETTY[d]} & {info['regime']} & {info['n']} & {info['d']} & {res['results'][d]['main']['n_train']} & "
                 f"{res['results'][d]['sub25']['n_train']} & {100*info['pos_frac']:.0f}\\% \\\\\n")
for d in NAMES:
    mac(f"N{DTAG[d]}", res["datasets"][d]["n"])
    mac(f"D{DTAG[d]}", res["datasets"][d]["d"])
    mac(f"NTrainMain{DTAG[d]}", res["results"][d]["main"]["n_train"])
    mac(f"NTrainSub{DTAG[d]}", res["results"][d]["sub25"]["n_train"])

# per-condition tables: merged (reference accuracies + two-line paired differences), accuracies, local fractions
for c in m["conditions"]:
    rows = []
    for d in NAMES:
        s = res["results"][d][c]["summary"]
        rows.append((SHORT[d], [f"{100*s[mm]['mean_acc']:.1f}" for mm in ["linear", "rbf", "best_global"]], [s[mm] for mm in LOCAL]))
    write_two_line_table(os.path.join(OUT, f"table_merged_{c}.tex"), rows)
    with open(os.path.join(OUT, f"table_diff_{c}.tex"), "w") as fh:  # one-line version (results/tables.md style)
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
pos_cells = [(d, mm) for d in NAMES for mm in LOCAL if res["results"][d]["main"]["summary"][mm]["sig"] == "pos"]
mac("NPosCellsMain", len(pos_cells))
mac("PosCellsMain", "; ".join(f"{MPRETTY[mm]} on {PRETTY[d]}" for d, mm in pos_cells) if pos_cells else "none")
neg_total = sum(res["results"][d]["main"]["summary"][mm]["sig"] == "neg" for d in NAMES for mm in LOCAL)
mac("NNegCellsMain", neg_total)
mac("NCellsMain", len(NAMES) * len(LOCAL))
mac("NCellsAll", len(m["conditions"]) * len(NAMES) * len(LOCAL))
# "expected by chance" (referee 2, M4): one-sided counts, nominal (0.025 N) and with the coverage of the
# percentile bootstrap simulated by bootstrap_coverage.py (i.i.d. normal folds, the favourable case)
cov = json.load(open(os.path.join(ROOT, "results", "bootstrap_coverage.json")))
cc = cov["counts"]
mac("CovTen", f"{100*cov['sim']['10']['coverage']:.1f}")
mac("CovFive", f"{100*cov['sim']['5']['coverage']:.1f}")
mac("OneSidedTen", f"{100*cov['sim']['10']['p_one_sided']:.1f}")
mac("OneSidedFive", f"{100*cov['sim']['5']['p_one_sided']:.1f}")
mac("CovReps", cov["sim"]["10"]["replications"])
mac("ExpectedPosMainNominal", f"{cc['expected_above_main_nominal']:.1f}")
mac("ExpectedPosRobustNominal", f"{cc['expected_above_robust_nominal']:.1f}")
mac("ExpectedPosMain", f"{cc['expected_above_main_sim']:.1f}")
mac("ExpectedPosRobust", f"{cc['expected_above_robust_sim']:.1f}")
mac("PAtLeastRobustSim", f"{cc['p_at_least_obs_robust_sim']:.2f}")
mac("PAtLeastRobustNominal", f"{cc['p_at_least_obs_robust_nominal']:.2f}")
mac("PAtLeastMainSim", f"{cc['p_at_least_obs_main_sim']:.2f}")
# range of the significant negative differences of the three local linear families on the multiscale sets
neg_vals = [100 * res["results"][d]["main"]["summary"][mm]["diff_mean"] for d in REGIMES["multiscale"] for mm in ["knn_svm", "cell_svm", "llsvm"]
            if res["results"][d]["main"]["summary"][mm]["sig"] == "neg"]
mac("NNegLinLocalMulti", len(neg_vals))
mac("NegLinLocalMultiMin", f"{min(neg_vals):.1f}" if neg_vals else "n/a")
mac("NegLinLocalMultiMax", f"{max(neg_vals):.1f}" if neg_vals else "n/a")

# absolute range of the significant negative differences of the local linear families on the multiscale sets
mac("NegLinLocalMultiLoAbs", f"{abs(max(neg_vals)):.1f}" if neg_vals else "n/a")  # smallest loss
mac("NegLinLocalMultiHiAbs", f"{abs(min(neg_vals)):.1f}" if neg_vals else "n/a")  # largest loss
# robustness conditions: counts of intervals above / below zero and the list of the positive cells
rob = [c for c in m["conditions"] if c != "main"]
rob_cells = [(c, d, mm) for c in rob for d in NAMES for mm in LOCAL]
mac("NRobustCells", len(rob_cells))
rob_pos = [(c, d, mm) for c, d, mm in rob_cells if res["results"][d][c]["summary"][mm]["sig"] == "pos"]
mac("NPosRobustCells", len(rob_pos))
mac("NNegRobustCells", sum(res["results"][d][c]["summary"][mm]["sig"] == "neg" for c, d, mm in rob_cells))
CNAME = {"noise20": "noise", "sub25": "sub"}
mac("PosCellsRobust", "; ".join(f"{MPRETTY[mm]} on {PRETTY[d]} under {CNAME[c]}" for c, d, mm in rob_pos) if rob_pos else "none")
mac("NPosRobustMoons", sum(d == "moons_2scale" for c, d, mm in rob_pos))
# referee 2, m4: which robustness positives persist against the post-hoc oracle AND the fixed RBF-SVM
persist = [(c, d, mm) for c, d, mm in rob_pos
           if post["conditions"][c][d][f"{mm}_vs_oracle"]["sig"] == "pos" and post["conditions"][c][d][f"{mm}_vs_rbf"]["sig"] == "pos"]
mac("NPosRobustPersist", len(persist))
mac("NPosRobustPersistMoons", sum(d == "moons_2scale" for c, d, mm in persist))
mac("PosRobustNotPersist", "; ".join(f"{MPRETTY[mm]} on {PRETTY[d]} under {CNAME[c]}" for c, d, mm in rob_pos if (c, d, mm) not in persist) or "none")
# v0.1 results (kept in results/v01/) for the before/after statements about the grids; macros only, nothing typed
v01_path = os.path.join(ROOT, "results", "v01", "results.json")
if os.path.exists(v01_path):
    v1 = json.load(open(v01_path))
    g1 = v1["meta"]["grid"]
    for d in NAMES:
        for mm in LOCAL:
            mac(f"VOneDiffMain{DTAG[d]}{TAG[mm]}", pp(v1["results"][d]["main"]["summary"][mm]["diff_mean"]))
    v1neg = [100 * v1["results"][d]["main"]["summary"][mm]["diff_mean"] for d in REGIMES["multiscale"] for mm in ["knn_svm", "cell_svm", "llsvm"]]
    mac("VOneLinLocalMultiLoAbs", f"{abs(max(v1neg)):.1f}")
    mac("VOneLinLocalMultiHiAbs", f"{abs(min(v1neg)):.1f}")
    mac("VOneGammaMultMax", f"{max(g1['gamma_mults']):g}")
    mac("VOneCRbfMax", f"{max(g1['C_rbf']):g}")
    mac("VOneMMax", max(g1["cell_Ms"]))
    mac("VOneKMin", min(g1["knn_ks"]))
    folds_ms = [f for d in REGIMES["multiscale"] for f in v1["results"][d]["main"]["folds"]]
    mac("VOneMultiFolds", len(folds_ms))
    mac("VOneEdgeRbfGammaHi", sum(f["rbf"]["cfg"]["gamma_mult"] == max(g1["gamma_mults"]) for f in folds_ms))
    mac("VOneEdgeRbfCHi", sum(f["rbf"]["cfg"]["C"] == max(g1["C_rbf"]) for f in folds_ms))
    mac("VOneEdgeCellMHi", sum(f["cell_svm"]["cfg"]["M"] == max(g1["cell_Ms"]) for f in folds_ms))
    mac("VOneEdgeLlsvmMHi", sum(f["llsvm"]["cfg"]["M"] == max(g1["llsvm_Ms"]) for f in folds_ms))
    mac("VOneEdgeKnnKLo", sum(f["knn_svm"]["cfg"]["k"] == min(g1["knn_ks"]) for f in folds_ms))
    mac("VOneSecondsMain", int(round(v1["meta"]["seconds"])))
    # referee 2, M2: the C grids of cell-SVM and LLSVM were not widened although v0.1 already saturated them
    mac("VOneEdgeCellCHi", sum(f["cell_svm"]["cfg"]["C"] == max(g1["cell_Cs"]) for f in folds_ms))
    mac("VOneEdgeLlsvmCHi", sum(f["llsvm"]["cfg"]["C"] == max(g1["llsvm_Cs"]) for f in folds_ms))
    mac("VOneNPosRobustCells", sum(v1["results"][d][c]["summary"][mm]["sig"] == "pos" for c in rob for d in NAMES for mm in LOCAL))

# criterion
for mm, v in res["criterion"].items():
    mac(f"Crit{TAG[mm]}Pos", v["n_ci_positive"])
    mac(f"Crit{TAG[mm]}Neg", v["n_ci_negative"])
    mac(f"Crit{TAG[mm]}Majority", "met" if v["majority_criterion"] else "not met")
    mac(f"Crit{TAG[mm]}Regimes", ", ".join(v["named_regimes"]) if v["named_regimes"] else "none")
    mac(f"Crit{TAG[mm]}Verdict", "yes" if v["added_value"] else "no")
mac("NFamiliesAddedValue", sum(v["added_value"] for v in res["criterion"].values()))
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

# post-hoc oracle (two-line) and nested comparison against each family's own fixed global member
for c in m["conditions"]:
    rows_or, rows_nest = [], []
    for d in NAMES:
        r = post["conditions"][c][d]
        rows_or.append((PRETTY[d], [f"{100*r['oracle_mean_acc']:.1f}"], [r[f"{mm}_vs_oracle"] for mm in LOCAL]))
        rows_nest.append((PRETTY[d], [], [r[f"{mm}_vs_{OWN_MEMBER[mm]}"] for mm in LOCAL]))
    write_two_line_table(os.path.join(OUT, f"table_posthoc_{c}.tex"), rows_or)
    write_two_line_table(os.path.join(OUT, f"table_nested_{c}.tex"), rows_nest)
    for d in NAMES:
        for mm in LOCAL:
            r = post["conditions"][c][d][f"{mm}_vs_oracle"]
            mac(f"Post{CTAG[c]}{DTAG[d]}{TAG[mm]}", pp(r["diff_mean"]))
            mac(f"PostLo{CTAG[c]}{DTAG[d]}{TAG[mm]}", pp(r["diff_ci"][0]))
            mac(f"PostHi{CTAG[c]}{DTAG[d]}{TAG[mm]}", pp(r["diff_ci"][1]))
            r = post["conditions"][c][d][f"{mm}_vs_{OWN_MEMBER[mm]}"]
            mac(f"Nest{CTAG[c]}{DTAG[d]}{TAG[mm]}", pp(r["diff_mean"]))
            mac(f"NestLo{CTAG[c]}{DTAG[d]}{TAG[mm]}", pp(r["diff_ci"][0]))
            mac(f"NestHi{CTAG[c]}{DTAG[d]}{TAG[mm]}", pp(r["diff_ci"][1]))
    for mm in LOCAL:
        sig = [post["conditions"][c][d][f"{mm}_vs_oracle"]["sig"] for d in NAMES]
        mac(f"PostNPos{CTAG[c]}{TAG[mm]}", sum(s == "pos" for s in sig))
        mac(f"PostNNeg{CTAG[c]}{TAG[mm]}", sum(s == "neg" for s in sig))
        sig = [post["conditions"][c][d][f"{mm}_vs_{OWN_MEMBER[mm]}"]["sig"] for d in NAMES]
        mac(f"NestNPos{CTAG[c]}{TAG[mm]}", sum(s == "pos" for s in sig))
        mac(f"NestNNeg{CTAG[c]}{TAG[mm]}", sum(s == "neg" for s in sig))
mac("PostNPosMain", sum(post["conditions"]["main"][d][f"{mm}_vs_oracle"]["sig"] == "pos" for d in NAMES for mm in LOCAL))
mac("PostNPosAll", sum(post["conditions"][c][d][f"{mm}_vs_oracle"]["sig"] == "pos" for c in m["conditions"] for d in NAMES for mm in LOCAL))
mac("NestNPosAll", sum(post["conditions"][c][d][f"{mm}_vs_{OWN_MEMBER[mm]}"]["sig"] == "pos" for c in m["conditions"] for d in NAMES for mm in LOCAL))
mac("NestNPosMain", sum(post["conditions"]["main"][d][f"{mm}_vs_{OWN_MEMBER[mm]}"]["sig"] == "pos" for d in NAMES for mm in LOCAL))
mac("NestNNegMain", sum(post["conditions"]["main"][d][f"{mm}_vs_{OWN_MEMBER[mm]}"]["sig"] == "neg" for d in NAMES for mm in LOCAL))
mac("PostNCellsAll", len(m["conditions"]) * len(NAMES) * len(LOCAL))

# ---------------------------------------------------------------- grid saturation (referee B1)
EDGE_ROWS = [("linear", "C", "linear SVM: $C$", "lo", "hi"), ("rbf", "gamma_mult", r"RBF-SVM: $\gamma$", "lo", "hi"), ("rbf", "C", "RBF-SVM: $C$", "lo", "hi"),
             ("knn_svm", "k", "kNN-SVM: $k$", "lo", None), ("cell_svm", "M", "cell-SVM: $M$", None, "hi"), ("cell_svm", "C", "cell-SVM: $C$", "lo", "hi"),
             ("vb_rbf", "gamma_mult", r"VB-RBF-SVM: $\gamma$", "lo", "hi"), ("vb_rbf", "C", "VB-RBF-SVM: $C$", "lo", "hi"), ("vb_rbf", "beta", r"VB-RBF-SVM: $\beta$", None, "hi"),
             ("llsvm", "M", "LLSVM: $M$", None, "hi"), ("llsvm", "C", "LLSVM: $C$", "lo", "hi")]
PTAG = {"C": "C", "gamma_mult": "Gamma", "k": "K", "M": "M", "beta": "Beta"}
has_edge = all("edge" in res["results"][d]["main"]["summary"] for d in NAMES)
mac("HasEdge", "yes" if has_edge else "no")
for c in m["conditions"]:
    with open(os.path.join(OUT, f"table_edge_{c}.tex"), "w") as fh:
        for meth, par, label, lo, hi in EDGE_ROWS:
            cells, tot_lo, tot_hi, tot_n = [], 0, 0, 0
            for d in NAMES:
                e = res["results"][d][c]["summary"].get("edge", {}).get(meth, {}).get(par) if has_edge else None
                if e is None:
                    cells.append("n/a")
                    continue
                a = "--" if e["lo"] is None else str(e["lo"])
                b = "--" if e["hi"] is None else str(e["hi"])
                cells.append(f"{a}/{b}")
                tot_lo += e["lo"] or 0
                tot_hi += e["hi"] or 0
                tot_n += e["n"]
                mac(f"Edge{CTAG[c]}{DTAG[d]}{TAG[meth]}{PTAG[par]}Lo", "--" if e["lo"] is None else e["lo"])
                mac(f"Edge{CTAG[c]}{DTAG[d]}{TAG[meth]}{PTAG[par]}Hi", "--" if e["hi"] is None else e["hi"])
            n_fold = res["results"][NAMES[0]][c]["summary"]["edge"][meth][par]["n"] if has_edge else 0
            fh.write(f"{label} & " + " & ".join(cells) + f" & {'--' if lo is None else tot_lo}/{'--' if hi is None else tot_hi} \\\\\n")
            mac(f"Edge{CTAG[c]}All{TAG[meth]}{PTAG[par]}Lo", tot_lo)
            mac(f"Edge{CTAG[c]}All{TAG[meth]}{PTAG[par]}Hi", tot_hi)
            mac(f"Edge{CTAG[c]}All{TAG[meth]}{PTAG[par]}N", tot_n)
            if has_edge:
                ms = [res["results"][d][c]["summary"]["edge"][meth][par] for d in REGIMES["multiscale"]]
                mac(f"Edge{CTAG[c]}Multi{TAG[meth]}{PTAG[par]}Lo", sum(e["lo"] or 0 for e in ms))
                mac(f"Edge{CTAG[c]}Multi{TAG[meth]}{PTAG[par]}Hi", sum(e["hi"] or 0 for e in ms))
                mac(f"Edge{CTAG[c]}Multi{TAG[meth]}{PTAG[par]}N", sum(e["n"] for e in ms))
    mac(f"Edge{CTAG[c]}FoldsPerSet", res["results"][NAMES[0]][c]["summary"]["edge"]["rbf"]["C"]["n"] if has_edge else 0)
if has_edge:
    # worst remaining saturation in the main condition: the largest per-data-set count at any edge, and where
    worst = max(((res["results"][d]["main"]["summary"]["edge"][meth][par][side] or 0, d, meth, par, side)
                 for meth, par, label, lo, hi in EDGE_ROWS for d in NAMES for side in ("lo", "hi")
                 if res["results"][d]["main"]["summary"]["edge"][meth][par][side] is not None))
    mac("EdgeMainWorstCount", worst[0])
    mac("EdgeMainWorstWhere", f"{MPRETTY[worst[2]]}, {dict((r[1], r[2].split(': ')[1]) for r in EDGE_ROWS)[worst[3]]} at the {'lower' if worst[4] == 'lo' else 'upper'} edge on {PRETTY[worst[1]]}")
    n_sat = sum(1 for meth, par, label, lo, hi in EDGE_ROWS for d in NAMES for side in ("lo", "hi")
                if res["results"][d]["main"]["summary"]["edge"][meth][par][side] is not None
                and res["results"][d]["main"]["summary"]["edge"][meth][par][side] >= 0.5 * res["results"][d]["main"]["summary"]["edge"][meth][par]["n"])
    mac("EdgeMainNHalfOrMore", n_sat)
    n_cells = sum(1 for meth, par, label, lo, hi in EDGE_ROWS for d in NAMES for side in ("lo", "hi")
                  if res["results"][d]["main"]["summary"]["edge"][meth][par][side] is not None)
    mac("EdgeMainNCells", n_cells)

# ---------------------------------------------------------------- referee 2 (03/10/2026): extra counts used in the text
gmax = {k: max(v) for k, v in m["grid"].items() if isinstance(v, list)}
fms = [f for d in REGIMES["multiscale"] for f in res["results"][d]["main"]["folds"]]
mac("EdgeMainMultiLlsvmBothHi", sum(f["llsvm"]["cfg"]["M"] == gmax["llsvm_Ms"] and f["llsvm"]["cfg"]["C"] == gmax["llsvm_Cs"] for f in fms))
mac("EdgeMainMultiCellBothHi", sum(f["cell_svm"]["cfg"]["M"] == gmax["cell_Ms"] and f["cell_svm"]["cfg"]["C"] == gmax["cell_Cs"] for f in fms))
mac("EdgeMainMultiN", len(fms))
mac("CellCMax", f"{gmax['cell_Cs']:g}")
mac("LlsvmCMax", f"{gmax['llsvm_Cs']:g}")
mac("LinCMin", f"{min(m['grid']['C_lin']):g}")
mac("CellCMin", f"{min(m['grid']['cell_Cs']):g}")
mac("LlsvmCMin", f"{min(m['grid']['llsvm_Cs']):g}")
# M6: the positive Gaussian cell in test points (accuracies are hits / n_test, n_test = n - n_train)
gd = "gauss_linear"
gF = res["results"][gd]["main"]["folds"]
nte = res["datasets"][gd]["n"] - res["results"][gd]["main"]["n_train"]
hits = [{mm: int(round(f[mm]["acc"] * nte)) for mm in METHODS} for f in gF]
pick = [f["best_global"]["cfg"]["pick"] for f in gF]
vb_over_sel = sum(h["vb_rbf"] - h["best_global"] for h in hits)
mac("GaussCellPts", vb_over_sel)
mac("GaussCellN", nte * len(gF))
mac("GaussVbOwnFolds", sum(h["vb_rbf"] > h["rbf"] for h in hits))  # VB above its own RBF member
mac("GaussVbOwnPts", sum(h["vb_rbf"] - h["rbf"] for h in hits if h["vb_rbf"] > h["rbf"]))
mac("GaussSelLinFolds", sum(p == "linear" for p in pick))
mac("GaussSelLinLossFolds", sum(p == "linear" and h["rbf"] > h["linear"] for p, h in zip(pick, hits)))
mac("GaussSelLinVbGainFolds", sum(p == "linear" and h["vb_rbf"] > h["best_global"] for p, h in zip(pick, hits)))
mac("GaussPickRbfN", sum(p == "rbf" for p in pick))
mac("GaussPickRbfLinBetter", sum(p == "rbf" and h["linear"] > h["rbf"] for p, h in zip(pick, hits)))
mac("GaussPickRbfTie", sum(p == "rbf" and h["linear"] == h["rbf"] for p, h in zip(pick, hits)))
mac("GaussPickRbfLinWorse", sum(p == "rbf" and h["linear"] < h["rbf"] for p, h in zip(pick, hits)))
mac("GaussPickRbfLossMax", max(h["linear"] - h["rbf"] for p, h in zip(pick, hits) if p == "rbf"))
assert vb_over_sel == sum(h["vb_rbf"] > h["best_global"] for h in hits) and all(h["vb_rbf"] >= h["best_global"] for h in hits)
# the text says "by one point" / "one point each" / "the other differences cancel": check that it is so
assert all(h["vb_rbf"] - h["rbf"] in (0, 1) for h in hits if h["vb_rbf"] >= h["rbf"])
assert all(h["rbf"] - h["linear"] == 1 for p, h in zip(pick, hits) if p == "linear")
assert sum(h["rbf"] - h["linear"] for p, h in zip(pick, hits) if p == "rbf") == -max(h["linear"] - h["rbf"] for p, h in zip(pick, hits) if p == "rbf")
# m3: the upper end of the wine/cell-SVM interval, to three decimals of a percentage point
mac("DiffHiExactMainWineCell", f"{100*res['results']['wine']['main']['summary']['cell_svm']['diff_ci'][1]:.3f}")
# m5: the D1 worst case in excess risk (Bayes risk subtracted) as well as in risk
mac("ExKnnCWorstExc", f"{ex['D1_knn_centroid']['rows'][str(max(ex['D1_knn_centroid']['rows'], key=lambda k: ex['D1_knn_centroid']['rows'][k]['mean']))]['mean'] - ex['meta']['bayes']:.4f}")
mac("ExKnnCGlobalExc", f"{ex['D1_knn_centroid']['rows'][str(ex['B_partition']['n'])]['mean'] - ex['meta']['bayes']:.4f}")

# ---------------------------------------------------------------- exact example
e = ex
mac("ExDelta", e["meta"]["delta"])
mac("ExMu", f"{e['meta']['mu']:.3f}")
mac("ExBayes", f"{e['meta']['bayes']:.4f}")
mac("ExMonotone", "strictly decreasing" if e["A_monotone_check"]["strictly_decreasing"] else "NOT strictly decreasing")
mac("ExMonotoneMax", e["A_monotone_check"]["range"][1])
mac("ExPartN", e["B_partition"]["n"])
for n, r in e["A_learning_curve"].items():
    mac(f"ExRnc{W(n)}", f"{r['risk']:.5f}")
    mac(f"ExExc{W(n)}", f"{1e4*r['excess']:.1f}")  # in units of 1e-4
with open(os.path.join(OUT, "table_exact_curve.tex"), "w") as fh:
    for n, r in e["A_learning_curve"].items():
        fh.write(f"{n} & {r['risk']:.5f} & {1e4*r['excess']:.1f} \\\\\n")
with open(os.path.join(OUT, "table_exact_partition.tex"), "w") as fh:
    for M, r in e["B_partition"]["rows"].items():
        fh.write(f"{M} & {r['risk']:.5f} & {1e4*r['excess']:.1f} & {r['excess_ratio_vs_global']:.2f} \\\\\n")
for M, r in e["B_partition"]["rows"].items():
    mac(f"ExPartRisk{W(M)}", f"{r['risk']:.5f}")
    mac(f"ExPartExc{W(M)}", f"{1e4*r['excess']:.1f}")
    mac(f"ExPartRatio{W(M)}", f"{r['excess_ratio_vs_global']:.2f}")
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
    mac(f"ExKnnC{W(k)}", f"{r['mean']:.4f}")
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
    mac(f"ExKnnS{'All' if k == 'all' else W(k)}", f"{r['mean']:.4f}")
    mac(f"ExKnnSSe{'All' if k == 'all' else W(k)}", f"{r['se']:.4f}")
d3 = e["D3_svm_learning_curve"]
mac("ExDthreeReps", d3["reps"])
with open(os.path.join(OUT, "table_exact_svmcurve.tex"), "w") as fh:
    for n, r in d3["rows"].items():
        fh.write(f"{n} & {r['mean']:.4f} & {r['se']:.4f} \\\\\n")
for n, r in d3["rows"].items():
    mac(f"ExSvmCurve{W(n)}", f"{r['mean']:.4f}")
    mac(f"ExSvmCurveSe{W(n)}", f"{r['se']:.4f}")
vals = [d3["rows"][n]["mean"] for n in d3["rows"]]
mac("ExSvmCurveMonotone", "decreasing at every step" if all(b < a for a, b in zip(vals, vals[1:])) else "NOT monotone")
d4 = e["D4_svm_partition"]
mac("ExDfourReps", d4["reps"])
with open(os.path.join(OUT, "table_exact_svmpart.tex"), "w") as fh:
    for M, r in d4["rows"].items():
        fh.write(f"{M} & {r['mean']:.4f} & {r['se']:.4f} \\\\\n")
for M, r in d4["rows"].items():
    mac(f"ExSvmPart{W(M)}", f"{r['mean']:.4f}")
    mac(f"ExSvmPartSe{W(M)}", f"{r['se']:.4f}")
w = e["E_prefactor_witness"]
mac("ExPrefreeMinEig", f"{w['min_eig_prefactor_free']:.2f}")
mac("ExFullMinEig", f"{w['min_eig_full_kernel']:.2f}")
mac("ExPrefreeN", len(w["x"]))
mac("ExPrefreeAmin", f"{min(w['a']):.3f}")
mac("ExPrefreeAmax", f"{max(w['a']):.0f}")

# table bodies: drop the trailing row terminator (main.tex writes it explicitly before \midrule/\bottomrule)
for tf in glob.glob(os.path.join(OUT, "table_*.tex")):
    body = open(tf).read()
    body = re.sub(r" \\\\\n$", "\n", body)
    open(tf, "w").write(body)

with open(os.path.join(OUT, "numbers.tex"), "w") as fh:
    fh.write("% generated by experiments/make_numbers.py -- do not edit\n" + "\n".join(L) + "\n")
print(f"wrote {len(L)} macros and table bodies to {OUT}")
