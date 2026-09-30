#!/usr/bin/env python3
"""RTK001 -- Geometry of recursive knots: iterated cables by frame offsets.

Builds K_0 (circle), K_1, K_2, K_3 as polygons, where K_d is the (p_d, q_d)
pattern placed on the tube of radius r_d around K_{d-1} using a closed
rotation-minimising (Bishop) frame, and measures for each polygon:

  L        polygon length
  minRad   min circumradius of consecutive vertex triples
  dcsd     min distance between doubly-critical vertex pairs
  tau      polygonal thickness proxy  min(minRad, dcsd/2)
  tau_pt   min point-tangent global radius of curvature (Gonzalez-Maddocks)
  Rop      L / tau   (numerical ropelength of the explicit polygon)
  Wr       Gauss writhe (discrete double sum), holonomy alpha of the Bishop frame

All numbers in the manuscript come from results/results.json written here.
Deterministic (no randomness); the seed is recorded only for bookkeeping.
"""
import json
import os
import platform
import sys
import time

import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
RES = os.path.join(ROOT, "results")
FIG = os.path.join(ROOT, "figures")
os.makedirs(RES, exist_ok=True)
os.makedirs(FIG, exist_ok=True)

SEED = 20260930
np.random.seed(SEED)
FAST = "--fast" in sys.argv


# ----------------------------------------------------------------------------
# geometry helpers
# ----------------------------------------------------------------------------
def unit(v):
    return v / np.linalg.norm(v, axis=-1, keepdims=True)


def circle(N, R=1.0):
    t = 2 * np.pi * np.arange(N) / N
    return np.stack([R * np.cos(t), R * np.sin(t), np.zeros(N)], axis=1)


def tangents(P):
    """Central-difference unit tangents of a closed polygon."""
    return unit(np.roll(P, -1, axis=0) - np.roll(P, 1, axis=0))


def rotate(v, axis, ang):
    """Rodrigues rotation of vector v about unit axis by angle ang."""
    return (v * np.cos(ang) + np.cross(axis, v) * np.sin(ang)
            + axis * np.dot(axis, v) * (1 - np.cos(ang)))


def bishop_frame(P):
    """Closed Bishop frame (N, B) along the closed polygon P.

    Parallel transport of the normal from vertex to vertex (rotation taking
    T_i to T_{i+1}); the holonomy alpha in (-pi, pi] after one loop is removed
    by a linear twist so that the frame is periodic.  Returns T, N, B, alpha.
    """
    T = tangents(P)
    n = len(P)
    N = np.zeros_like(P)
    # initial normal: any unit vector orthogonal to T_0
    a = np.array([0.0, 0.0, 1.0])
    if abs(np.dot(a, T[0])) > 0.9:
        a = np.array([1.0, 0.0, 0.0])
    N[0] = unit(a - np.dot(a, T[0]) * T[0])
    for i in range(1, n + 1):
        j = i % n
        prev = N[i - 1]
        ax = np.cross(T[i - 1], T[j])
        s = np.linalg.norm(ax)
        c = np.dot(T[i - 1], T[j])
        if s < 1e-14:
            nn = prev.copy()
        else:
            nn = rotate(prev, ax / s, np.arctan2(s, c))
        nn = unit(nn - np.dot(nn, T[j]) * T[j])
        if i < n:
            N[i] = nn
        else:
            N_end = nn  # transported N_0 after a full loop
    # holonomy: signed angle from N_end to N[0] in the plane orthogonal to T_0
    B0 = np.cross(T[0], N[0])
    alpha = np.arctan2(np.dot(N_end, B0), np.dot(N_end, N[0]))  # N_end = R(alpha) N_0
    # closing twist: rotate N_i by -alpha * i / n about T_i
    for i in range(n):
        N[i] = rotate(N[i], T[i], -alpha * i / n)
    B = np.cross(T, N)
    return T, N, B, alpha


def offset(P, N, B, r, p, q, phi=0.0):
    """K_d vertices: p copies of the base parameter with pattern angle q t/p."""
    M = len(P)
    j = np.arange(p * M)
    i = j % M
    theta = q * (2 * np.pi * j / M) / p + phi
    return P[i] + r * (np.cos(theta)[:, None] * N[i] + np.sin(theta)[:, None] * B[i])


