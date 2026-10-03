#!/usr/bin/env python3
"""
TCD001 -- exhaustive exact check of the Subset Sum -> Selection-Witness reduction for p = 2
(theory/hardness_p2.tex, Theorem "selection witnesses are NP-complete for p = 2") and of the
pseudo-polynomial dynamic programme for fixed p (Proposition "pseudo-polynomial algorithm").

For every source instance (b_1..b_m, t) the script
  1. builds the Lasso instance of the reduction (rule C and rule P);
  2. solves the Lasso EXACTLY (Fractions) on D and on D \\ R for EVERY proper nonempty R
     (enumeration of signed supports + KKT in rational arithmetic; uniqueness certified by
     full rank of X_E on the equicorrelation set E, Tibshirani 2013; anything else is reported);
  3. checks, set by set, the characterisation of the proof:
       variable 2 enters on D \\ R  <=>  gadget kept, >= 1 item kept, sum of kept b_i = t;
  4. checks  (witness for enter(2) exists)  <=>  (Subset Sum answer is YES, by brute force);
  5. cross-checks with experiments/lasso_fragility.py: the closed-form test of Prop. 3.1
     (removal_test, floating point) and the KKT-guarded homotopy solver (lasso_lars);
  6. recomputes f_enter(2) with the dynamic programme over (|K|, X_K^T X_K, X_K^T y_K) and compares.
Finally it runs the dynamic programme against exhaustive search on random small integer
instances (p = 2, 3; targets enter / leave / any) as a sanity check of the implementation.

Deterministic (seed 20261003).  Output: theory/check_hardness_output.txt (also printed).
"""
from __future__ import annotations

import itertools
import os
import random
import sys
import time
from fractions import Fraction as F

import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, "..", "experiments"))
import lasso_fragility as lf  # noqa: E402

OUT_LINES: list[str] = []


def log(msg: str = "") -> None:
    print(msg, flush=True)
    OUT_LINES.append(msg)


# ----------------------------------------------------------------------------------------------
# Exact small-p Lasso from sufficient statistics (G = X^T X, g = X^T y)
# ----------------------------------------------------------------------------------------------
def solve_exact(M, rhs):
    """Gaussian elimination over Fractions; None if singular."""
    k = len(rhs)
    A = [list(M[i]) + [rhs[i]] for i in range(k)]
    for col in range(k):
        piv = next((r for r in range(col, k) if A[r][col] != 0), None)
        if piv is None:
            return None
        A[col], A[piv] = A[piv], A[col]
        for r in range(k):
            if r != col and A[r][col] != 0:
                f = A[r][col] / A[col][col]
                A[r] = [a - f * b for a, b in zip(A[r], A[col])]
    return [A[i][k] / A[i][i] for i in range(k)]


def is_singular(M):
    k = len(M)
    if k == 0:
        return False
    return solve_exact(M, [F(0)] * k) is None


def exact_lasso_stats(G, g, mu):
    """Exact Lasso minimiser of 1/2 b^T G b - g^T b + mu ||b||_1 (G = X^T X).

    Returns (beta, status, tie) with status in {"unique", "undetermined"}:
      "unique"        a minimiser was found and X_E has full column rank on the equicorrelation
                      set E (G_EE nonsingular) => it is THE unique minimiser (Tibshirani 2013);
      "undetermined"  a minimiser was found but G_EE is singular (uniqueness not certified).
    tie = True iff some j outside the support has |c_j| = mu exactly (KKT boundary case).
    """
    p = len(g)
    for size in range(p + 1):
        for S in itertools.combinations(range(p), size):
            for s in itertools.product((1, -1), repeat=size):
                if size:
                    GSS = [[G[a][b] for b in S] for a in S]
                    bS = solve_exact(GSS, [g[a] - mu * sa for a, sa in zip(S, s)])
                    if bS is None:
                        continue
                    if any(sa * ba <= 0 for sa, ba in zip(s, bS)):
                        continue
                else:
                    bS = []
                beta = [F(0)] * p
                for a, ba in zip(S, bS):
                    beta[a] = ba
                c = [g[j] - sum(G[j][l] * beta[l] for l in range(p)) for j in range(p)]
                if any(abs(c[j]) > mu for j in range(p) if j not in S):
                    continue
                E = [j for j in range(p) if abs(c[j]) == mu]
                tie = any(abs(c[j]) == mu for j in range(p) if j not in S)
                GEE = [[G[a][b] for b in E] for a in E]
                status = "undetermined" if is_singular(GEE) else "unique"
                return beta, status, tie
    raise RuntimeError("no minimiser found (impossible)")


