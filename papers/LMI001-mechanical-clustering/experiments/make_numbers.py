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
L.append(rf"\newcommand{{\EoneMaxSigma}}{{{sci(max(r['sigma'] for r in e1['rows']))}}}")
with open(os.path.join(OUT, "table_e1.tex"), "w") as fh:
    rows = []
    for p in POTS:
        rr = [r for r in e1["rows"] if r["potential"] == p]
        cc = [c for c in cnd if c["potential"] == p]
        worst = max(r["max_rel_err"] for r in rr)
        ratio = [c["lam_min_cnd_kernel"] / c["lam_max_cnd_kernel"] for c in cc]
        psd = sum(c["cnd_kernel_psd"] for c in cc)
        lam_naive = min(r["lam_min_K"] for r in rr)
        GE = r"$\ge 0$"
        ratio_cell = sci(min(ratio)) if min(ratio) < 0 else GE
        rows.append(f"{POT_TEX[p]} & {'yes' if cc[0]['cnd_label'] else 'no'} & {sum(r['partitions'] for r in rr)} & "
                    f"{sci(worst)} & {ratio_cell} & {psd}/{len(cc)}")
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
pts_tex = lambda pts: ', '.join('(' + str(a) + ',' + str(b) + ')' for a, b in pts)
e4_cfgs = e4["configs"]
L.append(rf"\newcommand{{\EfourSeed}}{{{e4['seed']}}}")
L.append(rf"\newcommand{{\EfourPoints}}{{{pts_tex(e4_cfgs[0]['points'])}}}")
L.append(rf"\newcommand{{\EfourPointsB}}{{{pts_tex(e4_cfgs[1]['points']) if len(e4_cfgs) > 1 else ''}}}")
L.append(rf"\newcommand{{\EfourCells}}{{{e4['cells']}}}")
L.append(rf"\newcommand{{\EfourCellsSame}}{{{e4['cells_same_pattern']}}}")
ENAME = {"hooke_specific": r"$\sum_c \frac1{n_c}\sum d_{ij}^2$ (Hooke, per particle)",
         "hooke_total": r"$\sum_c \sum d_{ij}^2$ (Hooke, total)",
         "rest_fixed_specific": r"$\sum_c \frac1{n_c}\sum (d_{ij}^2-\rho)^2$, fixed $\rho$",
         "rest_adaptive_specific": r"$\sum_c \frac1{n_c}\sum (d_{ij}^2-\rho_c)^2$, $\rho_c$ = cluster mean",
         "threebody_specific": r"$\sum_c \frac1{n_c}\sum_{i<j<l} 4\,\mathrm{area}(ijl)^2$ (three-body)",
         "hooke_per_spring": r"$\sum_c \binom{n_c}{2}^{-1}\sum d_{ij}^2$ (per spring)"}


def e4_cell(en, w):
    """yes/no plus the relative residuals on every configuration, separated by ';'."""
    rs = [next(r for r in c["results"] if r["energy"] == en and r["family_w"] == w) for c in e4_cfgs]
    verdicts = {r["representable"] for r in rs}
    word = "yes" if verdicts == {True} else ("no" if verdicts == {False} else "mixed")
    return f"{word} (" + "; ".join("0" if r["representable"] else f"{r['relative_residual']:.3f}" for r in rs) + ")"


with open(os.path.join(OUT, "table_e4.tex"), "w") as fh:
    rows = []
    for en in ["hooke_specific", "hooke_total", "rest_fixed_specific", "rest_adaptive_specific",
               "threebody_specific", "hooke_per_spring"]:
        rows.append(f"{ENAME[en]} & {e4_cell(en, 'per_particle')} & {e4_cell(en, 'total')}")
    fh.write(" \\\\\n".join(rows) + "\n")
ranks = lambda w: sorted({r["rank"] for c in e4_cfgs for r in c["results"] if r["family_w"] == w})
L.append(rf"\newcommand{{\EfourRankSpecific}}{{{'/'.join(map(str, ranks('per_particle')))}}}")
L.append(rf"\newcommand{{\EfourRankTotal}}{{{'/'.join(map(str, ranks('total')))}}}")

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
L.append(rf"\newcommand{{\EthreeDistinguishable}}{{{agg['distinguishable_configs']}}}")
L.append(rf"\newcommand{{\EthreeRelaxBetter}}{{{agg['relax_better_configs']}}}")
L.append(rf"\newcommand{{\EthreeLloydRelaxBetter}}{{{agg['lloydrelax_better_configs']}}}")
L.append(rf"\newcommand{{\EthreeMaxAbsDiff}}{{{sci(agg['max_abs_relax_minus_lloydrelax_rel'])}}}")
L.append(rf"\newcommand{{\EthreeAriOne}}{{{agg['ari_relax_vs_lloydrelax_equal_one']}}}")
L.append(rf"\newcommand{{\EthreeDirectCheck}}{{{sci(agg['direct_check_max_rel_err'])}}}")
n_shift = sum(c["kernel_used"].endswith("+shift") for c in cfgs)
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
        assert vor == tot, f"relaxation fixed points not all Voronoi-stable for {p}: {vor}/{tot}"
        rows.append(f"{POT_TEX[p]} & {f('relax')} & {f('lloyd+relax')} & {f('lloyd')} & {f('lloyd_naive')} & "
                    f"{g('relax')} & {g('lloyd+relax')} & {g('lloyd')} & {hart}/{tot} & {ari1}/{len(cc)}")
    fh.write(" \\\\\n".join(rows) + "\n")
