#!/usr/bin/env python3
"""Numerical checks of every intermediate inequality in theory/Hc_derivation.md
on the real RTK001 family (p = 2 patterns), reusing experiments/recursive_knots.py.

Checks (per level d >= 1 of each chain):
  [A]  Lemma A on the base polygon K = K_{d-1}: for base vertex pairs with chord < 2 tau,
       the shorter arc has sigma < pi tau and chord >= 2 tau sin(sigma / 2 tau).
  [E]  (E3) |w.e| <= |w| beta(delta) for w = U_1 (perp T(a));  (E4) |U_1.(y-x)| <= E(delta);
       (E5c) |(U_2 - U~_2)_perp e| <= delta^2/3;  (E6+E3) |(U~_2-U_1)_perp e| >= 2|sin(dpsi/2)| sqrt(1-beta^2).
  [C]  components: A >= Lambda(delta) and |Q| >= r P(delta, dpsi) for all local pairs (delta < pi).
  [D]  final pair bound |X2-X1| >= max(D_k, l0 - 2r) for all local pairs, split by strand index k.
  [c1] the constant c_1(f, eta_min, eta_max) by grid minimisation, versus measured dcsd/2 / r.
  [K]  curvature: formula for K_d'' versus finite differences; bound kappa_d <= ... versus 1/minRad.
  [c0] same-strand conditional constant c_0 (uses the curvature bound).
Runtime target: <= 3 CPU minutes.
"""
import os, sys, time, json
import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
sys.path.insert(0, os.path.join(ROOT, "experiments"))
sys.argv = [sys.argv[0]]  # recursive_knots reads sys.argv for --fast
from recursive_knots import circle, bishop_frame, offset, measure, rotate, unit  # noqa: E402

OUT = []
def log(*a):
    s = " ".join(str(x) for x in a)
    print(s, flush=True)
    OUT.append(s)

# ----------------------------------------------------------------------------
# bound functions (units: lengths in r; tau = 1/f)
# ----------------------------------------------------------------------------
def l0(delta, tau):           # Lemma A chord lower bound
    return 2 * tau * np.sin(delta / 2)

def Efun(delta, tau):         # (E4)
    return np.where(delta <= np.pi / 2, tau * (1 - np.cos(delta)), tau * (1 + delta - np.pi / 2))

def beta(delta):              # (E3)
    d = np.maximum(delta, 1e-300)
    return d ** 2 / (4 * np.sin(d / 2))

def Lambda(delta, tau, r):    # (3.1) along-chord lower bound
    L0 = l0(delta, tau)
    return L0 - 2 * r * Efun(delta, tau) / np.maximum(L0, 1e-300)

def Pfun(delta, dpsi):        # (3.2) in units of r
    b2 = np.clip(1 - beta(delta) ** 2, 0, None)
    return np.clip(2 * np.abs(np.sin(dpsi / 2)) * np.sqrt(b2) - delta ** 2 / 3, 0, None)

def Dbound(delta, dpsi, tau, r):
    return np.sqrt(np.clip(Lambda(delta, tau, r), 0, None) ** 2 + (r * Pfun(delta, dpsi)) ** 2)

def pair_bound(delta, dpsi, tau, r):
    return np.maximum(Dbound(delta, dpsi, tau, r), l0(delta, tau) - 2 * r)

def c1_constant(f, eta_min, eta_max, k=1, ngrid=1500, u_lo=0.0):
    """c_k := (1/2r) inf_{delta in (0,pi), u in [delta/(f eta_max), delta/(f eta_min)]} max(D_k, l0 - 2r), r = 1."""
    r, tau = 1.0, 1.0 / f
    deltas = np.linspace(1e-4, np.pi, ngrid)
    best = np.inf; arg = None
    for d in deltas:
        ua, ub = d / (f * eta_max), d / (f * eta_min)
        ua = max(ua, u_lo)
        if ub < ua:
            continue
        us = np.linspace(ua, ub, 400)
        val = pair_bound(np.full_like(us, d), us + np.pi * k, tau, r)
        i = int(np.argmin(val))
        if val[i] < best:
            best, arg = float(val[i]), (float(d), float(us[i]))
    return best / 2, arg

