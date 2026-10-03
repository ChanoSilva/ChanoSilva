#!/usr/bin/env python3
"""Turn results/results.json into LaTeX macros (manuscript/numbers.tex) and table bodies
(manuscript/table_*.tex).  Every number in main.tex comes from here."""
import json
import os

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
res = json.load(open(os.path.join(ROOT, "results", "results.json")))
OUT = os.path.join(ROOT, "manuscript")


def sci(x, digits=1, zero_below=1e-14):
    """Scientific notation.  In table cells (zero_below=1e-14) machine noise is shown as 0; for the
    floating-point gaps of identity checks call with zero_below=None so the actual value is printed."""
    if x is None:
        return "--"
    if zero_below is not None and abs(x) < zero_below:
        return r"\ensuremath{0}"
    e = int(f"{x:e}".split("e")[1])
    m = x / 10 ** e
    if round(m, digits) >= 10:            # 9.96 -> 10.0 rollover
        m /= 10
        e += 1
    return rf"\ensuremath{{{m:.{digits}f}\times 10^{{{e}}}}}"


def fnum(x, d=2):
    return "--" if x is None else f"{x:.{d}f}"


def pct(x, d=1):
    return f"{100 * x:.{d}f}"


def sig(s):
    return f"{s:.3g}"


def ci_pct(c, d=1):
    return f"[{100 * c[0]:.{d}f}, {100 * c[1]:.{d}f}]"


L = []
def M(name, val):
    L.append(rf"\newcommand{{\{name}}}{{{val}}}")


def write_table(name, rows):
    body = " \\\\\n".join(rows) + "\n"      # last row without terminator: main.tex adds it after \input
    open(os.path.join(OUT, f"table_{name}.tex"), "w").write(body)


m = res["meta"]
M("MetaSeed", m["seed"]); M("MetaPython", m["python"]); M("MetaNumpy", m["numpy"]); M("MetaScipy", m["scipy"])
M("MetaSeconds", int(round(m["seconds"]))); M("MetaCpuSeconds", int(round(m["cpu_seconds"])))
M("MetaSecondsTotal", int(round(m["seconds_total"]))); M("MetaCpuSecondsTotal", int(round(m["cpu_seconds_total"])))
M("MetaScriptSha", m["script_sha256"][:12]); M("MetaDate", m["date_utc"][:10])
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
    M(f"EoneSlopeOneSe{tag}", fnum(S["slope_e1_se"], 2)); M(f"EoneSlopeTwoSe{tag}", fnum(S["slope_e2_se"], 2)); M(f"EoneSlopeThreeSe{tag}", fnum(S["slope_e3_se"], 2))
    M(f"EoneCiHalfRelMax{tag}", pct(S["ci_halfwidth_rel_max"], 0))
    M(f"EoneConeLargest{tag}", fnum(S["C1_largest_sigma_uniform"], 2)); M(f"EoneConeWhole{tag}", "yes" if S["C1_holds_whole_grid"] else "no")
    M(f"EoneConeFirstFail{tag}", fnum(S["C1_first_failing_sigma"], 2))
    M(f"EoneSigmaMax{tag}", fnum(S["sigma_max_grid"], 1))
    M(f"EoneRtoAtMax{tag}", fnum(S["r21_at_sigma_max"], 2)); M(f"EoneRttCells{tag}", S["r32_med_below_1_cells"]); M(f"EoneCells{tag}", S["cells"])
    M(f"EoneRttMin{tag}", fnum(S["r32_min_over_grid"], 3))
    M(f"EoneRatioGtOneSigma{tag}", fnum(S["sigma_largest_r21_gt1_uniform"], 2))      # observed |E2| < |E1| in every replication
    if S["bound2_holds_all"] is not None:
        # certificates (k+1) B2 < |Q2| in every replication: micro-data (segmentwise B2) and moment-and-range (B2box)
        M(f"EoneCertSigma{tag}", fnum(S["sigma_largest_cert_observable"], 3))
        M(f"EoneCertBoxSigma{tag}", fnum(S["sigma_largest_cert_box"], 3))
        M(f"EoneCertConeSigma{tag}", fnum(S["sigma_largest_cert_c1"], 3))
        M(f"EoneCertConeBoxSigma{tag}", fnum(S["sigma_largest_cert_c1_box"], 3))
        M(f"EoneBoundSigmaNonobs{tag}", fnum(S["sigma_largest_bound2_le_e1_median_nonobservable"], 2))   # diagnostic only (v0.1 test)
        M(f"EoneEtwoOverBtwoMax{tag}", fnum(S["ratio_E2_over_B2_max"], 3))
        M(f"EoneBoxOverSeg{tag}", fnum(S["ratio_B2box_over_B2_max"], 0)); M(f"EoneBoundHolds{tag}", "yes" if S["bound2_holds_all"] else "no")
