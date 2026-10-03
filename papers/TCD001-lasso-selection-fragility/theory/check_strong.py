#!/usr/bin/env python3
"""
TCD001 -- exhaustive exact check of the reduction  X3C -> Selection-Witness  with p growing
(theory/strong_hardness.tex, Theorem thm:strong; derivation in theory/strong_hardness_derivation.md).

Construction (rule C).  Universe U = {0..3q-1}, triples C_1..C_m.  Columns: target 0, absorbers e in U
(p = 3q+1).  Rows (n = m+3q):
    triple row i   : x_{i0} = rho/q,       x_{ie} = 1 (e in C_i),          y_i = 1
    anchor row a_e : x_{a_e,0} = kappa*u/(3q), x_{a_e,e} = u,              y_{a_e} = S/u
with u = 3m, S = m, mu = S+1, eta = kappa-rho = 1/2, theta = 1/(24q), rho = 1-(eta*S-theta)/mu.
The instance is then scaled to INTEGER data (X *= L_X, y *= L_Y, mu *= L_X L_Y), and everything
below is run on the integer instance.

For every source instance the script
  1. solves the Lasso EXACTLY (Fractions) on D and on D \\ R for EVERY proper nonempty R:
     floating coordinate descent proposes a signed support, the KKT system is then solved and checked
     in rational arithmetic; if the check fails, all 3^p signed supports are enumerated
     (theory/check_hardness.exact_lasso_stats).  Uniqueness is certified by full rank of X_E
     (Tibshirani 2013); a set with an entering target and uncertified uniqueness is reported;
  2. checks, set by set, the characterisation of the proof:
       target enters on D \\ R (unique minimiser)  <=>  all anchors kept and the kept triples are an exact cover;
  3. checks  (a witness exists)  <=>  (X3C answer YES, brute force);
  4. checks the intermediate claims of the proof on every subset, on the problem WITHOUT the target column:
       the minimiser is >= 0, its support is {anchored e with cov_e >= 2}, and |X_0^T r_{-0}| > mu iff predicted;
  5. cross-checks a sample of subsets with the KKT-guarded homotopy solver of experiments/lasso_fragility.py;
  6. runs negative controls that violate the conditions of the proof (they must produce failures).

Deterministic (seed 20261003).  Output: theory/check_strong_output.txt (also printed).
"""
from __future__ import annotations

import itertools
import os
import random
import sys
import time
from fractions import Fraction as F
from math import lcm

import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
sys.path.insert(0, os.path.join(HERE, "..", "experiments"))
import check_hardness as ch  # noqa: E402  (theory/check_hardness.py: solve_exact, is_singular, ...)
import lasso_fragility as lf  # noqa: E402

OUT: list[str] = []
T0 = time.process_time()


def log(msg: str = "") -> None:
    print(msg, flush=True)
    OUT.append(msg)


# ----------------------------------------------------------------------------------------------
# Source problem
# ----------------------------------------------------------------------------------------------
def x3c_yes(q, triples):
    U = set(range(3 * q))
    for comb in itertools.combinations(range(len(triples)), q):
        cov = set()
        ok = True
        for i in comb:
            if cov & set(triples[i]):
                ok = False
                break
            cov |= set(triples[i])
        if ok and cov == U:
            return True
    return False


# ----------------------------------------------------------------------------------------------
# The reduction
# ----------------------------------------------------------------------------------------------
def build(q, triples, override=None, integer=True):
    override = override or {}
    m, d = len(triples), 3 * q
    u = override.get("u", 3 * m)
    S = F(override.get("S", m))
    eta = F(override.get("eta", F(1, 2)))
    theta = F(override.get("theta", F(1, 24 * q)))
    mu = S + 1
    eps = (eta * S - theta) / mu
    rho = 1 - eps
    kappa = rho + eta
    w = F(1, d)
    X, y = [], []
    for C in triples:
        X.append([rho / q] + [F(1) if e in C else F(0) for e in range(d)])
        y.append(F(1))
    for e in range(d):
        X.append([kappa * w * u] + [F(u) if e2 == e else F(0) for e2 in range(d)])
        y.append(S / u)
    par = dict(u=u, S=S, eta=eta, theta=theta, mu=mu, rho=rho, kappa=kappa)
    if integer:
        LX = lcm(*[v.denominator for row in X for v in row])
        LY = lcm(*[v.denominator for v in y])
        X = [[v * LX for v in row] for row in X]
        y = [v * LY for v in y]
        mu = mu * LX * LY
        par.update(LX=LX, LY=LY, maxX=max(abs(v) for row in X for v in row),
                   maxy=max(abs(v) for v in y), mu_int=mu)
        assert all(v.denominator == 1 for row in X for v in row) and all(v.denominator == 1 for v in y)
        assert mu.denominator == 1
    return X, y, mu, par


