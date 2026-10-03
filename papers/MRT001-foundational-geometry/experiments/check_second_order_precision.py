#!/usr/bin/env python3
"""High-precision check of Theorem 5.11(ii) and of the range of Proposition 5.13 (v0.9, round 6).

Round 6 of the internal review (m4) observed that theory/check_second_order.py evaluates
d_TV(N_n, Po(1-1/n)) with 150 digits, which resolves the bound (2^{n+1}-n-2)/(n(n+1)!) of
Theorem 5.11(ii) only for n <~ 95.  This script, written for the paper (it imports nothing from
theory/), redoes that check for EVERY 3 <= n <= NMAX with a working precision chosen per n,

    mp.dps = ceil(log10((n+1)!)) + 30,

so that the rounding error of d_TV is below 10^-25 times the bound.  It also records where the
positive part of p_k - q~_k is supported (round 6, m8) and evaluates the explicit function B(n) of
Proposition 5.13 from n = 14 on (round 6, m7).  Deterministic: no random numbers.

Parts
  P1  exact law of N_n (number of i with pi(i+1) = pi(i)-1) for n <= NMAX in integers, two ways:
      Kaplansky's closed form binom(n-1,k)(D_{n-k}+D_{n-k-1}) and the recurrence obtained by
      inserting n into a permutation of [n-1]; brute force over S_n for n <= 8; factorial moments
      E[(N_n)_r] = 1 - r/n exactly for n <= 100.
  P2  Theorem 5.8(i): max |r_{n,k}| n k! (n-k+1)! over 1 <= n <= NMAX, 0 <= k <= n-1 (claim <= 1).
  P3  Theorem 5.11(ii): max |d_TV - Phi(1/n)| / bound over 3 <= n <= NMAX (claim <= 1); the sets
      {k : p_k > q~_k}; Theorem 5.11(iii): theta_n = 48 e n^2 (n^2 Phi(1/n) - 3/(4e) - 1/(4en)).
  P4  Proposition 5.13: n^2 B(n) for 14 <= n <= NB, monotonicity, values, limit 259 + 10/e.

Writes results/check_second_order_precision_output.txt (no timing lines), its .sha256,
results/check_second_order_precision.json and results/check_second_order_precision_meta.json
(SHA-256 of both files and CPU seconds).  make_numbers.py verifies both SHA-256.
"""
import hashlib
import itertools
import json
import math
import os
import platform
import sys
import time

import mpmath
from mpmath import mp, mpf

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
NMAX = int(os.environ.get("NMAX_TEST", 1000))      # Theorem 5.11(ii) is checked for every 3 <= n <= NMAX
NB = 5000        # n^2 B(n) is evaluated for 14 <= n <= NB
NBRUTE = 8
NMOM = 100

t0 = time.process_time()
out = []


def say(s=""):
    out.append(s)
    print(s, flush=True)


# ---------------------------------------------------------------------------------------------
say("=" * 78)
say("(P1) exact law of N_n, 1 <= n <= %d" % NMAX)
say("=" * 78)
D = [1, 0]                                    # derangement numbers D_0, D_1, ...
for m in range(2, NMAX + 2):
    D.append((m - 1) * (D[-1] + D[-2]))
fact = [1]
for m in range(1, NMAX + 3):
    fact.append(fact[-1] * m)


def closed(n):
    return [math.comb(n - 1, k) * (D[n - k] + D[n - k - 1]) for k in range(n)]


law = {1: [1]}
prev = [1]
ok_rec = True
for n in range(2, NMAX + 1):
    cur = [0] * n
    for k in range(n):
        v = (n - 1 - k) * prev[k] if k < len(prev) else 0      # n placed in a gap that changes nothing
        if 1 <= k <= len(prev):
            v += prev[k - 1]                                       # n placed just before n-1: +1
        if k + 1 < len(prev):
            v += (k + 1) * prev[k + 1]                             # n placed inside a succession: -1
        cur[k] = v
    law[n] = cur
    prev = cur
    if cur != closed(n) or sum(cur) != fact[n]:
        ok_rec = False
ok_closed1 = closed(1) == law[1]
say(f"P1 insertion recurrence = Kaplansky closed form binom(n-1,k)(D_(n-k)+D_(n-k-1)) for all n<={NMAX}: "
    f"{ok_rec and ok_closed1}")
ok_bf = True
for n in range(1, NBRUTE + 1):
    cnt = [0] * n
    for p in itertools.permutations(range(n)):
        cnt[sum(1 for i in range(n - 1) if p[i + 1] == p[i] - 1)] += 1
    ok_bf &= cnt == law[n]
say(f"P1 = brute force over S_n for n<={NBRUTE}: {ok_bf}")
mism = 0
for n in range(1, NMOM + 1):
    for r in range(n):
        if sum(law[n][k] * math.perm(k, r) for k in range(r, n)) != (n - r) * fact[n - 1]:
            mism += 1
say(f"P1 E[(N_n)_r] = 1 - r/n for all 0<=r<=n-1, n<={NMOM} (integers): mismatches = {mism}")

