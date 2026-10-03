#!/usr/bin/env python3
"""
Numerical check of theory/sharp_rate.tex (MRT001 v0.6, sharp first-order rates in
Theorem 5.6 / Proposition 5.7).

Conventions as in check_realizer_law.py: pi uniform in S_n (0-based values),
N = #{i : pi(i+1) = pi(i) - 1}, R = number of realizers modulo the swap, Z ~ Po(1),
p_k = P(N_n = k), pi_k = e^{-1}/k!.

(A) exact law of N_n for n <= 60 in rational arithmetic, three independent ways
    (inversion of the factorial moments 1 - r/n; closed form C(n-1,k)(D_{n-k}+D_{n-k-1})/n!;
    insertion recurrence), plus brute force for n <= 8; checks
      p_k = pi_k (1 - (k-1)/n) + r_{n,k},  |r_{n,k}| <= 1/(n k! (n-k+1)!),
      d_TV(N_n, Po(1)) = (p_0 - pi_0) + (p_1 - pi_1)^+,  |n d_TV - e^{-1}| <= 2/n!,
    and n^2 d_TV(N_n, Po(1 - 1/n)) -> 3/(4e) (remark, not claimed as proved).
(B) the first-order signed measure mu of R_n and c_2 = |mu|/2 = 1 + 1/(2e).
(C) the explicit bound P(R_n != 2^N_n) <= 5/n + 220/n^2 (n >= 20): pair moments checked by
    exhaustive enumeration (n = 8, 9) and the closed forms evaluated for 20 <= n <= 3000;
    exact law of R_n by enumeration for n <= 8.
(D) Monte Carlo of d_TV(R_n, 2^Z) with the exact law of 2^{N_n} as control variate
    (R computed by the substitution-tree formula of check_realizer_law.py on samples that
    have an interval of length in [3, K] or [n-K, n-1]; R = 2^N on the others by Step 1).
(E) comparison with results/results_realizer_law.json (E5f) and the frozen output
    results/check_realizer_law_output.txt.

Usage: python3 check_sharp_rate.py      (writes check_sharp_rate_output.txt)
"""
import itertools
import json
import math
import os
import platform
import sys
import time
from collections import Counter
from fractions import Fraction

import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
sys.dont_write_bytecode = True     # do not touch theory/__pycache__
sys.path.insert(0, HERE)
import check_realizer_law as crl  # noqa: E402  (read-only reuse: realizers_formula, flag_batch, n_desc)

SEED = 20261004
OUT = os.path.join(HERE, "check_sharp_rate_output.txt")
_lines = []


def say(*args):
    s = " ".join(str(a) for a in args)
    print(s, flush=True)
    _lines.append(s)


FACT = [math.factorial(i) for i in range(2200)]
EINV = sum(Fraction((-1) ** s, FACT[s]) for s in range(171))       # |EINV - 1/e| < 1/171!
TOL = Fraction(1, 10 ** 250)
D = [1, 0]
for _m in range(2, 2100):
    D.append((_m - 1) * (D[-1] + D[-2]))                              # derangement numbers
E1 = math.exp(-1.0)


# --------------------------------------------------------------------------
# (A) exact law of N_n
# --------------------------------------------------------------------------
def law_moments(n):
    """inversion P(N=k) = sum_r (-1)^{r-k} C(r,k) E[(N)_r]/r! with E[(N)_r] = 1 - r/n (r < n), 0 (r >= n)."""
    return [sum(Fraction((-1) ** s, FACT[k] * FACT[s]) * (1 - Fraction(k + s, n)) for s in range(n - k))
            for k in range(n)]


def law_closed(n):
    """P(N_n = k) = C(n-1,k) (D_{n-k} + D_{n-k-1}) / n!  (Kaplansky; Roselle)."""
    return [Fraction(math.comb(n - 1, k) * (D[n - k] + D[n - k - 1]), FACT[n]) for k in range(n)]


