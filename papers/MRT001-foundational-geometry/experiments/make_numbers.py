#!/usr/bin/env python3
"""Turn results/results.json into LaTeX macros and table bodies for main.tex."""
import json
import os

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
res = json.load(open(os.path.join(ROOT, "results", "results.json")))
out_dir = os.path.join(ROOT, "manuscript")


def sci(x, digits=1):
    if x == 0:
        return r"\ensuremath{0}"
    e = int(f"{x:e}".split("e")[1])
    m = x / 10 ** e
    if digits == 0:
        return rf"\ensuremath{{10^{{{e}}}}}"
    return rf"\ensuremath{{{m:.{digits}f}\times 10^{{{e}}}}}"


def word(n):
    return {8: "eight", 16: "sixteen", 32: "thirtytwo", 64: "sixtyfour",
            128: "onetwentyeight", 256: "twofiftysix"}[n]


L = []
m = res["meta"]
L.append(rf"\newcommand{{\MetaSeed}}{{{m['seed']}}}")
L.append(rf"\newcommand{{\MetaPython}}{{{m['python']}}}")
L.append(rf"\newcommand{{\MetaNumpy}}{{{m['numpy']}}}")
L.append(rf"\newcommand{{\MetaScipy}}{{{m['scipy']}}}")
L.append(rf"\newcommand{{\MetaSklearn}}{{{m['sklearn']}}}")
L.append(rf"\newcommand{{\MetaSeconds}}{{{int(round(m['seconds']))}}}")

# E1
e1 = res["E1"]
rows = e1["random"]
L.append(rf"\newcommand{{\EoneConfigs}}{{{rows[0]['configurations']}}}")
L.append(rf"\newcommand{{\EoneSettings}}{{{len(rows)}}}")
L.append(rf"\newcommand{{\EoneTotalConfigs}}{{{sum(r['configurations'] for r in rows)}}}")
L.append(rf"\newcommand{{\EoneBetweenTotal}}{{{sum(r['betweenness_instances'] for r in rows)}}}")
L.append(rf"\newcommand{{\EoneCongTotal}}{{{sum(r['congruence_instances'] for r in rows)}}}")
L.append(rf"\newcommand{{\EoneGridExp}}{{30}}")
with open(os.path.join(out_dir, "table_e1.tex"), "w") as fh:
    for r in rows:
        fh.write(f"{r['n']} & {r['d']} & {r['configurations']} & "
                 f"{r['betweenness_instances']} & {r['congruence_instances']} \\\\\n")
with open(os.path.join(out_dir, "table_e1_controls.tex"), "w") as fh:
    for r in e1["controls"]:
        g = r['grid'].replace("x", r"$\times$")
        fh.write(f"{g} & {r['n']} & {r['betweenness_instances']} & "
                 f"{r['congruence_instances']} \\\\\n")

# E2
e2 = res["E2"]
import math
with open(os.path.join(out_dir, "table_e2.tex"), "w") as fh:
    prev = {}
    for r in e2["recovery"]:
        loc = "--"
        if r["d"] in prev:
            pn, pm = prev[r["d"]]
            loc = f"{-math.log(r['median_disparity'] / pm) / math.log(r['n'] / pn):.1f}"
        prev[r["d"]] = (r["n"], r["median_disparity"])
        fh.write(f"{r['d']} & {r['n']} & {r['repetitions']} & {sci(r['median_disparity'])} & "
                 f"{sci(r['q1'])} & {sci(r['q3'])} & {sci(r['max'])} & {sci(r['median_discordance'])} & {loc} \\\\\n")
for r in e2["recovery"]:
    tag = ("Dtwo" if r["d"] == 2 else "Dthree") + "N" + word(r["n"])
    L.append(rf"\newcommand{{\EtwoMed{tag}}}{{{sci(r['median_disparity'])}}}")
    L.append(rf"\newcommand{{\EtwoMax{tag}}}{{{sci(r['max'])}}}")
