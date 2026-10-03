#!/usr/bin/env python3
"""Margins of Conjecture conj on SMOOTH curves (review round 4, M2): how biased are the polygonal vertex-pair margins?

Adapted from the independent smooth construction written for the round-4 internal review (referee4_RTK001/smooth.py
and margin_smooth.py; no code of recursive_knots.py).  K_0 is sampled exactly (M_0 = 1024 points); at each depth the
closed Bishop frame is obtained by spectral integration of the connection 1-form in a periodic normal frame,
normalised as in Definition def:family (N(0) = unit projection of e_z), and K_d is built by eq:Kd at the samples (the
curves are trigonometric polynomials up to the spectral tail, reported).  Doubly critical pairs: all local minima of
h_1^2 + h_2^2 (h_i = (X_1 - X_2).T_i) on the sample grid with distance < 1.15 * 2 r_d, refined by Newton's method on
the Fourier interpolant (step < 1e-13), antipodal pairs of one normal disc excluded; margin = min distance/(2 r_d) - 1.
Exclusion window (documented in v0.6, review round 5, m6): the grid stage discards pairs with |ds - pi| <= 0.05 in the
normalised parameter of K_d (and pairs closer than r_d/2).  ds = pi is the antipodal pair of one normal disc; at d = 3 the
window also discards pairs on opposite strands whose base points are < 0.1 apart in the parameter of K_2 (base arc of
about 0.5, i.e. about 2.5 tau_2).  The round-5 referee re-ran this script with a window of 0.004 and obtained the same
five margins to the printed digits, so the window does not affect the reported values.
r_d as in the polygonal chain: r_1 = 1/2, r_2 = f tau(K_1) with the N_0 = 512 polygonal tau (results/results.json),
r_3 = r_2/2.  Phases: (beta_2, beta_3) = rotation of the initial normal of the frames of K_1 and K_2 (= phi_2, phi_3).
This is a smooth evaluation (spectral accuracy), not a certified bound.  Output: results/smooth_margin.json.
"""
import json
import os
import time

import numpy as np

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


