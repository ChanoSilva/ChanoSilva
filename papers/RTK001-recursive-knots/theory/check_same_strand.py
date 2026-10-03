#!/usr/bin/env python3
"""Numerical checks for theory/same_strand_derivation.md (same-strand doubly critical pairs, p = 2)
on the real RTK001 family, reusing experiments/recursive_knots.py and theory/check_Hc.py.

Per level d of each (2,3) chain:
  [X]   cone angle chi(t) = angle(T_d, T) of K_d lies in [chi_lo, chi_hi]  (chi_hi = arctan(1/zeta_min)).
  [R1]  discrete turning of T_d per unit base arclength <= Omega_bar (route R1; (H_3) data for d >= 2).
  [Y]   |dY/dsigma| <= kappa + (m/v) sin(chi_1) <= 1/tau + sin(chi_1)/h_min for Y = cos chi_1 T + sin chi_1 W.
  [T]   on every same-strand arc (k = 0, shorter base arc, delta < delta_cap): discrete
        max_t [a(t) + b(t)] <= 2 dchi + delta + u sin(chi_hi)  (route R2), total turning <= tau Omega_bar delta (R1),
        and, for delta < delta_turn, (X2 - X1).(T1 + T2) > 0 (conclusion of Lemma T: not doubly critical).
  [DC]  census of doubly critical pairs on the polygon: (a) vertex pairs that are local minima of the distance
        in both indices, (b) cells where both (X_j-X_i).T_i and (X_j-X_i).T_j change sign (catches saddles/maxima);
        same-strand local ones must have delta >= delta_turn and distance >= 2 c_0 r.
  [c0]  new same-strand constants: c0_Lam = (1/2r) inf_{delta >= delta_turn} max(Lambda, l0 - 2r) (1-D, Lipschitz-
        corrected) and c0_2D (with the P_0 term, grid value).
  [Kap] refined curvature bound (exact identity, psi kept pointwise, sup over (x, v)) vs measured kappa_d.
  [AP]  a-priori constants for the (2,3) family: Theta_min >= 1.8028 * 2^(d-2) (d >= 2), delta_R2^ap.
Runtime target <= 3 CPU minutes.
"""
import os, sys, time, json
import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
sys.path.insert(0, HERE)
sys.path.insert(0, os.path.join(ROOT, "experiments"))
sys.argv = [sys.argv[0]]
from recursive_knots import circle, bishop_frame, offset, measure, tangents  # noqa: E402
from check_Hc import base_data, Lambda, l0, Pfun, curvature_bound  # noqa: E402

OUT = []
def log(*a):
    s = " ".join(str(x) for x in a)
    print(s, flush=True)
    OUT.append(s)

PI = np.pi

# ----------------------------------------------------------------------------
# constants
# ----------------------------------------------------------------------------
def turning_constants(f, Th_min, zeta, dchi=None, tauG3p=0.0):
    """Route R1: tau*Omega_bar = 1 + sin^2 chi_hi + sin chi_hi / Theta_min + tau Gamma_3'; delta_R1 = pi / (tau Omega_bar).
       Route R2: delta_R2 = (pi - 2 dchi) / (1 + sin chi_hi / Theta_min); a-priori version uses dchi = chi_hi."""
    chi_hi = np.arctan(1.0 / zeta)
    s = np.sin(chi_hi)
    tauOm = 1 + s ** 2 + s / Th_min + tauG3p
    dR1 = PI / tauOm
    if dchi is None:
        dchi = chi_hi
    dR2 = (PI - 2 * dchi) / (1 + s / Th_min)
    return dict(chi_hi=chi_hi, sin_hi=s, tauOm=tauOm, dR1=dR1, dR2=dR2)

