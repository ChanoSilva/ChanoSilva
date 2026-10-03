#!/usr/bin/env python3
"""Turn results/*.json and theory/check_Hc_summary.json into LaTeX macros (numbers.tex) and the table body.

Every number quoted in manuscript/main.tex is a macro defined here; nothing is typed by hand.
"""
import json
import os

import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
res = json.load(open(os.path.join(ROOT, "results", "results.json")))
out = os.path.join(ROOT, "manuscript")
os.makedirs(out, exist_ok=True)

FN = {0.25: "Quarter", 0.35: "ThirtyFive", 0.5: "Half", 0.6: "Sixty"}
DN = {0: "Zero", 1: "One", 2: "Two", 3: "Three"}
PN = {"(3,2)": "ThreeTwo", "(2,5)": "TwoFive"}
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


def fine_N0(pattern):
    return max(c["N0"] for c in chains if c["pattern"] == pattern)


N0s = meta["N0s"]
fine, coarse = N0s[-1], N0s[0]
mac("MetaSeed", meta["seed"])
mac("MetaPython", meta["python"])
mac("MetaNumpy", meta["numpy"])
mac("MetaSeconds", int(round(meta["seconds"])))
mac("MetaMinutes", f"{meta['seconds']/60:.1f}")   # wall-clock minutes (meta.seconds is wall time)
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
            mac("LowerRop" + k, f"{m['L']/m['r']:.1f}")          # Prop. (p=2): Rop >= L_d / r_d
    if str(f) in theory:
        th = theory[str(f)]
        mac("Gamma" + FN[f], f"{th['gamma']:.3f}")
        mac("Aconst" + FN[f], f"{th['A']:.2f}")
        mac("Lambda" + FN[f], f"{th['Lambda']:.1f}")
        for d in range(1, meta["depth"] + 1):
            mac("Bound" + FN[f] + DN[d], f"{th['bounds'][d]:.0f}")
        # the same constants with the natural constant c = 1 (gamma = min(1-f, f sin(pi/p)), p = 2)
        g1 = min(1 - f, f)
        mac("GammaOne" + FN[f], f"{g1:.3f}")
        mac("LambdaOne" + FN[f], f"{th['A']/g1:.1f}")
    # a priori lower bound inside the family: Rop_d >= 2 pi (p(1-f)/f)^d  (p = 2)
    if f <= 0.5 + 1e-12:
        for d in range(1, meta["depth"] + 1):
            mac("LowerApriori" + FN[f] + DN[d], f"{2*np.pi*(2*(1-f)/f)**d:.1f}")
    # p/f and growth ratios Rop_d / Rop_{d-1}
    mac("PoverF" + FN[f], f"{2/f:.2f}")
    for d in range(2, meta["depth"] + 1):
        mac("Growth" + FN[f] + DN[d], f"{c['levels'][d]['Rop']/c['levels'][d-1]['Rop']:.2f}")

# legacy names (growth of the f = 1/2 chain)
c = chain("(2,3)", 0.5, fine)
for d in range(2, meta["depth"] + 1):
    mac("Growth" + DN[d], f"{c['levels'][d]['Rop']/c['levels'][d-1]['Rop']:.2f}")

# convergence: max relative change of Rop and tau between coarse and fine over all chains/levels; writhe differences
maxrel_rop, maxrel_tau = 0.0, 0.0
conv_rows = []
seen = set()
wr_diff_max, wr_diff_where, wr_diff_default_one = 0.0, "", 0.0
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
        conv_rows.append((c["pattern"], c["f"], d, a["N"], a["Rop"], b["N"], b["Rop"], 100 * rr,
                          abs(b["writhe"] - a["writhe"])))
        dw = abs(b["writhe"] - a["writhe"])
        if dw > wr_diff_max:
            wr_diff_max, wr_diff_where = dw, f"${c['pattern']}$"
        if c["pattern"] == "(2,3)" and d == 1:
            wr_diff_default_one = max(wr_diff_default_one, dw)
mac("ConvMaxRelRop", f"{100*maxrel_rop:.2f}")
mac("ConvMaxRelTau", f"{100*maxrel_tau:.2f}")
mac("WrDiffMax", f"{wr_diff_max:.3f}")
mac("WrDiffMaxWhere", wr_diff_where)
mac("WrDiffDefaultOne", f"{wr_diff_default_one:.0e}".replace("e-0", r"\cdot10^{-").replace("e-", r"\cdot10^{-") + "}"
    if wr_diff_default_one > 0 else "0")

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

