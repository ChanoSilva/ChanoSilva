#!/usr/bin/env python3
"""Independent verification (author, round 3) of theory/H3_uniform_lemma.tex.  Uses no code of the author's scripts.

(a) sympy frame calculus in the moving frame (T, U, W):  K_d' , w' identity (eq:wprime), cross-product identity,
    and the coefficients of the fourth-order term kappa_perp'' and of v'' in the normal part of K_d'''.
(b) mpmath constants of cor:tolerance and of the d = 2 analogue.
(c) smooth check K_1 -> K_2: K_1 is a trigonometric polynomial (exact derivatives), its Bishop frame is integrated with
    DOP853 (rtol 1e-12), K_2 is differentiated spectrally; Lemma lem:speedrec and Prop. prop:curvrec are compared with
    the measured nu(K_2), kappa_max(K_2).
Archived in experiments/ in round 4 (review m4): identical to the round-3 scratch script except for the JSON summary
written at the end (results/verify_H3.json); stdout is saved as results/verify_H3_output.txt.
"""
import json
import os
import numpy as np
import sympy as sp
import mpmath as mp
from scipy.integrate import solve_ivp

print("=== (a) frame calculus ===")
t = sp.symbols("t", real=True)
r, m = sp.symbols("r m", positive=True)
v = sp.Function("v")(t)
kp = sp.Function("kp")(t)   # kappa_perp = k.U
kw = sp.Function("kw")(t)   # kappa_W   = k.W


def D(X):
    a, b, c = X
    # T' = v(kp U + kw W), U' = m W - v kp T, W' = -m U - v kw T
    return (sp.diff(a, t) - b * v * kp - c * v * kw,
            sp.diff(b, t) + a * v * kp - c * m,
            sp.diff(c, t) + a * v * kw + b * m)


def cross(X, Y):  # basis (T, U, W) right-handed: T x U = W, U x W = T, W x T = U
    return (X[1] * Y[2] - X[2] * Y[1], X[2] * Y[0] - X[0] * Y[2], X[0] * Y[1] - X[1] * Y[0])


def dot(X, Y):
    return sum(x * y for x, y in zip(X, Y))


Kd1 = (v, 0, 0)
Kd1 = tuple(sp.expand(a + r * b) for a, b in zip(Kd1, (-v * kp, 0, m)))     # K' + r U'
print("K_d' =", Kd1)
Kd2 = tuple(sp.expand(e) for e in D(Kd1))
Kd3 = tuple(sp.expand(e) for e in D(Kd2))
x = r * kp
cT, cW = v * (1 - x), r * m
kdot_perp = sp.diff(kp, t) - m * kw          # kappa_par'.U
a0 = sp.diff(v, t) * (1 - x) - r * v * kdot_perp
w = sp.sqrt(cT ** 2 + cW ** 2)
wp = sp.diff(w, t)
print("w' identity residual:", sp.simplify(wp - cT * (a0 - r * v * m * kw) / w))
A, B = cT ** 2, cW ** 2
a_, bU, bW = Kd2
print("a = a0 - 2 r v m kw residual:", sp.simplify(a_ - (a0 - 2 * r * v * m * kw)))
print("b_U residual:", sp.simplify(bU - (v ** 2 * (1 - x) * kp - r * m ** 2)), " b_W residual:", sp.simplify(bW - v ** 2 * (1 - x) * kw))
C = cross(Kd1, Kd2)
print("cross identity residual:", sp.simplify(dot(C, C) - (bU ** 2 * (A + B) + (cW * a_ - cT * bW) ** 2)))
print("c_W a - c_T b_W residual:", sp.simplify(cW * a_ - cT * bW - (r * m * a0 - kw * v * (A + 2 * B))))
# normal part of K_d''' along n_chi = (sin chi, 0, -cos chi) = (cW, 0, -cT)/w ; along U the normal direction is U itself
n3 = sp.expand(Kd3[0] * cW - Kd3[2] * cT)       # = w * (K_d'''. n_chi)
kpp, vpp = sp.diff(kp, t, 2), sp.diff(v, t, 2)
print("coefficient of kp'' in w*(K_d'''.n_chi):", sp.factor(sp.expand(n3).coeff(kpp)), "  [-> -r v sin(chi) after /w]")
print("coefficient of v''  in w*(K_d'''.n_chi):", sp.factor(sp.expand(n3).coeff(vpp)), "  [-> (1-x) sin(chi) after /w]")
print("kp'' or v'' in K_d'''.U ?", sp.expand(Kd3[1]).has(kpp), sp.expand(Kd3[1]).has(vpp))
print("highest derivative of kp, kw in K_d''':", [max(sp.ode_order(e, f) for f in (kp, kw)) for e in Kd3])

