#!/usr/bin/env python3
"""Turn results/*.json into LaTeX macros (manuscript/numbers.tex) and table bodies.

Every number quoted in manuscript/main.tex comes from these macros; none is typed by hand.
"""
import json
import os

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
OUT = os.path.join(ROOT, "manuscript")
tr = json.load(open(os.path.join(ROOT, "results", "results_traffic.json")))
wf = json.load(open(os.path.join(ROOT, "results", "results_welfare.json")))
_cm_path = os.path.join(ROOT, "results", "results_commodity.json")
cm = json.load(open(_cm_path)) if os.path.exists(_cm_path) else None


def sci(x, digits=1):
    if x == 0:
        return r"\ensuremath{0}"
    e = int(f"{x:e}".split("e")[1])
    m = x / 10 ** e
    return rf"\ensuremath{{{m:.{digits}f}\times 10^{{{e}}}}}"


def pct(x, d=0):
    return f"{100 * x:.{d}f}"


L = []
def mac(name, val):
    L.append(rf"\newcommand{{\{name}}}{{{val}}}")

# meta
mac("MetaSeed", tr["meta"]["seed"])
mac("MetaPython", tr["meta"]["python"])
mac("MetaNumpy", tr["meta"]["numpy"])
mac("MetaScipy", wf["meta"]["scipy"])
mac("MetaSecondsTraffic", f"{tr['meta']['seconds']:.0f}")
mac("MetaSecondsWelfare", f"{wf['meta']['seconds']:.0f}")
mac("MetaSecondsCommodity", f"{cm['meta']['seconds']:.0f}" if cm else "--")


def crit_phrase(d):
    """'All criteria hold' is generated from the pass/fail flags written by the scripts."""
    if d is None:
        return "no criteria record"
    n = len([k for k in d if k != "all_pass"])
    failed = [k for k, v in d.items() if k != "all_pass" and not v["pass"]]
    return f"all {n} criteria hold" if not failed else f"{len(failed)} of {n} criteria FAIL ({', '.join(failed)})"


mac("CritTraffic", crit_phrase(tr.get("criteria")))
mac("CritWelfare", crit_phrase(wf.get("criteria")))
mac("CritCommodity", crit_phrase(cm.get("criteria")) if cm else "no run")

# E1a Pigou
# (v0.3) table_pigou.tex is no longer generated: the manuscript does not use it (values in results/tables_traffic.md)
p = {r["d"]: r for r in tr["E1a_pigou"]}
mac("PigouPoAOne", f"{p[1]['price_of_anarchy']:.6f}")
mac("PigouPoATwo", f"{p[2]['price_of_anarchy']:.4f}")
mac("PigouPoASixteen", f"{p[16]['price_of_anarchy']:.4f}")
mac("PigouDmax", max(p))
mac("PigouGridGap", sci(max(abs(r["optimum_cost"] - r["optimum_cost_grid_search"]) for r in tr["E1a_pigou"])))

# E1b/E1c affine
e = tr["E1b_affine"]
mac("AffInstances", e["instances"])
mac("AffPoAMax", f"{e['poa_max']:.4f}")
mac("AffPoAMean", f"{e['poa_mean']:.4f}")
mac("AffPoAMedian", f"{e['poa_median']:.4f}")
mac("AffViolations", e["bound_violations"])
mac("AffMaxResidual", sci(e["max_residual"]))
mac("AffMaxDevWaterfill", sci(e["max_dev_vs_waterfill"]))
mac("AffPoAOneCount", e["n_poa_equals_one"])
mac("AffPoAOnePct", pct(e["fraction_poa_equals_one"]))
mac("AffMaxIter", e["max_iterations"])
mac("AffFracAboveOnePct", pct(e["fraction_poa_above_1p01"]))
mac("AffFracAboveTenPct", pct(e["fraction_poa_above_1p10"]))
mac("AffMaxEqualCostSpread", sci(e["max_equal_cost_spread_eq"]))
am = e["argmax_instance"]
mac("AffArgmaxLinks", am["links"])

