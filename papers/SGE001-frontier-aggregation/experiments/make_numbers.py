#!/usr/bin/env python3
"""Turn results/results.json into LaTeX macros (manuscript/numbers.tex) and table bodies
(manuscript/table_*.tex).  Every number in main.tex comes from here."""
import json
import os

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
res = json.load(open(os.path.join(ROOT, "results", "results.json")))
OUT = os.path.join(ROOT, "manuscript")


def sci(x, digits=1):
    if x is None:
        return "--"
    if x == 0:
        return r"\ensuremath{0}"
    e = int(f"{x:e}".split("e")[1])
    m = x / 10 ** e
    if round(m, digits) >= 10:            # 9.96 -> 10.0 rollover
        m /= 10
        e += 1
    return rf"\ensuremath{{{m:.{digits}f}\times 10^{{{e}}}}}"


def fnum(x, d=2):
    return f"{x:.{d}f}"


def pct(x, d=1):
    return f"{100 * x:.{d}f}"


def sig(s):
    return f"{s:.3g}"


L = []
def M(name, val):
    L.append(rf"\newcommand{{\{name}}}{{{val}}}")


def write_table(name, rows):
    body = " \\\\\n".join(rows) + "\n"      # last row without terminator: main.tex adds it after \input
    open(os.path.join(OUT, f"table_{name}.tex"), "w").write(body)


m = res["meta"]
M("MetaSeed", m["seed"]); M("MetaPython", m["python"]); M("MetaNumpy", m["numpy"]); M("MetaScipy", m["scipy"])
M("MetaSeconds", int(round(m["seconds"])))
M("EzeroCDthird", sci(res["E0"]["CD"]["third"])); M("EzeroCESthird", sci(res["E0"]["CES"]["third"]))

# ---------------------------------------------------------------- E1
E1 = res["E1"]
rows = E1["rows"]
M("EoneN", rows[0]["N"]); M("EoneReps", rows[0]["reps"])
M("EoneXbarK", E1["xbar"][0]); M("EoneXbarL", E1["xbar"][1]); M("EoneCorr", E1["corr"])
keys = {"CD-LN": "CDLN", "CD-SU": "CDSU", "CES-LN": "CESLN", "CES-SU": "CESSU"}
for key, tag in keys.items():
    S = E1["summary"][key]
    M(f"EoneSlopeOne{tag}", fnum(S["slope_e1"], 2)); M(f"EoneSlopeTwo{tag}", fnum(S["slope_e2"], 2)); M(f"EoneSlopeThree{tag}", fnum(S["slope_e3"], 2))
    M(f"EoneConeLargest{tag}", fnum(S["C1_largest_sigma_uniform"], 2)); M(f"EoneConeWhole{tag}", "yes" if S["C1_holds_whole_grid"] else "no")
    M(f"EoneSigmaMax{tag}", fnum(S["sigma_max_grid"], 1)); M(f"EoneRtoMinLeTwo{tag}", fnum(S["r21_min_sigma_le_0p2"], 0))
    M(f"EoneRtoAtMax{tag}", fnum(S["r21_at_sigma_max"], 2)); M(f"EoneRttCells{tag}", S["r32_med_below_1_cells"]); M(f"EoneCells{tag}", S["cells"])
    M(f"EoneRttMin{tag}", fnum(S["r32_min_over_grid"], 3))
    if S["bound2_holds_all"] is not None:
        M(f"EoneBoundSigma{tag}", fnum(S["sigma_largest_bound2_le_e1"], 2)); M(f"EoneEtwoOverBtwoMax{tag}", fnum(S["ratio_E2_over_B2_max"], 3))
        M(f"EoneBoxOverSeg{tag}", fnum(S["ratio_B2box_over_B2_max"], 0)); M(f"EoneBoundHolds{tag}", "yes" if S["bound2_holds_all"] else "no")
sel_sig = {"LN": [0.01, 0.1, 0.316, 1.0], "SU": [0.01, 0.0935, 0.286, 0.5]}
tr = []
for key in keys:
    fname, law = key.split("-")
    sel = [r for r in rows if r["frontier"] == fname and r["law"] == law]
    for s in sel_sig[law]:
        r = min(sel, key=lambda x: abs(x["sigma"] - s))
        b = sci(r["bound2_rel_med"]) if "bound2_rel_med" in r else "--"
        tr.append(f"{fname} & {law} & {sig(r['sigma'])} & {sci(r['e1_med'])} & {sci(r['e2_med'])} & {sci(r['e3_med'])} & "
                  f"{r['r21_min']:.1f} & {r['r32_med']:.2f} & {b}")
