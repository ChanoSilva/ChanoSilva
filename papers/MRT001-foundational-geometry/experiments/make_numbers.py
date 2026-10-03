#!/usr/bin/env python3
"""Turn results/results.json into LaTeX macros and table bodies for main.tex."""
import json
import math
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


def up(x, d):
    """Round upwards to d decimals (for quantities presented as upper bounds; round 5, m4)."""
    return f"{math.ceil(x * 10 ** d - 1e-9) / 10 ** d:.{d}f}"


def down(x, d):
    """Round downwards to d decimals (for quantities presented as lower bounds)."""
    return f"{math.floor(x * 10 ** d + 1e-9) / 10 ** d:.{d}f}"


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
    if "rmse_median_unrelated_votes_only" in dd[-1]:
        a_all, a_inc = dd[-1]["rmse_median"], dd[-1]["rmse_median_unrelated_votes_only"]
        rel = 100.0 * (a_inc - a_all) / a_all
        # always print the signed percentage (round 3: no verbal substitute for the number)
        L.append(rf"\newcommand{{\EfiveDablation}}{{{rel:+.1f}\%}}")
        L.append(rf"\newcommand{{\EfiveDrmseLastFour}}{{{a_all:.4f}}}")
        L.append(rf"\newcommand{{\EfiveDrmseAblLastFour}}{{{a_inc:.4f}}}")
    if "E5e" in lz:
        e5e = lz["E5e"]
        rows_e = e5e["rows"]
        with open(os.path.join(out_dir, "table_e5e.tex"), "w") as fh:
            body = []
            for r in rows_e:
                body.append(f"{r['n']} & {r['samples']} & {r['not_enumerated']} & {r['fraction_unique']:.2f} & "
                            f"{r['fraction_two']:.2f} & {r['fraction_le_eight']:.2f} & {r['median_colour_classes']:.0f}")
            fh.write(" \\\\\n".join(body) + "\n")
        L.append(rf"\newcommand{{\EfiveEnmax}}{{{rows_e[-1]['n']}}}")
        L.append(rf"\newcommand{{\EfiveEuniqueNmax}}{{{rows_e[-1]['fraction_unique']:.2f}}}")
        L.append(rf"\newcommand{{\EfiveEleEightNmax}}{{{rows_e[-1]['fraction_le_eight']:.2f}}}")
        L.append(rf"\newcommand{{\EfiveEtwoNmax}}{{{rows_e[-1]['fraction_two']:.2f}}}")
        L.append(rf"\newcommand{{\EfiveEmaxCountNten}}{{{rows_e[0]['max_count']}}}")
        L.append(rf"\newcommand{{\EfiveEcrossAgree}}{{{e5e['crosscheck_n6_agree']}}}")
        L.append(rf"\newcommand{{\EfiveEcrossTested}}{{{e5e['crosscheck_n6_tested']}}}")
    L.append(rf"\newcommand{{\EfiveSeconds}}{{{int(round(lz['meta']['seconds']))}}}")
    L.append(r"\newcommand{\HasLorentz}{1}")