# looseness of B2: smallest factor B2/|E2| in any replication, largest median factor over the sweep (both laws)
_cd = [E1["summary"][k] for k in ("CD-LN", "CD-SU")]
M("EoneLooseMin", f"{1.0 / max(S['ratio_E2_over_B2_max'] for S in _cd):.0f}")
M("EoneLooseMax", f"{1.0 / min(S['ratio_E2_over_B2_med_min'] for S in _cd):.0f}")
sel_sig = {"LN": [0.01, 0.1, 1.0], "SU": [0.01, 0.0935, 0.5]}
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
# E1c: finite-N effect on the exponents
E1c = res["E1c"]
M("EonecReps", E1c["rows"][0]["reps"])
_ntag = {200: "Small", 2000: "Mid", 20000: "Large", 200000: "Huge"}
for r in E1c["rows"]:
    t = _ntag[r["N"]]
    M(f"EonecSlopeTwoN{t}", fnum(r["slope_e2"], 2)); M(f"EonecSlopeTwoSeN{t}", fnum(r["slope_e2_se"], 2))
    M(f"EonecSlopeThreeN{t}", fnum(r["slope_e3"], 2)); M(f"EonecSlopeThreeSeN{t}", fnum(r["slope_e3_se"], 3))
    M(f"EonecThirdTermN{t}", sci(r["third_moment_term_med_smallest_sigma"]))
    M(f"EonecN{t}", r["N"])
M("EonecNs", ", ".join(str(r["N"]) for r in E1c["rows"]))
M("EonecSlopeThreeMin", fnum(min(r["slope_e3"] for r in E1c["rows"]), 2)); M("EonecSlopeThreeMax", fnum(max(r["slope_e3"] for r in E1c["rows"]), 2))
M("EonecSlopeThreeSeMax", fnum(max(r["slope_e3_se"] for r in E1c["rows"]), 3))