def reduced_mu_exact(mu, n, k, rule):
    return mu if rule == "C" else mu * F(n - k, n)


# ----------------------------------------------------------------------------------------------
# The reduction
# ----------------------------------------------------------------------------------------------
def build_instance(b, t, rule, override=None):
    """Instance of the reduction (rows: m items then the gadget; target variable index 1).
    `override` (ablations only) replaces u, eta or rho by values that violate the proof's conditions."""
    override = override or {}
    m, B = len(b), sum(b)
    assert 1 <= t <= B - 1
    s0 = F(1, 2)
    eta = F(override.get("eta", F(1, 2 * B)))
    kappa = 1 + eta
    u = override.get("u", m + 1)
    if rule == "C":
        mu = t + s0
        yit = [F(bi) for bi in b]
    else:
        lam = t + s0
        mu = lam * (m + 1)
        yit = [bi + lam for bi in b]
    eps = eta / (4 * mu)
    rho = F(override.get("rho", 1 - eps))
    X = [[F(1), rho] for _ in range(m)] + [[F(u), kappa * u]]
    y = yit + [s0 / u]
    return X, y, mu, dict(s0=s0, eta=eta, kappa=kappa, u=u, eps=eps, rho=rho)


def subset_sum_yes(b, t):
    sums = {0}
    for bi in b:
        sums |= {x + bi for x in sums}
    return t in sums


def stats_all_masks(X, y):
    """G_K, g_K for every kept set K given as a bitmask (Fractions)."""
    n, p = len(X), len(X[0])
    contrib = []
    for i in range(n):
        Gi = [[X[i][a] * X[i][b] for b in range(p)] for a in range(p)]
        gi = [X[i][a] * y[i] for a in range(p)]
        contrib.append((Gi, gi))
    stats = [None] * (1 << n)
    stats[0] = ([[F(0)] * p for _ in range(p)], [F(0)] * p)
    for mask in range(1, 1 << n):
        low = (mask & -mask).bit_length() - 1
        G0, g0 = stats[mask & (mask - 1)]
        Gi, gi = contrib[low]
        stats[mask] = ([[G0[a][c] + Gi[a][c] for c in range(p)] for a in range(p)],
                       [g0[a] + gi[a] for a in range(p)])
    return stats


def check_reduction_instance(b, t, rule, lib_check=True, override=None, dp=True):
    X, y, mu, par = build_instance(b, t, rule, override)
    n, m = len(X), len(b)
    full = (1 << n) - 1
    stats = stats_all_masks(X, y)
    res = dict(n=n, subsets=0, undetermined=0, ties=0, char_fail=0, entries=0,
               lib_test_disagree=0, lib_fit_disagree=0, lib_fit_checked=0)
    # full data
    Gf, gf = stats[full]
    beta, st, tie = exact_lasso_stats(Gf, gf, mu)
    ok_D = (st == "unique" and beta[0] > 0 and beta[1] == 0 and not tie)
    min_R = None
    exact_pattern = {}
    for keep in range(1, full):           # K nonempty, R = complement nonempty
        res["subsets"] += 1
        k = n - bin(keep).count("1")
        mu_k = reduced_mu_exact(mu, n, k, rule)
        G, g = stats[keep]
        beta, st, tie = exact_lasso_stats(G, g, mu_k)
        res["undetermined"] += st != "unique"
        res["ties"] += tie
        enters = (st == "unique" and beta[1] != 0)
        gadget = bool(keep >> m & 1)
        items = [i for i in range(m) if keep >> i & 1]
        predicted = gadget and len(items) >= 1 and sum(b[i] for i in items) == t
        res["char_fail"] += enters != predicted
        if enters:
            res["entries"] += 1
            if min_R is None or k < min_R:
                min_R = k
        exact_pattern[keep] = (st == "unique" and beta[0] > 0 and beta[1] == 0)
    yes = subset_sum_yes(b, t)
    witness = min_R is not None
    # library cross-check (floating point): Prop. 3.1 closed-form test + KKT-guarded solver
    if lib_check:
        Xf = np.array([[float(v) for v in row] for row in X])
        yf = np.array([float(v) for v in y])
        muf = float(mu)
        st0 = lf.fit_state(Xf, yf, muf)
        if not (list(st0.S) == [0] and list(st0.s) == [1]):
            res["lib_test_disagree"] += 1
        for k in range(1, n):
            Rb = np.array(list(itertools.combinations(range(n), k)), dtype=int)
            out = lf.removal_test(st0, Rb, rule=rule)
            for R, pres in zip(Rb, out["preserved"]):
                keep = full ^ sum(1 << int(i) for i in R)
                res["lib_test_disagree"] += bool(pres) != exact_pattern[keep]
        # homotopy solver with KKT guard on every subsample (n <= 9) or on 200 random ones
        keeps = list(range(1, full))
        if n > 9:
            keeps = random.Random(n * 1000 + t).sample(keeps, 200)
        for keep in keeps:
            idx = [i for i in range(n) if keep >> i & 1]
            k = n - len(idx)
            mu_k = reduced_mu_exact(mu, n, k, rule)
            bf = lf.lasso_lars(Xf[idx], yf[idx], float(mu_k))
            G, g = stats[keep]
            be, st, _ = exact_lasso_stats(G, g, mu_k)
            supp_f = tuple(np.flatnonzero(np.abs(bf) > lf.ZERO_TOL))
            supp_e = tuple(j for j in range(2) if be[j] != 0)
            res["lib_fit_checked"] += 1
            res["lib_fit_disagree"] += supp_f != supp_e
    # dynamic programme over sufficient statistics (Proposition "pseudo-polynomial")
    f_dp, nstates = (dp_fragility(X, y, mu, rule, target="enter", j=1, S0=(0,), s0=(1,))
                     if dp else (None, 0))
    f_ex = min_R if min_R is not None else None
    res.update(ok_D=ok_D, yes=yes, witness=witness, f_enter=f_ex, f_dp=f_dp, dp_states=nstates,
               params=par, mu=mu)
    return res