# E5f (law of the realizer count), if available
rl_path = os.path.join(ROOT, "results", "results_realizer_law.json")
if os.path.exists(rl_path):
    rl = json.load(open(rl_path))
    rr = rl["rows"]
    # v0.6: observed exception rate against the first-order value 5/n of Proposition prop:exceptions
    def exc_frac(r):
        return (r['samples'] - r['equal_to_two_pow_N']) / r['samples']
    with open(os.path.join(out_dir, "table_e5f.tex"), "w") as fh:
        body = []
        for r in rr:
            body.append(f"{r['n']} & {r['samples']} & {r['equal_to_two_pow_N']}/{r['samples']} & {r['mean_N']:.2f} & "
                        f"{r['fraction_unique']:.2f} & {r['fraction_two']:.2f} & {r['fraction_le_eight']:.2f}")
        fh.write(" \\\\\n".join(body) + "\n")
    from fractions import Fraction as _Fr

    def ratio_set(rows):
        s = sorted({_Fr(e['count'], 2 ** e['N']) for r in rows for e in r['exceptions']})
        out = [rf"$\tfrac{{{q.numerator}}}{{{q.denominator}}}$" if q.denominator > 1 else f"${q.numerator}$" for q in s]
        return ", ".join(out[:-1]) + " and " + out[-1] if len(out) > 1 else out[0]
    L.append(rf"\newcommand{{\RlawExcFirst}}{{{exc_frac(rr[0]):.3f}}}")
    L.append(rf"\newcommand{{\RlawFiveNFirst}}{{{5 / rr[0]['n']:.3f}}}")
    _big = [r for r in rr if r["n"] >= 100]
    L.append(rf"\newcommand{{\RlawExcBig}}{{{sum(r['samples'] - r['equal_to_two_pow_N'] for r in _big)}}}")
    L.append(rf"\newcommand{{\RlawExcBigExpected}}{{{sum(r['samples'] * 5 / r['n'] for r in _big):.1f}}}")
    L.append(rf"\newcommand{{\RlawRatiosAll}}{{{ratio_set(rr)}}}")
    L.append(rf"\newcommand{{\RlawRatiosBig}}{{{ratio_set(_big)}}}")
    last = rr[-1]
    L.append(rf"\newcommand{{\RlawNmin}}{{{rr[0]['n']}}}")
    L.append(rf"\newcommand{{\RlawNmax}}{{{last['n']}}}")
    L.append(rf"\newcommand{{\RlawSamplesNmax}}{{{last['samples']}}}")
    L.append(rf"\newcommand{{\RlawEqualNmax}}{{{last['equal_to_two_pow_N']}}}")
    L.append(rf"\newcommand{{\RlawEqualFracNmin}}{{{rr[0]['fraction_equal']:.2f}}}")
    L.append(rf"\newcommand{{\RlawEqualTotal}}{{{rl['total_equal']}}}")
    L.append(rf"\newcommand{{\RlawSamplesTotal}}{{{rl['total_samples']}}}")
    big = [r for r in rr if r["n"] >= 100]
    L.append(rf"\newcommand{{\RlawBigNmin}}{{{big[0]['n']}}}")
    L.append(rf"\newcommand{{\RlawEqualBig}}{{{sum(r['equal_to_two_pow_N'] for r in big)}}}")
    L.append(rf"\newcommand{{\RlawSamplesBig}}{{{sum(r['samples'] for r in big)}}}")
    p = rl["poisson_predictions"]
    L.append(rf"\newcommand{{\RlawPoissonOne}}{{{p['P_N_eq_0']:.3f}}}")
    L.append(rf"\newcommand{{\RlawPoissonLeThree}}{{{p['P_N_le_3']:.3f}}}")
    L.append(rf"\newcommand{{\RlawSeconds}}{{{int(round(rl['meta']['seconds']))}}}")
    L.append(r"\newcommand{\HasRlaw}{1}")

