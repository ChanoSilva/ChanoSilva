#!/usr/bin/env python3
"""Turn results/results.json and results/results_regime.json into LaTeX macros
(manuscript/numbers.tex) and table bodies (manuscript/table_*.tex). No number in
main.tex is typed by hand.

Protocol v0.3 (internal review round 2): the JSON comes from the preregistered run with
widened grids (PREREGISTRO_SPD001_ronda2.md); results/v02/ holds the v0.2 run, which this
script also reads to tabulate the v0.2 -> v0.3 changes with the same (common) bootstrap.
Exact ties between references are handled as in support_geometry.compare(): all tied
references are kept, wins/losses must hold against each of them.

Besides the bootstrap summaries stored in the JSON, this script recomputes from the
per-fold accuracy lists:
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


def _digits(v, nd):
    """Number of decimals: nd, or more (up to 3) when the value would print as zero."""
    while nd < 3 and v != 0 and round(abs(v), nd) == 0:
        nd += 1
    return nd


def signed(x, nd=1):
    """Signed number of accuracy points for LaTeX: typographic minus (math mode, works in
    text and math), never '-0.0' (a non-zero value that rounds to zero gets more decimals)."""
    v = 100 * x
    nd = _digits(v, nd)
    if round(abs(v), nd) == 0:
        return f"{0:.{nd}f}"
    return rf"\ensuremath{{{'-' if v < 0 else '+'}{abs(v):.{nd}f}}}"


def msigned(x, nd=2):
    """Same, plain text for the Markdown tables."""
    v = 100 * x
    nd = _digits(v, nd)
    if round(abs(v), nd) == 0:
        return f"{0:.{nd}f}"
    return f"{'-' if v < 0 else '+'}{abs(v):.{nd}f}"


def ci(s, nd=1):
    return rf"{signed(s['mean'], nd)} [{signed(s['ci_low'], nd)}, {signed(s['ci_high'], nd)}]"


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


def mdci(s):
    return f"{msigned(s['mean'])} [{msigned(s['ci_low'])}, {msigned(s['ci_high'])}]"


def mdnb(s):
    return f"[{msigned(s['lo'])}, {msigned(s['hi'])}]"


def body(rows):
    """Rows joined by \\\\; the last row has no terminator, main.tex supplies it after \\input."""
    return " \\\\\n".join(rows) + "\n"


def sep(ncol):
    return "|" + "---|" * ncol


def frac_at(DD, n, method, key, value):
    ps = DD[n]["methods"][method]["params"]
    return 100.0 * sum(p[key] == value for p in ps) / len(ps)


K_METHODS = ["NFL", "HKNN", "LPH", "LCD", "SD", "T", "TOD", "TO", "TD", "OD"]
M_METHODS = ["LPH", "T", "TOD", "TO", "TD", "OD"]


def saturation(DD, n):
    """Percent of folds at the top of the dataset's grid, per method and hyper-parameter.
    'k_natural' says whether the top k is k_cap (the whole class but the point: a natural
    boundary) rather than a truncation; m counts only m = max(M) when it is below the
    full tangent dimension min(k-1, d-1) (truncation)."""
    g = DD[n]["grids"]
    kt = max(g["k_grid"])
    out = dict(k_top=kt, k_natural=(kt == g["k_cap"]))
    out["k"] = {me: frac_at(DD, n, me, "k", kt) for me in K_METHODS}
    out["knn"] = frac_at(DD, n, "kNN", "k", max(g["knn_grid"]))
    out["lam"] = frac_at(DD, n, "HKNN", "lambda_rel", max(g["lambda_grid"]))
    mt = max(g["m_grid"])
    d = DD[n]["d"]
    out["m"] = {}
    for me in M_METHODS:
        ps = DD[n]["methods"][me]["params"]
        out["m"][me] = 100.0 * sum(p["m"] == mt and mt < min(p["k"] - 1, d - 1) for p in ps) / len(ps)
    return out


def tied_of(c):
    return c.get("best_reference_tied", [c["best_reference"]])


def refname(c):
    return "/".join(tied_of(c))


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
mac("MetaKgrid", ", ".join(str(k) for k in m["k_base"]))
mac("MetaMgrid", ", ".join(str(k) for k in m["m_grid"]))
mac("MetaKnnGrid", ", ".join(str(k) for k in m["knn_base"]))
mac("MetaLambdaGrid", ", ".join(f"{x:g}" if x < 1000 else f"10^{{{int(round(math.log10(x)))}}}" for x in m["lambda_grid"]))
mac("MetaRidge", f"{m['ridge']:g}")
mac("MetaKMax", max(m["k_base"]))
mac("MetaKnnKMax", max(m["knn_base"]))
mac("MetaLambdaMax", f"10^{{{int(round(math.log10(max(m['lambda_grid']))))}}}")
mac("MetaMMax", max(m["m_grid"]))
mac("MetaPreregSha", (m.get("preregistration_sha256") or "none")[:12])
mac("MetaProtocol", m.get("protocol", "v0.2"))

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
    mac(f"BestRef{tag}", refname(c))
    mac(f"NTied{tag}", len(tied_of(c)))
    mac(f"TotCorrect{tag}", c["total_correct"][c["best_reference"]] if "total_correct" in c else "")
    mac(f"NTestTotal{tag}", sum(d["methods"]["kNN"]["n_test"]) if "n_test" in d["methods"]["kNN"] else "")
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
    # Nadeau-Bengio reading with ties: the largest upper limit over the tied references
    nbt = [nb_vs(D, n, "TOD", r) for r in tied_of(c)]
    nbv = dict(nbv, hi_max=max(x["hi"] for x in nbt), lo_min=min(x["lo"] for x in nbt),
               win_all=all(x["lo"] > 0 for x in nbt), loss_all=all(x["hi"] < 0 for x in nbt))
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
    FR[n] = saturation(D, n)
    for me in K_METHODS:
        mac(f"FracKMax{tag}{ME[me]}", int(round(FR[n]["k"][me])))
    for me in M_METHODS:
        mac(f"FracMMax{tag}{ME[me]}", int(round(FR[n]["m"][me])))
    mac(f"FracKMax{tag}Knn", int(round(FR[n]["knn"])))
    mac(f"FracLamMax{tag}", int(round(FR[n]["lam"])))
    mac(f"KTop{tag}", FR[n]["k_top"])
    mac(f"KCap{tag}", d["grids"]["k_cap"])
    # HKNN without hull term: chosen k > d (rho = d for a generic neighbourhood)
    mac(f"FracHknnKgtD{tag}", int(round(100.0 * sum(p["k"] > d["d"] for p in d["methods"]["HKNN"]["params"]) / d["folds"])))
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
mac("NBestRefHull", sum(all(r in ("HKNN", "LPH", "NFL") for r in tied_of(C[n])) for n in D))
mac("NBestRefHullAny", sum(any(r in ("HKNN", "LPH", "NFL") for r in tied_of(C[n])) for n in D))
mac("NBestRefTies", sum(len(tied_of(C[n])) > 1 for n in D))
mac("TiesList", "; ".join(f"{DSNAME[n]} ({', '.join(tied_of(C[n]))}, {C[n]['total_correct'][C[n]['best_reference']]} of "
                          f"{sum(D[n]['methods']['kNN']['n_test'])} correct)" for n in D if len(tied_of(C[n])) > 1) or "none")
mac("NBestRefHknn", sum("HKNN" in tied_of(C[n]) for n in D))
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
mac("CiHiBestMaxNb", signed(max(NBBEST[n]["hi_max"] for n in D)))
mac("CiHiBestMaxNbTwo", signed(max(NBBEST[n]["hi_max"] for n in D), 2))
mac("CiHiBestMaxNbArg", DSNAME[max(D, key=lambda n: NBBEST[n]["hi_max"])])
mac("NSigWinsNb", sum(NBBEST[n]["win_all"] for n in D))
mac("NSigLossesNb", sum(NBBEST[n]["loss_all"] for n in D))
# complementary reading across datasets (Demsar 2006): Wilcoxon signed-rank and sign test
from scipy.stats import wilcoxon, binomtest
_dl = np.array([C[n]["vs_best"]["mean"] for n in D])
_w = wilcoxon(_dl, alternative="two-sided")
_w1 = wilcoxon(_dl, alternative="greater")
mac("WilcoxonW", f"{_w.statistic:g}")
mac("WilcoxonP", f"{_w.pvalue:.3f}")
mac("WilcoxonPGreater", f"{_w1.pvalue:.2f}")
mac("SignTestPos", int((_dl > 0).sum()))
mac("SignTestP", f"{binomtest(int((_dl > 0).sum()), int((_dl != 0).sum()), 0.5, alternative='greater').pvalue:.2f}")
mac("CiHiHknnMax", signed(max(C[n]["vs_each"]["HKNN"]["ci_high"] for n in D)))
mac("CiHiLphMax", signed(max(C[n]["vs_each"]["LPH"]["ci_high"] for n in D)))
mac("AblDepthCiHiMax", signed(max(C[n]["ablation"]["TO"]["ci_high"] for n in D)))
mac("AblTangCiHiMax", signed(max(C[n]["ablation"]["OD"]["ci_high"] for n in D)))
mac("AblDepthNbHiMax", signed(max(NBABL[n]["TO"]["hi"] for n in D)))
mac("AblTangNbHiMax", signed(max(NBABL[n]["OD"]["hi"] for n in D)))
mac("NWDNegative", sum(C[n]["weights_mean"]["TOD"]["D"] < 0 for n in D))
mac("NHknnLambdaMax", sum(PM[n]["HKNN"]["lambda_rel"] == max(D[n]["grids"]["lambda_grid"]) for n in D))
mac("NKnnKMax", sum(PM[n]["kNN"]["k"] == max(D[n]["grids"]["knn_grid"]) for n in D))
mac("NLocalKMax", sum(PM[n]["TOD"]["k"] == max(D[n]["grids"]["k_grid"]) for n in D))
# residual saturation: (dataset, method) pairs whose chosen k sits at a truncating top of the
# grid (k = 75, or the cost cap on digits) in more than half of the folds
SAT = [(n, me, FR[n]["k"][me]) for n in D for me in K_METHODS if not FR[n]["k_natural"] and FR[n]["k"][me] > 50]
mac("NSatTrunc", len(SAT))
mac("SatTruncList", "; ".join(f"{DSNAME[n]}: " + ", ".join(f"{me} {x:.0f}\\%" for nn, me, x in SAT if nn == n)
                               for n in D if any(nn == n for nn, _, _ in SAT)) or "none")
mac("SatTruncDatasets", ", ".join(DSNAME[n] for n in D if any(nn == n for nn, _, _ in SAT)) or "none")
_ns = [n for n in D if not FR[n]["k_natural"] and not any(nn == n for nn, _, _ in SAT)]
mac("NoSatDatasets", ", ".join(DSNAME[n] for n in _ns) or "none")
mac("FracKMaxNoSatMax", int(round(max([FR[n]["k"][me] for n in _ns for me in K_METHODS] or [0]))))
_nat = [n for n in D if FR[n]["k_natural"]]
mac("NaturalCapDatasets", ", ".join(DSNAME[n] for n in _nat) or "none")
mac("SatKnnMax", int(round(max(FR[n]["knn"] for n in D))))
mac("SatKnnMaxArg", DSNAME[max(D, key=lambda n: FR[n]["knn"])])
mac("SatLamMax", int(round(max(FR[n]["lam"] for n in D))))
mac("SatLamMaxArg", DSNAME[max(D, key=lambda n: FR[n]["lam"])])
mac("SatMMax", int(round(max(FR[n]["m"][me] for n in D for me in M_METHODS))))
mac("SatMMaxArg", ", ".join(sorted({f"{me} on {DSNAME[n]}" for n in D for me in M_METHODS
                                    if FR[n]["m"][me] == max(FR[x]["m"][y] for x in D for y in M_METHODS)})))
mac("SatMMaxNoT", int(round(max(FR[n]["m"][me] for n in D for me in M_METHODS if me != "T"))))
mac("SatMMaxNoTArg", DSNAME[max(D, key=lambda n: max(FR[n]["m"][me] for me in M_METHODS if me != "T"))])
mac("NTWorst", sum(min(C[n]["means"], key=C[n]["means"].get) == "T" for n in D))
mac("LphCiAboveList", ", ".join(DSNAME[n] for n in D if C[n]["vs_each"]["LPH"]["ci_low"] > 0) or "none")
mac("SdCiAboveList", ", ".join(DSNAME[n] for n in D if C[n]["vs_each"]["SD"]["ci_low"] > 0) or "none")
mac("KnnCiAboveList", ", ".join(DSNAME[n] for n in D if C[n]["vs_each"]["kNN"]["ci_low"] > 0) or "none")
mac("SelBelowList", ", ".join(DSNAME[n] for n in D if C[n]["sel_vs_best"]["ci_high"] < 0) or "none")
mac("SelAboveList", ", ".join(DSNAME[n] for n in D if C[n]["sel_vs_best"]["ci_low"] > 0) or "none")
mac("NWOLargest", sum(C[n]["weights_mean"]["TOD"]["O"] > max(abs(C[n]["weights_mean"]["TOD"]["T"]), abs(C[n]["weights_mean"]["TOD"]["D"])) for n in D))
mac("HullFamilyMaxSpreadArg", DSNAME[max(D, key=lambda n: max(C[n]["means"][x] for x in ("HKNN", "LPH", "TOD", "TO", "OD")) - min(C[n]["means"][x] for x in ("HKNN", "LPH", "TOD", "TO", "OD")))])
mac("NNearCeiling", sum(C[n]["means"][C[n]["best_reference"]] >= 0.96 for n in D))
mac("NearCeilingList", ", ".join(DSNAME[n] for n in D if C[n]["means"][C[n]["best_reference"]] >= 0.96))
mac("NLowDim", sum(D[n]["d"] < min(D[n]["grids"]["k_grid"]) for n in D))
mac("LowDimList", ", ".join(DSNAME[n] for n in D if D[n]["d"] < min(D[n]["grids"]["k_grid"])))
mac("KMin", min(min(D[n]["grids"]["k_grid"]) for n in D))
# datasets on which the selected HKNN neighbourhood has k > d in every fold / in some folds
_hk = {n: sum(p["k"] > D[n]["d"] for p in D[n]["methods"]["HKNN"]["params"]) / D[n]["folds"] for n in D}
mac("NHknnKgtDAll", sum(v == 1 for v in _hk.values()))
mac("HknnKgtDAllList", ", ".join(DSNAME[n] for n in D if _hk[n] == 1) or "none")
mac("NHknnKgtDSome", sum(0 < v < 1 for v in _hk.values()))
mac("HknnKgtDSomeList", ", ".join(f"{DSNAME[n]} ({100 * _hk[n]:.0f}\\%)" for n in D if 0 < _hk[n] < 1) or "none")
mac("NHknnKgtDNone", sum(v == 0 for v in _hk.values()))
mac("HknnKgtDNoneList", ", ".join(DSNAME[n] for n in D if _hk[n] == 0) or "none")
mac("NHknnKgtDMajority", sum(v > 0.5 for v in _hk.values()))
mac("NBestRefHknnKgtD", sum("HKNN" in tied_of(C[n]) and _hk[n] > 0.5 for n in D))

# regime scan
R = reg["datasets"]
RC = reg["comparison"]
rn = sorted(R, key=lambda n: R[n]["p"])
NBREG, NBREGD, REGSAT = {}, {}, {}
for n in rn:
    p = R[n]["p"]
    tag = f"P{PNUM[p]}"
    for me in METHODS:
        mac(f"Reg{tag}{ME[me]}", pct(RC[n]["means"][me]))
    mac(f"RegBest{tag}", refname(RC[n]))
    FRR = saturation(R, n)
    for me in K_METHODS:
        mac(f"FracKMaxReg{tag}{ME[me]}", int(round(FRR["k"][me])))
    mac(f"FracKMaxReg{tag}Knn", int(round(FRR["knn"])))
    mac(f"FracLamMaxReg{tag}", int(round(FRR["lam"])))
    REGSAT[n] = FRR
    mac(f"RegDelta{tag}", signed(RC[n]["vs_best"]["mean"]))
    mac(f"RegLo{tag}", signed(RC[n]["vs_best"]["ci_low"]))
    mac(f"RegHi{tag}", signed(RC[n]["vs_best"]["ci_high"]))
    NBREG[n] = nb_vs(R, n, "TOD", RC[n]["best_reference"])
    _t = [nb_vs(R, n, "TOD", r) for r in tied_of(RC[n])]
    NBREG[n].update(win_all=all(x["lo"] > 0 for x in _t), loss_all=all(x["hi"] < 0 for x in _t))
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
    mac(f"RegAblOrth{tag}", signed(RC[n]["ablation"]["TD"]["mean"]))
    mac(f"RegAblOrthLo{tag}", signed(RC[n]["ablation"]["TD"]["ci_low"]))
    mac(f"RegAblOrthHi{tag}", signed(RC[n]["ablation"]["TD"]["ci_high"]))
mac("NRegSigWins", sum(RC[n]["win_vs_all_tied"] for n in rn))
mac("NRegSigLosses", sum(RC[n]["loss_vs_all_tied"] for n in rn))
mac("NRegSigWinsNb", sum(NBREG[n]["win_all"] for n in rn))
mac("NRegSigLossesNb", sum(NBREG[n]["loss_all"] for n in rn))
mac("RegSigLossesList", ", ".join(f"$p={R[n]['p']}$" for n in rn if RC[n]["loss_vs_all_tied"]) or "none")
mac("RegAblOrthCiAboveList", ", ".join(f"$p={R[n]['p']}$" for n in rn if RC[n]["ablation"]["TD"]["ci_low"] > 0) or "none")
mac("NRegAblOrthCiAboveZero", sum(RC[n]["ablation"]["TD"]["ci_low"] > 0 for n in rn))
mac("RegReusedNote", ", ".join(f"$p={R[n]['p']}$ = {DSNAME[R[n]['reused_from']]}" for n in rn if "reused_from" in R[n]))
mac("NRegime", len(rn))
mac("RegDeltaMin", signed(min(RC[n]["vs_best"]["mean"] for n in rn)))
mac("RegDeltaMax", signed(max(RC[n]["vs_best"]["mean"] for n in rn)))
mac("RegBestSet", ", ".join(sorted(set(r for n in rn for r in tied_of(RC[n])))))
mac("RegAblDepthMin", signed(min(RC[n]["ablation"]["TO"]["mean"] for n in rn)))
mac("RegAblDepthMax", signed(max(RC[n]["ablation"]["TO"]["mean"] for n in rn)))
mac("RegAblTangMin", signed(min(RC[n]["ablation"]["OD"]["mean"] for n in rn)))
mac("RegAblTangMax", signed(max(RC[n]["ablation"]["OD"]["mean"] for n in rn)))
mac("RegAblOrthMin", signed(min(RC[n]["ablation"]["TD"]["mean"] for n in rn)))
mac("RegAblOrthMax", signed(max(RC[n]["ablation"]["TD"]["mean"] for n in rn)))
mac("NRegAblDepthCiAboveZero", sum(RC[n]["ablation"]["TO"]["ci_low"] > 0 for n in rn))
mac("NRegAblTangCiAboveZero", sum(RC[n]["ablation"]["OD"]["ci_low"] > 0 for n in rn))
mac("NRegAblDepthNbAboveZero", sum(NBREGD[n]["lo"] > 0 for n in rn))
rn_new = [n for n in rn if "reused_from" not in R[n]]          # E2 rows not identical to an E1 dataset
mac("NDepthIntervals", len(D) + len(rn_new))
mac("NDepthIntervalsBootAboveZero", sum(C[n]["ablation"]["TO"]["ci_low"] > 0 for n in D)
    + sum(RC[n]["ablation"]["TO"]["ci_low"] > 0 for n in rn_new))
mac("NDepthIntervalsNbAboveZero", sum(NBABL[n]["TO"]["lo"] > 0 for n in D) + sum(NBREGD[n]["lo"] > 0 for n in rn_new))
mac("DepthBootAboveList", ", ".join([DSNAME[n] for n in D if C[n]["ablation"]["TO"]["ci_low"] > 0]
                                    + [f"$p={R[n]['p']}$" for n in rn_new if RC[n]["ablation"]["TO"]["ci_low"] > 0]) or "none")
# E2 saturation: rows with TD (or any method) at k = 75 in more than half of the folds
mac("RegSatList", "; ".join(f"$p={R[n]['p']}$: " + ", ".join(f"{me} {REGSAT[n]['k'][me]:.0f}\\%" for me in K_METHODS if REGSAT[n]["k"][me] > 50)
                             for n in rn_new if any(REGSAT[n]["k"][me] > 50 for me in K_METHODS)) or "none")
mac("RegSdDrop", pct(RC[rn[0]]["means"]["SD"] - RC[rn[-1]]["means"]["SD"]))
mac("RegKnnDrop", pct(RC[rn[0]]["means"]["kNN"] - RC[rn[-1]]["means"]["kNN"]))
mac("RegTodDrop", pct(RC[rn[0]]["means"]["TOD"] - RC[rn[-1]]["means"]["TOD"]))
mac("RegHknnDrop", pct(RC[rn[0]]["means"]["HKNN"] - RC[rn[-1]]["means"]["HKNN"]))


# ------------------------------------------------- v0.2 -> v0.3 (results/v02, same common bootstrap)
import sys
from fractions import Fraction
sys.path.insert(0, HERE)
import support_geometry as sg  # noqa: E402

V02MD = []
V2 = {}
_v02p = os.path.join(ROOT, "results", "v02", "results.json")
if os.path.exists(_v02p):
    v02 = json.load(open(_v02p))
    v02r = json.load(open(os.path.join(ROOT, "results", "v02", "results_regime.json")))

    def v02_stats(DD, n):
        d = DD["datasets"][n]
        acc = {me: np.array(d["methods"][me]["acc"]) for me in METHODS}
        # exact means: the v0.2 JSON stores fold accuracies c/n with n <= 200
        ex = {me: sum(Fraction(a).limit_denominator(400) for a in d["methods"][me]["acc"]) for me in REFS}
        top = max(ex.values())
        tied = [me for me in REFS if ex[me] == top]
        ratio = 1.0 / (d["n_splits"] - 1)
        vs = {me: sg.paired_stats(acc["TOD"], acc[me], ratio) for me in tied}
        rep = max(tied, key=lambda me: (vs[me]["ci_high"], -REFS.index(me)))
        out = dict(tied=tied, best=rep, vs_best=vs[rep],
                   abl={a: sg.paired_stats(acc["TOD"], acc[a], ratio) for a in ("TO", "TD", "OD")},
                   frac_td=frac_at(DD["datasets"], n, "TD", "k", 30), frac_tod=frac_at(DD["datasets"], n, "TOD", "k", 30))
        return out

    V02MD += ["\n## v0.2 (k <= 30) -> v0.3 (preregistered grids): TOD minus the best reference and the three ablations\n",
              "Both runs summarised with the same common bootstrap (v0.3 code); v0.2 per-fold lists from results/v02/. "
              "%TD@top: % of folds with the TD neighbourhood size at the top of the grid (v0.2: k = 30).\n",
              "| dataset | run | best ref. | TOD - best | TOD - TO (depth) | TOD - TD (orthogonal) | TOD - OD (tangential) | %TD@top |",
              sep(8)]
    for n in D:
        a = v02_stats(v02, n)
        V2[n] = a
        tag = DS[n]
        mac(f"VtwoAblTd{tag}", signed(a["abl"]["TD"]["mean"]))
        mac(f"VtwoAblTdLo{tag}", signed(a["abl"]["TD"]["ci_low"]))
        mac(f"VtwoAblTdHi{tag}", signed(a["abl"]["TD"]["ci_high"]))
        mac(f"VtwoAblTo{tag}", signed(a["abl"]["TO"]["mean"]))
        mac(f"VtwoDeltaBest{tag}", signed(a["vs_best"]["mean"]))
        mac(f"VtwoBestRef{tag}", "/".join(a["tied"]))
        mac(f"VtwoFracTd{tag}", int(round(a["frac_td"])))
        _nt = D[n]["methods"]["kNN"]["n_test"]
        _tc = {r: sum(int(round(x * t)) for x, t in zip(v02["datasets"][n]["methods"][r]["acc"], _nt)) for r in a["tied"]}
        mac(f"VtwoTieCorrect{tag}", ", ".join(sorted(set(str(v) for v in _tc.values()))))
        mac(f"VtwoNTied{tag}", len(a["tied"]))
        mac(f"VtwoDeltaLo{tag}", signed(a["vs_best"]["ci_low"]))
        mac(f"VtwoDeltaHi{tag}", signed(a["vs_best"]["ci_high"]))
        V02MD.append(f"| {DSNAME[n]} | v0.2 | {'/'.join(a['tied'])} | {mdci(a['vs_best'])} | " + " | ".join(mdci(a["abl"][x]) for x in ("TO", "TD", "OD"))
                     + f" | {a['frac_td']:.0f} |")
        c = C[n]
        V02MD.append(f"| {DSNAME[n]} | v0.3 | {refname(c)} | {mdci(c['vs_best'])} | " + " | ".join(mdci(c["ablation"][x]) for x in ("TO", "TD", "OD"))
                     + f" | {FR[n]['k']['TD']:.0f} |")
    for n in rn_new:
        a = v02_stats(v02r, n)
        tag = f"P{PNUM[R[n]['p']]}"
        mac(f"VtwoRegAblTd{tag}", signed(a["abl"]["TD"]["mean"]))
        mac(f"VtwoRegAblTo{tag}", signed(a["abl"]["TO"]["mean"]))
        mac(f"VtwoRegAblToLo{tag}", signed(a["abl"]["TO"]["ci_low"]))
        V02MD.append(f"| E2 p={R[n]['p']} | v0.2 | {'/'.join(a['tied'])} | {mdci(a['vs_best'])} | " + " | ".join(mdci(a["abl"][x]) for x in ("TO", "TD", "OD"))
                     + f" | {a['frac_td']:.0f} |")
        c = RC[n]
        V02MD.append(f"| E2 p={R[n]['p']} | v0.3 | {refname(c)} | {mdci(c['vs_best'])} | " + " | ".join(mdci(c["ablation"][x]) for x in ("TO", "TD", "OD"))
                     + f" | {REGSAT[n]['k']['TD']:.0f} |")
    rows = []
    for n in D:
        a, c = V2[n], C[n]
        rows.append(f"{DSNAME[n]} & {ci(a['abl']['TD'])} & {a['frac_td']:.0f} & {ci(c['ablation']['TD'])} & "
                    f"{FR[n]['k']['TD']:.0f}{'$^{c}$' if FR[n]['k_natural'] else ''} & {ci(a['vs_best'])} & {ci(c['vs_best'])}")
    for n in rn_new:
        a, c = v02_stats(v02r, n), RC[n]
        rows.append(f"E2, $p={R[n]['p']}$ & {ci(a['abl']['TD'])} & {a['frac_td']:.0f} & {ci(c['ablation']['TD'])} & "
                    f"{REGSAT[n]['k']['TD']:.0f} & {ci(a['vs_best'])} & {ci(c['vs_best'])}")
    open(os.path.join(OUT, "table_v02.tex"), "w").write(body(rows))
    # v0.2 orthogonal-ablation range and counts, for the text
    mac("VtwoAblOrthMin", signed(min(V2[n]["abl"]["TD"]["mean"] for n in D)))
    mac("VtwoAblOrthMax", signed(max(V2[n]["abl"]["TD"]["mean"] for n in D)))
    mac("VtwoNAblOrthCiAboveZero", sum(V2[n]["abl"]["TD"]["ci_low"] > 0 for n in D))
    mac("VtwoNSigWins", sum(all(sg.paired_stats(np.array(v02["datasets"][n]["methods"]["TOD"]["acc"]),
                                                np.array(v02["datasets"][n]["methods"][r]["acc"]), 0.25)["ci_low"] > 0
                                for r in V2[n]["tied"]) for n in D))
    mac("VtwoSecondsCpu", int(round(v02["meta"]["seconds_cpu"])))
    # C2 robustness rule of the preregistration: bootstrap interval above zero in v0.3 and neither TOD nor
    # TD at a truncating top of the grid in more than half of the folds
    def _trunc(n, me):
        return (not FR[n]["k_natural"]) and FR[n]["k"][me] > 50
    ROB = [n for n in D if C[n]["ablation"]["TD"]["ci_low"] > 0 and not _trunc(n, "TOD") and not _trunc(n, "TD")]
    GRIDDEP = [n for n in D if C[n]["ablation"]["TD"]["ci_low"] > 0 and (_trunc(n, "TOD") or _trunc(n, "TD"))]
    LOST = [n for n in D if V2[n]["abl"]["TD"]["ci_low"] > 0 and not C[n]["ablation"]["TD"]["ci_low"] > 0]
    mac("NOrthRobust", len(ROB))
    mac("OrthRobustList", ", ".join(DSNAME[n] for n in ROB) or "none")
    mac("NOrthGridDep", len(GRIDDEP))
    mac("OrthGridDepList", ", ".join(DSNAME[n] for n in GRIDDEP) or "none")
    mac("NOrthLost", len(LOST))
    mac("OrthLostList", ", ".join(DSNAME[n] for n in LOST) or "none")
    mac("OrthRobustEffects", ", ".join(f"{signed(C[n]['ablation']['TD']['mean'])} on {DSNAME[n]}" for n in ROB) or "none")
    mac("OrthRobustNbList", ", ".join(DSNAME[n] for n in ROB if NBABL[n]["TD"]["lo"] > 0) or "none")
    mac("NOrthRobustNb", sum(NBABL[n]["TD"]["lo"] > 0 for n in ROB))


# ------------------------------------------------------------------ tables

def bold_best(c, me):
    v = pct(c["means"][me])
    return rf"\textbf{{{v}}}" if me in tied_of(c) else v


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
    rows.append(f"{DSNAME[n]} & {refname(c)}{'$^{*}$' if len(tied_of(c)) > 1 else ''} & {ci(s, 2)} & {nbci(NBBEST[n], 2)} & {pval(s['nb_p'])} & "
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
    rows.append(f"{DSNAME[n]} & {ci(c['ablation']['TO'], 2)} & {ci(c['ablation']['TD'], 2)} & {nbci(NBABL[n]['TD'], 2)} & "
                f"{ci(c['ablation']['OD'], 2)}")
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
    lam = pm['HKNN']['lambda_rel']
    lam_s = f"{lam:g}" if lam < 1000 else f"$10^{{{int(round(math.log10(lam)))}}}$"
    rows.append(f"{DSNAME[n]} & {pm['kNN']['k']} & ({pm['HKNN']['k']}, {lam_s}) & "
                f"({pm['LPH']['k']}, {pm['LPH']['m']}) & {pm['SD']['k']} & ({pm['TOD']['k']}, {pm['TOD']['m']}) & "
                f"{FR[n]['k_top']}{'' if not FR[n]['k_natural'] else '$^{c}$'} & "
                f"{FR[n]['k']['TOD']:.0f} / {FR[n]['k']['TD']:.0f} / {FR[n]['k']['HKNN']:.0f} & "
                f"{w['T']:.2f} & {w['O']:.2f} & {w['D']:.2f}")
open(os.path.join(OUT, "table_params.tex"), "w").write(body(rows))

rows = []
for n in rn:
    c = RC[n]
    rows.append(f"{R[n]['p']} & " + " & ".join(pct(c["means"][me]) for me in ["kNN", "NFL", "HKNN", "LPH", "LCD", "SD", "TOD", "TO", "TD", "OD"])
                + f" & {c['best_reference']} & {ci(c['vs_best'])}")
open(os.path.join(OUT, "table_regime.tex"), "w").write(body(rows))

# ------------------------------------------------ supplementary tables (results/tables_appendix.md)


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
MD += ["\n## Best reference and exact ties (integer counts of correct test predictions over the 25 folds)\n",
       "| dataset | tied best references | total correct (of all test predictions) | shown in tables |", sep(4)]
for n in D:
    c = C[n]
    MD.append(f"| {DSNAME[n]} | {', '.join(tied_of(c))} | {c['total_correct'][c['best_reference']]} of {sum(D[n]['methods']['kNN']['n_test'])} | {c['best_reference']} |")
MD += ["\n## Hyper-parameters: deterministic mode over folds and mean TOD weights\n",
       "| dataset | k grid | kNN k | HKNN (k, lambda_rel) | LPH (k, m) | SD k | TOD (k, m) | TD (k, m) | w_T | w_O | w_D |",
       sep(11)]
for n in D:
    pm, w = PM[n], C[n]["weights_mean"]["TOD"]
    MD.append(f"| {DSNAME[n]} | {D[n]['grids']['k_grid']} | {pm['kNN']['k']} | ({pm['HKNN']['k']}, {pm['HKNN']['lambda_rel']:g}) | ({pm['LPH']['k']}, {pm['LPH']['m']}) | "
              f"{pm['SD']['k']} | ({pm['TOD']['k']}, {pm['TOD']['m']}) | ({pm['TD']['k']}, {pm['TD']['m']}) | "
              f"{w['T']:.2f} | {w['O']:.2f} | {w['D']:.2f} |")
MD += ["\n## Residual saturation: % of folds at the top of the grid, per method (protocol v0.3)\n",
       "Top k = largest k of the dataset's grid; (c) = k_cap, the whole class but the point (natural boundary, not a truncation). "
       "kNN: % at the largest k_NN; lambda: % of HKNN folds at lambda_rel = 10^4 (natural boundary: centroid distance); "
       "m: % of folds at m = 21 when 21 < min(k-1, d-1) (truncation), maximum over LPH, T, TOD, TO, TD, OD.\n",
       "| dataset | top k | " + " | ".join(K_METHODS) + " | kNN | lambda | m (max) |", sep(5 + len(K_METHODS))]
for nm, DD, SS in [(n, D, FR[n]) for n in D] + [(n, R, REGSAT[n]) for n in rn_new]:
    lab = DSNAME[nm] if nm in D else f"E2 p={R[nm]['p']}"
    MD.append(f"| {lab} | {SS['k_top']}{' (c)' if SS['k_natural'] else ''} | " + " | ".join(f"{SS['k'][me]:.0f}" for me in K_METHODS)
              + f" | {SS['knn']:.0f} | {SS['lam']:.0f} | {max(SS['m'].values()):.0f} |")
MD += ["\n## HKNN: % of folds with selected k > d (no hull term for a generic neighbourhood)\n",
       "| dataset | d | % folds k > d |", sep(3)]
for n in D:
    MD.append(f"| {DSNAME[n]} | {D[n]['d']} | {100 * _hk[n]:.0f} |")
MD += V02MD
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