def law_closed_float(n, kmax=60):
    return [float(Fraction(math.comb(n - 1, k) * (D[n - k] + D[n - k - 1]), FACT[n])) for k in range(min(n, kmax))]


def law_dp(n):
    """insertion of the largest element m into a permutation of [m-1] with j descending successions:
    1 slot (just before m-1) creates one, j slots (inside a succession) destroy one, m-1-j are neutral."""
    S = [1]
    for m in range(2, n + 1):
        new = [0] * m
        for j, c in enumerate(S):
            if c:
                new[j + 1] += c
                if j:
                    new[j - 1] += c * j
                new[j] += c * (m - 1 - j)
        S = new
    return [Fraction(c, FACT[n]) for c in S]


def law_brute(n):
    cnt = Counter()
    for p in itertools.permutations(range(n)):
        cnt[sum(1 for i in range(n - 1) if p[i + 1] == p[i] - 1)] += 1
    return [Fraction(cnt[k], FACT[n]) for k in range(n)]


def part_a():
    say("=" * 78)
    say("(A) exact law of N_n (rational arithmetic, 1/e replaced by a rational within 1/171!)")
    say("=" * 78)
    t0 = time.time()
    ok_laws = ok_moments = True
    for n in range(1, 61):
        a, b, c = law_moments(n), law_closed(n), law_dp(n)
        if not (a == b == c):
            ok_laws = False
        if n <= 8 and law_brute(n) != b:
            ok_laws = False
        for r in range(n + 1):
            fm = sum(Fraction(math.perm(k, r)) * b[k] for k in range(n))
            if fm != (1 - Fraction(r, n) if r < n else 0):
                ok_moments = False
    say(f"n = 1..60: inversion of factorial moments == closed form C(n-1,k)(D_(n-k)+D_(n-k-1))/n! == insertion "
        f"recurrence (and == brute force for n <= 8): {ok_laws}")
    say(f"n = 1..60: E[(N_n)_r] = 1 - r/n for 0 <= r <= n-1 and 0 for r = n: {ok_moments}")
    say(f"  ({time.time() - t0:.1f} s)")
    say("")
    say("first-order expansion  p_k = pi_k (1 - (k-1)/n) + r_{n,k},  claimed |r_{n,k}| <= 1/(n k! (n-k+1)!)")
    say("d_TV identity  d_TV(N_n, Po(1)) = (p_0 - pi_0) + (p_1 - pi_1)^+  and  |n d_TV - 1/e| <= 2/n!  (n >= 4)")
    say(" n | max_k |r_{n,k}| n k!(n-k+1)! | sign pattern ok | identity ok | n*d_TV            | n*d_TV - 1/e | "
        "n!*(n*d_TV - 1/e) | d_TV / (e^2/n + (2^n+1)/(2n!))")
    all_ok = True
    worst_r = Fraction(0)
    worst_dev = Fraction(0)
    for n in range(4, 61):
        p = law_closed(n)
        pis = [EINV / FACT[k] for k in range(n)]
        rr = max(abs(p[k] - pis[k] * (1 - Fraction(k - 1, n))) * n * FACT[k] * FACT[n - k + 1] for k in range(n))
        worst_r = max(worst_r, rr)
        signs = p[0] > pis[0] and all(p[k] < pis[k] for k in range(2, n))
        dtv = (sum(abs(p[k] - pis[k]) for k in range(n)) + (1 - sum(pis))) / 2
        ident = (p[0] - pis[0]) + max(p[1] - pis[1], Fraction(0))
        idok = abs(dtv - ident) < TOL
        dev = n * dtv - EINV
        dev_scaled = dev * FACT[n]
        worst_dev = max(worst_dev, abs(dev_scaled))
        ok = rr <= 1 and signs and idok and abs(dev_scaled) <= 2
        all_ok &= ok
        if n in (4, 5, 6, 7, 8, 10, 12, 15, 20, 25, 30, 40, 50, 60):
            old = math.exp(2) / n + (2 ** n + 1) / (2 * FACT[n])
            say(f"{n:2d} | {float(rr):.4f} | {signs} | {idok} | {float(n * dtv):.15f} | {float(dev):+.3e} | "
                f"{float(dev_scaled):+.4f} | {float(dtv) / old:.4f}")
    say(f"all n in [4, 60]: bounds and identities hold: {all_ok};  max |r| n k!(n-k+1)! = {float(worst_r):.4f} (<= 1);"
        f"  max |n!(n d_TV - 1/e)| = {float(worst_dev):.4f} (<= 2)")
    say(f"1/e = {E1:.15f}")
    say("")
    say("Remark (numerical only): n^2 d_TV(N_n, Po(1 - 1/n)) against 3/(4e) = %.6f" % (3 / (4 * math.e)))
    for n in (10, 20, 40, 60, 100, 200, 500, 1000):
        p = law_closed_float(n)
        lam = 1 - 1 / n
        q = [math.exp(-lam) * lam ** k / FACT[k] for k in range(len(p))]
        dtv = 0.5 * (sum(abs(a - b) for a, b in zip(p, q)) + max(0.0, 1 - sum(q)))
        say(f"  n = {n:4d}: n^2 d_TV(N_n, Po(1-1/n)) = {n * n * dtv:.6f}")
    say(f"  ({time.time() - t0:.1f} s)")