write_table("e1", tr)
# E1b
E1b = res["E1b"]
M("EonebN", E1b["N"]); M("EonebReps", E1b["reps"]); M("EonebSdTheta", fnum(E1b["summary"]["sd_over_mean_theta"], 2))
M("EonebSigmaCov", fnum(E1b["summary"]["largest_sigma_cov_dominates"], 2)); M("EonebRatioSmallest", sci(E1b["summary"]["ratio_cov_over_e2_smallest_sigma"], 0))
M("EonebPredMin", fnum(E1b["summary"]["ratio_cov_over_pred_min"], 2)); M("EonebPredMax", fnum(E1b["summary"]["ratio_cov_over_pred_max"], 2))
write_table("e1b", [f"{sig(r['sigma'])} & {sci(r['e2_med'])} & {sci(r['cov_term_med'])} & {sci(r['e2_theta_med'])} & {sci(r['floor_pred_med'])}"
                    for r in E1b["rows"] if r["sigma"] in (0.01, 0.1, 1.0) or abs(r["sigma"] - 0.0316) < 1e-3 or abs(r["sigma"] - 0.316) < 1e-3])

# ---------------------------------------------------------------- E2
E2 = res["E2"]; S2 = E2["summary"]
M("EtwoN", E2["N"]); M("EtwoReps", E2["reps"]); M("EtwoCells", S2["n_cells"]); M("EtwoTwoSided", "all" if S2["two_sided_bound_holds_all"] else "NOT all")
M("EtwoLowerInformative", S2["n_cells_lower_bound_informative"]); M("EtwoCrossingCells", S2["crossing_cells"])
M("EtwoSlopeCappedLN", fnum(S2["LN-delta0.0"]["slope_e2_capped"], 2)); M("EtwoSlopeSmoothLN", fnum(S2["LN-delta0.0"]["slope_e2_smooth"], 2))
M("EtwoSlopeCappedSU", fnum(S2["SU-delta0.0"]["slope_e2_capped"], 2)); M("EtwoSlopeSmoothSU", fnum(S2["SU-delta0.0"]["slope_e2_smooth"], 2))
M("EtwoRatioSmallest", fnum(S2["LN_delta0_ratio_smallest_sigma"], 4)); M("EtwoRatioMin", fnum(S2["LN_delta0_ratio_range"][0], 2)); M("EtwoRatioMax", fnum(S2["LN_delta0_ratio_range"][1], 2))
M("EtwoAmplification", sci(S2["LN_delta0_amplification_smallest_sigma"], 0)); M("EtwoEtwoCapped", sci(S2["LN_delta0_e2_smallest_sigma"])); M("EtwoEtwoSmooth", sci(S2["LN_delta0_e2smooth_smallest_sigma"]))
M("EtwoRtoDeltaZero", fnum(S2["LN-delta0.0"]["r21_min"], 2)); M("EtwoRtoFarSmall", fnum(S2["LN-delta-0.3"]["r21_min_small_sigma"], 0))
M("EtwoSlopeTransition", fnum(S2["LN-delta-0.03"]["slope_e2_capped"], 1)); M("EtwoSigmaMin", fnum(S2["sigma_min"], 2))
M("EtwoDeltas", ", ".join(f"{d:+.2f}" for d in E2["deltas"]))
tr = []
for delta in (-0.3, -0.03, 0.0, 0.1):
    sel = [r for r in E2["rows"] if r["law"] == "LN" and r["delta"] == delta]
    for s in (0.01, 0.0316, 0.1, 0.316):
        r = min(sel, key=lambda x: abs(x["sigma"] - s))
        rr = r["E2_over_minusNTu_med"]
        tr.append(f"{delta:+.2f} & {sig(r['sigma'])} & {sci(r['e1_med'])} & {sci(r['e2_med'])} & {sci(r['e2_smooth_med'])} & {r['r21_min']:.2f} & "
                  f"{sci(r['NTu_rel_med'])} & {('%.3f' % rr) if rr is not None else '--'} & {r['frac_above_med']:.2f}")
write_table("e2", tr)