# E2 two-player
t = wf["E2_two_player"]
mac("TwoBetaOne", f"{t['beta1']:g}")
mac("TwoBetaTwo", f"{t['beta2']:g}")
mac("TwoAlpha", f"{t['alpha']:g}")
mac("TwoXstar", f"({t['x_star'][0]:.6g}, {t['x_star'][1]:.6g})")
mac("TwoResidual", sci(t["residual"]))
mac("TwoAngleLow", f"{t['boundary_angles_deg'][0]:.2f}")
mac("TwoAngleHigh", f"{t['boundary_angles_deg'][1]:.2f}")
mac("TwoAngles", t["angles_tested"])
mac("TwoAgreement", t["agreement"])
mac("TwoInCone", t["in_cone_count"])
mac("TwoWitnessLambda", f"({t['witness_lambda'][0]:g}, {t['witness_lambda'][1]:g})")
mac("TwoWitnessGap", f"{t['witness_gap']:.4f}")
mac("TwoWitnessX", f"({t['witness_better_x'][0]:.4g}, {t['witness_better_x'][1]:.4g})")

# E2 Cournot
c = wf["E2_cournot"]
ci, cb, ni = c["interior"], c["boundary"], c["nikaido_isoda"]
mac("CourIntXstar", f"({ci['x_star'][0]:.4f}, {ci['x_star'][1]:.4f})")
mac("CourIntGrid", ci["grid_points"])
mac("CourIntInLambda", ci["grid_points_in_Lambda"])
mac("CourIntPayEq", f"{ci['payoffs_at_equilibrium'][0]:.4f}")
mac("CourIntPayColl", f"{ci['payoffs_at_collusion'][0]:.4f}")
mac("CourBdXstar", f"({cb['x_star'][0]:.4g}, {cb['x_star'][1]:.4g})")
mac("CourBdDim", cb["cone_dim"])
mac("CourBdGrid", cb["grid_points"])
mac("CourBdInLone", cb["grid_in_L1"])
mac("CourBdInL", cb["grid_in_L"])
mac("CourBdAgreement", cb["agreement"])
mac("NIgrid", ni["grid_x"])
mac("NIlambdas", ni["lambda_directions"])
mac("NImax", sci(abs(ni["max_W_prime_over_grid_all_lambda"])) if ni["max_W_prime_over_grid_all_lambda"] != 0 else "0")
mac("NIok", "yes" if ni["x_star_optimal_for_all_lambda"] else "no")

# E3/E4 random games
rows = []
tot = {"c": {"inst": 0, "nontriv": 0, "tested": 0, "tested_in": 0, "gout": 0, "gout_out": 0, "gin": 0, "gin_in": 0, "wit": 0, "res": 0.0},
       "n": {"inst": 0, "nontriv": 0, "tested": 0, "tested_in": 0, "gout": 0, "gout_out": 0, "gin": 0, "gin_in": 0, "wit": 0, "res": 0.0}}
pga_diff = 0.0
for a in wf["E3_E4_summary"]:
    key = "c" if a["concave"] else "n"
    T = tot[key]
    T["inst"] += a["instances"]; T["nontriv"] += a["nontrivial"]; T["tested"] += a["tested_in_L1"]
    T["tested_in"] += a["tested_in_L1_in_L"]; T["gout"] += a["grid_out_L1"]; T["gout_out"] += a["grid_out_L1_out_L"]
    T["gin"] += a["grid_in_L1"]; T["gin_in"] += a["grid_in_L1_in_L"]; T["wit"] += a["witness_instances"]
    T["res"] = max(T["res"], a["max_residual"])
    pga_diff = max(pga_diff, a.get("pga_max_abs_diff", 0.0))
    dims = ", ".join(f"{k}:{v}" for k, v in a["dims"].items()) or "--"
    rows.append(f"{a['N']} & {'yes' if a['concave'] else 'no'} & {a['instances']} & {a['nontrivial']} & {dims} & "
                f"{a['tested_in_L1_in_L']}/{a['tested_in_L1']} & {a['grid_in_L1_in_L']}/{a['grid_in_L1']} & "
                f"{a['grid_out_L1_out_L']}/{a['grid_out_L1']} & {a['witness_instances']}")
    tag = f"N{ {3: 'Three', 4: 'Four', 5: 'Five'}[a['N']] }{'C' if a['concave'] else 'X'}"
    mac(f"Rnd{tag}Inst", a["instances"]); mac(f"Rnd{tag}Nontriv", a["nontrivial"])
    mac(f"Rnd{tag}Wit", a["witness_instances"]); mac(f"Rnd{tag}Bdry", pct(a["boundary_coord_fraction"]))
    mac(f"Rnd{tag}Indef", a["any_indefinite_H"])
