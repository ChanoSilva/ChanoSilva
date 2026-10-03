#!/usr/bin/env python3
"""TCD001 -- exact checks for the signed ANY target with p >= 2 (Proposition 5.12 of main.tex v0.6/v0.7, and the
identities recorded in results/signed_any_notes.md).

Copy of the derivation-time original theory/check_signed_any.py (identical computations, same seed); only the
output paths differ, and the run is frozen like check_strong.py: it writes results/check_signed_any_output.txt
(no timing lines), its SHA-256 to results/check_signed_any_output.sha256 (checked by make_numbers.py) and
results/signed_any.json (the counts of theory/signed_any_results.json plus a "meta" block with the CPU time).
Everything is in rational arithmetic (fractions.Fraction); seed fixed.

v0.7 (round 5, m1): part (A) also evaluates the polynomial certificate of Proposition 5.12 -- the removal sets
R*_j of size f0 produced by the per-column sort; if the minimiser on D minus some R*_j is certified unique, then
f^signed = f0. The new counters use no random numbers and are logged after the unchanged lines of part (A), so
every earlier count and line is reproduced verbatim; only the frozen log (hence its SHA-256: v0.6
c3e7244d5c447f90..., see results/check_signed_any_output.sha256 for v0.7) and the JSON keys "cert_*" are new.

Parts
  (A) Proposition prop:signed-empty: if S(D) = {} then a signed-ANY witness is exactly a subsample with
      ||X_K^T y_K||_inf > mu' and a unique minimiser; f^signed >= f0 := min_j f0_j (per-column sorting,
      Theorem thm:hard(b)), with equality whenever the minimiser on every subsample is certified unique.
      Checked against exhaustive search over all nonempty proper R, both rules, p in {2,3}.
  (B) Lemma lem:cb (Cauchy--Binet form, p = 2, S = {1}): G11 (c2 - mu') = sum_{i<l} m_il m'_il
      - mu' sum_i x_i1 (x_i1 - x_i2), checked on random subsamples.
  (C) Remark rem:gadgets, X3C-type gadget: with all anchors kept, the fixed-support candidate on S = U has
      triple residuals r = gamma (I + M_K / L)^{-1} 1 and c0 = 3 q phi mu + gamma L (theta - 3 phi) f(K),
      f(K) = 1^T (L I + M_K)^{-1} 1 (an identity), and f is monotone along the relevant comparisons, so
      exact covers are neither the maximisers nor the minimisers of f among kept families with N >= q.
"""
from __future__ import annotations

import itertools
import json
import os
import random
from fractions import Fraction as F

HERE = os.path.dirname(os.path.abspath(__file__))
RES = os.path.join(os.path.dirname(HERE), "results")
OUT = os.path.join(RES, "check_signed_any_output.txt")
JSON = os.path.join(RES, "signed_any.json")
SEED = 20261003
LINES: list[str] = []


def log(msg: str = "") -> None:
    print(msg)
    LINES.append(msg)


# ----------------------------------------------------------------------------- exact linear algebra
def solve(M, b):
    """Solve M x = b exactly (Gauss--Jordan); return None if singular."""
    n = len(M)
    A = [list(M[i]) + [b[i]] for i in range(n)]
    for c in range(n):
        piv = next((r for r in range(c, n) if A[r][c] != 0), None)
        if piv is None:
            return None
        A[c], A[piv] = A[piv], A[c]
        pv = A[c][c]
        A[c] = [v / pv for v in A[c]]
        for r in range(n):
            if r != c and A[r][c] != 0:
                fac = A[r][c]
                A[r] = [A[r][k] - fac * A[c][k] for k in range(n + 1)]
    return [A[i][n] for i in range(n)]


def gram(X, y, K):
    p = len(X[0])
    G = [[sum((X[i][a] * X[i][b] for i in K), F(0)) for b in range(p)] for a in range(p)]
    q = [sum((X[i][a] * y[i] for i in K), F(0)) for a in range(p)]
    return G, q


