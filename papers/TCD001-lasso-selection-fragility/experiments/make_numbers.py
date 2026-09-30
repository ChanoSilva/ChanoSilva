#!/usr/bin/env python3
"""Turn results/*.json into LaTeX macros (manuscript/numbers.tex) and table bodies (manuscript/table_*.tex).
Every number quoted in main.tex comes from here."""
import json
import os
from fractions import Fraction

import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
RES = os.path.join(ROOT, "results")
OUT = os.path.join(ROOT, "manuscript")
val = json.load(open(os.path.join(RES, "validation.json")))
fra = json.load(open(os.path.join(RES, "fragility.json")))
sca = json.load(open(os.path.join(RES, "scaling.json")))
exa = json.load(open(os.path.join(RES, "examples.json")))

L = []


def mac(name, value):
    L.append(rf"\newcommand{{\{name}}}{{{value}}}")


def pct(x, d=0):
    return "--" if x is None else f"{100*x:.{d}f}"


def num(x, d=2):
    return "--" if x is None else f"{x:.{d}f}"


def frac_tex(s):
    f = Fraction(s)
    if f.denominator == 1:
        return f"{f.numerator}"
    sign = "-" if f < 0 else ""
    return rf"{sign}\tfrac{{{abs(f.numerator)}}}{{{f.denominator}}}"


def word(n):
    return {8: "Eight", 10: "Ten", 12: "Twelve", 14: "Fourteen", 18: "Eighteen", 22: "Twentytwo", 26: "Twentysix",
            30: "Thirty", 34: "Thirtyfour", 50: "Fifty", 100: "Hundred", 200: "Twohundred", 400: "Fourhundred"}[n]


# ------------------------------------------------------------------ meta
m = val["meta"]
mac("MetaSeed", fra["meta"]["seed"])
mac("MetaSeedScaling", sca["meta"]["seed"])
mac("MetaPython", m["python"])
mac("MetaNumpy", m["numpy"])
mac("MetaScipy", m["scipy"])
mac("MetaSklearn", m["sklearn"])
tot = val["meta"]["seconds"] + fra["meta"]["seconds"] + sca["meta"]["seconds"] + exa["seconds"]
mac("MetaSecondsValidation", int(round(val["meta"]["seconds"])))
mac("MetaSecondsFragility", int(round(fra["meta"]["seconds"])))
mac("MetaSecondsScaling", int(round(sca["meta"]["seconds"])))
mac("MetaSecondsTotal", int(round(tot)))
mac("MetaMinutesTotal", f"{tot/60:.1f}")

# ------------------------------------------------------------------ E0 examples
e2 = exa["example2"]
mac("ExTwoMu", frac_tex(e2["mu"]))
mac("ExTwoR", ",".join(str(i + 1) for i in e2["R"]))
mac("ExTwoRp", ",".join(str(i + 1) for i in e2["Rp"]))
mac("ExTwoTrials", e2["trials"])
mac("ExTwoSubsets", len(e2["all_subsets"]))
mac("ExTwoPairs", e2["nonmonotone_pairs_var0"])
mac("ExTwoStabSel", f"{e2['stability_selection_var0']['selected']}/{e2['stability_selection_var0']['subsamples']}")
an = {a["name"]: a for a in e2["analysis"]}
for key, tag in [("D", "D"), ("D\\R", "DR"), ("D\\R'", "DRp")]:
    a = an[key]
    mac(f"ExTwo{tag}Supp", ",".join(str(int(v) + 1) for v in a["support"]) or r"\emptyset")
    b = a["beta"]
    mac(f"ExTwo{tag}Beta", ", ".join(rf"\hat\beta_{{{int(k)+1}}}={frac_tex(v)}" for k, v in b.items()) if b else "0")
    c = a["inactive_c"]
    mac(f"ExTwo{tag}C", ", ".join(rf"c_{{{int(k)+1}}}={frac_tex(v)}" for k, v in c.items()) if c else "--")
    mg = a["marginal_xy"]
    for k, v in c.items():
        mac(f"ExTwo{tag}CVal{'One' if int(k) == 0 else 'Two'}", frac_tex(v))
    mac(f"ExTwo{tag}MargOne", frac_tex(mg["0"]))
    mac(f"ExTwo{tag}MargTwo", frac_tex(mg["1"]))
