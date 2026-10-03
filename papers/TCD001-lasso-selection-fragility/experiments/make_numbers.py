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


def _pct_digits(x, d):
    """One extra decimal when rounding would print 100 for a value below 1 or 0 for a positive value
    (round-2 finding m10: 237/238 must not print as 100%)."""
    if d == 0 and x is not None and (0.995 <= x < 1.0 or 0.0 < x < 0.005):
        return 1
    return d


def pct(x, d=0):
    return "--" if x is None else f"{100*x:.{_pct_digits(x, d)}f}"


def pctcell(x, d=0):
    """Percentage for a table cell: appends the % sign only when there is a value."""
    return "--" if x is None else f"{100*x:.{_pct_digits(x, d)}f}\\%"


def sig2(x):
    """Two significant digits (round-2 finding M2: cost ratios vary between runs, more digits are
    spurious).  Integers >= 10 are printed without a decimal point."""
    if x is None:
        return "--"
    if x == 0:
        return "0"
    if abs(x) >= 9.95:
        return f"{x:.0f}"
    out = f"{x:#.2g}"
    return out.rstrip(".") if "e" not in out else f"{x:.2g}"


def half(x):
    """A median of integers: printed as an integer, or with one decimal when it is a half (m5)."""
    return f"{x:.0f}" if float(x).is_integer() else f"{x:.1f}"


def sci(x, digits=2):
    """x as LaTeX scientific notation with `digits` significant digits, e.g. 3.6\\times10^{-14}."""
    m, e = f"{x:.{digits-1}e}".split("e")
    return rf"{m}\times10^{{{int(e)}}}"


def num(x, d=2):
    return "--" if x is None else f"{x:.{d}f}"


def se_pct(p, n, d=1):
    """Binomial standard error of a proportion, in percentage points."""
    return "--" if (p is None or not n) else f"{100*np.sqrt(p*(1-p)/n):.{d}f}"


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


def thousands(n):
    return f"{n:,}".replace(",", "{,}")


# ------------------------------------------------------------------ KKT guard of the solver (round-2 M1, m4)
# Counters written by each script into meta.kkt_guard (lasso_fragility.KKT_STATS).  The manuscript
# states (Limitations, Appendix A) that the fallback was triggered only in the integer-data search of
# E0, always at an exact tie of |x_j^T y| at the first entry, without changing the examples, and never
# in E1-E5; the assertions below make the build fail if a rerun contradicts that text.
kg0 = exa["meta"]["kkt_guard"]
kg_later = [val["meta"]["kkt_guard"], fra["meta"]["kkt_guard"], sca["meta"]["kkt_guard"]]
mac("EzeroFits", kg0["calls"])
mac("EzeroFallbacks", kg0["fallbacks"])
mac("EzeroFallbacksTie", kg0["fallbacks_tie_at_entry"])
mac("EzeroFallbacksFullRank", kg0["fallbacks_full_rank"])
mac("EzeroRejectedMaxErr", f"{kg0['max_active_rel_rejected']:.1f}")
mac("EzeroFallbackMaxErr", sci(kg0["max_active_rel_fallback"], 1) if kg0["max_active_rel_fallback"] > 0 else "0")
mac("EoneToFiveFits", thousands(sum(k["calls"] for k in kg_later)))
mac("EoneToFiveFallbacks", sum(k["fallbacks"] for k in kg_later))
kkt_act = max(k["max_active_rel"] for k in kg_later)
mac("KKTMaxActiveRel", sci(kkt_act, 2))
mac("KKTMaxInactiveRel", sci(max(k["max_inactive_rel"] for k in kg_later), 2) if max(k["max_inactive_rel"] for k in kg_later) > 0 else "0")
assert sum(k["fallbacks"] for k in kg_later) == 0, "text says the KKT fallback never fires in E1-E5"
assert kg0["fallbacks_tie_at_entry"] == kg0["fallbacks"] == kg0["fallbacks_full_rank"], "text says all E0 fallbacks are exact ties with full-rank X"
ng_path = os.path.join(RES, "examples_noguard.json")
if os.path.exists(ng_path):
    ng = json.load(open(ng_path))
    a_cmp = {k: v for k, v in exa.items() if k not in ("seconds", "meta")}
    b_cmp = {k: v for k, v in ng.items() if k not in ("seconds", "meta")}
    assert a_cmp == b_cmp, "text says the examples are identical with and without the KKT guard"
    mac("EzeroGuardIdentical", "identical")
    mac("EzeroNoGuardFits", ng["meta"]["kkt_guard"]["calls"])

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
# Example 4.2 (p = 1, leave and enter variants): number of (data set, rule) combinations verified exactly
ex1_checks = [e["exact_ok"] for key in ("example1", "example1b") if key in exa
              for rule in ("C", "P") for e in exa[key]["analysis"][rule]]
