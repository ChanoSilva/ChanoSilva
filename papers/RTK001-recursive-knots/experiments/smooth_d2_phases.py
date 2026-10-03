#!/usr/bin/env python3
"""Smooth (NOT certified) values of r_2 kappa_max(K_2) over the phases and over r_1, r_2 = r_1/2 (v0.6, review round 5, m3).

Purpose: the sharpness sentence of Remark rem:d2method.  The certified bound of Prop. prop:d2cert is
r_2 kappa_max(K_2) <= 1.187 for all r_1 <= 1/2, r_2 <= r_1/2 and all phases; this script measures the actual smooth value
on a grid of (r_1, phi_2) with r_2 = r_1/2 (the largest admissible r_2), to show how far from sharp the bound is.

Construction (same as experiments/verify_H3.py, part (c), with a phase): K_1 is the explicit trigonometric polynomial
(x + iy = e^{2is} + (r_1/2i)(e^{5is} - e^{-is}), z = r_1 cos 3s), its Bishop frame is integrated with DOP853
(rtol 1e-12) from N_0(0) = unit projection of e_z (Definition def:family), closed by the linear twist with
alpha_2 in (-pi, pi], and K_2(t) = K_1(t mod 2pi) + r_2 [cos(1.5 t + phi_2) N + sin(1.5 t + phi_2) B], t in [0, 4pi),
sampled at 8192 points and differentiated spectrally.  A change of phi_1 (or of N_0(0)) only moves the base point and
rotates the initial normal, i.e. it is a change of phi_2 (Definition def:family; Prop. prop:d2cert, proof), and
phi_2 + pi gives the same curve, so phi_2 in [0, pi) with phi_1 = 0 covers every choice of phases.

Grid: r_1 in {0.05, 0.10, ..., 0.45} (24 phases) and r_1 in [0.45, 0.5] with step 0.0025 plus 0.4900-0.4910 around
r_* ~ 0.4904, where alpha_2 crosses pi and m_2 jumps from ~1 to ~2 (48 phases); then a local refinement of
(r_1, phi_2) around the maximum.  A grid evaluation: the true maximum over the phases can be slightly larger.

Also records (review round 5, m1) kappa_min(K_1) at r_1 = 0.25, 0.35, 4/13, 0.5: kappa(K_1) vanishes at r_1 = 4/13,
s = pi/2 (kappa(K_1)(pi/2) = |4 - 13 r_1| / (4(1 - r_1)^2 + 9 r_1^2)).

Output: results/smooth_d2_phases.json; stdout saved as results/smooth_d2_phases_output.txt.  Deterministic.  ~1 min CPU.
"""
import json
import os
import time

import numpy as np
from scipy.integrate import solve_ivp

HERE = os.path.dirname(os.path.abspath(__file__))
M2 = 8192


def K1d(s, r1, j):
    s = np.asarray(s, dtype=float)
    xy = ((2j) ** j) * np.exp(2j * s) + (r1 / 2j) * (((5j) ** j) * np.exp(5j * s) - ((-1j) ** j) * np.exp(-1j * s))
    z = r1 * np.real(((3j) ** j) * np.exp(3j * s))
    return np.stack([xy.real, xy.imag, z], axis=-1)


def spectral_derivs(P, period, nder):
    M = len(P)
    kk = np.fft.fftfreq(M, d=period / M) * 2 * np.pi
    F = np.fft.fft(P, axis=0)
    return [np.real(np.fft.ifft(((1j * kk) ** j)[:, None] * F, axis=0)) for j in range(1, nder + 1)]