# matrix rows for the example
rows = " \\\\ ".join(" & ".join(str(v) for v in row) + f" & {yv}" for row, yv in zip(e2["X"], e2["y"]))
mac("ExTwoRows", rows)

# ------------------------------------------------------------------ E1 validation
A = val["A_single"]
mac("EoneSingleTests", sum(r["tests"] for r in A))
mac("EoneSingleAgree", sum(r["agreements"] for r in A))
mac("EoneSinglePreserved", sum(r["preserved"] for r in A))
mac("EoneSingleMaxDiff", f"{max(r['max_coef_diff'] for r in A):.0e}".replace("e-", r"\times 10^{-").replace("e+", r"\times 10^{") + "}")
B = val["B_multi"]
mac("EoneMultiTests", sum(r["tests"] for r in B))
mac("EoneMultiAgree", sum(r["agreements"] for r in B))
mac("EoneMultiMaxDiff", f"{max(r['max_coef_diff'] for r in B):.0e}".replace("e-", r"\times 10^{-").replace("e+", r"\times 10^{") + "}")
cd = val["A_cd_crosscheck"]
mac("EoneCdN", cd["n"])
mac("EoneCdDis", cd["support_disagreements"])
mac("EoneCdMaxDiff", f"{cd['max_coef_diff']:.0e}".replace("e-", r"\times 10^{-").replace("e+", r"\times 10^{") + "}")
mac("EoneReps", val["meta"]["reps_per_cell"])
C = val["C_certificates"]
mac("EoneCorStable", sum(r["stable_single_removals"] for r in C))
mac("EoneCorCertified", sum(r["certified_by_cor2"] for r in C))
mac("EoneCorCoverage", pct(sum(r["certified_by_cor2"] for r in C) / sum(r["stable_single_removals"] for r in C)))
mac("EoneCorInstances", sum(r["instances"] for r in C))
D = val["D_throughput"]
mac("EoneOracleUs", f"{D['oracle_seconds_per_subset']*1e6:.1f}")
mac("EoneRefitUs", f"{D['refit_seconds_per_subset']*1e6:.0f}")
mac("EoneSpeedup", f"{D['speedup']:.0f}")
mac("EoneThroughputN", D["n"])
mac("EoneThroughputP", D["p"])
mac("EoneThroughputSubsets", D["subsets"])
with open(os.path.join(OUT, "table_e1.tex"), "w") as fh:
    for r in A:
        fh.write(f"{r['n']} & {r['p']} & {r['rule']} & {r['tests']} & {r['agreements']} & {r['preserved']} & {r['max_coef_diff']:.0e} \\\\\n".replace("e-", "e$-$"))
with open(os.path.join(OUT, "table_e1b.tex"), "w") as fh:
    for r in C:
        fh.write(f"{r['n']} & {r['p']} & {r['instances']} & {r['stable_single_removals']} & {r['certified_by_cor2']} & {pct(r['cor2_coverage'])}\\% & {pct(r['frac_f1'])}\\% & {pct(r['frac_kstar_ge1_given_f_ge2'])}\\% & {num(r['mean_gap_given_f_ge2'])} \\\\\n")

# ------------------------------------------------------------------ E2 fragility (n <= 14)
agg = fra["aggregates"]
fm = fra["meta"]
mac("EtwoReps", fm["reps"])
mac("EtwoInstances", sum(a["instances"] for a in agg))
mac("EtwoKmax", fm["kmax_targeted"])
for fam, f in fm["families"].items():
    mac(f"Fam{fam}p", f["p"])
    mac(f"Fam{fam}b", f"{f['b']:.0f}")
    mac(f"Fam{fam}rho", f"{f['rho']:.1f}")
    mac(f"Fam{fam}c", f"{f['c']:.1f}")
    mac(f"Fam{fam}s", f["s0"])