mac("ExOneChecks", f"{sum(ex1_checks)}/{len(ex1_checks)}")
mac("ExOnebPresent", "yes" if "example1b" in exa else "no")

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
        fh.write(f"{r['n']} & {r['p']} & {r['instances']} & {r['stable_single_removals']} & {r['certified_by_cor2']} & {pctcell(r['cor2_coverage'])} & {pctcell(r['frac_f1'])} & {pctcell(r['frac_kstar_ge1_given_f_ge2'])} & {num(r['mean_gap_given_f_ge2'])} \\\\\n")
mac("EoneCorInstancesPerCell", C[0]["instances"])

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
# cost ratio with the heuristic's initial fit removed (round-1 finding M5): the exhaustive-search
# timer starts after the initial fit and the O(n p s0) precomputation, while the heuristic timer
# includes its initial fit.  We subtract one refit's worth of time, estimated per instance as the
# heuristic's total time divided by its number of refits (this also removes one scoring step, so
# the adjustment favours the heuristic).
adj_ratios = {}
for fam in fm["families"]:
    for tgt in ["any", "leave", "enter"]:
        fkey = {"any": "f_any_C", "leave": "f_leave_C", "enter": "f_enter_C"}[tgt]
        tkey = {"any": "t_any_C", "leave": "t_leave_C", "enter": "t_enter_C"}[tgt]
        base = [r for r in fra["records"] if r["family"] == fam and fkey in r and r[fkey] is not None and r[tkey] > 0]
        for meth in ["onestep", "amip", "cook"]:
            rr = [(r[f"g_{tgt}_{meth}_t"] * (1 - 1 / r[f"g_{tgt}_{meth}_refits"])) / r[tkey] for r in base
                  if r.get(f"g_{tgt}_{meth}_refits")]
            adj_ratios[f"{fam}_{tgt}_{meth}"] = float(np.median(rr)) if rr else None
mac("EthreeMinCostAdjusted", sig2(min(v for v in adj_ratios.values() if v is not None)))
mac("EthreeMinCostRaw", sig2(min(v["median_cost_ratio"] for v in ver.values() if v["median_cost_ratio"] is not None)))
assert min(v["median_cost_ratio"] for v in ver.values()) > crit["cost"] and min(adj_ratios.values()) > crit["cost"], \
    "text says no heuristic meets the cost part at n <= 14, even after the adjustment"
with open(os.path.join(OUT, "table_e3.tex"), "w") as fh:
    for fam in fm["families"]:
        for tgt in ["any", "leave", "enter"]:
            for meth in ["onestep", "amip", "cook"]:
                v = ver[f"{fam}_{tgt}_{meth}"]
                fh.write(f"{fam} & {tgt} & {names[meth]} & {v['n']} & {pct(v['exact'])}\\% $\\pm$ {se_pct(v['exact'], v['n'])} & {v['n_nontrivial']} & {pctcell(v['exact_nontrivial'])} & {sig2(v['median_cost_ratio'])} & {sig2(adj_ratios[f'{fam}_{tgt}_{meth}'])} & {'yes' if v['advantage'] else 'no'} \\\\\n")
                mac(f"Ethree{fam}{tgt.capitalize()}{meth.capitalize()}Exact", pct(v["exact"]))
                mac(f"Ethree{fam}{tgt.capitalize()}{meth.capitalize()}ExactSE", se_pct(v["exact"], v["n"]))
                mac(f"Ethree{fam}{tgt.capitalize()}{meth.capitalize()}ExactNT", pct(v["exact_nontrivial"]))
                mac(f"Ethree{fam}{tgt.capitalize()}{meth.capitalize()}Cost", sig2(v["median_cost_ratio"]))
                mac(f"Ethree{fam}{tgt.capitalize()}{meth.capitalize()}CostAdj", sig2(adj_ratios[f"{fam}_{tgt}_{meth}"]))
                mac(f"Ethree{fam}{tgt.capitalize()}{meth.capitalize()}N", v["n"])