# ---------------------------------------------------------------- E3
E3 = res["E3"]; S3 = E3["summary"]
M("EthreeG", S3["G"]); M("Ethreen", S3["n"]); M("EthreeN", S3["N"]); M("EthreeReps", S3["reps"])
M("EthreeLemmaGap", sci(S3["lemma_topdown_equals_pooled_max_rel_gap"], 0)); M("EthreeBetterCells", S3["smooth_hier2_better_cells"]); M("EthreeCells", S3["smooth_cells"])
M("EthreeGainMin", fnum(S3["smooth_gain_min"], 2)); M("EthreeGainMax", f"{S3['smooth_gain_max']:.0f}"); M("EthreeBoundsHold", "yes" if S3["smooth_bounds_hold_all"] else "no")
M("EthreeCappedRatioMin", fnum(S3["capped_hier2_over_pooled2_min"], 3)); M("EthreeCappedRatioMax", fnum(S3["capped_hier2_over_pooled2_max"], 2))
M("EthreeNonStraddleShare", sci(S3["capped_share_from_nonstraddling_max"])); M("EthreeStraddleMin", pct(S3["capped_frac_firms_straddling_min"], 0)); M("EthreeStraddleMax", pct(S3["capped_frac_firms_straddling_max"], 0))
tr = []
sm = {(r["sigma_B"], r["sigma_W"]): r for r in E3["rows"] if not r["capped"]}
cp = {(r["sigma_B"], r["sigma_W"]): r for r in E3["rows"] if r["capped"]}
for k in sorted(sm):
    if 0.1 in k:
        continue
    a, b = sm[k], cp[k]
    tr.append(f"{k[0]} & {k[1]} & {sci(a['pooled1_med'])} & {sci(a['pooled2_med'])} & {sci(a['hier2_med'])} & {a['gain_hier_over_pooled_med']:.1f} & "
              f"{sci(b['pooled2_med'])} & {sci(b['hier2_med'])} & {pct(b['frac_firms_straddling_med'], 0)}")
write_table("e3", tr)
for k, tag in (((0.4, 0.05), "HighBLowW"), ((0.05, 0.4), "LowBHighW"), ((0.05, 0.05), "LowLow"), ((0.4, 0.4), "HighHigh")):
    M(f"EthreePooledTwo{tag}", sci(sm[k]["pooled2_med"])); M(f"EthreeHierTwo{tag}", sci(sm[k]["hier2_med"])); M(f"EthreeGain{tag}", f"{sm[k]['gain_hier_over_pooled_med']:.1f}")
    M(f"EthreeCapPooledTwo{tag}", sci(cp[k]["pooled2_med"])); M(f"EthreeCapHierTwo{tag}", sci(cp[k]["hier2_med"]))

# ---------------------------------------------------------------- E4
E4 = res["E4"]; S4 = E4["summary"]
M("EfourN", S4["N"]); M("EfourTrials", S4["trials"]); M("EfourGammaMax", pct(S4["gamma_max"], 0))
M("EfourEligibleSmooth", S4["C2_eligible_smooth_cells"]); M("EfourEligibleCapped", S4["C2_eligible_capped_cells"])
M("EfourEligible", S4["C2_eligible_cells"]); M("EfourFailing", S4["C2_failing_cells"]); M("EfourFailingSmooth", S4["C2_failing_smooth_cells"]); M("EfourFailingCapped", S4["C2_failing_capped_cells"])
M("EfourCtwoHolds", "yes" if S4["C2_holds"] else "no"); M("EfourCertifiedReversals", S4["certified_reversals_total"]); M("EfourCertifiedOneReversals", S4["certified1_reversals_total"])
M("EfourSmoothRevOneMax", pct(S4["smooth_rev1_max"], 1)); M("EfourSmoothRevTwoMax", pct(S4["smooth_rev2_max"], 1))
M("EfourCapRevOneMax", pct(S4["capped0_rev1_max"], 1)); M("EfourCapRevTwoMax", pct(S4["capped0_rev2_max"], 1)); M("EfourCapRevTwoMin", pct(S4["capped0_rev2_min"], 1))
sm4 = {r["sigma"]: r for r in E4["rows"] if r["prox"] == "none"}
c0 = {r["sigma"]: r for r in E4["rows"] if r["prox"] == 0.0}
c1 = {r["sigma"]: r for r in E4["rows"] if r["prox"] == 0.1}
sgs = sorted(sm4)
M("EfourSigmaMin", sgs[0]); M("EfourSigmaMax", sgs[-1])
M("EfourRevThreeLargeSigma", pct(sm4[sgs[-1]]["rev3"], 1)); M("EfourRevOneLargeSigma", pct(sm4[sgs[-1]]["rev1"], 1)); M("EfourRevTwoLargeSigma", pct(sm4[sgs[-1]]["rev2"], 1))
M("EfourCertFracSmall", pct(sm4[sgs[0]]["certified_frac"], 1)); M("EfourCertFracPointTwo", pct(sm4[0.2]["certified_frac"], 1)); M("EfourCertFracPointFour", pct(sm4[0.4]["certified_frac"], 1))
M("EfourCertOneFracPointTwo", pct(sm4[0.2]["certified1_frac"], 1))
M("EfourCapZeroRevOneSmall", pct(c0[sgs[0]]["rev1"], 1)); M("EfourCapZeroRevTwoSmall", pct(c0[sgs[0]]["rev2"], 1))
M("EfourCapTenRevOnePointTwo", pct(c1[0.2]["rev1"], 1)); M("EfourCapTenRevTwoPointTwo", pct(c1[0.2]["rev2"], 1))
tr = []
for s in sgs:
    a, b, c = sm4[s], c1[s], c0[s]
    tr.append(f"{s} & {pct(a['rev1'])} & {pct(a['rev2'])} & {pct(a['rev3'])} & {pct(a['certified_frac'], 0)} & {a['certified_reversals']} & "
              f"{pct(b['rev1'])} & {pct(b['rev2'])} & {pct(c['rev1'])} & {pct(c['rev2'])} & {pct(c['rev3'])}")
