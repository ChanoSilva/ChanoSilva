#!/usr/bin/env python3
"""RTK001 round 3 -- numerical checks for the (H_3)-uniformity analysis (theory/H3_uniform_derivation.md).

On the real polygons of experiments/recursive_knots.py ((2,3), r_d = f * tau_measured(K_{d-1})):
  [D]   per level j: v_min, v_max, kappa_max, nu = sup|v'|/v^2, mu = sup|Pi_perp dk/dsigma|,
        M_v = sup|v'|, M_kappa = sup|kappa_par'| (parameter t), and the user's r_{j+1} M_v / v_min, r_{j+1}^2 M_kappa
  [W]   identity (1.2): w' = c_T (a_0 - r v m kappa_W)/w   vs finite differences of |K_d'|
  [NU]  speed recursion (Prop. 2.1):   nu_d <= nu/(1-eps) + (r mu + lam kappa_max)/(1-eps)^2
  [KA]  curvature recursion (Prop. 2.2): kappa_max(K_d) <= kappa G(zeta')/(1-eps) + 1/(r(1+zeta'^2)) + lam(nu(1+eps)+r mu)/(1-eps)^3
  [TOL] tolerance (Cor. 2.3), d >= 3:   26.63 4^-d nu_{d-1} + 17.75 8^-d mu_{d-1} <= 0.896  (a priori constants)
        sharp form with measured eps, lam:  S_d := eps G/(1-eps) + 1/(1+zeta'^2) + r lam (nu(1+eps)+r mu)/(1-eps)^3 <= 2
  [LOSS] size of the lost-derivative coefficient r_d sin(chi_hi) and of the fourth-order term
Run time target: < 3 min CPU.  Output: theory/check_H3_output.txt

FROZEN COPY for v0.4 (review round 3): identical to theory/check_H3.py except that (i) it writes to results/
(results/check_H3_output.txt) and (ii) it also writes results/check_H3_summary.json (the numbers printed in the
text output, collected in SUMMARY). make_numbers.py reads only the JSON. SHA-256 in results/FROZEN_THEORY_SHA256.txt.
"""
import os
import sys
import time

import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
sys.path.insert(0, os.path.join(ROOT, "experiments"))
import recursive_knots as rk  # noqa: E402

OUT = []
SUMMARY = []


def log(*a):
    s = " ".join(str(x) for x in a)
    print(s, flush=True)
    OUT.append(s)


def d1(F, dt):
    return (np.roll(F, -1, 0) - np.roll(F, 1, 0)) / (2 * dt)


def d2(F, dt):
    return (np.roll(F, -1, 0) - 2 * F + np.roll(F, 1, 0)) / dt ** 2


def d3(F, dt):
    return (np.roll(F, -2, 0) - 2 * np.roll(F, -1, 0) + 2 * np.roll(F, 1, 0) - np.roll(F, 2, 0)) / (2 * dt ** 3)


def g(z):
    return z * (z ** 2 + 2) / (z ** 2 + 1) ** 1.5


def G(zmin):
    return g(np.sqrt(2.0)) if zmin <= np.sqrt(2.0) else g(zmin)


def level_data(P):
    """Geometric data of a closed polygon P sampled at t_i = 2 pi i/M (parameter of period 2 pi)."""
    M = len(P)
    dt = 2 * np.pi / M
    Kp, Kpp, Kppp = d1(P, dt), d2(P, dt), d3(P, dt)
    v = np.linalg.norm(Kp, axis=1)
    T = Kp / v[:, None]
    vp = np.einsum("ij,ij->i", T, Kpp)                       # v' = T.K''
    k = (Kpp - vp[:, None] * T) / v[:, None] ** 2            # curvature vector dT/dsigma
    kap = np.linalg.norm(k, axis=1)
    kp = d1(k, dt)                                           # dk/dt
    kpar_p = kp - np.einsum("ij,ij->i", kp, T)[:, None] * T  # Pi_perp dk/dt = kappa_par'
    Mk = np.linalg.norm(kpar_p, axis=1)
    # check K''' = v'' T + 3 v v' k + v^2 dk/dt (the identity used in the text)
    return dict(M=M, dt=dt, v=v, T=T, vp=vp, k=k, kap=kap, kpar_p=kpar_p, Mk=Mk,
                nu=float(np.max(np.abs(vp) / v ** 2)), mu=float(np.max(Mk / v)),
                Mv=float(np.max(np.abs(vp))), Mkap=float(np.max(Mk)),
                vmin=float(v.min()), vmax=float(v.max()), kmax=float(kap.max()),
                K3=float(np.linalg.norm(Kppp, axis=1).max()))