# ----------------------------------------------------------------------------------------------
# Exact Lasso from sufficient statistics: float proposal + exact KKT verification (+ fallback)
# ----------------------------------------------------------------------------------------------
STATS = dict(solves=0, fallbacks=0)


def cd_float(G, g, mu, sweeps=5000):
    Gf = np.array([[float(v) for v in row] for row in G])
    gf = np.array([float(v) for v in g])
    muf = float(mu)
    p = len(gf)
    b = np.zeros(p)
    diag = np.diag(Gf).copy()
    scale = max(1.0, float(np.max(np.abs(gf))) if p else 1.0)
    for _ in range(sweeps):
        md = 0.0
        for j in range(p):
            if diag[j] <= 0:
                b[j] = 0.0
                continue
            c = gf[j] - Gf[j] @ b + diag[j] * b[j]
            new = np.sign(c) * max(abs(c) - muf, 0.0) / diag[j]
            md = max(md, abs(new - b[j]) * diag[j])
            b[j] = new
        if md < 1e-13 * scale:
            break
    return b


def exact_check(G, g, mu, S, s):
    p = len(g)
    if S:
        GSS = [[G[a][b] for b in S] for a in S]
        bS = ch.solve_exact(GSS, [g[a] - mu * sa for a, sa in zip(S, s)])
        if bS is None or any(sa * ba <= 0 for sa, ba in zip(s, bS)):
            return None
    else:
        bS = []
    beta = [F(0)] * p
    for a, ba in zip(S, bS):
        beta[a] = ba
    c = [g[j] - sum(G[j][l] * beta[l] for l in S) for j in range(p)]
    if any(abs(c[j]) > mu for j in range(p) if j not in S):
        return None
    return beta, c


def exact_lasso(G, g, mu):
    """(beta, certified_unique, tie, c) for 1/2 b'Gb - g'b + mu|b|_1, exact."""
    STATS["solves"] += 1
    p = len(g)
    bf = cd_float(G, g, mu)
    thr = 1e-9 * max(1.0, float(np.max(np.abs(bf))) if p else 1.0)
    S = tuple(j for j in range(p) if abs(bf[j]) > thr)
    s = tuple(1 if bf[j] > 0 else -1 for j in S)
    out = exact_check(G, g, mu, S, s)
    if out is None:
        STATS["fallbacks"] += 1
        beta, status, tie = ch.exact_lasso_stats(G, g, mu)
        c = [g[j] - sum(G[j][l] * beta[l] for l in range(p)) for j in range(p)]
        return beta, status == "unique", tie, c
    beta, c = out
    E = [j for j in range(p) if abs(c[j]) == mu]
    unique = not ch.is_singular([[G[a][b] for b in E] for a in E])
    tie = any(abs(c[j]) == mu and beta[j] == 0 for j in range(p))
    return beta, unique, tie, c