print("\n=== (b) constants ===")
mp.mp.dps = 30
g = lambda z: z * (z ** 2 + 2) / (z ** 2 + 1) ** mp.mpf(1.5)
s13 = mp.sqrt(13)
R3 = 2 - g(s13) - mp.mpf(1) / 14
print("g(sqrt13) =", g(s13), " 2-g(sqrt13)-1/14 =", R3)
print("coef nu: 96/sqrt13 =", 96 / s13, "  coef mu: 64/sqrt13 =", 64 / s13)
print("nu threshold (alone): ", R3 * s13 / 96, "* 4^d ;  mu threshold (alone):", R3 * s13 / 64, "* 8^d")
print("half each:", R3 * s13 / 192, "* 4^d ;", R3 * s13 / 128, "* 8^d")
# d = 2 analogue: zeta' >= sqrt13/2, r_2 <= 1/4, lam <= 2/sqrt13
z2 = s13 / 2
print("d=2: coef nu 12*(1/4)*(2/sqrt13) =", 12 * mp.mpf(1) / 4 * 2 / s13, " coef mu 8*(1/16)*(2/sqrt13) =", 8 * mp.mpf(1) / 16 * 2 / s13,
      " rhs 2-g(sqrt13/2)-4/17 =", 2 - g(z2) - mp.mpf(4) / 17)
print("g decreasing on [sqrt2, inf): g'(z) sign at 1.5, 3.6, 10:", [mp.diff(g, z) < 0 for z in (1.5, 3.6, 10)])
print("(1+e)/(1-e)^3 at e=1/2:", mp.mpf(1.5) / mp.mpf(0.5) ** 3, " (1-e)^-3:", 1 / mp.mpf(0.5) ** 3)
print("a priori r_d sin(chi_d) <= 2^-d * 2 lam <= 2^-d * 2^(4-d)/sqrt13 = (16/sqrt13) 4^-d; 16/sqrt13 =", 16 / s13)

print("\n=== (c) smooth K_1 -> K_2 ===")


def _fix(s, r1, j):
    s = np.asarray(s, dtype=float)
    xy = ((2j) ** j) * np.exp(2j * s) + (r1 / 2j) * (((5j) ** j) * np.exp(5j * s) - ((-1j) ** j) * np.exp(-1j * s))
    z = r1 * np.real(((3j) ** j) * np.exp(3j * s))
    return np.stack([xy.real, xy.imag, z], axis=-1)
K1d = _fix


def curve_data(D1, D2, D3):
    vv = np.linalg.norm(D1, axis=-1)
    T = D1 / vv[:, None]
    vp = np.einsum("ij,ij->i", T, D2)
    k = (D2 - vp[:, None] * T) / vv[:, None] ** 2
    kap = np.linalg.norm(k, axis=-1)
    out = dict(v=vv, T=T, vp=vp, k=k, kap=kap, nu=float(np.max(np.abs(vp) / vv ** 2)))
    if D3 is not None:
        P3 = D3 - np.einsum("ij,ij->i", D3, T)[:, None] * T
        dk = (P3 - 3 * (vv * vp)[:, None] * k) / vv[:, None] ** 2      # Pi_perp dk/dt
        out["mu"] = float(np.max(np.linalg.norm(dk, axis=-1) / vv))
    return out


def spectral_derivs(P, period, nder):
    M = len(P)
    kk = np.fft.fftfreq(M, d=period / M) * 2 * np.pi
    F = np.fft.fft(P, axis=0)
    return [np.real(np.fft.ifft(((1j * kk) ** j)[:, None] * F, axis=0)) for j in range(1, nder + 1)]


