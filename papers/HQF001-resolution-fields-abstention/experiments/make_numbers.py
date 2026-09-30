#!/usr/bin/env python3
"""Turn results/results.json and results/results_identity.json into LaTeX macros
(manuscript/numbers.tex) and table bodies (manuscript/table_*.tex). No number in
main.tex is typed by hand."""
import json
import math
import os

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
OUT = os.path.join(ROOT, "manuscript")
res = json.load(open(os.path.join(ROOT, "results", "results.json")))
ide = json.load(open(os.path.join(ROOT, "results", "results_identity.json")))

DS_TAG = {"iris": "Iris", "wine": "Wine", "breast_cancer": "Bc", "digits": "Digits",
          "synth_informative": "Sinfo", "moons_aniso": "Moons", "synth_classcov": "Ccov", "synth_lda": "Slda"}
DS_NAME = {"iris": "iris", "wine": "wine", "breast_cancer": "breast-cancer", "digits": "digits",
           "synth_informative": "synth-informative", "moons_aniso": "moons-aniso",
           "synth_classcov": "synth-classcov", "synth_lda": "synth-lda"}
M_TAG = {"kNN": "Knn", "NCM": "Ncm", "LDA": "Lda", "QDA": "Qda", "LogReg": "Logreg", "RForest": "Rforest",
         "DANN": "Dann", "Field-aniso": "Faniso", "Field-iso": "Fiso", "Field-euclid": "Feuclid",
         "Field-vol": "Fvol", "Field-anis": "Fanis", "Field-aniso-gproto": "Fgproto"}
M_NAME = {"kNN": "$k$-NN", "NCM": "NCM", "LDA": "LDA", "QDA": "QDA", "LogReg": "LogReg", "RForest": "RForest",
          "DANN": "DANN", "Field-aniso": "Field (aniso)", "Field-iso": "Field (iso)", "Field-euclid": "Field (Eucl.)",
          "Field-vol": "Field (volume)", "Field-anis": "Field (anisotropy)", "Field-aniso-gproto": "Field (aniso, global prot.)"}
REFS = [m for m, g in res["method_groups"].items() if g == "reference"]
FIELDS = [m for m, g in res["method_groups"].items() if g == "field"]
S = res["summary"]
meta = res["meta"]
L = []


def mac(name, val):
    L.append(rf"\newcommand{{\{name}}}{{{val}}}")


def sci(x, digits=1):
    if x == 0:
        return r"\ensuremath{0}"
    e = int(math.floor(math.log10(abs(x))))
    m = x / 10 ** e
    if round(m, digits) >= 10:
        m /= 10
        e += 1
    return rf"\ensuremath{{{m:.{digits}f}\times 10^{{{e}}}}}"


def pct(x, d=2):
    return f"{100 * x:.{d}f}"


def spct(x, d=2):
    return f"{100 * x:+.{d}f}"


