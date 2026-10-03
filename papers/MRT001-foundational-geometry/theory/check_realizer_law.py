#!/usr/bin/env python3
"""
Numerical check of the realizer law (Conjecture 5.3 of MRT001 v0.5, proved in
theory/realizer_law_theorem.tex).

Conventions (as in experiments/realizer_law.py): positions = u-ranks, values =
v-ranks, pi uniform in S_n, causal order i < j iff i < j and pi(i) < pi(j),
N = #{i : pi(i+1) = pi(i) - 1} (descending successions), R = number of
realizers modulo the swap.

(a) exact formula R = 1 (identity) or 1/2 * prod over the substitution tree of
    f(node) (simple: 2, skew sum with k children: k!, direct sum: 1), compared with
      - lc.brute_force_realizers_mod_swap (pairs of linear extensions), n <= 6, all pi;
      - an independent brute force over all u-orders, n <= 7, all pi;
      - lc.count_realizers_mod_swap (Golumbic colour classes), n <= 7 all pi, and
        random pi up to n = 120;
    plus: Gallai check (every simple pi, 4 <= n <= 8, has R = 1 and one colour class);
          on the event E_n (no interval of length 3..n-1) R == 2^N always;
          factor table for a single exceptional interval (exhaustive n = 8, 9).
(b) exception rate P(R != 2^N) and P(E_n^c) against n, compared with 5/n and
    with the first-moment bound s_n = sum_{k=3}^{n-1} (n-k+1)^2 / C(n,k).
(c) exact identities: E[(N)_r] = 1 - r/n, law of N, TV bound, bound on s_n.

Usage: python3 check_realizer_law.py      (writes check_realizer_law_output.txt)
"""
import itertools
import math
import os
import sys
import time
from collections import Counter, defaultdict
from fractions import Fraction

import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(os.path.dirname(HERE), "experiments"))
import lorentzian_chain as lc  # noqa: E402

SEED = 20261003
OUT = os.path.join(HERE, "check_realizer_law_output.txt")
_lines = []


def say(*args):
    s = " ".join(str(a) for a in args)
    print(s, flush=True)
    _lines.append(s)


# --------------------------------------------------------------------------
# permutations, orders, successions
# --------------------------------------------------------------------------
def order_matrix(p):
    p = np.asarray(p)
    idx = np.arange(len(p))
    return (idx[:, None] < idx[None, :]) & (p[:, None] < p[None, :])


def n_desc(p):
    p = np.asarray(p)
    return int(np.sum(p[1:] == p[:-1] - 1))


def standardize(vals):
    order = sorted(range(len(vals)), key=lambda i: vals[i])
    out = [0] * len(vals)
    for r, i in enumerate(order):
        out[i] = r
    return out


def proper_interval_ends(p):
    """best[a] = largest b such that p[a..b] is an interval of length < len(p) (a if none)."""
    m = len(p)
    best = list(range(m))
    if m <= 64:
        for a in range(m):
            mx = mn = p[a]
            for b in range(a + 1, m):
                x = p[b]
                if x > mx:
                    mx = x
                elif x < mn:
                    mn = x
                if mx - mn == b - a and b - a + 1 < m:
                    best[a] = b
    else:
        arr = np.asarray(p)
        for a in range(m):
            sub = arr[a:]
            span = np.maximum.accumulate(sub) - np.minimum.accumulate(sub)
            hits = np.nonzero(span == np.arange(len(sub)))[0]
            if a == 0:
                hits = hits[hits < m - 1]
            if len(hits):
                best[a] = a + int(hits[-1])
    return best


def is_simple(s):
    if len(s) <= 2:
        return True
    return all(b == a for a, b in enumerate(proper_interval_ends(s)))


def intervals_of_length(p, lengths):
    """list of (a, b) intervals of p whose length b-a+1 lies in `lengths` (a set)."""
    m = len(p)
    out = []
    for a in range(m):
        mx = mn = p[a]
        for b in range(a + 1, m):
            x = p[b]
            mx = max(mx, x)
            mn = min(mn, x)
            if mx - mn == b - a and (b - a + 1) in lengths:
                out.append((a, b))
    return out


# --------------------------------------------------------------------------
# exact formula by substitution decomposition
# --------------------------------------------------------------------------
STATS = Counter()


