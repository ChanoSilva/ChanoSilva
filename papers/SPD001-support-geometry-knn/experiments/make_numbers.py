#!/usr/bin/env python3
"""Turn results/results.json and results/results_regime.json into LaTeX macros
(manuscript/numbers.tex) and table bodies (manuscript/table_*.tex). No number in
main.tex is typed by hand.

Besides the bootstrap summaries stored in the JSON, this script recomputes from the
per-fold accuracy lists (v0.2, after internal review round 1):
  * the 95% interval with the Nadeau-Bengio variance,
        mean +- t_{0.975,J-1} * sqrt((1/J + n_test/n_train) * var),
    for every paired comparison used in the text (macros Nb*, AblNb*, SelNb*, RegNb*);
  * the fraction of folds in which a chosen hyper-parameter sits at the upper end of
    its grid (macros FracKMax*, FracLamMax*);
  * a deterministic modal hyper-parameter (ties broken towards the smallest values),
    used for the hyper-parameter table instead of the stored mode.
"""
import json
import math
import os
from collections import Counter

import numpy as np
from scipy.stats import t as student_t

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
OUT = os.path.join(ROOT, "manuscript")
res = json.load(open(os.path.join(ROOT, "results", "results.json")))
reg = json.load(open(os.path.join(ROOT, "results", "results_regime.json")))

DS = {"iris": "Iris", "wine": "Wine", "breast_cancer": "Bc", "digits": "Digits", "swiss_roll": "Swiss",
      "moons": "Moons", "moons_noise10": "MoonsN", "spheres": "Spheres"}
DSNAME = {"iris": "iris", "wine": "wine", "breast_cancer": "breast cancer", "digits": "digits",
          "swiss_roll": "swiss roll", "moons": "moons", "moons_noise10": "moons+10 noise", "spheres": "spheres"}
ME = {"kNN": "Knn", "NFL": "Nfl", "HKNN": "Hknn", "LPH": "Lph", "LCD": "Lcd", "SD": "Sd",
      "TOD": "Tod", "TO": "To", "TD": "Td", "OD": "Od", "T": "T"}
METHODS = ["kNN", "NFL", "HKNN", "LPH", "LCD", "SD", "TOD", "TO", "TD", "OD", "T"]
REFS = ["kNN", "NFL", "HKNN", "LPH", "LCD", "SD"]
PNUM = {0: "Zero", 2: "Two", 5: "Five", 10: "Ten", 20: "Twenty"}
L = []


def mac(name, val):
    L.append(rf"\newcommand{{\{name}}}{{{val}}}")


def pct(x, nd=1):
    return f"{100 * x:.{nd}f}"


def signed(x, nd=1):
    return f"{100 * x:+.{nd}f}"


def ci(s, nd=1):
    return rf"${signed(s['mean'], nd)}$ [{signed(s['ci_low'], nd)}, {signed(s['ci_high'], nd)}]"


def pval(p):
    return "$<0.001$" if p < 0.001 else f"{p:.3f}"


# ------------------------------------------------------------ recomputed statistics
def nb_interval(a, b, n_splits):
    """Mean of the fold-level differences a - b and its 95% interval with the
    Nadeau-Bengio variance inflation 1/J + n_test/n_train (= 1/J + 1/(n_splits-1))."""
    dlt = np.asarray(a, float) - np.asarray(b, float)
    J = len(dlt)
    var = dlt.var(ddof=1)
    half = student_t.ppf(0.975, J - 1) * math.sqrt((1.0 / J + 1.0 / (n_splits - 1)) * var)
    mean = float(dlt.mean())
    return dict(mean=mean, lo=mean - half, hi=mean + half)


def nb_vs(DD, n, m1, m2, metric="acc"):
    d = DD[n]
    return nb_interval(d["methods"][m1][metric], d["methods"][m2][metric], d["n_splits"])


def nbci(s, nd=1):
    return rf"[{signed(s['lo'], nd)}, {signed(s['hi'], nd)}]"


def frac_at(DD, n, method, key, value):
    ps = DD[n]["methods"][method]["params"]
    return 100.0 * sum(p[key] == value for p in ps) / len(ps)


def params_mode(DD, n, method):
    """Most frequent hyper-parameter setting over folds; ties broken towards the
    smallest values (deterministic, unlike max(set(...), key=count))."""
    ps = [json.dumps(p, sort_keys=True) for p in DD[n]["methods"][method]["params"]]
    cnt = Counter(ps)
    top = max(cnt.values())
    tied = [json.loads(k) for k, v in cnt.items() if v == top]
    return min(tied, key=lambda p: tuple(p[kk] for kk in sorted(p)))