# all levels, all patterns (finest resolution of each pattern), f <= 1/2: failures of c = 1 and near-equalities
allok, alln, all_lower_ok = 0, 0, 0
minr_all, minr_all_one = 1e9, 1e9
n_all_half, fails_one, eq_one = 0, [], {}
no_twist_min, minrad_over_r = 1e9, 1e9
for c in chains:
    for m in c["levels"][1:]:
        alln += 1
        allok += int(m["L"] <= m["L_bound"])
        all_lower_ok += int(m["L"] >= m["L_lower"] * (1 - 1e-12))
        # length bound without the twist term p|alpha| r
        no_twist = m["L_bound"] - m["p"] * abs(m["alpha"]) * m["r"]
        no_twist_min = min(no_twist_min, no_twist / m["L"])
        minrad_over_r = min(minrad_over_r, m["minRad"] / m["r"])
        if c["f"] <= 0.5 + 1e-12:
            minr_all = min(minr_all, m["tau"] / m["rho_pred"])
            minr_all_one = min(minr_all_one, m["tau"] / m["rho_pred_cone"])
            if c["N0"] == fine_N0(c["pattern"]):
                n_all_half += 1
                ratio1 = m["tau"] / m["rho_pred_cone"]
                if ratio1 < 1 - 1e-9:
                    fails_one.append((c["pattern"], c["f"], m["d"], ratio1))
                if abs(ratio1 - 1) < 5e-3:
                    eq_one.setdefault(c["pattern"], []).append(m["d"])
mac("AllLevels", alln)
mac("AllLenBoundOk", allok)
mac("AllLenLowerOk", all_lower_ok)
mac("AllMinTauOverRho", f"{minr_all:.2f}")
mac("AllMinTauOverRhoOne", f"{minr_all_one:.2f}")
mac("NoTwistMinRatio", f"{no_twist_min:.3f}")
mac("MinRadOverRMin", f"{minrad_over_r:.2f}")
mac("HypLevelsAll", n_all_half)
mac("HypFailOne", len(fails_one))
mac("HypFailOneList", "; ".join(
    (f"${p}$, $f={f}$, $d={d}$ (${r:.3f}$)" if p == "(2,3)" else f"${p}$, $d={d}$ (${r:.3f}$)")
    for p, f, d, r in fails_one))
mac("HypEqOneListOther", "; ".join(f"${p}$, $d={','.join(str(d) for d in ds)}$" for p, ds in eq_one.items() if p != "(2,3)") or "none")

# frame linking number residual |Wr_{d-1} - alpha_d/2pi - n|
res_fine = max(abs(m["Lk_residual"]) for c in chains for m in c["levels"][1:] if c["N0"] == fine_N0(c["pattern"]))
res_all = max(abs(m["Lk_residual"]) for c in chains for m in c["levels"][1:])
mac("LkResidualMax", f"{res_fine:.1e}".replace("e-0", r"\cdot10^{-").replace("e-", r"\cdot10^{-") + "}")
mac("LkResidualMaxCoarse", f"{res_all:.1e}".replace("e-0", r"\cdot10^{-").replace("e-", r"\cdot10^{-") + "}")

# tau_pt cross-check
maxrel_pt = max(abs(m["tau_pt"] - m["tau"]) / m["tau"] for c in chains for m in c["levels"][1:])
mac("PtMaxRel", f"{100*maxrel_pt:.2f}")
# tau determined by dcsd in how many levels
ndc = sum(int(m["dcsd"] / 2 <= m["minRad"]) for c in chains for m in c["levels"][1:])
mac("LevelsDcsd", ndc)

# other patterns
for pat, nm in PN.items():
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
    for d in range(2, meta["depth"] + 1):
        mac("Growth" + nm + DN[d], f"{c['levels'][d]['Rop']/c['levels'][d-1]['Rop']:.2f}")
    p, q = c["pq"][0]
    mac("PoverF" + nm, f"{p/(c['f']*np.sin(np.pi/p)):.2f}" if pat == "(3,2)" else f"{p/c['f']:.2f}")
    mac("NZero" + nm, c["N0"])

# optional curve-shortening probe
shp = os.path.join(ROOT, "results", "results_shrink.json")
if os.path.exists(shp):
    sh = json.load(open(shp))
    mac("HasShrink", 1)
    mac("ShrinkSteps", sh["meta"]["steps"])
    mac("ShrinkLam", sh["meta"]["lam"])
    mac("ShrinkNZero", sh["meta"]["N0"])
    for lv in sh["levels"]:
        k = DN[lv["d"]]
        mac("ShrinkStart" + k, f"{lv['Rop_start']:.1f}")
        mac("ShrinkBest" + k, f"{lv['Rop_best']:.1f}")
        mac("ShrinkStep" + k, lv["best_step"])
        mac("ShrinkEnd" + k, f"{lv['Rop_end']:.1f}")
        mac("ShrinkPct" + k, f"{lv['improvement_pct']:.1f}")
        mac("ShrinkLost" + k, "yes" if lv["lost_thickness"] else "no")
else:
    mac("HasShrink", 0)

# auxiliary checks (review round 1): critical pair at d = 1, writhe crossing, segment-segment contrast
auxp = os.path.join(ROOT, "results", "aux_checks.json")
if os.path.exists(auxp):
    aux = json.load(open(auxp))
    for cp in aux["critical_pairs_d1"]:
        if cp["pattern"] == "(2,3)":
            k = FN[cp["f"]]
        else:
            k = PN[cp["pattern"]]
        mac("CritSep" + k, f"{cp['base_sep_deg']:.1f}")
        mac("CritBaseDist" + k, f"{cp['base_dist']:.3f}")
        mac("CritSameDisc" + k, "yes" if cp["same_disc"] else "no")
    mac("SegLocalMin", f"{min(cp['seg_local_over_vertex'] for cp in aux['critical_pairs_d1']):.5f}")
    wc = [w for w in aux["writhe_crossing"] if w["N0"] == max(x["N0"] for x in aux["writhe_crossing"])][0]
    mac("WrCrossRstar", f"{wc['r_star']:.4f}")
    for sg in aux["segment_check"]:
        mac("SegRatio" + FN[sg["f"]] + DN[sg["d"]], f"{sg['ratio_global']:.5f}")