def t_formula(p):
    """number of transitive orientations of the incomparability (= permutation) graph
    of p, computed as the product over the substitution decomposition tree:
    simple node -> 2, skew-sum node with k children -> k!, direct-sum node -> 1."""
    m = len(p)
    if m == 1:
        return 1
    cuts, mx = [], -1
    for k in range(m - 1):
        mx = max(mx, p[k])
        if mx == k:
            cuts.append(k + 1)
    if cuts:                                   # direct sum: parallel node
        STATS["sum"] += 1
        prod, lo = 1, 0
        for c in cuts + [m]:
            prod *= t_formula(standardize(p[lo:c]))
            lo = c
        return prod
    cuts, mn = [], m
    for k in range(m - 1):
        mn = min(mn, p[k])
        if mn == m - 1 - k:
            cuts.append(k + 1)
    if cuts:                                   # skew sum: series node with k children
        STATS["skew"] += 1
        prod, lo = math.factorial(len(cuts) + 1), 0
        for c in cuts + [m]:
            prod *= t_formula(standardize(p[lo:c]))
            lo = c
        return prod
    STATS["simple"] += 1                       # inflation of a simple permutation
    best = proper_interval_ends(p)
    blocks, a = [], 0
    while a < m:
        blocks.append((a, best[a]))
        a = best[a] + 1
    for a, b in blocks:
        assert max(p[a:b + 1]) - min(p[a:b + 1]) == b - a, "block is not an interval"
    sigma = standardize([p[a] for a, _ in blocks])
    assert len(sigma) >= 4 and is_simple(sigma), "quotient is not simple"
    prod = 2
    for a, b in blocks:
        if b > a:
            prod *= t_formula(standardize(p[a:b + 1]))
    return prod


def realizers_formula(p):
    p = list(p)
    if all(x == i for i, x in enumerate(p)):
        return 1
    t = t_formula(p)
    assert t % 2 == 0
    return t // 2


# --------------------------------------------------------------------------
# independent brute force over u-orders
# --------------------------------------------------------------------------
_POS_CACHE = {}


def brute_force_uorders(p):
    """Ordered realizers (L1, L2) <-> linear extensions L1 such that the tournament
    L2 = order on comparable pairs + reverse of L1 on incomparable pairs is transitive
    (a tournament is transitive iff its out-degrees are 0..n-1).  Returns the count
    modulo the swap."""
    n = len(p)
    if n not in _POS_CACHE:
        perms = np.array(list(itertools.permutations(range(n))), dtype=np.int8)
        pos = np.empty_like(perms)
        pos[np.arange(len(perms))[:, None], perms] = np.arange(n, dtype=np.int8)
        _POS_CACHE[n] = pos
    pos = _POS_CACHE[n]
    R = order_matrix(p)
    inc = ~(R | R.T)
    np.fill_diagonal(inc, False)
    before = pos[:, :, None] < pos[:, None, :]            # [L, a, b]: a before b in L1
    ext = ~np.any(R[None] & ~before, axis=(1, 2))         # L1 extends the order
    V = R[None] | (inc[None] & ~before)                   # a <_V b
    deg = np.sort(V.sum(axis=2), axis=1)
    trans = np.all(deg == np.arange(n)[None, :], axis=1)
    count = int(np.sum(ext & trans))
    chain = not inc.any()
    return (count + (1 if chain else 0)) // 2


