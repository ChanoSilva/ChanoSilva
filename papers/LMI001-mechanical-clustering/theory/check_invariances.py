#!/usr/bin/env python3
"""LMI001 theory check: invariances of the trace form J and size weights.

Verifies, in exact rational arithmetic (fractions.Fraction) unless stated:

 (i)  dim V_{n,k}, V_{n,k} = {Delta symmetric : J_Delta(C) constant over the
      partitions of [n] into k non-empty clusters}, for 2 <= n <= 7 and all k,
      against the formula  n+1 (2 <= k <= n-1),  n(n+1)/2 (k in {1, n});
      that span{I, g1^T + 1g^T} lies in V_{n,k} and has dimension n+1;
      and dim W_n, W_n = {Delta : J_Delta(C) = alpha + beta (n-k) for all
      partitions with any k}, against n+1.
 (ii) size weights (Next step (c)): for candidate w and 2 <= k <= n-2,
      the rank of the pair functions C -> w(n_c(i)) [i ~ j] plus the constant
      (predicted: binom(n,2)+1 unless w ~ 1/m, then binom(n,2) for k >= 3),
      the rank of the weighted-kernel-k-means space G_omega (predicted
      <= binom(n,2)), and whether W_w is contained in G_omega for omega = 1
      and for a random positive rational omega.  Plus random-A float checks
      and the explicit annihilator nu(omega) for n = 4, k = 2.
 (iii) rest-length spring: the four-point quadratic form -8rs (exact),
      and the minimal shift lambda_max(P A P) >= 2rs (float).

Deterministic: seed 20261003.  Runtime: a few seconds of CPU.
Output: printed; redirect to check_invariances_output.txt.
"""
from fractions import Fraction as Fr
from itertools import combinations
from math import comb
import random
import sys
import time

import numpy as np

SEED = 20261003
NMAX = 7


# ---------------------------------------------------------------- utilities
def set_partitions(elements):
    """All set partitions of a list (as lists of lists)."""
    if not elements:
        yield []
        return
    first, rest = elements[0], elements[1:]
    for p in set_partitions(rest):
        for i in range(len(p)):
            yield p[:i] + [[first] + p[i]] + p[i + 1:]
        yield [[first]] + p


def partitions_k(n, k):
    return [p for p in set_partitions(list(range(n))) if len(p) == k]


def rank_exact(rows):
    """Rank of a matrix given as a list of rows of Fractions (Gaussian elim.)."""
    M = [list(r) for r in rows]
    if not M:
        return 0
    ncol = len(M[0])
    r = 0
    for c in range(ncol):
        piv = None
        for i in range(r, len(M)):
            if M[i][c] != 0:
                piv = i
                break
        if piv is None:
            continue
        M[r], M[piv] = M[piv], M[r]
        pv = M[r][c]
        for i in range(len(M)):
            if i != r and M[i][c] != 0:
                f = M[i][c] / pv
                Mi, Mr = M[i], M[r]
                for j in range(c, ncol):
                    if Mr[j] != 0:
                        Mi[j] -= f * Mr[j]
        r += 1
        if r == len(M):
            break
    return r


def sym_basis(n):
    """Index list of the symmetric-matrix basis: (i, i) and (i, j), i < j."""
    return [(i, i) for i in range(n)] + list(combinations(range(n), 2))


def J_row(part, n):
    """Coefficients of J_Delta(C) in the basis E_ii, E_ij + E_ji (Fractions)."""
    row = {}
    for (i, j) in sym_basis(n):
        row[(i, j)] = Fr(0)
    for c in part:
        m = len(c)
        for i in c:
            row[(i, i)] += 1 - Fr(1, m)
        for i, j in combinations(sorted(c), 2):
            row[(i, j)] += -Fr(2, m)
    return [row[b] for b in sym_basis(n)]


def nullity(rows, ncol):
    return ncol - rank_exact(rows)


def vec_of_matrix(D, n):
    return [Fr(D[i][j]) for (i, j) in sym_basis(n)]