# ---------------------------------------------------------------------------------------------
say("=" * 78)
say("(P2, P3) Theorems 5.8(i) and 5.11(ii)-(iii), every n with mp.dps = ceil(log10((n+1)!)) + 30")
say("=" * 78)


def Phi(x):
    return mpf(1) / 2 * mp.exp(-1) * (3 - x) * (1 - (1 - x) * mp.exp(x))


r_max = (mpf(0), None)
s1_max = (mpf(0), None)
theta_lo, theta_hi = None, None
pos_exc = []
sign_margin = None
digits_lo, digits_hi = None, None
rows = {}
for n in range(1, NMAX + 1):
    dps = math.ceil(math.log10(fact[n + 1])) + 30
    mp.dps = dps
    if n >= 3:
        digits_lo = dps if digits_lo is None else min(digits_lo, dps)
        digits_hi = dps if digits_hi is None else max(digits_hi, dps)
    nf = mpf(fact[n])
    x = mpf(1) / n
    lam = 1 - x
    q = mp.exp(-1)                 # q_k = e^-1/k!
    qt = mp.exp(-lam)              # q~_k = e^-lam lam^k/k!
    dtv = mpf(0)
    pos = []
    marg = None
    scale = mpf(10) ** dps / n                    # converts |p_k - q~_k| into units of n 10^-dps
    for k in range(n):
        if k > 0:
            q = q / k
            qt = qt * lam / k
        pk = mpf(law[n][k]) / nf
        # Theorem 5.8(i): r_{n,k} = p_k - q_k (1 - (k-1)/n), |r| <= 1/(n k! (n-k+1)!)
        r = pk - q * (1 - mpf(k - 1) / n)
        rr = abs(r) * n * fact[k] * fact[n - k + 1]
        if rr > r_max[0]:
            r_max = (rr, n)
        if n >= 3:
            d = pk - qt
            if d > 0:
                dtv += d
                pos.append(k)
            m_ = abs(d) * scale
            marg = m_ if marg is None else min(marg, m_)
    if n < 3:
        continue
    sign_margin = marg if sign_margin is None else min(sign_margin, marg)
    if pos != [1, 2]:
        pos_exc.append((n, pos))
    bound = mpf(2 ** (n + 1) - n - 2) / (n * mpf(fact[n + 1]))
    eps = dtv - Phi(x)
    ratio = abs(eps) / bound
    if ratio > s1_max[0]:
        s1_max = (ratio, n)
    th = 48 * mp.e * n ** 2 * (n ** 2 * Phi(x) - 3 / (4 * mp.e) - 1 / (4 * mp.e * n))
    theta_lo = th if theta_lo is None else min(theta_lo, th)
    theta_hi = th if theta_hi is None else max(theta_hi, th)
    rows[n] = (dtv, eps, bound, ratio, dps)

mp.dps = 30
say(f"P2 max |r_nk| n k! (n-k+1)! over 1<=n<={NMAX}, 0<=k<=n-1: {mpmath.nstr(r_max[0], 6)} at n={r_max[1]} (claim <= 1)")
say(f"P3 working precision: {digits_lo} to {digits_hi} digits (n=3 to n={NMAX})")
say(f"P3 max |d_TV(N_n,Po(1-1/n)) - Phi(1/n)| / bound over 3<=n<={NMAX}: {mpmath.nstr(s1_max[0], 6)} "
    f"at n={s1_max[1]} (claim <= 1)")
say(f"P3 smallest |p_k - q~_k| in units of n 10^-dps (signs resolved if >> 1): 10^{int(mpmath.floor(mpmath.log10(sign_margin)))}")
say(f"P3 n with {{k: p_k > q~_k}} != {{1,2}}, 3<=n<={NMAX} (not needed by the theorem): {pos_exc}")
say(f"P3 theta_n over 3<=n<={NMAX}: [{mpmath.nstr(theta_lo, 7)}, {mpmath.nstr(theta_hi, 7)}] (claim (0,1])")
say("    n   digits     d_TV(N_n,Po(1-1/n))   |d_TV-Phi(1/n)|          bound      ratio")
for n in [v for v in (3, 4, 5, 6, 10, 20, 50, 95, 100, 150, 200, 300, 500, 700, 1000) if v <= NMAX]:
    dtv, eps, bound, ratio, dps = rows[n]
    say(f"{n:5d} {dps:8d}  {mpmath.nstr(dtv, 15):>22}  {mpmath.nstr(abs(eps), 4):>14}  "
        f"{mpmath.nstr(bound, 4):>12}  {mpmath.nstr(ratio, 6):>9}")

# ---------------------------------------------------------------------------------------------
say("=" * 78)
say(f"(P4) Proposition 5.13: n^2 B(n), 14 <= n <= {NB}, B(n) as in equation (2)")
say("=" * 78)
mp.dps = 50
E1 = mp.exp(-1)


def ff(m, j):
    v = mpf(1)
    for i in range(j):
        v *= (m - i)
    return v


