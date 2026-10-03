"""check_second_order.py -- numerical verification of theory/second_order.tex (MRT001).

Parts
  (A) law of N_n against Po(1-1/n): exact rational law (closed form, factorial-moment inversion,
      brute force), Theorem S1 (closed form of d_TV, bound on the remainder), the expansion
      3/(4e) + 1/(4en) + theta/(48 e n^2), the sign lemma, the factorial moments, and the best
      Poisson (Theorem S2): n^2 min_lambda d_TV -> 1/(2e) at lambda = 1 - 1/n + 1/(2n^2).
  (B) simple permutations s_m from the compositional inverse of sum n! z^n (ODE recurrence),
      checked against brute force and the known initial values.
  (C) exact law of R_n on the atoms 2^k and 3*2^k from the substitution decomposition
      (generating function in z, y = log2 t, w = factor 3), in exact integer arithmetic for
      n <= NEXACT and in scaled floating point for n <= NFLOAT; checked against brute force
      (n <= 8) and exact-versus-float.
  (D) d_TV(R_n, 2^Z) exactly (up to float rounding) for n <= NFLOAT: first-order constant
      c_2 = 1 + 1/(2e), atoms against mu, the explicit constant of Proposition S3 over the whole
      range, and extrapolated second-order coefficients (numerical only).
  (E) the explicit bound B(n) of Proposition S3 and the inequalities used in its proof.

Deterministic (no random numbers).  Writes theory/check_second_order_output.txt and
theory/second_order_results.json.
"""
import itertools
import json
import math
import os
import sys
import time
from collections import Counter
from fractions import Fraction

import numpy as np
import mpmath as mp

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
sys.dont_write_bytecode = True
import check_realizer_law as crl  # noqa: E402  (read-only reuse: realizers_formula, brute_force_uorders, is_simple)

OUT = os.path.join(HERE, "check_second_order_output.txt")
JSON_OUT = os.path.join(HERE, "second_order_results.json")
NEXACT = 30
NFLOAT = int(os.environ.get("NFLOAT", "600"))
KY = 20            # y-truncation: t = 2^a 3^b with a < KY
_lines = []
RES = {}
T0 = time.process_time()


def say(*args):
    s = " ".join(str(a) for a in args)
    print(s, flush=True)
    _lines.append(s)


E = math.e
C2 = 1 + 1 / (2 * E)


# =============================================================================
# (A) law of N_n
# =============================================================================
def derangements(nmax):
    D = [1, 0]
    for m in range(2, nmax + 1):
        D.append((m - 1) * (D[-1] + D[-2]))
    return D


DER = derangements(1100)


def law_closed(n):
    """P(N_n = k) = C(n-1,k)(D_{n-k}+D_{n-k-1})/n!, k = 0..n-1 (exact)."""
    f = math.factorial(n)
    return [Fraction(math.comb(n - 1, k) * (DER[n - k] + DER[n - k - 1]), f) for k in range(n)]


def law_moments(n):
    return [sum(Fraction((-1) ** s, math.factorial(s)) * (1 - Fraction(k + s, n))
                for s in range(n - k)) / math.factorial(k) for k in range(n)]


def law_brute(n):
    c = Counter(sum(1 for i in range(n - 1) if p[i + 1] == p[i] - 1)
                for p in itertools.permutations(range(n)))
    f = math.factorial(n)
    return [Fraction(c.get(k, 0), f) for k in range(n)]


def Dclosed(x):
    return mp.e ** -1 / 2 * (3 - x) * (1 - (1 - x) * mp.e ** x)


def d_coef(j):
    return Fraction(-j * j + 5 * j - 3, 2 * math.factorial(j))


