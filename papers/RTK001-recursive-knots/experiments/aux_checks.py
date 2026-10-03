#!/usr/bin/env python3
"""RTK001 -- auxiliary checks added after internal review round 1 (30/09/2026).

 (i)   geometry of the doubly critical vertex pair that realises dcsd at depth 1
       (base-point separation in degrees, base distance, same normal disc or not);
 (ii)  the offset radius r* at which Wr(K_1; r) for the (2,3) pattern crosses 3.5 (bisection);
 (iii) segment-segment minimal distance versus the vertex-pair dcsd (proxy check), both near
       the critical pair and globally over pairs with cyclic index separation > N/10.
Writes results/aux_checks.json.  Deterministic, no randomness.
"""
import json
import os
import sys
import time

import numpy as np

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import recursive_knots as rk  # noqa: E402

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
RES = os.path.join(ROOT, "results")


def argmin_dcsd(P):
    """Brute-force doubly critical vertex pair realising dcsd (same local-minimum test as pair_scan)."""
    D = np.linalg.norm(P[:, None, :] - P[None, :, :], axis=2)
    crit = ((D <= np.roll(D, 1, 0)) & (D <= np.roll(D, -1, 0))
            & (D <= np.roll(D, 1, 1)) & (D <= np.roll(D, -1, 1)))
    np.fill_diagonal(crit, False)
    idx = np.argwhere(crit)
    k = int(np.argmin(D[crit]))
    i, j = idx[k]
    return float(D[i, j]), int(i), int(j)


def seg_seg_dist(P1, D1, Q1, D2):
    """Closest distance between segments P1+s*D1 and Q1+t*D2 (s,t in [0,1]); broadcasting shapes (...,3)."""
    r = P1 - Q1
    a = np.einsum("...k,...k->...", D1, D1)
    e = np.einsum("...k,...k->...", D2, D2)
    f = np.einsum("...k,...k->...", D2, r)
    c = np.einsum("...k,...k->...", D1, r)
    b = np.einsum("...k,...k->...", D1, D2)
    denom = a * e - b * b
    with np.errstate(divide="ignore", invalid="ignore"):
        s = np.where(denom > 1e-18, np.clip((b * f - c * e) / denom, 0.0, 1.0), 0.0)
        t = (b * s + f) / e
        s = np.where(t < 0, np.clip(-c / a, 0.0, 1.0), s)
        s = np.where(t > 1, np.clip((b - c) / a, 0.0, 1.0), s)
    t = np.clip(t, 0.0, 1.0)
    diff = P1 + s[..., None] * D1 - (Q1 + t[..., None] * D2)
    return np.linalg.norm(diff, axis=-1)