def Fbar(m):
    return 42 / ff(m, 2) + 936 / ff(m, 3) + 600 / ff(m, 4) + 4320 / ff(m, 5)


def Pbar(n):
    return 90 / ff(n, 2) + 944 / ff(n, 3) + 600 / ff(n, 4) + 4320 / ff(n, 5)


def sbar(m):
    return mpf(10) / m + Fbar(m)


def hbar(m):
    return mpf(8) / m + 18 / ff(m, 2) + Fbar(m)


def dbar(m):
    return E1 / m + 2 / (m * mp.factorial(m))


def B(n):
    w3 = 3 * mpf(n - 2) / ff(n, 2)
    return (mpf(2) ** (n + 1) / (n * mp.factorial(n + 1)) + 1 / mp.factorial(n) + Pbar(n)
            + w3 * (sbar(n - 2) + 3 * hbar(n - 2)) + 12 / ff(n, 2) + mpf(2) / n * (sbar(n - 1) + hbar(n - 1))
            + w3 * (mpf(4) / (n - 2) + 2 * dbar(n - 2)) + mpf(2) / n * (mpf(2) / (n - 1) + 2 * dbar(n - 1))
            + 3 / ff(n, 2))


vals = {n: n * n * B(n) for n in range(14, NB + 1)}
mono = all(vals[n + 1] <= vals[n] for n in range(14, NB))
limit = 259 + 10 / mp.e
say(f"P4 n^2 B(n) non-increasing on 14<=n<={NB}: {mono}")
say("   n0 -> n0^2 B(n0): " + ", ".join(f"{n}: {mpmath.nstr(vals[n], 7)}" for n in (14, 16, 18, 20, 21, 22, 30, 100, 1000)))
say(f"   n^2 B(n) at n={NB}: {mpmath.nstr(vals[NB], 8)}; limit 259 + 10/e = {mpmath.nstr(limit, 8)}")
cpu = time.process_time() - t0

# ---------------------------------------------------------------------------------------------
# consistency with the frozen second-order check (values only; nothing is imported from theory/)
so = json.load(open(os.path.join(ROOT, "results", "second_order_results.json")))
agree = all(abs(float(vals[int(k)]) - v) < 1e-6 for k, v in so["C_table"].items() if int(k) <= NB)
say(f"P4 n^2 B(n) at n in {sorted(int(k) for k in so['C_table'])} agrees with results/second_order_results.json (C_table): {agree}")
agree_s1 = abs(float(s1_max[0]) - so["S1_maxratio"]) < 1e-9
say(f"P3 max ratio agrees with S1_maxratio of results/second_order_results.json (n<=80): {agree_s1}")

res = {
    "NMAX": NMAX, "NB": NB, "law_recurrence_eq_closed_form": ok_rec and ok_closed1, "law_eq_bruteforce": ok_bf,
    "factorial_moment_mismatches": mism, "digits_lo": digits_lo, "digits_hi": digits_hi,
    "r_max": float(r_max[0]), "r_max_n": r_max[1],
    "S1_maxratio_all": float(s1_max[0]), "S1_maxratio_n": s1_max[1],
    "sign_margin_log10": int(mpmath.floor(mpmath.log10(sign_margin))),
    "pos_exceptions": pos_exc, "theta_lo": float(theta_lo), "theta_hi": float(theta_hi),
    "B_monotone_from_14": mono, "n2B": {str(n): float(vals[n]) for n in (14, 16, 18, 20, 21, 22, 30, 100, 1000, NB)},
    "B_limit": float(limit), "C_table_agrees": agree, "S1_agrees": agree_s1,
}
ok = (ok_rec and ok_closed1 and ok_bf and mism == 0 and r_max[0] <= 1 and s1_max[0] <= 1 and mono and agree
      and agree_s1 and theta_lo > 0 and theta_hi <= 1)
say(f"ALL CHECKS PASSED: {ok}")
txt = "\n".join(out) + "\n"
jtxt = json.dumps(res, indent=1, sort_keys=True) + "\n"
rdir = os.path.join(ROOT, "results")
open(os.path.join(rdir, "check_second_order_precision_output.txt"), "w").write(txt)
open(os.path.join(rdir, "check_second_order_precision.json"), "w").write(jtxt)
sha = hashlib.sha256(txt.encode()).hexdigest()
sha_j = hashlib.sha256(jtxt.encode()).hexdigest()
open(os.path.join(rdir, "check_second_order_precision_output.sha256"), "w").write(
    f"{sha}  check_second_order_precision_output.txt\n")
meta = {"script": "experiments/check_second_order_precision.py", "deterministic": True,
        "seconds": round(cpu, 1), "cpu": "one core", "sha256_output": sha, "sha256_json": sha_j,
        "python": platform.python_version(), "mpmath": mpmath.__version__}
json.dump(meta, open(os.path.join(rdir, "check_second_order_precision_meta.json"), "w"), indent=1)
print(f"total CPU time: {cpu:.1f} s")
sys.exit(0 if ok else 1)