def chain(N0, f, depth, measure_upto):
    P = rk.circle(N0)
    taus = [1.0]
    levels = [P]
    alphas = [None]
    for d in range(1, depth + 1):
        T, Nn, B, alpha = rk.bishop_frame(P)
        r = f * taus[-1]
        Q = rk.offset(P, Nn, B, r, 2, 3)
        if d <= measure_upto:
            tau = rk.measure(Q)["tau"]
        else:
            tau = np.nan
        taus.append(tau)
        levels.append(Q)
        alphas.append(float(alpha))
        P = Q
    return levels, taus, alphas


def check_W(Pb, r, alpha, p=2, q=3):
    """Identity (1.2) on the level built over base Pb, in the base parameter t (no reparametrisation)."""
    bd = level_data(Pb)
    M, dt = bd["M"], bd["dt"]
    _, Nn, B, _ = rk.bishop_frame(Pb)
    j = np.arange(p * M)
    i = j % M
    theta = q * (2 * np.pi * j / M) / p
    U = np.cos(theta)[:, None] * Nn[i] + np.sin(theta)[:, None] * B[i]
    T = bd["T"][i]
    W = np.cross(T, U)
    k = bd["k"][i]
    x = r * np.einsum("ij,ij->i", k, U)
    kW = np.einsum("ij,ij->i", k, W)
    kdot = np.einsum("ij,ij->i", bd["kpar_p"][i], U)
    v, vp = bd["v"][i], bd["vp"][i]
    m = q / p - alpha / (2 * np.pi)
    a0 = vp * (1 - x) - r * v * kdot
    cT = v * (1 - x)
    w = np.sqrt(cT ** 2 + (r * m) ** 2)
    wp_pred = cT * (a0 - r * v * m * kW) / w
    Q = Pb[i] + r * U
    wfd = np.linalg.norm(d1(Q, dt), axis=1)
    wp_fd = d1(wfd, dt)
    rel_w = float(np.max(np.abs(wfd - w)) / np.max(w))
    rel_wp = float(np.max(np.abs(wp_fd - wp_pred)) / np.max(np.abs(wp_fd)))
    # lost-derivative term: r sin(chi) |v kappa_par''.U + v'' kappa_perp + 2 v' kappa_perp'|, compared with |Pi_perp K_d'''|
    kpp = d1(bd["kpar_p"], dt)                              # (d/dt) of kappa_par' (contains kappa_par'')
    vpp = d1(bd["vp"], dt)
    kperp_p = d1(np.einsum("ij,ij->i", bd["k"][i], U), dt) if False else None
    four = r * np.abs(v * np.einsum("ij,ij->i", kpp[i], U) + vpp[i] * x / r)
    sinchi = (r * m) / w
    Kd3 = d3(Q, dt)
    Td = d1(Q, dt) / wfd[:, None]
    Kd3n = np.linalg.norm(Kd3 - np.einsum("ij,ij->i", Kd3, Td)[:, None] * Td, axis=1)
    return dict(rel_w=rel_w, rel_wp=rel_wp, m=m, loss_max=float(np.max(sinchi * four)),
                Kd3n_max=float(Kd3n.max()), sinchi_max=float(sinchi.max()))