with open(os.path.join(OUT, "table_e2.tex"), "w") as fh:
    for a in agg:
        d = a["f_any_signed_C_dist"]
        dist = "/".join(str(d[str(k)]) for k in range(1, 6)) + (f"/{d['6']+d['7']+d['notfound']}" )
        t = a["types_C"]
        fh.write(f"{a['family']} & {a['n']} & {a['mean_support']:.1f} & {pct(a['frac_true_support'])}\\% & {dist} & {num(a['f_any_signed_C_mean'])} & {pct(a['f_any_signed_C_frac1'])}\\% & {num(a['f_any_signed_P_mean'])} & {pct(a['f_any_signed_P_frac1'])}\\% & {t['leave']}/{t['enter']}/{t['swap']}/{t['sign_only']} & {num(a['f_leave_C_mean'],1)} ({a['f_leave_C_notfound']}) & {num(a['f_enter_C_mean'],1)} ({a['f_enter_C_notfound']}) \\\\\n")
# pooled statistics per family
for fam in fm["families"]:
    rs = [r for r in fra["records"] if r["family"] == fam]
    fs = np.array([r["f_any_signed_C"] if r["f_any_signed_C"] is not None else np.nan for r in rs], float)
    mac(f"Etwo{fam}NotFound", int(np.sum(np.isnan(fs))))
    mac(f"Etwo{fam}EmptySupport", int(sum(r["support_size"] == 0 for r in rs)))
    mac(f"Etwo{fam}FracOne", pct(np.mean(fs == 1)))
    mac(f"Etwo{fam}Max", int(np.nanmax(fs)))
    mac(f"Etwo{fam}Mean", num(np.nanmean(fs)))
    mac(f"Etwo{fam}TrueSupp", pct(np.mean([r["true_support"] for r in rs])))
    mac(f"Etwo{fam}SignedNeUnsigned", pct(np.mean([r["f_any_signed_C"] != r["f_any_C"] for r in rs]), 1))
    mac(f"Etwo{fam}SignedNeUnsignedCount", int(sum(r["f_any_signed_C"] != r["f_any_C"] for r in rs)))
    mac(f"Etwo{fam}N", len(rs))
    types = sum([r.get("types_any_signed_C", []) for r in rs], [])
    mac(f"Etwo{fam}TypesLeave", pct(np.mean([t == "leave" for t in types])))
    mac(f"Etwo{fam}TypesEnter", pct(np.mean([t == "enter" for t in types])))
    mac(f"Etwo{fam}TypesSwap", pct(np.mean([t == "swap" for t in types])))
    mac(f"Etwo{fam}TypesSign", int(sum(t == "sign_only" for t in types)))
    mac(f"Etwo{fam}TypesN", len(types))
    fl = [r["f_leave_C"] for r in rs if "f_leave_C" in r]
    mac(f"Etwo{fam}LeaveN", len(fl))
    mac(f"Etwo{fam}LeaveNotFound", sum(f is None for f in fl))
    mac(f"Etwo{fam}LeaveMean", num(np.mean([f for f in fl if f is not None]), 1))
    fe = [r["f_enter_C"] for r in rs if "f_enter_C" in r]
    mac(f"Etwo{fam}EnterN", len(fe))
    mac(f"Etwo{fam}EnterNotFound", sum(f is None for f in fe))
    mac(f"Etwo{fam}EnterMean", num(np.mean([f for f in fe if f is not None]), 1))
    # certificate at n<=14
    ge2 = [r for r in rs if r["f_any_signed_C"] is not None and r["f_any_signed_C"] >= 2]
    mac(f"Etwo{fam}NGeTwo", len(ge2))
    mac(f"Etwo{fam}KstarGeOne", pct(np.mean([r["kstar"] >= 1 for r in ge2])) if ge2 else "--")
    mac(f"Etwo{fam}KstarGap", num(np.mean([r["f_any_signed_C"] - 1 - r["kstar"] for r in ge2]), 1) if ge2 else "--")
    # exact search cost
    mac(f"Etwo{fam}TimeAnyMs", f"{1e3*np.mean([r['t_any_C'] for r in rs]):.0f}")
    tl = [r["t_leave_C"] for r in rs if "t_leave_C" in r]
    mac(f"Etwo{fam}TimeLeaveMs", f"{1e3*np.mean(tl):.0f}")
    mac(f"Etwo{fam}TimeLeaveMaxS", f"{np.max(tl):.1f}")
    rl = [r["refits_leave_C"] for r in rs if "refits_leave_C" in r]
    mac(f"Etwo{fam}RefitsLeaveMax", int(np.max(rl)))
    ol = [r["oracle_leave_C"] for r in rs if "oracle_leave_C" in r]
    mac(f"Etwo{fam}OracleLeaveMax", int(np.max(ol)))