# ----------------------------------------------------------------------------
# discrete geometry of the base polygon
# ----------------------------------------------------------------------------
def base_data(P):
    """Closed Bishop frame (as in the family), parallel-frame curvatures, speed, arclength."""
    M = len(P)
    dt = 2 * np.pi / M
    T, N, B, alpha = bishop_frame(P)
    Kp = (np.roll(P, -1, 0) - np.roll(P, 1, 0)) / (2 * dt)          # K'
    Kpp = (np.roll(P, -1, 0) - 2 * P + np.roll(P, 1, 0)) / dt ** 2   # K''
    v = np.linalg.norm(Kp, axis=1)
    kap = np.linalg.norm(np.cross(Kp, Kpp), axis=1) / v ** 3
    # T' = v (kappa_1 N_0 + kappa_2 B_0); in the closed frame the same components up to the twist rotation,
    # i.e. kappa_1^c = T'.N / v, kappa_2^c = T'.B / v  (closed-frame components; |(k1,k2)| = kappa)
    Tp = (np.roll(T, -1, 0) - np.roll(T, 1, 0)) / (2 * dt)
    k1 = np.einsum("ij,ij->i", Tp, N) / v
    k2 = np.einsum("ij,ij->i", Tp, B) / v
    seg = np.linalg.norm(np.roll(P, -1, 0) - P, axis=1)
    S = np.concatenate([[0.0], np.cumsum(seg)[:-1]])
    Ltot = seg.sum()
    vp = (np.roll(v, -1) - np.roll(v, 1)) / (2 * dt)
    k1p = (np.roll(k1, -1) - np.roll(k1, 1)) / (2 * dt)
    k2p = (np.roll(k2, -1) - np.roll(k2, 1)) / (2 * dt)
    return dict(M=M, dt=dt, T=T, N=N, B=B, alpha=float(alpha), v=v, kap=kap, k1=k1, k2=k2,
                S=S, L=Ltot, vp=vp, k1p=k1p, k2p=k2p)

def check_lemmaA(P, tau, bd):
    """Lemma A on base vertex pairs."""
    S, L = bd["S"], bd["L"]
    M = len(P)
    worst_ratio = np.inf; viol_arc = 0; n_pairs = 0
    for a in range(0, M, 512):
        b = min(M, a + 512)
        diff = P[a:b, None, :] - P[None, :, :]
        D = np.linalg.norm(diff, axis=2)
        dS = np.abs(S[a:b, None] - S[None, :])
        sig = np.minimum(dS, L - dS)
        mask = (D < 2 * tau) & (D > 0)
        n_pairs += int(mask.sum())
        viol_arc += int((mask & (sig >= np.pi * tau)).sum())
        with np.errstate(divide="ignore", invalid="ignore"):
            ratio = D / (2 * tau * np.sin(np.minimum(sig, np.pi * tau) / (2 * tau)))
        if mask.any():
            worst_ratio = min(worst_ratio, float(ratio[mask].min()))
    return worst_ratio, viol_arc, n_pairs