m = res["meta"]
mac("MetaSeed", m["seed"])
mac("MetaPython", m["python"])
mac("MetaNumpy", m["numpy"])
mac("MetaScipy", m["scipy"])
mac("MetaSklearn", m["sklearn"])
mac("MetaSecondsWall", int(round(m["seconds_wall"])))
mac("MetaSecondsCpu", int(round(m["seconds_cpu"])))
mac("MetaMinutesCpu", f"{m['seconds_cpu'] / 60:.1f}")
mac("MetaSplits", m["n_splits"])
mac("MetaRepeats", m["n_repeats"])
mac("MetaFolds", m["n_splits"] * m["n_repeats"])
mac("MetaBoot", f"{m['n_boot']:,}".replace(",", r"\,"))
mac("MetaCoverage", int(round(100 * m["coverage"])))
mac("MetaKgrid", ", ".join(str(k) for k in m["k_grid"]))
mac("MetaMgrid", ", ".join(str(k) for k in m["m_grid"]))
mac("MetaKnnGrid", ", ".join(str(k) for k in m["knn_grid"]))
mac("MetaLambdaGrid", ", ".join(str(k) for k in m["lambda_grid"]))
mac("MetaRidge", f"{m['ridge']:g}")
mac("MetaKMax", max(m["k_grid"]))
mac("MetaKnnKMax", max(m["knn_grid"]))
mac("MetaLambdaMax", f"{max(m['lambda_grid']):g}")

D = res["datasets"]
C = res["comparison"]
V = res["verdict"]
mac("NDatasets", V["n_datasets"])
mac("NRequired", V["required_wins"])
mac("NSigWins", len(V["significant_wins"]))
mac("NSigLosses", len(V["significant_losses"]))
mac("SigWinsList", ", ".join(DSNAME[n] for n in V["significant_wins"]) or "none")
mac("SigLossesList", ", ".join(DSNAME[n] for n in V["significant_losses"]) or "none")
mac("VerdictWord", "adds" if V["adds_information"] else "does not add")
mac("VerdictBool", "true" if V["adds_information"] else "false")