def lasso_status(G, q, mu):
    """Return ('zero', None) if beta = 0 is the (unique) minimiser; ('unique', (S, s, beta)) if a signed
    support with full-rank Gram and strict inactive inequalities solves KKT (unique minimiser,
    Tibshirani 2013); ('undetermined', None) otherwise (ties)."""
    p = len(q)
    if max(abs(v) for v in q) <= mu:
        return "zero", None
    for size in range(1, p + 1):
        for S in itertools.combinations(range(p), size):
            GSS = [[G[a][b] for b in S] for a in S]
            for s in itertools.product((1, -1), repeat=size):
                beta = solve(GSS, [q[a] - mu * sg for a, sg in zip(S, s)])
                if beta is None:
                    continue
                if any(sg * bv <= 0 for sg, bv in zip(s, beta)):
                    continue
                strict = True
                for j in range(p):
                    if j in S:
                        continue
                    c = q[j] - sum(G[j][a] * bv for a, bv in zip(S, beta))
                    if abs(c) > mu:
                        strict = None
                        break
                    if abs(c) == mu:
                        strict = False
                if strict is True:
                    return "unique", (S, s, beta)
    return "undetermined", None


def mu_rule(mu, n, k, rule):
    return mu if rule == "C" else mu * F(n - k, n)


# ----------------------------------------------------------------------------- part A
def f0_sorting(X, y, mu, rule):
    """min_j of the p = 1 selection-witness number (Theorem thm:hard(b)), computed by sorting."""
    n, p = len(X), len(X[0])
    best = None
    for j in range(p):
        a = sorted(X[i][j] * y[i] for i in range(n))
        T = sum(a, F(0))
        for k in range(1, n):
            mk = mu_rule(mu, n, k, rule)
            small = sum(a[:k], F(0))          # sum of the k smallest a_i
            large = sum(a[n - k:], F(0))      # sum of the k largest a_i
            if T - small > mk or T - large < -mk:
                if best is None or k < best:
                    best = k
                break
    return best


def status_xe(G, q, mu):
    """v0.7. Like lasso_status, but ties |c_j| = mu are resolved by the sufficient condition of Tibshirani (2013):
    find an exact KKT point, form the equicorrelation set E (common to all minimisers, which share the fit) and
    certify uniqueness iff X_E has full column rank (G_EE nonsingular). Returns 'zero', 'unique' or
    'undetermined' (X_E rank deficient: the minimiser may or may not be unique)."""
    p = len(q)
    if max(abs(v) for v in q) <= mu:
        return "zero"
    for size in range(1, p + 1):
        for S in itertools.combinations(range(p), size):
            GSS = [[G[a][b] for b in S] for a in S]
            for s in itertools.product((1, -1), repeat=size):
                beta = solve(GSS, [q[a] - mu * sg for a, sg in zip(S, s)])
                if beta is None or any(sg * bv <= 0 for sg, bv in zip(s, beta)):
                    continue
                c = [q[j] - sum(G[j][a] * bv for a, bv in zip(S, beta)) for j in range(p)]
                if any(abs(c[j]) > mu for j in range(p) if j not in S):
                    continue
                E = [j for j in range(p) if abs(c[j]) == mu]          # contains S
                GEE = [[G[a][b] for b in E] for a in E]
                return "unique" if solve(GEE, [F(0)] * len(E)) is not None else "undetermined"
    return "undetermined"   # not reached: some minimiser has a support with full-rank Gram (Lemma lem:rank)


def exhaustive_signed_xe(X, y, mu, rule):
    """v0.7. Least |R| whose subsample has ||X_K^T y_K|| > mu' and a minimiser certified unique by status_xe
    (an upper bound for f^signed, equal to it when every subsample is decided)."""
    n = len(X)
    for k in range(1, n):
        mk = mu_rule(mu, n, k, rule)
        for R in itertools.combinations(range(n), k):
            K = [i for i in range(n) if i not in R]
            G, q = gram(X, y, K)
            if status_xe(G, q, mk) == "unique":
                return k
    return None


def rstar_sets(X, y, mu, rule, f0):
    """The removal sets R*_j of size f0 produced by the sort of Theorem thm:hard(b), for every column j with
    f0_j = f0: the f0 smallest a_ij = x_ij y_i (removal raises the sum) and/or the f0 largest (removal lowers
    it), ties in the sort broken by row index. Each has |X_{K,j}^T y_K| > mu_{f0} by construction."""
    n, p = len(X), len(X[0])
    out = []
    for j in range(p):
        a = [X[i][j] * y[i] for i in range(n)]
        order = sorted(range(n), key=lambda i: (a[i], i))
        T = sum(a, F(0))
        for k in range(1, n):
            mk = mu_rule(mu, n, k, rule)
            small = sum((a[i] for i in order[:k]), F(0))
            large = sum((a[i] for i in order[n - k:]), F(0))
            lo_ok, hi_ok = T - small > mk, T - large < -mk
            if lo_ok or hi_ok:
                if k == f0:
                    if lo_ok:
                        out.append(tuple(sorted(order[:k])))
                    if hi_ok:
                        out.append(tuple(sorted(order[n - k:])))
                break
    return sorted(set(out))