SMOOTH = []
for (f1, r2) in [(0.5, 0.5 * 0.41582), (0.5, 0.25), (0.35, 0.35 * 0.35), (0.25, 0.25 * 0.25)]:
    r1 = f1
    sg = np.linspace(0, 2 * np.pi, 40001)[:-1]
    B1 = curve_data(K1d(sg, r1, 1), K1d(sg, r1, 2), K1d(sg, r1, 3))
    vmin, kmax, nu1, mu1 = B1["v"].min(), B1["kap"].max(), B1["nu"], B1["mu"]

    def rhs(s, y):
        D1, D2 = K1d(s, r1, 1), K1d(s, r1, 2)
        vv = np.linalg.norm(D1)
        T = D1 / vv
        Tp = (D2 - np.dot(T, D2) * T) / vv
        return -np.dot(y, Tp) * T

    T0 = K1d(0.0, r1, 1); T0 = T0 / np.linalg.norm(T0)
    ez = np.array([0.0, 0.0, 1.0])
    assert abs(T0 @ ez) <= 0.9
    N0 = ez - (ez @ T0) * T0; N0 /= np.linalg.norm(N0)
    M2 = 8192                                 # samples of K_2 on [0, 4 pi)
    tt = 4 * np.pi * np.arange(M2) / M2
    sp_ = tt[: M2 // 2]                       # one period of the base
    sol = solve_ivp(rhs, (0, 2 * np.pi), N0, method="DOP853", rtol=1e-12, atol=1e-13, t_eval=np.append(sp_, 2 * np.pi))
    Nn = sol.y.T
    Nend = Nn[-1]; Nn = Nn[:-1]
    Tb = K1d(sp_, r1, 1); Tb /= np.linalg.norm(Tb, axis=1)[:, None]
    B0 = np.cross(T0, N0)
    alpha = np.arctan2(Nend @ B0, Nend @ N0)
    om = -alpha * sp_ / (2 * np.pi)
    Bn = np.cross(Tb, Nn)
    Nc = np.cos(om)[:, None] * Nn + np.sin(om)[:, None] * Bn
    Bc = np.cross(Tb, Nc)
    Nc2, Bc2, P1 = np.vstack([Nc, Nc]), np.vstack([Bc, Bc]), np.vstack([K1d(sp_, r1, 0)] * 2)
    th = 1.5 * tt
    K2 = P1 + r2 * (np.cos(th)[:, None] * Nc2 + np.sin(th)[:, None] * Bc2)
    D1, D2, D3 = spectral_derivs(K2, 4 * np.pi, 3)
    C2 = curve_data(D1, D2, None)
    kap2 = np.linalg.norm(np.cross(D1, D2), axis=1) / np.linalg.norm(D1, axis=1) ** 3
    m2 = 1.5 - alpha / (2 * np.pi)
    eps = r2 * kmax; lam = r2 * m2 / vmin; zp = vmin * (1 - eps) / (r2 * m2)
    gg = lambda z: z * (z ** 2 + 2) / (z ** 2 + 1) ** 1.5
    G = gg(np.sqrt(2)) if zp <= np.sqrt(2) else gg(zp)
    nu_b = nu1 / (1 - eps) + (r2 * mu1 + lam * kmax) / (1 - eps) ** 2
    ka_b = kmax * G / (1 - eps) + 1 / (r2 * (1 + zp ** 2)) + lam * (nu1 * (1 + eps) + r2 * mu1) / (1 - eps) ** 3
    tail = np.abs(np.fft.fft(K2, axis=0))[M2 // 2 - 50: M2 // 2 + 50].max() / np.abs(np.fft.fft(K2, axis=0)).max()
    print(f"f1={f1} r2={r2:.4f}: K_1 v_min={vmin:.5f} kappa_max={kmax:.5f} nu={nu1:.4f} mu={mu1:.4f}; alpha_2={alpha:.4f} m_2={m2:.4f}; "
          f"spectral tail {tail:.1e}")
    print(f"   nu(K_2) = {C2['nu']:.4f} <= bound {nu_b:.4f} ? {C2['nu'] <= nu_b} (ratio {C2['nu']/nu_b:.3f});  "
          f"kappa_max(K_2) = {kap2.max():.4f} <= bound {ka_b:.4f} ? {kap2.max() <= ka_b} (ratio {kap2.max()/ka_b:.3f}); r2*bound = {r2*ka_b:.4f}")
    SMOOTH.append(dict(f1=f1, r2=r2, v_min1=float(vmin), kappa_max1=float(kmax), nu1=float(nu1), mu1=float(mu1),
                       alpha2=float(alpha), m2=float(m2), nu2=float(C2["nu"]), kappa_max2=float(kap2.max()),
                       nu2_bound=float(nu_b), kappa2_bound=float(ka_b), r2_kappa_max2=float(r2 * kap2.max()),
                       r2_kappa2_bound=float(r2 * ka_b), spectral_tail=float(tail)))

with open(os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "results", "verify_H3.json"), "w") as fh:
    json.dump(dict(smooth=SMOOTH), fh, indent=1)