with open(os.path.join(OUT, "table_random.tex"), "w") as fh:
    fh.write(" \\\\\n".join(rows) + "\n")
for key, name in (("c", "Conc"), ("n", "Nonc")):
    T = tot[key]
    mac(f"Rnd{name}Inst", T["inst"]); mac(f"Rnd{name}Nontriv", T["nontriv"])
    mac(f"Rnd{name}Tested", T["tested"]); mac(f"Rnd{name}TestedIn", T["tested_in"])
    mac(f"Rnd{name}Gout", T["gout"]); mac(f"Rnd{name}GoutOut", T["gout_out"])
    mac(f"Rnd{name}Gin", T["gin"]); mac(f"Rnd{name}GinIn", T["gin_in"])
    mac(f"Rnd{name}Wit", T["wit"]); mac(f"Rnd{name}MaxRes", sci(T["res"]))
    mac(f"Rnd{name}WitPct", pct(T["wit"] / T["nontriv"]) if T["nontriv"] else "--")
    mac(f"Rnd{name}GinOut", T["gin"] - T["gin_in"])
    mac(f"Rnd{name}NontrivPct", pct(T["nontriv"] / T["inst"]))
mac("RndPgaDiff", sci(pga_diff) if pga_diff > 0 else "0")
mac("RndPgaChecks", sum(a.get("pga_checks", 0) for a in wf["E3_E4_summary"]))
mac("RndTotalInst", tot["c"]["inst"] + tot["n"]["inst"])
mac("RndTotalQP", tot["c"]["tested"] + tot["c"]["gout"] + tot["c"]["gin"] + tot["n"]["tested"] + tot["n"]["gout"] + tot["n"]["gin"])
w = wf.get("E4_witness_examples", [])
def vec(v):
    return "(" + ", ".join(f"{(t if abs(t) > 5e-4 else 0.0):.3f}" for t in v) + ")"
if w:
    mac("WitGame", w[0]["game"].replace("_", " "))
    mac("WitLambda", vec(w[0]["lambda"]))
    mac("WitXstar", vec(w[0]["x_star"]))
    mac("WitBetter", vec(w[0]["better_x"]))
    mac("WitGap", f"{w[0]['gap']:.3f}")
    mac("HasWitness", "1")
else:
    mac("HasWitness", "0")

# E2c non-polyhedral example
npx = wf.get("E2_nonpolyhedral")
if npx:
    sm = npx["strongly_monotone_variant"]
    mac("NPslicePts", npx["slice_points"]); mac("NPmismatch", npx["slice_mismatches"])
    mac("NPbisDiff", sci(npx["max_abs_bisection_minus_parabola"]))
    mac("NPwitGap", f"{npx['witness_gap']:.5f}")
    mac("NPwitLambda", "(" + ", ".join(f"{t:g}" for t in npx["witness_lambda"]) + ")")
    mac("NPwitX", "(" + ", ".join(f"{t:g}" for t in npx["witness_better_x"]) + ")")
    mac("NPresidual", sci(npx["residual_at_x_star"]))
    mac("NPsmEps", f"{sm['eps']:g}"); mac("NPsmMu", f"{sm['mu']:g}"); mac("NPsmNpts", len(sm["lambda1_grid"]))
    mac("NPsmLow", f"{sm['lambda1_grid'][0]:g}"); mac("NPsmHigh", f"{sm['lambda1_grid'][-1]:g}")
    mac("NPsmPhiDiff", sci(sm["max_abs_boundary_minus_phi"]))
    mac("HasNP", "1")
else:
    mac("HasNP", "0")