def exhaustive_signed(X, y, mu, rule):
    """Exhaustive signed-ANY fragility number on an instance with S(D) = {} (certified witnesses only)."""
    n = len(X)
    undetermined = 0
    f = None
    f_nounique = None   # min |R| with ||X_K^T y_K|| > mu' irrespective of uniqueness
    for k in range(1, n):
        mk = mu_rule(mu, n, k, rule)
        for R in itertools.combinations(range(n), k):
            K = [i for i in range(n) if i not in R]
            G, q = gram(X, y, K)
            st, _ = lasso_status(G, q, mk)
            if st != "zero" and f_nounique is None:
                f_nounique = k
            if st == "undetermined":
                undetermined += 1
            if st == "unique" and f is None:
                f = k
        if f is not None and f_nounique is not None:
            break
    return f, f_nounique, undetermined


def part_a(rng):
    log("== (A) signed ANY from the empty support: exhaustive search vs per-column sorting ==")
    tot = agree = ge_ok = 0
    tie_inst = 0
    rows = []
    f0_inf = f0_fin = cert_ok = cert_fail = cert_ok_ties = ties_eq = 0
    cert_open = []
    for trial in range(400):
        p = rng.choice([2, 3])
        n = rng.choice([5, 6, 7, 8])
        rule = rng.choice(["C", "P"])
        wide = trial % 4 != 0          # every 4th instance: small integers (ties likely, adversarial)
        lo = 9 if wide else 2
        X = [[F(rng.randint(-lo, lo)) for _ in range(p)] for _ in range(n)]
        y = [F(rng.randint(-lo, lo)) for _ in range(n)]
        _, qD = gram(X, y, range(n))
        top = max(abs(v) for v in qD)
        mu = top + F(rng.randint(0, 6), rng.choice([1, 2, 3]))   # S(D) = {} by construction
        if mu <= 0:
            mu = F(1, 2)
        fe, fnu, und = exhaustive_signed(X, y, mu, rule)
        fs = f0_sorting(X, y, mu, rule)
        tot += 1
        # v0.7: polynomial certificate R*_j (no random numbers consumed). fx: exhaustive value with uniqueness
        # certified by full rank of X_E (differs from fe only on tied instances; an upper bound for f^signed)
        fx = fe if und == 0 else exhaustive_signed_xe(X, y, mu, rule)
        if fs is None:
            f0_inf += 1
        else:
            f0_fin += 1
            cands = rstar_sets(X, y, mu, rule, fs)
            assert cands, "the sort produces at least one R*_j of size f0"
            sts = []
            for Rs in cands:
                K = [i for i in range(n) if i not in Rs]
                G, q = gram(X, y, K)
                st = status_xe(G, q, mu_rule(mu, n, len(Rs), rule))
                assert st != "zero", "R*_j has ||X_K^T y_K||_inf > mu'"
                sts.append(st)
            if "unique" in sts:
                cert_ok += 1
                cert_fail += fx != fs
                cert_ok_ties += und > 0
            else:
                cert_open.append((trial, p, n, rule, fe, fs, und))
        if und > 0:
            ties_eq += fx == fs
        # f^signed >= f0 always (f = None means infinity)
        if fe is None or (fs is not None and fe >= fs):
            ge_ok += 1
        if und == 0:
            if fe == fs and fnu == fs:
                agree += 1
            else:
                rows.append(("MISMATCH", trial, p, n, rule, fe, fs, fnu))
        else:
            tie_inst += 1
            if fnu != fs:
                rows.append(("MISMATCH-nounique", trial, p, n, rule, fe, fs, fnu))
    clean = tot - tie_inst
    log(f"instances: {tot} (p in {{2,3}}, n in 5..8, both rules, S(D) empty)")
    log(f"f_signed >= f0 (per-column sorting): {ge_ok}/{tot}")
    log(f"min|R| with ||X_K^T y_K||_inf > mu' equals f0 in all instances: "
        f"{sum(1 for r in rows if r[0] == 'MISMATCH-nounique') == 0}")
    log(f"instances with every subsample certified (no ties): {clean}; f_signed == f0 there: {agree}/{clean}")
    log(f"instances with at least one undetermined (tied) subsample: {tie_inst}")
    for r in rows[:10]:
        log("  " + str(r))
    log(f"[v0.7] instances with f0 = infinity (then f_signed = infinity = f0): {f0_inf}")
    log(f"[v0.7] certificate R*_j (a sort-produced removal set of size f0 whose minimiser is certified unique by "
        f"full rank of X_E): closes f_signed = f0 in {cert_ok}/{f0_fin} instances with finite f0, "
        f"{cert_ok_ties}/{tie_inst} of them with tied subsamples; disagreements with exhaustive search: {cert_fail}")
    log(f"[v0.7] tied instances searched again with uniqueness certified by full rank of X_E: "
        f"f_signed = f0 in {ties_eq}/{tie_inst}")
    for r in cert_open[:10]:
        log("  [v0.7] not closed by R*: (trial, p, n, rule, f_signed, f0, tied subsamples) = " + str(r))
    return dict(total=tot, ge_ok=ge_ok, clean=clean, agree=agree, tie_instances=tie_inst,
                mismatches=len(rows), f0_infinite=f0_inf, f0_finite=f0_fin, cert_ok=cert_ok,
                cert_fail=cert_fail, cert_ok_ties=cert_ok_ties, cert_open=len(cert_open), ties_equal_xe=ties_eq)


