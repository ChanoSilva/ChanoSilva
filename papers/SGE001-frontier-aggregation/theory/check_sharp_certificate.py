#!/usr/bin/env python3
"""SGE001 -- numerical check of the fourth-order ("sharp") certificate of improvement.

Theory note: theory/sharp_certificate_derivation.md; LaTeX block: theory/sharp_certificate.tex.

What is checked (nothing in experiments/, results/ or manuscript/ is modified):
  1. closed-form D^4 f of the Cobb-Douglas frontier (falling factorials) against central differences of the
     analytic third derivative of experiments/frontier_aggregation.py, and the generic (Faa di Bruno) CES
     derivatives against the analytic Hessian / third tensor of the experiment and central differences;
  2. E1 (Cobb-Douglas, LN and SU, N = 2000, 20 replications, the same generator and draws as the reference run):
     the identity E2 = C3 + E3 with C3 = (N/6)<D^3 f(xbar), mu3> (signed third central moment tensor),
     the bounds |E3| <= B3 and |E2| <= |C3| + B3 in every replication and cell, and the largest dispersion
     up to which the certificates hold in every replication, old ((k+1) B2 < |Q2|) against new
     ((k+1)(|C3| + B3) < |Q2|), k = 1 and k = 5, in moment-and-range (box) and micro-data (segmentwise) form,
     in the manuscript's Euclidean norm and in the coordinates scaled by xbar;
  3. the leading-order prediction of the certified dispersion (log-normal, population moments);
  4. E4 (no-capacity cells, the same draws as the reference run, all 1000 trials per cell): share of comparisons
     certified by the margin condition with the old and with the sharp bounds;
  5. (optional item) CES: certified suprema of ||D^3 f|| and ||D^4 f|| on boxes by interval enclosure of the
     Faa di Bruno formula, and the old and new certificates for CES on E1 (same draws).
Output: theory/check_sharp_certificate_output.txt and theory/sharp_certificate_results.json.
"""
import itertools
import json
import math
import os
import sys
import time

import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
sys.dont_write_bytecode = True          # do not write a .pyc into experiments/
sys.path.insert(0, os.path.join(ROOT, "experiments"))
import frontier_aggregation as fa  # noqa: E402  (classes, input laws, moments, aggregate; nothing is run)

OUT_TXT = os.path.join(HERE, "check_sharp_certificate_output.txt")
OUT_JSON = os.path.join(HERE, "sharp_certificate_results.json")
LINES = []


def say(*a):
    s = " ".join(str(x) for x in a)
    print(s, flush=True)
    LINES.append(s)


def falling(a, n):
    out = 1.0
    for r in range(n):
        out *= (a - r)
    return out


def counts(idx, d):
    e = np.zeros(d, int)
    for m in idx:
        e[m] += 1
    return e


# --------------------------------------------------------------------------- Cobb-Douglas, any order
def cd_coef(front, idx):
    """A * prod_m (a_m)_{e_m}: the entry of D^k f at x equals coef * prod_m x_m^{a_m - e_m}."""
    e = counts(idx, len(front.al))
    return front.A * np.prod([falling(front.al[m], e[m]) for m in range(len(front.al))])


def cd_deriv(front, x, k):
    """D^k f(x) as an array (..., d, ..., d) from the closed form."""
    d = len(front.al)
    x = np.asarray(x, float)
    T = np.zeros(x.shape[:-1] + (d,) * k)
    for idx in itertools.product(range(d), repeat=k):
        e = counts(idx, d)
        T[(...,) + idx] = cd_coef(front, idx) * np.prod(x ** (front.al - e), axis=-1)
    return T


def cd_box_sup(front, k, lo, hi, s=None):
    """Upper bound of sup_{y in [lo, hi]} ||D^k f(y)|| (Euclidean norm of h) or, with s, of
    sup ||D^k f(y)[s*., ..., s*.]|| (norm in the coordinates v = h / s): every entry is coef * prod x_m^{p_m},
    monotone in each coordinate, so its sup is at the corner hi_m (p_m > 0) or lo_m (p_m < 0); the Frobenius
    norm of the entrywise sups dominates the operator norm."""
    d = len(front.al)
    tot = 0.0
    for idx in itertools.product(range(d), repeat=k):
        e = counts(idx, d)
        c = abs(cd_coef(front, idx))
        if c == 0.0:
            continue
        v = c * np.ones(np.broadcast(lo[..., 0], hi[..., 0]).shape)
        for m in range(d):
            p = front.al[m] - e[m]
            if p > 0:
                v = v * hi[..., m] ** p
            elif p < 0:
                v = v * lo[..., m] ** p
            if s is not None and e[m] > 0:
                v = v * s[..., m] ** e[m]
        tot = tot + v ** 2
    return np.sqrt(tot)


# --------------------------------------------------------------------------- CES, any order (Faa di Bruno)
def set_partitions(seq):
    if len(seq) == 1:
        yield [seq]
        return
    first, rest = seq[0], seq[1:]
    for p in set_partitions(rest):
        for i in range(len(p)):
            yield p[:i] + [[first] + p[i]] + p[i + 1:]
        yield [[first]] + p


