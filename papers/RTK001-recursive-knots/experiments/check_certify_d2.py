#!/usr/bin/env python3
"""Author's independent check (review round 4) of the computer-assisted proof of the case d = 2 (certify_d2.py).

Not part of the proof; it tests the proof's implementation against independent formulas and plain floating point.
  1. Independent formulas: K_1(s; r) in real coordinates, derivatives by sympy; nu = |dv/ds|/v^2 and
     mu = |Pi_perp d(kappa-vector)/ds|/v obtained by differentiating v and the curvature vector symbolically
     (the proof uses closed forms in D_1, D_2, D_3 instead).
  2. Containment, per r_1-box: plain float values on a dense grid of the FULL period s in [0, 2pi) (so the 3-fold
     symmetry used in the proof is tested too), at r_1 = lo, mid, hi of each of the 512 boxes, must satisfy
     v >= v_min_lo, kappa <= kappa_max_hi, nu <= nu_hi, mu <= mu_hi of that box.
  3. Containment, per (r_1, s)-box: for 5 r_1-boxes and all 2048 s-boxes, float values at 9 points of each box must
     lie in the pointwise interval enclosures of certify_d2.base_quantities.
  4. The final inequality recomputed in mpmath (50 digits) from the box data, with an independent implementation of
     r_2 * RHS(eq:kaprec); and a sampled monotonicity test of that expression in its six inputs.
  5. Unit test of the interval class Iv against exact rational arithmetic (fractions) on random intervals.
Output: results/check_certify_d2.json (+ stdout in results/check_certify_d2_output.txt).  Deterministic (seed 0).
"""
import json
import os
import time
from fractions import Fraction

import mpmath as mp
import numpy as np
import sympy as sp

import certify_d2 as C

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(os.path.dirname(HERE), "results")
t0, c0 = time.time(), time.process_time()
res = {}

# ---------------------------------------------------------------- 1. independent formulas
s, r = sp.symbols("s r", real=True)
K = sp.Matrix([sp.cos(2 * s) * (1 + r * sp.sin(3 * s)), sp.sin(2 * s) * (1 + r * sp.sin(3 * s)), r * sp.cos(3 * s)])
D1, D2, D3 = K.diff(s), K.diff(s, 2), K.diff(s, 3)
f_D1, f_D2, f_D3 = (sp.lambdify((s, r), list(X), "numpy") for X in (D1, D2, D3))


def quantities(S, R):
    d1 = np.stack(np.broadcast_arrays(*f_D1(S, R)), -1)
    d2 = np.stack(np.broadcast_arrays(*f_D2(S, R)), -1)
    d3 = np.stack(np.broadcast_arrays(*f_D3(S, R)), -1)
    v = np.linalg.norm(d1, axis=-1)
    T = d1 / v[..., None]
    dv = np.einsum("...i,...i->...", T, d2)                       # dv/ds
    kv = (d2 - dv[..., None] * T) / v[..., None] ** 2              # curvature vector
    # d(kv)/ds by the quotient rule, with dT/ds = (d2 - dv T)/v and d^2v/ds^2 = (d1.d3 + |d2|^2 - dv^2)/v
    dT = (d2 - dv[..., None] * T) / v[..., None]
    ddv = (np.einsum("...i,...i->...", d1, d3) + np.einsum("...i,...i->...", d2, d2) - dv ** 2) / v
    num = d2 - dv[..., None] * T
    dnum = d3 - ddv[..., None] * T - dv[..., None] * dT
    dk = dnum / v[..., None] ** 2 - 2 * num * (dv / v ** 3)[..., None]
    Pdk = dk - np.einsum("...i,...i->...", dk, T)[..., None] * T
    return dict(v=v, kap=np.linalg.norm(kv, axis=-1), nu=np.abs(dv) / v ** 2, mu=np.linalg.norm(Pdk, axis=-1) / v)


# ---------------------------------------------------------------- 2. per r_1-box containment (full period)
E_B = C.trig_boxes(2048, Fraction(1, 3))
worst, rows = C.certify_continuum(E_B, 2048, 512)
Sg = np.linspace(0, 2 * np.pi, 6000, endpoint=False)
slack = dict(v=np.inf, kap=np.inf, nu=np.inf, mu=np.inf)
viol = 0
for rw in rows:
    a, b = rw["r1_lo"], rw["r1_hi"]
    for rr in (a, 0.5 * (a + b), b):
        Q = quantities(Sg, rr)
        sv = Q["v"].min() - rw["v_min_lo"]
        sk = rw["kappa_max_hi"] - Q["kap"].max()
        sn = rw["nu_hi"] - Q["nu"].max()
        sm = rw["mu_hi"] - Q["mu"].max()
        viol += int(min(sv, sk, sn, sm) < 0)
        for key, val in (("v", sv), ("kap", sk), ("nu", sn), ("mu", sm)):
            slack[key] = min(slack[key], float(val))
