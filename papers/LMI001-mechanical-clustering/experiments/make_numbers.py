#!/usr/bin/env python3
"""Turn results/*.json into LaTeX macros (manuscript/numbers.tex) and table bodies."""
import json
import os

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
RES = os.path.join(ROOT, "results")
OUT = os.path.join(ROOT, "manuscript")

ident = json.load(open(os.path.join(RES, "results_identity.json")))
relax = json.load(open(os.path.join(RES, "results_relaxation.json")))

POTS = ["hooke", "hooke_lift", "rest", "tension", "gauss", "log"]
POT_TEX = {"hooke": r"$d^2$ (Hooke)", "hooke_lift": r"$d^2$ on the lift $(x,|x|^2/s)$",
           "rest": r"$(d-r)^2$ (rest length)", "tension": r"$d$ (constant tension)",
           "gauss": r"$1-e^{-d^2/2\ell^2}$ (saturating)", "log": r"$\log(1+d^2/\ell^2)$ (soft)"}
DATA_ORDER = ["blobs", "moons", "circles", "digits", "iris"]


def sci(x, digits=1):
    if x == 0:
        return r"\ensuremath{0}"
    e = int(f"{x:e}".split("e")[1])
    m = x / 10 ** e
    return rf"\ensuremath{{{m:.{digits}f}\times 10^{{{e}}}}}"


def pct(x):
    return f"{100 * x:.0f}"


L = []
mi, mr = ident["meta"], relax["meta"]
L.append(rf"\newcommand{{\MetaSeed}}{{{mi['seed']}}}")
L.append(rf"\newcommand{{\MetaSeedRelax}}{{{mr['seed']}}}")
L.append(rf"\newcommand{{\MetaPython}}{{{mi['python']}}}")
L.append(rf"\newcommand{{\MetaNumpy}}{{{mi['numpy']}}}")
L.append(rf"\newcommand{{\MetaScipy}}{{{mi['scipy']}}}")
L.append(rf"\newcommand{{\MetaSklearn}}{{{mi['sklearn']}}}")
L.append(rf"\newcommand{{\IdentitySeconds}}{{{int(round(mi['seconds']))}}}")
L.append(rf"\newcommand{{\RelaxSeconds}}{{{int(round(mr['seconds']))}}}")
ds = mi["datasets"]
L.append(rf"\newcommand{{\Nsynth}}{{{ds['blobs']['n']}}}")
L.append(rf"\newcommand{{\Ndigits}}{{{ds['digits']['n']}}}")
L.append(rf"\newcommand{{\Niris}}{{{ds['iris']['n']}}}")
L.append(rf"\newcommand{{\NumDatasets}}{{{len(ds)}}}")
L.append(rf"\newcommand{{\NumPotentials}}{{{len(POTS)}}}")
with open(os.path.join(OUT, "table_datasets.tex"), "w") as fh:
    rows = [f"{d} & {ds[d]['n']} & {ds[d]['dim']} & {ds[d]['k']}" for d in DATA_ORDER]
    fh.write(" \\\\\n".join(rows) + "\n")