write_table("e4", tr)

# ---------------------------------------------------------------- E5
E5 = res["E5"]; S5 = E5["summary"]
M("EfiveN", E5["N"]); M("EfiveReps", E5["reps"]); M("EfiveLambdaGlobal", fnum(E5["lambda_global"], 2))
M("EfiveLambdaSmooth", fnum(E5["lambda_regime"]["smooth"], 2)); M("EfiveLambdaBelow", fnum(E5["lambda_regime"]["below"], 2)); M("EfiveLambdaAt", fnum(E5["lambda_regime"]["at"], 2))
M("EfiveTrainSigmas", ", ".join(str(s) for s in E5["train_sigma"])); M("EfiveTestSigmas", ", ".join(str(s) for s in E5["test_sigma"]))
for name, T in (("order2", "Otwo"), ("global", "Glob"), ("regime", "Reg")):
    for law in ("LN", "SU"):
        for reg, Rg in (("smooth", "Smooth"), ("below", "Below"), ("at", "At"), ("above", "Above")):
            M(f"Efive{T}{law}{Rg}", fnum(S5[f"{name}-{law}-{reg}"], 2))
    M(f"Efive{T}ConeAll", "yes" if S5[f"{name}-C1-holds-all"] else "no"); M(f"Efive{T}ConeSmooth", "yes" if S5[f"{name}-C1-holds-smooth"] else "no")
tr = []
for law in ("LN", "SU"):
    for reg in ("smooth", "below", "at", "above"):
        tr.append(f"{law} & {reg} & {fnum(S5[f'order2-{law}-{reg}'], 2)} & {fnum(S5[f'global-{law}-{reg}'], 2)} & {fnum(S5[f'regime-{law}-{reg}'], 2)}")
write_table("e5", tr)
# per-sigma detail for the smooth LN regime and the below LN regime
tr = []
for reg in ("smooth", "below"):
    for r in [x for x in E5["rows"] if x["law"] == "LN" and x["regime"] == reg]:
        tr.append(f"{reg} & {r['sigma']} & {sci(r['e1_med'])} & {sci(r['order2_med'])} & {sci(r['global_med'])} & {sci(r['regime_med'])}")
write_table("e5b", tr)

# ---------------------------------------------------------------- E6
E6 = res["E6"]
M("EsixKinkEps", E6["kink"]["eps"]); M("EsixKinkSigma", E6["kink"]["sigma"]); M("EsixKinkYA", E6["kink"]["YA_per_unit"]); M("EsixKinkYB", fnum(E6["kink"]["YB_per_unit"], 2))
M("EsixSqrtDelta", E6["sqrt"]["delta"]); M("EsixSqrtSigma", E6["sqrt"]["sigma"]); M("EsixSqrtYB", fnum(E6["sqrt"]["YB"], 4)); M("EsixSqrtYoneB", fnum(E6["sqrt"]["Y1B"], 4)); M("EsixSqrtYtwoB", fnum(E6["sqrt"]["Y2B"], 4))

with open(os.path.join(OUT, "numbers.tex"), "w") as fh:
    fh.write("% generated by experiments/make_numbers.py -- do not edit\n" + "\n".join(L) + "\n")
print(f"wrote numbers.tex ({len(L)} macros) and table bodies")