def c0_lambda(f, delta_lo, ngrid=40000):
    """(1/2) inf_{delta in [delta_lo, pi)} max(Lambda/r, l0/r - 2), r = 1, tau = 1/f; with Lipschitz correction."""
    if delta_lo >= PI:
        return np.inf, None, np.inf
    tau = 1.0 / f
    d = np.linspace(delta_lo, PI, ngrid)
    F = np.maximum(Lambda(d, tau, 1.0), l0(d, tau) - 2.0)
    i = int(np.argmin(F))
    step = d[1] - d[0]
    lip = float(np.abs(np.diff(F)).max() / step)
    return F[i] / 2, float(d[i]), (F[i] - 2 * lip * step) / 2

def c0_2d(f, Th_min, Th_max, delta_lo, ngrid=1500, nu=300):
    """(1/2) inf over delta in [delta_lo, pi), u in [delta/Th_max, delta/Th_min] of max(sqrt(Lam_+^2 + P_0^2), l0 - 2)."""
    if delta_lo >= PI:
        return np.inf, None
    tau = 1.0 / f
    best, arg = np.inf, None
    for d in np.linspace(delta_lo, PI, ngrid):
        us = np.linspace(d / Th_max, d / Th_min, nu)
        dd = np.full_like(us, d)
        val = np.maximum(np.sqrt(np.clip(Lambda(dd, tau, 1.0), 0, None) ** 2 + Pfun(dd, us) ** 2), l0(dd, tau) - 2.0)
        j = int(np.argmin(val))
        if val[j] < best:
            best, arg = float(val[j]), (float(d), float(us[j]))
    return best / 2, arg

def kappa_hat(f, tau, r, m, vmin, vmax, V1, K1, nx=1601, nv=161):
    """Refined a-priori curvature bound (route 1 of the task): with x = r kappa_perp in [-f, f], |kappa_W| <= sqrt(1/tau^2 - x^2/r^2),
       |a_0| <= V1 (1 - x) + r v K1, A = v^2 (1-x)^2, B = r^2 m^2:
       kappa_d <= sup_{x, v} sqrt( b_U^2 (A+B) + (r m |a_0| + |kappa_W| v (A + 2B))^2 ) / (A+B)^{3/2}.
       Returns grid sup and a Lipschitz-corrected value."""
    x = np.linspace(-f, f, nx)[:, None]
    v = np.linspace(vmin, vmax, nv)[None, :] if vmax > vmin * (1 + 1e-9) else np.array([[vmin]])
    kap = 1.0 / tau
    kW = np.sqrt(np.clip(kap ** 2 - (x / r) ** 2, 0, None))
    A = v ** 2 * (1 - x) ** 2
    B = (r * m) ** 2
    bU = v ** 2 * (1 - x) * (x / r) - r * m ** 2
    a0 = V1 * (1 - x) + r * v * K1
    num = bU ** 2 * (A + B) + (r * m * a0 + kW * v * (A + 2 * B)) ** 2
    F = np.sqrt(num) / (A + B) ** 1.5
    i = np.unravel_index(int(np.argmax(F)), F.shape)
    # Lipschitz correction (finite differences, x2 safety) -- sqrt(1/tau^2 - x^2/r^2) has infinite slope at |x| = f,
    # so we correct with the observed max increment between neighbours instead of slope*step
    incx = np.abs(np.diff(F, axis=0)).max() if F.shape[0] > 1 else 0.0
    incv = np.abs(np.diff(F, axis=1)).max() if F.shape[1] > 1 else 0.0
    return float(F[i]), float(F[i] + 2 * (incx + incv)), (float(x[i[0], 0]), float(v[0, min(i[1], v.shape[1] - 1)]))

