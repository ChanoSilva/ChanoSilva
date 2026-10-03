#!/usr/bin/env python3
"""Turn results/results.json, results/results_identity.json and (if present) results/results_v01.json
into LaTeX macros (manuscript/numbers.tex) and table bodies (manuscript/table_*.tex). No number in
main.tex is typed by hand.

v0.2: every paired comparison carries three 95% intervals (percentile bootstrap over folds -- the
predefined one --, Student t over folds, Nadeau-Bengio corrected t), wins/ties/losses and a borderline
flag (an end of the bootstrap or t interval within 0.02 of zero, AURC x 100). In the marked tables a
cell is bold/italic only when BOTH the bootstrap and the t interval exclude zero; a superscript b (t)
marks a cell where only the bootstrap (only the t) interval does; a superscript circle marks a
borderline cell.

v0.3: the main JSON is the v0.3 run (widened field grid, PREREGISTRO_HQF001_rejilla_20261003.md); the
v0.2 run (predefined grid) is read from results/v02/results.json and exported with the prefix VTwo.
Ablation counts are given under the three readings and, separately, without the borderline pairs
(R2-M1); ranges run over the three readings; grid-edge saturation and geometry-only ratios are exported;
ties in text lists are broken by dataset name so that regeneration is byte-identical (R2-m11)."""
import glob
import json
import math
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
OUT = os.path.join(ROOT, "manuscript")
res = json.load(open(os.path.join(ROOT, "results", "results.json")))
ide = json.load(open(os.path.join(ROOT, "results", "results_identity.json")))
V01 = os.path.join(ROOT, "results", "results_v01.json")
v01 = json.load(open(V01)) if os.path.exists(V01) else None
V02 = os.path.join(ROOT, "results", "v02", "results.json")
v02 = json.load(open(V02)) if os.path.exists(V02) else None
SPEC = os.path.join(ROOT, "results", "results_spectrum.json")
spec = json.load(open(SPEC)) if os.path.exists(SPEC) else None
sys.path.insert(0, HERE)
from selective_benchmark import grid_saturation  # noqa: E402

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
CRIT = res["criterion"]
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
    s = f"{100 * x:+.{d}f}"
    if float(s) == 0.0:          # rounds to zero at d decimals: print three decimals instead (m9)
        s = f"{100 * x:+.3f}"
    return s


def ci(c, kind):
    lo, hi = {"boot": ("ci_lo", "ci_hi"), "t": ("t_lo", "t_hi"), "nb": ("nb_lo", "nb_hi")}[kind]
    return f"[{spct(c[lo])}, {spct(c[hi])}]"


def wtl(c):
    return f"{c['wins']}/{c['ties']}/{c['losses']}"


def mark(c, first, second, cell):
    """bold: both intervals favour the first; italic: both favour the second; ^b / ^t: only one of them
    excludes zero; ^circ: borderline."""
    vb, vt = c["verdict"], c["verdict_t"]
    sup = ""
    if vb == first and vt == first:
        cell = rf"\textbf{{{cell}}}"
    elif vb == second and vt == second:
        cell = rf"\textit{{{cell}}}"
    elif vb != "inconclusive":
        sup += "b"
    elif vt != "inconclusive":
        sup += "t"
    if c["borderline"]:
        sup += r"\circ"
    return rf"{cell}$^{{{sup}}}$" if sup else cell


def yes(b):
    return "yes" if b else "no"


def rng_str(*vals):
    """'a' if all values are equal, else 'min--max' (v0.3: over any number of readings)."""
    return f"{vals[0]}" if min(vals) == max(vals) else f"{min(vals)}--{max(vals)}"


def names(lst):
    return ", ".join(DS_NAME[d] for d in lst) if lst else "none"