def ces_terms(front, idx):
    """f = A S^beta, S = sum_j a_j x_j^rho (separable).  d^k f / dx_idx = sum over set partitions pi of the
    positions with constant index on each block of  coef(pi) * S^(beta - |pi|) * prod_j x_j^(expo_j(pi))."""
    beta, rho, d = front.nu / front.rho, front.rho, len(front.a)
    terms = []
    for pi in set_partitions(list(range(len(idx)))):
        js = []
        ok = True
        for B in pi:
            vals = {idx[p] for p in B}
            if len(vals) > 1:
                ok = False
                break
            js.append(idx[B[0]])
        if not ok:
            continue
        r = len(pi)
        c = front.A * falling(beta, r)
        ex = np.zeros(d)
        for B, j in zip(pi, js):
            c *= front.a[j] * falling(rho, len(B))
            ex[j] += rho - len(B)
        terms.append((c, beta - r, ex))
    return terms


def ces_deriv(front, x, k):
    d = len(front.a)
    x = np.asarray(x, float)
    S = front._S(x)
    T = np.zeros(x.shape[:-1] + (d,) * k)
    for idx in itertools.product(range(d), repeat=k):
        val = 0.0
        for c, ps, ex in ces_terms(front, idx):
            val = val + c * S ** ps * np.prod(x ** ex, axis=-1)
        T[(...,) + idx] = val
    return T


def ces_box_sup(front, k, lo, hi, s=None):
    """Rigorous enclosure of
    sup_{y in box} ||D^k f(y)|| for CES with rho < 0 and beta = nu/rho < 0: every Faa di Bruno term is
    coef * S^(beta - r) * prod_j x_j^(ex_j) with negative exponents, and S = sum a_j x_j^rho is decreasing in
    each x_j; so each positive factor lies between its values at the two corners, the interval of every entry
    is the sum of the term intervals, and the Frobenius norm of the entrywise sup |.| bounds the norm.
    Rounding: a relative margin 1e-9 and an absolute margin 1e-12 * sum |terms| per entry (the rounding error of
    these few dozen floating-point operations is below 1e-14 * sum |terms|)."""
    assert front.rho < 0 and front.nu / front.rho < 0
    d = len(front.a)
    S_lo_corner = front._S(lo)          # largest S on the box
    S_hi_corner = front._S(hi)          # smallest S on the box
    tot = 0.0
    for idx in itertools.product(range(d), repeat=k):
        L = 0.0
        U = 0.0
        absum = 0.0
        for c, ps, ex in ces_terms(front, idx):
            assert ps < 0 and np.all(ex <= 0)
            pmin = S_lo_corner ** ps * np.prod(hi ** ex, axis=-1)
            pmax = S_hi_corner ** ps * np.prod(lo ** ex, axis=-1)
            absum = absum + abs(c) * pmax
            if c >= 0:
                L, U = L + c * pmin, U + c * pmax
            else:
                L, U = L + c * pmax, U + c * pmin
        v = np.maximum(np.abs(L), np.abs(U)) * (1 + 1e-9) + 1e-12 * absum   # covers floating-point rounding
        if s is not None:
            e = counts(idx, d)
            for m in range(d):
                v = v * s[..., m] ** e[m]
        tot = tot + v ** 2
    return np.sqrt(tot)


def ces_box_sup_sub(front, k, lo, hi, s=None, n=4):
    """Same enclosure, maximised over an n x n geometric subdivision of each (two-dimensional) box."""
    best = 0.0
    r = (hi / lo) ** (1.0 / n)
    for i in range(n):
        for j in range(n):
            l = lo * np.stack([r[..., 0] ** i, r[..., 1] ** j], axis=-1)
            h = l * r
            best = np.maximum(best, ces_box_sup(front, k, l, h, s))
    return best


# --------------------------------------------------------------------------- bounds for one cell
def sharp_terms(front, X, kind, sub=1):
    """Old and new bound ingredients for populations X (T, N, d).  kind: 'CD' or 'CES'."""
    T, N, d = X.shape
    xb, Sig, mu3, s2, m3 = fa.moments(X)
    Hc = X - xb[:, None, :]
    V = Hc / xb[:, None, :]                                   # coordinates scaled by xbar
    hn = np.sqrt(np.sum(Hc ** 2, axis=2))
    vn = np.sqrt(np.sum(V ** 2, axis=2))
    D3 = front.third(xb)
    C3 = N / 6.0 * np.einsum("tijk,tijk->t", D3, mu3)          # signed third-moment term = Yhat3 - Yhat2
    m4, m4s, m3s = np.mean(hn ** 4, axis=1), np.mean(vn ** 4, axis=1), np.mean(vn ** 3, axis=1)
    glo, ghi = X.min(axis=1), X.max(axis=1)                    # coordinate box of the population
    slo, shi = np.minimum(X, xb[:, None, :]), np.maximum(X, xb[:, None, :])   # box spanned by xbar and x_i
    sb = xb[:, None, :]
    if kind == "CD":
        sup = lambda k, lo, hi, s=None: cd_box_sup(front, k, lo, hi, s)
        supg = sup
    else:
        sup = lambda k, lo, hi, s=None: ces_box_sup(front, k, lo, hi, s)
        supg = lambda k, lo, hi, s=None: ces_box_sup_sub(front, k, lo, hi, s, n=sub)
    out = {"C3": C3, "m4": m4}
    # old bounds (third order) -- euclidean and scaled
    out["B2box"] = N / 6.0 * supg(3, glo, ghi) * m3
    out["B2seg"] = np.sum(sup(3, slo, shi) * hn ** 3, axis=1) / 6.0
    out["B2box_s"] = N / 6.0 * supg(3, glo, ghi, xb) * m3s
    out["B2seg_s"] = np.sum(sup(3, slo, shi, sb) * vn ** 3, axis=1) / 6.0
    # new bounds: fourth-order remainder
    out["B3box"] = N / 24.0 * supg(4, glo, ghi) * m4
    out["B3seg"] = np.sum(sup(4, slo, shi) * hn ** 4, axis=1) / 24.0
    out["B3box_s"] = N / 24.0 * supg(4, glo, ghi, xb) * m4s
    out["B3seg_s"] = np.sum(sup(4, slo, shi, sb) * vn ** 4, axis=1) / 24.0
    out["M3box_s"] = supg(3, glo, ghi, xb)
    out["M4box_s"] = supg(4, glo, ghi, xb)
    return out