# how far below the 90% threshold is the one-step greedy on ENTER, in standard errors
for fam in fm["families"]:
    v = ver[f"{fam}_enter_onestep"]
    se = np.sqrt(v["exact"] * (1 - v["exact"]) / v["n"])
    mac(f"Ethree{fam}EnterOnestepShortfallSE", f"{(crit['exact'] - v['exact']) / se:.1f}")
mac("EthreeNMin", min(v["n"] for v in ver.values()))
mac("EthreeNMax", max(v["n"] for v in ver.values()))
ses = [100 * np.sqrt(v["exact"] * (1 - v["exact"]) / v["n"]) for v in ver.values() if v["exact"] not in (None, 0.0, 1.0)]
mac("EthreeSEMin", f"{min(ses):.1f}")
mac("EthreeSEMax", f"{max(ses):.1f}")
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
        fh.write(f"{a['family']} & {a['n']} & {pct(a['frac_true_support'])}\\% & {dist} & {num(a['f_C_median'],1)} & {pct(a['f_C_frac1'])}\\% & {num(a['f_P_median'],1)} & {pct(a['greedy_onestep_exact_C'])}\\% & {pct(a['greedy_sorted_exact_C'])}\\% & {num(a['kstar_mean'])} & {num(a['t_C_mean'])} & {sig2(a['cost_ratio_onestep_median'])} \\\\\n")
with open(os.path.join(OUT, "table_e4b.tex"), "w") as fh:
    for a in sca["greedy"]:
        fh.write(f"{a['family']} & {a['n']} & {pct(a['frac_true_support'])}\\% & {half(a['g_onestep_C_median'])} [{half(a['g_onestep_C_q1'])}, {half(a['g_onestep_C_q3'])}] & {num(a['g_onestep_C_mean_over_n'],3)} & {half(a['g_sorted_C_median'])} & {half(a['g_onestep_P_median'])} & {half(a['kstar_median'])} & {pct(a['frac_kstar_ge1'])}\\% & {num(a['mean_bracket_ratio'])} & {num(a['t_onestep_mean'],3)} \\\\\n")
for a in sca["exact"]:
    tag = a["family"] + word(a["n"])
    mac(f"Efour{tag}Mean", num(a["f_C_mean"]))
    mac(f"Efour{tag}FracOne", pct(a["f_C_frac1"]))
    mac(f"Efour{tag}NotFound", a["f_C_dist"]["notfound"])
    mac(f"Efour{tag}Time", num(a["t_C_mean"]))
    mac(f"Efour{tag}OnestepExact", pct(a["greedy_onestep_exact_C"]))
    mac(f"Efour{tag}AmipExact", pct(a["greedy_sorted_exact_C"]))
    mac(f"Efour{tag}KpredExact", pct(a["amip_kpred_exact"]))
    mac(f"Efour{tag}CostOnestep", sig2(a["cost_ratio_onestep_median"]))
    mac(f"Efour{tag}Instances", a["instances"])
for a in sca["greedy"]:
    tag = a["family"] + word(a["n"])
    mac(f"Efour{tag}Median", half(a["g_onestep_C_median"]))
    mac(f"Efour{tag}MeanOverN", num(a["g_onestep_C_mean_over_n"], 3))
    mac(f"Efour{tag}Kstar", half(a["kstar_median"]))
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
    mac(f"Efour{fam}CostOnestepMedian", sig2(np.median([r["t_onestep_C"] / r["t_C"] for r in rr if r["t_C"] > 0])) if rr else "--")
    big = [r for r in rr if r["n"] >= 22]
    mac(f"Efour{fam}CostOnestepMedianBig", sig2(np.median([r["t_onestep_C"] / r["t_C"] for r in big if r["t_C"] > 0])) if big else "--")
    mac(f"Efour{fam}OnestepExactBig", pct(np.mean([r["g_onestep_C"] == r["f_C"] for r in big])) if big else "--")
    mac(f"Efour{fam}NBig", len(big))
    # same statistics over all instances with n >= 22, including those whose f was not found within the cap
    big_all = [r for r in recs if r["family"] == fam and r["n"] >= 22]
    mac(f"Efour{fam}CostOnestepMedianBigAll", sig2(np.median([r["t_onestep_C"] / r["t_C"] for r in big_all if r["t_C"] > 0])) if big_all else "--")
    mac(f"Efour{fam}NBigAll", len(big_all))
    mac(f"Efour{fam}NotFoundAll", sum(r["f_C"] is None for r in recs if r["family"] == fam))
    mac(f"Efour{fam}KpredExactAll", pct(np.mean([r["kpred_amip_C"] == r["f_C"] for r in rr])) if rr else "--")