# v0.6: frozen output of theory/check_realizer_law.py (numerical check of the proof of the
# realizer law), read only after its SHA-256 matches the recorded one
chk_path = os.path.join(ROOT, "results", "check_realizer_law_output.txt")
chk_sha_path = os.path.join(ROOT, "results", "check_realizer_law_output.sha256")
if os.path.exists(chk_path) and os.path.exists(chk_sha_path):
    import hashlib
    import re
    raw = open(chk_path, "rb").read()
    sha = hashlib.sha256(raw).hexdigest()
    recorded = open(chk_sha_path).read().split()[0]
    if sha != recorded:
        raise SystemExit(f"check_realizer_law_output.txt: SHA-256 {sha} != recorded {recorded}")
    txt = raw.decode()
    rows_b = re.findall(r"^(\d+) \| (\d+) \| [\d.]+ \| [\d.]+ \| [\d.]+ \([\d., ]+\) \| [\d.]+ \| [\d.]+ \| ([\d.]+) \|",
                        txt, flags=re.M)
    nP = [float(x[2]) for x in rows_b]
    L.append(rf"\newcommand{{\RlawChkNlo}}{{{rows_b[0][0]}}}")
    L.append(rf"\newcommand{{\RlawChkNhi}}{{{rows_b[-1][0]}}}")
    L.append(rf"\newcommand{{\RlawChkNPlo}}{{{min(nP):.2f}}}")
    L.append(rf"\newcommand{{\RlawChkNPhi}}{{{max(nP):.2f}}}")
    L.append(rf"\newcommand{{\RlawChkSamplesMin}}{{{min(int(x[1]) for x in rows_b)}}}")
    L.append(rf"\newcommand{{\RlawChkSamplesMax}}{{{max(int(x[1]) for x in rows_b)}}}")
    brute = re.findall(r"^n=(\d+): (\d+) perms \| mismatches formula vs lc.brute_force: (\S+), vs u-order brute force: (\d+)",
                       txt, flags=re.M)
    L.append(rf"\newcommand{{\RlawChkBruteNmax}}{{{max(int(b[0]) for b in brute)}}}")
    L.append(rf"\newcommand{{\RlawChkBrutePerms}}{{{sum(int(b[1]) for b in brute)}}}")
    L.append(rf"\newcommand{{\RlawChkBruteMismatch}}{{{sum(int(b[3]) + (int(b[2]) if b[2].isdigit() else 0) for b in brute)}}}")
    gal = re.findall(r"^Gallai check n=(\d+): (\d+) simple permutations .*?; R != 1 in (\d+)", txt, flags=re.M)
    L.append(rf"\newcommand{{\RlawChkGallaiNmax}}{{{max(int(g[0]) for g in gal)}}}")
    L.append(rf"\newcommand{{\RlawChkGallaiSimple}}{{{sum(int(g[1]) for g in gal)}}}")
    L.append(rf"\newcommand{{\RlawChkGallaiBad}}{{{sum(int(g[2]) for g in gal)}}}")
    ndtv = sorted({x for x in re.findall(r"n\*d_TV = ([\d.]+)", txt)})
    L.append(rf"\newcommand{{\RlawChkNdTV}}{{{ndtv[0] if len(ndtv) == 1 else ndtv[0] + '--' + ndtv[-1]}}}")
    sn_ratio = re.search(r"max ratio = ([\d.]+)", txt).group(1)
    chk_seconds = int(round(float(re.search(r"^total ([\d.]+) s", txt, flags=re.M).group(1))))
    L.append(rf"\newcommand{{\RlawChkSnRatio}}{{{sn_ratio}}}")
    L.append(rf"\newcommand{{\RlawChkSeconds}}{{{chk_seconds}}}")
    L.append(rf"\newcommand{{\RlawChkSha}}{{{sha[:16]}}}")
    # v0.7 (round 4, m2): the two brute-force counts cover n <= 6 only; n = 7 has one of them
    two = [b for b in brute if b[2].isdigit()]
    one = [b for b in brute if not b[2].isdigit()]
    L.append(rf"\newcommand{{\RlawChkBruteTwoNmax}}{{{max(int(b[0]) for b in two)}}}")
    L.append(rf"\newcommand{{\RlawChkBruteTwoPerms}}{{{sum(int(b[1]) for b in two)}}}")
    L.append(rf"\newcommand{{\RlawChkBruteOneN}}{{{', '.join(b[0] for b in one)}}}")
    L.append(rf"\newcommand{{\RlawChkBruteOnePerms}}{{{sum(int(b[1]) for b in one)}}}")
    # v0.7 (round 4, m3): 95% confidence intervals of n P(R_n != 2^N_n)
    ci_rows = re.findall(r"^(\d+) \| (\d+) \| [\d.]+ \| [\d.]+ \| ([\d.]+) \(([\d.]+), ([\d.]+)\) \|", txt, flags=re.M)
    cis = [(int(a), int(a) * float(lo), int(a) * float(hi)) for a, _, _, lo, hi in ci_rows]
    L.append(rf"\newcommand{{\RlawChkCIrows}}{{{len(cis)}}}")
    L.append(rf"\newcommand{{\RlawChkCIcontainFive}}{{{sum(1 for _, lo, hi in cis if lo <= 5 <= hi)}}}")
    L.append(rf"\newcommand{{\RlawChkCIfirst}}{{$[{cis[0][1]:.2f},{cis[0][2]:.2f}]$}}")
    L.append(rf"\newcommand{{\RlawChkCIlast}}{{$[{cis[-1][1]:.1f},{cis[-1][2]:.1f}]$}}")
    L.append(r"\newcommand{\HasRlawChk}{1}")