def part_a():
    say("=" * 78)
    say("(A) law of N_n versus Po(1-1/n)")
    say("=" * 78)
    mp.mp.dps = 60
    # A1: three exact laws
    for n in range(1, 9):
        assert law_closed(n) == law_moments(n) == law_brute(n), n
    for n in range(9, 61):
        assert law_closed(n) == law_moments(n), n
    say("A1 closed form = factorial-moment inversion for n<=60, = brute force for n<=8: OK")
    # A2: factorial moments
    bad = 0
    for n in range(1, 61):
        L = law_closed(n)
        for r in range(n):
            m = sum(p * math.perm(k, r) for k, p in enumerate(L))
            bad += (m != 1 - Fraction(r, n))
    say(f"A2 E[(N_n)_r] = 1 - r/n for all 0<=r<=n-1, n<=60 (exact): mismatches = {bad}")
    pis = [mp.e ** -1 / mp.factorial(k) for k in range(80)]
    nu = [pis[k] - (pis[k - 1] if k else 0) for k in range(80)]
    worst = max(abs(sum(nu[k] * mp.ff(k, r) for k in range(80)) + r) for r in range(0, 12))
    say(f"A2 sum_k nu(k)(k)_r = -r for r<=11: max error {mp.nstr(worst, 3)}")
    # A3: sign lemma on a grid and at x = 1/n
    nviol = 0
    for x in [mp.mpf(i) / 1000 for i in range(1, 500)]:
        h = [mp.e ** x * (1 - x) ** k - 1 - (1 - k) * x for k in range(0, 60)]
        nviol += (not (h[0] > 0 and h[1] < 0 and h[2] < 0 and all(v > 0 for v in h[3:])))
    say(f"A3 sign lemma (h_0>0, h_1<0, h_2<0, h_k>0 for 3<=k<60) on x=0.001..0.499: violations = {nviol}")
    # A4: Theorem S1 and its corollary
    mp.mp.dps = 150
    NS = list(range(3, 61)) + [70, 80, 100, 150, 200, 300, 400, 500, 700, 1000]
    rows, maxratio, th_lo, th_hi, sign_bad = [], 0, mp.mpf(10), mp.mpf(-10), []
    for n in NS:
        L = law_closed(n)
        x = mp.mpf(1) / n
        lam = 1 - x
        q = [mp.e ** (-lam) * lam ** k / mp.factorial(k) for k in range(n)]
        diffs = [mp.mpf(L[k].numerator) / L[k].denominator - q[k] for k in range(n)]
        dtv = sum(d for d in diffs if d > 0)
        pos = [k for k, d in enumerate(diffs) if d > 0]
        if pos != [1, 2]:
            sign_bad.append((n, pos))
        Dn = Dclosed(x)
        bound = mp.mpf(2 ** (n + 1) - n - 2) / (n * mp.factorial(n + 1))
        err = abs(dtv - Dn)
        if bound > mp.mpf(10) ** -130:
            maxratio = max(maxratio, err / bound)
            nmax_ratio = n
        else:
            assert err < mp.mpf(10) ** -130
        theta = (n * n * Dn - 3 / (4 * mp.e) - 1 / (4 * mp.e * n)) * 48 * mp.e * n * n
        th_lo, th_hi = min(th_lo, theta), max(th_hi, theta)
        rows.append((n, dtv, n * n * dtv, err, bound, theta))
    say("A4 Theorem S1: d_TV(N_n,Po(1-1/n)) = D(1/n) + eps_n, |eps_n| <= (2^{n+1}-n-2)/(n(n+1)!)")
    say(f"   n in 3..60 and {NS[58:]}; max |d_TV - D(1/n)|/bound over n<={nmax_ratio} (bound > 1e-130) = {mp.nstr(maxratio, 6)}")
    say(f"   (larger n: bound <= 1e-130 and |d_TV - D(1/n)| < 1e-130, computed with 150 digits)")
    say(f"   n where {{k: p_k > q_k}} != {{1,2}} (not needed by the theorem): {sign_bad}")
    say(f"   theta_n = 48 e n^2 (n^2 D(1/n) - 3/(4e) - 1/(4en)) in [{mp.nstr(th_lo, 8)}, {mp.nstr(th_hi, 8)}] (claim: (0,1])")
    say("    n      d_TV(N_n,Po(1-1/n))     n^2 d_TV        |d_TV-D(1/n)|   bound")
    for (n, dtv, nd, err, bound, theta) in rows:
        if n in (3, 4, 5, 6, 8, 10, 15, 20, 30, 40, 60, 100, 200, 500, 1000):
            say(f"   {n:4d}  {mp.nstr(dtv, 14):>22}  {mp.nstr(nd, 12):>14}  {mp.nstr(err, 3):>12}  {mp.nstr(bound, 3):>10}")
    say(f"   3/(4e) = {mp.nstr(3 / (4 * mp.e), 12)}; 3/(4e)+1/(4000e) = {mp.nstr(3 / (4 * mp.e) + 1 / (4000 * mp.e), 12)}")
    dser = [d_coef(j) for j in range(2, 9)]
    say("   d_j, j=2..8:", ", ".join(str(d) for d in dser))
    s5 = sum(abs(float(d_coef(j))) for j in range(5, 40))
    say(f"   sum_{{j>=5}} |d_j| = {s5:.6f}; (1/3)*sum = {s5 / 3:.6f} < 1/48 = {1 / 48:.6f}")
    RES["N1000_n2dtv"] = float(rows[-1][2])
    RES["N1000"] = 1000
    RES["three_over_4e"] = float(3 / (4 * mp.e))
    RES["one_over_4e"] = float(1 / (4 * mp.e))
    RES["S1_maxratio"] = float(maxratio)
    RES["theta_lo"], RES["theta_hi"] = float(th_lo), float(th_hi)
    RES["N_list"] = [r[0] for r in rows]
    # A5: best Poisson
    say("A5 best Poisson: a = n^2 (lambda - 1 + 1/n); n^2 d_TV(N_n, Po(lambda)) at a = 0, 1/4, 1/2, 1 and minimised over a")
    mp.mp.dps = 40
    best = []
    for n in (20, 50, 100, 200, 400, 1000):
        L = [mp.mpf(p.numerator) / p.denominator for p in law_closed(n)]

        def f(a, n=n, L=L):
            lam = 1 - mp.mpf(1) / n + mp.mpf(a) / n ** 2
            el = mp.e ** (-lam)
            tot, qk, qsum = mp.mpf(0), el, mp.mpf(0)
            for k in range(n):
                tot += abs(L[k] - qk)
                qsum += qk
                qk = qk * lam / (k + 1)
            tail = 1 - qsum                       # Poisson mass at k >= n, where p_k = 0
            return (tot + tail) / 2 * n ** 2

        vals = {a: f(a) for a in (0, 0.25, 0.5, 1)}
        # golden-section on [-0.5, 1.5]
        lo, hi = mp.mpf(-0.5), mp.mpf(1.5)
        g = (mp.sqrt(5) - 1) / 2
        c, d = hi - g * (hi - lo), lo + g * (hi - lo)
        fc, fd = f(c), f(d)
        for _ in range(70):
            if fc < fd:
                hi, d, fd = d, c, fc
                c = hi - g * (hi - lo)
                fc = f(c)
            else:
                lo, c, fc = c, d, fd
                d = lo + g * (hi - lo)
                fd = f(d)
        amin = (lo + hi) / 2
        fmin = f(amin)
        best.append((n, vals, amin, fmin))
        say(f"   n={n:5d}  a=0: {mp.nstr(vals[0], 8)}  a=1/4: {mp.nstr(vals[0.25], 8)}  a=1/2: {mp.nstr(vals[0.5], 8)}"
            f"  a=1: {mp.nstr(vals[1], 8)}  argmin a={mp.nstr(amin, 6)}  min={mp.nstr(fmin, 8)}")
    say(f"   limits L(a)/2: a=0: 3/(4e)={3 / (4 * E):.8f}  a=1/4: 5/(8e)={5 / (8 * E):.8f}  a=1/2: 1/(2e)={1 / (2 * E):.8f}  a=1: 1/e={1 / E:.8f}")
    RES["best_n"] = best[-1][0]
    RES["best_amin"] = float(best[-1][2])
    RES["best_min"] = float(best[-1][3])
    RES["one_over_2e"] = 1 / (2 * E)