# ---------------------------------------------------------------- E2
E2 = res["E2"]; S2 = E2["summary"]
M("EtwoN", E2["N"]); M("EtwoReps", E2["reps"]); M("EtwoCells", S2["n_cells"]); M("EtwoTwoSided", "all" if S2["two_sided_bound_holds_all"] else "NOT all")
M("EtwoLowerInformative", S2["n_cells_lower_bound_informative"]); M("EtwoCrossingCells", S2["crossing_cells"])
M("EtwoIdentityGap", sci(S2["identity_rel_gap_max"], 0, zero_below=None))
M("EtwoSlopeCappedLN", fnum(S2["LN-delta0.0"]["slope_e2_capped"], 2)); M("EtwoSlopeSmoothLN", fnum(S2["LN-delta0.0"]["slope_e2_smooth"], 2))
M("EtwoSlopeCappedSU", fnum(S2["SU-delta0.0"]["slope_e2_capped"], 2)); M("EtwoSlopeSmoothSU", fnum(S2["SU-delta0.0"]["slope_e2_smooth"], 2))
M("EtwoSlopeCappedSeLN", fnum(S2["LN-delta0.0"]["slope_e2_capped_se"], 3)); M("EtwoSlopeSmoothSeLN", fnum(S2["LN-delta0.0"]["slope_e2_smooth_se"], 2))
M("EtwoSlopeTransitionSe", fnum(S2["LN-delta-0.03"]["slope_e2_capped_se"], 2))
M("EtwoRatioMin", fnum(S2["LN_delta0_ratio_range"][0], 2)); M("EtwoRatioMax", fnum(S2["LN_delta0_ratio_range"][1], 2))
M("EtwoAmplification", sci(S2["LN_delta0_amplification_smallest_sigma"], 0)); M("EtwoEtwoCapped", sci(S2["LN_delta0_e2_smallest_sigma"])); M("EtwoEtwoSmooth", sci(S2["LN_delta0_e2smooth_smallest_sigma"]))
d0 = [r for r in E2["rows"] if r["law"] == "LN" and r["delta"] == 0.0]
s0 = [r for r in E2["rows"] if r["law"] == "SU" and r["delta"] == 0.0]
M("EtwoEtwoCappedLo", sci(d0[0]["e2_ci"][0])); M("EtwoEtwoCappedHi", sci(d0[0]["e2_ci"][1]))
M("EtwoRtoDeltaZero", fnum(S2["LN-delta0.0"]["r21_min"], 2)); M("EtwoRtoFarSmall", fnum(S2["LN-delta-0.3"]["r21_min_small_sigma"], 0))
M("EtwoRtoBelowLN", fnum(S2["LN_delta0_r21_min_below_smallest_sigma"], 3)); M("EtwoRtoBelowSU", fnum(S2["SU_delta0_r21_min_below_smallest_sigma"], 3))
M("EtwoRtoAltSU", fnum(S2["SU_delta0_r21_min_alt_branch_above"], 2))
M("EtwoFracAboveLNmin", pct(S2["LN_delta0_frac_reps_mean_above_range"][0], 0)); M("EtwoFracAboveLNmax", pct(S2["LN_delta0_frac_reps_mean_above_range"][1], 0))
M("EtwoFracAboveSUmax", pct(S2["SU_delta0_frac_reps_mean_above_range"][1], 0)); M("EtwoFracAboveSUaltMin", pct(S2["SU_delta0_frac_reps_mean_above_alt_range"][0], 0))
M("EtwoFxbarMinusCMaxLN", sci(S2["LN_delta0_fxbar_minus_c_rel_max"]))
M("EtwoFxbarMinusCSmallLN", sci(d0[0]["fxbar_minus_c_rel_max"])); M("EtwoFxbarMinusCPointThreeLN", sci(min(d0, key=lambda x: abs(x["sigma"] - 0.316))["fxbar_minus_c_rel_max"]))
_far = [r for r in E2["rows"] if r["law"] == "LN" and r["delta"] == -0.3 and r["E2_over_minusNTu_med"] is not None]
_clip = min(_far, key=lambda x: x["E2_over_minusNTu_med"])
M("EtwoRatioClipped", fnum(_clip["E2_over_minusNTu_med"], 1)); M("EtwoRatioClippedSigma", fnum(_clip["sigma"], 2))
M("EtwoTauSU", fnum(S2["SU_delta0_tau_ratio_smallest_sigma"], 3))
M("EtwoTauSUci", f"[{S2['SU_delta0_tau_ratio_smallest_sigma_ci'][0]:.3f}, {S2['SU_delta0_tau_ratio_smallest_sigma_ci'][1]:.3f}]")
M("EtwoTauLN", fnum(S2["LN_delta0_tau_ratio_smallest_sigma"], 3)); M("EtwoTaubLN", fnum(S2["LN_delta0_taub_ratio_smallest_sigma"], 3))
# per-replication distribution of the shifted ratio at the smallest sigma (M4, round 2)
M("EtwoTaubLNMin", fnum(d0[0]["Tu_over_sigma_taub_min"], 3)); M("EtwoTaubLNMax", fnum(d0[0]["Tu_over_sigma_taub_max"], 3))
M("EtwoTaubLNAbsDev", fnum(d0[0]["Tu_over_sigma_taub_absdev_med"], 4)); M("EtwoTauSUAbsDev", fnum(s0[0]["Tu_over_sigma_tau_absdev_med"], 4))
M("EtwoTaubLNPQ", pct(d0[0]["frac_reps_P_below_Q"], 0))
M("EtwoTaubLNMaxAbsDevPct", fnum(100 * max(abs(d0[0]["Tu_over_sigma_taub_min"] - 1), abs(d0[0]["Tu_over_sigma_taub_max"] - 1)), 1))
for s, tag in ((0.1, "PointOne"), (0.316, "PointThree")):
    r = min(s0, key=lambda x: abs(x["sigma"] - s)); M(f"EtwoTauSU{tag}", fnum(r["Tu_over_sigma_tau_med"], 3))
    r = min(d0, key=lambda x: abs(x["sigma"] - s)); M(f"EtwoTaubLN{tag}", fnum(r["Tu_over_sigma_taub_med"], 3))
    M(f"EtwoTaubLNPQ{tag}", pct(r["frac_reps_P_below_Q"], 0))