# ------------------------------------------------------------------- part (i)
def part_i(out):
    out.append("== (i) dim V_{n,k}: Delta with J_Delta constant on k-partitions ==")
    out.append("n  k  #partitions  dimV(exact)  formula  match  span{I,g1'+1g'} in V & rank")
    allok = True
    for n in range(2, NMAX + 1):
        nb = len(sym_basis(n))
        allparts = list(set_partitions(list(range(n))))
        for k in range(1, n + 1):
            parts = [p for p in allparts if len(p) == k]
            T = [J_row(p, n) for p in parts]
            # unknowns (Delta, alpha): J_Delta(C) - alpha = 0
            aug = [r + [Fr(-1)] for r in T]
            dimV = nullity(aug, nb + 1)  # alpha is determined by Delta
            formula = n + 1 if 2 <= k <= n - 1 else n * (n + 1) // 2
            # candidate generators: I and g1'+1g' for g = e_l
            gens = []
            I = [[Fr(int(i == j)) for j in range(n)] for i in range(n)]
            gens.append(vec_of_matrix(I, n))
            for l in range(n):
                G = [[Fr(int(i == l) + int(j == l)) for j in range(n)] for i in range(n)]
                gens.append(vec_of_matrix(G, n))
            in_V = True
            for g in gens:
                vals = [sum(a * b for a, b in zip(r, g)) for r in T]
                if any(v != vals[0] for v in vals):
                    in_V = False
            rk = rank_exact(gens)
            ok = (dimV == formula) and in_V and rk == n + 1
            allok &= ok
            out.append(f"{n}  {k}  {len(parts):11d}  {dimV:11d}  {formula:7d}  {str(dimV == formula):5s}  {in_V} & {rk}")
    out.append(f"ALL (i) V_(n,k) checks pass: {allok}")
    out.append("")
    out.append("== (i') dim W_n: J_Delta(C) = alpha + beta (n-k) for all partitions, all k ==")
    okW = True
    for n in range(2, NMAX + 1):
        nb = len(sym_basis(n))
        rows = []
        for p in set_partitions(list(range(n))):
            k = len(p)
            rows.append(J_row(p, n) + [Fr(-1), Fr(-(n - k))])
        nul = nullity(rows, nb + 2)
        # (alpha, beta) are determined by Delta because k takes >= 2 values
        dimW = nul
        okW &= dimW == n + 1
        out.append(f"n={n}: #partitions={len(rows)}  dim W_n={dimW}  formula n+1={n + 1}  match={dimW == n + 1}")
    out.append(f"ALL (i') checks pass: {okW}")
    out.append("")
    return allok and okW


# ------------------------------------------------------------------ part (ii)
WEIGHTS = {
    "1/m": lambda m: Fr(1, m),
    "1 (total)": lambda m: Fr(1),
    "1/m^2": lambda m: Fr(1, m * m),
    "1/(m-1)": lambda m: Fr(1, m - 1) if m >= 2 else Fr(0),
    "1/binom(m,2)": lambda m: Fr(2, m * (m - 1)) if m >= 2 else Fr(0),
    "m": lambda m: Fr(m),
}


def pair_function_rows(parts, n, w):
    """Rows: partitions; columns: pair (a,b) -> w(n_c)[a~b], plus constant."""
    pairs = list(combinations(range(n), 2))
    rows = []
    for p in parts:
        lab = {}
        for ci, c in enumerate(p):
            for i in c:
                lab[i] = ci
        sizes = [len(c) for c in p]
        r = []
        for (a, b) in pairs:
            r.append(w(sizes[lab[a]]) if lab[a] == lab[b] else Fr(0))
        r.append(Fr(1))
        rows.append(r)
    return rows


def G_rows(parts, n, om):
    """Rows: partitions; columns: symmetric B basis; entry of
    sum_c (1_c^T B 1_c) / omega(C_c), i.e. the omega-weighted kernel k-means
    objective up to the constant sum_i omega_i K_ii, with B = W K W."""
    basis = sym_basis(n)
    rows = []
    for p in parts:
        r = []
        for (i, j) in basis:
            v = Fr(0)
            for c in p:
                if i in c and j in c:
                    v += Fr(1 if i == j else 2) / sum(om[s] for s in c)
            r.append(v)
        rows.append(r)
    return rows