# v0.8 (round 5): frozen output of theory/check_second_order.py (second-order results), written by
# experiments/freeze_second_order.py without timing lines; both SHA-256 are verified before reading
so_exact = {}
so_path = os.path.join(ROOT, "results", "check_second_order_output.txt")
so_json_path = os.path.join(ROOT, "results", "second_order_results.json")
so_meta_path = os.path.join(ROOT, "results", "check_second_order_meta.json")
if os.path.exists(so_path) and os.path.exists(so_json_path) and os.path.exists(so_meta_path):
    import hashlib
    import re
    so_raw = open(so_path, "rb").read()
    so_jraw = open(so_json_path, "rb").read()
    so_meta = json.load(open(so_meta_path))
    so_sha = hashlib.sha256(so_raw).hexdigest()
    so_rec = open(os.path.join(ROOT, "results", "check_second_order_output.sha256")).read().split()[0]
    if so_sha != so_rec or so_sha != so_meta["sha256_frozen_output"]:
        raise SystemExit(f"check_second_order_output.txt: SHA-256 {so_sha} != recorded {so_rec}")
    if hashlib.sha256(so_jraw).hexdigest() != so_meta["sha256_frozen_json"]:
        raise SystemExit("second_order_results.json: SHA-256 does not match the meta file")
    so_txt = so_raw.decode()
    sj = json.loads(so_jraw)

    def so_grab(pattern):
        m_ = re.search(pattern, so_txt, re.M)
        if m_ is None:
            raise SystemExit(f"check_second_order_output.txt: pattern not found: {pattern}")
        return m_

    for pat in (r"^A1 .*: OK$", r"^A2 E\[\(N_n\)_r\] .*: mismatches = 0$", r"^A3 sign lemma .*violations = 0$",
                r"^B1 .*: True$", r"^B2 .*agree: True$", r"^B3 .*agree: True$", r"^C2 .*n<=(\d+): True$",
                r"^C3 .*n<=(\d+): True$", r"^E3 n\^2 B\(n\) non-increasing on 22<=n<=(\d+): True$"):
        so_grab(pat)
    if not (sj["S1_maxratio"] <= 1 and 0 < sj["theta_lo"] and sj["theta_hi"] <= 1 and max(sj["E1"]) <= 1
            and sj["E2"] <= 1 and sj["dtvR_ratio_to_bound"] <= 1):
        raise SystemExit("second-order check: a bound of Theorem S1, Lemma intref or Proposition S3 fails")

    def macro(name, val):
        L.append(rf"\newcommand{{\{name}}}{{{val}}}")

    def sci_up(x, sig=2):
        e_ = math.floor(math.log10(abs(x)))
        mant = math.ceil(x / 10 ** e_ * 10 ** (sig - 1) - 1e-9) / 10 ** (sig - 1)
        return rf"\ensuremath{{{mant:.{sig - 1}f}\cdot10^{{{e_}}}}}"

    macro("SecDigits", so_grab(r"computed with (\d+) digits").group(1))
    nl = sj["N_list"]
    run_end = max(i for i in range(len(nl)) if nl[i] == nl[0] + i)
    macro("SecNrange", rf"$\,{nl[0]}\le n\le{nl[run_end]}$ and $n\in\{{{','.join(str(v) for v in nl[run_end + 1:])}\}}$")
    macro("SecLawBruteN", so_grab(r"^A1 closed form = factorial-moment inversion for n<=\d+, = brute force for n<=(\d+)").group(1))
    macro("SecLawNmax", so_grab(r"^A1 closed form = factorial-moment inversion for n<=(\d+)").group(1))
    macro("SecSOneRatio", up(sj["S1_maxratio"], 3))
    macro("SecThetaLo", down(sj["theta_lo"], 3))
    macro("SecThetaHi", up(sj["theta_hi"], 4))
    macro("SecNthousand", str(sj["N1000"]))
    macro("SecNthousandVal", f"{sj['N1000_n2dtv']:.7f}")
    macro("SecNthousandPred", f"{sj['three_over_4e'] + sj['one_over_4e'] / sj['N1000']:.7f}")
    macro("SecThreeFourE", f"{sj['three_over_4e']:.5f}")
    macro("SecOneTwoE", f"{sj['one_over_2e']:.5f}")
    macro("SecBestN", str(sj["best_n"]))
    macro("SecBestA", f"{sj['best_amin']:.4f}")
    macro("SecBestMin", f"{sj['best_min']:.5f}")
    macro("SecExactNmax", so_grab(r"^C1 exact integer generating function up to n=(\d+)").group(1))
    macro("SecGallaiN", so_grab(r"^C2 .*n<=(\d+): True$").group(1))
    macro("SecBruteN", so_grab(r"^C3 .*n<=(\d+): True$").group(1))
    macro("SecFloatNmax", str(sj["NFLOAT"]))
    macro("SecFloatErr", sci_up(sj["gf_float_relerr"]))
    macro("SecRatioB", up(sj["dtvR_ratio_to_bound"], 4))
    macro("SecAtomsMax", up(sj["atoms_max_n2dev"], 2))
    m_ = so_grab(r"^E1 max sum_\{k=4\}\^\{m-2\} E I_k / Fbar\(m\) over (\d+)<=m<=(\d+)")
    macro("SecIntrefMlo", m_.group(1))
    macro("SecIntrefMhi", m_.group(2))
    macro("SecIntrefA", up(sj["E1"][0], 4))
    macro("SecIntrefS", up(sj["E1"][1], 4))
    macro("SecIntrefH", up(sj["E1"][2], 4))
    macro("SecIntrefP", up(sj["E2"], 4))
    macro("SecMonoNhi", so_grab(r"^E3 n\^2 B\(n\) non-increasing on 22<=n<=(\d+): True$").group(1))
    ct = sj["C_table"]
    macro("SecBtwentytwo", f"{ct['22']:.2f}")
    macro("SecBhundred", f"{ct['100']:.2f}")
    macro("SecCtwentytwo", str(math.ceil(ct["22"])))
    macro("SecChundred", str(math.ceil(ct["100"])))
    macro("SecClimit", f"{sj['C_limit']:.2f}")
    macro("SecDtvMaxTT", up(sj["dtvR_max_e2_22"], 2))
    macro("SecDtvMaxAll", up(sj["dtvR_max_e2_all"], 2))
    ke = sj["kappa_est"]
    macro("SecKappa", f"{ke[2]:.5f}")
    macro("SecKappaTwo", f"{ke[0]:.6f}")
    macro("SecKappaThree", f"{ke[1]:.6f}")
    macro("SecKappaFour", f"{ke[2]:.6f}")
    macro("SecKappaConj", f"{sj['kappa_conjecture']:.6f}")
    macro("SecMuTwoDev", sci_up(max(sj["mu2_conj_maxdev"])))
    natoms = len(sj["mu2_est"])
    macro("SecAtomsN", str(natoms))
    macro("SecAtomsK", str(sum(1 for x_ in sj["mu2_est"] if int(x_) & (int(x_) - 1) == 0)))
    macro("SecUntracked", f"{sj['untracked_n2_est']:.6f}")
    macro("SecSeconds", str(int(round(so_meta["seconds"]))))
    macro("SecSha", so_sha[:16])
    # exact n d_TV(R_n, 2^Z) from part (D), used in Table tab:sharp and in the text (round 5, m2)
    for nn_, v_ in re.findall(r"^ +(\d+) +[\d.]+ +([\d.]+) +[+\-][\d.]+ +[\d.]+ +[\d.na]+$", so_txt, flags=re.M):
        so_exact[int(nn_)] = float(v_)
    macro("SecExactFifty", f"{so_exact[50]:.3f}")
    L.append(r"\newcommand{\HasSecond}{1}")