# ----------------------------------------------------------------------------------------------
# One source instance
# ----------------------------------------------------------------------------------------------
def check_instance(q, triples, override=None, intermediate=True, lib_sample=60, seed=0):
    X, y, mu, par = build(q, triples, override)
    m, d = len(triples), 3 * q
    n = m + d
    full = (1 << n) - 1
    stats = ch.stats_all_masks(X, y)
    res = dict(n=n, p=d + 1, subsets=0, entries=0, char_fail=0, uncert_entry=0, uncert=0, ties=0,
               inter_fail=0, inter_sign_fail=0, lib_checked=0, lib_disagree=0, min_R=None)
    # full data D
    G, g = stats[full]
    beta, uniq, tie, _ = exact_lasso(G, g, mu)
    res["D_ok"] = uniq and beta[0] == 0
    anchors_mask = ((1 << d) - 1) << m
    for keep in range(1, full):
        res["subsets"] += 1
        G, g = stats[keep]
        beta, uniq, tie, _ = exact_lasso(G, g, mu)
        res["uncert"] += not uniq
        res["ties"] += tie
        enters = beta[0] != 0
        if enters and not uniq:
            res["uncert_entry"] += 1
        witness = enters and uniq
        kept_tr = [i for i in range(m) if keep >> i & 1]
        cov = [sum(1 for i in kept_tr if e in triples[i]) for e in range(d)]
        all_anch = (keep & anchors_mask) == anchors_mask
        predicted = all_anch and all(c == 1 for c in cov)
        res["char_fail"] += witness != predicted
        if witness:
            res["entries"] += 1
            k = n - bin(keep).count("1")
            res["min_R"] = k if res["min_R"] is None else min(res["min_R"], k)
        if intermediate:
            # problem without the target column (absorbers only)
            Gr = [row[1:] for row in G[1:]]
            gr = g[1:]
            br, _, _, _ = exact_lasso(Gr, gr, mu)
            P = [e for e in range(d) if keep >> (m + e) & 1]
            pred_supp = {e for e in P if cov[e] >= 2}
            supp = {e for e in range(d) if br[e] != 0}
            res["inter_sign_fail"] += any(v < 0 for v in br)
            c0 = g[0] - sum(G[0][1 + e] * br[e] for e in range(d))
            res["inter_fail"] += (supp != pred_supp) or ((abs(c0) > mu) != predicted)
    # library cross-check on a sample of subsets (floating point, KKT-guarded homotopy)
    if lib_sample:
        Xf = np.array([[float(v) for v in row] for row in X])
        yf = np.array([float(v) for v in y])
        rng = random.Random(seed)
        keeps = rng.sample(range(1, full + 1), min(lib_sample, full))
        for keep in keeps:
            idx = [i for i in range(n) if keep >> i & 1]
            bl = lf.lasso_lars(Xf[idx], yf[idx], float(mu))
            G, g = stats[keep]
            be, _, _, _ = exact_lasso(G, g, mu)
            sl = tuple(np.flatnonzero(np.abs(bl) > 1e-7 * max(1.0, np.max(np.abs(bl)))))
            se = tuple(j for j in range(d + 1) if be[j] != 0)
            res["lib_checked"] += 1
            res["lib_disagree"] += sl != se
    res["yes"] = x3c_yes(q, triples)
    res["witness"] = res["min_R"] is not None
    res["par"] = par
    return res


def fmt_tr(triples):
    return "{" + ",".join("".join(str(e) for e in sorted(C)) for C in triples) + "}"


def make_instances(q, m_values, n_each, seed):
    rng = random.Random(seed)
    alltr = [tuple(c) for c in itertools.combinations(range(3 * q), 3)]
    yes, no = [], []
    seen = set()
    tries = 0
    while (len(yes) < n_each or len(no) < n_each) and tries < 100000:
        tries += 1
        m = rng.choice(m_values)
        tr = tuple(sorted(rng.sample(alltr, m)))
        if tr in seen:
            continue
        seen.add(tr)
        # nontrivial: the whole family is not itself an exact cover
        if m == q and x3c_yes(q, list(tr)):
            continue
        if x3c_yes(q, list(tr)):
            if len(yes) < n_each:
                yes.append(list(tr))
        elif len(no) < n_each:
            no.append(list(tr))
    return yes + no