NBBEST, NBEACH, NBABL, NBSEL, FR, PM = {}, {}, {}, {}, {}, {}
for n in D:
    d = D[n]
    c = C[n]
    tag = DS[n]
    mac(f"N{tag}", d["n"])
    mac(f"Dim{tag}", d["d"])
    mac(f"Cls{tag}", d["classes"])
    for me in METHODS:
        mac(f"Acc{tag}{ME[me]}", pct(c["means"][me]))
        mac(f"Sd{tag}{ME[me]}", pct(c["sds"][me]))
        mac(f"Sel{tag}{ME[me]}", pct(c["sel_means"][me]))
        # optimism of the training-fold selection: leave-one-out (or resubstitution, for the
        # logit models) accuracy minus test accuracy, in points
        mac(f"Optim{tag}{ME[me]}", f"{100 * (float(np.mean(d['methods'][me]['loo'])) - c['means'][me]):.1f}")
    mac(f"BestRef{tag}", c["best_reference"])
    mac(f"AccBest{tag}", pct(c["means"][c["best_reference"]]))
    s = c["vs_best"]
    mac(f"DeltaBest{tag}", signed(s["mean"]))
    mac(f"DeltaBestTwo{tag}", signed(s["mean"], 2))
    mac(f"CiLoBest{tag}", signed(s["ci_low"]))
    mac(f"CiHiBest{tag}", signed(s["ci_high"]))
    mac(f"CiLoBestTwo{tag}", signed(s["ci_low"], 2))
    mac(f"CiHiBestTwo{tag}", signed(s["ci_high"], 2))
    mac(f"WinsBest{tag}", f"{s['wins']}/{s['losses']}/{s['ties']}")
    mac(f"NbPBest{tag}", pval(s["nb_p"]))
    # Nadeau-Bengio interval of the same differences
    nbv = nb_vs(D, n, "TOD", c["best_reference"])
    NBBEST[n] = nbv
    mac(f"NbLoBest{tag}", signed(nbv["lo"]))
    mac(f"NbHiBest{tag}", signed(nbv["hi"]))
    mac(f"NbLoBestTwo{tag}", signed(nbv["lo"], 2))
    mac(f"NbHiBestTwo{tag}", signed(nbv["hi"], 2))
    NBEACH[n] = {}
    for me in REFS:
        mac(f"DeltaVs{tag}{ME[me]}", signed(c["vs_each"][me]["mean"]))
        mac(f"CiLoVs{tag}{ME[me]}", signed(c["vs_each"][me]["ci_low"]))
        mac(f"CiHiVs{tag}{ME[me]}", signed(c["vs_each"][me]["ci_high"]))
        NBEACH[n][me] = nb_vs(D, n, "TOD", me)
        mac(f"NbLoVs{tag}{ME[me]}", signed(NBEACH[n][me]["lo"]))
        mac(f"NbHiVs{tag}{ME[me]}", signed(NBEACH[n][me]["hi"]))
    NBABL[n] = {}
    for me in ["TO", "TD", "OD", "T"]:
        mac(f"Abl{tag}{ME[me]}", signed(c["ablation"][me]["mean"]))
        mac(f"AblLo{tag}{ME[me]}", signed(c["ablation"][me]["ci_low"]))
        mac(f"AblHi{tag}{ME[me]}", signed(c["ablation"][me]["ci_high"]))
        NBABL[n][me] = nb_vs(D, n, "TOD", me)
        mac(f"AblNbLo{tag}{ME[me]}", signed(NBABL[n][me]["lo"]))
        mac(f"AblNbHi{tag}{ME[me]}", signed(NBABL[n][me]["hi"]))
    w = c["weights_mean"]["TOD"]
    mac(f"WT{tag}", f"{w['T']:.2f}")
    mac(f"WO{tag}", f"{w['O']:.2f}")
    mac(f"WD{tag}", f"{w['D']:.2f}")
    ss = c["sel_vs_best"]
    mac(f"SelDeltaBest{tag}", signed(ss["mean"]))
    mac(f"SelCiLo{tag}", signed(ss["ci_low"]))
    mac(f"SelCiHi{tag}", signed(ss["ci_high"]))
    NBSEL[n] = nb_vs(D, n, "TOD", c["best_reference"], "sel")
    mac(f"SelNbLo{tag}", signed(NBSEL[n]["lo"]))
    mac(f"SelNbHi{tag}", signed(NBSEL[n]["hi"]))
    # selective accuracy against the reference that is best *by selective accuracy*
    bs = c["sel_vs_best_by_sel"]
    mac(f"SelBySelRef{tag}", c["sel_best_reference_by_sel"])
    mac(f"SelBySelDelta{tag}", signed(bs["mean"]))
    mac(f"SelBySelLo{tag}", signed(bs["ci_low"]))
    mac(f"SelBySelHi{tag}", signed(bs["ci_high"]))
    # fraction of folds with the chosen hyper-parameter at the top of its grid
    FR[n] = dict(Tod=frac_at(D, n, "TOD", "k", max(m["k_grid"])),
                 Hknn=frac_at(D, n, "HKNN", "k", max(m["k_grid"])),
                 Knn=frac_at(D, n, "kNN", "k", max(m["knn_grid"])),
                 Lam=frac_at(D, n, "HKNN", "lambda_rel", max(m["lambda_grid"])))
    for key, val in FR[n].items():
        mac(f"Frac{'LamMax' if key == 'Lam' else 'KMax'}{tag}{'' if key == 'Lam' else key}", int(round(val)))
    # resolution of one test error in accuracy points (largest test fold)
    mac(f"FoldRes{tag}", f"{100.0 / math.ceil(d['n'] / d['n_splits']):.2f}")
    PM[n] = {me: params_mode(D, n, me) for me in METHODS}
    for me in METHODS:
        if PM[n][me] != c["params_mode"][me]:
            print(f"note: deterministic mode differs from stored mode for {n}/{me}: "
                  f"{PM[n][me]} vs {c['params_mode'][me]} (tie)")