# ------------------------------------------------------------------ E3 heuristics
crit = fm["criterion"]
mac("EthreeCritExact", pct(crit["exact"]))
mac("EthreeCritCost", pct(crit["cost"]))
ver = fra["verdict"]
names = {"onestep": "one-step greedy", "amip": "sorted scores (AMIP-style)", "cook": "Cook's distance"}
with open(os.path.join(OUT, "table_e3.tex"), "w") as fh:
    for fam in fm["families"]:
        for tgt in ["any", "leave", "enter"]:
            for meth in ["onestep", "amip", "cook"]:
                v = ver[f"{fam}_{tgt}_{meth}"]
                fh.write(f"{fam} & {tgt} & {names[meth]} & {v['n']} & {pct(v['exact'])}\\% & {v['n_nontrivial']} & {pct(v['exact_nontrivial'])}\\% & {num(v['median_cost_ratio'])} & {'yes' if v['advantage'] else 'no'} \\\\\n")
                mac(f"Ethree{fam}{tgt.capitalize()}{meth.capitalize()}Exact", pct(v["exact"]))
                mac(f"Ethree{fam}{tgt.capitalize()}{meth.capitalize()}ExactNT", pct(v["exact_nontrivial"]))
                mac(f"Ethree{fam}{tgt.capitalize()}{meth.capitalize()}Cost", num(v["median_cost_ratio"]))
mac("EthreeAnyAdvantage", "none" if not any(v["advantage"] for v in ver.values()) else "some")
mac("EthreeNumAdvantage", sum(v["advantage"] for v in ver.values()))
mac("EthreeNumVerdicts", len(ver))
# amip prediction accuracy pooled
for fam in fm["families"]:
    rs = [r for r in fra["records"] if r["family"] == fam]
    for tgt, fkey in [("any", "f_any_C"), ("leave", "f_leave_C"), ("enter", "f_enter_C")]:
        base = [r for r in rs if fkey in r and r[fkey] is not None and r.get(f"g_{tgt}_amip_kpred") is not None]
        mac(f"Ethree{fam}{tgt.capitalize()}KpredExact", pct(np.mean([r[f"g_{tgt}_amip_kpred"] == r[fkey] for r in base])) if base else "--")
        mac(f"Ethree{fam}{tgt.capitalize()}KpredUnder", pct(np.mean([r[f"g_{tgt}_amip_kpred"] < r[fkey] for r in base])) if base else "--")
        mac(f"Ethree{fam}{tgt.capitalize()}KpredOver", pct(np.mean([r[f"g_{tgt}_amip_kpred"] > r[fkey] for r in base])) if base else "--")