# ---- E1 ----
e1 = ident["E1"]
L.append(rf"\newcommand{{\EoneChecks}}{{{e1['checks']}}}")
L.append(rf"\newcommand{{\EoneFailures}}{{{e1['failures']}}}")
L.append(rf"\newcommand{{\EonePassed}}{{{e1['checks'] - e1['failures']}}}")
L.append(rf"\newcommand{{\EoneMaxRelErr}}{{{sci(e1['max_rel_err'])}}}")
L.append(rf"\newcommand{{\EoneHookeSSEErr}}{{{sci(e1['hooke_sse_max_rel_err'])}}}")
L.append(rf"\newcommand{{\EoneRandomPartitions}}{{{e1['n_random_partitions']}}}")
L.append(rf"\newcommand{{\EoneEqualSizeErr}}{{{sci(e1['equal_size_factor_max_rel_err'])}}}")
L.append(rf"\newcommand{{\EoneRatioMin}}{{{e1['total_over_specific_ratio_min']:.1f}}}")
L.append(rf"\newcommand{{\EoneRatioMax}}{{{e1['total_over_specific_ratio_max']:.1f}}}")
L.append(rf"\newcommand{{\EoneConfigs}}{{{len(e1['rows'])}}}")
L.append(rf"\newcommand{{\EonePartitionsTotal}}{{{sum(r['partitions'] for r in e1['rows'])}}}")
cnd = e1["cnd_eigs"]
cnd_true = [c for c in cnd if c["cnd_label"]]
cnd_false = [c for c in cnd if not c["cnd_label"]]
L.append(rf"\newcommand{{\EoneCndConfigs}}{{{len(cnd_true)}}}")
L.append(rf"\newcommand{{\EoneCndPsd}}{{{sum(c['cnd_kernel_psd'] for c in cnd_true)}}}")
L.append(rf"\newcommand{{\EoneRestConfigs}}{{{len(cnd_false)}}}")
L.append(rf"\newcommand{{\EoneRestIndefinite}}{{{sum(not c['cnd_kernel_psd'] for c in cnd_false)}}}")
L.append(rf"\newcommand{{\EoneCndWorstRatio}}{{{sci(max(-c['lam_min_cnd_kernel'] / c['lam_max_cnd_kernel'] for c in cnd_true) if any(c['lam_min_cnd_kernel'] < 0 for c in cnd_true) else 0.0)}}}")
with open(os.path.join(OUT, "table_e1.tex"), "w") as fh:
    rows = []
    for p in POTS:
        rr = [r for r in e1["rows"] if r["potential"] == p]
        cc = [c for c in cnd if c["potential"] == p]
        worst = max(r["max_rel_err"] for r in rr)
        ratio = [c["lam_min_cnd_kernel"] / c["lam_max_cnd_kernel"] for c in cc]
        psd = sum(c["cnd_kernel_psd"] for c in cc)
        lam_naive = min(r["lam_min_K"] for r in rr)
        rows.append(f"{POT_TEX[p]} & {'yes' if cc[0]['cnd_label'] else 'no'} & {sum(r['partitions'] for r in rr)} & "
                    f"{sci(worst)} & {sci(min(ratio)) if min(ratio) < 0 else '$\\ge 0$'} & {psd}/{len(cc)}")
    fh.write(" \\\\\n".join(rows) + "\n")

# ---- E2 ----
e2 = ident["E2"]
L.append(rf"\newcommand{{\EtwoRuns}}{{{e2['runs']}}}")
L.append(rf"\newcommand{{\EtwoIdentical}}{{{e2['identical']}}}")
L.append(rf"\newcommand{{\EtwoMaxRelErr}}{{{sci(e2['max_rel_err_energy'])}}}")
L.append(rf"\newcommand{{\EtwoNsub}}{{{e2['n_sub']}}}")
L.append(rf"\newcommand{{\EtwoAnchoredRuns}}{{{e2['anchored_runs']}}}")
L.append(rf"\newcommand{{\EtwoAnchoredIdentical}}{{{e2['anchored_identical']}}}")
L.append(rf"\newcommand{{\EtwoAnchoredMaxErr}}{{{sci(e2['anchored_max_rel_err_inertia'])}}}")
L.append(rf"\newcommand{{\EtwoSecondsPhysics}}{{{sum(r['seconds_physics'] for r in e2['rows']):.0f}}}")
L.append(rf"\newcommand{{\EtwoSecondsKernel}}{{{sum(r['seconds_kernel'] for r in e2['rows']):.1f}}}")
L.append(rf"\newcommand{{\EtwoMaxSweeps}}{{{max(r['sweeps'] for r in e2['rows'])}}}")
L.append(rf"\newcommand{{\EtwoMeanSweeps}}{{{sum(r['sweeps'] for r in e2['rows']) / len(e2['rows']):.1f}}}")