# summaries across datasets
vals = [C[n]["vs_best"]["mean"] for n in D]
mac("DeltaBestMin", signed(min(vals)))
mac("DeltaBestMax", signed(max(vals)))
mac("DeltaBestAbsMax", pct(max(abs(v) for v in vals)))
mac("NDeltaWithinOne", sum(abs(v) < 0.01 for v in vals))
mac("NDeltaWithinHalf", sum(abs(v) < 0.005 for v in vals))
mac("NDeltaPositive", sum(v > 0 for v in vals))
mac("DeltaPositiveList", ", ".join(DSNAME[n] for n in D if C[n]["vs_best"]["mean"] > 0) or "none")
hk = [C[n]["vs_each"]["HKNN"]["mean"] for n in D]
mac("DeltaHknnMin", signed(min(hk)))
mac("DeltaHknnMax", signed(max(hk)))
mac("NHknnCiAboveZero", sum(C[n]["vs_each"]["HKNN"]["ci_low"] > 0 for n in D))
mac("NHknnCiBelowZero", sum(C[n]["vs_each"]["HKNN"]["ci_high"] < 0 for n in D))
lph = [C[n]["vs_each"]["LPH"]["mean"] for n in D]
mac("DeltaLphMin", signed(min(lph)))
mac("DeltaLphMax", signed(max(lph)))
mac("NLphCiAboveZero", sum(C[n]["vs_each"]["LPH"]["ci_low"] > 0 for n in D))
sd = [C[n]["vs_each"]["SD"]["mean"] for n in D]
mac("DeltaSdMin", signed(min(sd)))
mac("DeltaSdMax", signed(max(sd)))
mac("NSdCiAboveZero", sum(C[n]["vs_each"]["SD"]["ci_low"] > 0 for n in D))
knn = [C[n]["vs_each"]["kNN"]["mean"] for n in D]
mac("DeltaKnnMin", signed(min(knn)))
mac("DeltaKnnMax", signed(max(knn)))
mac("NKnnCiAboveZero", sum(C[n]["vs_each"]["kNN"]["ci_low"] > 0 for n in D))
mac("NKnnCiBelowZero", sum(C[n]["vs_each"]["kNN"]["ci_high"] < 0 for n in D))
for me in REFS:
    mac(f"N{ME[me]}NbAboveZero", sum(NBEACH[n][me]["lo"] > 0 for n in D))
    mac(f"N{ME[me]}NbBelowZero", sum(NBEACH[n][me]["hi"] < 0 for n in D))
for me, word in (("TO", "Depth"), ("TD", "Orth"), ("OD", "Tang")):
    a = [C[n]["ablation"][me]["mean"] for n in D]
    mac(f"Abl{word}Min", signed(min(a)))
    mac(f"Abl{word}Max", signed(max(a)))
    mac(f"NAbl{word}CiAboveZero", sum(C[n]["ablation"][me]["ci_low"] > 0 for n in D))
    mac(f"NAbl{word}CiBelowZero", sum(C[n]["ablation"][me]["ci_high"] < 0 for n in D))
    mac(f"Abl{word}ArgMax", DSNAME[max(D, key=lambda n: C[n]["ablation"][me]["mean"])])
    mac(f"NAbl{word}NbAboveZero", sum(NBABL[n][me]["lo"] > 0 for n in D))
    mac(f"NAbl{word}NbBelowZero", sum(NBABL[n][me]["hi"] < 0 for n in D))
    mac(f"Abl{word}NbAboveList", ", ".join(DSNAME[n] for n in D if NBABL[n][me]["lo"] > 0) or "none")
sel = [C[n]["sel_vs_best"]["mean"] for n in D]
mac("SelDeltaMin", signed(min(sel)))
mac("SelDeltaMax", signed(max(sel)))
mac("NSelCiAboveZero", sum(C[n]["sel_vs_best"]["ci_low"] > 0 for n in D))
mac("NSelCiBelowZero", sum(C[n]["sel_vs_best"]["ci_high"] < 0 for n in D))
mac("NSelNbAboveZero", sum(NBSEL[n]["lo"] > 0 for n in D))
mac("NSelNbBelowZero", sum(NBSEL[n]["hi"] < 0 for n in D))
selb = [C[n]["sel_vs_best_by_sel"]["mean"] for n in D]
mac("SelBySelDeltaMin", signed(min(selb)))
mac("SelBySelDeltaMax", signed(max(selb)))
mac("NSelBySelCiAboveZero", sum(C[n]["sel_vs_best_by_sel"]["ci_low"] > 0 for n in D))
mac("NSelBySelCiBelowZero", sum(C[n]["sel_vs_best_by_sel"]["ci_high"] < 0 for n in D))
mac("SelBySelBelowList", ", ".join(DSNAME[n] for n in D if C[n]["sel_vs_best_by_sel"]["ci_high"] < 0) or "none")
mac("SelBySelAboveList", ", ".join(DSNAME[n] for n in D if C[n]["sel_vs_best_by_sel"]["ci_low"] > 0) or "none")
wd = [C[n]["weights_mean"]["TOD"]["D"] for n in D]
wo = [C[n]["weights_mean"]["TOD"]["O"] for n in D]
wt = [C[n]["weights_mean"]["TOD"]["T"] for n in D]
mac("WDMin", f"{min(wd):.2f}")
mac("WDMax", f"{max(wd):.2f}")
mac("WOMin", f"{min(wo):.2f}")
mac("WOMax", f"{max(wo):.2f}")
mac("WTMin", f"{min(wt):.2f}")
mac("WTMax", f"{max(wt):.2f}")
# how many datasets have a local-support method (hull or feature line) as best reference
mac("NBestRefHull", sum(C[n]["best_reference"] in ("HKNN", "LPH", "NFL") for n in D))
mac("NBestRefKnn", sum(C[n]["best_reference"] == "kNN" for n in D))
mac("NBestRefLcd", sum(C[n]["best_reference"] == "LCD" for n in D))
mac("NBestRefSd", sum(C[n]["best_reference"] == "SD" for n in D))
best_refs = sorted(set(C[n]["best_reference"] for n in D))
mac("BestRefSet", ", ".join(best_refs))
# max accuracy gap between the best and the worst of {HKNN, LPH, TOD, TO, OD} per dataset
gaps = [max(C[n]["means"][x] for x in ("HKNN", "LPH", "TOD", "TO", "OD")) -
        min(C[n]["means"][x] for x in ("HKNN", "LPH", "TOD", "TO", "OD")) for n in D]