d2 = [r for r in e2["recovery"] if r["d"] == 2]
d3 = [r for r in e2["recovery"] if r["d"] == 3]
L.append(rf"\newcommand{{\EtwoRepsDtwo}}{{{d2[0]['repetitions']}}}")
L.append(rf"\newcommand{{\EtwoRepsDthree}}{{{d3[0]['repetitions']}}}")
L.append(rf"\newcommand{{\EtwoNmaxDtwo}}{{{d2[-1]['n']}}}")
L.append(rf"\newcommand{{\EtwoNmaxDthree}}{{{d3[-1]['n']}}}")
L.append(rf"\newcommand{{\EtwoMedDtwoFirst}}{{{sci(d2[0]['median_disparity'])}}}")
L.append(rf"\newcommand{{\EtwoMedDtwoLast}}{{{sci(d2[-1]['median_disparity'])}}}")
L.append(rf"\newcommand{{\EtwoMaxDtwoLast}}{{{sci(d2[-1]['max'])}}}")
L.append(rf"\newcommand{{\EtwoMedDthreeFirst}}{{{sci(d3[0]['median_disparity'])}}}")
L.append(rf"\newcommand{{\EtwoMedDthreeLast}}{{{sci(d3[-1]['median_disparity'])}}}")
L.append(rf"\newcommand{{\EtwoTotalRuns}}{{{sum(r['repetitions'] for r in e2['recovery'])}}}")
L.append(rf"\newcommand{{\EtwoDiscDtwoLast}}{{{sci(d2[-1]['median_discordance'])}}}")
L.append(rf"\newcommand{{\EtwoDiscDtwoFirst}}{{{sci(d2[0]['median_discordance'])}}}")
L.append(rf"\newcommand{{\EtwoDiscDthreeLast}}{{{sci(d3[-1]['median_discordance'])}}}")
L.append(rf"\newcommand{{\EtwoDropDtwo}}{{{math.log10(d2[0]['median_disparity'] / d2[-1]['median_disparity']):.1f}}}")
L.append(rf"\newcommand{{\EtwoDropDthree}}{{{math.log10(d3[0]['median_disparity'] / d3[-1]['median_disparity']):.1f}}}")
loc2 = [(-math.log(b['median_disparity']/a['median_disparity'])/math.log(b['n']/a['n'])) for a, b in zip(d2, d2[1:])]
L.append(rf"\newcommand{{\EtwoLocMaxDtwo}}{{{max(loc2):.1f}}}")
L.append(rf"\newcommand{{\EtwoLocMinDtwo}}{{{min(loc2):.1f}}}")
b = e2["distortion"]
L.append(rf"\newcommand{{\EtwoBn}}{{{b['n']}}}")
L.append(rf"\newcommand{{\EtwoBreps}}{{{b['repetitions']}}}")
L.append(rf"\newcommand{{\EtwoBpreserved}}{{{b['ordinal_pattern_preserved_by_distortion']}}}")
L.append(rf"\newcommand{{\EtwoBmetricTrue}}{{{sci(b['metric_mds_on_true_metric_median_disparity_to_X'])}}}")
L.append(rf"\newcommand{{\EtwoBmetricDist}}{{{sci(b['metric_mds_on_distorted_metric_median_disparity_to_X'])}}}")
L.append(rf"\newcommand{{\EtwoBmetricDistMin}}{{{sci(b['metric_mds_on_distorted_metric_min_disparity_to_X'])}}}")
L.append(rf"\newcommand{{\EtwoBordMax}}{{{sci(b['nonmetric_mds_true_vs_distorted_max_disparity'])}}}")

# E3
e3 = res["E3"]
for k, v in e3["n4_patterns"].items():
    tag = {"d=1": "Done", "d=2": "Dtwo", "d=3": "Dthree"}[k]
    L.append(rf"\newcommand{{\EthreePatterns{tag}}}{{{v['distinct_patterns_observed']}}}")
    L.append(rf"\newcommand{{\EthreeLeast{tag}}}{{{v['least_frequent_pattern_count']}}}")
L.append(rf"\newcommand{{\EthreeSamples}}{{{e3['n4_patterns']['d=2']['samples']:,}}}".replace(",", r"\,"))
t = e3["triangle_example"]
L.append(rf"\newcommand{{\EthreeTriAnglesA}}{{{', '.join(f'{a:.1f}' for a in t[0]['angles_deg'])}}}")
L.append(rf"\newcommand{{\EthreeTriAnglesB}}{{{', '.join(f'{a:.1f}' for a in t[1]['angles_deg'])}}}")