# constants of Theorem (H_c, p = 2) evaluated by theory/check_Hc.py on the polygons (N0 = 256 chains)
hcp = os.path.join(ROOT, "theory", "check_Hc_summary.json")
if os.path.exists(hcp):
    hc = json.load(open(hcp))
    for lv in hc:
        lab = lv["label"]                      # e.g. "(2,3) f=0.50 N0=256 d=1"
        pat = lab.split()[0]
        N0 = int(lab.split("N0=")[1].split()[0])
        d = int(lab.split("d=")[1])
        if N0 != 256:
            continue
        k = (FN[lv["f"]] if pat == "(2,3)" else PN[pat]) + DN[d]
        mac("HcCone" + k, f"{lv['c1d']:.2f}")
        mac("HcCzero" + k, f"{lv['c0']:.2f}")
        mac("HcCkappa" + k, f"{lv['c_kappa']:.2f}")
        mac("HcC" + k, f"{lv['c_level']:.2f}")
        mac("HcTheta" + k, f"{lv['Theta_min']:.2f}")
        if pat == "(2,3)" and abs(lv["f"] - 0.5) < 1e-9 and d == 1:
            mac("HcConeBase", f"{lv['c1d']:.4f}")          # c_1(1/2, 2/3), certified grid value
            mac("HcTwoConeBase", f"{2*lv['c1d']:.3f}")

with open(os.path.join(out, "numbers.tex"), "w") as fh:
    fh.write("% generated by experiments/make_numbers.py -- do not edit\n" + "\n".join(L) + "\n")

# ---- table body (merged: default family + other patterns, finest resolution) --------------------
rows = []
for f in meta["fs"]:
    c = chain("(2,3)", f, fine)
    for m in c["levels"][1:]:
        ftxt = f"{f}" + (r"$^\dagger$" if f > 0.5 + 1e-12 else "")
        rows.append(f"$(2,3)$ & {ftxt} & {m['d']} & {m['N']} & {m['r']:.4f} & {m['L']:.3f} & {m['tau']:.4f} & "
                    f"{m['Rop']:.1f} & {m['tau']/m['rho_pred_cone']:.3f} & {m['writhe']:.2f} & {m['cable_slope']} \\\\")
    rows.append("\\addlinespace[2pt]")
for pat in PN:
    c = [x for x in chains if x["pattern"] == pat and x["N0"] == fine_N0(pat)][0]
    for m in c["levels"][1:]:
        rows.append(f"${pat}$ & {c['f']} & {m['d']} & {m['N']} & {m['r']:.4f} & {m['L']:.3f} & {m['tau']:.4f} & "
                    f"{m['Rop']:.1f} & {m['tau']/m['rho_pred_cone']:.3f} & {m['writhe']:.2f} & {m['cable_slope']} \\\\")
    rows.append("\\addlinespace[2pt]")
while rows and rows[-1].startswith("\\addlinespace"):
    rows.pop()
txt = "\n".join(rows).rstrip()
if txt.endswith("\\\\"):   # a final "\\" before an \input-ed \bottomrule triggers "Misplaced \noalign"
    txt = txt[:-2].rstrip()
with open(os.path.join(out, "table_main.tex"), "w") as fh:
    fh.write(txt + "\n")

# resolution check (former Table 3) goes to results/convergence.md
with open(os.path.join(ROOT, "results", "convergence.md"), "w") as fh:
    fh.write("# RTK001 resolution check (criterion C1) and writhe stability\n\n")
    fh.write("| pattern | f | d | N coarse | L/tau coarse | N fine | L/tau fine | change (%) | |Wr_coarse - Wr_fine| |\n")
    fh.write("|---|---|---|---|---|---|---|---|---|\n")
    for r in conv_rows:
        fh.write(f"| {r[0]} | {r[1]} | {r[2]} | {r[3]} | {r[4]:.2f} | {r[5]} | {r[6]:.2f} | {r[7]:.3f} | {r[8]:.4f} |\n")
    fh.write(f"\nmax relative change: Rop {100*maxrel_rop:.3f} %, tau {100*maxrel_tau:.3f} %; "
             f"max |Wr_coarse - Wr_fine| = {wr_diff_max:.4f} ({wr_diff_where})\n")

# stale table bodies from v0.1 are no longer used
for name in ["table_patterns.tex", "table_conv.tex", "table_bounds.tex"]:
    pth = os.path.join(out, name)
    if os.path.exists(pth):
        os.remove(pth)
print("wrote numbers.tex and table_main.tex with", len(L), "macros")