def check_level(P, tau_base, r, p, q, Q, meas, label):
    """All pair checks on level K_d = Q built over base P."""
    t0 = time.time()
    bd = base_data(P)
    M = len(P); dt = bd["dt"]
    alpha = bd["alpha"]
    m = q / p - alpha / (2 * np.pi)
    v = bd["v"]; vmin, vmax = float(v.min()), float(v.max())
    f = r / tau_base
    hmin, hmax = vmin / m, vmax / m
    eta_min, eta_max = hmin / r, hmax / r
    log(f"\n=== {label}: M={M}, N_d={len(Q)}, r={r:.5f}, tau_base={tau_base:.5f}, f={f:.4f}, "
        f"alpha={alpha:+.4f}, m={m:.4f}, v in [{vmin:.4f},{vmax:.4f}], h in [{hmin:.4f},{hmax:.4f}], "
        f"eta=h/r in [{eta_min:.3f},{eta_max:.3f}], r*kappa_max={r*bd['kap'].max():.4f}")
    # [A]
    wr, va, npairs = check_lemmaA(P, tau_base, bd)
    log(f"[A] Lemma A on base: pairs with chord<2tau: {npairs}; arcs >= pi*tau among them: {va} "
        f"(must be 0); min chord/(2 tau sin(sigma/2tau)) = {wr:.6f} (must be >= 1 - O(1/M^2))")
    # pair scan over K_d vertices
    NQ = len(Q)
    T, N, B, S, L = bd["T"], bd["N"], bd["B"], bd["S"], bd["L"]
    jidx = np.arange(NQ); base_j = jidx % M
    theta = q * (2 * np.pi * jidx / M) / p
    U = np.cos(theta)[:, None] * N[base_j] + np.sin(theta)[:, None] * B[base_j]
    res = dict(E3=np.inf, E4=np.inf, E5c=np.inf, E6=np.inf, Cmin=np.inf, Qmin=np.inf,
               D=[np.inf] * p, Dpair=[None] * p, loc=[0] * p, minDist=[np.inf] * p)
    chunk = max(16, int(2e6 // NQ))
    for a in range(0, NQ, chunk):
        b = min(NQ, a + chunk)
        I = jidx[a:b]; J = jidx
        bi = I % M; bj = J % M
        # signed parameter difference along the arclength-shorter base arc
        fwd_idx = (bj[None, :] - bi[:, None]) % M                      # forward steps
        sig_f = (S[bj][None, :] - S[bi][:, None]) % L
        sig_b = L - sig_f
        use_f = sig_f <= sig_b
        sigma = np.where(use_f, sig_f, sig_b)
        s_par = np.where(use_f, fwd_idx, fwd_idx - M) * dt             # signed base param along that arc
        Dpar = ((J[None, :] - I[:, None]) % NQ) * dt                   # K_d parameter difference in [0, 2 pi p)
        k = np.rint((Dpar - s_par) / (2 * np.pi)).astype(int) % p      # strand index relative to the arc
        dpsi = m * s_par + 2 * np.pi * q * k / p
        delta = sigma / tau_base
        X1 = Q[I][:, None, :]; X2 = Q[J][None, :, :]
        dX = X2 - X1
        dist = np.linalg.norm(dX, axis=2)
        same = (bi[:, None] == bj[None, :])
        local = (~same) & (delta < np.pi) & (delta > 0)
        if not local.any():
            continue
        # chord of base and direction e
        x = P[bi][:, None, :]; y = P[bj][None, :, :]
        C = y - x
        ell = np.linalg.norm(C, axis=2)
        e = C / np.maximum(ell, 1e-300)[..., None]
        A = np.einsum("ijk,ijk->ij", dX, e)
        Qv = dX - A[..., None] * e
        Qn = np.linalg.norm(Qv, axis=2)
        # [E3] with w = U_1 (perp T(a)): |w.e| <= beta
        U1 = U[I][:, None, :]; U2 = U[J][None, :, :]
        w_e = np.abs(np.einsum("ijk,ijk->ij", np.broadcast_to(U1, dX.shape), e))
        bet = beta(delta)
        res["E3"] = min(res["E3"], float((bet - w_e)[local].min()))
        # [E4] |U_1.(y-x)| <= E(delta)
        u1C = np.abs(np.einsum("ijk,ijk->ij", np.broadcast_to(U1, dX.shape), C))
        res["E4"] = min(res["E4"], float((Efun(delta, tau_base) - u1C)[local].min()))
        # U~_2 = angle (theta_2 - alpha s/2pi) in the closed frame at a
        ang = theta[J][None, :] - alpha * s_par / (2 * np.pi)
        Ut2 = np.cos(ang)[..., None] * N[bi][:, None, :] + np.sin(ang)[..., None] * B[bi][:, None, :]
        d5 = U2 - Ut2
        d5perp = d5 - np.einsum("ijk,ijk->ij", d5, e)[..., None] * e
        res["E5c"] = min(res["E5c"], float((delta ** 2 / 3 - np.linalg.norm(d5perp, axis=2))[local].min()))
        w = Ut2 - U1
        wperp = w - np.einsum("ijk,ijk->ij", w, e)[..., None] * e
        lhs = np.linalg.norm(wperp, axis=2)
        rhs = 2 * np.abs(np.sin(dpsi / 2)) * np.sqrt(np.clip(1 - bet ** 2, 0, None))
        res["E6"] = min(res["E6"], float((lhs - rhs)[local].min()))
        # [C] components
        Lam = Lambda(delta, tau_base, r)
        res["Cmin"] = min(res["Cmin"], float((A - Lam)[local].min()))
        Pb = r * Pfun(delta, dpsi)
        res["Qmin"] = min(res["Qmin"], float((Qn - Pb)[local].min()))
        # [D] final bound by strand index
        pb = pair_bound(delta, dpsi, tau_base, r)
        for kk in range(p):
            mk = local & (k == kk)
            if mk.any():
                gap = (dist / np.maximum(pb, 1e-300))[mk]
                i0 = int(np.argmin(gap))
                if gap[i0] < res["D"][kk]:
                    res["D"][kk] = float(gap[i0])
                    res["Dpair"][kk] = (float(delta[mk][i0]), float((m * np.abs(s_par))[mk][i0]), float(dist[mk][i0]), float(pb[mk][i0]))
                res["loc"][kk] += int(mk.sum())
                res["minDist"][kk] = min(res["minDist"][kk], float(dist[mk].min()))
    log(f"[E] slack (must be >= -tol): E3 {res['E3']:+.3e}  E4 {res['E4']:+.3e}  E5c {res['E5c']:+.3e}  E6+E3 {res['E6']:+.3e}")
    log(f"[C] min(A - Lambda) = {res['Cmin']:+.3e} (>=0 required);  min(|Q| - r P) = {res['Qmin']:+.3e} (>=0 required)")
    for kk in range(p):
        if res["Dpair"][kk]:
            d0, u0, di, pb = res["Dpair"][kk]
            log(f"[D] strand k={kk}: {res['loc'][kk]} local pairs; min dist/bound = {res['D'][kk]:.4f} "
                f"(>=1 required) at delta={d0:.3f}, u={u0:.3f}, dist={di:.4f}, bound={pb:.4f}; min dist (k={kk}) = {res['minDist'][kk]:.4f}")
    # [c1]
    c1, arg = c1_constant(f, eta_min, eta_max, k=1)
    meas_c = meas["dcsd"] / 2 / r
    log(f"[c1] c_1(f={f:.3f}, eta_min={eta_min:.3f}, eta_max={eta_max:.3f}) = {c1:.4f} at (delta,u)={arg}; "
        f"measured dcsd/2/r = {meas_c:.4f}; min(tau-r, c_1 r) = {min(tau_base-r, c1*r):.4f} vs measured tau_d = {meas['tau']:.4f} "
        f"-> ratio tau_d/rho = {meas['tau']/min(tau_base-r, c1*r):.3f}")
    # [K] curvature formula vs finite differences, and bound
    # K_d'' formula at vertices (closed-frame components; psi-rotation handled by using theta and the closed frame
    # with twist rate omega' = -alpha/2pi: U' = (q/p + omega') W - kappa_perp v T, W' = -(q/p+omega') U - kappa_W v T)
    th = theta; bj = base_j
    Tb, Nb, Bb = T[bj], N[bj], B[bj]
    Uv = U; Wv = -np.sin(th)[:, None] * Nb + np.cos(th)[:, None] * Bb
    k1, k2 = bd["k1"][bj], bd["k2"][bj]
    kperp = k1 * np.cos(th) + k2 * np.sin(th)
    kW = -k1 * np.sin(th) + k2 * np.cos(th)
    vv, vp = v[bj], bd["vp"][bj]
    k1p, k2p = bd["k1p"][bj], bd["k2p"][bj]
    # d/dt of closed-frame components: k_c' includes the twist: (k1 cos th + k2 sin th)' = k1' cos + k2' sin + m kW
    # (k1,k2 closed-frame comps differ from parallel ones by rotation omega; k1'cos+k2'sin computed numerically on closed comps
    #  already includes the omega' rotation; the theta' part gives (q/p) kW; total rate m kW) -- we use the identity below
    kperp_p = k1p * np.cos(th) + k2p * np.sin(th) + (q / p) * kW
    Kd1 = (vv * (1 - r * kperp))[:, None] * Tb + (r * m) * Wv
    Kd2 = ((vp * (1 - r * kperp) - r * vv * kperp_p))[:, None] * Tb \
        + (vv ** 2 * (1 - r * kperp))[:, None] * (k1[:, None] * Nb + k2[:, None] * Bb) \
        - (r * m ** 2) * Uv - (r * m * kW * vv)[:, None] * Tb
    kd_formula = np.linalg.norm(np.cross(Kd1, Kd2), axis=1) / np.linalg.norm(Kd1, axis=1) ** 3
    # finite-difference curvature of K_d polygon (circumradius)
    a_, b_, c_ = np.roll(Q, 1, 0), Q, np.roll(Q, -1, 0)
    ab, bc, ca = np.linalg.norm(a_ - b_, axis=1), np.linalg.norm(b_ - c_, axis=1), np.linalg.norm(c_ - a_, axis=1)
    kd_fd = 2 * np.linalg.norm(np.cross(b_ - a_, c_ - a_), axis=1) / (ab * bc * ca)
    rel = np.abs(kd_formula - kd_fd) / kd_fd.max()
    kmax_base = float(bd["kap"].max())
    V1 = float(np.abs(bd["vp"]).max()); K1 = float((np.abs(bd["k1p"]) + np.abs(bd["k2p"])).max())
    num = V1 * (1 + f) + r * vmax * K1 + 2 * r * vmax * m * kmax_base + vmax ** 2 * (1 + f) * kmax_base + r * m ** 2
    den = vmin ** 2 * (1 - f) ** 2 + r ** 2 * m ** 2
    kbar = num / den
    kd_meas = 1 / meas["minRad"]
    log(f"[K] kappa_d formula vs FD: max rel. diff {rel.max():.3e} (should be O(1/M)); max kappa_d FD = {kd_fd.max():.4f}, "
        f"formula {kd_formula.max():.4f}, 1/minRad = {kd_meas:.4f}")
    log(f"[K] base derivative data: |v'|max={V1:.4f}, (|k1'|+|k2'|)max={K1:.4f}, kappa_max={kmax_base:.4f}; "
        f"bound kappa_d <= {kbar:.4f} (= 1/{1/kbar:.4f});  r*kbar = {r*kbar:.4f}  -> 1/kbar >= rho? {1/kbar >= min(tau_base-r, 0.5*r)}")
    # [c0] same strand, conditional on kbar
    Vd = vmax * (1 + f) + r * m
    s0 = np.pi / (kbar * Vd)
    c0, arg0 = c1_constant(f, eta_min, eta_max, k=0, u_lo=m * s0)
    log(f"[c0] same-strand (conditional on kappa_d <= {kbar:.3f}): s_0 = pi/(kbar V_d) = {s0:.4f}, u >= {m*s0:.4f}; "
        f"c_0 = {c0:.4f} at (delta,u)={arg0}")
    log(f"    time {time.time()-t0:.1f}s")
    return dict(label=label, f=f, m=m, eta_min=eta_min, eta_max=eta_max, c1=c1, c0=c0, kbar=kbar,
                meas_c=meas_c, tau=meas["tau"], r=r, tau_base=tau_base, minRad=meas["minRad"],
                lemmaA_ratio=wr, Dmin=res["D"], Cmin=res["Cmin"], Qmin=res["Qmin"])

def run_chain(N0, f, pq, depth, label):
    P = circle(N0)
    m0 = measure(P)
    tau_prev = m0["tau"]
    out = []
    for d in range(1, depth + 1):
        p, q = pq
        T, Nn, B, alpha = bishop_frame(P)
        r = f * tau_prev
        Q = offset(P, Nn, B, r, p, q, 0.0)
        meas = measure(Q)
        out.append(check_level(P, tau_prev, r, p, q, Q, meas, f"{label} d={d}"))
        P, tau_prev = Q, meas["tau"]
    return out

def main():
    t0 = time.time()
    log("check_Hc.py -- numerical checks of theory/Hc_derivation.md on the RTK001 family (p = 2)")
    summary = []
    summary += run_chain(256, 0.25, (2, 3), 3, "(2,3) f=0.25 N0=256")
    summary += run_chain(256, 0.35, (2, 3), 3, "(2,3) f=0.35 N0=256")
    summary += run_chain(256, 0.50, (2, 3), 3, "(2,3) f=0.50 N0=256")
    summary += run_chain(512, 0.50, (2, 3), 2, "(2,3) f=0.50 N0=512")
    summary += run_chain(256, 0.50, (2, 5), 3, "(2,5) f=0.50 N0=256")
    # table of c_1 for the depth-1 situation (constant speed, alpha = 0): eta = h/r = (1/f)(p/q)
    log("\n=== c_1 table, depth 1 (v = 1, alpha = 0, eta_min = eta_max = (1/f)(p/q)) ===")
    for (p, q) in [(2, 3), (2, 5), (2, 7)]:
        for f in [0.25, 0.35, 0.5]:
            eta = (1 / f) * (p / q)
            c1, arg = c1_constant(f, eta, eta, k=1, ngrid=800)
            log(f"  (p,q)=({p},{q}) f={f}: eta={eta:.3f}  c_1={c1:.4f}  at (delta,u)={tuple(round(x,3) for x in arg)}")
    log("\n=== c_1 as a function of eta (f = 1/2, eta_min = eta_max = eta) ===")
    for eta in [0.5, 0.75, 1.0, 1.25, 1.333, 1.5, 2.0, 3.0, 5.0, 10.0]:
        c1, arg = c1_constant(0.5, eta, eta, k=1, ngrid=600)
        log(f"  eta={eta:5.3f}: c_1={c1:.4f} at (delta,u)={tuple(round(x,3) for x in arg)}")
    log("\n=== SUMMARY ===")
    log("level | f | m | eta_min | eta_max | c_1 (proved, k=1) | measured dcsd/2/r | tau_d/min(tau-r,c_1 r) | min dist/bound k=1 | k=0 | kbar*r (cond.) | c_0 (cond.)")
    for s in summary:
        log(f"{s['label']} | {s['f']:.3f} | {s['m']:.3f} | {s['eta_min']:.3f} | {s['eta_max']:.3f} | {s['c1']:.4f} | {s['meas_c']:.4f} | "
            f"{s['tau']/min(s['tau_base']-s['r'], s['c1']*s['r']):.3f} | {s['Dmin'][1]:.4f} | {s['Dmin'][0]:.4f} | {s['kbar']*s['r']:.3f} | {s['c0']:.4f}")
    log(f"\ntotal time {time.time()-t0:.1f}s")
    with open(os.path.join(HERE, "check_Hc_output.txt"), "w") as fh:
        fh.write("\n".join(OUT) + "\n")
    with open(os.path.join(HERE, "check_Hc_summary.json"), "w") as fh:
        json.dump(summary, fh, indent=1, default=float)

if __name__ == "__main__":
    main()