# =============================================================================
# (B) simple permutations
# =============================================================================
def simple_counts(M):
    """s_m for m <= M from the compositional inverse g of f(z) = sum_{n>=1} n! z^n, which
    satisfies (1+u) g g' - u g' + g^2 = 0; then sum_{m>=4} s_m u^m = u - g(u) - 2u^2/(1+u)."""
    g = [0, 1] + [0] * (M - 1)
    for k in range(2, M + 1):
        rest = 0
        for i in range(2, k):                      # g g' at degree k without g_k
            rest += g[i] * (k - i + 1) * g[k - i + 1]
        for i in range(1, k):                      # g g' at degree k-1
            rest += g[i] * (k - i) * g[k - i]
        for i in range(1, k):                      # g^2 at degree k
            rest += g[i] * g[k - i]
        g[k] = -rest
    s = [0] * (M + 1)
    for m in range(1, M + 1):
        two = 2 * (-1) ** m if m >= 2 else 0       # [u^m] 2u^2/(1+u) = 2(-1)^m
        s[m] = (1 if m == 1 else 0) - g[m] - two
    s[1], s[2] = 1, 2                              # conventional values (not used: m >= 4)
    return g, s


def part_b():
    say("=" * 78)
    say("(B) simple permutations")
    say("=" * 78)
    M = max(NFLOAT, NEXACT) + 2
    g, s = simple_counts(M)
    # check f(g(u)) = u to order 30
    f = [0] + [math.factorial(n) for n in range(1, 31)]
    comp = [0] * 31
    power = [1] + [0] * 30
    for n in range(1, 31):
        power = [sum(power[i] * g[j - i] for i in range(j + 1) if j - i <= 30) for j in range(31)]
        for j in range(31):
            comp[j] += f[n] * power[j]
    say(f"B1 f(g(u)) = u to order 30: {comp[:31] == [0, 1] + [0] * 29}")
    known = {4: 2, 5: 6, 6: 46, 7: 338, 8: 2926, 9: 28146, 10: 298526}
    say(f"B2 s_4..s_10 = {[s[m] for m in range(4, 11)]}; known values (Albert-Atkinson-Klazar) agree: "
        f"{all(s[m] == v for m, v in known.items())}")
    bf = {m: sum(1 for p in itertools.permutations(range(m)) if crl.is_simple(list(p))) for m in range(4, 9)}
    say(f"B3 brute-force counts of simple permutations, m=4..8: {[bf[m] for m in range(4, 9)]}; agree: "
        f"{all(bf[m] == s[m] for m in bf)}")
    mlist = [m for m in (50, 100, 200) if m < M] + [M]
    rat = [s[m] / math.factorial(m) * math.e ** 2 for m in mlist]
    say(f"B4 e^2 s_m/m! at m={mlist}: " + ", ".join(f"{r:.6f}" for r in rat)
        + "  (expected 1 - 4/m + O(m^-2))")
    return s