# --------------------------------------------------------------------------
# (B) first-order law of R_n and c_2
# --------------------------------------------------------------------------
def pois(k):
    return E1 / FACT[k] if k >= 0 else 0.0


def law_add(L, M, w=1.0):
    out = dict(L)
    for x, v in M.items():
        out[x] = out.get(x, 0.0) + w * v
    return out


def law_of(values_probs):
    out = {}
    for x, v in values_probs:
        out[x] = out.get(x, 0.0) + v
    return out


def mu_closed(kmax=60):
    mu = {}
    for k in range(kmax):
        mu[Fraction(2 ** k)] = -3 * pois(k) + 3 * pois(k - 1) - pois(k - 2)
    for k in range(1, kmax):
        mu[Fraction(3 * 2 ** k)] = pois(k - 1)
    return mu


def mu_components(kmax=60):
    """nu_N + [L(6*2^Z) - L(4*2^Z)] + 4 [L(2^(Z+1)) - L(2^Z)], nu_N(2^k) = pi_k - pi_{k-1}."""
    nu = {Fraction(2 ** k): pois(k) - pois(k - 1) for k in range(kmax)}
    six = law_of((Fraction(6 * 2 ** k), pois(k)) for k in range(kmax))
    four = law_of((Fraction(4 * 2 ** k), pois(k)) for k in range(kmax))
    two = law_of((Fraction(2 ** (k + 1)), pois(k)) for k in range(kmax))
    one = law_of((Fraction(2 ** k), pois(k)) for k in range(kmax))
    m = law_add(nu, six)
    m = law_add(m, four, -1)
    m = law_add(m, two, 4)
    m = law_add(m, one, -4)
    return m


def part_b():
    say("=" * 78)
    say("(B) first-order signed measure mu of R_n:  P(R_n = x) = P(2^Z = x) + mu(x)/n + O(n^-2)")
    say("=" * 78)
    mc, mk = mu_closed(), mu_components()
    keys = set(mc) | set(mk)
    diff = max(abs(mc.get(x, 0.0) - mk.get(x, 0.0)) for x in keys)
    say(f"closed form mu(2^k) = -(e^-1/k!)(k-1)(k-3), mu(3*2^k) = e^-1/(k-1)!  vs  sum of components: max diff {diff:.1e}")
    say(f"total mass of mu: {sum(mc.values()):+.1e}")
    c2 = 0.5 * sum(abs(v) for v in mc.values())
    say(f"c_2 = |mu|/2 = {c2:.15f};  1 + 1/(2e) = {1 + 1 / (2 * math.e):.15f}")
    s = sum(abs((k - 1) * (k - 3)) / FACT[k] for k in range(80))
    say(f"sum_k |(k-1)(k-3)|/k! = {s:.15f};  e + 1 = {math.e + 1:.15f}")
    s = 0.5 * sum(abs(k - 1) / FACT[k] for k in range(80))
    say(f"c_1 = (e^-1/2) sum_k |k-1|/k! = {E1 * s:.15f};  e^-1 = {E1:.15f}")
    say("atoms: x | P(2^Z = x) | mu(x)")
    for x in sorted(mc, key=float):
        if float(x) <= 96:
            say(f"  {str(x):>3} | {pois(int(math.log2(x))) if (x.denominator == 1 and int(x) & (int(x) - 1) == 0) else 0.0:.6f} | {mc[x]:+.6f}")