# ----------------------------------------------------------------------------
# per-level checks
# ----------------------------------------------------------------------------
def check_level(P, tau_b, r, p, q, Q, meas, label, Theta_ap=None):
    t0 = time.time()
    bd = base_data(P)
    M = len(P); NQ = len(Q)
    alpha = bd["alpha"]; m = q / p - alpha / (2 * PI)
    v = bd["v"]; vmin, vmax = float(v.min()), float(v.max())
    f = r / tau_b
    hmin, hmax = vmin / m, vmax / m
    Th_min, Th_max = hmin / tau_b, hmax / tau_b
    zeta = (1 - f) * hmin / r
    V1 = float(np.abs(bd["vp"]).max())
    K1 = float((np.sqrt(bd["k1p"] ** 2 + bd["k2p"] ** 2) + abs(alpha) / (2 * PI) * bd["kap"]).max())
    chi_hi = float(np.arctan(r * m / (vmin * (1 - f))))
    chi_lo = float(np.arctan(r * m / (vmax * (1 + f))))
    dchi = chi_hi - chi_lo
    G3p = r * m * (V1 * (1 + f) / vmin + r * K1) / (vmin ** 2 * (1 - f) ** 2 + r ** 2 * m ** 2)
    tc = turning_constants(f, Th_min, zeta, dchi=dchi, tauG3p=tau_b * G3p)
    dR1, dR2, tauOm, s_hi = tc["dR1"], tc["dR2"], tc["tauOm"], tc["sin_hi"]
    # the route used for the proved statement: d = 1 (circle base, a_0 = 0): R1; d >= 2: R2 (no H_3)
    circle_base = (V1 < 1e-8 and K1 < 1e-8)
    d_turn = dR1 if circle_base else dR2
    d_turn_best = max(dR1, dR2)
    log(f"\n=== {label}: M={M}, N_d={NQ}, r={r:.5f}, tau={tau_b:.5f}, f={f:.4f}, m={m:.4f}, v in [{vmin:.4f},{vmax:.4f}], "
        f"Theta in [{Th_min:.4f},{Th_max:.4f}], zeta_min={zeta:.4f}")
    log(f"[const] chi in [{chi_lo:.4f},{chi_hi:.4f}] (dchi={dchi:.4f}); R1: tau*Omega_bar = 1 + {s_hi**2:.4f} + {s_hi/Th_min:.4f} + "
        f"tau*Gamma3' {tau_b*G3p:.4f} = {tauOm:.4f} -> delta_R1 = {dR1:.4f}; R2 (no H_3): delta_R2 = {dR2:.4f}; "
        f"pi/3 = {PI/3:.4f}; route used: {'R1 (circle base, a_0=0)' if circle_base else 'R2 (no H_3)'} -> delta_turn = {d_turn:.4f} "
        f"(>= pi/3? {d_turn >= PI/3})")
    # ---- discrete geometry of K_d
    jidx = np.arange(NQ); bj = jidx % M
    theta = q * (2 * PI * jidx / M) / p
    Tb, Nb, Bb = bd["T"][bj], bd["N"][bj], bd["B"][bj]
    U = np.cos(theta)[:, None] * Nb + np.sin(theta)[:, None] * Bb
    W = np.cross(Tb, U)
    Td = tangents(Q)
    chi = np.arctan2(np.einsum("ij,ij->i", Td, W), np.einsum("ij,ij->i", Td, Tb))
    offU = np.abs(np.einsum("ij,ij->i", Td, U)).max()
    log(f"[X] chi(t) in [{chi.min():.5f},{chi.max():.5f}] vs bound [{chi_lo:.5f},{chi_hi:.5f}]: "
        f"slack lo {chi.min()-chi_lo:+.2e}, hi {chi_hi-chi.max():+.2e} (>= -O(1/M^2)); max |T_d.U| = {offU:.1e}")
    seg = np.linalg.norm(np.roll(P, -1, 0) - P, axis=1)       # base arclength of step b -> b+1
    dsig = seg[bj]                                             # step j -> j+1 of K_d covers base step bj -> bj+1
    turn = np.arccos(np.clip(np.einsum("ij,ij->i", Td, np.roll(Td, -1, 0)), -1, 1))
    rate = turn / dsig
    log(f"[R1] max discrete turning of T_d per base arclength * tau = {tau_b*rate.max():.4f} <= tau*Omega_bar = {tauOm:.4f}? "
        f"{tau_b*rate.max() <= tauOm*(1+1e-3)} (ratio {tau_b*rate.max()/tauOm:.3f})")
    worstY = -np.inf; worstYg = -np.inf
    for c1 in [chi_lo, 0.5 * (chi_lo + chi_hi), chi_hi]:
        Y = np.cos(c1) * Tb + np.sin(c1) * W
        dY = np.linalg.norm(np.roll(Y, -1, 0) - Y, axis=1) / dsig
        bound_pt = bd["kap"][bj] + (m / v[bj]) * np.sin(c1)                    # kappa + (m/v) sin chi_1  (pointwise)
        bound_gl = 1 / tau_b + np.sin(c1) / hmin                               # 1/tau + sin chi_1 / h_min
        worstY = max(worstY, float((dY / bound_pt).max()))
        worstYg = max(worstYg, float((dY / bound_gl).max()))
    log(f"[Y] max |dY/dsigma| / (kappa + (m/v) sin chi_1) over chi_1 in {{lo, mid, hi}} = {worstY:.4f} (pointwise, forward difference: <= 1 + O(1/M)); "
        f"max |dY/dsigma| / (1/tau + sin chi_1/h_min) = {worstYg:.4f} (the bound used in R2: <= 1 required)")
    # ---- [T] all same-strand arcs with delta < delta_cap
    S = bd["S"]; L = bd["L"]
    d_cap = min(PI, 1.25 * d_turn_best)
    Wmax = int(np.searchsorted(np.cumsum(np.sort(seg)), d_cap * tau_b)) + 2   # max steps for base arclength d_cap*tau
    Wmax = min(Wmax, M - 1)
    stride = max(1, int(np.ceil(NQ * Wmax ** 2 / 1.5e8)))
    worst_R2, worst_R1, minF_below, n_below, n_pairs, maxab_below = -np.inf, -np.inf, np.inf, 0, 0, 0.0
    cums = np.concatenate([[0.0], np.cumsum(np.concatenate([seg, seg]))])
    for i in range(0, NQ, stride):
        idx = (i + np.arange(Wmax + 1)) % NQ
        Tw = Td[idx]
        ang = np.arccos(np.clip(Tw @ Tw.T, -1, 1))
        Ssum = ang[:, 0][:, None] + ang                           # a(t) + b_n(t), rows t, columns n
        tri = np.arange(Wmax + 1)[:, None] > np.arange(Wmax + 1)[None, :]
        Ssum[tri] = -np.inf
        abmax = Ssum.max(axis=0)                                  # max_{t <= n} a(t) + b_n(t)
        n = np.arange(1, Wmax + 1)
        b0 = i % M
        sig = cums[b0 + n] - cums[b0]
        keep = (sig <= L / 2) & (sig / tau_b < d_cap)
        if not keep.any():
            continue
        n = n[keep]; sig = sig[keep]; delta = sig / tau_b
        u = m * n * bd["dt"]
        ab = abmax[n]
        Phi = np.concatenate([[0.0], np.cumsum(turn[idx[:-1]])])[n]
        bR2 = 2 * dchi + delta + u * s_hi
        worst_R2 = max(worst_R2, float((ab - bR2).max()))
        worst_R1 = max(worst_R1, float((Phi - tauOm * delta).max()))
        X1 = Q[i]; X2 = Q[idx[n]]
        F = (X2 - X1) @ Td[i] + np.einsum("ij,ij->i", X2 - X1, Td[idx[n]])
        below = delta < d_turn
        n_pairs += int(len(n)); n_below += int(below.sum())
        if below.any():
            minF_below = min(minF_below, float((F[below] / np.linalg.norm(X2 - X1, axis=1)[below]).min()))
            maxab_below = max(maxab_below, float(ab[below].max()))
    log(f"[T] same-strand arcs checked: {n_pairs} (stride {stride}, up to {Wmax} steps, delta < {d_cap:.3f}); "
        f"max[(a+b)_max - (2dchi + delta + u sin chi_hi)] = {worst_R2:+.2e} (<= O(1/M)); "
        f"max[Phi - tau Omega_bar delta] = {worst_R1:+.2e} (<= 0)")
    log(f"[T] arcs with delta < delta_turn = {d_turn:.4f}: {n_below}; max (a+b)_max among them = {maxab_below:.4f} (< pi required); "
        f"min (X2-X1).(T1+T2)/|X2-X1| = {minF_below:.4f} (> 0 required: not doubly critical)")
    # ---- [DC] census of doubly critical pairs
    D = np.linalg.norm(Q[:, None, :] - Q[None, :, :], axis=2)
    lm = np.ones_like(D, dtype=bool)
    for ax in (0, 1):
        for sh in (1, -1):
            lm &= D <= np.roll(D, sh, axis=ax)
    np.fill_diagonal(lm, False)
    dX = Q[None, :, :] - Q[:, None, :]                       # X_j - X_i
    g1 = np.einsum("ijk,ik->ij", dX, Td)
    g2 = np.einsum("ijk,jk->ij", dX, Td)
    del dX
    def both_signs(g):
        c = [g, np.roll(g, -1, 0), np.roll(g, -1, 1), np.roll(np.roll(g, -1, 0), -1, 1)]
        return (np.maximum.reduce(c) > 0) & (np.minimum.reduce(c) < 0)
    cell = both_signs(g1) & both_signs(g2)
    del g1, g2
    I, J = np.meshgrid(jidx, jidx, indexing="ij")
    gap = np.minimum((J - I) % NQ, (I - J) % NQ)
    cell &= gap > 2
    bi, bjj = I % M, J % M
    fwd = (bjj - bi) % M
    sig_f = (S[bjj] - S[bi]) % L
    use_f = sig_f <= L - sig_f
    sigma = np.where(use_f, sig_f, L - sig_f)
    s_par = np.where(use_f, fwd, fwd - M)
    k = np.rint((((J - I) % NQ) - s_par) / M).astype(int) % p
    delta = sigma / tau_b
    local0 = (k == 0) & (bi != bjj) & (delta < PI)
    out = {}
    for name, mask in [("vertex local minima", lm), ("sign-change cells", cell)]:
        mk = mask & local0
        allk = mask & (bi != bjj)
        if mk.any():
            dmin = float(delta[mk].min()); dist = float(D[mk].min())
            out[name] = (int(mk.sum()), dmin, dist / r)
            log(f"[DC] {name}: {int(allk.sum())} pairs with distinct base points; same-strand local (k=0, delta<pi): {int(mk.sum())}, "
                f"min delta = {dmin:.4f} (>= delta_turn {d_turn:.4f}? {dmin >= d_turn}), min dist/r = {dist/r:.4f}")
        else:
            out[name] = (0, np.inf, np.inf)
            log(f"[DC] {name}: {int(allk.sum())} pairs with distinct base points; same-strand local (k=0, delta<pi): none")
    del D, lm, cell, I, J
    # ---- constants
    c0L, dL, c0L_cert = c0_lambda(f, d_turn)
    c02, arg2 = c0_2d(f, Th_min, Th_max, d_turn)
    c0L_best, _, c0L_best_cert = c0_lambda(f, d_turn_best)
    log(f"[c0] same strand: c0_Lam(delta >= {d_turn:.4f}) = {c0L:.4f} (cert. {c0L_cert:.4f}) at delta={dL}; "
        f"with P_0 term c0_2D = {c02:.4f} at {arg2}; using max(R1,R2) (R1 needs H_3 for d>=2): c0_Lam = {c0L_best_cert:.4f}; "
        f">= 1/2? {c0L_cert >= 0.5}")
    # ---- refined curvature bound
    kh, kh_cert, argk = kappa_hat(f, tau_b, r, m, vmin, vmax, V1, K1)
    kbar_old, _ = curvature_bound(f, tau_b, r, m, vmin, vmax, V1, K1, None)
    a_, b_, c_ = np.roll(Q, 1, 0), Q, np.roll(Q, -1, 0)
    ab, bc, ca = np.linalg.norm(a_ - b_, axis=1), np.linalg.norm(b_ - c_, axis=1), np.linalg.norm(c_ - a_, axis=1)
    kd_fd = float((2 * np.linalg.norm(np.cross(b_ - a_, c_ - a_), axis=1) / (ab * bc * ca)).max())
    log(f"[Kap] refined bound r*kappa_hat = {r*kh:.4f} (Lipschitz-corrected {r*kh_cert:.4f}) at (x,v)={argk}; old r*kbar = {r*kbar_old:.4f}; "
        f"measured r*kappa_d,max = {r*kd_fd:.4f}; valid? {kh >= kd_fd*(1-5e-3)}; c_kappa new = {1/(r*kh_cert):.4f} (old {1/(r*kbar_old):.4f})")
    res = dict(label=label, f=f, r=r, tau_base=tau_b, m=m, vmin=vmin, vmax=vmax, Theta_min=Th_min, Theta_max=Th_max, zeta=zeta,
               V1=V1, K1=K1, chi_lo=chi_lo, chi_hi=chi_hi, tauOmega=tauOm, delta_R1=dR1, delta_R2=dR2, delta_turn=d_turn,
               route="R1" if circle_base else "R2", c0_Lam=c0L_cert, c0_2D=c02, c0_Lam_best=c0L_best_cert,
               r_kappa_hat=r * kh_cert, r_kbar_old=r * kbar_old, r_kappa_meas=r * kd_fd, c_kappa_new=1 / (r * kh_cert),
               c_kappa_old=1 / (r * kbar_old), T_worst_R2=worst_R2, T_worst_R1=worst_R1, T_minF_below=minF_below,
               T_n_below=n_below, DC=out, tau_d=meas["tau"], chi_meas=(float(chi.min()), float(chi.max())),
               R1_rate_meas=float(tau_b * rate.max()))
    if Theta_ap is not None:
        zap = (1 - f) * Theta_ap / f
        tap = turning_constants(f, Theta_ap, zap)
        if circle_base:   # d = 1: exact circle data (Theta = 2/3, a_0 = 0), route R1 is a priori
            res.update(Theta_ap=Theta_ap, delta_R2_ap=tap["dR1"])
            log(f"[AP] d=1 (exact circle base, route R1): delta_R1 = {tap['dR1']:.4f} >= pi/3? {tap['dR1'] >= PI/3}; "
                f"c0_Lam = {c0_lambda(f, tap['dR1'])[2]:.4f}")
        else:
            res.update(Theta_ap=Theta_ap, delta_R2_ap=tap["dR2"])
            log(f"[AP] a priori Theta_min >= {Theta_ap:.4f} (measured {Th_min:.4f}): delta_R2^ap = {tap['dR2']:.4f} >= pi/3? {tap['dR2'] >= PI/3}; "
                f"c0_Lam^ap = {c0_lambda(f, tap['dR2'])[2]:.4f}")
    log(f"    time {time.time()-t0:.1f}s")
    return res

