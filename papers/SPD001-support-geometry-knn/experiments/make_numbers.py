#!/usr/bin/env python3
"""Turn results/results.json and results/results_regime.json into LaTeX macros
(manuscript/numbers.tex) and table bodies (manuscript/table_*.tex). No number in
main.tex is typed by hand."""
import json
import os

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
    mac(f"BestRef{tag}", c["best_reference"])
    mac(f"AccBest{tag}", pct(c["means"][c["best_reference"]]))
    s = c["vs_best"]
    mac(f"DeltaBest{tag}", signed(s["mean"]))
    mac(f"DeltaBestTwo{tag}", signed(s["mean"], 2))
    mac(f"CiLoBest{tag}", signed(s["ci_low"]))
    mac(f"CiHiBest{tag}", signed(s["ci_high"]))
    mac(f"WinsBest{tag}", f"{s['wins']}/{s['losses']}/{s['ties']}")
    mac(f"NbPBest{tag}", pval(s["nb_p"]))
    for me in REFS:
        mac(f"DeltaVs{tag}{ME[me]}", signed(c["vs_each"][me]["mean"]))
    for me in ["TO", "TD", "OD", "T"]:
        mac(f"Abl{tag}{ME[me]}", signed(c["ablation"][me]["mean"]))
        mac(f"AblLo{tag}{ME[me]}", signed(c["ablation"][me]["ci_low"]))
        mac(f"AblHi{tag}{ME[me]}", signed(c["ablation"][me]["ci_high"]))
    w = c["weights_mean"]["TOD"]
    mac(f"WT{tag}", f"{w['T']:.2f}")
    mac(f"WO{tag}", f"{w['O']:.2f}")
    mac(f"WD{tag}", f"{w['D']:.2f}")
    ss = c["sel_vs_best"]
    mac(f"SelDeltaBest{tag}", signed(ss["mean"]))
    mac(f"SelCiLo{tag}", signed(ss["ci_low"]))
    mac(f"SelCiHi{tag}", signed(ss["ci_high"]))

# summaries across datasets
vals = [C[n]["vs_best"]["mean"] for n in D]
mac("DeltaBestMin", signed(min(vals)))
mac("DeltaBestMax", signed(max(vals)))
mac("DeltaBestAbsMax", pct(max(abs(v) for v in vals)))
mac("NDeltaWithinOne", sum(abs(v) < 0.01 for v in vals))
mac("NDeltaWithinHalf", sum(abs(v) < 0.005 for v in vals))
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
for me, word in (("TO", "Depth"), ("TD", "Orth"), ("OD", "Tang")):
    a = [C[n]["ablation"][me]["mean"] for n in D]
    mac(f"Abl{word}Min", signed(min(a)))
    mac(f"Abl{word}Max", signed(max(a)))
    mac(f"NAbl{word}CiAboveZero", sum(C[n]["ablation"][me]["ci_low"] > 0 for n in D))
    mac(f"NAbl{word}CiBelowZero", sum(C[n]["ablation"][me]["ci_high"] < 0 for n in D))
    mac(f"Abl{word}ArgMax", DSNAME[max(D, key=lambda n: C[n]["ablation"][me]["mean"])])
sel = [C[n]["sel_vs_best"]["mean"] for n in D]
mac("SelDeltaMin", signed(min(sel)))
mac("SelDeltaMax", signed(max(sel)))
mac("NSelCiAboveZero", sum(C[n]["sel_vs_best"]["ci_low"] > 0 for n in D))
mac("NSelCiBelowZero", sum(C[n]["sel_vs_best"]["ci_high"] < 0 for n in D))
wd = [C[n]["weights_mean"]["TOD"]["D"] for n in D]
wo = [C[n]["weights_mean"]["TOD"]["O"] for n in D]
wt = [C[n]["weights_mean"]["TOD"]["T"] for n in D]
mac("WDMin", f"{min(wd):.2f}")
mac("WDMax", f"{max(wd):.2f}")
mac("WOMin", f"{min(wo):.2f}")
mac("WOMax", f"{max(wo):.2f}")
mac("WTMin", f"{min(wt):.2f}")
mac("WTMax", f"{max(wt):.2f}")
# how many datasets pick lambda > 0 for HKNN (modal), and how many where the best reference is a hull method
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
# T-only and SD ranges
mac("AccTMin", pct(min(C[n]["means"]["T"] for n in D)))
mac("AccTMax", pct(max(C[n]["means"]["T"] for n in D)))
mac("AccTArgMin", DSNAME[min(D, key=lambda n: C[n]["means"]["T"])])

mac("CiHiBestMax", signed(max(C[n]["vs_best"]["ci_high"] for n in D)))
mac("CiHiHknnMax", signed(max(C[n]["vs_each"]["HKNN"]["ci_high"] for n in D)))
mac("CiHiLphMax", signed(max(C[n]["vs_each"]["LPH"]["ci_high"] for n in D)))
mac("AblDepthCiHiMax", signed(max(C[n]["ablation"]["TO"]["ci_high"] for n in D)))
mac("AblTangCiHiMax", signed(max(C[n]["ablation"]["OD"]["ci_high"] for n in D)))
mac("NWDNegative", sum(C[n]["weights_mean"]["TOD"]["D"] < 0 for n in D))
mac("NHknnLambdaMax", sum(C[n]["params_mode"]["HKNN"]["lambda_rel"] == max(m["lambda_grid"]) for n in D))
mac("NKnnKMax", sum(C[n]["params_mode"]["kNN"]["k"] == max(m["knn_grid"]) for n in D))
mac("NLocalKMax", sum(C[n]["params_mode"][x]["k"] == max(m["k_grid"]) for n in D for x in ("TOD",)))