def model_law(n):
    """refined first-order model: law of 2^{N_n} plus the five exception types with exact weights
    (n-2)/(n(n-1)) (patterns 321, 231, 312) and 1/n (pi(1)=n, pi(n)=1) and exact laws of N_{n-2}, N_{n-1}."""
    pN = law_closed_float(n)
    L = {Fraction(2 ** k): v for k, v in enumerate(pN)}
    w3, w1 = (n - 2) / (n * (n - 1)), 1 / n
    q2, q1 = law_closed_float(n - 2), law_closed_float(n - 1)
    L = law_add(L, law_of((Fraction(6 * 2 ** k), v) for k, v in enumerate(q2)), w3)
    L = law_add(L, law_of((Fraction(4 * 2 ** k), v) for k, v in enumerate(q2)), -w3)
    for q, w in ((q2, 2 * w3), (q1, 2 * w1)):
        L = law_add(L, law_of((Fraction(2 ** (k + 1)), v) for k, v in enumerate(q)), w)
        L = law_add(L, law_of((Fraction(2 ** k), v) for k, v in enumerate(q)), -w)
    return L


def poisson_pow2(kmax=64):
    return {Fraction(2 ** k): pois(k) for k in range(kmax)}


def dtv(L, M):
    keys = set(L) | set(M)
    return 0.5 * sum(abs(L.get(x, 0.0) - M.get(x, 0.0)) for x in keys)


# --------------------------------------------------------------------------
# (C) explicit bound P(R != 2^N) <= 5/n + 220/n^2 and exact small-n laws of R
# --------------------------------------------------------------------------
def EI(n, k):
    return crl.EI(n, k)


def pair_formulas(n):
    F = Fraction
    c33 = (F(18 * (n - 4) * (n - 5), n * (n - 1) * (n - 2) * (n - 3)) + F(4 * (n - 3), n * (n - 1) * (n - 2))
           + F(8 * (n - 4), n * (n - 1) * (n - 2) * (n - 3)))
    c3n = F(4 * (6 * n - 16), n * (n - 1) * (n - 2))
    cnn = F(2, n * (n - 1))
    return c33, c3n, cnn


