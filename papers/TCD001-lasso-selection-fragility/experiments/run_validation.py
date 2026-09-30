#!/usr/bin/env python3
"""
E1: numerical validation of the exact removal test (Proposition 1), of the single-removal
sufficient condition (Corollary 2) and of the k-removal certificate (Proposition 3), against
refits with the exact homotopy solver (and a coordinate-descent cross-check).

Writes results/validation.json and results/validation.md.
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
from lasso_fragility import (certificate_k, fit_state, fragility_exact, lasso_cd, lasso_lars,
                             make_instance, reduced_mu, refit_pattern, removal_test,
                             signed_pattern, single_removal_indices, support)

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
SEED = 20260930
FAST = "--fast" in sys.argv


def same_pattern(S1, s1, S2, s2):
    return len(S1) == len(S2) and np.array_equal(S1, S2) and np.array_equal(s1, s2)


def main():
    t_start = time.time()
    rng = np.random.default_rng(SEED)
    cells = [(10, 5), (20, 10), (50, 20), (12, 24)]
    reps = 4 if FAST else 15
    out = {"meta": {"seed": SEED, "python": platform.python_version(), "numpy": np.__version__,
                    "scipy": scipy.__version__, "sklearn": sklearn.__version__,
                    "design": "b=2, rho=0.3, s0=2, sigma=1, c=1.0", "reps_per_cell": reps}}

    # ---------------- A: single removals, oracle vs refit ----------------
    A = []
    cd_checks = {"n": 0, "support_disagreements": 0, "max_coef_diff": 0.0}
    for (n, p) in cells:
        for rule in ["C", "P"]:
            agree = total = 0
            n_pres = 0
            maxdiff = 0.0
            min_margin_disagree = []
            for _ in range(reps):
                X, y, mu, _ = make_instance(rng, n, p, 2, 2.0, 0.3, 1.0, 1.0)
                st = fit_state(X, y, mu)
                res = removal_test(st, np.arange(n)[:, None], rule)
                for i in range(n):
                    S_new, s_new = refit_pattern(X, y, mu, (i,), rule, n)
                    same = same_pattern(st.S, st.s, S_new, s_new)
                    total += 1
                    agree += int(same == bool(res["preserved"][i]))
                    if same:
                        n_pres += 1
                        keep = np.ones(n, bool)
                        keep[i] = False
                        b_ref = lasso_lars(X[keep], y[keep], reduced_mu(mu, n, 1, rule))
                        maxdiff = max(maxdiff, float(np.max(np.abs(b_ref[st.S] - res["beta_new"][i]))) if len(st.S) else 0.0)
                        if rule == "C" and n == 10:
                            b_cd = lasso_cd(X[keep], y[keep], reduced_mu(mu, n, 1, rule), 1e-13)
                            cd_checks["n"] += 1
                            cd_checks["support_disagreements"] += int(not np.array_equal(support(b_ref), np.flatnonzero(np.abs(b_cd) > 1e-7)))
                            cd_checks["max_coef_diff"] = max(cd_checks["max_coef_diff"], float(np.max(np.abs(b_ref - b_cd))))
            A.append(dict(n=n, p=p, rule=rule, tests=total, agreements=agree, preserved=n_pres,
                          max_coef_diff=maxdiff))
            print(f"A n={n} p={p} rule={rule}: {agree}/{total} agree, preserved {n_pres}, maxdiff {maxdiff:.1e}")
    out["A_single"] = A
    out["A_cd_crosscheck"] = cd_checks

    # ---------------- B: multiple removals, oracle vs refit ----------------
    B = []
    for (n, p) in cells:
        for rule in ["C", "P"]:
            for k in [2, 3, 5]:
                agree = total = n_pres = 0
                maxdiff = 0.0
                for _ in range(reps):
                    X, y, mu, _ = make_instance(rng, n, p, 2, 2.0, 0.3, 1.0, 1.0)
                    st = fit_state(X, y, mu)
                    nsets = 10 if FAST else 20
                    Rb = np.array([np.sort(rng.choice(n, k, replace=False)) for _ in range(nsets)])
                    res = removal_test(st, Rb, rule)
                    for t, R in enumerate(Rb):
                        S_new, s_new = refit_pattern(X, y, mu, tuple(R), rule, n)
                        same = same_pattern(st.S, st.s, S_new, s_new)
                        total += 1
                        agree += int(same == bool(res["preserved"][t]))
                        if same and len(st.S):
                            n_pres += 1
                            keep = np.ones(n, bool)
                            keep[R] = False
                            b_ref = lasso_lars(X[keep], y[keep], reduced_mu(mu, n, k, rule))
                            maxdiff = max(maxdiff, float(np.max(np.abs(b_ref[st.S] - res["beta_new"][t]))))
                B.append(dict(n=n, p=p, rule=rule, k=k, tests=total, agreements=agree, preserved=n_pres,
                              max_coef_diff=maxdiff))
                print(f"B n={n} p={p} rule={rule} k={k}: {agree}/{total} agree, preserved {n_pres}, maxdiff {maxdiff:.1e}")
    out["B_multi"] = B

    # ---------------- C: sufficient conditions (Cor. 2) and certificate (Prop. 3), rule C ------
    C = []
    for (n, p) in cells:
        stable = certified = 0
        inst = 0
        f_list, kstar_list = [], []
        for _ in range(reps * 2):
            X, y, mu, _ = make_instance(rng, n, p, 2, 2.0, 0.3, 1.0, 1.0)
            st = fit_state(X, y, mu)
            res = removal_test(st, np.arange(n)[:, None], "C")
            ind = single_removal_indices(st)
            stable += int(res["preserved"].sum())
            certified += int(np.sum(res["preserved"] & (ind["iota"] < 1)))
            # sanity: the sufficient condition never certifies an unstable removal
            assert not np.any((~res["preserved"]) & (ind["iota"] < 1)), "Cor. 2 violated"
            kmax = min(n - 2, 6)
            fe = fragility_exact(st, "any_signed", "C", kmax=kmax)
            ks = certificate_k(st, kmax)
            f = fe["f"] if fe["f"] is not None else kmax + 1
            assert ks < f, "Prop. 3 violated"
            f_list.append(f)
            kstar_list.append(ks)
            inst += 1
        f_arr, k_arr = np.array(f_list), np.array(kstar_list)
        C.append(dict(n=n, p=p, instances=inst, stable_single_removals=stable, certified_by_cor2=certified,
                      cor2_coverage=(certified / stable if stable else None),
                      frac_f1=float(np.mean(f_arr == 1)), frac_f_ge2=float(np.mean(f_arr >= 2)),
                      frac_kstar_ge1_given_f_ge2=(float(np.mean(k_arr[f_arr >= 2] >= 1)) if np.any(f_arr >= 2) else None),
                      mean_gap_given_f_ge2=(float(np.mean((f_arr - 1 - k_arr)[f_arr >= 2])) if np.any(f_arr >= 2) else None),
                      kmax=kmax))
        print(f"C n={n} p={p}: cor2 coverage {certified}/{stable}, P(f=1)={np.mean(f_arr==1):.2f}, "
              f"P(k*>=1|f>=2)={C[-1]['frac_kstar_ge1_given_f_ge2']}, gap={C[-1]['mean_gap_given_f_ge2']}")
    out["C_certificates"] = C

    # ---------------- D: throughput of the oracle vs refits ----------------
    n, p = 14, 6
    X, y, mu, _ = make_instance(rng, n, p, 2, 4.0, 0.0, 1.0, 1.5)
    st = fit_state(X, y, mu)
    import itertools
    Rb = np.array(list(itertools.combinations(range(n), 4)))
    t0 = time.perf_counter()
    for _ in range(5):
        removal_test(st, Rb, "C")
    t_oracle = (time.perf_counter() - t0) / (5 * len(Rb))
    t0 = time.perf_counter()
    m = 200 if not FAST else 50
    for R in Rb[:m]:
        refit_pattern(X, y, mu, tuple(R), "C", n)
    t_refit = (time.perf_counter() - t0) / m
    out["D_throughput"] = dict(n=n, p=p, k=4, subsets=int(len(Rb)), oracle_seconds_per_subset=t_oracle,
                               refit_seconds_per_subset=t_refit, speedup=t_refit / t_oracle)
    print(f"D throughput: oracle {t_oracle*1e6:.1f} us/subset, refit {t_refit*1e6:.1f} us/subset, x{t_refit/t_oracle:.0f}")

    out["meta"]["seconds"] = time.time() - t_start
    os.makedirs(os.path.join(ROOT, "results"), exist_ok=True)
    with open(os.path.join(ROOT, "results", "validation.json"), "w") as fh:
        json.dump(out, fh, indent=1)
    # markdown
    L = ["# E1 — Validation of the exact removal test and certificates", "",
         f"Seed {SEED}; {reps} instances per cell; design {out['meta']['design']}.", "",
         "## A. Single removals: oracle vs refit", "", "| n | p | rule | tests | agreements | preserved | max coef diff |", "|---|---|---|---|---|---|---|"]
    for r in A:
        L.append(f"| {r['n']} | {r['p']} | {r['rule']} | {r['tests']} | {r['agreements']} | {r['preserved']} | {r['max_coef_diff']:.1e} |")
    L += ["", f"CD cross-check on {cd_checks['n']} refits: {cd_checks['support_disagreements']} support disagreements, max coef diff {cd_checks['max_coef_diff']:.1e}.", "",
          "## B. Multiple removals: oracle vs refit", "", "| n | p | rule | k | tests | agreements | preserved | max coef diff |", "|---|---|---|---|---|---|---|---|"]
    for r in B:
        L.append(f"| {r['n']} | {r['p']} | {r['rule']} | {r['k']} | {r['tests']} | {r['agreements']} | {r['preserved']} | {r['max_coef_diff']:.1e} |")
    L += ["", "## C. Sufficient condition (Cor. 2) and certificate (Prop. 3), constant rule", "",
          "| n | p | instances | stable single removals | certified by Cor. 2 | P(f=1) | P(k*>=1 given f>=2) | mean gap f-1-k* given f>=2 |", "|---|---|---|---|---|---|---|---|"]
    for r in C:
        L.append(f"| {r['n']} | {r['p']} | {r['instances']} | {r['stable_single_removals']} | {r['certified_by_cor2']} | {r['frac_f1']:.2f} | {r['frac_kstar_ge1_given_f_ge2']} | {r['mean_gap_given_f_ge2']} |")
    d = out["D_throughput"]
    L += ["", "## D. Throughput", "", f"n={d['n']}, p={d['p']}, all {d['subsets']} subsets of size {d['k']}: oracle {d['oracle_seconds_per_subset']*1e6:.1f} us/subset, refit {d['refit_seconds_per_subset']*1e6:.1f} us/subset (x{d['speedup']:.0f}).", "",
          f"Total time {out['meta']['seconds']:.0f} s."]
    with open(os.path.join(ROOT, "results", "validation.md"), "w") as fh:
        fh.write("\n".join(L) + "\n")
    print("done in", out["meta"]["seconds"], "s")


if __name__ == "__main__":
    main()