# E4
e4 = res["E4"]
L.append(rf"\newcommand{{\EfourTrials}}{{{e4['trials']}}}")
L.append(rf"\newcommand{{\EfourN}}{{{e4['n']}}}")
names = {"centroid": "centroid (position)", "diameter_value": "diameter (value)",
         "affine_dimension": "affine dimension", "gabriel_graph": "Gabriel graph",
         "diameter_pair": "diameter pair",
         "knn_graph_k3": "$k$-nearest-neighbour graph ($k=3$)", "mst_edges": "minimum spanning tree",
         "rng_graph": "relative neighbourhood graph"}
depth = {"centroid": "coordinate", "diameter_value": "metric", "affine_dimension": "metric",
         "gabriel_graph": "metric", "diameter_pair": "ordinal", "knn_graph_k3": "ordinal",
         "mst_edges": "ordinal", "rng_graph": "ordinal"}
with open(os.path.join(out_dir, "table_e4.tex"), "w") as fh:
    for r in e4["table"]:
        f = lambda v: "--" if v is None else f"{v:.2f}"
        fh.write(f"{names[r['quantity']]} & {depth[r['quantity']]} & {f(r['rigid'])} & "
                 f"{f(r['similarity'])} & {f(r['monotone'])} \\\\\n")
aff = [r for r in e4["table"] if r["quantity"] == "affine_dimension"][0]
L.append(rf"\newcommand{{\EfourAffMono}}{{{aff['monotone']:.2f}}}")
gab = [r for r in e4["table"] if r["quantity"] == "gabriel_graph"][0]
L.append(rf"\newcommand{{\EfourGabrielMono}}{{{gab['monotone']:.2f}}}")
e4b = res.get("E4b")
if e4b:
    yes = lambda b: "yes" if b else "no"
    L.append(rf"\newcommand{{\EfourbCollinearSame}}{{{yes(e4b['collinear']['pattern_equal'])}}}")
    L.append(rf"\newcommand{{\EfourbCollinearDims}}{{{e4b['collinear']['affine_dimension'][0]} and {e4b['collinear']['affine_dimension'][1]}}}")
    L.append(rf"\newcommand{{\EfourbGabrielSame}}{{{yes(e4b['gabriel']['pattern_equal'])}}}")
    L.append(rf"\newcommand{{\EfourbGabrielEdges}}{{{yes(e4b['gabriel']['edge_12_present'][0])} and {yes(e4b['gabriel']['edge_12_present'][1])}}}")

# E2 empirical log-log slopes of the median disparity against n
import numpy as np
for d, tag in ((2, "Dtwo"), (3, "Dthree")):
    sel = [r for r in e2["recovery"] if r["d"] == d and r["n"] >= 16]
    x = np.log([r["n"] for r in sel]); y = np.log([r["median_disparity"] for r in sel])
    slope = np.polyfit(x, y, 1)[0]
    L.append(rf"\newcommand{{\EtwoSlope{tag}}}{{{-slope:.1f}}}")