# --------------------------------------------------------------------------
# (a) exact formula versus brute force
# --------------------------------------------------------------------------
def part_a():
    say("=" * 78)
    say("(a) exact formula versus brute force")
    say("=" * 78)
    t0 = time.time()
    for n in range(1, 8):
        tot = mism_bf = mism_u = mism_cc = cc_skip = eq2N = inE = inE_bad = 0
        for p in itertools.permutations(range(n)):
            p = list(p)
            tot += 1
            f = realizers_formula(p)
            if n <= 6:
                mism_bf += int(lc.brute_force_realizers_mod_swap(order_matrix(p)) != f)
            mism_u += int(brute_force_uorders(p) != f)
            if n <= 6:
                c, _ = lc.count_realizers_mod_swap(order_matrix(p), max_classes=12)
                if c is None:
                    cc_skip += 1
                else:
                    mism_cc += int(c != f)
            N = n_desc(p)
            eq2N += int(f == 2 ** N)
            if n >= 5 and not intervals_of_length(p, set(range(3, n))):
                inE += 1
                inE_bad += int(f != 2 ** N)
        bf = f"{mism_bf}" if n <= 6 else "-"
        cc = f"{mism_cc} ({cc_skip} skipped, >12 classes)" if n <= 6 else "- (see random n >= 10 below)"
        say(f"n={n}: {tot} perms | mismatches formula vs lc.brute_force: {bf}, vs u-order brute force: "
            f"{mism_u}, vs colour classes: {cc} | "
            f"R == 2^N in {eq2N}/{tot} | in E_n: {inE}, of which R != 2^N: {inE_bad}")
    say(f"  ({time.time() - t0:.1f} s)")

    # Gallai check on simple permutations
    t0 = time.time()
    for n in range(4, 9):
        n_simple = bad = multi = 0
        for p in itertools.permutations(range(n)):
            if not is_simple(p):
                continue
            n_simple += 1
            R = order_matrix(p)
            k = len(lc.implication_colour_classes(R))
            c, _ = lc.count_realizers_mod_swap(R)
            bad += int(c != 1)
            multi += int(k != 1)
        say(f"Gallai check n={n}: {n_simple} simple permutations (A111111: 2, 6, 46, 338, 2926); "
            f"R != 1 in {bad}; colour classes != 1 in {multi}")
    say(f"  ({time.time() - t0:.1f} s)")

    # random permutations, larger n, versus colour classes
    t0 = time.time()
    rng = np.random.default_rng(SEED)
    for n, reps in [(10, 300), (15, 300), (20, 300), (30, 200), (50, 150), (80, 80), (120, 40)]:
        mism = skip = neq = 0
        for _ in range(reps):
            p = list(rng.permutation(n))
            f = realizers_formula(p)
            c, _ = lc.count_realizers_mod_swap(order_matrix(p), max_classes=11)
            if c is None:
                skip += 1
                continue
            mism += int(c != f)
            neq += int(f != 2 ** n_desc(p))
        say(f"random n={n}: {reps} perms, mismatches formula vs colour classes: {mism} "
            f"({skip} skipped, >11 classes); R != 2^N in {neq}")
    say(f"  ({time.time() - t0:.1f} s)")

    # factor table for a single exceptional interval
    t0 = time.time()
    for n, exhaustive in [(8, True), (9, False)]:
        table = defaultdict(Counter)
        rng9 = np.random.default_rng(SEED + n)
        it = itertools.permutations(range(n)) if exhaustive else \
            (list(rng9.permutation(n)) for _ in range(60000))
        for p in it:
            p = list(p)
            J = intervals_of_length(p, set(range(3, n)))
            if len(J) != 1:
                continue
            a, b = J[0]
            if b - a + 1 == 3:
                key = "len3 " + "".join(str(x + 1) for x in standardize(p[a:b + 1]))
            elif b - a + 1 == n - 1:
                key = ("pi(1)=" + ("1" if p[0] == 0 else "n")) if a == 1 else \
                      ("pi(n)=" + ("1" if p[-1] == 0 else "n"))
            else:
                key = f"len{b - a + 1}"
            table[key][Fraction(realizers_formula(p), 2 ** n_desc(p))] += 1
        say(f"single interval of length in [3, n-1], n={n} ({'exhaustive' if exhaustive else '60000 random'}): "
            "ratio R/2^N -> frequency")
        for key in sorted(table):
            say(f"   {key:10s}: " + ", ".join(f"{str(r)}: {c}" for r, c in sorted(table[key].items())))
    say(f"  ({time.time() - t0:.1f} s)")


# --------------------------------------------------------------------------
# (b) exception rates against n
# --------------------------------------------------------------------------
def EI(n, k):
    return math.exp(2 * math.log(n - k + 1) + math.lgamma(k + 1) + math.lgamma(n - k + 1) - math.lgamma(n + 1))


def s_n(n, lo=3, hi=None):
    hi = n - 1 if hi is None else hi
    return sum(EI(n, k) for k in range(lo, hi + 1))


def flag_batch(P, n, K):
    """flag[i] = permutation P[i] has an interval with length in [3, K] or [n-K, n-1]."""
    flag = np.zeros(P.shape[0], dtype=bool)
    mx, mn = P.copy(), P.copy()
    for w in range(2, K + 1):
        mx = np.maximum(mx[:, :-1], P[:, w - 1:])
        mn = np.minimum(mn[:, :-1], P[:, w - 1:])
        if w >= 3:
            flag |= np.any(mx - mn == w - 1, axis=1)
    for j in range(1, K + 1):
        L = n - j
        if L <= K:
            continue
        for a in range(j + 1):
            sub = P[:, a:a + L]
            flag |= (sub.max(axis=1) - sub.min(axis=1)) == L - 1
    return flag