def part_c():
    say("=" * 78)
    say("(C) explicit bound  P(R_n != 2^N_n) <= 5/n + 220/n^2  for n >= 20")
    say("=" * 78)
    t0 = time.time()
    for n in (8, 9):
        P = np.array(list(itertools.permutations(range(n))), dtype=np.int8)
        I3 = np.zeros(len(P), dtype=np.int64)
        for a in range(n - 2):
            w = P[:, a:a + 3]
            I3 += (w.max(axis=1) - w.min(axis=1) == 2)
        In1 = np.isin(P[:, 0], (0, n - 1)).astype(np.int64) + np.isin(P[:, -1], (0, n - 1)).astype(np.int64)
        obs = (Fraction(int((I3 * (I3 - 1) // 2).sum()), FACT[n]), Fraction(int((I3 * In1).sum()), FACT[n]),
               Fraction(int((In1 * (In1 - 1) // 2).sum()), FACT[n]))
        say(f"n = {n} exhaustive: E[C(I3,2)], E[I3 I_(n-1)], E[C(I_(n-1),2)] = {obs[0]}, {obs[1]}, {obs[2]};"
            f" formulas: {pair_formulas(n)};  equal: {obs == pair_formulas(n)}")
    worst = {"sum4": 0.0, "c33": 0.0, "c3n": 0.0, "cnn": 0.0, "total": -1e9}
    for n in range(20, 3001):
        s4 = sum(EI(n, k) for k in range(4, n - 1))
        c33, c3n, cnn = (float(v) for v in pair_formulas(n))
        first = 3 * (n - 2) / (n * (n - 1)) + 2 / n
        tot = first + s4 + c33 + c3n + cnn
        worst["sum4"] = max(worst["sum4"], s4 * n * n / 172)
        worst["c33"] = max(worst["c33"], c33 * n * n / 23)
        worst["c3n"] = max(worst["c3n"], c3n * n * n / 25)
        worst["cnn"] = max(worst["cnn"], cnn * n * n / 3)
        worst["total"] = max(worst["total"], (tot - 5 / n) * n * n)
        if n in (20, 50, 100, 1000):
            say(f"  n = {n:4d}: 3(n-2)/(n(n-1))+2/n = {first:.5f}, sum_(k=4)^(n-2) E I_k = {s4:.2e}, pairs = "
                f"{c33:.2e} + {c3n:.2e} + {cnn:.2e};  bound = {tot:.5f} = 5/n + {(tot - 5 / n) * n * n:.1f}/n^2")
    say(f"  20 <= n <= 3000: max of [sum_(k=4)^(n-2) E I_k]/(172/n^2) = {worst['sum4']:.4f}, E[C(I3,2)]/(23/n^2) = "
        f"{worst['c33']:.4f}, E[I3 I_(n-1)]/(25/n^2) = {worst['c3n']:.4f}, E[C(I_(n-1),2)]/(3/n^2) = {worst['cnn']:.4f}"
        f"  (all must be <= 1)")
    say(f"  max over 20 <= n <= 3000 of n^2 (bound - 5/n) = {worst['total']:.2f} (<= 220)")
    say(f"  ({time.time() - t0:.1f} s)")
    say("")
    say("exact law of R_n by enumeration (substitution-tree formula), small n -- only a sanity check, the")
    say("O(n^-2) terms dominate here:  n | P(R != 2^N) | d_TV(R_n, 2^Z) | n d_TV | n d_TV(model, 2^Z) | d_TV(R_n, model)")
    PZ = poisson_pow2()
    for n in range(5, 9):
        cnt = Counter()
        exc = 0
        for p in itertools.permutations(range(n)):
            r = crl.realizers_formula(list(p))
            N = sum(1 for i in range(n - 1) if p[i + 1] == p[i] - 1)
            exc += r != 2 ** N
            cnt[Fraction(r)] += 1
        L = {x: c / FACT[n] for x, c in cnt.items()}
        Lm = model_law(n)
        say(f"  {n} | {exc / FACT[n]:.4f} | {dtv(L, PZ):.4f} | {n * dtv(L, PZ):.3f} | {n * dtv(Lm, PZ):.3f} | "
            f"{dtv(L, Lm):.4f}")
    say(f"  ({time.time() - t0:.1f} s)")


# --------------------------------------------------------------------------
# (D) Monte Carlo with control variate
# --------------------------------------------------------------------------
def part_d():
    say("=" * 78)
    say("(D) Monte Carlo of d_TV(R_n, 2^Z): P(R=x) estimated as P(2^{N_n}=x) [exact] + mean of 1{R=x} - 1{2^N=x}")
    say("=" * 78)
    rng = np.random.default_rng(SEED)
    PZ = poisson_pow2()
    mu = mu_closed()
    c2 = 1 + 1 / (2 * math.e)
    K = 6
    plan = [(50, 300000), (100, 200000), (200, 150000), (400, 150000), (1000, 60000)]
    G = 10
    summary = []
    for n, M in plan:
        t0 = time.time()
        missed = crl.s_n(n, K + 1, n - K - 1)
        pN = law_closed_float(n)
        base = {Fraction(2 ** k): v for k, v in enumerate(pN)}
        dpos = [Counter() for _ in range(G)]      # per group: #{R = x, 2^N != x}
        dneg = [Counter() for _ in range(G)]      # per group: #{2^N = x, R != x}
        Mg = [0] * G
        exc = flagged = 0
        ratios = Counter()
        B = max(1, min(20000, 4_000_000 // n))
        done = 0
        while done < M:
            b = min(B, M - done)
            P = np.argsort(rng.random((b, n)), axis=1).astype(np.int32)
            F = crl.flag_batch(P, n, K)
            g = (done // B) % G
            Mg[g] += b
            for i in np.nonzero(F)[0]:
                p = P[i].tolist()
                r = crl.realizers_formula(p)
                N = crl.n_desc(p)
                if r != 2 ** N:
                    exc += 1
                    ratios[Fraction(r, 2 ** N)] += 1
                    dpos[g][Fraction(r)] += 1
                    dneg[g][Fraction(2 ** N)] += 1
            flagged += int(F.sum())
            done += b

        def est(groups):
            m = sum(Mg[j] for j in groups)
            L = dict(base)
            for j in groups:
                for x, c in dpos[j].items():
                    L[x] = L.get(x, 0.0) + c / m
                for x, c in dneg[j].items():
                    L[x] = L.get(x, 0.0) - c / m
            return L, m

        Lall, _ = est(range(G))
        d_all = dtv(Lall, PZ)
        loo = [dtv(est([j for j in range(G) if j != h])[0], PZ) for h in range(G)]
        se = math.sqrt((G - 1) / G * sum((v - sum(loo) / G) ** 2 for v in loo))
        Lm = model_law(n)
        d_model = dtv(Lm, PZ)
        pe = exc / M
        say(f"n = {n}: {M} samples, flagged {flagged / M:.4f}, missed-interval bound {missed:.1e}, "
            f"P(R != 2^N) = {pe:.5f} (n P = {n * pe:.3f} +- {1.96 * n * math.sqrt(pe * (1 - pe) / M):.3f}); "
            f"ratios R/2^N: " + ", ".join(f"{str(r)}: {c}" for r, c in sorted(ratios.items())))
        say(f"   n d_TV(R_n, 2^Z): Monte Carlo {n * d_all:.4f} +- {1.96 * n * se:.4f} (95%, jackknife over {G} groups); "
            f"refined first-order model {n * d_model:.4f}; c_2 = {c2:.4f}; d_TV(model, MC estimate) * n = "
            f"{n * dtv(Lm, Lall):.4f}")
        say("   x  | n(P_MC(R=x) - P(2^Z=x)) +- 1.96 SE | mu(x) | n(P_model(x) - P(2^Z=x))")
        for x in [Fraction(v) for v in (1, 2, 4, 8, 16, 32, 6, 12, 24, 48, 3)]:
            npos = sum(dpos[j][x] for j in range(G))
            nneg = sum(dneg[j][x] for j in range(G))
            var = (npos + nneg) / M - ((npos - nneg) / M) ** 2
            val = n * (Lall.get(x, 0.0) - PZ.get(x, 0.0))
            say(f"   {str(x):>3} | {val:+.3f} +- {1.96 * n * math.sqrt(var / M):.3f} | {mu.get(x, 0.0):+.3f} | "
                f"{n * (Lm.get(x, 0.0) - PZ.get(x, 0.0)):+.3f}")
        say(f"   ({time.time() - t0:.1f} s)")
        summary.append((n, n * d_all, 1.96 * n * se, n * d_model))
    say("summary: n | n d_TV MC (95%) | n d_TV model | c_2 | old bound n*[(10+e^2)/n+167/n^2] | new bound n*[(5+1/e)/n+221/n^2]")
    for n, a, b, c in summary:
        say(f"  {n:4d} | {a:.3f} +- {b:.3f} | {c:.3f} | {c2:.3f} | {10 + math.e ** 2 + 167 / n:.2f} | {5 + E1 + 221 / n:.2f}")


# --------------------------------------------------------------------------
# (E) E5f samples and frozen check output
# --------------------------------------------------------------------------
def part_e():
    say("=" * 78)
    say("(E) E5f samples (results/results_realizer_law.json) and frozen results/check_realizer_law_output.txt")
    say("=" * 78)
    d = json.load(open(os.path.join(ROOT, "results", "results_realizer_law.json")))
    say("first-order predictions: P(R=1) = e^-1(1-3/n), P(R=2) = e^-1 + O(n^-2), P(R<=8) = (8/3)e^-1 - (3/2)e^-1/n,"
        " P(R=2^N) = 1-5/n")
    say(" n | samples | unique obs/pred | two obs/pred | <=8 obs/pred | R=2^N obs/pred")
    tot = {k: [0.0, 0.0, 0.0] for k in ("u", "t", "l", "e")}
    for r in d["rows"]:
        n, S = r["n"], r["samples"]
        pred = {"u": E1 * (1 - 3 / n), "t": E1, "l": 8 / 3 * E1 - 1.5 * E1 / n, "e": 1 - 5 / n}
        obs = {"u": r["fraction_unique"], "t": r["fraction_two"], "l": r["fraction_le_eight"],
               "e": r["equal_to_two_pow_N"] / S}
        for k in tot:
            tot[k][0] += obs[k] * S
            tot[k][1] += pred[k] * S
            tot[k][2] += pred[k] * (1 - pred[k]) * S
        say(f" {n:3d} | {S:3d} | {obs['u']:.3f}/{pred['u']:.3f} | {obs['t']:.3f}/{pred['t']:.3f} | "
            f"{obs['l']:.3f}/{pred['l']:.3f} | {obs['e']:.3f}/{pred['e']:.3f}")
    say(" pooled z-scores (obs - pred)/sd: " + ", ".join(
        f"{k}: {(v[0] - v[1]) / math.sqrt(v[2]):+.2f}" for k, v in tot.items()))
    ratios = Counter()
    for r in d["rows"]:
        for e in r["exceptions"]:
            ratios[Fraction(e["count"], 2 ** e["N"])] += 1
    say(" E5f ratios R/2^N among exceptions (all n): " + ", ".join(f"{str(k)}: {v}" for k, v in sorted(ratios.items())))
    path = os.path.join(ROOT, "results", "check_realizer_law_output.txt")
    say(f" frozen {os.path.relpath(path, ROOT)}: share of ratio 3/2 among the ratios {{3/2, 2}} "
        f"(first-order prediction 1/5)")
    s32 = s2 = 0
    cols = None
    with open(path) as fh:
        for line in fh:
            parts = [x.strip() for x in line.split("|")]
            if parts[0] == "n" and "n*P obs" in parts:
                cols = parts
                continue
            if cols and len(parts) == len(cols) and parts[0].isdigit():
                n = int(parts[0])
                rat = dict((a.split(":")[0].strip(), int(a.split(":")[1].split()[0]))
                           for a in parts[-1].split(",") if ":" in a)
                a, b = rat.get("3/2", 0), rat.get("2", 0)
                s32 += a
                s2 += b
                say(f"   n = {n:4d}: n P(R != 2^N) = {parts[cols.index('n*P obs')]}; 3/2: {a}, 2: {b}, "
                    f"share {a / max(1, a + b):.3f}")
    say(f"   pooled: 3/2: {s32}, 2: {s2}, share {s32 / (s32 + s2):.3f} "
        f"(95% CI +- {1.96 * math.sqrt(0.2 * 0.8 / (s32 + s2)):.3f} around 0.2)")


def main():
    t0 = time.time()
    say(f"check_sharp_rate.py  seed={SEED}  python {platform.python_version()}  numpy {np.__version__}")
    part_a()
    part_b()
    part_c()
    part_d()
    part_e()
    say(f"total {time.time() - t0:.1f} s")
    with open(OUT, "w") as fh:
        fh.write("\n".join(_lines) + "\n")


if __name__ == "__main__":
    main()