def main():
    log("TCD001 -- check_strong.py (seed 20261003)")
    log("Reduction: X3C (q, triples C_1..C_m) -> Lasso with p = 3q+1, n = m+3q, rule C, target enter(0)")
    log("triple rows (rho/q ; 1 on C_i ; y=1), anchor rows (kappa*u/(3q) ; u at e ; y=S/u),")
    log("u = 3m, S = m, mu = S+1, eta = kappa-rho = 1/2, theta = 1/(24q), rho = 1-(eta*S-theta)/mu; data scaled to integers")
    log("")
    tot = dict(inst=0, yes=0, no=0, eq_ok=0, subsets=0, char_fail=0, uncert=0, uncert_entry=0, ties=0,
               inter_fail=0, inter_sign_fail=0, D_ok=0, lib_checked=0, lib_disagree=0)
    maxint = 0
    insts = [(2, tr) for tr in make_instances(2, [3, 4, 5, 6], 18, 20261003)]
    # two hand-made q = 2 instances: every element covered, no exact cover / exact cover hidden among overlaps
    insts.append((2, [(0, 1, 2), (2, 3, 4), (4, 5, 0), (1, 3, 5)]))     # NO
    insts.append((2, [(0, 1, 2), (0, 3, 4), (1, 3, 5), (3, 4, 5)]))     # YES ({012,345})
    q3 = [(3, [(0, 1, 2), (3, 4, 5), (6, 7, 8), (0, 3, 6)]),            # YES
          (3, [(0, 1, 2), (2, 3, 4), (5, 6, 7), (6, 7, 8)])]            # NO (no disjoint cover)
    for q, tr in insts + q3:
        t1 = time.process_time()
        r = check_instance(q, tr, intermediate=True, lib_sample=40 if q == 2 else 20, seed=len(tr) * 7 + q)
        dt = time.process_time() - t1
        tot["inst"] += 1
        tot["yes"] += r["yes"]
        tot["no"] += not r["yes"]
        tot["eq_ok"] += r["yes"] == r["witness"]
        for key in ("subsets", "char_fail", "uncert", "uncert_entry", "ties", "inter_fail", "inter_sign_fail",
                    "lib_checked", "lib_disagree"):
            tot[key] += r[key]
        tot["D_ok"] += r["D_ok"]
        par = r["par"]
        maxint = max(maxint, par["maxX"], par["maxy"])
        log(f"  q={q} m={len(tr)} {fmt_tr(tr)}: X3C={'YES' if r['yes'] else 'NO '} witness={'yes' if r['witness'] else 'no '}"
            f" f_enter={r['min_R']} | n={r['n']} p={r['p']} subsets={r['subsets']} entries={r['entries']}"
            f" char_fail={r['char_fail']} uncert={r['uncert']} (with entry {r['uncert_entry']}) ties={r['ties']}"
            f" inter_fail={r['inter_fail']} neg_coef={r['inter_sign_fail']} D_ok={r['D_ok']}"
            f" | lib {r['lib_disagree']}/{r['lib_checked']} | max|X|={par['maxX']} max|y|={par['maxy']} mu={par['mu_int']} | {dt:.1f}s")
    log("")
    log(f"SUMMARY: {tot['inst']} X3C instances ({tot['yes']} YES, {tot['no']} NO), rule C.")
    log(f"  equivalence (witness exists <=> X3C YES): {tot['eq_ok']}/{tot['inst']}")
    log(f"  set-by-set characterisation failures: {tot['char_fail']} over {tot['subsets']} subsets D\\R")
    log(f"  full data: target inactive and minimiser unique on {tot['D_ok']}/{tot['inst']}")
    log(f"  uniqueness not certified by rank(X_E) on {tot['uncert']} subsets, of which with the target in the found minimiser: {tot['uncert_entry']}")
    log(f"  KKT ties (|c_j| = mu with beta_j = 0) on {tot['ties']} subsets (expected: an anchored absorber covered once by the kept triples sits exactly at |c_e| = mu)")
    log(f"  intermediate claims (problem without target: support = anchored e with cov_e >= 2, |X_0'r| > mu iff predicted): {tot['inter_fail']} failures; negative coefficients: {tot['inter_sign_fail']}")
    log(f"  library cross-check (lasso_lars with KKT guard, float): {tot['lib_disagree']} support disagreements in {tot['lib_checked']} fits")
    log(f"  largest integer in the data over all instances: {maxint}")
    log(f"  exact solves {STATS['solves']}, enumeration fallbacks {STATS['fallbacks']}")
    log("")
    # negative controls: conditions of the proof violated; at least one failure expected for each
    log("NEGATIVE CONTROLS (each violates a condition of the proof; a failure must be detected):")
    ctrl_insts = [inst for inst in insts if inst[0] == 2][:8] + insts[-2:]
    controls = [("theta = 1/q (> eta/(6q))", dict(theta=F(1, 2))),
                ("theta = -1/(24q) (no margin)", dict(theta=F(-1, 48))),
                ("S = 0 (no offset)", dict(S=0)),
                ("u = 1 (no anchor dominance)", dict(u=1))]
    for name, ov in controls:
        nfail_eq = nfail_char = nfail_inter = 0
        for q, tr in ctrl_insts:
            ov2 = dict(ov)
            if "theta" in ov2:
                ov2["theta"] = ov2["theta"] if ov2["theta"] < 0 else F(1, q)
                if ov2["theta"] < 0:
                    ov2["theta"] = F(-1, 24 * q)
            r = check_instance(q, tr, override=ov2, intermediate=True, lib_sample=0)
            nfail_eq += r["yes"] != r["witness"]
            nfail_char += r["char_fail"]
            nfail_inter += r["inter_fail"]
        det = (nfail_eq + nfail_char + nfail_inter) > 0
        log(f"  {name}: equivalence failures {nfail_eq}/{len(ctrl_insts)}, characterisation failures {nfail_char},"
            f" intermediate failures {nfail_inter} -> {'DETECTED' if det else 'not detected'}")
    log("")
    log(f"total CPU time {time.process_time() - T0:.1f}s; lasso_lars KKT guard: {lf.kkt_stats()}")
    with open(os.path.join(HERE, "check_strong_output.txt"), "w") as fh:
        fh.write("\n".join(OUT) + "\n")


if __name__ == "__main__":
    main()