def part_b():
    say("=" * 78)
    say("(b) exception rate against n  (R computed by the exact formula of (a) on flagged samples)")
    say("=" * 78)
    rng = np.random.default_rng(SEED + 1)
    say("n | samples | P(E_n^c) obs | s_n bound | P(R!=2^N) obs (95% CI) | 5/n | 3(n-2)/(n(n-1))+2/n | "
        "n*P obs | missed-interval bound | ratios R/2^N among exceptions")
    plan = [(20, 20000), (50, 20000), (100, 20000), (200, 20000), (500, 20000), (1000, 20000), (2000, 10000)]
    for n, S in plan:
        t0 = time.time()
        K = n - 1 if n <= 200 else 8
        missed = 0.0 if K == n - 1 else s_n(n, K + 1, n - K - 1)
        flagged = exc = 0
        ratios = Counter()
        B = max(1, min(2000, 4_000_000 // n))
        done = 0
        while done < S:
            b = min(B, S - done)
            P = np.argsort(rng.random((b, n)), axis=1).astype(np.int32)
            F = flag_batch(P, n, K)
            for i in np.nonzero(F)[0]:
                p = P[i].tolist()
                r = realizers_formula(p)
                N = n_desc(p)
                if r != 2 ** N:
                    exc += 1
                    ratios[Fraction(r, 2 ** N)] += 1
            flagged += int(F.sum())
            done += b
        ph = exc / S
        ci = 1.96 * math.sqrt(max(ph * (1 - ph), 1e-12) / S)
        first = 3 * (n - 2) / (n * (n - 1)) + 2 / n
        rs = ", ".join(f"{str(r)}: {c}" for r, c in sorted(ratios.items()))
        say(f"{n} | {S} | {flagged / S:.4f} | {s_n(n):.4f} | {ph:.4f} ({ph - ci:.4f}, {ph + ci:.4f}) | "
            f"{5 / n:.4f} | {first:.4f} | {n * ph:.2f} | {missed:.1e} | {rs}   ({time.time() - t0:.1f} s)")


# --------------------------------------------------------------------------
# (c) exact identities and analytic bounds
# --------------------------------------------------------------------------
def law_N_exact(n):
    return [sum(Fraction((-1) ** s, math.factorial(j) * math.factorial(s)) * (1 - Fraction(j + s, n))
                for s in range(0, n - j)) for j in range(n)]


def part_c():
    say("=" * 78)
    say("(c) exact identities and analytic bounds")
    say("=" * 78)
    for n in range(2, 9):
        Ns = [n_desc(p) for p in itertools.permutations(range(n))]
        tot = len(Ns)
        fm_ok = all(Fraction(sum(math.perm(N, r) for N in Ns), tot) == 1 - Fraction(r, n) for r in range(n))
        law = law_N_exact(n)
        cnt = Counter(Ns)
        law_ok = all(Fraction(cnt.get(j, 0), tot) == law[j] for j in range(n))
        exc = sum(1 for p in itertools.permutations(range(n)) if realizers_formula(p) != 2 ** n_desc(p))
        say(f"n={n}: E[(N)_r] = 1 - r/n for all r: {fm_ok}; inclusion-exclusion law of N exact: {law_ok}; "
            f"exact P(R != 2^N) = {exc}/{tot} = {exc / tot:.4f} (n*P = {n * exc / tot:.2f})")
    worst_tv = 0.0
    for n in list(range(5, 61)) + [100, 200, 400]:
        law = [float(x) for x in law_N_exact(n)]
        pois = [math.exp(-1 - math.lgamma(j + 1)) for j in range(n)]
        tv = 0.5 * (sum(abs(a - b) for a, b in zip(law, pois)) + max(0.0, 1 - sum(pois)))
        bound = math.e ** 2 / n + math.exp(math.log(2 ** n + 1) - math.log(2) - math.lgamma(n + 1))
        worst_tv = max(worst_tv, tv / bound)
        if n in (10, 20, 50, 100, 200, 400):
            say(f"n={n}: d_TV(N, Po(1)) = {tv:.2e}  (n*d_TV = {n * tv:.3f});  bound e^2/n + ... = {bound:.2e}")
    say(f"max over tested n of d_TV / bound = {worst_tv:.3f} (must be <= 1)")
    worst = max(s_n(n) / (10 / n + 171 / n ** 2) for n in range(20, 3001))
    say(f"s_n <= 10/n + 171/n^2 for 20 <= n <= 3000: max ratio = {worst:.4f} (must be <= 1); "
        f"n*s_n at n=20, 100, 1000, 3000: " + ", ".join(f"{n * s_n(n):.3f}" for n in (20, 100, 1000, 3000)))
    say(f"P(E^c_n) - first order 10/n: n^2*(s_n - 10/n) at n=100, 1000, 3000: " +
        ", ".join(f"{n * n * (s_n(n) - 10 / n):.1f}" for n in (100, 1000, 3000)))


def main():
    t_all = time.time()
    say(f"check_realizer_law.py  seed={SEED}  python {sys.version.split()[0]}  numpy {np.__version__}")
    part_a()
    part_c()
    part_b()
    say(f"node counts in the substitution trees evaluated: {dict(STATS)}")
    say(f"total {time.time() - t_all:.1f} s")
    with open(OUT, "w") as fh:
        fh.write("\n".join(_lines) + "\n")


if __name__ == "__main__":
    main()