# ---- E4 ----
e4 = ident["E4"]
L.append(rf"\newcommand{{\EfourN}}{{{e4['n']}}}")
L.append(rf"\newcommand{{\EfourK}}{{{e4['k']}}}")
L.append(rf"\newcommand{{\EfourPartitions}}{{{e4['partitions']}}}")
L.append(rf"\newcommand{{\EfourUnknowns}}{{{e4['unknowns']}}}")
L.append(rf"\newcommand{{\EfourPoints}}{{{', '.join('(' + str(a) + ',' + str(b) + ')' for a, b in e4['points'])}}}")
ENAME = {"hooke_specific": r"$\sum_c \frac1{n_c}\sum d_{ij}^2$ (Hooke, per particle)",
         "hooke_total": r"$\sum_c \sum d_{ij}^2$ (Hooke, total)",
         "rest_fixed_specific": r"$\sum_c \frac1{n_c}\sum (d_{ij}^2-\rho)^2$, fixed $\rho$",
         "rest_adaptive_specific": r"$\sum_c \frac1{n_c}\sum (d_{ij}^2-\rho_c)^2$, $\rho_c$ = cluster mean",
         "threebody_specific": r"$\sum_c \frac1{n_c}\sum_{i<j<l} 4\,\mathrm{area}(ijl)^2$ (three-body)",
         "hooke_per_spring": r"$\sum_c \binom{n_c}{2}^{-1}\sum d_{ij}^2$ (per spring)"}
with open(os.path.join(OUT, "table_e4.tex"), "w") as fh:
    rows = []
    for en in ["hooke_specific", "hooke_total", "rest_fixed_specific", "rest_adaptive_specific",
               "threebody_specific", "hooke_per_spring"]:
        rr = {r["family_w"]: r for r in e4["results"] if r["energy"] == en}
        cell = lambda r: "yes (0)" if r["representable"] else f"no ({r['relative_residual']:.3f})"
        rows.append(f"{ENAME[en]} & {cell(rr['per_particle'])} & {cell(rr['total'])}")
    fh.write(" \\\\\n".join(rows) + "\n")
L.append(rf"\newcommand{{\EfourRankSpecific}}{{{[r for r in e4['results'] if r['family_w'] == 'per_particle'][0]['rank']}}}")
L.append(rf"\newcommand{{\EfourRankTotal}}{{{[r for r in e4['results'] if r['family_w'] == 'total'][0]['rank']}}}")

# ---- E3 ----
agg = relax["aggregate"]
cfgs = relax["configs"]
L.append(rf"\newcommand{{\EthreeConfigs}}{{{len(cfgs)}}}")
L.append(rf"\newcommand{{\EthreeR}}{{{mr['R']}}}")
L.append(rf"\newcommand{{\EthreeRanneal}}{{{mr['R_anneal']}}}")
L.append(rf"\newcommand{{\EthreeAnnealSweeps}}{{{mr['anneal_sweeps']}}}")
for m, tag in (("relax", "Relax"), ("lloyd+relax", "LloydRelax"), ("lloyd", "Lloyd"),
               ("anneal", "Anneal"), ("lloyd_naive", "Naive")):
    a = agg[m]
    L.append(rf"\newcommand{{\EthreeRuns{tag}}}{{{a['n_runs']}}}")
    L.append(rf"\newcommand{{\EthreeVoronoi{tag}}}{{{a['n_voronoi_stable']}}}")
    L.append(rf"\newcommand{{\EthreeHartigan{tag}}}{{{a['n_hartigan_stable']}}}")
    L.append(rf"\newcommand{{\EthreeReach{tag}}}{{{a['configs_reaching_best']}}}")
    L.append(rf"\newcommand{{\EthreeMedianExcess{tag}}}{{{sci(a['median_of_median_rel_excess'])}}}")
    L.append(rf"\newcommand{{\EthreeMaxBestExcess{tag}}}{{{sci(a['max_best_rel_excess'])}}}")
    L.append(rf"\newcommand{{\EthreeMeanFracReach{tag}}}{{{pct(a['mean_frac_reaching_best'])}}}")