# =============================================================================
# (C) exact law of R_n from the substitution decomposition
# =============================================================================
# coefficient blocks are arrays (2, KY): index [b, a] = coefficient of w^b y^a.
def convmat(u, dtype):
    """matrix Mu with vec(u * v) = Mu @ vec(v), truncated (b <= 1, a < KY)."""
    L = 2 * KY
    Mu = np.zeros((L, L), dtype=dtype)
    for b in range(2):
        for a in range(KY):
            for b2 in range(b + 1):
                for a2 in range(a + 1):
                    c = u[b - b2, a - a2]
                    if c:
                        Mu[b * KY + a, b2 * KY + a2] = c
    return Mu


def shift(v, sa, sb=0):
    out = np.zeros_like(v)
    if sb == 0:
        out[:, sa:] = v[:, :KY - sa]
    else:
        out[1, sa:] = v[0, :KY - sa]
    return out


def gf_law(N, s, exact):
    """Returns list Acoef[d] (2, KY): exact counts (exact=True) or counts/d! (float) of nonempty
    permutations of length d with t(G_pi) = 2^a 3^b, b <= 1."""
    dt = object if exact else np.float64
    L = 2 * KY
    zero = np.zeros((2, KY), dtype=dt) if not exact else np.array([[0] * KY, [0] * KY], dtype=object)
    A, Ip, Im, B, P2, P3, P4 = ([zero.copy() for _ in range(N + 1)] for _ in range(7))
    W = np.zeros((N + 1, N + 1, L), dtype=dt) if not exact else np.array(
        [[[0] * L for _ in range(N + 1)] for _ in range(N + 1)], dtype=object)
    Ms = [None] * (N + 1)
    MsIm = [None] * (N + 1)
    MsIp = [None] * (N + 1)
    if exact:
        sig = s
        binv = lambda d, j: 1  # noqa: E731
    else:
        sig = [float(Fraction(s[m], math.factorial(m))) if m >= 4 else 0.0 for m in range(N + 1)]
        binv = lambda d, j: 1.0 / math.comb(d, j)  # noqa: E731

    for d in range(1, N + 1):
        unit = zero.copy()
        if d == 1:
            unit[0, 0] = 1
        # powers A^m, m >= 2, at degree d
        if d >= 2:
            Y = np.zeros((d + 1, L), dtype=dt) if not exact else np.array([[0] * L for _ in range(d + 1)], dtype=object)
            for j in range(1, d):
                rows = W[1:d - j + 1, d - j]               # m-1 = 1..d-j
                contrib = rows.dot(Ms[j].T)
                if exact:
                    Y[2:d - j + 2] = Y[2:d - j + 2] + contrib
                else:
                    Y[2:d - j + 2] += binv(d, j) * contrib
            if not exact:
                Y[2:] *= np.arange(2, d + 1)[:, None]
            W[2:d + 1, d] = Y[2:d + 1]
        # S at degree d
        Sd = zero.copy()
        for m in range(4, d + 1):
            Sd = Sd + sig[m] * W[m, d].reshape(2, KY)
        Sd = shift(Sd, 1)
        # K at degree d: y I-^2 + y w I-^3 + y^3 w I-^4
        p2, p3, p4 = zero.copy(), zero.copy(), zero.copy()
        for j in range(1, d):
            c = binv(d, j)
            p2 = p2 + c * (MsIm[j] @ Im[d - j].reshape(L)).reshape(2, KY)
            p3 = p3 + c * (MsIm[j] @ P2[d - j].reshape(L)).reshape(2, KY)
            p4 = p4 + c * (MsIm[j] @ P3[d - j].reshape(L)).reshape(2, KY)
        P2[d], P3[d], P4[d] = p2, p3, p4
        Kd = shift(p2, 1) + shift(p3, 1, 1) + shift(p4, 3, 1)
        # D at degree d: sum_j I+_j B_{d-j}
        Dd = zero.copy()
        for j in range(1, d):
            Dd = Dd + binv(d, j) * (MsIp[j] @ B[d - j].reshape(L)).reshape(2, KY)
        Ip[d] = unit + Kd + Sd
        Im[d] = unit + Dd + Sd
        B[d] = Ip[d] + Dd
        A[d] = unit + Dd + Kd + Sd
        W[1, d] = A[d].reshape(L)
        Ms[d] = convmat(A[d], dt)
        MsIm[d] = convmat(Im[d], dt)
        MsIp[d] = convmat(Ip[d], dt)
    return A