# ----------------------------------------------------------------------------------------------
# Pseudo-polynomial dynamic programme for fixed p (states = (|K|, G_K, g_K))
# ----------------------------------------------------------------------------------------------
def freeze(G, g):
    p = len(g)
    return tuple(G[a][c] for a in range(p) for c in range(a, p)) + tuple(g)


def dp_fragility(X, y, mu, rule, target, j=None, S0=None, s0=None):
    """f_target(D) via the DP over reachable (|K|, upper(G_K), g_K); returns (f or None, #states)."""
    n, p = len(X), len(X[0])
    states = {(0,) + tuple([F(0)] * (p * (p + 1) // 2 + p))}
    for i in range(n):
        xi, yi = X[i], y[i]
        add = tuple(xi[a] * xi[c] for a in range(p) for c in range(a, p)) + tuple(xi[a] * yi for a in range(p))
        new = set(states)
        for s in states:
            new.add((s[0] + 1,) + tuple(u + v for u, v in zip(s[1:], add)))
        states = new
    best_keep = None
    for s in states:
        kept = s[0]
        if kept == 0 or kept == n:
            continue
        up = s[1:1 + p * (p + 1) // 2]
        g = list(s[1 + p * (p + 1) // 2:])
        G = [[F(0)] * p for _ in range(p)]
        it = iter(up)
        for a in range(p):
            for c in range(a, p):
                G[a][c] = G[c][a] = next(it)
        mu_k = reduced_mu_exact(mu, n, n - kept, rule)
        beta, st, _ = exact_lasso_stats(G, g, mu_k)
        if st != "unique":
            continue
        if holds(target, beta, j, S0, s0):
            best_keep = kept if best_keep is None else max(best_keep, kept)
    return (None if best_keep is None else n - best_keep), len(states)


def holds(target, beta, j, S0, s0):
    S = tuple(i for i, v in enumerate(beta) if v != 0)
    s = tuple(1 if beta[i] > 0 else -1 for i in S)
    if target == "enter":
        return beta[j] != 0
    if target == "leave":
        return beta[j] == 0
    if target == "any":                       # signed
        return (S, s) != (tuple(S0), tuple(s0))
    raise ValueError(target)


def exhaustive_fragility(X, y, mu, rule, target, j, S0, s0):
    n = len(X)
    stats = stats_all_masks(X, y)
    full = (1 << n) - 1
    best = None
    for keep in range(1, full):
        k = n - bin(keep).count("1")
        G, g = stats[keep]
        beta, st, _ = exact_lasso_stats(G, g, reduced_mu_exact(mu, n, k, rule))
        if st == "unique" and holds(target, beta, j, S0, s0):
            best = k if best is None else min(best, k)
    return best


# ----------------------------------------------------------------------------------------------
def main():
    t0 = time.time()
    rng = random.Random(20261003)
    log("TCD001 -- check_hardness.py (seed 20261003)")
    log("Reduction: Subset Sum (b, t), 1 <= t <= sum(b)-1  ->  p = 2 Lasso, target enter(variable 2)")
    log("items (1, rho; y_i), gadget (u, kappa*u; 1/(2u)); rule C: y_i = b_i, mu = t+1/2;")
    log("rule P: y_i = b_i + lam, lam = t+1/2, mu = lam*(m+1); kappa = 1+1/(2B), u = m+1, rho = 1-eta/(4mu)")
    log("")
    # source instances: hand-made + exhaustive targets for two small b + random
    insts = []
    for b in ([3, 5, 7], [2, 3, 7], [4, 6, 9, 13]):
        for t in range(1, sum(b)):
            insts.append((list(b), t))
    insts.append(([1], None))  # placeholder removed below (m = 1 has no valid t)
    insts = [x for x in insts if x[1] is not None]
    while len(insts) < 140:
        m = rng.randint(2, 9)
        b = [rng.randint(1, 30) for _ in range(m)]
        t = rng.randint(1, sum(b) - 1)
        insts.append((b, t))
    while len(insts) < 156:                   # larger instances, n = 11, 12
        m = rng.randint(10, 11)
        b = [rng.randint(1, 30) for _ in range(m)]
        t = rng.randint(1, sum(b) - 1)
        insts.append((b, t))
    tot = dict(inst=0, yes=0, no=0, equiv_ok=0, char_fail=0, subsets=0, undetermined=0, ties=0,
               okD=0, lib_test_disagree=0, lib_fit_disagree=0, lib_fit_checked=0, dp_agree=0,
               maxn=0)
    for rule in ("C", "P"):
        log(f"=== rule {rule} ===")
        per = dict(inst=0, yes=0, equiv=0, char_fail=0, subsets=0, undet=0, ties=0, okD=0,
                   ltd=0, lfd=0, lfc=0, dp=0)
        for idx, (b, t) in enumerate(insts):
            r = check_reduction_instance(b, t, rule, lib_check=True)
            equiv = (r["witness"] == r["yes"])
            per["inst"] += 1
            per["yes"] += r["yes"]
            per["equiv"] += equiv
            per["char_fail"] += r["char_fail"]
            per["subsets"] += r["subsets"]
            per["undet"] += r["undetermined"]
            per["ties"] += r["ties"]
            per["okD"] += r["ok_D"]
            per["ltd"] += r["lib_test_disagree"]
            per["lfd"] += r["lib_fit_disagree"]
            per["lfc"] += r["lib_fit_checked"]
            per["dp"] += (r["f_dp"] == r["f_enter"])
            tot["maxn"] = max(tot["maxn"], r["n"])
            if idx < 12 or not equiv or r["char_fail"]:
                log(f"  b={b} t={t}: SS={'YES' if r['yes'] else 'NO '} witness={'yes' if r['witness'] else 'no '}"
                    f" f_enter={r['f_enter']} (DP {r['f_dp']}, {r['dp_states']} states)"
                    f" | subsets={r['subsets']} entries={r['entries']} char_fail={r['char_fail']}"
                    f" undet={r['undetermined']} ties={r['ties']} D_ok={r['ok_D']}"
                    f" | lib: test_disagree={r['lib_test_disagree']} fit_disagree={r['lib_fit_disagree']}/{r['lib_fit_checked']}")
        log(f"  rule {rule}: {per['inst']} instances ({per['yes']} YES, {per['inst'] - per['yes']} NO);"
            f" equivalence witness<=>YES holds in {per['equiv']}/{per['inst']};"
            f" set-by-set characterisation failures {per['char_fail']} over {per['subsets']} subsets;")
        log(f"           uniqueness not certified on {per['undet']} subsets; KKT ties on {per['ties']} subsets;"
            f" full data S={{1}}, variable 2 inactive, unique, no tie: {per['okD']}/{per['inst']};")
        log(f"           Prop. 3.1 closed-form test vs exact: {per['ltd']} disagreements;"
            f" lasso_lars support vs exact: {per['lfd']} disagreements in {per['lfc']} fits;"
            f" DP f_enter = exhaustive f_enter in {per['dp']}/{per['inst']}")
        log("")
        for kk in ("inst", "char_fail", "subsets"):
            tot[kk] += per[kk]
        tot["yes"] += per["yes"]
        tot["equiv_ok"] += per["equiv"]
        tot["undetermined"] += per["undet"]
        tot["ties"] += per["ties"]
        tot["okD"] += per["okD"]
        tot["lib_test_disagree"] += per["ltd"]
        tot["lib_fit_disagree"] += per["lfd"]
        tot["lib_fit_checked"] += per["lfc"]
        tot["dp_agree"] += per["dp"]
    log(f"TOTAL reduction: {tot['inst']} (instance, rule) pairs, n <= {tot['maxn']}, {tot['subsets']} subsets solved exactly;"
        f" equivalence {tot['equiv_ok']}/{tot['inst']}; characterisation failures {tot['char_fail']};"
        f" undetermined {tot['undetermined']}; ties {tot['ties']}; D ok {tot['okD']}/{tot['inst']};"
        f" closed-form test disagreements {tot['lib_test_disagree']}; solver disagreements"
        f" {tot['lib_fit_disagree']}/{tot['lib_fit_checked']}; DP agreement {tot['dp_agree']}/{tot['inst']}")
    log("")
    # ablations: the checks must detect a violation of each condition used in the proof
    log("=== ablations (negative controls; each violates one condition of the proof) ===")
    abl = [("u = 1 (violates u^2 > N)", {"u": 1}),
           ("rho = 1 (items with x2 = x1; uniqueness on item-only subsamples lost)", {"rho": F(1)}),
           ("eta = 1, kappa = 2 (violates kappa - rho <= 1/B)", {"eta": F(1)})]
    abl_insts = [([3, 5, 7], 8), ([2, 3, 7], 5), ([1, 1, 20], 2), ([2, 2, 2, 30], 4), ([1, 2, 40], 3),
                 ([4, 6, 9, 13], 10), ([5, 5, 50], 5)]
    for name, ov in abl:
        for rule in ("C", "P"):
            nfail = nund = neq = 0
            for b, t in abl_insts:
                r = check_reduction_instance(b, t, rule, lib_check=False, override=ov, dp=False)
                nfail += r["char_fail"]
                nund += r["undetermined"]
                neq += r["witness"] != r["yes"]
            log(f"  {name}, rule {rule}: characterisation failures {nfail}, uncertified uniqueness {nund},"
                f" equivalence failures {neq} (over {len(abl_insts)} instances)")
    log("")
    # DP versus exhaustive on random small integer data (implementation sanity check, p = 2, 3)
    log("=== DP over (|K|, X_K^T X_K, X_K^T y_K) vs exhaustive search, random integer data ===")
    agree = total = 0
    states_sum = subs_sum = 0
    for trial in range(60):
        p = 2 if trial < 36 else 3
        n = rng.randint(5, 9)
        Mx = 1 if trial % 2 == 0 else 2
        X = [[F(rng.randint(-Mx, Mx)) for _ in range(p)] for _ in range(n)]
        y = [F(rng.randint(-3, 3)) for _ in range(n)]
        mu = F(rng.randint(1, 8), 2)
        rule = "C" if trial % 3 else "P"
        G = [[sum(X[i][a] * X[i][c] for i in range(n)) for c in range(p)] for a in range(p)]
        g = [sum(X[i][a] * y[i] for i in range(n)) for a in range(p)]
        beta, st, _ = exact_lasso_stats(G, g, mu)
        if st != "unique":
            continue
        S0 = tuple(i for i in range(p) if beta[i] != 0)
        s0 = tuple(1 if beta[i] > 0 else -1 for i in S0)
        tgts = [("any", None)]
        if S0:
            tgts.append(("leave", S0[0]))
        inact = [i for i in range(p) if beta[i] == 0]
        if inact:
            tgts.append(("enter", inact[0]))
        for tg, jj in tgts:
            fd, ns = dp_fragility(X, y, mu, rule, tg, jj, S0, s0)
            fe = exhaustive_fragility(X, y, mu, rule, tg, jj, S0, s0)
            total += 1
            agree += fd == fe
            states_sum += ns
            subs_sum += 2 ** n
    log(f"  {agree}/{total} (instance, target) pairs agree; mean reachable states {states_sum / max(total, 1):.1f}"
        f" vs mean 2^n = {subs_sum / max(total, 1):.1f}")
    log("")
    log(f"elapsed {time.time() - t0:.1f} s")
    with open(os.path.join(HERE, "check_hardness_output.txt"), "w") as fh:
        fh.write("\n".join(OUT_LINES) + "\n")


if __name__ == "__main__":
    main()