mac("HullFamilyMaxSpread", pct(max(gaps)))
# optimism ranges (leave-one-out minus test accuracy, points) for TOD and HKNN
for me in ("TOD", "HKNN"):
    opt = [100 * (float(np.mean(D[n]["methods"][me]["loo"])) - C[n]["means"][me]) for n in D]
    mac(f"Optim{ME[me]}Min", f"{min(opt):.1f}")
    mac(f"Optim{ME[me]}Max", f"{max(opt):.1f}")
# T-only and SD ranges
mac("AccTMin", pct(min(C[n]["means"]["T"] for n in D)))
mac("AccTMax", pct(max(C[n]["means"]["T"] for n in D)))
mac("AccTArgMin", DSNAME[min(D, key=lambda n: C[n]["means"]["T"])])

mac("CiHiBestMax", signed(max(C[n]["vs_best"]["ci_high"] for n in D)))
mac("CiHiBestMaxTwo", signed(max(C[n]["vs_best"]["ci_high"] for n in D), 2))
mac("CiHiBestMaxArg", DSNAME[max(D, key=lambda n: C[n]["vs_best"]["ci_high"])])
mac("CiHiBestMaxNb", signed(max(NBBEST[n]["hi"] for n in D)))
mac("CiHiBestMaxNbTwo", signed(max(NBBEST[n]["hi"] for n in D), 2))
mac("CiHiBestMaxNbArg", DSNAME[max(D, key=lambda n: NBBEST[n]["hi"])])
mac("NSigWinsNb", sum(NBBEST[n]["lo"] > 0 for n in D))
mac("NSigLossesNb", sum(NBBEST[n]["hi"] < 0 for n in D))
mac("CiHiHknnMax", signed(max(C[n]["vs_each"]["HKNN"]["ci_high"] for n in D)))
mac("CiHiLphMax", signed(max(C[n]["vs_each"]["LPH"]["ci_high"] for n in D)))
mac("AblDepthCiHiMax", signed(max(C[n]["ablation"]["TO"]["ci_high"] for n in D)))
mac("AblTangCiHiMax", signed(max(C[n]["ablation"]["OD"]["ci_high"] for n in D)))
mac("AblDepthNbHiMax", signed(max(NBABL[n]["TO"]["hi"] for n in D)))
mac("AblTangNbHiMax", signed(max(NBABL[n]["OD"]["hi"] for n in D)))
mac("NWDNegative", sum(C[n]["weights_mean"]["TOD"]["D"] < 0 for n in D))
mac("NHknnLambdaMax", sum(PM[n]["HKNN"]["lambda_rel"] == max(m["lambda_grid"]) for n in D))
mac("NKnnKMax", sum(PM[n]["kNN"]["k"] == max(m["knn_grid"]) for n in D))
mac("NLocalKMax", sum(PM[n]["TOD"]["k"] == max(m["k_grid"]) for n in D))
# grid-edge fractions outside the two moons datasets, and number of near-ceiling datasets
others = [n for n in D if n not in ("moons", "moons_noise10")]
mac("FracKMaxOtherMax", int(round(max(max(FR[n]["Tod"], FR[n]["Hknn"]) for n in others))))
mac("FracKMaxOtherMaxArg", ", ".join(DSNAME[n] for n in others
                                     if max(FR[n]["Tod"], FR[n]["Hknn"]) == max(max(FR[x]["Tod"], FR[x]["Hknn"]) for x in others)))
mac("NNearCeiling", sum(C[n]["means"][C[n]["best_reference"]] >= 0.96 for n in D))
mac("NearCeilingList", ", ".join(DSNAME[n] for n in D if C[n]["means"][C[n]["best_reference"]] >= 0.96))
mac("NLowDim", sum(D[n]["d"] <= 3 for n in D))
mac("LowDimList", ", ".join(DSNAME[n] for n in D if D[n]["d"] <= 3))