def law_from_gf(Acoef_n, n, exact):
    """atoms: {('p', k): P(R_n = 2^k), ('t', k): P(R_n = 3*2^k)} for the tracked range."""
    f = math.factorial(n)
    out = {}
    for k in range(KY - 1):
        c0, c1 = Acoef_n[0, k + 1], Acoef_n[1, k + 1]
        if exact:
            out[("p", k)] = Fraction(int(c0) + (1 if k == 0 else 0), f)
            out[("t", k)] = Fraction(int(c1), f)
        else:
            out[("p", k)] = float(c0) + (1.0 / f if (k == 0 and n < 170) else 0.0)
            out[("t", k)] = float(c1)
    return out


def brute_law(n, fn):
    c = Counter(fn(list(p)) for p in itertools.permutations(range(n)))
    f = math.factorial(n)
    out = {}
    for k in range(KY - 1):
        out[("p", k)] = Fraction(c.get(2 ** k, 0), f)
        out[("t", k)] = Fraction(c.get(3 * 2 ** k, 0), f)
    other = Fraction(sum(v for r, v in c.items() if not (r & (r - 1) == 0 or (r % 3 == 0 and (r // 3) & (r // 3 - 1) == 0))), f)
    return out, other


def part_c(s):
    say("=" * 78)
    say("(C) exact law of R_n on the atoms 2^k, 3*2^k (substitution decomposition)")
    say("=" * 78)
    t = time.process_time()
    Aex = gf_law(NEXACT, s, exact=True)
    say(f"C1 exact integer generating function up to n={NEXACT} ({time.process_time() - t:.1f}s)")
    ok = True
    for n in range(1, 9):
        g = law_from_gf(Aex[n], n, True)
        b, _ = brute_law(n, crl.realizers_formula)
        ok &= (g == b)
    say(f"C2 GF law = law of Gallai's product formula (Remark B.1) on all permutations, n<=8: {ok}")
    ok = True
    for n in range(1, 7):
        g = law_from_gf(Aex[n], n, True)
        b, _ = brute_law(n, crl.brute_force_uorders)
        ok &= (g == b)
    say(f"C3 GF law = brute force over pairs of linear extensions, n<=6: {ok}")
    t = time.process_time()
    Afl = gf_law(NFLOAT, s, exact=False)
    say(f"C4 scaled floating-point generating function up to n={NFLOAT} ({time.process_time() - t:.1f}s)")
    worst = 0.0
    for n in range(1, NEXACT + 1):
        g = law_from_gf(Aex[n], n, True)
        h = law_from_gf(Afl[n], n, False)
        for key in g:
            if g[key]:
                worst = max(worst, abs(float(g[key]) - h[key]) / float(g[key]))
    say(f"C5 float versus exact, n<={NEXACT}, all tracked atoms: max relative error {worst:.2e}")
    RES["gf_float_relerr"] = worst
    return Aex, Afl


# =============================================================================
# (D) d_TV(R_n, 2^Z) and the second-order coefficient
# =============================================================================
def pois_float(k):
    return math.exp(-1) / math.factorial(k) if k >= 0 else 0.0


def mu_atom(key):
    kind, k = key
    if kind == "p":
        return -math.exp(-1) / math.factorial(k) * (k - 1) * (k - 3)
    return math.exp(-1) / math.factorial(k - 1) if k >= 1 else 0.0


def dtv_from_law(law):
    """(1/2)[sum over tracked atoms |P - P_Z| + untracked mass]; the untracked Poisson mass
    P(Z >= KY-1) < 1e-17 is the only approximation."""
    tracked = 0.0
    tot = 0.0
    for key, p in law.items():
        q = pois_float(key[1]) if key[0] == "p" else 0.0
        tracked += abs(p - q)
        tot += p
    rest = 1.0 - tot
    return 0.5 * (tracked + rest), rest


def part_d(Afl, bound_fn):
    say("=" * 78)
    say("(D) d_TV(R_n, 2^Z) from the exact law")
    say("=" * 78)
    rows = []
    for n in range(4, NFLOAT + 1):
        law = law_from_gf(Afl[n], n, False)
        dtv, rest = dtv_from_law(law)
        rows.append((n, dtv, rest, law))
    say("    n     d_TV(R_n,2^Z)    n d_TV     n^2(d_TV - c2/n)   n^2 P(R not 2^k, 3*2^k)   n^2 B(n)")
    e2 = {}
    for (n, dtv, rest, law) in rows:
        e2[n] = n * n * (dtv - C2 / n)
        if n in (4, 5, 6, 8, 10, 12, 15, 20, 22, 25, 30, 40, 50, 60, 80, 100, 150, 200, 250, 300, 400, 500) and n <= NFLOAT:
            bn = n * n * bound_fn(n) if n >= 22 else float("nan")
            say(f"   {n:4d}  {dtv:.12f}  {n * dtv:.8f}  {e2[n]:+14.6f}  {n * n * rest:14.6f}  {bn:12.3f}")
    worst22 = max(abs(e2[n]) for n in e2 if n >= 22)
    worst_all = max(abs(e2[n]) for n in e2)
    ratio = max(abs(e2[n]) / (n * n * bound_fn(n)) for n in e2 if n >= 22)
    say(f"D1 max_{{22<=n<={NFLOAT}}} n^2|d_TV - c2/n| = {worst22:.4f}; over 4<=n<={NFLOAT}: {worst_all:.4f}")
    say(f"   largest ratio |d_TV - c2/n| / B(n) for 22<=n<={NFLOAT}: {ratio:.4f} (Proposition S3: <= 1)")
    RES["dtvR_max_e2_22"] = worst22
    RES["dtvR_max_e2_all"] = worst_all
    RES["dtvR_ratio_to_bound"] = ratio
    RES["NFLOAT"] = NFLOAT
    RES["dtvR_at_N"] = rows[-1][1]
    RES["n_dtvR_at_N"] = NFLOAT * rows[-1][1]
    RES["e2_at_N"] = e2[NFLOAT]
    # atoms versus mu
    say("D2 n (P(R_n = x) - P(2^Z = x)) against mu(x), and n^2 (P - P_Z - mu/n):")
    keys = [("p", 0), ("p", 1), ("p", 2), ("p", 3), ("p", 4), ("p", 5), ("t", 0), ("t", 1), ("t", 2), ("t", 3), ("t", 4)]
    lab = {("p", k): str(2 ** k) for k in range(KY)}
    lab.update({("t", k): str(3 * 2 ** k) for k in range(KY)})
    for n in [m for m in (50, 100, 200) if m < NFLOAT] + [NFLOAT]:
        law = rows[n - 4][3]
        parts = []
        for key in keys:
            q = pois_float(key[1]) if key[0] == "p" else 0.0
            parts.append(f"{lab[key]}:{n * (law[key] - q):+.5f}")
        say(f"   n={n:4d} " + " ".join(parts))
    say("   mu(x):   " + " ".join(f"{lab[key]}:{mu_atom(key):+.5f}" for key in keys))
    maxdev = 0.0
    for (n, dtv, rest, law) in rows:
        if n >= 100:
            for key in law:
                q = pois_float(key[1]) if key[0] == "p" else 0.0
                maxdev = max(maxdev, abs(n * (law[key] - q) - mu_atom(key)) * n)
    say(f"   max over atoms and 100<=n<={NFLOAT} of n^2 |P - P_Z - mu/n| = {maxdev:.4f} (so the first-order law holds with O(n^-2) atom by atom)")
    RES["atoms_max_n2dev"] = maxdev
    # Richardson-type extrapolation of second-order coefficients
    ns = np.arange(max(100, NFLOAT // 3), NFLOAT + 1)

    def extrap(vals, deg):
        X = np.vstack([(1.0 / ns) ** i for i in range(deg + 1)]).T
        coef, *_ = np.linalg.lstsq(X, vals, rcond=None)
        return coef[0]

    est = {}
    for key in keys:
        q = pois_float(key[1]) if key[0] == "p" else 0.0
        vals = np.array([n * n * (rows[n - 4][3][key] - q - mu_atom(key) / n) for n in ns])
        est[key] = [extrap(vals, d) for d in (2, 3, 4)]
    vals = np.array([n * n * rows[n - 4][2] for n in ns])
    est_rest = [extrap(vals, d) for d in (2, 3, 4)]
    vals = np.array([e2[n] for n in ns])
    est_k = [extrap(vals, d) for d in (2, 3, 4)]
    say(f"D3 extrapolated second-order coefficients mu_2(x) = lim n^2(P - P_Z - mu/n) (fits in 1/n of degree 2,3,4 on {ns[0]}<=n<={ns[-1]}):")
    for key in keys:
        say(f"   x={lab[key]:>3}: " + ", ".join(f"{v:+.6f}" for v in est[key]))
    say("   untracked mass n^2 P(R not 2^k or 3*2^k): " + ", ".join(f"{v:+.6f}" for v in est_rest))
    say("   kappa = lim n^2 (d_TV - c2/n): " + ", ".join(f"{v:+.6f}" for v in est_k))
    mu2 = {key: est[key][1] for key in keys}
    pos = sum(mu2[k] for k in keys if mu_atom(k) > 1e-12)
    zero = sum(max(mu2[k], 0) for k in keys if abs(mu_atom(k)) <= 1e-12)
    allkeys = [("p", k) for k in range(12)] + [("t", k) for k in range(12)]
    mu2all = {}
    for key in allkeys:
        q = pois_float(key[1]) if key[0] == "p" else 0.0
        vals = np.array([n * n * (rows[n - 4][3][key] - q - mu_atom(key) / n) for n in ns])
        mu2all[key] = extrap(vals, 3)
    say("   all tracked atoms, e * mu_2(x) (fit of degree 3): " + "; ".join(
        f"{lab[k]}:{math.e * mu2all[k]:+.6f}" for k in allkeys))
    pos = sum(mu2all[k] for k in allkeys if mu_atom(k) > 1e-15)
    zero = sum(max(mu2all[k], 0) for k in allkeys if abs(mu_atom(k)) <= 1e-15)
    say(f"   consistency: sum over mu>0 atoms of mu_2 + sum over mu=0 atoms of mu_2^+ + untracked = "
        f"{pos + zero + est_rest[1]:+.6f} (atoms 2^k, 3*2^k with k<12)")
    RES["kappa_est"] = [float(v) for v in est_k]
    RES["kappa_consistency"] = float(pos + zero + est_rest[1])
    RES["mu2_est"] = {lab[k]: float(mu2all[k]) for k in allkeys}
    RES["untracked_n2_est"] = float(est_rest[1])
    return rows


# =============================================================================
# (E) the explicit bound of Proposition S3
# =============================================================================
def ff(n, j):
    r = 1
    for i in range(j):
        r *= (n - i)
    return r


def Fbar(m):
    return 42 / ff(m, 2) + 936 / ff(m, 3) + 600 / ff(m, 4) + 4320 / ff(m, 5)


def sbar(m):
    return 10 / m + Fbar(m)


def hbar(m):
    return 8 / m + 18 / ff(m, 2) + Fbar(m)


def dbar(m):
    return math.exp(-1) / m + 2 / (m * math.factorial(min(m, 170)))


def PEbar(n):
    return 90 / ff(n, 2) + 944 / ff(n, 3) + 600 / ff(n, 4) + 4320 / ff(n, 5)


def Ebadbar(n):
    return (3 * (n - 2) / ff(n, 2)) * (sbar(n - 2) + 3 * hbar(n - 2)) + 12 / ff(n, 2) \
        + (2 / n) * (sbar(n - 1) + hbar(n - 1))


def Occbar(n):
    return (3 * (n - 2) / ff(n, 2)) * (4 / (n - 2) + 2 * dbar(n - 2)) + (2 / n) * (2 / (n - 1) + 2 * dbar(n - 1))


def rho1bar(n):
    return math.exp((n + 1) * math.log(2) - math.lgamma(n + 2) - math.log(n)) + math.exp(-math.lgamma(n + 1))


def Bbound(n):
    return rho1bar(n) + PEbar(n) + Ebadbar(n) + Occbar(n) + 3 / ff(n, 2)


def EIf(n):
    """float vector E I_k(n), k = 0..n (E I_k = (n-k+1)^2 / C(n,k))."""
    k = np.arange(n + 1)
    lg = np.array([math.lgamma(i + 1) for i in range(n + 1)])
    return (n - k + 1) ** 2 * np.exp(lg[k] + lg[n - k] - lg[n])


def part_e():
    say("=" * 78)
    say("(E) explicit constant of Proposition S3")
    say("=" * 78)
    # E1: the interval inequalities used in the proof, exact sums versus bounds
    worstF = worsts = worsth = 0.0
    for m in range(12, 3001):
        ei = EIf(m)
        Fm = ei[4:m - 1].sum()
        sm = ei[3:m].sum()
        l = np.arange(2, m)
        hm = (np.minimum(l, m - l + 1) / (m - l + 1) * ei[2:m]).sum()
        worstF = max(worstF, float(Fm) / Fbar(m))
        if m >= 20:
            worsts = max(worsts, float(sm) / sbar(m))
            worsth = max(worsth, float(hm) / hbar(m))
    say(f"E1 max sum_{{k=4}}^{{m-2}} E I_k / Fbar(m) over 12<=m<=3000: {worstF:.4f} (claim <= 1)")
    say(f"   max s_m / sbar(m), h_m / hbar(m) over 20<=m<=3000: {worsts:.4f}, {worsth:.4f} (claim <= 1)")
    # E2: pair moments exact formulas (Lemma B.2) versus the simplified bounds
    worstP = 0.0
    for n in range(12, 3001):
        pe_exact_parts = float(EIf(n)[4:n - 1].sum()) \
            + 18 * (n - 4) * (n - 5) / ff(n, 4) + 4 * (n - 3) / ff(n, 3) + 8 * (n - 4) / ff(n, 4) \
            + 4 * (6 * n - 16) / ff(n, 3) + 2 / ff(n, 2)
        worstP = max(worstP, pe_exact_parts / PEbar(n))
    say(f"E2 (Lemma B.2 pieces with exact interval sums) / PEbar(n), 12<=n<=3000: max {worstP:.4f} (claim <= 1)")
    # E3: monotonicity and the constants
    vals = [(n, n * n * Bbound(n)) for n in range(22, 5001)]
    mono = all(vals[i][1] >= vals[i + 1][1] for i in range(len(vals) - 1))
    say(f"E3 n^2 B(n) non-increasing on 22<=n<=5000: {mono}")
    table = {}
    for n0 in (22, 30, 50, 100, 200, 1000):
        table[n0] = n0 * n0 * Bbound(n0)
    lim = 90 + (3 * (10 + 24) + 12 + 2 * 18) + (12 + 6 / E + 4 + 4 / E) + 3
    say("   n0 -> n0^2 B(n0): " + ", ".join(f"{n0}: {v:.2f}" for n0, v in table.items())
        + f"; limit {lim:.2f}")
    pieces = {n: (n * n * PEbar(n), n * n * Ebadbar(n), n * n * Occbar(n), 3 * n * n / ff(n, 2)) for n in (22, 100, 1000)}
    for n, p in pieces.items():
        say(f"   n={n}: n^2 x [P(E) bound, E[#occ; E] bound, occurrence approximation, weights] = "
            + ", ".join(f"{v:.2f}" for v in p))
    # Lemma B.2(a) bound 223/n^2 versus PEbar
    say(f"   PEbar(n) n^2 at n=20 (if valid; needs n>=12): {400 * PEbar(20):.2f} (Lemma B.2(a): 223)")
    RES["C_table"] = {str(k): v for k, v in table.items()}
    RES["C_limit"] = lim
    RES["E1"] = [worstF, worsts, worsth]
    RES["E2"] = worstP
    return Bbound


def main():
    part_a()
    s = part_b()
    bound_fn = part_e()
    _, Afl = part_c(s)
    part_d(Afl, bound_fn)
    say("=" * 78)
    cpu = time.process_time() - T0
    RES["cpu_seconds"] = cpu
    say(f"total CPU time: {cpu:.1f} s")
    with open(OUT, "w") as fh:
        fh.write("\n".join(_lines) + "\n")
    with open(JSON_OUT, "w") as fh:
        json.dump(RES, fh, indent=1, default=str)


if __name__ == "__main__":
    main()