def part_ii(out):
    rng = random.Random(SEED)
    out.append("== (ii) size weights w: rank of {C -> w(n_c)[a~b]} + const vs binom(n,2)+1;")
    out.append("        containment W_w in G_omega (weighted kernel k-means space) ==")
    out.append("n k  w             rank(W_w+1) full=C(n,2)+1  rank G_1  rank G_rand  W_w<=G_1  W_w<=G_rand")
    ok = True
    for n in range(4, NMAX + 1):
        allparts = list(set_partitions(list(range(n))))
        om_rand = [Fr(rng.randint(1, 9), rng.randint(1, 9)) for _ in range(n)]
        for k in range(2, n - 1):
            parts = [p for p in allparts if len(p) == k]
            G1 = G_rows(parts, n, [Fr(1)] * n)
            Gr = G_rows(parts, n, om_rand)
            rG1 = rank_exact(G1)
            rGr = rank_exact(Gr)
            for name, w in WEIGHTS.items():
                Wr = pair_function_rows(parts, n, w)
                rW = rank_exact(Wr)
                full = comb(n, 2) + 1
                inc1 = rank_exact([a + b for a, b in zip(G1, Wr)]) == rG1
                incr = rank_exact([a + b for a, b in zip(Gr, Wr)]) == rGr
                # predictions (k >= 3 and w(2) != 0; k = 2 checked separately)
                if name == "1/m":
                    pred_rank = full - 1
                    pred_inc1 = True
                else:
                    pred_rank = full if k >= 3 else None
                    pred_inc1 = False if k >= 3 else None
                if pred_rank is not None and rW != pred_rank:
                    ok = False
                if pred_inc1 is not None and inc1 != pred_inc1:
                    ok = False
                if rG1 > comb(n, 2) or rGr > comb(n, 2):
                    ok = False
                out.append(f"{n} {k}  {name:12s}  {rW:4d} {str(rW == full):5s} {full:4d}"
                           f"  {rG1:8d}  {rGr:11d}  {str(inc1):8s}  {incr}")
    out.append(f"ALL (ii) exact predictions hold (k>=3; and 1/m for all k): {ok}")
    out.append("")
    return ok


def k2_condition(out):
    """For k = 2 the dimension count is inconclusive iff h(a)+h(n-a) is
    constant, h(m) = w(m) m(m-1)/2.  Report which candidates hit this."""
    out.append("== (ii') k = 2: is h(a)+h(n-a) constant (dimension count inconclusive)? ==")
    for n in range(4, NMAX + 1):
        line = []
        for name, w in WEIGHTS.items():
            h = [w(m) * m * (m - 1) / 2 if m >= 2 else Fr(0) for m in range(n + 1)]
            vals = {h[a] + h[n - a] for a in range(1, n)}
            line.append(f"{name}:{'const' if len(vals) == 1 else 'non-const'}")
        out.append(f"n={n}: " + ", ".join(line))
    out.append("")


def random_float_checks(out):
    rng = np.random.default_rng(SEED)
    out.append("== (ii'') random-A float checks ==")
    worst_spec = 0.0
    resid_tot = []
    for trial in range(20):
        n = int(rng.integers(5, 8))
        k = int(rng.integers(3, n - 1))
        parts = partitions_k(n, k)
        A = rng.normal(size=(n, n)); A = (A + A.T) / 2
        # w = 1/m: E_spec = 1/2 J_{-A} + 1/2 (n-k) A_ii-mean? (zero the diagonal)
        np.fill_diagonal(A, 0.0)
        K = -A
        for p in parts:
            E = sum(sum(A[i, j] for i, j in combinations(c, 2)) / len(c) for c in p)
            J = np.trace(K) - sum(K[np.ix_(c, c)].sum() / len(c) for c in p)
            worst_spec = max(worst_spec, abs(E - 0.5 * J))
        # w = 1: least-squares distance of F_A (A >= 0) to G_omega for random omega
        Ap = np.abs(A)
        F = np.array([sum(sum(Ap[i, j] for i, j in combinations(c, 2)) for c in p) for p in parts])
        om = rng.uniform(0.2, 5.0, size=n)
        basis = sym_basis(n)
        G = np.array([[sum((1 if i == j else 2) / om[c].sum() for c in p if i in c and j in c)
                       for (i, j) in basis] for p in parts])
        coef, *_ = np.linalg.lstsq(G, F, rcond=None)
        resid_tot.append(np.linalg.norm(F - G @ coef) / np.linalg.norm(F))
    out.append(f"w=1/m: max |E_spec - J_(-A)/2| over 20 random (n,k,A), all partitions: {worst_spec:.2e}")
    out.append(f"w=1, A>=0: relative LS residual of F_A off G_omega (random omega): "
               f"min {min(resid_tot):.3e}, max {max(resid_tot):.3e}")
    out.append("")
    return worst_spec < 1e-12 and min(resid_tot) > 1e-6