# ---- meta
mac("MetaSeed", meta["seed"])
mac("MetaPython", meta["python"])
mac("MetaNumpy", meta["numpy"])
mac("MetaScipy", meta["scipy"])
mac("MetaSklearn", meta["sklearn"])
mac("MetaCpuSeconds", int(round(meta["cpu_seconds"])))
mac("MetaCpuMinutes", f"{meta['cpu_seconds'] / 60:.1f}")
mac("MetaWallSeconds", int(round(meta["wall_seconds"])))
mac("MetaRepeats", meta["n_repeats"])
mac("MetaSplits", meta["n_splits"])
mac("MetaFolds", meta["n_repeats"] * meta["n_splits"])
mac("MetaInner", meta["inner_splits"])
mac("MetaBootB", meta["bootstrap_B"])
mac("MetaNDatasets", len(S))
mac("MetaMajority", len(S) // 2 + 1)
mac("MetaNRefs", len(REFS))
mac("MetaNFields", len(FIELDS))
mac("IdCpuSeconds", f"{ide['meta']['cpu_seconds']:.2f}")

# ---- datasets table
with open(os.path.join(OUT, "table_datasets.tex"), "w") as fh:
    # complete tabular: \input of row files does not work inside a tabular with a p{} column
    fh.write(r"\begin{tabular}{lrrrrp{0.46\linewidth}}" + "\n" + r"\toprule" + "\n")
    fh.write(r"dataset & $n$ & $d$ & $K$ & Bayes err.\ (\%) & description\\" + "\n" + r"\midrule" + "\n")
    for ds, info in res["datasets"].items():
        be = "--" if info.get("bayes_error") is None else pct(info["bayes_error"], 1)
        note = {"iris": "Fisher's iris", "wine": "UCI wine", "breast_cancer": "Wisconsin diagnostic",
                "digits": "UCI optical digits, PCA to 20 comp.",
                "synth_informative": "\\texttt{make\\_classification}: 5 inf.\\ + 3 red.\\ + 2 noise, 2 clusters/class, 3\\% label noise",
                "moons_aniso": "two moons + anisotropic noise (sd $0.30\\times0.06$, $30^\\circ$) + 3 nuisance dims",
                "synth_classcov": "two Gaussians, $d=6$, rotated class-specific covariances",
                "synth_lda": "three Gaussians, $d=6$, one shared covariance"}[ds]
        fh.write(f"{DS_NAME[ds]} & {info['n']} & {info['d_used']} & {info['n_classes']} & {be} & {note} \\\\\n")
    fh.write(r"\bottomrule" + "\n" + r"\end{tabular}" + "\n")
shifts = {ds: info.get("shift") for ds, info in res["datasets"].items()}
if any(v is None for ds, v in shifts.items() if res["datasets"][ds].get("bayes_error") is not None):
    # results.json produced before the shift was exported: replay the deterministic generator
    import sys
    sys.path.insert(0, HERE)
    from selective_benchmark import make_datasets, SEED
    D = make_datasets(SEED)
    for ds in shifts:
        if ds in D and "shift" in D[ds]:
            shifts[ds] = D[ds]["shift"]
for ds, info in res["datasets"].items():
    if info.get("bayes_error") is not None:
        mac(f"Bayes{DS_TAG[ds]}", pct(info["bayes_error"], 1))
        mac(f"Shift{DS_TAG[ds]}", f"{shifts[ds]:.2f}")
    mac(f"N{DS_TAG[ds]}", info["n"])

# ---- per dataset / method macros and tables
for ds in S:
    t = DS_TAG[ds]
    for m in S[ds]["methods"]:
        v = S[ds]["methods"][m]
        mac(f"Aurc{t}{M_TAG[m]}", pct(v["aurc_mean"]))
        mac(f"AurcSd{t}{M_TAG[m]}", pct(v["aurc_sd"]))
        mac(f"Acc{t}{M_TAG[m]}", pct(v["acc_mean"], 1))
        mac(f"AccNinety{t}{M_TAG[m]}", pct(v["acc90_mean"], 1))
        mac(f"AccEighty{t}{M_TAG[m]}", pct(v["acc80_mean"], 1))
        mac(f"Err{t}{M_TAG[m]}", pct(v["error_rate"], 1))
    br = S[ds]["best_reference"]
    mac(f"BestRef{t}", M_NAME[br])
    mac(f"BestRefAurc{t}", pct(S[ds]["methods"][br]["aurc_mean"]))
    for f in FIELDS:
        c = S[ds]["comparisons"][f]["__best__"]
        mac(f"Diff{t}{M_TAG[f]}", spct(c["mean_diff"]))
        mac(f"DiffLo{t}{M_TAG[f]}", spct(c["ci_lo"]))
        mac(f"DiffHi{t}{M_TAG[f]}", spct(c["ci_hi"]))
        mac(f"DiffP{t}{M_TAG[f]}", f"{c['wilcoxon_p']:.3f}")
        mac(f"DiffWins{t}{M_TAG[f]}", c["wins"])

with open(os.path.join(OUT, "table_aurc_refs.tex"), "w") as fh:
    for ds in S:
        best = S[ds]["best_reference"]
        cells = []
        for m in REFS:
            v = S[ds]["methods"][m]
            cell = f"{pct(v['aurc_mean'])}"
            cells.append(rf"\textbf{{{cell}}}" if m == best else cell)
        err = S[ds]["methods"][best]["error_rate"]
        fh.write(f"{DS_NAME[ds]} & " + " & ".join(cells) + f" & {pct(err, 1)} \\\\\n")

with open(os.path.join(OUT, "table_aurc_field.tex"), "w") as fh:
    for ds in S:
        best = S[ds]["best_reference"]
        cells = []
        for m in FIELDS:
            v = S[ds]["methods"][m]
            cells.append(f"{pct(v['aurc_mean'])}")
        fh.write(f"{DS_NAME[ds]} & {M_NAME[best]} & {pct(S[ds]['methods'][best]['aurc_mean'])} & " + " & ".join(cells) + " \\\\\n")

with open(os.path.join(OUT, "table_diff.tex"), "w") as fh:
    for ds in S:
        best = S[ds]["best_reference"]
        cells = []
        for f in ["Field-aniso", "Field-iso", "Field-euclid"]:
            c = S[ds]["comparisons"][f]["__best__"]
            cells.append(f"{spct(c['mean_diff'])} [{spct(c['ci_lo'])}, {spct(c['ci_hi'])}] & {c['wins']}/{S[ds]['n_folds']}")
        fh.write(f"{DS_NAME[ds]} & {M_NAME[best]} & " + " & ".join(cells) + " \\\\\n")

ABL_KEYS = ["Field-aniso - Field-iso", "Field-aniso - Field-euclid", "Field-euclid - NCM",
            "Field-aniso - Field-vol", "Field-aniso - Field-anis", "Field-aniso - Field-aniso-gproto"]
with open(os.path.join(OUT, "table_ablation.tex"), "w") as fh:
    for ds in S:
        cells = []
        for k in ABL_KEYS:
            a = S[ds]["ablations"][k]
            cell = f"{spct(a['mean_diff'])}"
            if a["ci_hi"] < 0:
                cell = rf"\textbf{{{cell}}}"
            elif a["ci_lo"] > 0:
                cell = rf"\textit{{{cell}}}"
            cells.append(cell)
        fh.write(f"{DS_NAME[ds]} & " + " & ".join(cells) + " \\\\\n")
for k, tag in [("Field-aniso - Field-iso", "AnisoIso"), ("Field-aniso - Field-euclid", "AnisoEuclid"),
               ("Field-euclid - NCM", "EuclidNcm"), ("Field-aniso - Field-vol", "AnisoVol"),
               ("Field-aniso - Field-aniso-gproto", "AnisoGproto"), ("Field-aniso - kNN", "AnisoKnn"),
               ("Field-aniso - LDA", "AnisoLda"), ("Field-aniso - DANN", "AnisoDann")]:
    first = [ds for ds in S if S[ds]["ablations"][k]["ci_hi"] < 0]
    second = [ds for ds in S if S[ds]["ablations"][k]["ci_lo"] > 0]
    mac(f"Abl{tag}First", len(first))
    mac(f"Abl{tag}Second", len(second))
    mac(f"Abl{tag}FirstList", ", ".join(DS_NAME[d] for d in first) if first else "none")
    mac(f"Abl{tag}SecondList", ", ".join(DS_NAME[d] for d in second) if second else "none")

with open(os.path.join(OUT, "table_acc.tex"), "w") as fh:
    for ds in S:
        best = S[ds]["best_reference"]
        cells = []
        for m in [best, "Field-aniso", "Field-iso"]:
            v = S[ds]["methods"][m]
            cells.append(f"{pct(v['acc_mean'], 1)} & {pct(v['acc90_mean'], 1)} & {pct(v['acc80_mean'], 1)}")
        fh.write(f"{DS_NAME[ds]} & {M_NAME[best]} & " + " & ".join(cells) + " \\\\\n")

# geometry-only scores against the error rate of their own predictions
with open(os.path.join(OUT, "table_geom.tex"), "w") as fh:
    for ds in S:
        cells = []
        for m in ["Field-aniso", "Field-vol", "Field-anis"]:
            v = S[ds]["methods"][m]
            cell = pct(v["aurc_mean"])
            if v["aurc_mean"] >= v["error_rate"]:
                cell = rf"\textit{{{cell}}}"
            cells.append(f"{pct(v['error_rate'], 1)} & {cell}")
        fh.write(f"{DS_NAME[ds]} & " + " & ".join(cells) + " \\\\\n")
for m, tag in [("Field-vol", "Vol"), ("Field-anis", "Anis"), ("Field-aniso", "Margin")]:
    above = sum(1 for ds in S if S[ds]["methods"][m]["aurc_mean"] >= S[ds]["methods"][m]["error_rate"])
    half = sum(1 for ds in S if S[ds]["methods"][m]["aurc_mean"] >= 0.5 * S[ds]["methods"][m]["error_rate"])
    mac(f"Geom{tag}AboveRandom", above)
    mac(f"Geom{tag}AboveHalf", half)
    mac(f"Geom{tag}AboveRandomList", ", ".join(DS_NAME[ds] for ds in S if S[ds]["methods"][m]["aurc_mean"] >= S[ds]["methods"][m]["error_rate"]) or "none")

# ---- criterion
for f in FIELDS:
    c = res["criterion"][f]
    mac(f"Crit{M_TAG[f]}Better", len(c["better"]))
    mac(f"Crit{M_TAG[f]}Worse", len(c["worse"]))
    mac(f"Crit{M_TAG[f]}Incon", len(c["inconclusive"]))
    mac(f"Crit{M_TAG[f]}BetterList", ", ".join(DS_NAME[d] for d in c["better"]) if c["better"] else "none")
    mac(f"Crit{M_TAG[f]}WorseList", ", ".join(DS_NAME[d] for d in c["worse"]) if c["worse"] else "none")
    mac(f"Crit{M_TAG[f]}InconList", ", ".join(DS_NAME[d] for d in c["inconclusive"]) if c["inconclusive"] else "none")
    mac(f"Crit{M_TAG[f]}Met", "met" if c["criterion_met"] else "not met")

# how often Field-aniso beats each reference individually (CI excluding 0)
for r in REFS:
    n_better = sum(1 for ds in S if S[ds]["comparisons"]["Field-aniso"][r]["ci_hi"] < 0)
    n_worse = sum(1 for ds in S if S[ds]["comparisons"]["Field-aniso"][r]["ci_lo"] > 0)
    mac(f"VsRef{M_TAG[r]}Better", n_better)
    mac(f"VsRef{M_TAG[r]}Worse", n_worse)
with open(os.path.join(OUT, "table_vsrefs.tex"), "w") as fh:
    for ds in S:
        cells = []
        for r in REFS:
            c = S[ds]["comparisons"]["Field-aniso"][r]
            cell = spct(c["mean_diff"])
            if c["ci_hi"] < 0:
                cell = rf"\textbf{{{cell}}}"
            elif c["ci_lo"] > 0:
                cell = rf"\textit{{{cell}}}"
            cells.append(cell)
        fh.write(f"{DS_NAME[ds]} & " + " & ".join(cells) + " \\\\\n")

for ds in S:
    best = S[ds]["best_reference"]
    gap = S[ds]["methods"][best]["acc_mean"] - S[ds]["methods"]["Field-aniso"]["acc_mean"]
    mac(f"AccGap{DS_TAG[ds]}", f"{100 * gap:.1f}")
acc_worse = [ds for ds in S if S[ds]["methods"][S[ds]["best_reference"]]["acc_mean"] - S[ds]["methods"]["Field-aniso"]["acc_mean"] >= 0.01]
mac("AccGapBigList", ", ".join(DS_NAME[d] for d in acc_worse) if acc_worse else "none")
mac("AccGapBigN", len(acc_worse))
acc_better = [ds for ds in S if S[ds]["methods"]["Field-aniso"]["acc_mean"] > S[ds]["methods"][S[ds]["best_reference"]]["acc_mean"]]
mac("AccBetterList", ", ".join(DS_NAME[d] for d in acc_better) if acc_better else "none")
mac("AccBetterN", len(acc_better))

# largest / smallest gap to the best reference for Field-aniso
gaps = {ds: S[ds]["comparisons"]["Field-aniso"]["__best__"]["mean_diff"] for ds in S}
worst = max(gaps, key=gaps.get)
closest = min(gaps, key=gaps.get)
mac("GapWorstDs", DS_NAME[worst])
mac("GapWorst", spct(gaps[worst]))
mac("GapClosestDs", DS_NAME[closest])
mac("GapClosest", spct(gaps[closest]))

# selected hyper-parameters of Field-aniso (pooled over datasets and folds)
alpha_cnt, km_cnt, tot = {}, {}, 0
for ds in S:
    for k, c in S[ds]["methods"]["Field-aniso"]["selected_params"].items():
        p = json.loads(k)
        alpha_cnt[p["alpha"]] = alpha_cnt.get(p["alpha"], 0) + c
        km_cnt[p["K_m"]] = km_cnt.get(p["K_m"], 0) + c
        tot += c
ALPHA_W = {0.05: "Low", 0.2: "Mid", 0.5: "High"}
KM_W = {20: "Twenty", 40: "Forty", 80: "Eighty"}
for a in ALPHA_W:
    mac(f"AlphaFrac{ALPHA_W[a]}", f"{100 * alpha_cnt.get(a, 0) / tot:.0f}")
for k in KM_W:
    mac(f"KmFrac{KM_W[k]}", f"{100 * km_cnt.get(k, 0) / tot:.0f}")
mac("AlphaTotal", tot)

# ---- identity (Proposition 1) macros
k2 = ide["K2_equal_priors"]
mac("IdD", ide["meta"]["d"])
mac("IdN", ide["meta"]["n"])
mac("IdKtwoSpearman", f"{k2['spearman_s_m']:.6f}")
mac("IdKtwoMaxDev", sci(k2["max_abs_m_minus_tanh"]))
mac("IdKtwoAurcDiff", sci(k2["aurc_abs_diff"]) if k2["aurc_abs_diff"] > 0 else "0")
mac("IdKtwoErr", pct(k2["error_rate"], 2))
mac("IdKtwoMonotone", "yes" if k2["monotone"] else "no")
ku = ide["K2_unequal_priors"]
mac("IdUneqPriorA", f"{ku['priors'][0]:.1f}")
mac("IdUneqPriorB", f"{ku['priors'][1]:.1f}")
mac("IdUneqSpearman", f"{ku['spearman_s_m']:.4f}")
mac("IdUneqFrac", pct(ku["frac_predictions_differ"], 2))
mac("IdUneqMonotone", "yes" if ku["monotone"] else "no")
mac("IdUneqCorrectedMonotone", "yes" if ku["corrected_monotone"] else "no")
mac("IdUneqCorrectedDev", sci(ku["corrected_max_abs_m_minus_tanh"]))
mac("IdUneqAurcS", sci(ku["aurc_s_with_own_predictions"], 2))
mac("IdUneqAurcM", sci(ku["aurc_m"], 2))
k3 = ide["K3_sample"]
mac("IdKthreeMaxDev", sci(k3["max_abs_s_minus_two_log_ratio"]))
mac("IdKthreeSpearTop", f"{k3['spearman_s_top2']:.4f}")
mac("IdKthreeSpearMsp", f"{k3['spearman_s_msp']:.4f}")
mac("IdKthreeAurcS", pct(k3["aurc_s"], 3))
mac("IdKthreeAurcTop", pct(k3["aurc_top2"], 3))
mac("IdKthreeAurcMsp", pct(k3["aurc_msp"], 3))
mac("IdKthreeErr", pct(k3["error_rate"], 1))
mac("IdKthreeMonoTop", "yes" if k3["monotone_in_top2_diff"] else "no")
mac("IdKthreeMonoMsp", "yes" if k3["monotone_in_msp"] else "no")
mac("IdKthreeMonoLr", "yes" if k3["monotone_in_log_ratio"] else "no")
cx = ide["K3_counterexample"]
mac("CexSA", f"{cx['score_s'][0]:.4g}")
mac("CexSB", f"{cx['score_s'][1]:.4g}")
mac("CexMA", f"{cx['top2_diff'][0]:.3f}")
mac("CexMB", f"{cx['top2_diff'][1]:.3f}")
mac("CexMspA", f"{cx['max_posterior'][0]:.3f}")
mac("CexMspB", f"{cx['max_posterior'][1]:.3f}")
mac("CexLrA", f"{cx['two_log_ratio'][0]:.4g}")
mac("CexLrB", f"{cx['two_log_ratio'][1]:.4g}")
mac("CexDtwoA", ", ".join(f"{v:.4g}" for v in cx["d2"][0]))
mac("CexDtwoB", ", ".join(f"{v:.4g}" for v in cx["d2"][1]))
iso = ide["iso_rescaling_example"]
mac("IsoSi", f"{iso['s_i']:.2f}")
mac("IsoSj", f"{iso['s_j']:.2f}")
mac("IsoLam", f"{iso['lambda_i']:.2f}")
mac("IsoRescaledI", f"{iso['rescaled_i']:.2f}")


# Strip the final row terminator of every row-body table: a "\\\\" at the very end of an
# \input file breaks the following \bottomrule (main.tex supplies it as \input{...}\\\\).
import glob
for t in glob.glob(os.path.join(OUT, "table_*.tex")):
    if t.endswith("table_datasets.tex"):
        continue  # complete tabular, not a row body
    body = open(t).read().rstrip()
    if body.endswith("\\\\"):
        body = body[:-2].rstrip()
    open(t, "w").write(body + "\n")

with open(os.path.join(OUT, "numbers.tex"), "w") as fh:
    fh.write("% generated by experiments/make_numbers.py -- do not edit\n")
    fh.write("\n".join(L) + "\n")
print(f"wrote {len(L)} macros and tables to {OUT}")