# regime scan
R = reg["datasets"]
RC = reg["comparison"]
rn = sorted(R, key=lambda n: R[n]["p"])
NBREG, NBREGD = {}, {}
for n in rn:
    p = R[n]["p"]
    tag = f"P{PNUM[p]}"
    for me in METHODS:
        mac(f"Reg{tag}{ME[me]}", pct(RC[n]["means"][me]))
    mac(f"RegBest{tag}", RC[n]["best_reference"])
    mac(f"RegDelta{tag}", signed(RC[n]["vs_best"]["mean"]))
    mac(f"RegLo{tag}", signed(RC[n]["vs_best"]["ci_low"]))
    mac(f"RegHi{tag}", signed(RC[n]["vs_best"]["ci_high"]))
    NBREG[n] = nb_vs(R, n, "TOD", RC[n]["best_reference"])
    mac(f"RegNbLo{tag}", signed(NBREG[n]["lo"]))
    mac(f"RegNbHi{tag}", signed(NBREG[n]["hi"]))
    mac(f"RegAblDepth{tag}", signed(RC[n]["ablation"]["TO"]["mean"]))
    mac(f"RegAblDepthLo{tag}", signed(RC[n]["ablation"]["TO"]["ci_low"]))
    mac(f"RegAblDepthHi{tag}", signed(RC[n]["ablation"]["TO"]["ci_high"]))
    NBREGD[n] = nb_vs(R, n, "TOD", "TO")
    mac(f"RegAblDepthNbLo{tag}", signed(NBREGD[n]["lo"]))
    mac(f"RegAblDepthNbHi{tag}", signed(NBREGD[n]["hi"]))
    mac(f"RegAblDepthNbP{tag}", pval(RC[n]["ablation"]["TO"]["nb_p"]))
    mac(f"RegBestAcc{tag}", pct(RC[n]["means"][RC[n]["best_reference"]]))
    mac(f"RegAblTang{tag}", signed(RC[n]["ablation"]["OD"]["mean"]))
mac("NRegSigWins", sum(RC[n]["vs_best"]["ci_low"] > 0 for n in rn))
mac("NRegSigLosses", sum(RC[n]["vs_best"]["ci_high"] < 0 for n in rn))
mac("NRegSigWinsNb", sum(NBREG[n]["lo"] > 0 for n in rn))
mac("NRegSigLossesNb", sum(NBREG[n]["hi"] < 0 for n in rn))
mac("NRegime", len(rn))
mac("RegDeltaMin", signed(min(RC[n]["vs_best"]["mean"] for n in rn)))
mac("RegDeltaMax", signed(max(RC[n]["vs_best"]["mean"] for n in rn)))
mac("RegBestSet", ", ".join(sorted(set(RC[n]["best_reference"] for n in rn))))
mac("RegAblDepthMin", signed(min(RC[n]["ablation"]["TO"]["mean"] for n in rn)))
mac("RegAblDepthMax", signed(max(RC[n]["ablation"]["TO"]["mean"] for n in rn)))
mac("RegAblTangMin", signed(min(RC[n]["ablation"]["OD"]["mean"] for n in rn)))
mac("RegAblTangMax", signed(max(RC[n]["ablation"]["OD"]["mean"] for n in rn)))
mac("RegAblOrthMin", signed(min(RC[n]["ablation"]["TD"]["mean"] for n in rn)))
mac("RegAblOrthMax", signed(max(RC[n]["ablation"]["TD"]["mean"] for n in rn)))
mac("NRegAblDepthCiAboveZero", sum(RC[n]["ablation"]["TO"]["ci_low"] > 0 for n in rn))
mac("NRegAblTangCiAboveZero", sum(RC[n]["ablation"]["OD"]["ci_low"] > 0 for n in rn))
mac("NRegAblDepthNbAboveZero", sum(NBREGD[n]["lo"] > 0 for n in rn))
mac("NDepthIntervals", len(D) + len(rn))
mac("NDepthIntervalsBootAboveZero", sum(C[n]["ablation"]["TO"]["ci_low"] > 0 for n in D)
    + sum(RC[n]["ablation"]["TO"]["ci_low"] > 0 for n in rn))