def nu_certificate(out):
    """n = 4, k = 2: nu(C) = eps(C) omega(X) omega(Y), eps = +1 for 1+3 splits,
    -1 for 2+2 splits, annihilates G_omega and the constants; and
    <nu, F_A> = sum_{a<b} A_ab [ (w3 - w2) omega_ab omega_cd + 2 w3 omega_c omega_d ]."""
    rng = random.Random(SEED + 1)
    out.append("== (ii''') n=4, k=2 annihilator nu(omega) (exact, 200 random rational omega, A) ==")
    n = 4
    parts = partitions_k(4, 2)
    ok = True
    for trial in range(200):
        om = [Fr(rng.randint(1, 20), rng.randint(1, 20)) for _ in range(4)]
        nu = []
        for p in parts:
            X, Y = p
            eps = 1 if len(X) in (1, 3) else -1
            nu.append(eps * sum(om[i] for i in X) * sum(om[i] for i in Y))
        G = G_rows(parts, n, om)
        for col in range(len(G[0])):
            if sum(nu[r] * G[r][col] for r in range(len(parts))) != 0:
                ok = False
        if sum(nu) != 0:
            ok = False
        w2, w3 = Fr(rng.randint(1, 9), rng.randint(1, 9)), Fr(rng.randint(1, 9), rng.randint(1, 9))
        A = {(a, b): Fr(rng.randint(-9, 9)) for a, b in combinations(range(4), 2)}
        F = []
        for p in parts:
            v = Fr(0)
            for c in p:
                wc = w2 if len(c) == 2 else (w3 if len(c) == 3 else Fr(0))
                v += wc * sum(A[(a, b)] for a, b in combinations(sorted(c), 2))
            F.append(v)
        lhs = sum(x * y for x, y in zip(nu, F))
        rhs = Fr(0)
        for (a, b) in combinations(range(4), 2):
            c, d = [x for x in range(4) if x not in (a, b)]
            rhs += A[(a, b)] * ((w3 - w2) * (om[a] + om[b]) * (om[c] + om[d]) + 2 * w3 * om[c] * om[d])
        if lhs != rhs:
            ok = False
    out.append(f"nu annihilates G_omega and constants, and the pairing formula holds: {ok}")
    out.append("")
    return ok


# ----------------------------------------------------------------- part (iii)
def part_iii(out):
    out.append("== (iii) rest-length spring phi(d) = (d - r)^2 ==")
    ok = True
    for (r, s) in [(Fr(1), Fr(1)), (Fr(1), Fr(5)), (Fr(3, 2), Fr(7, 3)), (Fr(2), Fr(50))]:
        xs = [0, s, 2 * s, 3 * s]
        c = [1, -1, -1, 1]
        q = sum(c[i] * c[j] * (-(abs(xs[i] - xs[j]) - r) ** 2) for i in range(4) for j in range(4))
        ok &= q == -8 * r * s
        out.append(f"r={r}, s={s}: sum c_i c_j (-phi(d_ij)) = {q}  (-8rs = {-8 * r * s})")
    # minimal PSD shift on X_s: lambda_max(P A P) >= 2 r s (float)
    rr = 1.0
    for s in [0.5, 1.0, 5.0, 50.0]:
        x = np.array([0, s, 2 * s, 3 * s])
        A = (np.abs(x[:, None] - x[None, :]) - rr) ** 2
        P = np.eye(4) - np.ones((4, 4)) / 4
        lam = np.linalg.eigvalsh(P @ A @ P).max()
        out.append(f"r=1, s={s}: sigma_min = lambda_max(PAP) = {lam:.4f} >= 2rs = {2 * rr * s:.4f}: {lam >= 2 * rr * s - 1e-12}")
        ok &= lam >= 2 * rr * s - 1e-12
    out.append(f"ALL (iii) checks pass: {ok}")
    out.append("")
    return ok


def main():
    t0 = time.process_time()
    out = [f"check_invariances.py  seed={SEED}  python={sys.version.split()[0]}  numpy={np.__version__}", ""]
    r1 = part_i(out)
    r2 = part_ii(out)
    k2_condition(out)
    r3 = random_float_checks(out)
    r4 = nu_certificate(out)
    r5 = part_iii(out)
    out.append(f"SUMMARY: (i) {r1}  (ii) {r2}  (ii'') {r3}  (ii''') {r4}  (iii) {r5}")
    out.append(f"CPU seconds: {time.process_time() - t0:.1f}")
    print("\n".join(out))


if __name__ == "__main__":
    main()