# ---- meta
mac("MetaVersion", meta.get("script_version", "v0.1"))
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
mac("MetaBootB", f"{meta['bootstrap_B']:,}".replace(",", r"\,"))
mac("MetaRho", f"{meta.get('nb_rho', 1.0 / (meta['n_splits'] - 1)):.2f}")
mac("MetaNDatasets", len(S))
mac("MetaMajority", len(S) // 2 + 1)
mac("MetaNRefs", len(REFS))
mac("MetaNFields", len(FIELDS))
mac("IdCpuSeconds", f"{ide['meta']['cpu_seconds']:.2f}")

# ---- datasets table (complete tabular: \input of row files does not work inside a tabular with a p{} column)
with open(os.path.join(OUT, "table_datasets.tex"), "w") as fh:
    fh.write(r"\begin{tabular}{lrrrrp{0.46\linewidth}}" + "\n" + r"\toprule" + "\n")
    fh.write(r"dataset & $n$ & $d$ & $K$ & Bayes err.\ (\%) & description\\" + "\n" + r"\midrule" + "\n")
    for ds, info in res["datasets"].items():
        be = "--" if info.get("bayes_error") is None else pct(info["bayes_error"], 1)
        sh = info.get("shift")
        note = {"iris": "Fisher's iris", "wine": "UCI wine", "breast_cancer": "Wisconsin diagnostic",
                "digits": "UCI optical digits, PCA to 20 comp.",
                "synth_informative": "\\texttt{make\\_classification}: 5 inf.\\ + 3 red.\\ + 2 noise, 2 clusters/class, 3\\% label noise",
                "moons_aniso": "two moons + anisotropic noise (sd $0.30\\times0.06$, $30^\\circ$) + 3 nuisance dims",
                "synth_classcov": f"two Gaussians, $d=6$, rotated class-specific covariances (spectrum $2\\to0.25$), mean shift {sh:.2f}" if sh is not None else "two Gaussians, $d=6$, rotated class-specific covariances",
                "synth_lda": f"three Gaussians, $d=6$, one shared covariance (spectrum $2\\to0.05$), mean shift {sh:.2f}" if sh is not None else "three Gaussians, $d=6$, one shared covariance"}[ds]
        fh.write(f"{DS_NAME[ds]} & {info['n']} & {info['d_used']} & {info['n_classes']} & {be} & {note} \\\\\n")
    fh.write(r"\bottomrule" + "\n" + r"\end{tabular}" + "\n")
for ds, info in res["datasets"].items():
    if info.get("bayes_error") is not None:
        mac(f"Bayes{DS_TAG[ds]}", pct(info["bayes_error"], 1))
        mac(f"Shift{DS_TAG[ds]}", f"{info['shift']:.2f}" if info.get("shift") is not None else "--")
        mac(f"ShiftAtBound{DS_TAG[ds]}", yes(info.get("shift_at_bound")))
    mac(f"N{DS_TAG[ds]}", info["n"])
    mac(f"TestSize{DS_TAG[ds]}", info["n"] // meta["n_splits"])

# ---- per dataset / method macros
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
        ft = M_TAG[f]
        mac(f"Diff{t}{ft}", spct(c["mean_diff"]))
        mac(f"DiffLo{t}{ft}", spct(c["ci_lo"]))
        mac(f"DiffHi{t}{ft}", spct(c["ci_hi"]))
        mac(f"DiffBoot{t}{ft}", ci(c, "boot"))
        mac(f"DiffT{t}{ft}", ci(c, "t"))
        mac(f"DiffNb{t}{ft}", ci(c, "nb"))
        mac(f"DiffP{t}{ft}", f"{c['wilcoxon_p']:.3f}")
        mac(f"DiffWins{t}{ft}", c["wins"])
        mac(f"DiffTies{t}{ft}", c["ties"])
        mac(f"DiffLosses{t}{ft}", c["losses"])
        mac(f"DiffWtl{t}{ft}", wtl(c))
        mac(f"DiffBorder{t}{ft}", yes(c["borderline"]))

# folds in which the best reference has AURC exactly 0 (ties with the field are then frequent)
for ds in S:
    br = S[ds]["best_reference"]
    z = sum(1 for f in res["per_fold"][ds] if f[br]["aurc"] == 0.0)
    mac(f"ZeroFolds{DS_TAG[ds]}", z)

# ---- Table: AURC of references and field variants in one table
with open(os.path.join(OUT, "table_aurc_all.tex"), "w") as fh:
    for ds in S:
        best = S[ds]["best_reference"]
        cells = []
        for m in REFS:
            cell = pct(S[ds]["methods"][m]["aurc_mean"])
            cells.append(rf"\textbf{{{cell}}}" if m == best else cell)
        cells.append(pct(S[ds]["methods"][best]["error_rate"], 1))
        for m in FIELDS:
            cells.append(pct(S[ds]["methods"][m]["aurc_mean"]))
        fh.write(f"{DS_NAME[ds]} & " + " & ".join(cells) + " \\\\\n")

# ---- Table: anisotropic field vs best reference, three intervals, W/T/L, Wilcoxon p
with open(os.path.join(OUT, "table_diff.tex"), "w") as fh:
    for ds in S:
        c = S[ds]["comparisons"]["Field-aniso"]["__best__"]
        delta = spct(c["mean_diff"]) + (r"$^{\circ}$" if c["borderline"] else "")
        fh.write(f"{DS_NAME[ds]} & {delta} & {ci(c, 'boot')} & {ci(c, 't')} & {ci(c, 'nb')} & {wtl(c)} & {c['wilcoxon_p']:.3f} \\\\\n")

# ---- Table (appendix): isotropic and Euclidean ablations vs best reference
with open(os.path.join(OUT, "table_diff_abl.tex"), "w") as fh:
    for ds in S:
        cells = []
        for f in ["Field-iso", "Field-euclid"]:
            c = S[ds]["comparisons"][f]["__best__"]
            delta = spct(c["mean_diff"]) + (r"$^{\circ}$" if c["borderline"] else "")
            cells.append(f"{delta} & {ci(c, 'boot')} & {ci(c, 't')} & {wtl(c)}")
        fh.write(f"{DS_NAME[ds]} & {M_NAME[S[ds]['best_reference']]} & " + " & ".join(cells) + " \\\\\n")

# ---- Table: anisotropic field against each reference (marked means)
with open(os.path.join(OUT, "table_vsrefs.tex"), "w") as fh:
    for ds in S:
        cells = [mark(S[ds]["comparisons"]["Field-aniso"][r], "field better", "field worse",
                      spct(S[ds]["comparisons"]["Field-aniso"][r]["mean_diff"])) for r in REFS]
        fh.write(f"{DS_NAME[ds]} & " + " & ".join(cells) + " \\\\\n")
for ds in S:
    for r in REFS:
        c = S[ds]["comparisons"]["Field-aniso"][r]
        mac(f"Vs{DS_TAG[ds]}{M_TAG[r]}", f"{spct(c['mean_diff'])} {ci(c, 'boot')}")
        mac(f"VsT{DS_TAG[ds]}{M_TAG[r]}", ci(c, "t"))
        mac(f"VsWtl{DS_TAG[ds]}{M_TAG[r]}", wtl(c))
for r in REFS:
    cs = {ds: S[ds]["comparisons"]["Field-aniso"][r] for ds in S}
    mac(f"VsRef{M_TAG[r]}Better", sum(1 for c in cs.values() if c["verdict"] == "field better"))
    mac(f"VsRef{M_TAG[r]}Worse", sum(1 for c in cs.values() if c["verdict"] == "field worse"))
    mac(f"VsRef{M_TAG[r]}BetterT", sum(1 for c in cs.values() if c["verdict_t"] == "field better"))
    mac(f"VsRef{M_TAG[r]}WorseT", sum(1 for c in cs.values() if c["verdict_t"] == "field worse"))
    mac(f"VsRef{M_TAG[r]}BetterBoth", sum(1 for c in cs.values() if c["verdict"] == "field better" and c["verdict_t"] == "field better"))
    mac(f"VsRef{M_TAG[r]}WorseBoth", sum(1 for c in cs.values() if c["verdict"] == "field worse" and c["verdict_t"] == "field worse"))
    mac(f"VsRef{M_TAG[r]}BetterList", names([ds for ds in S if cs[ds]["verdict"] == "field better"]))
    mac(f"VsRef{M_TAG[r]}BetterListT", names([ds for ds in S if cs[ds]["verdict_t"] == "field better"]))
vs_border = [f"{DS_NAME[ds]} vs {M_NAME[r]}" for ds in S for r in REFS if S[ds]["comparisons"]["Field-aniso"][r]["borderline"]]
mac("VsRefBorderList", "; ".join(vs_border) if vs_border else "none")
mac("VsRefBorderN", len(vs_border))
vs_bonly = [f"{DS_NAME[ds]} vs {M_NAME[r]}" for ds in S for r in REFS
            if S[ds]["comparisons"]["Field-aniso"][r]["verdict"] != "inconclusive" and S[ds]["comparisons"]["Field-aniso"][r]["verdict_t"] == "inconclusive"]
mac("VsRefBootOnlyList", "; ".join(vs_bonly) if vs_bonly else "none")
mac("VsRefBootOnlyN", len(vs_bonly))
mac("NVsRefCells", len(S) * len(REFS))

# ---- Table: ablations
ABL_KEYS = ["Field-aniso - Field-iso", "Field-aniso - Field-euclid", "Field-euclid - NCM",
            "Field-aniso - Field-vol", "Field-aniso - Field-anis", "Field-aniso - Field-aniso-gproto"]
ABL_TAG = {"Field-aniso - Field-iso": "AnisoIso", "Field-aniso - Field-euclid": "AnisoEuclid", "Field-euclid - NCM": "EuclidNcm",
           "Field-aniso - Field-vol": "AnisoVol", "Field-aniso - Field-anis": "AnisoAnis", "Field-aniso - Field-aniso-gproto": "AnisoGproto"}
ABL_NAME = {"Field-aniso - Field-iso": "aniso$-$iso", "Field-aniso - Field-euclid": "aniso$-$Eucl.", "Field-euclid - NCM": "Eucl.$-$NCM",
            "Field-aniso - Field-vol": "aniso$-$vol.", "Field-aniso - Field-anis": "aniso$-$anis.", "Field-aniso - Field-aniso-gproto": "aniso$-$glob.\\ prot."}
with open(os.path.join(OUT, "table_ablation.tex"), "w") as fh:
    for ds in S:
        a = S[ds]["ablations"][ABL_KEYS[0]]
        delta = spct(a["mean_diff"]) + (r"$^{\circ}$" if a["borderline"] else "")
        cells = [f"{delta} & {ci(a, 'boot')} & {ci(a, 't')} & {wtl(a)}"]
        for k in ABL_KEYS[1:]:
            a = S[ds]["ablations"][k]
            cells.append(mark(a, "first better", "second better", spct(a["mean_diff"])))
        fh.write(f"{DS_NAME[ds]} & " + " & ".join(cells) + " \\\\\n")
mac("NAblCells", len(S) * len(ABL_KEYS))
abl_border = []
for k in ABL_KEYS:
    tag = ABL_TAG[k]
    A = {ds: S[ds]["ablations"][k] for ds in S}
    fb = [ds for ds in S if A[ds]["verdict"] == "first better"]
    sb = [ds for ds in S if A[ds]["verdict"] == "second better"]
    ft = [ds for ds in S if A[ds]["verdict_t"] == "first better"]
    st = [ds for ds in S if A[ds]["verdict_t"] == "second better"]
    fn = [ds for ds in S if A[ds]["verdict_nb"] == "first better"]
    sn = [ds for ds in S if A[ds]["verdict_nb"] == "second better"]
    mac(f"Abl{tag}First", len(fb)); mac(f"Abl{tag}Second", len(sb))
    mac(f"Abl{tag}FirstList", names(fb)); mac(f"Abl{tag}SecondList", names(sb))
    mac(f"Abl{tag}FirstT", len(ft)); mac(f"Abl{tag}SecondT", len(st))
    mac(f"Abl{tag}FirstListT", names(ft)); mac(f"Abl{tag}SecondListT", names(st))
    mac(f"Abl{tag}FirstNB", len(fn)); mac(f"Abl{tag}SecondNB", len(sn))
    mac(f"Abl{tag}FirstListNB", names(fn)); mac(f"Abl{tag}SecondListNB", names(sn))
    mac(f"Abl{tag}FirstBoth", len([d for d in fb if d in ft])); mac(f"Abl{tag}SecondBoth", len([d for d in sb if d in st]))
    mac(f"Abl{tag}FirstRange", rng_str(len(fb), len(ft), len(fn))); mac(f"Abl{tag}SecondRange", rng_str(len(sb), len(st), len(sn)))
    # R2-M1: robust count = bootstrap and t both exclude zero and the pair is not borderline
    fr = [d for d in fb if d in ft and not A[d]["borderline"]]
    sr = [d for d in sb if d in st and not A[d]["borderline"]]
    fbd = [d for d in fb if d not in fr]   # counted 'better' by the bootstrap only, or borderline
    sbd = [d for d in sb if d not in sr]
    mac(f"Abl{tag}FirstRobust", len(fr)); mac(f"Abl{tag}FirstRobustList", names(fr))
    mac(f"Abl{tag}SecondRobust", len(sr)); mac(f"Abl{tag}SecondRobustList", names(sr))
    mac(f"Abl{tag}FirstWeak", len(fbd)); mac(f"Abl{tag}FirstWeakList", names(fbd))
    mac(f"Abl{tag}SecondWeak", len(sbd)); mac(f"Abl{tag}SecondWeakList", names(sbd))
    for ds in S:
        a = A[ds]
        mac(f"Abl{tag}{DS_TAG[ds]}", f"{spct(a['mean_diff'])} {ci(a, 'boot')}")
        mac(f"Abl{tag}T{DS_TAG[ds]}", ci(a, "t"))
        mac(f"Abl{tag}Wtl{DS_TAG[ds]}", wtl(a))
    fav = sorted(set(fb) | set(ft), key=lambda d: (-A[d]["wins"], A[d]["losses"], DS_NAME[d]))
    mac(f"Abl{tag}WinsText", ", ".join(f"{DS_NAME[d]} {wtl(A[d])}" for d in fav) if fav else "none")
    abl_border += [f"{DS_NAME[ds]} ({ABL_NAME[k]})" for ds in S if A[ds]["borderline"]]
mac("AblBorderList", "; ".join(abl_border) if abl_border else "none")
mac("AblBorderN", len(abl_border))

# ---- accuracy and geometry tables (appendix)
with open(os.path.join(OUT, "table_acc.tex"), "w") as fh:
    for ds in S:
        best = S[ds]["best_reference"]
        cells = []
        for m in [best, "Field-aniso", "Field-iso"]:
            v = S[ds]["methods"][m]
            cells.append(f"{pct(v['acc_mean'], 1)} & {pct(v['acc90_mean'], 1)} & {pct(v['acc80_mean'], 1)}")
        fh.write(f"{DS_NAME[ds]} & {M_NAME[best]} & " + " & ".join(cells) + " \\\\\n")
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
    above = [ds for ds in S if S[ds]["methods"][m]["aurc_mean"] >= S[ds]["methods"][m]["error_rate"]]
    half = sum(1 for ds in S if S[ds]["methods"][m]["aurc_mean"] >= 0.5 * S[ds]["methods"][m]["error_rate"])
    mac(f"Geom{tag}AboveRandom", len(above))
    mac(f"Geom{tag}AboveHalf", half)
    mac(f"Geom{tag}AboveRandomList", names(above))

# ---- criterion: predefined (bootstrap) and the same count under the t and Nadeau-Bengio intervals
for f in FIELDS:
    c = CRIT[f]
    ft = M_TAG[f]
    for suffix, cc in [("", c), ("T", c["t"]), ("NB", c["nb"])]:
        mac(f"Crit{ft}Better{suffix}", len(cc["better"]))
        mac(f"Crit{ft}Worse{suffix}", len(cc["worse"]))
        mac(f"Crit{ft}Incon{suffix}", len(cc["inconclusive"]))
        mac(f"Crit{ft}BetterList{suffix}", names(cc["better"]))
        mac(f"Crit{ft}WorseList{suffix}", names(cc["worse"]))
        mac(f"Crit{ft}InconList{suffix}", names(cc["inconclusive"]))
    mac(f"Crit{ft}Met", "met" if c["criterion_met"] else "not met")
    mac(f"Crit{ft}WorseRange", rng_str(len(c["worse"]), len(c["t"]["worse"]), len(c["nb"]["worse"])))
    mac(f"Crit{ft}BorderList", names(c["borderline"]))
    mac(f"Crit{ft}BorderN", len(c["borderline"]))

# ---- accuracy gaps, extreme gaps, selected hyper-parameters
for ds in S:
    best = S[ds]["best_reference"]
    gap = S[ds]["methods"][best]["acc_mean"] - S[ds]["methods"]["Field-aniso"]["acc_mean"]
    mac(f"AccGap{DS_TAG[ds]}", f"{100 * gap:.1f}")
acc_worse = [ds for ds in S if S[ds]["methods"][S[ds]["best_reference"]]["acc_mean"] - S[ds]["methods"]["Field-aniso"]["acc_mean"] >= 0.01]
mac("AccGapBigList", names(acc_worse))
mac("AccGapBigN", len(acc_worse))
mac("AccGapBigText", ", ".join(f"{100 * (S[d]['methods'][S[d]['best_reference']]['acc_mean'] - S[d]['methods']['Field-aniso']['acc_mean']):.1f} ({DS_NAME[d]})" for d in acc_worse) if acc_worse else "none")
acc_better = [ds for ds in S if S[ds]["methods"]["Field-aniso"]["acc_mean"] > S[ds]["methods"][S[ds]["best_reference"]]["acc_mean"]]
mac("AccBetterList", names(acc_better))
mac("AccBetterN", len(acc_better))
gaps = {ds: S[ds]["comparisons"]["Field-aniso"]["__best__"]["mean_diff"] for ds in S}
worst = max(gaps, key=gaps.get)
closest = min(gaps, key=gaps.get)
mac("GapWorstDs", DS_NAME[worst]); mac("GapWorst", spct(gaps[worst]))
mac("GapClosestDs", DS_NAME[closest]); mac("GapClosest", spct(gaps[closest]))
alpha_cnt, km_cnt, tot = {}, {}, 0
for ds in S:
    for k, c in S[ds]["methods"]["Field-aniso"]["selected_params"].items():
        p = json.loads(k)
        alpha_cnt[p["alpha"]] = alpha_cnt.get(p["alpha"], 0) + c
        km_cnt[p["K_m"]] = km_cnt.get(p["K_m"], 0) + c
        tot += c
FG = res["grids"]["Field-aniso"]
mac("AlphaFracText", ", ".join(f"$\\alpha={a:g}$ in {100 * alpha_cnt.get(a, 0) / tot:.0f}\\%" for a in FG["alpha"]))
mac("KmFracText", ", ".join(f"$K_m={k}$ in {100 * km_cnt.get(k, 0) / tot:.0f}\\%" for k in FG["K_m"]))
mac("FieldGridAlpha", ", ".join(f"{a:g}" for a in FG["alpha"]))
mac("FieldGridKm", ", ".join(f"{k}" for k in FG["K_m"]))
mac("AlphaTotal", tot)
dropped = [(m, ds, S[ds]["methods"][m].get("inner_configs_dropped", 0)) for ds in S for m in S[ds]["methods"] if S[ds]["methods"][m].get("inner_configs_dropped", 0)]
mac("DroppedConfigs", sum(d[2] for d in dropped))
mac("DroppedConfigsList", "; ".join(f"{M_NAME[m]} on {DS_NAME[ds]}: {n}" for m, ds, n in dropped) if dropped else "none")

# ---- synth-classcov as it was in v0.1 (coinciding means), recomputed from the stored v0.1 folds
if v01 is not None and "synth_classcov" in v01["per_fold"]:
    import numpy as np
    from scipy.stats import t as t_dist
    pf = v01["per_fold"]["synth_classcov"]
    s1 = v01["summary"]["synth_classcov"]
    mac("VOneBayesCcov", pct(v01["datasets"]["synth_classcov"]["bayes_error"], 1))
    mac("VOneBestRefCcov", M_NAME[s1["best_reference"]])
    for m in s1["methods"]:
        mac(f"VOneAurcCcov{M_TAG[m]}", pct(s1["methods"][m]["aurc_mean"]))
        mac(f"VOneErrCcov{M_TAG[m]}", pct(s1["methods"][m]["error_rate"], 1))
    def v01_pair(a, b, tag):
        d = np.array([f[a]["aurc"] - f[b]["aurc"] for f in pf])
        n = len(d); q = t_dist.ppf(0.975, n - 1); se = d.std(ddof=1) / np.sqrt(n)
        mac(f"VOne{tag}", spct(d.mean()))
        mac(f"VOne{tag}T", f"[{spct(d.mean() - q * se)}, {spct(d.mean() + q * se)}]")
        mac(f"VOne{tag}Wtl", f"{int((d < 0).sum())}/{int((d == 0).sum())}/{int((d > 0).sum())}")
    v01_pair("Field-aniso", s1["best_reference"], "DiffCcovFaniso")
    v01_pair("Field-aniso", "Field-iso", "AblAnisoIsoCcov")
    v01_pair("Field-aniso", "Field-euclid", "AblAnisoEuclidCcov")
    for r in ["kNN", "DANN", "RForest", "NCM", "LDA", "LogReg"]:
        v01_pair("Field-aniso", r, f"VsCcov{M_TAG[r]}")
    c1 = v01["criterion"]["Field-aniso"]
    mac("VOneCritFanisoBetter", len(c1["better"])); mac("VOneCritFanisoWorse", len(c1["worse"])); mac("VOneCritFanisoIncon", len(c1["inconclusive"]))
    mac("VOneCpuSeconds", int(round(v01["meta"]["cpu_seconds"])))
    mac("VOneAvailable", "yes")
else:
    mac("VOneAvailable", "no")

# ---- identity (Proposition 3.1 / 3.2) macros
k2 = ide["K2_equal_priors"]
mac("IdD", ide["meta"]["d"])
mac("IdN", ide["meta"]["n"])
mac("IdKtwoSpearman", f"{k2['spearman_s_m']:.6f}")
mac("IdKtwoMaxDev", sci(k2["max_abs_m_minus_tanh"]))
mac("IdKtwoAurcDiff", sci(k2["aurc_abs_diff"]) if k2["aurc_abs_diff"] > 0 else "0")
mac("IdKtwoErr", pct(k2["error_rate"], 2))
mac("IdKtwoMonotone", yes(k2["monotone"]))
ku = ide["K2_unequal_priors"]
mac("IdUneqPriorA", f"{ku['priors'][0]:.1f}")
mac("IdUneqPriorB", f"{ku['priors'][1]:.1f}")
mac("IdUneqSpearman", f"{ku['spearman_s_m']:.4f}")
mac("IdUneqFrac", pct(ku["frac_predictions_differ"], 2))
mac("IdUneqMonotone", yes(ku["monotone"]))
mac("IdUneqCorrectedMonotone", yes(ku["corrected_monotone"]))
mac("IdUneqCorrectedDev", sci(ku["corrected_max_abs_m_minus_tanh"]))
k3 = ide["K3_sample"]
mac("IdKthreeMaxDev", sci(k3["max_abs_s_minus_two_log_ratio"]))
mac("IdKthreeSpearTop", f"{k3['spearman_s_top2']:.4f}")
mac("IdKthreeSpearMsp", f"{k3['spearman_s_msp']:.4f}")
mac("IdKthreeAurcS", pct(k3["aurc_s"], 3))
mac("IdKthreeAurcTop", pct(k3["aurc_top2"], 3))
mac("IdKthreeAurcMsp", pct(k3["aurc_msp"], 3))
mac("IdKthreeErr", pct(k3["error_rate"], 1))
mac("IdKthreeMonoTop", yes(k3["monotone_in_top2_diff"]))
mac("IdKthreeMonoMsp", yes(k3["monotone_in_msp"]))
mac("IdKthreeMonoLr", yes(k3["monotone_in_log_ratio"]))
cx = ide["K3_counterexample"]
mac("CexSA", f"{cx['score_s'][0]:.4g}")
mac("CexMA", f"{cx['top2_diff'][0]:.3f}"); mac("CexMB", f"{cx['top2_diff'][1]:.3f}")
mac("CexMspA", f"{cx['max_posterior'][0]:.3f}"); mac("CexMspB", f"{cx['max_posterior'][1]:.3f}")
mac("CexDtwoA", ", ".join(f"{v:.4f}" for v in cx["d2"][0]))
mac("CexDtwoB", ", ".join(f"{v:.4f}" for v in cx["d2"][1]))
if "K3_unequal_priors_general_identity" in ide:
    g = ide["K3_unequal_priors_general_identity"]
    mac("IdGenPriors", ", ".join(f"{p:.1f}" for p in g["priors"]))
    mac("IdGenNaiveDev", f"{g['max_abs_s_minus_two_log_ratio']:.2f}")
    mac("IdGenDev", sci(g["max_abs_s_minus_prior_corrected_log_ratio"]))
    mac("IdGenFracCoincide", pct(g["frac_nearest_pair_is_top_posterior_pair"], 1))
if "local_prototype_decomposition" in ide:
    g = ide["local_prototype_decomposition"]
    mac("IdLocalResidual", sci(g["max_abs_residual"]))
    mac("IdLocalCases", g["n_cases"])

# Strip the final row terminator of every row-body table (main.tex supplies it as \input{...}\\).
for t in glob.glob(os.path.join(OUT, "table_*.tex")):
    if t.endswith("table_datasets.tex"):
        continue
    body = open(t).read().rstrip()
    if body.endswith("\\\\"):
        body = body[:-2].rstrip()
    open(t, "w").write(body + "\n")

with open(os.path.join(OUT, "numbers.tex"), "w") as fh:
    fh.write("% generated by experiments/make_numbers.py -- do not edit\n")
    fh.write("\n".join(L) + "\n")
print(f"wrote {len(L)} macros and tables to {OUT}")