res["per_r_box"] = dict(n_boxes=len(rows), s_points_full_period=len(Sg), violations=viol, min_slack=slack)
print(f"2. per r_1-box containment, {len(rows)} boxes x 3 r_1 values x {len(Sg)} s on [0,2pi): violations {viol}; "
      f"min slack {slack}")
# symmetry: suprema over [0,2pi) vs [0,2pi/3) at r_1 = 1/2
Qf = quantities(Sg, 0.5)
Qt = quantities(np.linspace(0, 2 * np.pi / 3, 2000, endpoint=False), 0.5)
sym = {k: float(abs((Qf[k].min() if k == "v" else Qf[k].max()) - (Qt[k].min() if k == "v" else Qt[k].max())))
       for k in ("v", "kap", "nu", "mu")}
res["symmetry_sup_difference_r05"] = sym
res["float_values_r05"] = {k: float(Qf[k].min() if k == "v" else Qf[k].max()) for k in ("v", "kap", "nu", "mu")}
print("   symmetry: |sup over [0,2pi) - sup over [0,2pi/3)| at r_1 = 1/2:", sym)

# ---------------------------------------------------------------- 3. per (r_1, s)-box containment
cont_viol, n_pts = 0, 0
smin = np.inf
sb = np.array([[2 * np.pi / 3 * j / 2048, 2 * np.pi / 3 * (j + 1) / 2048] for j in range(2048)])
for i in (0, 127, 255, 383, 511):
    a, b = 0.5 * i / 512, 0.5 * (i + 1) / 512
    Q = C.base_quantities(C.k1_derivs(E_B, C.Iv(np.array([[a]]), np.array([[b]])), 3))
    for fs in (0.0, 0.5, 1.0):
        for fr in (0.0, 0.5, 1.0):
            S = sb[:, 0] + fs * (sb[:, 1] - sb[:, 0])
            R = a + fr * (b - a)
            P = quantities(S, R)
            for key, sign in (("v", 1), ("kap", 1), ("mu", 1)):
                lo, hi = Q[key].lo.ravel(), Q[key].hi.ravel()
                d = np.minimum(P[key] - lo, hi - P[key])
                smin = min(smin, float(d.min()))
                cont_viol += int((d < 0).sum())
            lo, hi = Q["nu"].lo.ravel(), Q["nu"].hi.ravel()           # signed v'/v^2 in the proof, |.| here
            d = np.minimum(P["nu"] - np.minimum(np.abs(lo), np.where(lo * hi <= 0, 0, np.abs(hi))), np.maximum(np.abs(lo), np.abs(hi)) - P["nu"])
            smin = min(smin, float(d.min()))
            cont_viol += int((d < 0).sum())
            n_pts += 4 * len(S)
res["per_box_containment"] = dict(points_times_quantities=n_pts, violations=cont_viol, min_slack=smin)
print(f"3. per (r_1, s)-box containment: {n_pts} point-quantity tests, violations {cont_viol}, min slack {smin:.3e}")

# ---------------------------------------------------------------- 4. final inequality in mpmath, and monotonicity
mp.mp.dps = 50


def phi_mp(Kx, V, Nu, Mu, r2, m):
    Kx, V, Nu, Mu, r2, m = (mp.mpf(x) for x in (Kx, V, Nu, Mu, r2, m))
    eps = r2 * Kx
    lam = r2 * m / V
    z = V * (1 - eps) / (r2 * m)
    g = lambda x: x * (x ** 2 + 2) / (x ** 2 + 1) ** mp.mpf(1.5)   # noqa: E731
    G = g(mp.sqrt(2)) if z <= mp.sqrt(2) else g(z)
    return r2 * Kx * G / (1 - eps) + 1 / (1 + z ** 2) + r2 * lam * (Nu * (1 + eps) + r2 * Mu) / (1 - eps) ** 3, z