def seg_min_global(P, gap):
    """Min segment-segment distance over pairs of edges with cyclic index separation > gap."""
    n = len(P)
    E = np.roll(P, -1, axis=0) - P
    best = np.inf
    idx = np.arange(n)
    chunk = max(8, int(2e5 // n))
    for a in range(0, n, chunk):
        rows = np.arange(a, min(n, a + chunk))
        sep = np.abs(rows[:, None] - idx[None, :])
        sep = np.minimum(sep, n - sep)
        d = seg_seg_dist(P[rows][:, None, :], E[rows][:, None, :], P[None, :, :], E[None, :, :])
        d[sep <= gap] = np.inf
        best = min(best, float(d.min()))
    return best


def seg_min_local(P, i, j, w=3):
    """Min segment-segment distance among edges within w of i and of j."""
    n = len(P)
    E = np.roll(P, -1, axis=0) - P
    I = (i + np.arange(-w, w + 1)) % n
    J = (j + np.arange(-w, w + 1)) % n
    d = seg_seg_dist(P[I][:, None, :], E[I][:, None, :], P[J][None, :, :], E[J][None, :, :])
    return float(d.min())


def build_K1(N0, f, p, q):
    P = rk.circle(N0)
    T, N, B, al = rk.bishop_frame(P)
    return P, rk.offset(P, N, B, f, p, q)   # tau_0 = 1, so r_1 = f


def main():
    t0 = time.time()
    out = {"meta": {"seed": rk.SEED, "note": "deterministic auxiliary checks (review round 1)"}}

    # (i) critical pair at depth 1
    crit = []
    for (pat, p, q, N0, fs) in [("(2,3)", 2, 3, 1024, [0.25, 0.35, 0.5, 0.6]),
                                ("(3,2)", 3, 2, 512, [0.5]), ("(2,5)", 2, 5, 1024, [0.5])]:
        for f in fs:
            P, Q = build_K1(N0, f, p, q)
            dc, i, j = argmin_dcsd(Q)
            bi, bj = i % N0, j % N0
            ang = abs(((bi - bj) * 2 * np.pi / N0 + np.pi) % (2 * np.pi) - np.pi)
            rad = lambda x: float(np.hypot(x[0], x[1]))
            crit.append(dict(pattern=pat, f=f, N0=N0, N=len(Q), r=f, dcsd=dc, tau=dc / 2, ratio_tau_r=dc / (2 * f),
                             pair=[i, j], base_idx=[int(bi), int(bj)], same_disc=bool(bi == bj),
                             base_sep_deg=float(np.degrees(ang)), base_dist=float(np.linalg.norm(P[bi] - P[bj])),
                             cyl_radius=[rad(Q[i]), rad(Q[j])], z=[float(Q[i][2]), float(Q[j][2])],
                             inner_pitch_over_r=float((1 - f) * p / q / f),
                             seg_local_over_vertex=seg_min_local(Q, i, j) / dc))
            print(f"[crit] {pat} f={f}: dcsd={dc:.4f} tau/r={dc/(2*f):.4f} base sep={np.degrees(ang):.1f} deg "
                  f"same_disc={bi==bj} base_dist={np.linalg.norm(P[bi]-P[bj]):.3f} seg/vertex={crit[-1]['seg_local_over_vertex']:.6f}",
                  flush=True)
    out["critical_pairs_d1"] = crit

    # (ii) writhe crossing of 3.5 for (2,3), K_1, by bisection in r
    def wr_K1(N0, r):
        P, Q = build_K1(N0, r, 2, 3)
        return rk.pair_scan(Q, rk.tangents(Q))[2]
    cross = []
    for N0 in [512, 1024]:
        lo, hi = 0.45, 0.50
        wlo, whi = wr_K1(N0, lo), wr_K1(N0, hi)
        assert wlo < 3.5 < whi
        for _ in range(18):
            mid = 0.5 * (lo + hi)
            if wr_K1(N0, mid) < 3.5:
                lo = mid
            else:
                hi = mid
        cross.append(dict(N0=N0, r_star=0.5 * (lo + hi), bracket=[lo, hi], Wr_at_0p45=wlo, Wr_at_0p5=whi))
        print(f"[wr] N0={N0}: r* = {0.5*(lo+hi):.5f}  (Wr(0.45)={wlo:.4f}, Wr(0.5)={whi:.4f})", flush=True)
    out["writhe_crossing"] = cross

    # (iii) segment-segment versus vertex dcsd, (2,3) chain f = 0.5 at N0 = 512 (d = 1, 2) and f = 0.25 (d = 1)
    seg = []
    for f, depth in [(0.5, 2), (0.25, 1)]:
        N0 = 512
        P = rk.circle(N0)
        tau_prev = 1.0
        for d in range(1, depth + 1):
            T, N, B, al = rk.bishop_frame(P)
            Q = rk.offset(P, N, B, f * tau_prev, 2, 3)
            dc, i, j = argmin_dcsd(Q)
            n = len(Q)
            gap = n // 10
            sg = seg_min_global(Q, gap)
            seg.append(dict(f=f, d=d, N=n, gap=gap, dcsd_vertex=dc, seg_global=sg, ratio_global=sg / dc,
                            ratio_local=seg_min_local(Q, i, j) / dc, edge=float(rk.length(Q) / n)))
            print(f"[seg] f={f} d={d} N={n}: dcsd={dc:.6f} seg(global, gap>{gap})={sg:.6f} ratio={sg/dc:.6f} "
                  f"local ratio={seg[-1]['ratio_local']:.6f}", flush=True)
            P, tau_prev = Q, dc / 2
    out["segment_check"] = seg
    out["meta"]["seconds"] = time.time() - t0
    with open(os.path.join(RES, "aux_checks.json"), "w") as fh:
        json.dump(out, fh, indent=1)
    print(f"done in {time.time()-t0:.1f}s")


if __name__ == "__main__":
    main()