# the same per-potential table in Markdown (it was Table 1 of the manuscript up to v0.4; moved out in v0.5)
with open(os.path.join(RES, "tables_e3_by_potential.md"), "w") as fh:
    fh.write("# E3 by potential (generated by experiments/make_numbers.py from results/results_relaxation.json)\n\n"
             "Table 1 of the manuscript up to v0.4 (five datasets per potential). \"Reaching E*\" means within "
             f"{mr['rel_tol_best']:g} relative of the best energy found by any method. \"Lloyd f.p. 1-move stable\": Lloyd fixed "
             "points that no single move improves (all relaxation fixed points are Lloyd fixed points, Proposition 3.9(ii)). "
             "\"best ARI=1\": configurations in which the best partitions of relax and lloyd+relax coincide.\n\n"
             "| potential | configs reaching E* (of 5): relax | lloyd+relax | lloyd | naive | restarts reaching E* (%): relax | "
             "lloyd+relax | lloyd | Lloyd f.p. 1-move stable | best ARI=1 |\n|---|---|---|---|---|---|---|---|---|---|\n")
    for p in POTS:
        cc = [c for c in cfgs if c["potential"] == p]
        f = lambda m: f"{sum(c['summary'][m]['best_rel_excess'] <= mr['rel_tol_best'] for c in cc)}/{len(cc)}"
        g = lambda m: pct(sum(c['summary'][m]['frac_reaching_best'] for c in cc) / len(cc))
        tot = sum(c["summary"]["relax"]["runs"] for c in cc)
        hart = sum(round(c["summary"]["lloyd"]["frac_hartigan_stable"] * c["summary"]["lloyd"]["runs"]) for c in cc)
        ari1 = sum(c["ari_best_relax_vs_lloydrelax"] > 1 - 1e-12 for c in cc)
        fh.write(f"| {p} | {f('relax')} | {f('lloyd+relax')} | {f('lloyd')} | {f('lloyd_naive')} | "
                 f"{g('relax')} | {g('lloyd+relax')} | {g('lloyd')} | {hart}/{tot} | {ari1}/{len(cc)} |\n")
    fh.write(f"\nAll configurations: annealing reaches E* in {agg['anneal']['configs_reaching_best']}/{len(cfgs)} "
             f"(with {mr.get('R_anneal', 'fewer')} restarts only; not comparable); best partitions of relax and lloyd+relax "
             f"coincide (ARI = 1) in {agg['ari_relax_vs_lloydrelax_equal_one']}/{len(cfgs)}; configurations whose two best "
             f"energies agree but whose best partitions differ: {agree_diff}; spring-by-spring recomputation of the best "
             f"energies: max rel. err {agg['direct_check_max_rel_err']:.1e}.\n")
# per-configuration table
with open(os.path.join(OUT, "table_e3.tex"), "w") as fh:
    rows = []
    for d in DATA_ORDER:
        for p in POTS:
            c = next(c for c in cfgs if c["dataset"] == d and c["potential"] == p)
            s = c["summary"]
            ex = lambda m: ("0" if s[m]["best_rel_excess"] <= 1e-12 else sci(s[m]["best_rel_excess"], 1))
            ptex = p.replace("_", "\\_")
            rows.append(f"{d} & {ptex} & {c['E_best']:.5g} & {ex('relax')} & {ex('lloyd+relax')} & {ex('lloyd')} & {ex('lloyd_naive')} & "
                        f"{s['relax']['frac_reaching_best']:.2f} & {s['lloyd+relax']['frac_reaching_best']:.2f} & {s['lloyd']['frac_reaching_best']:.2f} & "
                        f"{s['relax']['frac_voronoi_stable']:.2f} & {s['lloyd']['frac_hartigan_stable']:.2f} & {c['ari_best_relax_vs_lloydrelax']:.2f}")
    fh.write(" \\\\\n".join(rows) + "\n")

with open(os.path.join(OUT, "numbers.tex"), "w") as fh:
    fh.write("% generated by experiments/make_numbers.py -- do not edit\n"
             "% per-method E3 macros (Runs/Voronoi/Hartigan/Reach/MedianExcess) are generated systematically; main.tex uses a subset\n")
    fh.write("\n".join(L) + "\n")
print("wrote numbers.tex and table bodies")