# v0.7 (round 4): frozen output of theory/check_sharp_rate.py (numerical check of the sharp rates),
# read only after its SHA-256 matches the recorded one; the frozen copy has no timing lines
sh_path = os.path.join(ROOT, "results", "check_sharp_rate_output.txt")
sh_sha_path = os.path.join(ROOT, "results", "check_sharp_rate_output.sha256")
sh_meta_path = os.path.join(ROOT, "results", "check_sharp_rate_meta.json")
if os.path.exists(sh_path) and os.path.exists(sh_sha_path) and os.path.exists(sh_meta_path):
    import hashlib
    import re
    raw = open(sh_path, "rb").read()
    sha = hashlib.sha256(raw).hexdigest()
    meta = json.load(open(sh_meta_path))
    recorded = open(sh_sha_path).read().split()[0]
    if sha != recorded or sha != meta["sha256_frozen_output"]:
        raise SystemExit(f"check_sharp_rate_output.txt: SHA-256 {sha} != recorded {recorded}")
    txt = raw.decode()

    def grab(pattern, flags=re.M):
        m_ = re.search(pattern, txt, flags)
        if m_ is None:
            raise SystemExit(f"check_sharp_rate_output.txt: pattern not found: {pattern}")
        return m_

    def tex_sci(x):
        mant, ex = f"{abs(x):.1e}".split("e")
        return rf"\ensuremath{{{mant}\times10^{{{int(ex)}}}}}"

    m_ = grab(r"^n = 1\.\.(\d+): inversion of factorial moments == closed form .*brute force for n <= (\d+)\): (\w+)")
    if m_.group(3) != "True":
        raise SystemExit("sharp check: the three laws of N_n disagree")
    L.append(rf"\newcommand{{\SharpLawNmax}}{{{m_.group(1)}}}")
    L.append(rf"\newcommand{{\SharpLawBruteNmax}}{{{m_.group(2)}}}")
    if grab(r"^n = 1\.\.\d+: E\[\(N_n\)_r\] = 1 - r/n .*: (\w+)").group(1) != "True":
        raise SystemExit("sharp check: factorial moments")
    m_ = grab(r"^all n in \[(\d+), (\d+)\]: bounds and identities hold: (\w+);  max \|r\| n k!\(n-k\+1\)! = ([\d.]+) .*max \|n!\(n d_TV - 1/e\)\| = ([\d.]+)")
    if m_.group(3) != "True":
        raise SystemExit("sharp check: Lemma A / Theorem A bounds fail")
    L.append(rf"\newcommand{{\SharpAnlo}}{{{m_.group(1)}}}")
    L.append(rf"\newcommand{{\SharpAnhi}}{{{m_.group(2)}}}")
    L.append(rf"\newcommand{{\SharpRmax}}{{{up(float(m_.group(4)), 2)}}}")
    L.append(rf"\newcommand{{\SharpDevMax}}{{{up(float(m_.group(5)), 2)}}}")
    dev_min = float(grab(r'^min over n in .* = ([\d.]+)').group(1))
    L.append(rf"\newcommand{{\SharpDevMin}}{{{down(dev_min, 3)}}}")
    for nn, name in ((10, "Ten"), (20, "Twenty")):
        v = float(grab(rf"^{nn:2d} \| [\d.]+ \| True \| True \| [\d.]+ \| ([+\-\d.e]+) \|").group(1))
        L.append(rf"\newcommand{{\SharpDev{name}}}{{{tex_sci(v)}}}")
    three_four_e = float(grab(r'against 3/\(4e\) = ([\d.]+)').group(1))
    L.append(rf"\newcommand{{\SharpThreeFourE}}{{{three_four_e:.4f}}}")
    m_ = grab(r"^  n = +(\d+): n\^2 d_TV\(N_n, Po\(1-1/n\)\) = ([\d.]+)\s*\n(?!  n =)")
    L.append(rf"\newcommand{{\SharpPoShiftN}}{{{m_.group(1)}}}")
    L.append(rf"\newcommand{{\SharpPoShift}}{{{float(m_.group(2)):.4f}}}")
    c2 = float(grab(r"^c_2 = \|mu\|/2 = ([\d.]+);").group(1))
    L.append(rf"\newcommand{{\SharpCtwo}}{{{c2:.3f}}}")
    L.append(rf"\newcommand{{\SharpCtwoLong}}{{{c2:.4f}}}")
    L.append(rf"\newcommand{{\SharpCoupling}}{{{5 + math.exp(-1):.2f}}}")
    pairs = re.findall(r"^n = (\d+) exhaustive: .*equal: (\w+)", txt, flags=re.M)
    if not pairs or any(e != "True" for _, e in pairs):
        raise SystemExit("sharp check: pair moments disagree with enumeration")
    L.append(rf"\newcommand{{\SharpPairsN}}{{{','.join(n_ for n_, _ in pairs)}}}")
    m_ = grab(r"^  20 <= n <= 3000: max of \[sum_\(k=4\)\^\(n-2\) E I_k\]/\(172/n\^2\) = ([\d.]+), E\[C\(I3,2\)\]/\(23/n\^2\) = ([\d.]+), E\[I3 I_\(n-1\)\]/\(25/n\^2\) = ([\d.]+), E\[C\(I_\(n-1\),2\)\]/\(3/n\^2\) = ([\d.]+)")
    if max(float(x) for x in m_.groups()) > 1:
        raise SystemExit("sharp check: a piece of Lemma B(a) exceeds its bound")
    L.append(rf"\newcommand{{\SharpPieceMax}}{{{up(max(float(x) for x in m_.groups()), 2)}}}")
    unrounded = float(grab(r'max over 20 <= n <= 3000 of n\^2 \(bound - 5/n\) = ([\d.]+)').group(1))
    L.append(rf"\newcommand{{\SharpBoundUnrounded}}{{{unrounded:.1f}}}")
    # Monte Carlo of d_TV(R_n, 2^Z): table body
    mc = re.findall(r"^n = (\d+): (\d+) samples, flagged ([\d.]+), missed-interval bound ([\d.e+-]+), P\(R != 2\^N\) = [\d.]+ \(n P = ([\d.]+) \+- ([\d.]+)\)", txt, flags=re.M)
    dt = re.findall(r"^   n d_TV\(R_n, 2\^Z\): Monte Carlo ([\d.]+) \+- ([\d.]+) .*refined first-order model ([\d.]+);", txt, flags=re.M)
    zz = re.findall(r"^   max over these atoms of \|MC - model\| / SE = ([\d.]+)", txt, flags=re.M)
    assert len(mc) == len(dt) == len(zz) >= 1
    with open(os.path.join(out_dir, "table_sharp.tex"), "w") as fh:
        body = [f"{a[0]} & {a[1]} & {float(a[4]):.2f} $\\pm$ {float(a[5]):.2f} & {float(b[0]):.3f} $\\pm$ {float(b[1]):.3f} & "
                f"{so_exact[int(a[0])]:.3f} & {float(b[2]):.3f} & {float(z):.1f}" for a, b, z in zip(mc, dt, zz)]
    # round 5, m2: at n = 50 the estimate exceeds the first-order value; macros for the text
    i50 = [int(a[0]) for a in mc].index(50)
    mc50, ci50, fo50 = float(dt[i50][0]), float(dt[i50][1]), float(dt[i50][2])
    L.append(rf"\newcommand{{\SharpFiftyMC}}{{{mc50:.3f}}}")
    L.append(rf"\newcommand{{\SharpFiftyCI}}{{{ci50:.3f}}}")
    L.append(rf"\newcommand{{\SharpFiftyFirst}}{{{fo50:.3f}}}")
    L.append(rf"\newcommand{{\SharpFiftyExcess}}{{{mc50 - fo50:.2f}}}")
    L.append(rf"\newcommand{{\SharpFiftyZ}}{{{(mc50 - fo50) / (ci50 / 1.96):.1f}}}")
        fh.write(" \\\\\n".join(body) + "\n")
    L.append(rf"\newcommand{{\SharpMCnlo}}{{{mc[0][0]}}}")
    L.append(rf"\newcommand{{\SharpMCnhi}}{{{mc[-1][0]}}}")
    L.append(rf"\newcommand{{\SharpMCsamplesMin}}{{{min(int(a[1]) for a in mc)}}}")
    L.append(rf"\newcommand{{\SharpMCsamplesMax}}{{{max(int(a[1]) for a in mc)}}}")
    L.append(rf"\newcommand{{\SharpMCmissedMax}}{{{tex_sci(max(float(a[3]) for a in mc))}}}")
    L.append(rf"\newcommand{{\SharpMCzFirst}}{{{float(zz[0]):.1f}}}")
    L.append(rf"\newcommand{{\SharpMCzRestMax}}{{{max(float(z) for z in zz[1:]):.1f}}}")
    # atoms 1, 6, 12 at n = 200
    blk = txt[txt.index("n = 200:"):]
    for x, name in (("1", "One"), ("6", "Six"), ("12", "Twelve")):
        m_ = re.search(rf"^ +{x} \| ([+\-][\d.]+) \+- ([\d.]+) \| ([+\-][\d.]+) \|", blk, flags=re.M)
        L.append(rf"\newcommand{{\SharpAtom{name}}}{{${float(m_.group(1)):.3f}\pm{float(m_.group(2)):.3f}$}}")
        L.append(rf"\newcommand{{\SharpMu{name}}}{{${float(m_.group(3)):.3f}$}}")
    L.append(r"\newcommand{\SharpAtomN}{200}")
    # (E) E5f and frozen realizer-law check
    m_ = grab(r"pooled z-scores \(obs - pred\)/sd: u: ([+\-][\d.]+), t: ([+\-][\d.]+), l: ([+\-][\d.]+), e: ([+\-][\d.]+)")
    for v, name in zip(m_.groups(), ("Unique", "Two", "LeEight", "Equal")):
        L.append(rf"\newcommand{{\SharpZ{name}}}{{${float(v):+.2f}$}}")
    m_ = grab(r"pooled over n >= 100: 3/2: (\d+), 2: (\d+), share ([\d.]+) \(95% CI \+- ([\d.]+)")
    L.append(rf"\newcommand{{\SharpShareHalf}}{{{float(m_.group(3)):.3f}}}")
    L.append(rf"\newcommand{{\SharpShareCI}}{{{float(m_.group(4)):.3f}}}")
    share20 = float(grab(r'n =   20: n P\(R != 2\^N\) = [\d.]+; 3/2: \d+, 2: \d+, share ([\d.]+)').group(1))
    L.append(rf"\newcommand{{\SharpShareTwenty}}{{{share20:.3f}}}")
    # (F) where the exceptions come from
    fr = re.findall(r"^ +(\d+) \| (\d+) \| ([\d.]+) \(([\d.]+), ([\d.]+)\) \| ([\d.]+) \| (\d+) \| (\d+) \| (\d+) \| ([\d.]+)", txt, flags=re.M)
    names = {"20": "Twenty", "40": "Forty", "100": "Hundred"}
    for r_ in fr:
        nm = names[r_[0]]
        L.append(rf"\newcommand{{\SharpF{nm}Samples}}{{{r_[1]}}}")
        L.append(rf"\newcommand{{\SharpF{nm}PE}}{{{float(r_[2]):.3f}}}")
        L.append(rf"\newcommand{{\SharpF{nm}PEbound}}{{{float(r_[5]):.3f}}}")
        L.append(rf"\newcommand{{\SharpF{nm}Exc}}{{{r_[6]}}}")
        L.append(rf"\newcommand{{\SharpF{nm}ExcBad}}{{{r_[8]}}}")
        L.append(rf"\newcommand{{\SharpF{nm}Share}}{{{float(r_[9]):.2f}}}")
    L.append(rf"\newcommand{{\SharpSeconds}}{{{int(round(meta['seconds']))}}}")
    L.append(rf"\newcommand{{\SharpSha}}{{{sha[:16]}}}")
    L.append(r"\newcommand{\HasSharp}{1}")