mac("RegSdDrop", pct(RC[rn[0]]["means"]["SD"] - RC[rn[-1]]["means"]["SD"]))
mac("RegKnnDrop", pct(RC[rn[0]]["means"]["kNN"] - RC[rn[-1]]["means"]["kNN"]))
mac("RegTodDrop", pct(RC[rn[0]]["means"]["TOD"] - RC[rn[-1]]["means"]["TOD"]))
mac("RegHknnDrop", pct(RC[rn[0]]["means"]["HKNN"] - RC[rn[-1]]["means"]["HKNN"]))


# ------------------------------------------------------------------ tables
def body(rows):
    """Rows joined by \\\\; the last row has no terminator, main.tex supplies it after \\input."""
    return " \\\\\n".join(rows) + "\n"


def bold_best(c, me):
    v = pct(c["means"][me])
    return rf"\textbf{{{v}}}" if me == c["best_reference"] else v


rows = []
for n in D:
    d, c = D[n], C[n]
    rows.append(f"{DSNAME[n]} & {d['n']} & {d['d']} & {d['classes']} & "
                + " & ".join(bold_best(c, me) for me in METHODS))
open(os.path.join(OUT, "table_main.tex"), "w").write(body(rows))

# primary comparison: bootstrap CI, Nadeau-Bengio CI and p, W/L/T, and TOD - HKNN
rows = []
for n in D:
    c = C[n]
    s = c["vs_best"]
    rows.append(f"{DSNAME[n]} & {c['best_reference']} & {ci(s, 2)} & {nbci(NBBEST[n], 2)} & {pval(s['nb_p'])} & "
                f"{s['wins']}/{s['losses']}/{s['ties']} & {ci(c['vs_each']['HKNN'], 2)}")
open(os.path.join(OUT, "table_delta.tex"), "w").write(body(rows))

# TOD minus each reference, bootstrap and Nadeau-Bengio intervals, in two halves (appendix)
for suffix, refs in (("a", REFS[:3]), ("b", REFS[3:])):
    rows = []
    for n in D:
        c = C[n]
        rows.append(f"{DSNAME[n]} & " + " & ".join(f"{ci(c['vs_each'][me])} & {nbci(NBEACH[n][me])}" for me in refs))
    open(os.path.join(OUT, f"table_each_{suffix}.tex"), "w").write(body(rows))
if os.path.exists(os.path.join(OUT, "table_each.tex")):
    os.remove(os.path.join(OUT, "table_each.tex"))

# ablations: bootstrap CI and, for the orthogonal component, the Nadeau-Bengio CI
rows = []
for n in D:
    c = C[n]
    rows.append(f"{DSNAME[n]} & {ci(c['ablation']['TO'])} & {ci(c['ablation']['TD'])} & {nbci(NBABL[n]['TD'])} & "
                f"{ci(c['ablation']['OD'])}")
open(os.path.join(OUT, "table_ablation.tex"), "w").write(body(rows))

# selective accuracy: against the best reference by accuracy and by selective accuracy
rows = []
for n in D:
    c = C[n]
    rows.append(f"{DSNAME[n]} & " + " & ".join(pct(c["sel_means"][me]) for me in ["kNN", "NFL", "HKNN", "LPH", "LCD", "SD", "TOD", "TO", "OD"])
                + f" & {ci(c['sel_vs_best'])} & {c['sel_best_reference_by_sel']} & {ci(c['sel_vs_best_by_sel'])}")
open(os.path.join(OUT, "table_selective.tex"), "w").write(body(rows))

# hyper-parameters (deterministic mode), grid-edge fractions and weights
rows = []
for n in D:
    c = C[n]
    pm = PM[n]
    w = c["weights_mean"]["TOD"]
    rows.append(f"{DSNAME[n]} & {pm['kNN']['k']} & ({pm['HKNN']['k']}, {pm['HKNN']['lambda_rel']:g}) & "
                f"({pm['LPH']['k']}, {pm['LPH']['m']}) & {pm['SD']['k']} & ({pm['TOD']['k']}, {pm['TOD']['m']}) & "
                f"{FR[n]['Tod']:.0f} / {FR[n]['Hknn']:.0f} & "
                f"{w['T']:.2f} & {w['O']:.2f} & {w['D']:.2f}")
open(os.path.join(OUT, "table_params.tex"), "w").write(body(rows))

rows = []
for n in rn:
    c = RC[n]
    rows.append(f"{R[n]['p']} & " + " & ".join(pct(c["means"][me]) for me in ["kNN", "NFL", "HKNN", "LPH", "LCD", "SD", "TOD", "TO", "TD", "OD"])
                + f" & {c['best_reference']} & {ci(c['vs_best'])}")
open(os.path.join(OUT, "table_regime.tex"), "w").write(body(rows))