def D(f, k=1):
    M = f.shape[0]
    F = np.fft.fft(f, axis=0)
    kk = np.fft.fftfreq(M, 1.0 / M)
    amp = np.abs(F)
    F = np.where(amp > 1e-15 * amp.max(), F, 0)
    if M % 2 == 0:
        F[M // 2] = 0
    mult = (1j * kk) ** k
    return np.real(np.fft.ifft(F * (mult[:, None] if f.ndim == 2 else mult), axis=0))


def antider0(c):
    M = len(c)
    F = np.fft.fft(c)
    kk = np.fft.fftfreq(M, 1.0 / M)
    mean = F[0].real / M
    G = np.zeros_like(F)
    nz = kk != 0
    G[nz] = F[nz] / (1j * kk[nz])
    I = np.real(np.fft.ifft(G))
    s = 2 * np.pi * np.arange(M) / M
    return mean * s + I - I[0], mean


def tail(f):
    F = np.abs(np.fft.fft(f, axis=0)).sum(axis=1)
    kk = np.abs(np.fft.fftfreq(len(F), 1.0 / len(F)))
    return float(F[kk > 0.4 * len(F)].max() / F.max())


nrm = lambda a: np.linalg.norm(a, axis=1)            # noqa: E731
dot = lambda a, b: np.einsum("ij,ij->i", a, b)       # noqa: E731


def frame(X, e1):
    X1 = D(X, 1)
    T = X1 / nrm(X1)[:, None]
    e1 = e1 - dot(e1, T)[:, None] * T
    e1 /= nrm(e1)[:, None]
    e2 = np.cross(T, e1)
    I, mean = antider0(dot(D(e1, 1), e2))
    alpha = (-2 * np.pi * mean + np.pi) % (2 * np.pi) - np.pi
    if alpha <= -np.pi:
        alpha += 2 * np.pi
    ez = np.array([0, 0, 1.0])
    a = ez if abs(T[0] @ ez) <= 0.9 else np.array([1.0, 0, 0])
    n0 = a - (a @ T[0]) * T[0]
    n0 /= np.linalg.norm(n0)
    th0 = np.arctan2(n0 @ e2[0], n0 @ e1[0])
    s = 2 * np.pi * np.arange(len(X)) / len(X)
    ph = th0 - I - alpha * s / (2 * np.pi)
    N = np.cos(ph)[:, None] * e1 + np.sin(ph)[:, None] * e2
    return N, np.cross(T, N), alpha


def build(X, N, B, r, phi=0.0, p=2, q=3):
    M = len(X)
    J = np.arange(p * M)
    jb = J % M
    th = q / p * 2 * np.pi * J / M + phi
    U = np.cos(th)[:, None] * N[jb] + np.sin(th)[:, None] * B[jb]
    return X[jb] + r * U, U


def chain(betas, RS, M0=1024):
    s = 2 * np.pi * np.arange(M0) / M0
    X = np.stack([np.cos(s), np.sin(s), 0 * s], 1)
    e1 = np.tile([0, 0, 1.0], (M0, 1))
    for d, b in enumerate(betas):
        N, B, _ = frame(X, e1)
        X, e1 = build(X, N, B, RS[d], phi=b)
    return X


class Interp:
    def __init__(self, X):
        self.M = len(X)
        self.C = np.fft.fft(X, axis=0) / self.M
        self.k = np.fft.fftfreq(self.M, 1.0 / self.M)
        self.C[self.M // 2] = 0

    def ev(self, t, der=0):
        return np.real((np.exp(1j * self.k * t) * (1j * self.k) ** der) @ self.C)


def margin(X, r, sub=4, cap=1.15):
    I = Interp(X)
    Y = X[::sub]
    n = len(Y)
    T = D(X, 1)[::sub]
    T /= nrm(T)[:, None]
    Dm = np.sqrt(((Y[:, None, :] - Y[None, :, :]) ** 2).sum(-1))
    XT = (Y * T).sum(1)
    G = (XT[:, None] - T @ Y.T) ** 2 + ((Y @ T.T) - XT[None, :]) ** 2
    idx = np.arange(n)
    ds = np.abs(idx[:, None] - idx[None, :])
    ds = np.minimum(ds, n - ds) * 2 * np.pi / n
    mask = (Dm < cap * 2 * r) & (Dm > 0.5 * r) & (np.abs(ds - np.pi) > 0.05) & (idx[:, None] < idx[None, :])
    Gp = np.pad(G, 1, mode="wrap")
    loc = np.ones_like(G, bool)
    for a in (-1, 0, 1):
        for b in (-1, 0, 1):
            if a or b:
                loc &= G <= Gp[1 + a:n + 1 + a, 1 + b:n + 1 + b]
    found = []
    for i, j in np.argwhere(mask & loc):
        t1, t2 = 2 * np.pi * i / n, 2 * np.pi * j / n
        ok = False
        for _ in range(30):
            P1, P2, d1, d2 = I.ev(t1), I.ev(t2), I.ev(t1, 1), I.ev(t2, 1)
            dd1, dd2 = I.ev(t1, 2), I.ev(t2, 2)
            dv = P1 - P2
            H = np.array([[d1 @ d1 + dv @ dd1, -d1 @ d2], [-d1 @ d2, d2 @ d2 - dv @ dd2]])
            try:
                st = np.clip(np.linalg.solve(H, -np.array([dv @ d1, -dv @ d2])), -0.02, 0.02)
            except np.linalg.LinAlgError:
                break
            t1 += st[0]
            t2 += st[1]
            if np.abs(st).max() < 1e-13:
                ok = True
                break
        if not ok:
            continue
        dv = I.ev(t1) - I.ev(t2)
        dt = (t2 - t1) % (2 * np.pi)
        if abs(dt - np.pi) < 1e-6 or min(dt, 2 * np.pi - dt) < 0.01:
            continue
        d1, d2, dd1, dd2 = I.ev(t1, 1), I.ev(t2, 1), I.ev(t1, 2), I.ev(t2, 2)
        H11, H22 = d1 @ d1 + dv @ dd1, d2 @ d2 - dv @ dd2
        found.append((float(np.linalg.norm(dv)), "min-min" if (H11 > 0 and H22 > 0) else "other"))
    found.sort()
    best = found[0] if found else (np.inf, "none")
    return dict(margin_pct=100 * (best[0] / (2 * r) - 1), pair_type=best[1], n_candidates=len(found))


def main():
    t0 = time.process_time()
    res = json.load(open(os.path.join(ROOT, "results", "results.json")))
    ch = [c for c in res["chains"] if c["pattern"] == "(2,3)" and c["f"] == 0.5 and c["N0"] == 512][0]
    tau1 = [lv for lv in ch["levels"] if lv["d"] == 1][0]["tau"]
    RS = [0.5, 0.5 * tau1, 0.25 * tau1]
    joint = json.load(open(os.path.join(ROOT, "results", "joint_phase_sweep.json")))["summary"]["argmin_256"]
    configs = [("d2_default", [0, 0]), ("d3_default", [0, 0, 0]), ("d3_1d_min", [0, 0, 0.4654211338651545]),
               ("d3_0_049", [0, 0, 0.49]), ("d3_joint_min", [0, joint["beta1"], joint["beta2"]])]
    out = dict(r=RS, tau1_poly_512=tau1, rows=[])
    for lab, betas in configs:
        X = chain(betas, RS)
        m = margin(X, RS[len(betas) - 1], sub=4 if len(betas) == 3 else 2)
        m.update(label=lab, betas=[float(b) for b in betas], spectral_tail=tail(X))
        out["rows"].append(m)
        print(m, flush=True)
    out["seconds_cpu"] = time.process_time() - t0
    with open(os.path.join(ROOT, "results", "smooth_margin.json"), "w") as fh:
        json.dump(out, fh, indent=1)
    print(f"CPU {out['seconds_cpu']:.1f} s")


if __name__ == "__main__":
    main()