# E5 commodity cones
if cm:
    fx, ag = cm["E5a_fixed"], cm["E5b_random"]
    mac("CmDirs", fx["n_dirs"]); mac("CmDirsInLone", fx["dirs_in_L1"]); mac("CmDirsInL", fx["dirs_in_L"])
    mac("CmResidual", sci(fx["residual"]))
    mac("CmBoundary", f"{fx['boundary_lambda1_at_lambda2_1']:.6f}")
    mac("CmBoundaryInv", f"{1.0 / fx['boundary_lambda1_at_lambda2_1']:.3f}")
    mac("CmWitGap", f"{fx['witness_lambda_0_1']['gap']:.4f}")
    mac("CmWitY", "(" + ", ".join(f"{t:.4g}" for t in fx["witness_lambda_0_1"]["better_y"]) + ")")
    mac("CmCostsEq", "(" + ", ".join(f"{t:.4g}" for t in fx["costs_at_eq"]) + ")")
    mac("CmCostsWit", "(" + ", ".join(f"{t:.4g}" for t in fx["witness_lambda_0_1"]["costs_at_better_y"]) + ")")
    mac("CmRandInst", ag["instances"]); mac("CmRandCorner", ag["corner_equilibria"])
    mac("CmRandLoneAny", ag["dirs_in_L1_any"]); mac("CmRandLoneFull", ag["L1_full_orthant"])
    mac("CmRandWit", ag["witness_instances"]); mac("CmRandViol", ag["violations_L_not_L1"])
    mac("CmRandTolDis", ag["tolerance_disagreements"])
    mac("CmRandTolDisViol", sci(ag["max_tolerance_disagreement_violation"]))
    mac("CmRandMaxRes", sci(ag["max_residual"]))
    mac("CmRandLoneDimTwo", ag["L1_dim2"]); mac("CmRandLoneRay", ag["L1_dim1"])
    mac("CmRandWitInterior", ag["witness_interior_dir_instances"]); mac("CmRandWitAxisOnly", ag["witness_axis_only_instances"])
    bp = ag["by_pattern"]
    mac("CmRandIntInst", bp["interior"]["instances"]); mac("CmRandIntRay", bp["interior"]["L1_dim1"])
    mac("CmRandIntWit", bp["interior"]["witness_instances"])
    mac("HasCommodity", "1")
else:
    mac("HasCommodity", "0")

# E6 MAX-CUT reduction check (v0.3)
_hd_path = os.path.join(ROOT, "results", "results_hardness.json")
if os.path.exists(_hd_path):
    hd = json.load(open(_hd_path))
    mac("CritHardness", crit_phrase(hd.get("criteria")))
    mac("HdPairs", hd["total_pairs"]); mac("HdMism", hd["total_mismatches"])
    mac("HdGraphs", sum(f["graphs"] for f in hd["families"]))
    mac("HdMember", sum(f["member_cases"] for f in hd["families"]))
    mac("HdNonmember", sum(f["nonmember_cases"] for f in hd["families"]))
    mac("HdEps", f"{hd['eps']:g}")
    mac("HdXcheck", hd["crosscheck_vertices_vs_faces"]["cases"])
    mac("MetaSecondsHardness", f"{hd['meta']['seconds']:.0f}")
    mac("HasHardness", "1")
else:
    mac("HasHardness", "0")

# E7 three-commodity example (v0.3)
_tc_path = os.path.join(ROOT, "results", "results_three_commodity.json")
if os.path.exists(_tc_path):
    tc = json.load(open(_tc_path))
    t7 = tc["E7"]
    mac("CritThree", crit_phrase(tc.get("criteria")))
    mac("TcResidual", sci(t7["residual"]))
    mac("TcBoundaryDiff", sci(t7["max_abs_boundary_minus_psi"]))
    mac("TcSlicePts", len(t7["slice_grid"]))
    mac("TcDescTests", t7["description_tests"]); mac("TcDescMism", t7["description_mismatches"])
    mac("TcWitGap", f"{t7['witness_gap']:.10f}")
    mac("MetaSecondsThree", f"{tc['meta']['seconds']:.0f}")
    mac("HasThree", "1")
else:
    mac("HasThree", "0")

with open(os.path.join(OUT, "numbers.tex"), "w") as fh:
    fh.write("% generated by experiments/make_numbers.py -- do not edit\n")
    fh.write("\n".join(L) + "\n")
print(f"wrote numbers.tex ({len(L)} macros) and table bodies")