# E5 (Lorentzian chain), if available
lz_path = os.path.join(ROOT, "results", "results_lorentz.json")
if os.path.exists(lz_path):
    lz = json.load(open(lz_path))
    a = lz["E5a"]
    L.append(rf"\newcommand{{\EfiveAn}}{{{a['n']}}}")
    L.append(rf"\newcommand{{\EfiveAtrials}}{{{a['trials']}}}")
    L.append(rf"\newcommand{{\EfiveAconfPreserved}}{{{a['conformal_order_preserved']}}}")
    L.append(rf"\newcommand{{\EfiveAconfTauChange}}{{{100*a['conformal_median_relative_tau_change']:.0f}}}")
    L.append(rf"\newcommand{{\EfiveAboostPreserved}}{{{a['boost_order_preserved']}}}")
    import math
    L.append(rf"\newcommand{{\EfiveAboostTauChange}}{{\ensuremath{{10^{{{math.ceil(math.log10(a['boost_max_relative_tau_change']))}}}}}}}")
    L.append(rf"\newcommand{{\EfiveArotChanged}}{{{100*a['rotation_median_fraction_of_pairs_changed']:.1f}}}")
    L.append(rf"\newcommand{{\EfiveArotChangedMin}}{{{100*a['rotation_min_fraction_of_pairs_changed']:.1f}}}")
    with open(os.path.join(out_dir, "table_e5b.tex"), "w") as fh:
        for r in lz["E5b"]:
            fh.write(f"{r['D']} & {r['n']} & {r['repetitions']} & ${r['ordering_fraction_mean']:.4f} \\pm {r['ordering_fraction_sd']:.4f}$ & "
                     f"{r['expected_fraction']:.4f} & ${r['dimension_estimate_mean']:.2f} \\pm {r['dimension_estimate_sd']:.2f}$ \\\\\n")
    L.append(rf"\newcommand{{\EfiveBn}}{{{lz['E5b'][0]['n']}}}")
    L.append(rf"\newcommand{{\EfiveBreps}}{{{lz['E5b'][0]['repetitions']}}}")
    c = lz["E5c"]
    with open(os.path.join(out_dir, "table_e5c.tex"), "w") as fh:
        for r in c:
            fh.write(f"{r['n']} & {r['pairs']} & {r['corr_L_tau']:.3f} & {r['corr_L_tau_distorted']:.3f} & "
                     f"{r['slope_L_vs_sqrtn_tau']:.3f} & {r['median_rel_err_tau_hat_tau_gt_quarter']:.3f} & "
                     f"{r['median_rel_err_vs_distorted_tau_gt_quarter']:.3f} \\\\\n")
    L.append(rf"\newcommand{{\EfiveCnmin}}{{{c[0]['n']}}}")
    L.append(rf"\newcommand{{\EfiveCnmax}}{{{c[-1]['n']}}}")
    L.append(rf"\newcommand{{\EfiveCpairsTotal}}{{{sum(r['pairs'] for r in c):,}}}".replace(",", r"\,"))
    L.append(rf"\newcommand{{\EfiveCcorrLast}}{{{c[-1]['corr_L_tau']:.3f}}}")
    L.append(rf"\newcommand{{\EfiveCcorrDistLast}}{{{c[-1]['corr_L_tau_distorted']:.2f}}}")
    L.append(rf"\newcommand{{\EfiveCslopeFirst}}{{{c[0]['slope_L_vs_sqrtn_tau']:.2f}}}")
    L.append(rf"\newcommand{{\EfiveCslopeLast}}{{{c[-1]['slope_L_vs_sqrtn_tau']:.2f}}}")
    L.append(rf"\newcommand{{\EfiveCerrFirst}}{{{100*c[0]['median_rel_err_tau_hat_tau_gt_quarter']:.0f}}}")
    L.append(rf"\newcommand{{\EfiveCerrLast}}{{{100*c[-1]['median_rel_err_tau_hat_tau_gt_quarter']:.0f}}}")
    L.append(rf"\newcommand{{\EfiveCerrDistLast}}{{{100*c[-1]['median_rel_err_vs_distorted_tau_gt_quarter']:.0f}}}")
    L.append(rf"\newcommand{{\EfiveCerrDistFirst}}{{{100*c[0]['median_rel_err_vs_distorted_tau_gt_quarter']:.0f}}}")
    dd = lz["E5d"]
    with open(os.path.join(out_dir, "table_e5d.tex"), "w") as fh:
        for r in dd:
            fh.write(f"{r['n']} & {r['repetitions']} & {r['rmse_median']:.4f} & {r['rmse_max']:.4f} & "
                     f"{r['rmse_times_sqrt_n']:.2f} & {100*r['order_disagreement_median']:.2f}\\% \\\\\n")
    L.append(rf"\newcommand{{\EfiveDnmin}}{{{dd[0]['n']}}}")
    L.append(rf"\newcommand{{\EfiveDnmax}}{{{dd[-1]['n']}}}")
    L.append(rf"\newcommand{{\EfiveDrmseFirst}}{{{dd[0]['rmse_median']:.3f}}}")
    L.append(rf"\newcommand{{\EfiveDrmseLast}}{{{dd[-1]['rmse_median']:.3f}}}")
    L.append(rf"\newcommand{{\EfiveDsqrtFirst}}{{{dd[0]['rmse_times_sqrt_n']:.2f}}}")
    L.append(rf"\newcommand{{\EfiveDsqrtLast}}{{{dd[-1]['rmse_times_sqrt_n']:.2f}}}")
    L.append(rf"\newcommand{{\EfiveDdisagreeLast}}{{{100*dd[-1]['order_disagreement_median']:.2f}}}")
    import numpy as _np
    _x = _np.log([r['n'] for r in dd]); _y = _np.log([r['rmse_median'] for r in dd])
    L.append(rf"\newcommand{{\EfiveDexponent}}{{{-_np.polyfit(_x, _y, 1)[0]:.2f}}}")
    L.append(rf"\newcommand{{\EfiveDdisagreeFirst}}{{{100*dd[0]['order_disagreement_median']:.2f}}}")
    L.append(rf"\newcommand{{\EfiveSeconds}}{{{int(round(lz['meta']['seconds']))}}}")
    L.append(r"\newcommand{\HasLorentz}{1}")

