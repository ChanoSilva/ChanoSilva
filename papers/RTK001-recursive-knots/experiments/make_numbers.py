#!/usr/bin/env python3
"""Turn results/results.json into LaTeX macros (numbers.tex) and table bodies."""
import json
import os

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
res = json.load(open(os.path.join(ROOT, "results", "results.json")))
out = os.path.join(ROOT, "manuscript")
os.makedirs(out, exist_ok=True)

FN = {0.25: "Quarter", 0.35: "ThirtyFive", 0.5: "Half", 0.6: "Sixty"}
DN = {0: "Zero", 1: "One", 2: "Two", 3: "Three"}
meta = res["meta"]
chains = res["chains"]
theory = res["theory"]
L = []


def mac(name, val):
    L.append(rf"\newcommand{{\{name}}}{{{val}}}")


def chain(pattern, f, N0):
    for c in chains:
        if c["pattern"] == pattern and abs(c["f"] - f) < 1e-12 and c["N0"] == N0:
            return c
    raise KeyError((pattern, f, N0))


N0s = meta["N0s"]
fine, coarse = N0s[-1], N0s[0]
mac("MetaSeed", meta["seed"])
mac("MetaPython", meta["python"])
mac("MetaNumpy", meta["numpy"])
mac("MetaSeconds", int(round(meta["seconds"])))
mac("MetaMinutes", f"{meta['seconds']/60:.1f}")
mac("NZeroCoarse", coarse)
mac("NZeroFine", fine)
mac("NZeroCoarseB", coarse // 2)
mac("NZeroFineB", fine // 2)
mac("Depth", meta["depth"])
mac("NumChains", len(chains))

# default family, finest resolution
for f in meta["fs"]:
    c = chain("(2,3)", f, fine)
    for m in c["levels"]:
        d = m["d"]
        k = FN[f] + DN[d]
        mac("Len" + k, f"{m['L']:.3f}")
        mac("Tau" + k, f"{m['tau']:.4f}")
        mac("Rop" + k, f"{m['Rop']:.1f}")
        mac("Nv" + k, m["N"])
        if d >= 1:
            mac("Rad" + k, f"{m['r']:.4f}")
            mac("Ratio" + k, f"{m['ratio_tau_r']:.3f}")
            mac("Wr" + k, f"{m['writhe']:.3f}")
            mac("Slope" + k, m["cable_slope"])
            mac("Lk" + k, m["Lk_frame"])
            mac("MinRad" + k, f"{m['minRad']:.4f}")
            mac("RhoPred" + k, f"{m['rho_pred']:.4f}")
            mac("LenBound" + k, f"{m['L_bound']:.2f}")
            mac("Alpha" + k, f"{m['alpha']:.3f}")
    if str(f) in theory:
        th = theory[str(f)]
        mac("Gamma" + FN[f], f"{th['gamma']:.3f}")
        mac("Aconst" + FN[f], f"{th['A']:.2f}")
        mac("Lambda" + FN[f], f"{th['Lambda']:.1f}")
        for d in range(1, meta["depth"] + 1):
            mac("Bound" + FN[f] + DN[d], f"{th['bounds'][d]:.0f}")

# ratios Rop_d / Rop_{d-1} for f = 0.5
c = chain("(2,3)", 0.5, fine)
for d in range(2, meta["depth"] + 1):
    mac("Growth" + DN[d], f"{c['levels'][d]['Rop']/c['levels'][d-1]['Rop']:.2f}")

# convergence: max relative change of Rop and tau between coarse and fine over all chains/levels
maxrel_rop, maxrel_tau = 0.0, 0.0
conv_rows = []
seen = set()
for c in chains:
    key = (c["pattern"], c["f"])
    if key in seen:
        continue
    seen.add(key)
    pair = [x for x in chains if (x["pattern"], x["f"]) == key]
    pair.sort(key=lambda x: x["N0"])
    lo, hi = pair[0], pair[-1]
    for d in range(1, meta["depth"] + 1):
        a, b = lo["levels"][d], hi["levels"][d]
        rr = abs(b["Rop"] - a["Rop"]) / b["Rop"]
        rt = abs(b["tau"] - a["tau"]) / b["tau"]
        maxrel_rop, maxrel_tau = max(maxrel_rop, rr), max(maxrel_tau, rt)
        conv_rows.append((c["pattern"], c["f"], d, a["N"], a["Rop"], b["N"], b["Rop"], 100 * rr))
mac("ConvMaxRelRop", f"{100*maxrel_rop:.2f}")
mac("ConvMaxRelTau", f"{100*maxrel_tau:.2f}")

# hypothesis check: min over (2,3), f <= 0.5, of tau_d / rho_pred and tau/r ; L <= L_bound checks
minr, minratio, nlev, nbound_ok = 1e9, 1e9, 0, 0
tau_eq_r = 0
minr_one, nok_one = 1e9, 0
for c in chains:
    if c["N0"] != fine or c["pattern"] != "(2,3)" or c["f"] > 0.5 + 1e-12:
        continue
    for m in c["levels"][1:]:
        nlev += 1
        minr = min(minr, m["tau"] / m["rho_pred"])
        minr_one = min(minr_one, m["tau"] / m["rho_pred_cone"])
        nok_one += int(m["tau"] >= m["rho_pred_cone"] * (1 - 1e-9))
        minratio = min(minratio, m["ratio_tau_r"])
        nbound_ok += int(m["L"] <= m["L_bound"])
        tau_eq_r += int(abs(m["ratio_tau_r"] - 1) < 5e-4)
mac("HypLevels", nlev)
mac("HypMinTauOverRho", f"{minr:.2f}")
mac("HypMinTauOverR", f"{minratio:.3f}")
mac("HypLenBoundOk", nbound_ok)
mac("HypTauEqR", tau_eq_r)
mac("HypMinTauOverRhoOne", f"{minr_one:.2f}")
mac("HypOkOne", nok_one)
# all levels, all patterns, L <= L_bound
allok, alln = 0, 0
minr_all, minr_all_one = 1e9, 1e9
for c in chains:
    for m in c["levels"][1:]:
        alln += 1
        allok += int(m["L"] <= m["L_bound"])
        if c["f"] <= 0.5 + 1e-12:
            minr_all = min(minr_all, m["tau"] / m["rho_pred"])
            minr_all_one = min(minr_all_one, m["tau"] / m["rho_pred_cone"])
mac("AllLevels", alln)
mac("AllLenBoundOk", allok)
mac("AllMinTauOverRho", f"{minr_all:.2f}")
mac("AllMinTauOverRhoOne", f"{minr_all_one:.2f}")
# tau_pt cross-check
maxrel_pt = max(abs(m["tau_pt"] - m["tau"]) / m["tau"] for c in chains for m in c["levels"][1:])
mac("PtMaxRel", f"{100*maxrel_pt:.2f}")
# tau determined by dcsd in how many levels
ndc = sum(int(m["dcsd"] / 2 <= m["minRad"]) for c in chains for m in c["levels"][1:])
mac("LevelsDcsd", ndc)

# other patterns
for pat, nm in [("(3,2)", "ThreeTwo"), ("(2,5)", "TwoFive")]:
    cs = [c for c in chains if c["pattern"] == pat]
    cs.sort(key=lambda x: x["N0"])
    c = cs[-1]
    for m in c["levels"][1:]:
        k = nm + DN[m["d"]]
        mac("Rop" + k, f"{m['Rop']:.1f}")
        mac("Tau" + k, f"{m['tau']:.4f}")
        mac("Ratio" + k, f"{m['ratio_tau_r']:.3f}")
        mac("Slope" + k, m["cable_slope"])
        mac("Wr" + k, f"{m['writhe']:.3f}")
    mac("NZero" + nm, c["N0"])

with open(os.path.join(out, "numbers.tex"), "w") as fh:
    fh.write("% generated by experiments/make_numbers.py -- do not edit\n" + "\n".join(L) + "\n")

# ---- table bodies -----------------------------------------------------------
with open(os.path.join(out, "table_main.tex"), "w") as fh:
    for k, f in enumerate(meta["fs"]):
        c = chain("(2,3)", f, fine)
        if k > 0:
            fh.write("\\addlinespace[2pt]\n")
        for m in c["levels"][1:]:
            fh.write(f"{f} & {m['d']} & {m['N']} & {m['r']:.4f} & {m['L']:.3f} & {m['minRad']:.3f} & "
                     f"{m['dcsd']/2:.4f} & {m['tau']:.4f} & {m['Rop']:.1f} & {m['rho_pred']:.4f} & "
                     f"{m['writhe']:.2f} & {m['cable_slope']} \\\\\n")

with open(os.path.join(out, "table_patterns.tex"), "w") as fh:
    for pat in ["(3,2)", "(2,5)"]:
        cs = sorted([c for c in chains if c["pattern"] == pat], key=lambda x: x["N0"])
        c = cs[-1]
        for m in c["levels"][1:]:
            fh.write(f"${pat}$ & {m['d']} & {m['N']} & {m['r']:.4f} & {m['L']:.3f} & {m['tau']:.4f} & "
                     f"{m['Rop']:.1f} & {m['rho_pred']:.4f} & {m['writhe']:.2f} & {m['cable_slope']} \\\\\n")

with open(os.path.join(out, "table_conv.tex"), "w") as fh:
    for r in conv_rows:
        fh.write(f"${r[0]}$ & {r[1]} & {r[2]} & {r[3]} & {r[4]:.2f} & {r[5]} & {r[6]:.2f} & {r[7]:.3f} \\\\\n")

with open(os.path.join(out, "table_bounds.tex"), "w") as fh:
    for f in meta["fs"]:
        if f > 0.5 + 1e-12:
            continue
        c = chain("(2,3)", f, fine)
        th = theory[str(f)]
        fh.write(f"{f} & {th['gamma']:.3f} & {th['A']:.2f} & {th['Lambda']:.1f} & "
                 + " & ".join(f"{c['levels'][d]['Rop']:.1f} / {th['bounds'][d]:.0f}" for d in range(1, meta["depth"] + 1))
                 + " \\\\\n")
print("wrote numbers.tex and tables with", len(L), "macros")

# strip the trailing row terminator of each table body (a final "\\" before an
# \input-ed \bottomrule triggers "Misplaced \noalign" in this TeX installation)
for name in ["table_main.tex", "table_patterns.tex", "table_conv.tex", "table_bounds.tex"]:
    pth = os.path.join(out, name)
    txt = open(pth).read().rstrip()
    if txt.endswith("\\\\"):
        txt = txt[:-2].rstrip()
    open(pth, "w").write(txt + "\n")
