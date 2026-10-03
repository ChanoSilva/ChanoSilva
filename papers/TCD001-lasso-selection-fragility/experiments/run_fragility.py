#!/usr/bin/env python3
"""
E2 (exact minimal witnesses), E3 (heuristics vs exact, predefined criterion) and E5 (frequency of
non-monotone changes) on synthetic designs with n <= 14.

Writes results/fragility.json (per-instance records + aggregates) and results/fragility.md.
"""
import json
import os
import platform
import sys
import time

import numpy as np
import scipy
import sklearn

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import lasso_fragility as LF  # noqa: E402  (KKT-guard counter, round-2 finding M1)
from lasso_fragility import (FAMILIES, certificate_k, fit_state, fragility_exact, heuristic,
                             lasso_lars, make_family_instance, refit_pattern, signed_pattern)

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
SEED = 20260930
FAST = "--fast" in sys.argv
NS = [8, 10, 12, 14]
REPS = 5 if FAST else 60
KMAX_TARGETED = 5
METHODS = ["onestep", "amip", "cook"]
TARGETS = ["any", "leave", "enter"]
# Predefined criterion for "computational advantage" of a heuristic (fixed before the run):
CRIT_EXACT = 0.90     # returns a witness of exactly minimal size in >= 90% of instances with finite f
CRIT_COST = 0.10      # at a median cost <= 10% of the exhaustive search (wall-clock, same machine)


def change_type(S0, s0, S1, s1):
    left = set(S0.tolist()) - set(S1.tolist())
    entered = set(S1.tolist()) - set(S0.tolist())
    if left and entered:
        return "swap"
    if left:
        return "leave"
    if entered:
        return "enter"
    return "sign_only"