# ----------------------------------------------------------------------------- part B
def part_b(rng):
    log("")
    log("== (B) Cauchy--Binet form of the inactive correlation, p = 2, S = {1} ==")
    ok = tot = 0
    for _ in range(300):
        n = rng.randint(2, 9)
        X = [[F(rng.randint(-7, 7)), F(rng.randint(-7, 7))] for _ in range(n)]
        y = [F(rng.randint(-7, 7)) for _ in range(n)]
        mu = F(rng.randint(1, 30), rng.randint(1, 4))
        K = [i for i in range(n) if rng.random() < 0.7] or [0]
        G, q = gram(X, y, K)
        if G[0][0] == 0:
            continue
        lhs = G[0][0] * (q[1] - G[0][1] * (q[0] - mu) / G[0][0] - mu)
        rhs = F(0)
        for a, b in itertools.combinations(K, 2):
            m = X[a][0] * X[b][1] - X[b][0] * X[a][1]
            mp = X[a][0] * y[b] - X[b][0] * y[a]
            rhs += m * mp
        rhs -= mu * sum((X[i][0] * (X[i][0] - X[i][1]) for i in K), F(0))
        tot += 1
        ok += lhs == rhs
    log(f"identity G11 (c2 - mu) = sum_(i<l) m_il m'_il - mu sum_i x_i1 (x_i1 - x_i2): {ok}/{tot}")
    # the 'variance' form for one-parameter polynomial item families (alpha = 1)
    ok2 = tot2 = 0
    for _ in range(200):
        N = rng.randint(2, 7)
        b = [F(rng.randint(-9, 9)) for _ in range(N)]
        e, y1 = F(rng.randint(1, 5), 7), F(rng.randint(1, 5), 3)
        rows = [(F(1), 1 + e * bi) for bi in b]
        ys = [F(2) + y1 * bi for bi in b]
        cb = sum(((r1[0] * r2[1] - r2[0] * r1[1]) * (r1[0] * yb - r2[0] * ya)
                  for (r1, ya), (r2, yb) in itertools.combinations(list(zip(rows, ys)), 2)), F(0))
        sig = sum(b, F(0))
        var = N * sum((bi * bi for bi in b), F(0)) - sig * sig
        tot2 += 1
        ok2 += cb == e * y1 * var
    log(f"items (1, 1 + e b_i), y_i = y0 + y1 b_i: item-item part = e y1 (N sum b_i^2 - sigma^2) >= 0: "
        f"{ok2}/{tot2}")
    return dict(cb_total=tot, cb_ok=ok, var_total=tot2, var_ok=ok2)


# ----------------------------------------------------------------------------- part C
def x3c_gadget(q, triples, L, theta, phi, gamma, b0, mu, keep):
    """Rows: kept triples (x0 = theta, incidence, y = 3 b0 + gamma) and L anchor copies per element
    (x0 = phi, x_e = 1, y = b0 + mu / L).  Returns the fixed-support candidate (S = U, s = +)."""
    U = 3 * q
    X, y = [], []
    for i in keep:
        X.append([theta] + [F(1) if e in triples[i] else F(0) for e in range(U)])
        y.append(3 * b0 + gamma)
    for e in range(U):
        for _ in range(L):
            X.append([phi] + [F(1) if e2 == e else F(0) for e2 in range(U)])
            y.append(b0 + mu / L)
    p = U + 1
    K = range(len(X))
    G, qv = gram(X, y, K)
    S = list(range(1, p))
    GSS = [[G[a][b] for b in S] for a in S]
    beta = solve(GSS, [qv[a] - mu for a in S])
    c0 = qv[0] - sum(G[0][a] * bv for a, bv in zip(S, beta))
    resid = [y[i] - sum(X[i][a] * bv for a, bv in zip(S, beta)) for i in range(len(keep))]
    return beta, c0, resid


