#!/usr/bin/env python3
"""
TCD001 v0.5 -- exact check of Theorem 5.1(c): for p = 1 the signed fragility number f_any^signed is
computable by sorting (referee round 3, M2).

For p = 1, with a_i = x_i y_i, T = sum_i a_i and mu_k the subsample penalty (rule C: mu; rule P:
mu (n-k)/n), the Lasso on D \\ R has the unique minimiser
    beta = sgn(A) (|A| - mu_k)_+ / ||x_K||^2,   A = sum_{i not in R} a_i
(unique also when x_K = 0: then the objective is constant + mu_k |beta|).  Hence
  * if |T| > mu (selected with sign s = sgn T), R is a signed-ANY witness iff s * A <= mu_{|R|}; for |R| = k
    the minimum of s * A is s*T - (sum of the k largest values of s * a_i), so a witness of size k exists iff
        s*T - sigma_k^{(s)} <= mu_k ;
  * if |T| <= mu (not selected), a witness is a selection witness (Theorem 5.1(b)):
        T - sigma_k^- > mu_k  or  T - sigma_k^+ < -mu_k .
The script compares this O(n log n) rule with brute force over all nonempty proper R, in exact rational
arithmetic (Fractions), on random instances with ties and zeros, under both rules.
Deterministic (seed 20261003).  Output: results/signed_any_p1.json (+ printed summary).
"""
from __future__ import annotations

import itertools
import json
import os
import random
import sys
import time
from fractions import Fraction as F

HERE = os.path.dirname(os.path.abspath(__file__))
RES = os.path.join(HERE, "..", "results")


def mu_k(mu, n, k, rule):
    return mu if rule == "C" else mu * F(n - k, n)


def brute(x, y, mu, rule):
    """f_any^signed by enumeration, exact."""
    n = len(x)
    a = [xi * yi for xi, yi in zip(x, y)]

    def signed_support(A, m):
        return 0 if abs(A) <= m else (1 if A > 0 else -1)

    s0 = signed_support(sum(a), mu)
    for k in range(1, n):
        mk = mu_k(mu, n, k, rule)
        for R in itertools.combinations(range(n), k):
            A = sum(a[i] for i in range(n) if i not in R)
            if signed_support(A, mk) != s0:
                return k
    return None


def by_sorting(x, y, mu, rule):
    """f_any^signed by Theorem 5.1(b),(c): one sort, prefix sums."""
    n = len(x)
    a = [xi * yi for xi, yi in zip(x, y)]
    T = sum(a)
    if abs(T) > mu:
        s = 1 if T > 0 else -1
        v = sorted((s * ai for ai in a), reverse=True)
        acc = F(0)
        for k in range(1, n):
            acc += v[k - 1]
            if s * T - acc <= mu_k(mu, n, k, rule):
                return k
        return None
    v = sorted(a)
    lo = hi = F(0)  # sums of the k smallest / k largest
    for k in range(1, n):
        lo += v[k - 1]
        hi += v[n - k]
        mk = mu_k(mu, n, k, rule)
        if T - lo > mk or T - hi < -mk:
            return k
    return None


def main():
    t0 = time.process_time()
    rng = random.Random(20261003)
    stats = dict(instances=0, agree=0, selected=0, not_selected=0, finite=0, rule_C=0, rule_P=0,
                 differs_from_unsigned_leave=0)
    for trial in range(2400):
        n = rng.randint(2, 10)
        M = rng.choice([1, 2, 3, 5])
        x = [F(rng.randint(-M, M)) for _ in range(n)]
        y = [F(rng.randint(-M, M)) for _ in range(n)]
        mu = F(rng.randint(1, 4 * M), rng.choice([1, 2, 3]))
        rule = "C" if trial % 2 == 0 else "P"
        fb = brute(x, y, mu, rule)
        fs = by_sorting(x, y, mu, rule)
        stats["instances"] += 1
        stats["agree"] += fb == fs
        stats[f"rule_{rule}"] += 1
        T = sum(xi * yi for xi, yi in zip(x, y))
        stats["selected" if abs(T) > mu else "not_selected"] += 1
        stats["finite"] += fb is not None
        if fb != fs:
            print("DISAGREEMENT", x, y, mu, rule, fb, fs)
    cpu = time.process_time() - t0
    stats["cpu_seconds"] = round(cpu, 1)
    stats["seed"] = 20261003
    stats["python"] = sys.version.split()[0]
    del stats["differs_from_unsigned_leave"]
    print(f"Theorem 5.1(c), p = 1: sorting rule = brute force on {stats['agree']}/{stats['instances']} instances"
          f" ({stats['selected']} selected, {stats['not_selected']} not selected on D; {stats['finite']} with finite f;"
          f" rules C/P {stats['rule_C']}/{stats['rule_P']}); CPU {cpu:.1f} s")
    os.makedirs(RES, exist_ok=True)
    with open(os.path.join(RES, "signed_any_p1.json"), "w") as fh:
        json.dump(stats, fh, indent=1)


if __name__ == "__main__":
    main()