# regime scan
R = reg["datasets"]
RC = reg["comparison"]
rn = sorted(R, key=lambda n: R[n]["p"])
for n in rn:
    p = R[n]["p"]
    tag = f"P{PNUM[p]}"
    for me in METHODS:
        mac(f"Reg{tag}{ME[me]}", pct(RC[n]["means"][me]))
    mac(f"RegBest{tag}", RC[n]["best_reference"])
    mac(f"RegDelta{tag}", signed(RC[n]["vs_best"]["mean"]))
    mac(f"RegLo{tag}", signed(RC[n]["vs_best"]["ci_low"]))
    mac(f"RegHi{tag}", signed(RC[n]["vs_best"]["ci_high"]))
    mac(f"RegAblDepth{tag}", signed(RC[n]["ablation"]["TO"]["mean"]))
    mac(f"RegAblDepthLo{tag}", signed(RC[n]["ablation"]["TO"]["ci_low"]))
    mac(f"RegAblDepthHi{tag}", signed(RC[n]["ablation"]["TO"]["ci_high"]))
    mac(f"RegBestAcc{tag}", pct(RC[n]["means"][RC[n]["best_reference"]]))
    mac(f"RegAblTang{tag}", signed(RC[n]["ablation"]["OD"]["mean"]))
mac("NRegSigWins", sum(RC[n]["vs_best"]["ci_low"] > 0 for n in rn))
mac("NRegSigLosses", sum(RC[n]["vs_best"]["ci_high"] < 0 for n in rn))
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
mac("RegSdDrop", pct(RC[rn[0]]["means"]["SD"] - RC[rn[-1]]["means"]["SD"]))
mac("RegKnnDrop", pct(RC[rn[0]]["means"]["kNN"] - RC[rn[-1]]["means"]["kNN"]))
mac("RegTodDrop", pct(RC[rn[0]]["means"]["TOD"] - RC[rn[-1]]["means"]["TOD"]))
mac("RegHknnDrop", pct(RC[rn[0]]["means"]["HKNN"] - RC[rn[-1]]["means"]["HKNN"]))

# ------------------------------------------------------------------ tables
def body(rows):
    return " \\\\\n".join(rows) + " \\\\\n"


def bold_best(c, me):
    v = pct(c["means"][me])
    return rf"\textbf{{{v}}}" if me == c["best_reference"] else v


rows = []
for n in D:
    d, c = D[n], C[n]
    rows.append(f"{DSNAME[n]} & {d['n']} & {d['d']} & {d['classes']} & "
                + " & ".join(bold_best(c, me) for me in METHODS))
open(os.path.join(OUT, "table_main.tex"), "w").write(body(rows))

rows = []
for n in D:
    c = C[n]
    s = c["vs_best"]
    rows.append(f"{DSNAME[n]} & {c['best_reference']} & {pct(c['means'][c['best_reference']], 2)} & "
                f"{pct(c['means']['TOD'], 2)} & {ci(s, 2)} & {s['wins']}/{s['losses']}/{s['ties']} & {pval(s['nb_p'])}")
open(os.path.join(OUT, "table_delta.tex"), "w").write(body(rows))

rows = []
for n in D:
    c = C[n]
    rows.append(f"{DSNAME[n]} & " + " & ".join(ci(c["vs_each"][me]) for me in REFS))
open(os.path.join(OUT, "table_each.tex"), "w").write(body(rows))

rows = []
for n in D:
    c = C[n]
    rows.append(f"{DSNAME[n]} & {ci(c['ablation']['TO'])} & {ci(c['ablation']['TD'])} & {ci(c['ablation']['OD'])} & "
                f"{ci(c['vs_each']['LPH'])} & {ci(c['vs_each']['SD'])}")
open(os.path.join(OUT, "table_ablation.tex"), "w").write(body(rows))

rows = []
for n in D:
    c = C[n]
    rows.append(f"{DSNAME[n]} & " + " & ".join(pct(c["sel_means"][me]) for me in ["kNN", "NFL", "HKNN", "LPH", "LCD", "SD", "TOD", "TO", "OD"])
                + f" & {ci(c['sel_vs_best'])}")
open(os.path.join(OUT, "table_selective.tex"), "w").write(body(rows))

rows = []
for n in D:
    c = C[n]
    pm = c["params_mode"]
    w = c["weights_mean"]["TOD"]
    rows.append(f"{DSNAME[n]} & {pm['kNN']['k']} & ({pm['HKNN']['k']}, {pm['HKNN']['lambda_rel']:g}) & "
                f"({pm['LPH']['k']}, {pm['LPH']['m']}) & {pm['SD']['k']} & ({pm['TOD']['k']}, {pm['TOD']['m']}) & "
                f"{w['T']:.2f} & {w['O']:.2f} & {w['D']:.2f}")
open(os.path.join(OUT, "table_params.tex"), "w").write(body(rows))

rows = []
for n in rn:
    c = RC[n]
    rows.append(f"{R[n]['p']} & " + " & ".join(pct(c["means"][me]) for me in ["kNN", "NFL", "HKNN", "LPH", "LCD", "SD", "TOD", "TO", "TD", "OD"])
                + f" & {c['best_reference']} & {ci(c['vs_best'])}")
open(os.path.join(OUT, "table_regime.tex"), "w").write(body(rows))

with open(os.path.join(OUT, "numbers.tex"), "w") as fh:
    fh.write("% generated by experiments/make_numbers.py -- do not edit\n")
    fh.write("\n".join(L) + "\n")
print(f"wrote numbers.tex ({len(L)} macros) and table bodies")