phis = [phi_mp(rw["kappa_max_hi"], rw["v_min_lo"], rw["nu_hi"], rw["mu_hi"], rw["r1_hi"] / 2, 2) for rw in rows]
pmax = max(p for p, _ in phis)
zmin = min(z for _, z in phis)
res["phi_mpmath"] = dict(max=float(pmax), max_certify=float(worst["total"]), zeta_min=float(zmin),
                         agree=bool(pmax <= worst["total"] and worst["total"] - pmax < 1e-9))
print(f"4. max_box Phi in mpmath = {float(pmax):.12f}; certify_d2 (outward rounded) = {worst['total']:.12f}; "
      f"min zeta' = {float(zmin):.3f} (> sqrt 2: G = g(zeta'))")
rng = np.random.default_rng(0)
bad, ntest = 0, 0
for _ in range(4000):
    x = [rng.uniform(0.5, 3), rng.uniform(0.5, 3), rng.uniform(0, 2), rng.uniform(0, 8), rng.uniform(0.01, 0.3), rng.uniform(1, 2)]
    if x[4] * x[0] >= 0.9:
        continue
    base = float(phi_mp(*x)[0])
    for k, sgn in ((0, 1), (1, -1), (2, 1), (3, 1), (4, 1), (5, 1)):
        y = list(x)
        y[k] *= 1 + 1e-3
        if y[4] * y[0] >= 0.9:
            continue
        ntest += 1
        bad += int(sgn * (float(phi_mp(*y)[0]) - base) < -1e-30)
res["monotonicity"] = dict(tests=ntest, violations=bad,
                           directions="non-decreasing in kappa_max, nu, mu, r_2, m; non-increasing in v_min")
print(f"   monotonicity of Phi: {ntest} finite-difference tests, violations {bad}")

# ---------------------------------------------------------------- 5. unit test of Iv against exact rationals
bad_iv, nt = 0, 0
for _ in range(3000):
    a = np.sort(rng.normal(size=2) * 10 ** rng.uniform(-3, 3))
    b = np.sort(rng.normal(size=2) * 10 ** rng.uniform(-3, 3))
    A, B = C.Iv(a[0], a[1]), C.Iv(b[0], b[1])
    Fa = [Fraction(float(x)) for x in a]
    Fb = [Fraction(float(x)) for x in b]
    ex = dict(add=[x + y for x in Fa for y in Fb], sub=[x - y for x in Fa for y in Fb], mul=[x * y for x in Fa for y in Fb])
    got = dict(add=A + B, sub=A - B, mul=A * B)
    if b[0] > 0 or b[1] < 0:
        ex["div"] = [x / y for x in Fa for y in Fb]
        got["div"] = A / B
    ex["sq"] = [x * x for x in Fa] + ([Fraction(0)] if a[0] <= 0 <= a[1] else [])
    got["sq"] = A.sq()
    for k in ex:
        nt += 1
        lo, hi = Fraction(float(got[k].lo)), Fraction(float(got[k].hi))
        bad_iv += int(not (lo <= min(ex[k]) and max(ex[k]) <= hi))
    if a[0] > 0:                                      # sqrt: check lo^2 <= a_lo and hi^2 >= a_hi exactly
        S_ = C.Iv(a[0], a[1]).sqrt()
        nt += 1
        bad_iv += int(not (Fraction(float(S_.lo)) ** 2 <= Fa[0] and Fraction(float(S_.hi)) ** 2 >= Fa[1]))
res["iv_unit_test"] = dict(tests=nt, violations=bad_iv)
print(f"5. Iv unit test against exact rationals: {nt} tests, violations {bad_iv}")
# mpmath.iv: an s-box containing an extremum of cos(3s)
e = C.iv.cos(3 * C.iv.mpf([1.0, 1.1]))                 # 3s in [3, 3.3] contains pi
res["mpmath_iv_extremum"] = dict(lower=float(e.a), contains_minus_one=bool(e.a <= -1))
print(f"   mpmath.iv cos(3[1, 1.1]) lower end {float(e.a)} (must be <= -1)")

res["meta"] = dict(seconds_wall=time.time() - t0, seconds_cpu=time.process_time() - c0, numpy=np.__version__,
                   sympy=sp.__version__, mpmath=mp.__version__)
with open(os.path.join(OUT, "check_certify_d2.json"), "w") as fh:
    json.dump(res, fh, indent=1)
print(f"wall {res['meta']['seconds_wall']:.1f} s, CPU {res['meta']['seconds_cpu']:.1f} s")