VARIANTS = [  # (label, kind, bound key)  kind: old -> B2 ; new -> |C3| + B3
    ("old moment-and-range (euclid., manuscript)", "old", "B2box"),
    ("old micro-data (euclid., manuscript)", "old", "B2seg"),
    ("old moment-and-range (scaled by xbar)", "old", "B2box_s"),
    ("old micro-data (scaled by xbar)", "old", "B2seg_s"),
    ("NEW moment-and-range (euclid.)", "new", "B3box"),
    ("NEW micro-data (euclid.)", "new", "B3seg"),
    ("NEW moment-and-range (scaled by xbar)", "new", "B3box_s"),
    ("NEW micro-data (scaled by xbar)", "new", "B3seg_s"),
]


def bound_of(R, kind, key):
    return R[key] if kind == "old" else np.abs(R["C3"]) + R[key]


def largest_uniform(sigmas, flags):
    out = 0.0
    for s, f in zip(sigmas, flags):
        if f:
            out = s
        else:
            break
    return float(out)


def main():
    t0, c0 = time.time(), time.process_time()
    res = {"meta": {"seed": fa.SEED, "script": "theory/check_sharp_certificate.py",
                    "numpy": np.__version__, "python": sys.version.split()[0]}}
    ref = json.load(open(os.path.join(ROOT, "results", "results.json")))
    gens = [np.random.default_rng(s) for s in np.random.SeedSequence(fa.SEED).spawn(12)]
    names = ["E0", "E1", "E1b", "E1c", "E2", "E3", "E4", "E5", "boot", "bootE2", "bootE3", "bootE1c"]
    G = dict(zip(names, gens))
    cd, ces = fa.CobbDouglas(), fa.CES()

    # ------------------------------------------------------------------ 1. derivative checks
    say("=" * 100)
    say("1. Derivative checks")
    rng = np.random.default_rng(12345)
    worst = {"CD_D3_closed_vs_code": 0.0, "CD_D4_vs_FD": 0.0, "CD_box_vs_code_M2": 0.0, "CD_box_vs_code_M3": 0.0,
             "CES_D2_generic_vs_code": 0.0, "CES_D3_generic_vs_code": 0.0, "CES_D4_vs_FD": 0.0,
             "CES_enclosure_violations": 0, "CD_box_violations": 0}
    for _ in range(40):
        x = np.exp(rng.uniform(-0.7, 0.7, size=2))
        worst["CD_D3_closed_vs_code"] = max(worst["CD_D3_closed_vs_code"],
                                            float(np.max(np.abs(cd_deriv(cd, x, 3) - cd.third(x)) / np.abs(cd.third(x)))))
        worst["CES_D2_generic_vs_code"] = max(worst["CES_D2_generic_vs_code"],
                                              float(np.max(np.abs(ces_deriv(ces, x, 2) - ces.hess(x)) / np.abs(ces.hess(x)))))
        worst["CES_D3_generic_vs_code"] = max(worst["CES_D3_generic_vs_code"],
                                              float(np.max(np.abs(ces_deriv(ces, x, 3) - ces.third(x)) / np.abs(ces.third(x)))))
        for name, D4, D3 in (("CD", cd_deriv(cd, x, 4), lambda y: cd.third(y)), ("CES", ces_deriv(ces, x, 4), lambda y: ces.third(y))):
            for j in range(2):
                e = np.zeros(2)
                e[j] = 1e-5 * x[j]
                fd = (D3(x + e) - D3(x - e)) / (2 * e[j])
                worst[f"{name}_D4_vs_FD"] = max(worst[f"{name}_D4_vs_FD"],
                                                float(np.max(np.abs(fd - D4[..., j]) / np.maximum(np.abs(D4[..., j]), 1e-12))))
        # box sups: agree with the experiment's box_bounds (k = 2, 3) and dominate the norm at random box points
        lo = x * np.exp(-rng.uniform(0, 0.5, 2))
        hi = x * np.exp(rng.uniform(0, 0.5, 2))
        M2, M3 = cd.box_bounds(lo, hi)
        worst["CD_box_vs_code_M2"] = max(worst["CD_box_vs_code_M2"], abs(cd_box_sup(cd, 2, lo, hi) / M2 - 1))
        worst["CD_box_vs_code_M3"] = max(worst["CD_box_vs_code_M3"], abs(cd_box_sup(cd, 3, lo, hi) / M3 - 1))
        for _ in range(20):
            y = lo + rng.uniform(size=2) * (hi - lo)
            for k in (3, 4):
                if np.sqrt(np.sum(cd_deriv(cd, y, k) ** 2)) > cd_box_sup(cd, k, lo, hi) * (1 + 1e-12):
                    worst["CD_box_violations"] += 1
                if np.sqrt(np.sum(ces_deriv(ces, y, k) ** 2)) > ces_box_sup(ces, k, lo, hi):
                    worst["CES_enclosure_violations"] += 1
    for k_, v in worst.items():
        say(f"   {k_:32s} {v:.3e}" if isinstance(v, float) else f"   {k_:32s} {v}")
    assert worst["CD_D4_vs_FD"] < 1e-5 and worst["CES_D4_vs_FD"] < 1e-5
    assert worst["CD_D3_closed_vs_code"] < 1e-12 and worst["CES_D3_generic_vs_code"] < 1e-10
    assert worst["CES_enclosure_violations"] == 0 and worst["CD_box_violations"] == 0
    res["derivative_checks"] = worst

    # ------------------------------------------------------------------ 2. E1, Cobb-Douglas (and CES draws)
    say("=" * 100)
    say("2. E1 reproduction (N = 2000, 20 replications, generator 'E1' of SeedSequence(SEED).spawn(12)) ")
    rngE1 = G["E1"]
    N, R = 2000, 20
    xbar = np.array([2.0, 1.0])
    grids = {"LN": np.logspace(-2, 0, 17), "SU": np.logspace(-2, math.log10(0.5), 15)}
    Zs = {}
    for fname in ("CD", "CES"):                 # same order of draws as run_E1
        for law in ("LN", "SU"):
            Zs[(fname, law)] = fa.base_noise(rngE1, R, N, law)
    refrows = {(r["frontier"], r["law"], round(r["sigma"], 10)): r for r in ref["E1"]["rows"]}
    res["E1"] = {}
    for fname, front in (("CD", cd), ("CES", ces)):
        for law in ("LN", "SU"):
            sig_grid = grids[law]
            cells = []
            for s in sig_grid:
                X = fa.inputs(xbar, s, Zs[(fname, law)], law)
                A = fa.aggregate(front, X, bounds=(fname == "CD"))
                Rb = sharp_terms(front, X, fname, sub=4)
                r21 = np.abs(A["E1"]) / np.abs(A["E2"])
                rr = refrows[(fname, law, round(float(s), 10))]
                cell = {"sigma": float(s), "repro_r21_min_reldiff": abs(r21.min() / rr["r21_min"] - 1),
                        "r21_min": float(r21.min())}
                if fname == "CD":       # reproduction of the manuscript's bounds
                    cell["repro_B2_reldiff"] = float(np.max(np.abs(Rb["B2seg"] / A["B2"] - 1)))
                    cell["repro_B2box_reldiff"] = float(np.max(np.abs(Rb["B2box"] / A["B2box"] - 1)))
                    cell["repro_cert_flags"] = int(int(np.all(2 * A["B2"] < np.abs(A["Q2"]))) == rr["cert_obs_holds_all"]
                                                   and int(np.all(2 * A["B2box"] < np.abs(A["Q2"]))) == rr["cert_box_holds_all"])
                # identity and bounds
                E2, E3, Q2, C3 = A["E2"], A["E3"], A["Q2"], Rb["C3"]
                cell["identity_E2_eq_C3_plus_E3"] = float(np.max(np.abs(E2 - (C3 + E3)) / np.abs(A["Y"])))
                for lab, kind, key in VARIANTS:
                    Bd = bound_of(Rb, kind, key)
                    cell[f"holds|{key}"] = int(np.all(np.abs(E2) <= Bd))
                    if kind == "new":
                        cell[f"holdsE3|{key}"] = int(np.all(np.abs(E3) <= Rb[key]))
                        cell[f"maxE3overB3|{key}"] = float(np.max(np.abs(E3) / Rb[key]))
                    cell[f"maxE2overB|{key}"] = float(np.max(np.abs(E2) / Bd))
                    for k in (1, 5):
                        cell[f"cert{k}|{key}"] = int(np.all((k + 1) * Bd < np.abs(Q2)))
                        cell[f"certfrac{k}|{key}"] = float(np.mean((k + 1) * Bd < np.abs(Q2)))
                        if kind == "new":   # signed form |Q2 + C3| - B3 > k (|C3| + B3)
                            sg = np.abs(Q2 + C3) - Rb[key] > k * Bd
                            cell[f"certsigned{k}|{key}"] = int(np.all(sg))
                        # the certificate must imply the improvement it certifies
                        c_ok = (k + 1) * Bd < np.abs(Q2)
                        cell[f"cert_implies{k}|{key}"] = int(np.all(r21[c_ok] > k)) if c_ok.any() else 1
                cell["ratio_C3_over_Q2_med"] = float(np.median(np.abs(C3 / Q2)))
                cell["ratio_B3s_over_Q2_med"] = float(np.median(Rb["B3box_s"] / np.abs(Q2)))
                cell["ratio_B2s_over_Q2_med"] = float(np.median(Rb["B2box_s"] / np.abs(Q2)))
                cell["M4box_s_med"] = float(np.median(Rb["M4box_s"]))
                cell["M3box_s_med"] = float(np.median(Rb["M3box_s"]))
                cells.append(cell)
            sig = [c["sigma"] for c in cells]
            summ = {"cells": len(cells),
                    "observed_r21_gt1": largest_uniform(sig, [c["r21_min"] > 1 for c in cells]),
                    "observed_r21_ge5": largest_uniform(sig, [c["r21_min"] >= 5 for c in cells]),
                    "observed_r21_gt5": largest_uniform(sig, [c["r21_min"] > 5 for c in cells]),
                    "identity_max": max(c["identity_E2_eq_C3_plus_E3"] for c in cells),
                    "repro_r21_max_reldiff": max(c["repro_r21_min_reldiff"] for c in cells)}
            if fname == "CD":
                summ["repro_B2_max_reldiff"] = max(c["repro_B2_reldiff"] for c in cells)
                summ["repro_B2box_max_reldiff"] = max(c["repro_B2box_reldiff"] for c in cells)
                summ["repro_cert_flags_all"] = int(all(c["repro_cert_flags"] for c in cells))
            for lab, kind, key in VARIANTS:
                summ[f"bound_holds_all|{key}"] = int(all(c[f"holds|{key}"] for c in cells))
                summ[f"maxE2overB|{key}"] = max(c[f"maxE2overB|{key}"] for c in cells)
                if kind == "new":
                    summ[f"boundE3_holds_all|{key}"] = int(all(c[f"holdsE3|{key}"] for c in cells))
                    summ[f"maxE3overB3|{key}"] = max(c[f"maxE3overB3|{key}"] for c in cells)
                for k in (1, 5):
                    summ[f"sigma_cert{k}|{key}"] = largest_uniform(sig, [c[f"cert{k}|{key}"] for c in cells])
                    summ[f"cert_implies{k}|{key}"] = int(all(c[f"cert_implies{k}|{key}"] for c in cells))
                    if kind == "new":
                        summ[f"sigma_certsigned{k}|{key}"] = largest_uniform(sig, [c[f"certsigned{k}|{key}"] for c in cells])
            res["E1"][f"{fname}-{law}"] = {"summary": summ, "cells": cells}
            # ---- print
            say("-" * 100)
            say(f"E1 {fname}-{law}: grid of {len(cells)} dispersions; reproduction: max rel. diff of min|E1|/|E2| vs results.json "
                f"{summ['repro_r21_max_reldiff']:.1e}" + (f"; of B2 (segment) {summ['repro_B2_max_reldiff']:.1e}, of B2box "
                f"{summ['repro_B2box_max_reldiff']:.1e}; certificate flags identical: {summ['repro_cert_flags_all']}" if fname == "CD" else ""))
            say(f"   identity E2 = C3 + E3: max |E2 - C3 - E3| / Y = {summ['identity_max']:.1e}")
            say(f"   observed (every replication): |E1|/|E2| > 1 up to sigma = {summ['observed_r21_gt1']:.4f};  >= 5 up to {summ['observed_r21_ge5']:.4f}")
            say(f"   {'variant':45s} {'bound holds':>11s} {'max|E2|/B':>10s} {'max|E3|/B3':>11s} {'sig* k=1':>9s} {'sig* k=5':>9s} {'signed k=1':>10s} {'signed k=5':>10s}")
            for lab, kind, key in VARIANTS:
                e3 = f"{summ[f'maxE3overB3|{key}']:.2e}" if kind == "new" else "-"
                sg1 = f"{summ[f'sigma_certsigned1|{key}']:.4f}" if kind == "new" else "-"
                sg5 = f"{summ[f'sigma_certsigned5|{key}']:.4f}" if kind == "new" else "-"
                say(f"   {lab:45s} {summ[f'bound_holds_all|{key}']:>11d} {summ[f'maxE2overB|{key}']:>10.2e} {e3:>11s} "
                    f"{summ[f'sigma_cert1|{key}']:>9.4f} {summ[f'sigma_cert5|{key}']:>9.4f} {sg1:>10s} {sg5:>10s}")
            say(f"   per-cell share of replications certified (k = 1), main variants:")
            say(f"   {'sigma':>7s} {'min r21':>9s} {'old box':>8s} {'old seg':>8s} {'new box':>8s} {'new seg':>8s} {'new box_s':>9s} {'new seg_s':>9s} "
                f"{'|C3|/|Q2|':>10s} {'B3box_s/|Q2|':>12s} {'B2box_s/|Q2|':>12s}")
            for c in cells:
                say(f"   {c['sigma']:7.4f} {c['r21_min']:9.2f} {c['certfrac1|B2box']:8.2f} {c['certfrac1|B2seg']:8.2f} "
                    f"{c['certfrac1|B3box']:8.2f} {c['certfrac1|B3seg']:8.2f} {c['certfrac1|B3box_s']:9.2f} {c['certfrac1|B3seg_s']:9.2f} "
                    f"{c['ratio_C3_over_Q2_med']:10.2e} {c['ratio_B3s_over_Q2_med']:12.2e} {c['ratio_B2s_over_Q2_med']:12.2e}")
            # consistency with the reference results.json (Cobb-Douglas)
            if fname == "CD":
                rs = ref["E1"]["summary"][f"CD-{law}"]
                say(f"   reference results.json: sigma_largest_cert_box = {rs['sigma_largest_cert_box']:.4f}, "
                    f"cert_observable = {rs['sigma_largest_cert_observable']:.4f}, c1_box = {rs['sigma_largest_cert_c1_box']:.4f}, "
                    f"c1 = {rs['sigma_largest_cert_c1']:.4f}")
                assert abs(summ["sigma_cert1|B2box"] - rs["sigma_largest_cert_box"]) < 1e-12
                assert abs(summ["sigma_cert1|B2seg"] - rs["sigma_largest_cert_observable"]) < 1e-12
                assert abs(summ["sigma_cert5|B2box"] - rs["sigma_largest_cert_c1_box"]) < 1e-12
                assert abs(summ["sigma_cert5|B2seg"] - rs["sigma_largest_cert_c1"]) < 1e-12
            for lab, kind, key in VARIANTS:
                assert summ[f"bound_holds_all|{key}"] == 1, (fname, law, key)
                assert summ[f"cert_implies1|{key}"] == 1 and summ[f"cert_implies5|{key}"] == 1
    res["meta"]["E1_cpu_seconds"] = time.process_time() - c0

    # ------------------------------------------------------------------ 3. leading-order prediction (LN, scaled coords)
    say("=" * 100)
    say("3. Leading-order prediction, log-normal inputs, coordinates scaled by xbar (population moments, no range inflation)")
    rho = fa.CORR
    P = np.array([[1, rho], [rho, 1.0]])
    fx = float(cd.f(xbar))
    k2 = cd_deriv(cd, xbar, 2) * np.outer(xbar, xbar) / fx          # = kappa_2 (dimensionless)
    k3 = cd_deriv(cd, xbar, 3) * np.einsum("i,j,k->ijk", xbar, xbar, xbar) / fx
    k4 = cd_deriv(cd, xbar, 4) * np.einsum("i,j,k,l->ijkl", xbar, xbar, xbar, xbar) / fx
    qcoef = float(np.sum(k2 * P))                                    # tr(H Sigma) = f sigma^2 q
    mu3z = np.einsum("jk,jl->jkl", P, P) + np.einsum("jk,kl->jkl", P, P) + np.einsum("jl,kl->jkl", P, P)
    c3coef = float(np.sum(k3 * mu3z))                                # <kappa3, mu3_rel> = sigma^4 c3 + O(sigma^5)
    mu4z = np.einsum("jk,lm->jklm", P, P) + np.einsum("jl,km->jklm", P, P) + np.einsum("jm,kl->jklm", P, P)
    e4coef = float(np.sum(k4 * mu4z))                                # <kappa4, mu4_rel> = sigma^4 e4 + O(sigma^5)
    zz = np.random.default_rng(7).standard_normal((2_000_000, 2)) @ np.linalg.cholesky(P).T
    Ez3 = float(np.mean(np.sum(zz ** 2, axis=1) ** 1.5))
    Ez4 = 3 + 3 + 2 * (1 + 2 * rho ** 2)
    nk3, nk4 = float(np.sqrt(np.sum(k3 ** 2))), float(np.sqrt(np.sum(k4 ** 2)))
    # |Q2|/N = f |q| s^2/2;  B2/N = f nk3 E|z|^3 s^3/6;  |C3|/N = f |c3| s^4/6;  B3/N = f nk4 E|z|^4 s^4/24
    a_old = nk3 * Ez3 / 3 / abs(qcoef)                               # B2/|Q2| = a_old * sigma
    a_new = (abs(c3coef) / 3 + nk4 * Ez4 / 12) / abs(qcoef)          # (|C3| + B3)/|Q2| = a_new * sigma^2
    a_true = abs(c3coef / 3 + e4coef / 12) / abs(qcoef)              # |E2|/|Q2| = a_true * sigma^2 (population)
    pred = {"q": qcoef, "c3": c3coef, "e4": e4coef, "norm_kappa3_F": nk3, "norm_kappa4_F": nk4, "E_norm_z_cubed": Ez3,
            "E_norm_z_fourth": Ez4, "a_old": a_old, "a_new": a_new, "a_true": a_true}
    for k in (1, 5):
        pred[f"sigma_old_k{k}"] = 1 / ((k + 1) * a_old)
        pred[f"sigma_new_k{k}"] = 1 / math.sqrt((k + 1) * a_new)
        pred[f"sigma_true_k{k}"] = 1 / math.sqrt((k + 1) * a_true)
    res["prediction_LN_scaled"] = pred
    say(f"   q = {qcoef:.4f}, c3 = {c3coef:.4f}, e4 = {e4coef:.4f}, ||kappa3||_F = {nk3:.4f}, ||kappa4||_F = {nk4:.4f}, "
        f"E||z||^3 = {Ez3:.4f}, E||z||^4 = {Ez4:.1f}")
    say(f"   old  B2/|Q2|        ~ {a_old:.3f} sigma      -> sigma*(k=1) = {pred['sigma_old_k1']:.3f}, sigma*(k=5) = {pred['sigma_old_k5']:.3f}")
    say(f"   new (|C3|+B3)/|Q2|  ~ {a_new:.3f} sigma^2    -> sigma*(k=1) = {pred['sigma_new_k1']:.3f}, sigma*(k=5) = {pred['sigma_new_k5']:.3f}")
    say(f"   true |E2|/|Q2|      ~ {a_true:.3f} sigma^2    -> ratio > k+1 ... up to sigma = {pred['sigma_true_k1']:.3f} (k=1), {pred['sigma_true_k5']:.3f} (k=5)")
    say("   (no range inflation: the measured certificates are smaller because M3, M4 are taken over the box of the sample)")
    # range-aware prediction: population moments of the relative deviations (large fixed-seed sample of the standard
    # shocks) and the box xbar * [u_lo, u_hi] given by the median sample range of N = 2000 units (LN) or the support (SU)
    from scipy.stats import norm as _norm
    zbig = np.random.default_rng(8).standard_normal((200_000, 2)) @ np.linalg.cholesky(P).T
    wbig = math.sqrt(3.0) * (2.0 * _norm.cdf(zbig) - 1.0)
    zmax = float(_norm.ppf((1 + 0.5 ** (1 / (2 * N))) / 2))        # median of max |z| over 2N standard normals
    T2s = cd_deriv(cd, xbar, 2) * np.outer(xbar, xbar)
    T3s = cd_deriv(cd, xbar, 3) * np.einsum("i,j,k->ijk", xbar, xbar, xbar)
    pred["zmax_median_N2000"] = zmax
    say(f"   Range-aware prediction (scaled coordinates; population moments; box from the median range, z_max = {zmax:.3f} for LN,")
    say(f"   the support 1 +- sqrt(3) sigma for SU), compared with the measured moment-and-range certificates (scaled), grid-limited:")
    for law in ("LN", "SU"):
        sg = np.linspace(0.002, 0.5, 250)
        r_old, r_new, sgs = [], [], []
        for sv in sg:
            if law == "LN":
                V = np.exp(sv * zbig - sv ** 2 / 2) - 1
                ulo, uhi = math.exp(-sv * zmax - sv ** 2 / 2), math.exp(sv * zmax - sv ** 2 / 2)
            else:
                V = sv * wbig
                ulo, uhi = 1 - math.sqrt(3) * sv, 1 + math.sqrt(3) * sv
                if ulo <= 0.05:
                    break
            V = V - V.mean(axis=0)
            q2 = 0.5 * abs(float(np.sum(T2s * (V.T @ V / len(V)))))
            c3 = abs(float(np.sum(T3s * np.einsum("ni,nj,nk->ijk", V, V, V) / len(V)))) / 6 if law == "LN" else 0.0
            vn = np.sqrt(np.sum(V ** 2, axis=1))
            lo, hi = xbar * ulo, xbar * uhi
            M3 = float(cd_box_sup(cd, 3, lo, hi, xbar))
            M4 = float(cd_box_sup(cd, 4, lo, hi, xbar))
            r_old.append(M3 * np.mean(vn ** 3) / 6 / q2)
            r_new.append((c3 + M4 * np.mean(vn ** 4) / 24) / q2)
            sgs.append(sv)
        for k in (1, 5):
            so = largest_uniform(sgs, [(k + 1) * r < 1 for r in r_old])
            sn = largest_uniform(sgs, [(k + 1) * r < 1 for r in r_new])
            pred[f"range_aware_{law}_old_k{k}"] = so
            pred[f"range_aware_{law}_new_k{k}"] = sn
            m = res["E1"][f"CD-{law}"]["summary"]
            say(f"   {law} k={k}: predicted old {so:.3f}, new {sn:.3f};  measured (scaled, moment-and-range) old "
                f"{m[f'sigma_cert{k}|B2box_s']:.4f}, new {m[f'sigma_cert{k}|B3box_s']:.4f}")

    # ------------------------------------------------------------------ 4. E4 margin condition, no-capacity cells
    say("=" * 100)
    say("4. E4, cells without capacity (N = 500 per sector, all 1000 trials, generator 'E4', same draws as the reference run)")
    rngE4 = G["E4"]
    N4, trials = 500, 1000
    xbarA = np.array([2.0, 1.0])
    deg = float(cd.al.sum())
    res["E4"] = []
    refE4 = {r["sigma"]: r for r in ref["E4"]["rows"] if r["prox"] == "none"}
    say(f"   {'sigma':>6s} {'old seg':>8s} {'old box':>8s} {'old seg_s':>9s} {'old box_s':>9s} | {'new seg':>8s} {'new box':>8s} {'new seg_s':>9s} {'new box_s':>9s} | "
        f"{'int seg_s':>9s} {'int box_s':>9s} {'int box':>8s} | {'rev2':>6s} {'cert.rev':>8s}")
    for s in [0.02, 0.05, 0.1, 0.2, 0.4, 0.8]:
        ZA = fa.base_noise(rngE4, trials, N4, "LN")
        ZB = fa.base_noise(rngE4, trials, N4, "LN")
        gamma = rngE4.uniform(-0.05, 0.05, size=trials)
        xbarB = xbarA[None, :] * (1.0 + gamma)[:, None] ** (1.0 / deg)
        XA = fa.inputs(xbarA, s, ZA, "LN")
        XB = fa.inputs(xbarB, s / 2.0, ZB, "LN")
        A = fa.aggregate(cd, XA)
        B = fa.aggregate(cd, XB)
        RA, RB = sharp_terms(cd, XA, "CD"), sharp_terms(cd, XB, "CD")
        true = np.sign(A["Y"] - B["Y"])
        d2 = A["Y2"] - B["Y2"]
        d3 = A["Y3"] - B["Y3"]
        row = {"sigma": s}
        # old margin (reproduction)
        row["old_seg"] = float(np.mean(np.abs(d2) > A["B2"] + B["B2"]))
        row["old_box"] = float(np.mean(np.abs(d2) > A["B2box"] + B["B2box"]))
        row["old_seg_s"] = float(np.mean(np.abs(d2) > RA["B2seg_s"] + RB["B2seg_s"]))
        row["old_box_s"] = float(np.mean(np.abs(d2) > RA["B2box_s"] + RB["B2box_s"]))
        assert abs(row["old_seg"] - refE4[s]["certified_frac"]) < 1e-12 and abs(row["old_box"] - refE4[s]["certified_box_frac"]) < 1e-12
        nrev = 0
        for key in ("B3seg", "B3box", "B3seg_s", "B3box_s"):
            # plug-in: Prop. margin with B = |C3| + B3 around Yhat2 (certifies sign of Yhat2 difference)
            m = np.abs(d2) > (np.abs(RA["C3"]) + RA[key]) + (np.abs(RB["C3"]) + RB[key])
            row[f"new_{key}"] = float(np.mean(m))
            nrev += int(np.sum(m & (np.sign(d2) != true)))
            # interval form: Y^A - Y^B lies within B3^A + B3^B of Yhat3^A - Yhat3^B; certifies the true ordering,
            # and the second-order ordering when sign(d2) = sign(d3)
            mi = np.abs(d3) > RA[key] + RB[key]
            row[f"int_{key}"] = float(np.mean(mi & (np.sign(d2) == np.sign(d3))))
            row[f"int_truth_{key}"] = float(np.mean(mi))
            nrev += int(np.sum(mi & (np.sign(d3) != true)))
        row["rev2"] = float(np.mean(np.sign(d2) != true))
        row["certified_reversals_new"] = nrev
        assert nrev == 0
        res["E4"].append(row)
        say(f"   {s:6.2f} {100*row['old_seg']:7.1f}% {100*row['old_box']:7.1f}% {100*row['old_seg_s']:8.1f}% {100*row['old_box_s']:8.1f}% | {100*row['new_B3seg']:7.1f}% {100*row['new_B3box']:7.1f}% "
            f"{100*row['new_B3seg_s']:8.1f}% {100*row['new_B3box_s']:8.1f}% | {100*row['int_B3seg_s']:8.1f}% {100*row['int_B3box_s']:8.1f}% "
            f"{100*row['int_B3box']:7.1f}% | {100*row['rev2']:5.1f}% {nrev:8d}")
    say("   old/new: margin condition |Yhat2^A - Yhat2^B| > B^A + B^B with B = B2 (old) or |C3| + B3 (new);")
    say("   int: |Yhat3^A - Yhat3^B| > B3^A + B3^B and sign agrees with the second-order difference (certifies the second-order ordering);")
    say("   cert.rev = reversals among all certified comparisons of the new variants (must be 0).")

    # ------------------------------------------------------------------ 5. CES suprema (summary)
    say("=" * 100)
    say("5. CES: enclosure of sup ||D^3 f||, sup ||D^4 f|| on boxes (Faa di Bruno + monotone factors; 4 x 4 subdivision for")
    say("   the coordinate box of the population, none for the segment boxes); certificates on E1 printed in section 2.")
    for law in ("LN", "SU"):
        c = res["E1"][f"CES-{law}"]["cells"]
        say(f"   CES-{law}: median scaled M3 over the box at the smallest / largest sigma: {c[0]['M3box_s_med']:.4f} / {c[-1]['M3box_s_med']:.4f}; "
            f"M4: {c[0]['M4box_s_med']:.4f} / {c[-1]['M4box_s_med']:.4f}")
    # tightness of the CES enclosure: enclosure over the population box against the largest Frobenius norm found on a
    # 41 x 41 grid of the same box (a lower bound of the true supremum of the Frobenius norm), first replication
    tight = {}
    for law in ("LN", "SU"):
        for sv in (0.01, 0.1):
            X = fa.inputs(xbar, sv, Zs[("CES", law)][:1], law)
            xb = X.mean(axis=1)
            lo, hi = X.min(axis=1)[0], X.max(axis=1)[0]
            g = np.stack(np.meshgrid(np.geomspace(lo[0], hi[0], 41), np.geomspace(lo[1], hi[1], 41)), axis=-1).reshape(-1, 2)
            for k in (3, 4):
                enc = float(ces_box_sup_sub(ces, k, lo, hi, xb[0], n=4))
                Dk = ces_deriv(ces, g, k)
                sc = xb[0]
                for ax in range(k):
                    shape = [1] * (k + 1)
                    shape[ax + 1] = 2
                    Dk = Dk * sc.reshape(shape)
                grid_max = float(np.max(np.sqrt(np.sum(Dk.reshape(len(g), -1) ** 2, axis=1))))
                tight[f"{law}_sigma{sv}_k{k}"] = enc / grid_max
                say(f"   CES-{law} sigma = {sv}: enclosure of sup ||D^{k} f|| (scaled) / grid max of the Frobenius norm = {enc / grid_max:.3f}")
    res["CES_enclosure_tightness"] = tight
    res["meta"]["cpu_seconds"] = time.process_time() - c0
    res["meta"]["wall_seconds"] = time.time() - t0
    say("=" * 100)
    say(f"CPU time {res['meta']['cpu_seconds']:.1f} s, wall {res['meta']['wall_seconds']:.1f} s (interpreter start-up excluded).")
    # compact JSON for the integrator (macros): drop per-cell detail except sigma and certified shares
    slim = {"meta": res["meta"], "derivative_checks": res["derivative_checks"], "prediction_LN_scaled": res["prediction_LN_scaled"],
            "CES_enclosure_tightness": res["CES_enclosure_tightness"],
            "E4_no_capacity": res["E4"], "E1": {}}
    for key, v in res["E1"].items():
        slim["E1"][key] = {"summary": v["summary"],
                           "cells": [{kk: vv for kk, vv in c.items() if kk in ("sigma", "r21_min", "ratio_C3_over_Q2_med",
                                     "ratio_B3s_over_Q2_med", "ratio_B2s_over_Q2_med", "M3box_s_med", "M4box_s_med",
                                     "identity_E2_eq_C3_plus_E3") or kk.startswith("certfrac")} for c in v["cells"]]}
    with open(OUT_JSON, "w") as fh:
        json.dump(slim, fh, indent=1, default=float)
    with open(OUT_TXT, "w") as fh:
        fh.write("\n".join(LINES) + "\n")


if __name__ == "__main__":
    main()