def run(f, N0, depth, measure_upto, tag):
    t0 = time.time()
    levels, taus, alphas = chain(N0, f, depth, measure_upto)
    log(f"\n=== (2,3) f={f} N0={N0} depth={depth} [{tag}] ===")
    data = [level_data(_reparam(P)) for P in levels]
    for j, (P, D) in enumerate(zip(levels, data)):
        rnext = f * taus[j] if j < depth else np.nan
        log(f"[D] j={j} N={D['M']} tau={taus[j]:.5f} v=[{D['vmin']:.4f},{D['vmax']:.4f}] kappa_max={D['kmax']:.4f} "
            f"nu={D['nu']:.4f} mu={D['mu']:.4f} M_v={D['Mv']:.4f} M_kappa={D['Mkap']:.4f} |K'''|max={D['K3']:.3f} "
            f"| r_(j+1) M_v/v_min={rnext*D['Mv']/D['vmin']:.4f} r_(j+1)^2 M_kappa={rnext**2*D['Mkap']:.5f} "
            f"r_(j+1) kappa_max={rnext*D['kmax']:.4f}")
    res = []
    for d in range(1, depth + 1):
        B_, Dd = data[d - 1], data[d]
        r = f * taus[d - 1]
        alpha = alphas[d]
        m = 1.5 - alpha / (2 * np.pi)
        eps = r * B_["kmax"]
        lam = r * m / B_["vmin"]
        zeta = B_["vmin"] * (1 - eps) / (r * m)
        nu_b = B_["nu"] / (1 - eps) + (r * B_["mu"] + lam * B_["kmax"]) / (1 - eps) ** 2
        ka_b = B_["kmax"] * G(zeta) / (1 - eps) + 1 / (r * (1 + zeta ** 2)) + lam * (B_["nu"] * (1 + eps) + r * B_["mu"]) / (1 - eps) ** 3
        S = eps * G(zeta) / (1 - eps) + 1 / (1 + zeta ** 2) + r * lam * (B_["nu"] * (1 + eps) + r * B_["mu"]) / (1 - eps) ** 3
        W = check_W(levels[d - 1] if d > 1 else levels[0], r, alpha) if levels[d - 1].shape[0] <= 4096 else None
        log(f"[W]  d={d}: |w|-identity rel.err {W['rel_w']:.2e}; w'-identity (1.2) rel.err {W['rel_wp']:.2e} (m={W['m']:.4f})")
        log(f"[NU] d={d}: measured nu_d={Dd['nu']:.4f} <= bound {nu_b:.4f} ? {Dd['nu'] <= nu_b}  (ratio {Dd['nu']/nu_b:.3f}; eps={eps:.4f}, lam={lam:.5f})")
        log(f"[KA] d={d}: measured kappa_max(K_d)={Dd['kmax']:.4f} <= bound {ka_b:.4f} ? {Dd['kmax'] <= ka_b}  (ratio {Dd['kmax']/ka_b:.3f}); "
            f"r_d*bound = {r*ka_b:.4f} (<= 2 needed), measured r_d kappa_max = {r*Dd['kmax']:.4f}")
        log(f"[TOL] d={d}: sharp S_d = {S:.4f} <= 2 ? {S <= 2}   (zeta'={zeta:.3f})")
        Tap = None
        if d >= 3:
            Tap = 96 / np.sqrt(13) * 4.0 ** (-d) * B_["nu"] + 64 / np.sqrt(13) * 8.0 ** (-d) * B_["mu"]
            log(f"[TOL] d={d}: a-priori LHS 26.63*4^-d*nu_(d-1) + 17.75*8^-d*mu_(d-1) = {Tap:.4f} <= 0.896 ? {Tap <= 0.896}; "
                f"checks of the a-priori inputs: r_d={r:.5f} <= 2^-d={2.0**-d:.5f} ? {r <= 2.0**-d}; "
                f"lam={lam:.5f} <= 2^(3-d)/sqrt13={2.0**(3-d)/np.sqrt(13):.5f} ? {lam <= 2.0**(3-d)/np.sqrt(13)}; eps={eps:.4f} <= f ? {eps <= f}")
        log(f"[LOSS] d={d}: sup sin(chi)={W['sinchi_max']:.5f}, sup r sin(chi)|v kpar''.U + v'' x/r| = {W['loss_max']:.4f} vs sup|Pi_perp K_d'''| = {W['Kd3n_max']:.3f} (parameter t of K_(d-1))")
        res.append(dict(d=d, nu=Dd["nu"], nu_b=nu_b, ka=Dd["kmax"], ka_b=ka_b, S=S, Tap=Tap, r=r, eps=eps, lam=lam,
                        sinchi=W["sinchi_max"], rel_wp=W["rel_wp"]))
    log(f"[growth] nu: " + ", ".join(f"{D['nu']:.3f}" for D in data) + " | mu: " + ", ".join(f"{D['mu']:.3f}" for D in data)
        + " | kappa_max: " + ", ".join(f"{D['kmax']:.3f}" for D in data)
        + " | M_v: " + ", ".join(f"{D['Mv']:.3f}" for D in data) + " | M_kappa: " + ", ".join(f"{D['Mkap']:.3f}" for D in data))
    SUMMARY.append(dict(tag=tag, f=f, N0=N0, depth=depth, checks=res,
                        levels=[dict(j=j, nu=D["nu"], mu=D["mu"], kmax=D["kmax"], vmin=D["vmin"], vmax=D["vmax"])
                                for j, D in enumerate(data)]))
    log(f"({tag} done in {time.time()-t0:.1f}s)")
    return res


def _reparam(P):
    """Polygons are already sampled at t_i = 2 pi i/N over one period (period-2pi parametrisation of each level)."""
    return P


def main():
    t0 = time.time()
    log("check_H3.py -- RTK001 round 3; (2,3), r_d = f tau_meas(K_(d-1)); derivatives by central differences in t")
    run(0.5, 256, 3, 2, "f=1/2, N0=256")
    run(0.5, 512, 3, 2, "f=1/2, N0=512 (resolution)")
    run(0.35, 256, 3, 2, "f=0.35")
    run(0.25, 256, 3, 2, "f=0.25")
    run(0.5, 128, 4, 3, "f=1/2, d=4, reduced N0=128")
    log(f"\ntotal {time.time()-t0:.1f}s")
    with open(os.path.join(ROOT, "results", "check_H3_output.txt"), "w") as fh:
        fh.write("\n".join(OUT) + "\n")
    import json
    with open(os.path.join(ROOT, "results", "check_H3_summary.json"), "w") as fh:
        json.dump(SUMMARY, fh, indent=1)


if __name__ == "__main__":
    main()