# max gaps pooled
for fam in fm["families"]:
    rs = [r for r in fra["records"] if r["family"] == fam]
    for meth in ["onestep", "amip", "cook"]:
        gaps = []
        for tgt, fkey in [("any", "f_any_C"), ("leave", "f_leave_C"), ("enter", "f_enter_C")]:
            gaps += [r[f"g_{tgt}_{meth}_f"] - r[fkey] for r in rs if fkey in r and r[fkey] is not None and r.get(f"g_{tgt}_{meth}_f") is not None]
        mac(f"Ethree{fam}{meth.capitalize()}MaxGap", int(max(gaps)) if gaps else "--")
        mac(f"Ethree{fam}{meth.capitalize()}MeanGap", num(np.mean(gaps)) if gaps else "--")

# ------------------------------------------------------------------ E5 non-monotonicity
with open(os.path.join(OUT, "table_e5.tex"), "w") as fh:
    for a in agg:
        fh.write(f"{a['family']} & {a['n']} & {a['nm_leave_instances']} & {pct(a['nm_leave_frac_instances_with_back'])}\\% & {pct(a['nm_leave_frac_pairs_back'],1)}\\% & {a['nm_any_instances']} & {pct(a['nm_any_frac_instances_with_back'])}\\% & {pct(a['nm_any_frac_pairs_back'],1)}\\% \\\\\n")
for fam in fm["families"]:
    rs = [r for r in fra["records"] if r["family"] == fam]
    for tgt in ["leave", "any"]:
        rr = [r for r in rs if r.get(f"nm_{tgt}_pairs", 0) > 0]
        mac(f"Efive{fam}{tgt.capitalize()}Instances", len(rr))
        mac(f"Efive{fam}{tgt.capitalize()}FracInst", pct(np.mean([r[f"nm_{tgt}_back"] > 0 for r in rr])) if rr else "--")
        mac(f"Efive{fam}{tgt.capitalize()}FracPairs", pct(sum(r[f"nm_{tgt}_back"] for r in rr) / sum(r[f"nm_{tgt}_pairs"] for r in rr), 1) if rr else "--")
        mac(f"Efive{fam}{tgt.capitalize()}Pairs", sum(r[f"nm_{tgt}_pairs"] for r in rr))

# ------------------------------------------------------------------ E4 scaling
sm = sca["meta"]
mac("EfourKmax", sm["kmax"])
mac("EfourNmaxExact", max(sm["ns_exact"]))
mac("EfourNmaxGreedy", max(sm["ns_greedy"]))
with open(os.path.join(OUT, "table_e4.tex"), "w") as fh:
    for a in sca["exact"]:
        d = a["f_C_dist"]
        dist = "/".join(str(d[str(k)]) for k in range(1, sm["kmax"] + 1)) + f"/{d['notfound']}"
        fh.write(f"{a['family']} & {a['n']} & {pct(a['frac_true_support'])}\\% & {dist} & {num(a['f_C_median'],1)} & {pct(a['f_C_frac1'])}\\% & {num(a['f_P_median'],1)} & {pct(a['greedy_onestep_exact_C'])}\\% & {pct(a['greedy_sorted_exact_C'])}\\% & {num(a['kstar_mean'])} & {num(a['t_C_mean'])} & {num(a['cost_ratio_onestep_median'],2)} \\\\\n")
with open(os.path.join(OUT, "table_e4b.tex"), "w") as fh:
    for a in sca["greedy"]:
        fh.write(f"{a['family']} & {a['n']} & {pct(a['frac_true_support'])}\\% & {a['g_onestep_C_median']:.0f} [{a['g_onestep_C_q1']:.0f}, {a['g_onestep_C_q3']:.0f}] & {num(a['g_onestep_C_mean_over_n'],3)} & {a['g_sorted_C_median']:.0f} & {a['g_onestep_P_median']:.0f} & {a['kstar_median']:.0f} & {pct(a['frac_kstar_ge1'])}\\% & {num(a['mean_bracket_ratio'])} & {num(a['t_onestep_mean'],3)} \\\\\n")