# ------------------------------------------------ supplementary tables (results/tables_appendix.md)
def mdci(s):
    return f"{signed(s['mean'], 2)} [{signed(s['ci_low'], 2)}, {signed(s['ci_high'], 2)}]"


def mdnb(s):
    return f"[{signed(s['lo'], 2)}, {signed(s['hi'], 2)}]"


def sep(ncol):
    return "|" + "---|" * ncol


MD = ["# SPD001 -- supplementary tables (generated by experiments/make_numbers.py from results/*.json)\n",
      "Accuracy points. boot = percentile bootstrap 95% interval over the 25 folds; NB = 95% interval with the "
      "Nadeau-Bengio variance (inflation 1/J + n_test/n_train = 1/25 + 1/4). Reference run, seed "
      f"{m['seed']}, {m['n_splits']}x{m['n_repeats']} repeated stratified k-fold.\n",
      "## TOD minus each reference\n",
      "| dataset | " + " | ".join(f"vs {r} boot | vs {r} NB" for r in REFS) + " |", sep(1 + 2 * len(REFS))]
for n in D:
    MD.append(f"| {DSNAME[n]} | " + " | ".join(f"{mdci(C[n]['vs_each'][r])} | {mdnb(NBEACH[n][r])}" for r in REFS) + " |")
MD += ["\n## Ablations: TOD minus the reduced model\n",
       "| dataset | - depth (vs TO) boot | NB | - orthogonal (vs TD) boot | NB | - tangential (vs OD) boot | NB |", sep(7)]
for n in D:
    MD.append(f"| {DSNAME[n]} | " + " | ".join(f"{mdci(C[n]['ablation'][a])} | {mdnb(NBABL[n][a])}" for a in ("TO", "TD", "OD")) + " |")
MD += ["\n## Selective accuracy at 80% coverage (mean over folds, %)\n",
       "| dataset | " + " | ".join(METHODS) + " | TOD - best ref. by accuracy, boot | NB | best ref. by sel. acc. | TOD - best ref. by sel. acc., boot |",
       sep(len(METHODS) + 5)]
for n in D:
    c = C[n]
    MD.append(f"| {DSNAME[n]} | " + " | ".join(pct(c["sel_means"][me], 2) for me in METHODS)
              + f" | {mdci(c['sel_vs_best'])} | {mdnb(NBSEL[n])} | {c['sel_best_reference_by_sel']} | {mdci(c['sel_vs_best_by_sel'])} |")
MD += ["\n## Hyper-parameters: deterministic mode over folds, % of folds at the top of the grid, mean TOD weights\n",
       "| dataset | kNN k | HKNN (k, lambda_rel) | LPH (k, m) | SD k | TOD (k, m) | % TOD k = max | % HKNN k = max | % kNN k = max | % HKNN lambda = max | w_T | w_O | w_D |",
       sep(13)]
for n in D:
    pm, w, f = PM[n], C[n]["weights_mean"]["TOD"], FR[n]
    MD.append(f"| {DSNAME[n]} | {pm['kNN']['k']} | ({pm['HKNN']['k']}, {pm['HKNN']['lambda_rel']:g}) | ({pm['LPH']['k']}, {pm['LPH']['m']}) | "
              f"{pm['SD']['k']} | ({pm['TOD']['k']}, {pm['TOD']['m']}) | {f['Tod']:.0f} | {f['Hknn']:.0f} | {f['Knn']:.0f} | {f['Lam']:.0f} | "
              f"{w['T']:.2f} | {w['O']:.2f} | {w['D']:.2f} |")
MD += ["\n## E2: moons regime scan, accuracy (%) against the number p of noise coordinates\n",
       "| p | " + " | ".join(METHODS) + " | best ref. | TOD - best ref., boot | NB | TOD - TO (depth), boot | NB |",
       sep(len(METHODS) + 6)]
for n in rn:
    c = RC[n]
    MD.append(f"| {R[n]['p']} | " + " | ".join(pct(c["means"][me], 2) for me in METHODS)
              + f" | {c['best_reference']} | {mdci(c['vs_best'])} | {mdnb(NBREG[n])} | {mdci(c['ablation']['TO'])} | {mdnb(NBREGD[n])} |")
with open(os.path.join(ROOT, "results", "tables_appendix.md"), "w") as fh:
    fh.write("\n".join(MD) + "\n")

with open(os.path.join(OUT, "numbers.tex"), "w") as fh:
    fh.write("% generated by experiments/make_numbers.py -- do not edit\n")
    fh.write("\n".join(L) + "\n")
print(f"wrote numbers.tex ({len(L)} macros) and table bodies")