def f_of(q, triples, L, keep):
    N = len(keep)
    M = [[F(len(triples[i] & triples[l])) + (L if i == l else 0) for l in keep] for i in keep]
    g = solve(M, [F(1)] * N)
    return sum(g, F(0)), g


def part_c(rng):
    log("")
    log("== (C) X3C-type gadget with uniform triple rows: c0 is affine in f(K) = 1^T (L I + M_K)^{-1} 1 ==")
    id_ok = id_tot = 0
    res_ok = 0
    cover_is_max = cover_is_min = cover_inst = 0
    for trial in range(30):
        q = 2
        U = 3 * q
        while True:
            m = rng.randint(3, 5)
            triples = [frozenset(rng.sample(range(U), 3)) for _ in range(m)]
            if len(set(triples)) == m:
                break
        L = rng.choice([2, 5, 20])
        theta, phi = F(rng.randint(1, 9), 5), F(rng.randint(0, 9), 7)
        gamma, b0, mu = F(rng.randint(1, 9), 4), F(rng.randint(1, 9), 3), F(rng.randint(1, 9))
        fam = {}
        for N in range(q, m + 1):
            for keep in itertools.combinations(range(m), N):
                beta, c0, resid = x3c_gadget(q, triples, L, theta, phi, gamma, b0, mu, keep)
                f, g = f_of(q, triples, L, keep)
                pred = 3 * q * phi * mu + gamma * L * (theta - 3 * phi) * f
                id_tot += 1
                id_ok += c0 == pred
                res_ok += all(r == gamma * L * gi for r, gi in zip(resid, g))
                fam[keep] = f
        covers = [k for k in fam if len(k) == q and len(frozenset().union(*[triples[i] for i in k])) == U]
        if covers:
            cover_inst += 1
            fmax, fmin = max(fam.values()), min(fam.values())
            cover_is_max += any(fam[c] == fmax for c in covers) and all(
                fam[k] < fmax for k in fam if k not in covers)
            cover_is_min += any(fam[c] == fmin for c in covers) and all(
                fam[k] > fmin for k in fam if k not in covers)
    log(f"identity c0 = 3 q phi mu + gamma L (theta - 3 phi) f(K): {id_ok}/{id_tot} (kept families, all anchors)")
    log(f"triple residuals r = gamma L (L I + M_K)^{{-1}} 1 = gamma (I + M_K/L)^{{-1}} 1: {res_ok}/{id_tot}")
    log(f"instances with an exact cover: {cover_inst}; exact covers are the strict maximisers of f: "
        f"{cover_is_max}; the strict minimisers: {cover_is_min}")
    return dict(id_total=id_tot, id_ok=id_ok, res_ok=res_ok, cover_instances=cover_inst,
                cover_strict_max=cover_is_max, cover_strict_min=cover_is_min)


def main():
    import hashlib
    import sys
    import time
    t0 = time.process_time()
    rng = random.Random(SEED)
    log("check_signed_any.py -- exact arithmetic, seed %d" % SEED)
    A = part_a(rng)
    B = part_b(rng)
    C = part_c(rng)
    cpu = time.process_time() - t0
    print(f"cpu seconds: {cpu:.1f}")          # printed only: the frozen log carries no timing line
    with open(OUT, "w") as fh:
        fh.write("\n".join(LINES) + "\n")
    sha = hashlib.sha256(open(OUT, "rb").read()).hexdigest()
    with open(os.path.join(RES, "check_signed_any_output.sha256"), "w") as fh:
        fh.write(f"{sha}  check_signed_any_output.txt\n")
    meta = dict(script="experiments/check_signed_any.py", original="theory/check_signed_any.py", seed=SEED,
                python=sys.version.split()[0], cpu_seconds=round(cpu, 1), log_sha256=sha, log_has_timing=False)
    with open(JSON, "w") as fh:
        json.dump({"meta": meta, "seed": SEED, "A_empty_support": A, "B_cauchy_binet": B, "C_x3c_gadget": C},
                  fh, indent=2)


if __name__ == "__main__":
    main()