def main():
    t_start = time.time()
    LF.reset_kkt_stats()
    rng = np.random.default_rng(SEED)
    records = []
    for fam in FAMILIES:
        for n in NS:
            for rep in range(REPS):
                X, y, mu, bstar = make_family_instance(rng, n, fam)
                st = fit_state(X, y, mu)
                rec = dict(family=fam, n=n, rep=rep, p=X.shape[1], support=st.S.tolist(),
                           support_size=int(len(st.S)), true_support=bool(np.array_equal(st.S, np.flatnonzero(bstar))),
                           gamma=float(st.gamma) if np.isfinite(st.gamma) else None,
                           m=float(st.m) if np.isfinite(st.m) else None, kstar=int(certificate_k(st, n - 2)))
                # ---- exact: any change of the signed support, rules C and P
                for rule in ["C", "P"]:
                    fe = fragility_exact(st, "any_signed", rule, kmax=n - 2)
                    rec[f"f_any_signed_{rule}"] = fe["f"]
                    rec[f"t_any_signed_{rule}"] = fe["seconds"]
                    rec[f"nwit_any_signed_{rule}"] = len(fe["witnesses"])
                    if fe["f"] is not None:
                        types = []
                        for R in fe["witnesses"][:20]:
                            S1, s1 = refit_pattern(X, y, mu, R, rule, n)
                            types.append(change_type(st.S, st.s, S1, s1))
                        rec[f"types_any_signed_{rule}"] = types
                        # the first witness of size f, used below for the 'any' (unsigned) check
                # ---- exact: unsigned any change, leave weakest, enter strongest (rule C)
                fe_any = fragility_exact(st, "any", "C", kmax=n - 2)
                rec["f_any_C"] = fe_any["f"]
                rec["t_any_C"] = fe_any["seconds"]
                rec["refits_any_C"] = fe_any["n_refit"]
                j_leave = int(st.S[np.argmin(np.abs(st.betaS))]) if len(st.S) else None
                j_enter = int(st.Sc[np.argmax(np.abs(st.c[st.Sc]))]) if len(st.Sc) else None
                rec["j_leave"], rec["j_enter"] = j_leave, j_enter
                exact = {"any": fe_any}
                if j_leave is not None:
                    fe = fragility_exact(st, "leave", "C", j_leave, kmax=min(n - 2, KMAX_TARGETED))
                    exact["leave"] = fe
                    rec["f_leave_C"], rec["t_leave_C"], rec["refits_leave_C"], rec["oracle_leave_C"] = fe["f"], fe["seconds"], fe["n_refit"], fe["n_oracle"]
                if j_enter is not None:
                    fe = fragility_exact(st, "enter", "C", j_enter, kmax=min(n - 2, KMAX_TARGETED))
                    exact["enter"] = fe
                    rec["f_enter_C"], rec["t_enter_C"], rec["refits_enter_C"], rec["oracle_enter_C"] = fe["f"], fe["seconds"], fe["n_refit"], fe["n_oracle"]
                # ---- greedy heuristics (rule C)
                for tgt in TARGETS:
                    j = {"any": None, "leave": j_leave, "enter": j_enter}[tgt]
                    if tgt != "any" and j is None:
                        continue
                    for meth in METHODS:
                        g = heuristic(X, y, mu, tgt, "C", j, meth, budget=n - 2)
                        if meth == "amip":
                            rec[f"g_{tgt}_amip_kpred"] = g["k_pred"]
                        rec[f"g_{tgt}_{meth}_f"] = g["f"]
                        rec[f"g_{tgt}_{meth}_t"] = g["seconds"]
                        rec[f"g_{tgt}_{meth}_refits"] = g["n_refit"]
                # ---- non-monotonicity: supersets (by one element) of minimal witnesses
                for tgt in ["leave", "any"]:
                    fe = exact.get(tgt)
                    if fe is None or fe["f"] is None:
                        continue
                    pairs = back = 0
                    for R in fe["witnesses"][:20]:
                        for i in range(n):
                            if i in R:
                                continue
                            Rp = tuple(sorted(R + (i,)))
                            if len(Rp) >= n - 1:
                                continue
                            S1, s1 = refit_pattern(X, y, mu, Rp, "C", n)
                            pairs += 1
                            if tgt == "leave":
                                back += int(j_leave in set(S1.tolist()))
                            else:
                                back += int(np.array_equal(S1, st.S))
                    rec[f"nm_{tgt}_pairs"], rec[f"nm_{tgt}_back"] = pairs, back
                records.append(rec)
            done = [r for r in records if r["family"] == fam and r["n"] == n]
            fs = [r["f_any_signed_C"] for r in done]
            print(f"family {fam} n={n}: {len(done)} instances, f_any_signed(C) mean {np.mean([f if f else n-1 for f in fs]):.2f}, "
                  f"P(f=1)={np.mean([f==1 for f in fs]):.2f}, elapsed {time.time()-t_start:.0f}s", flush=True)

    # ---------------------------------------------------------------- aggregates
    agg = []
    for fam in FAMILIES:
        for n in NS:
            rs = [r for r in records if r["family"] == fam and r["n"] == n]
            a = dict(family=fam, n=n, instances=len(rs), p=rs[0]["p"],
                     mean_support=float(np.mean([r["support_size"] for r in rs])),
                     frac_true_support=float(np.mean([r["true_support"] for r in rs])),
                     frac_empty_support=float(np.mean([r["support_size"] == 0 for r in rs])))
            for rule in ["C", "P"]:
                fs = np.array([r[f"f_any_signed_{rule}"] if r[f"f_any_signed_{rule}"] is not None else np.nan for r in rs], float)
                a[f"f_any_signed_{rule}_dist"] = {str(k): int(np.sum(fs == k)) for k in range(1, 8)} | {"notfound": int(np.sum(np.isnan(fs)))}
                a[f"f_any_signed_{rule}_mean"] = float(np.nanmean(fs))
                a[f"f_any_signed_{rule}_median"] = float(np.nanmedian(fs))
                a[f"f_any_signed_{rule}_frac1"] = float(np.mean(fs == 1))
                a[f"f_any_signed_{rule}_max"] = int(np.nanmax(fs))
                types = sum([r.get(f"types_any_signed_{rule}", []) for r in rs], [])
                a[f"types_{rule}"] = {t: int(sum(1 for x in types if x == t)) for t in ["leave", "enter", "swap", "sign_only"]}
            a["frac_signed_ne_unsigned_C"] = float(np.mean([r["f_any_signed_C"] != r["f_any_C"] for r in rs]))
            a["kstar_mean"] = float(np.mean([r["kstar"] for r in rs]))
            fge2 = [r for r in rs if r["f_any_signed_C"] is not None and r["f_any_signed_C"] >= 2]
            a["n_f_ge2"] = len(fge2)
            a["frac_kstar_ge1_given_f_ge2"] = float(np.mean([r["kstar"] >= 1 for r in fge2])) if fge2 else None
            a["mean_gap_given_f_ge2"] = float(np.mean([r["f_any_signed_C"] - 1 - r["kstar"] for r in fge2])) if fge2 else None
            for tgt in ["leave", "enter"]:
                fs = [r.get(f"f_{tgt}_C") for r in rs if f"f_{tgt}_C" in r]
                fin = [f for f in fs if f is not None]
                a[f"f_{tgt}_C_n"] = len(fs)
                a[f"f_{tgt}_C_notfound"] = len(fs) - len(fin)
                a[f"f_{tgt}_C_mean"] = float(np.mean(fin)) if fin else None
                a[f"f_{tgt}_C_dist"] = {str(k): int(sum(1 for f in fin if f == k)) for k in range(1, KMAX_TARGETED + 1)}
            a["t_exact_any_C_mean"] = float(np.mean([r["t_any_C"] for r in rs]))
            a["t_exact_leave_C_mean"] = float(np.mean([r["t_leave_C"] for r in rs if "t_leave_C" in r])) if any("t_leave_C" in r for r in rs) else None
            a["t_exact_enter_C_mean"] = float(np.mean([r["t_enter_C"] for r in rs if "t_enter_C" in r])) if any("t_enter_C" in r for r in rs) else None
            # heuristics vs exact
            for tgt in TARGETS:
                fkey = {"any": "f_any_C", "leave": "f_leave_C", "enter": "f_enter_C"}[tgt]
                tkey = {"any": "t_any_C", "leave": "t_leave_C", "enter": "t_enter_C"}[tgt]
                base = [r for r in rs if fkey in r and r[fkey] is not None]
                for meth in METHODS:
                    gf = [r[f"g_{tgt}_{meth}_f"] for r in base]
                    ex = [r[fkey] for r in base]
                    found = [g is not None for g in gf]
                    exact_hit = [g is not None and g == e for g, e in zip(gf, ex)]
                    gaps = [g - e for g, e in zip(gf, ex) if g is not None]
                    ratio = [r[f"g_{tgt}_{meth}_t"] / r[tkey] for r in base if r[tkey] > 0]
                    a[f"h_{tgt}_{meth}"] = dict(n=len(base), found=float(np.mean(found)) if base else None,
                                                exact=float(np.mean(exact_hit)) if base else None,
                                                mean_gap=float(np.mean(gaps)) if gaps else None,
                                                max_gap=int(np.max(gaps)) if gaps else None,
                                                median_cost_ratio=float(np.median(ratio)) if ratio else None,
                                                mean_refits=float(np.mean([r[f"g_{tgt}_{meth}_refits"] for r in base])) if base else None)
            for tgt in TARGETS:
                fkey = {"any": "f_any_C", "leave": "f_leave_C", "enter": "f_enter_C"}[tgt]
                base = [r for r in rs if fkey in r and r[fkey] is not None and r.get(f"g_{tgt}_amip_kpred") is not None]
                a[f"amip_kpred_exact_{tgt}"] = float(np.mean([r[f"g_{tgt}_amip_kpred"] == r[fkey] for r in base])) if base else None
                a[f"amip_kpred_mean_diff_{tgt}"] = float(np.mean([r[f"g_{tgt}_amip_kpred"] - r[fkey] for r in base])) if base else None
            # non-monotonicity
            for tgt in ["leave", "any"]:
                rr = [r for r in rs if f"nm_{tgt}_pairs" in r and r[f"nm_{tgt}_pairs"] > 0]
                a[f"nm_{tgt}_instances"] = len(rr)
                a[f"nm_{tgt}_frac_instances_with_back"] = float(np.mean([r[f"nm_{tgt}_back"] > 0 for r in rr])) if rr else None
                a[f"nm_{tgt}_frac_pairs_back"] = float(sum(r[f"nm_{tgt}_back"] for r in rr) / sum(r[f"nm_{tgt}_pairs"] for r in rr)) if rr else None
            agg.append(a)

    # pooled heuristic verdicts (all n, per family and target)
    verdict = {}
    for fam in FAMILIES:
        for tgt in TARGETS:
            fkey = {"any": "f_any_C", "leave": "f_leave_C", "enter": "f_enter_C"}[tgt]
            tkey = {"any": "t_any_C", "leave": "t_leave_C", "enter": "t_enter_C"}[tgt]
            base = [r for r in records if r["family"] == fam and fkey in r and r[fkey] is not None]
            for meth in METHODS:
                exact_hit = float(np.mean([r[f"g_{tgt}_{meth}_f"] == r[fkey] for r in base])) if base else None
                ratios = [r[f"g_{tgt}_{meth}_t"] / r[tkey] for r in base if r[tkey] > 0]
                ratio = float(np.median(ratios)) if ratios else None
                q1, q3 = (float(v) for v in np.percentile(ratios, [25, 75])) if ratios else (None, None)
                nontriv = [r for r in base if r[fkey] >= 2]
                exact_nontriv = float(np.mean([r[f"g_{tgt}_{meth}_f"] == r[fkey] for r in nontriv])) if nontriv else None
                verdict[f"{fam}_{tgt}_{meth}"] = dict(family=fam, target=tgt, method=meth, n=len(base), exact=exact_hit,
                                                     n_nontrivial=len(nontriv), exact_nontrivial=exact_nontriv,
                                                     median_cost_ratio=ratio, cost_ratio_q1=q1, cost_ratio_q3=q3,
                                                     advantage=bool(exact_hit is not None and exact_hit >= CRIT_EXACT and ratio is not None and ratio <= CRIT_COST))
    out = dict(meta=dict(seed=SEED, python=platform.python_version(), numpy=np.__version__, scipy=scipy.__version__,
                         sklearn=sklearn.__version__, reps=REPS, ns=NS, kmax_targeted=KMAX_TARGETED,
                         families=FAMILIES, criterion=dict(exact=CRIT_EXACT, cost=CRIT_COST),
                         seconds=time.time() - t_start),
               aggregates=agg, verdict=verdict, records=records)
    out["meta"]["kkt_guard"] = LF.kkt_stats()
    print("KKT guard:", out["meta"]["kkt_guard"])
    os.makedirs(os.path.join(ROOT, "results"), exist_ok=True)
    with open(os.path.join(ROOT, "results", "fragility.json"), "w") as fh:
        json.dump(out, fh, indent=1)
    # ---- markdown
    L = ["# E2/E3/E5 — Exact fragility numbers, heuristics and non-monotonicity (n <= 14)", "",
         f"Seed {SEED}; {REPS} instances per (family, n); families {json.dumps(FAMILIES)}; targeted searches capped at |R| <= {KMAX_TARGETED}.", "",
         "## E2. Fragility number for any change of the signed support (rule C / rule P)", "",
         "| fam | n | p | mean |S| | P(S=S*) | f dist C (1..7, nf) | mean C | P(f=1) C | mean P | P(f=1) P | types C (leave/enter/swap/sign) | k* mean | P(k*>=1 given f>=2) | gap |",
         "|---|---|---|---|---|---|---|---|---|---|---|---|---|---|"]
    for a in agg:
        d = a["f_any_signed_C_dist"]
        dist = ",".join(str(d[str(k)]) for k in range(1, 8)) + f",{d['notfound']}"
        t = a["types_C"]
        L.append(f"| {a['family']} | {a['n']} | {a['p']} | {a['mean_support']:.2f} | {a['frac_true_support']:.2f} | {dist} | {a['f_any_signed_C_mean']:.2f} | {a['f_any_signed_C_frac1']:.2f} | {a['f_any_signed_P_mean']:.2f} | {a['f_any_signed_P_frac1']:.2f} | {t['leave']}/{t['enter']}/{t['swap']}/{t['sign_only']} | {a['kstar_mean']:.2f} | {a['frac_kstar_ge1_given_f_ge2']} | {a['mean_gap_given_f_ge2']} |")
    L += ["", "## E2b. Targeted fragility numbers (rule C): weakest selected variable leaves / strongest inactive enters", "",
          "| fam | n | leave: n | mean f | dist 1..5 | not found | enter: n | mean f | dist 1..5 | not found | mean exact time any/leave/enter (s) |", "|---|---|---|---|---|---|---|---|---|---|---|"]
    for a in agg:
        dl = ",".join(str(a["f_leave_C_dist"][str(k)]) for k in range(1, KMAX_TARGETED + 1))
        de = ",".join(str(a["f_enter_C_dist"][str(k)]) for k in range(1, KMAX_TARGETED + 1))
        L.append(f"| {a['family']} | {a['n']} | {a['f_leave_C_n']} | {a['f_leave_C_mean']} | {dl} | {a['f_leave_C_notfound']} | {a['f_enter_C_n']} | {a['f_enter_C_mean']} | {de} | {a['f_enter_C_notfound']} | {a['t_exact_any_C_mean']:.3f}/{a['t_exact_leave_C_mean']}/{a['t_exact_enter_C_mean']} |")
    L += ["", "## E3. Heuristics vs exact (rule C)", "", "| fam | n | target | method | n | found | exact | mean gap | max gap | median cost ratio | mean refits |", "|---|---|---|---|---|---|---|---|---|---|---|"]
    for a in agg:
        for tgt in TARGETS:
            for meth in METHODS:
                h = a[f"h_{tgt}_{meth}"]
                L.append(f"| {a['family']} | {a['n']} | {tgt} | {meth} | {h['n']} | {h['found']} | {h['exact']} | {h['mean_gap']} | {h['max_gap']} | {h['median_cost_ratio']} | {h['mean_refits']} |")
    L += ["", f"### Verdict with the predefined criterion (exact >= {CRIT_EXACT}, median cost ratio <= {CRIT_COST}), pooled over n", "",
          "Cost ratio = heuristic time / exhaustive-search time per instance; median and interquartile range [q1, q3] over the instances (round-2 finding m13).", "",
          "| fam | target | method | n | exact | n nontrivial (f>=2) | exact on nontrivial | median cost ratio | IQR cost ratio | advantage? |", "|---|---|---|---|---|---|---|---|---|---|"]
    for k, v in verdict.items():
        L.append(f"| {v['family']} | {v['target']} | {v['method']} | {v['n']} | {v['exact']} | {v['n_nontrivial']} | {v['exact_nontrivial']} | {v['median_cost_ratio']:.3f} | [{v['cost_ratio_q1']:.3f}, {v['cost_ratio_q3']:.3f}] | {v['advantage']} |")
    L += ["", "## E5. Non-monotonicity: one-element supersets of minimal witnesses", "",
          "| fam | n | leave: instances | frac instances with re-entry | frac pairs re-entry | any: instances | frac instances restored | frac pairs restored |", "|---|---|---|---|---|---|---|---|"]
    for a in agg:
        L.append(f"| {a['family']} | {a['n']} | {a['nm_leave_instances']} | {a['nm_leave_frac_instances_with_back']} | {a['nm_leave_frac_pairs_back']} | {a['nm_any_instances']} | {a['nm_any_frac_instances_with_back']} | {a['nm_any_frac_pairs_back']} |")
    L += ["", f"Total time {out['meta']['seconds']:.0f} s."]
    with open(os.path.join(ROOT, "results", "fragility.md"), "w") as fh:
        fh.write("\n".join(L) + "\n")
    print("done in", out["meta"]["seconds"], "s")


if __name__ == "__main__":
    main()