# v0.7: first-order predictions of Theorem thm:sharpR against the E5f samples (computed here from
# results/results_realizer_law.json, independently of the check script)
if os.path.exists(rl_path):
    E1_ = math.exp(-1)
    acc = {k: [0.0, 0.0, 0.0] for k in ("u", "t", "l", "e")}
    for r in rl["rows"]:
        n_, S_ = r["n"], r["samples"]
        pred = {"u": E1_ * (1 - 3 / n_), "t": E1_, "l": 8 / 3 * E1_ - 1.5 * E1_ / n_, "e": 1 - 5 / n_}
        obs = {"u": r["fraction_unique"], "t": r["fraction_two"], "l": r["fraction_le_eight"],
               "e": r["equal_to_two_pow_N"] / S_}
        for k in acc:
            acc[k][0] += obs[k] * S_
            acc[k][1] += pred[k] * S_
            acc[k][2] += pred[k] * (1 - pred[k]) * S_
    for k, name in (("u", "Unique"), ("t", "Two"), ("l", "LeEight"), ("e", "Equal")):
        o, pr, v = acc[k]
        L.append(rf"\newcommand{{\RlawFirstOrderZ{name}}}{{${(o - pr) / math.sqrt(v):+.2f}$}}")
        L.append(rf"\newcommand{{\RlawFirstOrderObs{name}}}{{{o:.0f}}}")
        L.append(rf"\newcommand{{\RlawFirstOrderPred{name}}}{{{pr:.1f}}}")

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
        rows_tex.append(f"{r['n']} & {sci(r['gap_median'])} & "
                        f"{r['disjoint_extremal_pairs']}/{r['configurations']} & "
                        f"{r['perturbations_below_quarter_gap_kept']}/{r['perturbations_total']} & "
                        f"{r['quarter_gap_displacement_changed']}/{r['quarter_gap_displacement_tested']} & "
                        f"{r['walk_steps']} & {sci(r['walk_range_median'])}")
    with open(os.path.join(out_dir, "table_e2c.tex"), "w") as fh:
        fh.write(" \\\\\n".join(rows_tex) + "\n")     # last row without terminator
    L.append(rf"\newcommand{{\EtwocSlopeGap}}{{{-cl['slope_gap']:.1f}}}")
    L.append(rf"\newcommand{{\EtwocSlopeWalk}}{{{-cl['slope_walk_range']:.1f}}}")
    L.append(rf"\newcommand{{\EtwocNmax}}{{{rows_c[-1]['n']}}}")
    L.append(rf"\newcommand{{\EtwocConfigsTotal}}{{{sum(r['configurations'] for r in rows_c)}}}")
    L.append(rf"\newcommand{{\EtwocKeptTotal}}{{{sum(r['perturbations_below_quarter_gap_kept'] for r in rows_c)}}}")
    L.append(rf"\newcommand{{\EtwocPertTotal}}{{{sum(r['perturbations_total'] for r in rows_c)}}}")
    L.append(rf"\newcommand{{\EtwocChangedTotal}}{{{sum(r['quarter_gap_displacement_changed'] for r in rows_c)}}}")
    L.append(rf"\newcommand{{\EtwocChangedTested}}{{{sum(r['quarter_gap_displacement_tested'] for r in rows_c)}}}")
    for r in rows_c:
        if r["n"] == 64:
            L.append(rf"\newcommand{{\EtwocGapNsixtyfour}}{{{sci(r['gap_median'])}}}")
            L.append(rf"\newcommand{{\EtwocWalkNsixtyfour}}{{{sci(r['walk_range_median'])}}}")
            # order-of-magnitude estimate n(g/4)^2 / (n/6) = 3 g^2 / 8 of the disparity after displacing every point by g/4
            L.append(rf"\newcommand{{\EtwocDispEstNsixtyfour}}{{{sci(3 * r['gap_median'] ** 2 / 8)}}}")
    L.append(rf"\newcommand{{\EtwocGapNmax}}{{{sci(rows_c[-1]['gap_median'])}}}")
    L.append(rf"\newcommand{{\EtwocWalkNmax}}{{{sci(rows_c[-1]['walk_range_median'])}}}")
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
