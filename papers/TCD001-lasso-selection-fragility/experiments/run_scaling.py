#!/usr/bin/env python3
"""
E4: how the fragility number (any change of the signed support) scales with n.
  Part 1: exact minimal witnesses by exhaustive search with the closed-form removal test
          (n up to 30, |R| <= 6), rules C and P.
  Part 2: greedy upper bounds (one-step exact greedy) and certificate lower bounds (Prop. 3.4)
          for n up to 400, rule C.
Writes results/scaling.json and results/scaling.md.
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
from lasso_fragility import (FAMILIES, certificate_k, fit_state, fragility_exact, heuristic,
                             make_family_instance)

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
SEED = 20260931
FAST = "--fast" in sys.argv
NS_EXACT = [10, 14, 18, 22, 26, 30, 34]
KMAX = 6
NS_GREEDY = [50, 100, 200, 400]


def reps_exact(n):
    if FAST:
        return 3
    return 40 if n <= 22 else (30 if n <= 30 else 20)


def main():
    t_start = time.time()
    rng = np.random.default_rng(SEED)
    rec_exact, rec_greedy = [], []
    for fam in FAMILIES:
        for n in NS_EXACT:
            for rep in range(reps_exact(n)):
                X, y, mu, bstar = make_family_instance(rng, n, fam)
                st = fit_state(X, y, mu)
                r = dict(family=fam, n=n, rep=rep, support_size=int(len(st.S)),
                         true_support=bool(np.array_equal(st.S, np.flatnonzero(bstar))),
                         kstar=int(certificate_k(st, KMAX)))
                for rule in ["C", "P"]:
                    fe = fragility_exact(st, "any_signed", rule, kmax=min(KMAX, n - 2), max_witnesses=1)
                    r[f"f_{rule}"] = fe["f"]
                    r[f"t_{rule}"] = fe["seconds"]
                    r[f"oracle_{rule}"] = fe["n_oracle"]
                g = heuristic(X, y, mu, "any_signed", "C", None, "onestep", budget=n - 2)
                r["g_onestep_C"], r["t_onestep_C"] = g["f"], g["seconds"]
                g = heuristic(X, y, mu, "any_signed", "C", None, "amip", budget=n - 2)
                r["g_sorted_C"], r["t_amip_C"], r["kpred_amip_C"] = g["f"], g["seconds"], g["k_pred"]
                rec_exact.append(r)
            rs = [r for r in rec_exact if r["family"] == fam and r["n"] == n]
            print(f"exact fam {fam} n={n}: mean f_C {np.mean([r['f_C'] if r['f_C'] else KMAX+1 for r in rs]):.2f}, "
                  f"notfound {sum(r['f_C'] is None for r in rs)}, mean t {np.mean([r['t_C'] for r in rs]):.2f}s, elapsed {time.time()-t_start:.0f}s", flush=True)
        for n in NS_GREEDY:
            for rep in range(3 if FAST else 40):
                X, y, mu, bstar = make_family_instance(rng, n, fam)
                st = fit_state(X, y, mu)
                r = dict(family=fam, n=n, rep=rep, support_size=int(len(st.S)),
                         true_support=bool(np.array_equal(st.S, np.flatnonzero(bstar))),
                         kstar=int(certificate_k(st, n - 2)))
                t0 = time.perf_counter()
                g = heuristic(X, y, mu, "any_signed", "C", None, "onestep", budget=n - 2)
                r["g_onestep_C"], r["t_onestep_C"] = g["f"], time.perf_counter() - t0
                g = heuristic(X, y, mu, "any_signed", "C", None, "amip", budget=n - 2)
                r["g_sorted_C"], r["kpred_amip_C"] = g["f"], g["k_pred"]
                g = heuristic(X, y, mu, "any_signed", "P", None, "onestep", budget=n - 2)
                r["g_onestep_P"] = g["f"]
                rec_greedy.append(r)
            rs = [r for r in rec_greedy if r["family"] == fam and r["n"] == n]
            print(f"greedy fam {fam} n={n}: median g_onestep {np.median([r['g_onestep_C'] for r in rs])}, "
                  f"median k* {np.median([r['kstar'] for r in rs])}, elapsed {time.time()-t_start:.0f}s", flush=True)

    agg_exact, agg_greedy = [], []
    for fam in FAMILIES:
        for n in NS_EXACT:
            rs = [r for r in rec_exact if r["family"] == fam and r["n"] == n]
            a = dict(family=fam, n=n, instances=len(rs), mean_support=float(np.mean([r["support_size"] for r in rs])),
                     frac_true_support=float(np.mean([r["true_support"] for r in rs])))
            for rule in ["C", "P"]:
                fs = np.array([r[f"f_{rule}"] if r[f"f_{rule}"] is not None else np.nan for r in rs], float)
                a[f"f_{rule}_dist"] = {str(k): int(np.sum(fs == k)) for k in range(1, KMAX + 1)} | {"notfound": int(np.sum(np.isnan(fs)))}
                a[f"f_{rule}_median"] = float(np.nanmedian(fs)) if np.any(~np.isnan(fs)) else None
                a[f"f_{rule}_mean"] = float(np.nanmean(fs)) if np.any(~np.isnan(fs)) else None
                a[f"f_{rule}_frac1"] = float(np.mean(fs == 1))
                a[f"f_{rule}_mean_over_n"] = float(np.nanmean(fs) / n) if np.any(~np.isnan(fs)) else None
                a[f"t_{rule}_mean"] = float(np.mean([r[f"t_{rule}"] for r in rs]))
                a[f"oracle_{rule}_mean"] = float(np.mean([r[f"oracle_{rule}"] for r in rs]))
            fin = [r for r in rs if r["f_C"] is not None]
            a["greedy_onestep_exact_C"] = float(np.mean([r["g_onestep_C"] == r["f_C"] for r in fin])) if fin else None
            a["greedy_sorted_exact_C"] = float(np.mean([r["g_sorted_C"] == r["f_C"] for r in fin])) if fin else None
            a["greedy_onestep_gap_C"] = float(np.mean([r["g_onestep_C"] - r["f_C"] for r in fin])) if fin else None
            a["greedy_sorted_gap_C"] = float(np.mean([r["g_sorted_C"] - r["f_C"] for r in fin if r["g_sorted_C"] is not None])) if fin else None
            a["t_onestep_mean"] = float(np.mean([r["t_onestep_C"] for r in rs]))
            a["t_amip_mean"] = float(np.mean([r["t_amip_C"] for r in rs]))
            a["cost_ratio_onestep_median"] = float(np.median([r["t_onestep_C"] / r["t_C"] for r in rs if r["t_C"] > 0]))
            a["cost_ratio_amip_median"] = float(np.median([r["t_amip_C"] / r["t_C"] for r in rs if r["t_C"] > 0]))
            a["amip_kpred_exact"] = float(np.mean([r["kpred_amip_C"] == r["f_C"] for r in fin])) if fin else None
            nontriv = [r for r in fin if r["f_C"] >= 2]
            a["n_nontrivial"] = len(nontriv)
            a["greedy_onestep_exact_nontrivial_C"] = float(np.mean([r["g_onestep_C"] == r["f_C"] for r in nontriv])) if nontriv else None
            a["greedy_sorted_exact_nontrivial_C"] = float(np.mean([r["g_sorted_C"] == r["f_C"] for r in nontriv])) if nontriv else None
            a["kstar_mean"] = float(np.mean([r["kstar"] for r in rs]))
            a["frac_kstar_ge1_given_f_ge2"] = float(np.mean([r["kstar"] >= 1 for r in nontriv])) if nontriv else None
            agg_exact.append(a)
        for n in NS_GREEDY:
            rs = [r for r in rec_greedy if r["family"] == fam and r["n"] == n]
            g = np.array([r["g_onestep_C"] for r in rs], float)
            gs = np.array([r["g_sorted_C"] for r in rs], float)
            gp = np.array([r["g_onestep_P"] if r["g_onestep_P"] is not None else np.nan for r in rs], float)
            ks = np.array([r["kstar"] for r in rs], float)
            agg_greedy.append(dict(family=fam, n=n, instances=len(rs), mean_support=float(np.mean([r["support_size"] for r in rs])),
                                   frac_true_support=float(np.mean([r["true_support"] for r in rs])),
                                   g_onestep_C_median=float(np.median(g)), g_onestep_C_mean=float(np.mean(g)),
                                   g_onestep_C_q1=float(np.percentile(g, 25)), g_onestep_C_q3=float(np.percentile(g, 75)),
                                   g_onestep_C_mean_over_n=float(np.mean(g) / n), g_onestep_C_frac1=float(np.mean(g == 1)),
                                   g_sorted_C_median=float(np.median(gs)), frac_sorted_le_onestep=float(np.mean(gs <= g)),
                                   g_onestep_P_median=float(np.nanmedian(gp)), g_onestep_P_mean_over_n=float(np.nanmean(gp) / n),
                                   kstar_median=float(np.median(ks)), kstar_mean=float(np.mean(ks)),
                                   frac_kstar_ge1=float(np.mean(ks >= 1)), mean_bracket_ratio=float(np.mean((ks + 1) / g)),
                                   t_onestep_mean=float(np.mean([r["t_onestep_C"] for r in rs]))))
    out = dict(meta=dict(seed=SEED, python=platform.python_version(), numpy=np.__version__, scipy=scipy.__version__,
                         sklearn=sklearn.__version__, kmax=KMAX, ns_exact=NS_EXACT, ns_greedy=NS_GREEDY,
                         families=FAMILIES, seconds=time.time() - t_start),
               exact=agg_exact, greedy=agg_greedy, records_exact=rec_exact, records_greedy=rec_greedy)
    os.makedirs(os.path.join(ROOT, "results"), exist_ok=True)
    with open(os.path.join(ROOT, "results", "scaling.json"), "w") as fh:
        json.dump(out, fh, indent=1)
    L = ["# E4 — Scaling of the fragility number (any change of the signed support)", "",
         f"Seed {SEED}; exhaustive search with the closed-form removal test up to |R| <= {KMAX}.", "",
         "## Exact (n <= 30)", "",
         "| fam | n | inst | mean |S| | P(S=S*) | f_C dist (1..6, nf) | median C | mean C | mean/n C | P(f=1) C | median P | P(f=1) P | greedy onestep exact | amip exact | n f>=2 | onestep exact (f>=2) | amip exact (f>=2) | k* mean | P(k*>=1 given f>=2) | mean t_C (s) | mean oracle evals | cost ratio onestep | cost ratio amip | amip k_pred exact |",
         "|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|"]
    for a in agg_exact:
        d = a["f_C_dist"]
        dist = ",".join(str(d[str(k)]) for k in range(1, KMAX + 1)) + f",{d['notfound']}"
        L.append(f"| {a['family']} | {a['n']} | {a['instances']} | {a['mean_support']:.2f} | {a['frac_true_support']:.2f} | {dist} | {a['f_C_median']} | {a['f_C_mean']} | {a['f_C_mean_over_n']} | {a['f_C_frac1']:.2f} | {a['f_P_median']} | {a['f_P_frac1']:.2f} | {a['greedy_onestep_exact_C']} | {a['greedy_sorted_exact_C']} | {a['n_nontrivial']} | {a['greedy_onestep_exact_nontrivial_C']} | {a['greedy_sorted_exact_nontrivial_C']} | {a['kstar_mean']:.2f} | {a['frac_kstar_ge1_given_f_ge2']} | {a['t_C_mean']:.2f} | {a['oracle_C_mean']:.0f} | {a['cost_ratio_onestep_median']:.3f} | {a['cost_ratio_amip_median']:.3f} | {a['amip_kpred_exact']} |")
    L += ["", "## Greedy upper bounds and certificate lower bounds (n up to 400, rule C unless stated)", "",
          "| fam | n | inst | mean |S| | P(S=S*) | onestep median [q1,q3] | mean/n | P(g=1) | amip median | P(amip<=onestep) | onestep rule P median | mean/n (P) | k* median | P(k*>=1) | mean (k*+1)/g | mean time onestep (s) |",
          "|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|"]
    for a in agg_greedy:
        L.append(f"| {a['family']} | {a['n']} | {a['instances']} | {a['mean_support']:.2f} | {a['frac_true_support']:.2f} | {a['g_onestep_C_median']} [{a['g_onestep_C_q1']},{a['g_onestep_C_q3']}] | {a['g_onestep_C_mean_over_n']:.3f} | {a['g_onestep_C_frac1']:.2f} | {a['g_sorted_C_median']} | {a['frac_sorted_le_onestep']:.2f} | {a['g_onestep_P_median']} | {a['g_onestep_P_mean_over_n']:.3f} | {a['kstar_median']} | {a['frac_kstar_ge1']:.2f} | {a['mean_bracket_ratio']:.2f} | {a['t_onestep_mean']:.3f} |")
    L += ["", f"Total time {out['meta']['seconds']:.0f} s."]
    with open(os.path.join(ROOT, "results", "scaling.md"), "w") as fh:
        fh.write("\n".join(L) + "\n")
    print("done in", out["meta"]["seconds"], "s")


if __name__ == "__main__":
    main()