def closed_frame(r1):
    """closed Bishop frame of K_1 at the base samples s_k = 2 pi k/(M2/2); returns (P, N, B, alpha)."""
    def rhs(s, y):
        D1, D2 = K1d(s, r1, 1), K1d(s, r1, 2)
        vv = np.linalg.norm(D1)
        T = D1 / vv
        Tp = (D2 - np.dot(T, D2) * T) / vv
        return -np.dot(y, Tp) * T

    T0 = K1d(0.0, r1, 1)
    T0 = T0 / np.linalg.norm(T0)
    ez = np.array([0.0, 0.0, 1.0])
    assert abs(T0 @ ez) <= 0.9
    N0 = ez - (ez @ T0) * T0
    N0 /= np.linalg.norm(N0)
    sb = 2 * np.pi * np.arange(M2 // 2) / (M2 // 2)
    sol = solve_ivp(rhs, (0, 2 * np.pi), N0, method="DOP853", rtol=1e-12, atol=1e-13, t_eval=np.append(sb, 2 * np.pi))
    Nn = sol.y.T
    Nend, Nn = Nn[-1], Nn[:-1]
    Tb = K1d(sb, r1, 1)
    Tb /= np.linalg.norm(Tb, axis=1)[:, None]
    B0 = np.cross(T0, N0)
    alpha = float(np.arctan2(Nend @ B0, Nend @ N0))        # in (-pi, pi]
    om = -alpha * sb / (2 * np.pi)
    Bn = np.cross(Tb, Nn)
    Nc = np.cos(om)[:, None] * Nn + np.sin(om)[:, None] * Bn
    Bc = np.cross(Tb, Nc)
    return K1d(sb, r1, 0), Nc, Bc, alpha


def r2kappa(frame, r2, phi):
    P, Nc, Bc, _ = frame
    tt = 4 * np.pi * np.arange(M2) / M2
    th = 1.5 * tt + phi
    K2 = np.vstack([P, P]) + r2 * (np.cos(th)[:, None] * np.vstack([Nc, Nc]) + np.sin(th)[:, None] * np.vstack([Bc, Bc]))
    D1, D2 = spectral_derivs(K2, 4 * np.pi, 2)
    kap = np.linalg.norm(np.cross(D1, D2), axis=1) / np.linalg.norm(D1, axis=1) ** 3
    F = np.abs(np.fft.fft(K2, axis=0))
    tail = float(F[M2 // 2 - 50: M2 // 2 + 50].max() / F.max())
    return float(r2 * kap.max()), tail


def main():
    t0, c0 = time.time(), time.process_time()
    out = dict(rows=[], kappa_min_K1={})
    s = np.linspace(0, 2 * np.pi, 200001)[:-1]
    for lab, r1 in (("0.25", 0.25), ("0.35", 0.35), ("4/13", 4 / 13), ("0.5", 0.5)):
        D1, D2 = K1d(s, r1, 1), K1d(s, r1, 2)
        k = np.linalg.norm(np.cross(D1, D2), axis=1) / np.linalg.norm(D1, axis=1) ** 3
        out["kappa_min_K1"][lab] = dict(kappa_min=float(k.min()), s_argmin=float(s[k.argmin()]),
                                       formula_at_pi_half=abs(4 - 13 * r1) / (4 * (1 - r1) ** 2 + 9 * r1 ** 2))
        print(f"kappa_min(K_1) at r_1 = {lab}: {k.min():.4f} at s = {s[k.argmin()]:.4f}; "
              f"|4-13r|/(4(1-r)^2+9r^2) = {out['kappa_min_K1'][lab]['formula_at_pi_half']:.4f}")
    grid = {round(0.05 * i, 4): 24 for i in range(1, 9)}
    grid.update({round(0.45 + 0.0025 * i, 4): 48 for i in range(21)})
    grid.update({x: 48 for x in (0.4901, 0.4902, 0.4903, 0.4904, 0.4905, 0.4906, 0.4907, 0.4908)})
    grid = sorted(grid.items())
    tail_max = 0.0
    frames = {}
    for r1, nph in grid:
        fr = closed_frame(r1)
        frames[r1] = fr
        vals = []
        for ph in np.pi * np.arange(nph) / nph:
            v, tail = r2kappa(fr, r1 / 2, ph)
            vals.append(v)
            tail_max = max(tail_max, tail)
        i = int(np.argmax(vals))
        row = dict(r1=r1, r2=r1 / 2, alpha2=fr[3], m2=1.5 - fr[3] / (2 * np.pi), n_phases=nph,
                   max_r2kappa=float(vals[i]), phi2_argmax=float(np.pi * i / nph), default_phase=float(vals[0]),
                   min_r2kappa=float(min(vals)))
        out["rows"].append(row)
        print(f"r_1 = {r1:.4f}: alpha_2 = {row['alpha2']:+.4f}, m_2 = {row['m2']:.4f}; r_2 kappa_max(K_2): "
              f"phi_2 = 0 -> {row['default_phase']:.4f}, max over {nph} phases {row['max_r2kappa']:.4f} "
              f"(phi_2 = {row['phi2_argmax']:.3f}), min {row['min_r2kappa']:.4f}")
    best = max(out["rows"], key=lambda x: x["max_r2kappa"])
    # local refinement of (r_1, phi_2) around the grid maximum
    ref = []
    for r1 in np.round(best["r1"] + 0.0005 * np.arange(-4, 5), 5):
        if not (0 < r1 <= 0.5):
            continue
        fr = frames.get(float(r1)) or closed_frame(float(r1))
        for ph in best["phi2_argmax"] + (np.pi / 48) * np.linspace(-1, 1, 21):
            v, tail = r2kappa(fr, r1 / 2, ph)
            tail_max = max(tail_max, tail)
            ref.append(dict(r1=float(r1), phi2=float(ph % np.pi), r2kappa=v, alpha2=fr[3]))
    rb = max(ref, key=lambda x: x["r2kappa"])
    half = [x for x in out["rows"] if abs(x["r1"] - 0.5) < 1e-12][0]
    out["summary"] = dict(
        grid_max=best["max_r2kappa"], grid_argmax_r1=best["r1"], grid_argmax_phi2=best["phi2_argmax"],
        refined_max=rb["r2kappa"], refined_argmax_r1=rb["r1"], refined_argmax_phi2=rb["phi2"],
        refined_alpha2=rb["alpha2"], overall_max=max(rb["r2kappa"], best["max_r2kappa"]),
        half_default_phase=half["default_phase"], half_max_over_phases=half["max_r2kappa"],
        half_alpha2=half["alpha2"], half_m2=half["m2"], spectral_tail_max=tail_max,
        r1_cross=[x["r1"] for x in out["rows"] if x["alpha2"] > 0 and x["r1"] > 0.45][-1])
    sm = out["summary"]
    print(f"\ngrid max r_2 kappa_max(K_2) = {sm['grid_max']:.4f} at r_1 = {sm['grid_argmax_r1']}, phi_2 = "
          f"{sm['grid_argmax_phi2']:.3f}; refined {sm['refined_max']:.4f} at r_1 = {sm['refined_argmax_r1']}, phi_2 = "
          f"{sm['refined_argmax_phi2']:.3f} (alpha_2 = {sm['refined_alpha2']:+.4f})")
    print(f"r_1 = 0.5: default phase {sm['half_default_phase']:.4f}, max over phases {sm['half_max_over_phases']:.4f}; "
          f"alpha_2 = {sm['half_alpha2']:+.4f}, m_2 = {sm['half_m2']:.4f}; last r_1 > 0.45 with alpha_2 > 0: "
          f"{sm['r1_cross']}; spectral tail <= {tail_max:.1e}")
    out["meta"] = dict(seconds_wall=time.time() - t0, seconds_cpu=time.process_time() - c0, M2=M2)
    with open(os.path.join(os.path.dirname(HERE), "results", "smooth_d2_phases.json"), "w") as fh:
        json.dump(out, fh, indent=1)
    print(f"wall {out['meta']['seconds_wall']:.1f} s, CPU {out['meta']['seconds_cpu']:.1f} s; wrote smooth_d2_phases.json")


if __name__ == "__main__":
    main()