for a in sca["exact"]:
    tag = a["family"] + word(a["n"])
    mac(f"Efour{tag}Mean", num(a["f_C_mean"]))
    mac(f"Efour{tag}FracOne", pct(a["f_C_frac1"]))
    mac(f"Efour{tag}NotFound", a["f_C_dist"]["notfound"])
    mac(f"Efour{tag}Time", num(a["t_C_mean"]))
    mac(f"Efour{tag}OnestepExact", pct(a["greedy_onestep_exact_C"]))
    mac(f"Efour{tag}AmipExact", pct(a["greedy_sorted_exact_C"]))
    mac(f"Efour{tag}KpredExact", pct(a["amip_kpred_exact"]))
    mac(f"Efour{tag}CostOnestep", num(a["cost_ratio_onestep_median"], 3))
    mac(f"Efour{tag}Instances", a["instances"])
for a in sca["greedy"]:
    tag = a["family"] + word(a["n"])
    mac(f"Efour{tag}Median", f"{a['g_onestep_C_median']:.0f}")
    mac(f"Efour{tag}MeanOverN", num(a["g_onestep_C_mean_over_n"], 3))
    mac(f"Efour{tag}Kstar", f"{a['kstar_median']:.0f}")
    mac(f"Efour{tag}Bracket", num(a["mean_bracket_ratio"]))
    mac(f"Efour{tag}TimeMs", f"{1e3*a['t_onestep_mean']:.0f}")
# pooled: exactness of one-step greedy over all exact instances with n>=18, nontrivial
recs = sca["records_exact"]
for fam in sm["families"]:
    rr = [r for r in recs if r["family"] == fam and r["f_C"] is not None]
    nt = [r for r in rr if r["f_C"] >= 2]
    mac(f"Efour{fam}OnestepExactAll", pct(np.mean([r["g_onestep_C"] == r["f_C"] for r in rr])) if rr else "--")
    mac(f"Efour{fam}OnestepExactNT", pct(np.mean([r["g_onestep_C"] == r["f_C"] for r in nt])) if nt else "--")
    mac(f"Efour{fam}AmipExactNT", pct(np.mean([r["g_sorted_C"] == r["f_C"] for r in nt])) if nt else "--")
    mac(f"Efour{fam}NT", len(nt))
    mac(f"Efour{fam}NAll", len(rr))
    mac(f"Efour{fam}OnestepMaxGap", int(max(r["g_onestep_C"] - r["f_C"] for r in rr)) if rr else "--")
    mac(f"Efour{fam}CostOnestepMedian", num(np.median([r["t_onestep_C"] / r["t_C"] for r in rr if r["t_C"] > 0]), 2) if rr else "--")
    big = [r for r in rr if r["n"] >= 22]
    mac(f"Efour{fam}CostOnestepMedianBig", num(np.median([r["t_onestep_C"] / r["t_C"] for r in big if r["t_C"] > 0]), 3) if big else "--")
    mac(f"Efour{fam}OnestepExactBig", pct(np.mean([r["g_onestep_C"] == r["f_C"] for r in big])) if big else "--")
    mac(f"Efour{fam}NBig", len(big))
    mac(f"Efour{fam}NotFoundAll", sum(r["f_C"] is None for r in recs if r["family"] == fam))
    mac(f"Efour{fam}KpredExactAll", pct(np.mean([r["kpred_amip_C"] == r["f_C"] for r in rr])) if rr else "--")

# table bodies: drop the trailing row terminator (main.tex supplies it after \input)
for fn in os.listdir(OUT):
    if fn.startswith("table_") and fn.endswith(".tex"):
        p = os.path.join(OUT, fn)
        body = open(p).read().rstrip()
        if body.endswith("\\\\"):
            body = body[:-2].rstrip()
        open(p, "w").write(body + "\n")

with open(os.path.join(OUT, "numbers.tex"), "w") as fh:
    fh.write("% generated by experiments/make_numbers.py -- do not edit\n")
    fh.write("\n".join(L) + "\n")
print(f"wrote {len(L)} macros")