M("EtwoLowerSigmaLN", fnum(S2["LN_delta0_lower_informative_largest_sigma"], 2))
M("EtwoSlopeTransition", fnum(S2["LN-delta-0.03"]["slope_e2_capped"], 1)); M("EtwoSigmaMin", fnum(S2["sigma_min"], 2))
M("EtwoDeltas", ", ".join(f"{d:+.2f}" for d in E2["deltas"]))
tr = []
for law, sel in (("LN", d0), ("SU", s0)):
    for s in (0.01, 0.0316, 0.1, 0.316):
        r = min(sel, key=lambda x: abs(x["sigma"] - s))
        tr.append(f"{law} & {sig(r['sigma'])} & {sci(r['e1_med'])} & {sci(r['e2_med'])} & {sci(r['e2_smooth_med'])} & {r['r21_min']:.3f} & "
                  f"{fnum(r['r21_min_below_branch'], 3)} & {pct(r['frac_reps_mean_above'], 0)} & {fnum(r['E2_over_minusNTu_med'], 3)} & "
                  f"{fnum(r['Tu_over_sigma_tau_med'], 3)} & {fnum(r['Tu_over_sigma_taub_absdev_med'], 4)}")
write_table("e2", tr)

# ---------------------------------------------------------------- E3
E3 = res["E3"]; S3 = E3["summary"]
M("EthreeG", S3["G"]); M("Ethreen", S3["n"]); M("EthreeN", S3["N"]); M("EthreeReps", S3["reps"])
M("EthreeLemmaGap", sci(S3["lemma_topdown_equals_pooled_max_rel_gap"], 0, zero_below=None)); M("EthreeBetterCells", S3["smooth_hier2_better_cells"]); M("EthreeCells", S3["smooth_cells"])
M("EthreeGainMin", fnum(S3["smooth_gain_min"], 2)); M("EthreeGainMax", f"{S3['smooth_gain_max']:.0f}"); M("EthreeBoundsHold", "yes" if S3["smooth_bounds_hold_all"] else "no")
M("EthreeCappedRatioMin", fnum(S3["capped_hier2_over_pooled2_min"], 3)); M("EthreeCappedRatioMax", fnum(S3["capped_hier2_over_pooled2_max"], 2))
M("EthreeNonStraddleShare", sci(S3["capped_share_from_nonstraddling_max"])); M("EthreeStraddleMin", pct(S3["capped_frac_firms_straddling_min"], 0)); M("EthreeStraddleMax", pct(S3["capped_frac_firms_straddling_max"], 0))
sm = {(r["sigma_B"], r["sigma_W"]): r for r in E3["rows"] if not r["capped"]}
cp = {(r["sigma_B"], r["sigma_W"]): r for r in E3["rows"] if r["capped"]}
for k, tag in (((0.4, 0.05), "HighBLowW"), ((0.05, 0.4), "LowBHighW"), ((0.05, 0.05), "LowLow"), ((0.4, 0.4), "HighHigh")):
    M(f"EthreePooledTwo{tag}", sci(sm[k]["pooled2_med"])); M(f"EthreeHierTwo{tag}", sci(sm[k]["hier2_med"])); M(f"EthreeGain{tag}", f"{sm[k]['gain_hier_over_pooled_med']:.1f}")
    M(f"EthreeCapPooledTwo{tag}", sci(cp[k]["pooled2_med"])); M(f"EthreeCapHierTwo{tag}", sci(cp[k]["hier2_med"]))