L.append(rf"\newcommand{{\EthreeDistinguishable}}{{{agg['distinguishable_configs']}}}")
L.append(rf"\newcommand{{\EthreeRelaxBetter}}{{{agg['relax_better_configs']}}}")
L.append(rf"\newcommand{{\EthreeLloydRelaxBetter}}{{{agg['lloydrelax_better_configs']}}}")
L.append(rf"\newcommand{{\EthreeMaxAbsDiff}}{{{sci(agg['max_abs_relax_minus_lloydrelax_rel'])}}}")
L.append(rf"\newcommand{{\EthreeAriOne}}{{{agg['ari_relax_vs_lloydrelax_equal_one']}}}")
L.append(rf"\newcommand{{\EthreeAriMin}}{{{agg['ari_relax_vs_lloydrelax_min']:.2f}}}")
L.append(rf"\newcommand{{\EthreeDirectCheck}}{{{sci(agg['direct_check_max_rel_err'])}}}")
n_shift = sum(c["kernel_used"] == "theorem1f+shift" for c in cfgs)
L.append(rf"\newcommand{{\EthreeShiftedConfigs}}{{{n_shift}}}")
L.append(rf"\newcommand{{\EthreeLloydHartiganPct}}{{{pct(agg['lloyd']['n_hartigan_stable'] / agg['lloyd']['n_runs'])}}}")
L.append(rf"\newcommand{{\EthreeNaiveHartiganPct}}{{{pct(agg['lloyd_naive']['n_hartigan_stable'] / agg['lloyd_naive']['n_runs'])}}}")
# configurations where the energies of relax and lloyd+relax agree but partitions differ (ARI<1)
agree_diff = sum((abs(c["relax_minus_lloydrelax_rel"]) <= mr["rel_tol_best"]) and c["ari_best_relax_vs_lloydrelax"] < 1 - 1e-12 for c in cfgs)
L.append(rf"\newcommand{{\EthreeAgreeButDifferent}}{{{agree_diff}}}")
# per-potential aggregate table
with open(os.path.join(OUT, "table_e3_agg.tex"), "w") as fh:
    rows = []
    for p in POTS:
        cc = [c for c in cfgs if c["potential"] == p]
        f = lambda m: f"{sum(c['summary'][m]['best_rel_excess'] <= mr['rel_tol_best'] for c in cc)}/{len(cc)}"
        g = lambda m: pct(sum(c['summary'][m]['frac_reaching_best'] for c in cc) / len(cc))
        vor = sum(round(c["summary"]["relax"]["frac_voronoi_stable"] * c["summary"]["relax"]["runs"]) for c in cc)
        tot = sum(c["summary"]["relax"]["runs"] for c in cc)
        hart = sum(round(c["summary"]["lloyd"]["frac_hartigan_stable"] * c["summary"]["lloyd"]["runs"]) for c in cc)
        ari1 = sum(c["ari_best_relax_vs_lloydrelax"] > 1 - 1e-12 for c in cc)
        rows.append(f"{POT_TEX[p]} & {f('relax')} & {f('lloyd+relax')} & {f('lloyd')} & {f('lloyd_naive')} & "
                    f"{g('relax')} & {g('lloyd+relax')} & {g('lloyd')} & {vor}/{tot} & {hart}/{tot} & {ari1}/{len(cc)}")
    fh.write(" \\\\\n".join(rows) + "\n")
# per-configuration table
with open(os.path.join(OUT, "table_e3.tex"), "w") as fh:
    rows = []
    for d in DATA_ORDER:
        for p in POTS:
            c = next(c for c in cfgs if c["dataset"] == d and c["potential"] == p)
            s = c["summary"]
            ex = lambda m: ("0" if s[m]["best_rel_excess"] <= 1e-12 else sci(s[m]["best_rel_excess"], 1))
            rows.append(f"{d} & {p.replace('_', r'\_')} & {c['E_best']:.5g} & {ex('relax')} & {ex('lloyd+relax')} & {ex('lloyd')} & {ex('lloyd_naive')} & "
                        f"{s['relax']['frac_reaching_best']:.2f} & {s['lloyd+relax']['frac_reaching_best']:.2f} & {s['lloyd']['frac_reaching_best']:.2f} & "
                        f"{s['relax']['frac_voronoi_stable']:.2f} & {s['lloyd']['frac_hartigan_stable']:.2f} & {c['ari_best_relax_vs_lloydrelax']:.2f}")
    fh.write(" \\\\\n".join(rows) + "\n")

with open(os.path.join(OUT, "numbers.tex"), "w") as fh:
    fh.write("% generated by experiments/make_numbers.py -- do not edit\n")
    fh.write("\n".join(L) + "\n")
print("wrote numbers.tex and table bodies")