# ----------------------------------------------------------------------------
# measurements
# ----------------------------------------------------------------------------
def length(P):
    return float(np.linalg.norm(np.roll(P, -1, axis=0) - P, axis=1).sum())


def min_rad(P):
    """Min circumradius over consecutive vertex triples."""
    a, b, c = np.roll(P, 1, axis=0), P, np.roll(P, -1, axis=0)
    ab, bc, ca = np.linalg.norm(a - b, axis=1), np.linalg.norm(b - c, axis=1), np.linalg.norm(c - a, axis=1)
    area2 = np.linalg.norm(np.cross(b - a, c - a), axis=1)  # = 2*area
    with np.errstate(divide="ignore"):
        R = ab * bc * ca / (2 * area2)
    R[area2 < 1e-300] = np.inf
    return float(R.min())


def pair_scan(P, T, chunk=None):
    """Return (dcsd, tau_pt, writhe) from an O(N^2) scan in row chunks.

    dcsd   : min distance over doubly-critical vertex pairs (i != j), i.e. pairs
             where D[i,j] is a local minimum along both indices (D[i,i]=0 is
             included in the neighbourhood test, which excludes near-diagonal pairs).
    tau_pt : min over i != j of |x_j - x_i|^2 / (2 |T_i x (x_j - x_i)|).
    writhe : (1/4pi) sum_{i != j} (e_i x e_j).(m_i - m_j)/|m_i - m_j|^3 over segments.
    """
    n = len(P)
    if chunk is None:
        chunk = int(max(64, min(1024, 3e6 // n)))
    E = np.roll(P, -1, axis=0) - P
    Mid = P + 0.5 * E
    dcsd = np.inf
    tau_pt = np.inf
    wr = 0.0
    for a in range(0, n, chunk):
        b = min(n, a + chunk)
        rows = np.arange(a - 1, b + 1) % n  # one guard row each side
        diff = P[rows][:, None, :] - P[None, :, :]        # (k+2, n, 3)
        D = np.linalg.norm(diff, axis=2)
        Dm = D[1:-1]                                          # interior rows
        left = D[:-2]
        right = D[2:]
        up = np.roll(Dm, 1, axis=1)
        down = np.roll(Dm, -1, axis=1)
        crit = (Dm <= left) & (Dm <= right) & (Dm <= up) & (Dm <= down)
        ii = np.arange(a, b)
        crit[np.arange(b - a), ii] = False                    # exclude i == j
        if crit.any():
            dcsd = min(dcsd, float(Dm[crit].min()))
        # point-tangent radius
        d_int = -diff[1:-1]                                   # x_j - x_i
        cr = np.linalg.norm(np.cross(T[ii][:, None, :], d_int), axis=2)
        with np.errstate(divide="ignore", invalid="ignore"):
            rho = Dm ** 2 / (2 * cr)
        rho[np.arange(b - a), ii] = np.inf
        rho[~np.isfinite(rho)] = np.inf
        tau_pt = min(tau_pt, float(rho.min()))
        # writhe (segments)
        dm = Mid[ii][:, None, :] - Mid[None, :, :]
        dist = np.linalg.norm(dm, axis=2)
        cross = np.cross(E[ii][:, None, :], E[None, :, :])
        num = np.einsum("ijk,ijk->ij", cross, dm)
        with np.errstate(divide="ignore", invalid="ignore"):
            contrib = num / dist ** 3
        contrib[np.arange(b - a), ii] = 0.0
        contrib[~np.isfinite(contrib)] = 0.0
        wr += float(contrib.sum())
    return dcsd, tau_pt, wr / (4 * np.pi)


def measure(P):
    T = tangents(P)
    L = length(P)
    mr = min_rad(P)
    dcsd, tau_pt, wr = pair_scan(P, T)
    tau = min(mr, dcsd / 2)
    return dict(N=int(len(P)), L=L, minRad=mr, dcsd=dcsd, tau=tau, tau_pt=tau_pt,
                Rop=L / tau, Rop_pt=L / tau_pt, writhe=wr)


# ----------------------------------------------------------------------------
# chains
# ----------------------------------------------------------------------------
def build_chain(N0, f, pq, depth, phi=0.0):
    """Iterated cable with r_d = f * tau_{d-1} (polygonal tau of the previous level)."""
    P = circle(N0)
    out = []
    m0 = measure(P)
    m0.update(d=0, r=None, p=None, q=None, alpha=None)
    out.append(m0)
    tau_prev = m0["tau"]
    for d in range(1, depth + 1):
        p, q = pq[(d - 1) % len(pq)]
        T, Nn, B, alpha = bishop_frame(P)
        r = f * tau_prev
        Q = offset(P, Nn, B, r, p, q, phi)
        m = measure(Q)
        # meridian chord between adjacent strands; hypothesis (H_c): thick >= min(tau_prev - r, c r sin(pi/p))
        Lprev = out[-1]["L"]
        s = 2 * r * np.sin(np.pi / p)
        rho_half = min(tau_prev - r, 0.5 * r * np.sin(np.pi / p))   # c = 1/2 (used in the text)
        rho_one = min(tau_prev - r, 1.0 * r * np.sin(np.pi / p))    # c = 1 (sharp on a straight tube, p = 2)
        n_frame = int(np.rint(out[-1]["writhe"]))  # linking number of the closed Bishop frame
        m.update(d=d, r=r, p=p, q=q, f=f, alpha=float(alpha),
                 strand_sep=float(s), rho_pred=float(rho_half), rho_pred_cone=float(rho_one),
                 ratio_tau_r=float(m["tau"] / r),
                 L_bound=float(p * Lprev * (1 + r / tau_prev) + r * (2 * np.pi * q + p * abs(alpha))),
                 Lk_frame=n_frame, cable_slope=int(q + p * n_frame))
        out.append(m)
        P, tau_prev = Q, m["tau"]
    return out


def main():
    t0 = time.time()
    N0s = [256, 512] if FAST else [512, 1024]
    depth = 3
    fs = [0.25, 0.35, 0.5, 0.6]
    configs = [("(2,3)", [(2, 3)], f) for f in fs]
    configs += [("(3,2)", [(3, 2)], 0.5), ("(2,5)", [(2, 5)], 0.5)]
    chains = []
    for name, pq, f in configs:
        for N0 in ([n // 2 for n in N0s] if name == "(3,2)" else N0s):
            tc = time.time()
            ch = build_chain(N0, f, pq, depth)
            chains.append(dict(pattern=name, pq=pq, f=f, N0=N0, levels=ch,
                               seconds=time.time() - tc))
            top = ch[-1]
            print(f"{name} f={f} N0={N0}: " + " | ".join(
                f"d{m['d']}: N={m['N']} L={m['L']:.3f} tau={m['tau']:.4f} Rop={m['Rop']:.1f}"
                for m in ch) + f"  ({time.time()-tc:.1f}s)", flush=True)

    # theoretical constant Lambda = A/gamma for the default family, c = 1/2
    theory = {}
    for f in fs:
        p, q = 2, 3
        gamma = min(1 - f, 0.5 * f * np.sin(np.pi / p))
        A = p * (1 + f) + f * (q + p / 2)
        theory[str(f)] = dict(gamma=float(gamma), A=float(A), Lambda=float(A / gamma),
                              bounds=[float(2 * np.pi * (A / gamma) ** d) for d in range(depth + 1)])

    meta = dict(seed=SEED, python=platform.python_version(), numpy=np.__version__,
                seconds=time.time() - t0, fast=FAST, N0s=N0s, depth=depth, fs=fs)
    res = dict(meta=meta, chains=chains, theory=theory)
    with open(os.path.join(RES, "results.json"), "w") as fh:
        json.dump(res, fh, indent=1)

    # markdown tables
    lines = ["# RTK001 results (polygonal measurements)", "",
             f"seed {SEED}; total {meta['seconds']:.0f} s; N0 in {N0s}", "",
             "| pattern | f | N0 | d | N | r_d | L | minRad | dcsd/2 | tau | tau_pt | Rop | Rop_pt | Wr | alpha | rho_pred | tau/r | L_bound | Lk_frame | slope |",
             "|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|"]
    for ch in chains:
        for m in ch["levels"]:
            rr = "-" if m["r"] is None else f"{m['r']:.4f}"
            al = "-" if m["alpha"] is None else f"{m['alpha']:.3f}"
            rp = "-" if "rho_pred" not in m else f"{m['rho_pred']:.4f}"
            lb = "-" if "L_bound" not in m else f"{m['L_bound']:.2f}"
            tr = "-" if "ratio_tau_r" not in m else f"{m['ratio_tau_r']:.3f}"
            lk = "-" if "Lk_frame" not in m else f"{m['Lk_frame']}"
            sl = "-" if "cable_slope" not in m else f"{m['cable_slope']}"
            lines.append(f"| {ch['pattern']} | {ch['f']} | {ch['N0']} | {m['d']} | {m['N']} | {rr} | {m['L']:.4f} | "
                         f"{m['minRad']:.4f} | {m['dcsd']/2:.4f} | {m['tau']:.4f} | {m['tau_pt']:.4f} | "
                         f"{m['Rop']:.2f} | {m['Rop_pt']:.2f} | {m['writhe']:.3f} | {al} | {rp} | {tr} | {lb} | {lk} | {sl} |")
    lines += ["", "## Theory constants (default (2,3), c = 1/2)", "",
              "| f | gamma | A | Lambda | 2pi Lambda^d, d=1..3 |", "|---|---|---|---|---|"]
    for f in fs:
        th = theory[str(f)]
        lines.append(f"| {f} | {th['gamma']:.4f} | {th['A']:.4f} | {th['Lambda']:.4f} | "
                     + ", ".join(f"{b:.1f}" for b in th["bounds"][1:]) + " |")
    with open(os.path.join(RES, "tables.md"), "w") as fh:
        fh.write("\n".join(lines) + "\n")

    # figures
    try:
        import matplotlib
        matplotlib.use("Agg")
        import matplotlib.pyplot as plt
        # Fig 1: projections of K_1, K_2, K_3 (default, f=0.5, finest N0)
        ch = [c for c in chains if c["pattern"] == "(2,3)" and c["f"] == 0.5 and c["N0"] == N0s[-1]][0]
        P = circle(ch["N0"])
        curves = [P]
        tau_prev = 1.0
        for d in range(1, depth + 1):
            T, Nn, B, alpha = bishop_frame(P)
            r = 0.5 * tau_prev
            P = offset(P, Nn, B, r, 2, 3)
            curves.append(P)
            tau_prev = ch["levels"][d]["tau"]
        fig, axes = plt.subplots(1, 3, figsize=(11, 3.8))
        for ax, d in zip(axes, [1, 2, 3]):
            Q = curves[d]
            ax.plot(Q[:, 0], Q[:, 1], lw=0.6, color="#1f4e79")
            ax.set_aspect("equal")
            ax.set_title(f"$K_{d}$ (projection to $xy$), $N={len(Q)}$")
            ax.set_xticks([])
            ax.set_yticks([])
        fig.tight_layout()
        fig.savefig(os.path.join(FIG, "fig_curves.png"), dpi=160)
        fig.savefig(os.path.join(FIG, "fig_curves.pdf"))
        plt.close(fig)
        # Fig 2: Rop_d vs d for the f grid, with the theoretical bound
        fig, ax = plt.subplots(figsize=(5.2, 3.8))
        cols = ["#1f4e79", "#c0504d", "#4f7f2f", "#7f5f9f"]
        for k, f in enumerate(fs):
            c = [c for c in chains if c["pattern"] == "(2,3)" and c["f"] == f and c["N0"] == N0s[-1]][0]
            ds = [m["d"] for m in c["levels"]]
            ax.plot(ds, [m["Rop"] for m in c["levels"]], "o-", color=cols[k], label=f"measured, $f={f}$")
            if f <= 0.5:
                ax.plot(ds, theory[str(f)]["bounds"], "--", color=cols[k], alpha=0.6,
                        label=f"bound $2\\pi\\Lambda^d$, $f={f}$")
        ax.set_yscale("log")
        ax.set_xlabel("depth $d$")
        ax.set_ylabel("$L/\\tau$ (polygonal)")
        ax.set_xticks([0, 1, 2, 3])
        ax.legend(fontsize=7)
        fig.tight_layout()
        fig.savefig(os.path.join(FIG, "fig_rop.png"), dpi=160)
        fig.savefig(os.path.join(FIG, "fig_rop.pdf"))
        plt.close(fig)
    except Exception as e:  # figures are not load-bearing
        print("figure error:", e)
    print(f"done in {time.time()-t0:.1f}s")


if __name__ == "__main__":
    main()