M("EthreeHierTwoHighBLowWLo", sci(sm[(0.4, 0.05)]["hier2_ci"][0])); M("EthreeHierTwoHighBLowWHi", sci(sm[(0.4, 0.05)]["hier2_ci"][1]))
M("EthreePooledTwoHighBLowWLo", sci(sm[(0.4, 0.05)]["pooled2_ci"][0])); M("EthreePooledTwoHighBLowWHi", sci(sm[(0.4, 0.05)]["pooled2_ci"][1]))

# ---------------------------------------------------------------- E4
E4 = res["E4"]; S4 = E4["summary"]
M("EfourN", S4["N"]); M("EfourTrials", S4["trials"]); M("EfourGammaMax", pct(S4["gamma_max"], 0))
M("EfourEligibleSmooth", S4["C2_eligible_smooth_cells"]); M("EfourEligibleCapped", S4["C2_eligible_capped_cells"])
M("EfourEligible", S4["C2_eligible_cells"]); M("EfourFailing", S4["C2_failing_cells"]); M("EfourFailingSmooth", S4["C2_failing_smooth_cells"]); M("EfourFailingCapped", S4["C2_failing_capped_cells"])
M("EfourFailClearCapped", S4["C2_fail_clear_capped"]); M("EfourBorderlineCapped", S4["C2_borderline_capped"]); M("EfourBorderlineSmooth", S4["C2_borderline_smooth"])
M("EfourPassClearCapped", S4["C2_pass_clear_capped"]); M("EfourPassClearSmooth", S4["C2_pass_clear_smooth"])
M("EfourBorderline", len(S4["C2_borderline_cells"])); M("EfourPassing", len(S4["C2_passing_cells"]))
def cellname(c):
    p, s = c
    return (rf"no capacity, $\sigma={s}$" if p == "none" else rf"$+{100 * p:.0f}\%$, $\sigma={s}$")