def theta_ap(f, d):
    """A priori lower bound for Theta_min at depth d >= 2 in the (2,3) family with f_j <= 1/2 at every depth (here f_j = f):
       v_min(K_1) >= 2 sqrt((1-f)^2 + (3f/2)^2), tau_1 <= r_1 = f, v_min/tau at least doubles per depth, m <= 2."""
    if d == 1:
        return 2.0 / 3.0
    return np.sqrt((1 - f) ** 2 + 2.25 * f ** 2) / f * 2 ** (d - 2)

def run_chain(N0, f, pq, depth, label):
    P = circle(N0)
    tau_prev = measure(P)["tau"]
    out = []
    for d in range(1, depth + 1):
        p, q = pq
        T, Nn, B, alpha = bishop_frame(P)
        r = f * tau_prev
        Q = offset(P, Nn, B, r, p, q, 0.0)
        meas = measure(Q)
        out.append(check_level(P, tau_prev, r, p, q, Q, meas, f"{label} d={d}", Theta_ap=theta_ap(f, d)))
        P, tau_prev = Q, meas["tau"]
    return out

def main():
    t0 = time.time()
    log("check_same_strand.py -- checks of theory/same_strand_derivation.md on the RTK001 (2,3) family")
    # closed-form d = 1 values (exact circle base), and a-priori table
    log("\n=== closed forms ===")
    for f in [0.25, 0.35, 0.5]:
        zeta = (1 - f) / (1.5 * f)
        tc = turning_constants(f, 2 / 3, zeta, dchi=np.arctan(1.5 * f / (1 - f)) - np.arctan(1.5 * f / (1 + f)))
        log(f"  d=1, f={f}: zeta={zeta:.5f}, tau*Omega_bar = {tc['tauOm']:.6f}, delta_R1 = {tc['dR1']:.6f}, delta_R2 = {tc['dR2']:.6f} (pi/3 = {PI/3:.6f}); "
            f"c0_Lam(delta_R1) = {c0_lambda(f, tc['dR1'])[2]:.4f}; c0_2D(u = 1.5 delta) = {c0_2d(f, 2/3, 2/3, tc['dR1'])[0]:.4f}")
    for f in [0.35, 0.5]:
        for d in [2, 3, 4, 6]:
            Th = theta_ap(f, d); z = (1 - f) * Th / f
            tc = turning_constants(f, Th, z)
            log(f"  a priori f={f}, d={d}: Theta_min >= {Th:.4f}, zeta_min >= {z:.4f}, delta_R2^ap = {tc['dR2']:.4f} (>= pi/3: {tc['dR2'] >= PI/3}), "
                f"c0_Lam^ap = {c0_lambda(f, tc['dR2'])[2]:.4f}")
    # threshold Theta* (f = 1/2) for delta_R2^ap = pi/3
    Ts = np.linspace(0.5, 3, 25001)
    ok = [turning_constants(0.5, T, T)["dR2"] >= PI / 3 for T in Ts]
    log(f"  threshold: delta_R2^ap(f=1/2) >= pi/3 iff Theta_min >= {Ts[int(np.argmax(ok))]:.4f}")
    dd = np.linspace(PI / 3, PI - 1e-9, 200001)
    for f in [0.25, 0.35, 0.5]:
        log(f"  min_[pi/3, pi) Lambda/r at f={f}: {Lambda(dd, 1/f, 1.0).min():.6f} (>= 1 required)")
    summary = []
    summary += run_chain(256, 0.25, (2, 3), 3, "(2,3) f=0.25 N0=256")
    summary += run_chain(256, 0.35, (2, 3), 3, "(2,3) f=0.35 N0=256")
    summary += run_chain(256, 0.50, (2, 3), 3, "(2,3) f=0.50 N0=256")
    summary += run_chain(512, 0.50, (2, 3), 2, "(2,3) f=0.50 N0=512")
    log("\n=== SUMMARY ===")
    log("level | route | delta_turn | delta_R1 | delta_R2 | delta_R2^ap | c0_Lam (proved) | c0_2D | r kappa_hat | c_kappa new | c_kappa old | "
        "DC same-strand min delta (vertex / cells) | min dist/r | (a+b)-R2 slack | min F below")
    for s in summary:
        dc1 = s["DC"]["vertex local minima"]; dc2 = s["DC"]["sign-change cells"]
        log(f"{s['label']} | {s['route']} | {s['delta_turn']:.4f} | {s['delta_R1']:.4f} | {s['delta_R2']:.4f} | {s.get('delta_R2_ap', float('nan')):.4f} | "
            f"{s['c0_Lam']:.4f} | {s['c0_2D']:.4f} | {s['r_kappa_hat']:.4f} | {s['c_kappa_new']:.4f} | {s['c_kappa_old']:.4f} | "
            f"{dc1[1]:.4f} / {dc2[1]:.4f} | {min(dc1[2], dc2[2]):.4f} | {s['T_worst_R2']:+.1e} | {s['T_minF_below']:.4f}")
    log(f"\ntotal time {time.time()-t0:.1f}s")
    with open(os.path.join(HERE, "check_same_strand_output.txt"), "w") as fh:
        fh.write("\n".join(OUT) + "\n")
    with open(os.path.join(HERE, "check_same_strand_summary.json"), "w") as fh:
        json.dump(summary, fh, indent=1, default=float)

if __name__ == "__main__":
    main()