# ------------------------------------------------------------------ E4 cost of the greedy (round-2 finding M2)
# Accuracy of the one-step greedy at n = 34 (family A) with its binomial standard error.
a34 = next(a for a in sca["exact"] if a["family"] == "A" and a["n"] == 34)
p34 = a34["greedy_onestep_hits_C"] / a34["n_finite_C"]
mac("EfourAThirtyfourHits", a34["greedy_onestep_hits_C"])
mac("EfourAThirtyfourFinite", a34["n_finite_C"])
mac("EfourAThirtyfourOnestepSE", se_pct(p34, a34["n_finite_C"], 0))
mac("EfourAThirtyfourShortfallSE", f"{(crit['exact'] - p34) / np.sqrt(p34 * (1 - p34) / a34['n_finite_C']):.1f}")
# Median wall-clock times in family B (current run): one batch of closed-form tests vs the greedy.
bcells = [a for a in sca["exact"] if a["family"] == "B"]
mac("EfourBExhMsMax", f"{1e3*max(a['t_C_median'] for a in bcells):.2f}")
mac("EfourBGreedyMsMin", f"{1e3*min(a['t_onestep_median'] for a in bcells):.1f}")
mac("EfourBGreedyMsMax", f"{1e3*max(a['t_onestep_median'] for a in bcells):.1f}")
# Cell medians of the cost ratio of the one-step greedy over all archived complete runs
# (results/cost_ratios_run_*.json, written by snapshot_cost_ratios.py) and the current run.
import glob
runs4 = [{f"{a['family']}_{a['n']}_onestep": a["cost_ratio_onestep_median"] for a in sca["exact"]}]
runs3 = [{k: v["median_cost_ratio"] for k, v in ver.items()}]
for fn in sorted(glob.glob(os.path.join(RES, "cost_ratios_run_*.json"))):
    rj = json.load(open(fn))
    runs4.append({k: v for k, v in rj["e4_median_cost_ratio"].items() if k.endswith("_onestep") and "ge22" not in k})
    runs3.append(rj["e3_median_cost_ratio"])
mac("CostRuns", {1: "one", 2: "two", 3: "three", 4: "four"}.get(len(runs4), len(runs4)))


def span(keys):
    vals = [r[k] for r in runs4 for k in keys]
    return min(vals), max(vals)


fac4 = {k: max(r[k] for r in runs4) / min(r[k] for r in runs4) for k in runs4[0]}
kmax4 = max(fac4, key=fac4.get)
mac("EfourRunFactor", sig2(fac4[kmax4]))
mac("EfourRunFactorFam", kmax4.split("_")[0])
mac("EfourRunFactorN", kmax4.split("_")[1])
fac3 = {k: max(r[k] for r in runs3) / min(r[k] for r in runs3) for k in runs3[0]}
mac("EthreeRunFactor", sig2(max(fac3.values())))
groups = {"EfourACostSmall": [f"A_{n}_onestep" for n in (10, 14, 18)],
          "EfourACostMid": [f"A_{n}_onestep" for n in (22, 26)],
          "EfourAThirtyCost": ["A_30_onestep"], "EfourAThirtyfourCost": ["A_34_onestep"],
          "EfourBCost": [f"B_{n}_onestep" for n in sm["ns_exact"]]}
for name, keys in groups.items():
    lo, hi = span(keys)
    mac(name + "Lo", sig2(lo))
    mac(name + "Hi", sig2(hi))
# qualitative statements of Section 6 (E4), checked over every archived run:
assert span(groups["EfourACostSmall"])[0] > 1 and span(groups["EfourBCost"])[0] > 1, "greedy slower: A n<=18, B all n"
assert span(groups["EfourAThirtyCost"])[1] < 1, "greedy faster at A n=30"
assert span(groups["EfourAThirtyfourCost"])[1] <= crit["cost"], "below the cost threshold at A n=34"
assert all(span([k])[0] > crit["cost"] for k in runs4[0] if k != "A_34_onestep"), "only at A n=34 below the threshold"
assert all(span([f"A_{n}_onestep"])[1] >= 1 for n in (22, 26)), "cheaper in all runs only at A n>=30"

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