M("EfourBorderlineCellsText", "; ".join(cellname(c) for c in S4["C2_borderline_cells"]) or "none")
rowmap = {(r["prox"], r["sigma"]): r for r in E4["rows"]}
M("EfourPassingCellsText", "; ".join(cellname(c) for c in S4["C2_passing_cells"] if c[0] != "none") or "none")
M("EfourPassingMeanBelowMin", pct(min(rowmap[(c[0], c[1])]["fracA_mean_below_cap"] for c in S4["C2_passing_cells"] if c[0] != "none"), 0))
M("EfourPassingCapped", len([c for c in S4["C2_passing_cells"] if c[0] != "none"]))
M("EfourCtwoHolds", "yes" if S4["C2_holds"] else "no"); M("EfourCertifiedReversals", S4["certified_reversals_total"]); M("EfourCertifiedOneReversals", S4["certified1_reversals_total"])
M("EfourSmoothRevOneMax", pct(S4["smooth_rev1_max"], 1)); M("EfourSmoothRevTwoMax", pct(S4["smooth_rev2_max"], 1))
M("EfourCapRevOneMax", pct(S4["capped0_rev1_max"], 1)); M("EfourCapRevTwoMax", pct(S4["capped0_rev2_max"], 1)); M("EfourCapRevTwoMin", pct(S4["capped0_rev2_min"], 1))
sm4 = {r["sigma"]: r for r in E4["rows"] if r["prox"] == "none"}
c0 = {r["sigma"]: r for r in E4["rows"] if r["prox"] == 0.0}
c1 = {r["sigma"]: r for r in E4["rows"] if r["prox"] == 0.1}
sgs = sorted(sm4)
M("EfourSigmaMin", sgs[0]); M("EfourSigmaMax", sgs[-1])
M("EfourRevThreeLargeSigma", pct(sm4[sgs[-1]]["rev3"], 1)); M("EfourRevOneLargeSigma", pct(sm4[sgs[-1]]["rev1"], 1)); M("EfourRevTwoLargeSigma", pct(sm4[sgs[-1]]["rev2"], 1))
M("EfourSmoothRevOnePointFour", pct(sm4[0.4]["rev1"], 1)); M("EfourSmoothRevOnePointFourCi", ci_pct(sm4[0.4]["rev1_ci"]))
M("EfourSmoothRevTwoPointFour", pct(sm4[0.4]["rev2"], 1)); M("EfourSmoothRevTwoPointFourCi", ci_pct(sm4[0.4]["rev2_ci"]))
M("EfourCertFracSmall", pct(sm4[sgs[0]]["certified_frac"], 1)); M("EfourCertFracPointTwo", pct(sm4[0.2]["certified_frac"], 1)); M("EfourCertFracPointFour", pct(sm4[0.4]["certified_frac"], 1))
M("EfourCertOneFracPointTwo", pct(sm4[0.2]["certified1_frac"], 1))
M("EfourCertBoxFracSmall", pct(sm4[sgs[0]]["certified_box_frac"], 1)); M("EfourCertBoxFracPointTwo", pct(sm4[0.2]["certified_box_frac"], 1))
M("EfourCertBoxFracPointOne", pct(sm4[0.1]["certified_box_frac"], 1)); M("EfourCertFracPointOne", pct(sm4[0.1]["certified_frac"], 1))
M("EfourCertBoxFracPointFour", pct(sm4[0.4]["certified_box_frac"], 1))
M("EfourCertifiedBoxReversals", S4["certified_box_reversals_total"])
M("EfourCapZeroRevOneSmall", pct(c0[sgs[0]]["rev1"], 1)); M("EfourCapZeroRevTwoSmall", pct(c0[sgs[0]]["rev2"], 1))
M("EfourCapTenRevOnePointTwo", pct(c1[0.2]["rev1"], 1)); M("EfourCapTenRevTwoPointTwo", pct(c1[0.2]["rev2"], 1))
tr = []
for s in sgs:
    a, c = sm4[s], c0[s]
    tr.append(f"{s} & {pct(a['rev1'])} {ci_pct(a['rev1_ci'])} & {pct(a['rev2'])} {ci_pct(a['rev2_ci'])} & {pct(a['rev3'])} & {pct(a['certified_frac'], 1)} & {pct(a['certified_box_frac'], 1)} & {a['certified_reversals']} & "
              f"{pct(c['rev1'])} {ci_pct(c['rev1_ci'])} & {pct(c['rev2'])} {ci_pct(c['rev2_ci'])}")
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
        M(f"Efive{T}{law}AtBelow", fnum(S5[f"{name}-{law}-at-below"], 2))
    M(f"Efive{T}ConeAll", "yes" if S5[f"{name}-C1-holds-all"] else "no"); M(f"Efive{T}ConeSmooth", "yes" if S5[f"{name}-C1-holds-smooth"] else "no")
    M(f"Efive{T}ConeExclAbove", "yes" if S5[f"{name}-C1-holds-excl-above"] else "no")