import glob
for t in glob.glob(os.path.join(out_dir, "table_*.tex")):
    body = open(t).read().rstrip()
    if body.endswith("\\\\"):
        body = body[:-2].rstrip()
    open(t, "w").write(body + "\n")

# E2c (ordinal class), if available
cls_path = os.path.join(ROOT, "results", "results_class.json")
if os.path.exists(cls_path):
    cl = json.load(open(cls_path))
    rows_c = cl["rows"]
    rows_tex = []
    for r in rows_c:
        rows_tex.append(f"{r['n']} & {r['configurations']} & {sci(r['gap_median'])} & "
                        f"{r['disjoint_extremal_pairs']}/{r['configurations']} & "
                        f"{r['perturbations_below_quarter_gap_kept']}/{r['perturbations_total']} & "
                        f"{r['quarter_gap_displacement_changed']}/{r['quarter_gap_displacement_tested']} & "
                        f"{sci(r['walk_radius_median'])}")
    with open(os.path.join(out_dir, "table_e2c.tex"), "w") as fh:
        fh.write(" \\\\\n".join(rows_tex) + "\n")     # last row without terminator
    L.append(rf"\newcommand{{\EtwocSlopeGap}}{{{-cl['slope_gap']:.1f}}}")
    L.append(rf"\newcommand{{\EtwocSlopeWalk}}{{{-cl['slope_walk_radius']:.1f}}}")
    L.append(rf"\newcommand{{\EtwocNmax}}{{{rows_c[-1]['n']}}}")
    L.append(rf"\newcommand{{\EtwocConfigsTotal}}{{{sum(r['configurations'] for r in rows_c)}}}")
    L.append(rf"\newcommand{{\EtwocKeptTotal}}{{{sum(r['perturbations_below_quarter_gap_kept'] for r in rows_c)}}}")
    L.append(rf"\newcommand{{\EtwocPertTotal}}{{{sum(r['perturbations_total'] for r in rows_c)}}}")
    L.append(rf"\newcommand{{\EtwocChangedTotal}}{{{sum(r['quarter_gap_displacement_changed'] for r in rows_c)}}}")
    L.append(rf"\newcommand{{\EtwocChangedTested}}{{{sum(r['quarter_gap_displacement_tested'] for r in rows_c)}}}")
    for r in rows_c:
        if r["n"] == 64:
            L.append(rf"\newcommand{{\EtwocGapNsixtyfour}}{{{sci(r['gap_median'])}}}")
            L.append(rf"\newcommand{{\EtwocWalkNsixtyfour}}{{{sci(r['walk_radius_median'])}}}")
    L.append(rf"\newcommand{{\EtwocGapNmax}}{{{sci(rows_c[-1]['gap_median'])}}}")
    L.append(rf"\newcommand{{\EtwocWalkNmax}}{{{sci(rows_c[-1]['walk_radius_median'])}}}")
    L.append(rf"\newcommand{{\EtwocSeconds}}{{{int(round(cl['meta']['seconds']))}}}")
    L.append(r"\newcommand{\HasClass}{1}")
    # solver disparity at n = 64 from E2, for the comparison sentence
    for r in e2["recovery"]:
        if r["d"] == 2 and r["n"] == 64:
            L.append(rf"\newcommand{{\EtwoMedDtwoNsixtyfourAgain}}{{{sci(r['median_disparity'])}}}")
            L.append(rf"\newcommand{{\EtwoDiscDtwoNsixtyfour}}{{{sci(r['median_discordance'])}}}")

with open(os.path.join(out_dir, "numbers.tex"), "w") as fh:
    fh.write("% generated by experiments/make_numbers.py -- do not edit\n")
    fh.write("\n".join(L) + "\n")
print("wrote numbers.tex and table bodies")