# m7 (round 2): per-dispersion reading of the smooth and below regimes (LN)
_e5 = lambda law, reg: sorted([r for r in E5["rows"] if r["law"] == law and r["regime"] == reg], key=lambda r: r["sigma"])
_sm = _e5("LN", "smooth")
M("EfiveTestSigmaMax", f"{_sm[-1]['sigma']}"); M("EfiveTestSigmaSecond", f"{_sm[-2]['sigma']}")
M("EfiveRegLNSmoothMinExclMax", fnum(min(r["regime_ratio_min"] for r in _sm[:-1]), 2)); M("EfiveRegLNSmoothAtMax", fnum(_sm[-1]["regime_ratio_min"], 2))
M("EfiveOtwoLNSmoothMinExclMax", fnum(min(r["order2_ratio_min"] for r in _sm[:-1]), 2))
M("EfiveInvLambdaGlobal", fnum(1.0 / (E5["lambda_global"] - 1.0), 2)); M("EfiveInvLambdaBelow", fnum(1.0 / (E5["lambda_regime"]["below"] - 1.0), 2))
_bl = _e5("LN", "below")
M("EfiveRegLNBelowMid", ", ".join(fnum(r["regime_ratio_min"], 2) for r in _bl if 0.1 < r["sigma"] < 0.5))
M("EfiveRegLNBelowMidSigmas", ", ".join(str(r["sigma"]) for r in _bl if 0.1 < r["sigma"] < 0.5))
M("EfiveRegLNBelowAtMax", fnum(_bl[-1]["regime_ratio_min"], 2))
M("EfiveOtwoLNBelowMaxExclSmall", fnum(max(r["order2_ratio_min"] for r in _bl[1:]), 2))
for law in ("LN", "SU"):
    fa = S5[f"order2-{law}-at-frac-above"]
    M(f"EfiveAtFracAbove{law}Min", pct(fa[0], 0)); M(f"EfiveAtFracAbove{law}Max", pct(fa[1], 0))
tr = []
for law in ("LN", "SU"):
    for reg, label in (("smooth", "smooth"), ("below", "below"), ("at", "at (all replications)"), ("at-below", "at (below branch only)"), ("above", "above")):
        if reg == "above":
            tr.append(f"{law} & above & n/a & n/a & n/a")
        else:
            tr.append(f"{law} & {label} & {fnum(S5[f'order2-{law}-{reg}'], 2)} & {fnum(S5[f'global-{law}-{reg}'], 2)} & {fnum(S5[f'regime-{law}-{reg}'], 2)}")
write_table("e5", tr)

# ---------------------------------------------------------------- E6
E6 = res["E6"]
M("EsixKinkEps", E6["kink"]["eps"]); M("EsixKinkSigma", E6["kink"]["sigma"]); M("EsixKinkYA", E6["kink"]["YA_per_unit"]); M("EsixKinkYB", fnum(E6["kink"]["YB_per_unit"], 2))
M("EsixSqrtDelta", E6["sqrt"]["delta"]); M("EsixSqrtSigma", E6["sqrt"]["sigma"]); M("EsixSqrtYB", fnum(E6["sqrt"]["YB"], 4)); M("EsixSqrtYoneB", fnum(E6["sqrt"]["Y1B"], 4)); M("EsixSqrtYtwoB", fnum(E6["sqrt"]["Y2B"], 4))

# tables that are no longer used by main.tex (E1b, E3 and E5 per sigma live in results/tables.md)
for stale in ("table_e1b.tex", "table_e3.tex", "table_e5b.tex"):
    p = os.path.join(OUT, stale)
    if os.path.exists(p):
        os.remove(p)

with open(os.path.join(OUT, "numbers.tex"), "w") as fh:
    fh.write("% generated by experiments/make_numbers.py -- do not edit\n" + "\n".join(L) + "\n")
print(f"wrote numbers.tex ({len(L)} macros) and table bodies")
