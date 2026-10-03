#!/usr/bin/env python3
"""Classification of the doubly critical pairs of K_1, K_2, K_3 for the default (2,3) chains (review round 2, M2/M3).

Independent of theory/: only the polygon construction of recursive_knots.py is reused.

For every level d of the chains (2,3), f in {0.25, 0.35, 0.5}, N0 in {256, 512}:
  * vertex DC pairs: (i, j) with |X_i - X_j| a local minimum in i and in j (the definition of Section 2.4 of the
    manuscript; the diagonal D_ii = 0 is kept in the neighbourhood test);
  * sign-change cells: 2x2 cells of the index grid in which both g1 = (X_j - X_i).T_i and g2 = (X_j - X_i).T_j
    change sign (a necessary condition for a doubly critical pair inside the cell; also catches saddles and maxima
    of the distance, which the local-minimum test cannot see); cells within 2 steps of the diagonal are ignored;
  * classes (rule of the manuscript): "disc" = same base vertex; otherwise sigma = shorter base arc (arclength of the
    base polygon), delta = sigma / tau_base, s = signed base index difference along that arc,
    k = rint((j - i - s) / M) mod 2 (strand index relative to that arc); "far" if delta >= pi, else "k0" / "k1".
  * margin of Conjecture 3.16: smallest vertex-DC distance over pairs that are not "disc", divided by 2 r_d.
Output: results/classify_pairs.json, results/classify_pairs.md.  Deterministic; about 1 CPU minute.
"""
import json
import os
import sys
import time

import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
sys.path.insert(0, HERE)
sys.argv = [sys.argv[0]]
from recursive_knots import bishop_frame, circle, measure, offset, tangents  # noqa: E402

BLOCK = 512


def dist_matrix(Q):
    G = Q @ Q.T
    n2 = np.einsum("ij,ij->i", Q, Q)
    D2 = np.clip(n2[:, None] + n2[None, :] - 2 * G, 0, None)
    return np.sqrt(D2)


def vertex_dc(D):
    lm = np.ones_like(D, dtype=bool)
    for ax in (0, 1):
        for sh in (1, -1):
            lm &= D <= np.roll(D, sh, axis=ax)
    np.fill_diagonal(lm, False)
    return lm


def cell_dc(Q, T):
    """Cells (i, j) -- spanning i, i+1 and j, j+1 -- where g1 and g2 both change sign."""
    n = len(Q)
    out = np.zeros((n, n), dtype=bool)
    QT = np.einsum("ij,ij->i", Q, T)
    for a in range(0, n, BLOCK):
        ia = np.arange(a, min(a + BLOCK, n))
        ib = (ia + 1) % n
        rows = []
        for ii in (ia, ib):
            # g1[i, j] = (X_j - X_i).T_i ; g2[i, j] = (X_j - X_i).T_j
            g1 = T[ii] @ Q.T - QT[ii][:, None]
            g2 = QT[None, :] - Q[ii] @ T.T
            rows.append((g1, g2))
        def changes(k):
            c = [rows[0][k], np.roll(rows[0][k], -1, 1), rows[1][k], np.roll(rows[1][k], -1, 1)]
            return (np.maximum.reduce(c) > 0) & (np.minimum.reduce(c) < 0)
        out[ia] = changes(0) & changes(1)
    I = np.arange(n)
    gap = np.minimum((I[None, :] - I[:, None]) % n, (I[:, None] - I[None, :]) % n)
    out &= gap > 2
    return out


def classify(P, tau_b, n, I, J):
    M = len(P)
    seg = np.linalg.norm(np.roll(P, -1, 0) - P, axis=1)
    S = np.concatenate([[0.0], np.cumsum(seg)])[:-1]
    L = seg.sum()
    bi, bj = I % M, J % M
    fwd = (bj - bi) % M
    sf = (S[bj] - S[bi]) % L
    use_f = sf <= L - sf
    sigma = np.where(use_f, sf, L - sf)
    s = np.where(use_f, fwd, fwd - M)
    k = np.rint((((J - I) % n) - s) / M).astype(int) % 2
    delta = sigma / tau_b
    cls = np.where(bi == bj, "disc", np.where(delta >= np.pi, "far", np.where(k == 0, "k0", "k1")))
    chord = np.linalg.norm(P[bi] - P[bj], axis=1)
    return cls, delta, chord


def level_census(P, tau_b, r, Q):
    n = len(Q)
    D = dist_matrix(Q)
    T = tangents(Q)
    res = {}
    for name, mask in (("vertex", vertex_dc(D)), ("cell", cell_dc(Q, T))):
        I, J = np.nonzero(np.triu(mask, 1) | np.tril(mask, -1).T)
        cls, delta, chord = classify(P, tau_b, n, I, J)
        dist = D[I, J]
        entry = {}
        for c in ("disc", "far", "k1", "k0"):
            sel = cls == c
            if sel.any():
                j0 = int(np.argmin(dist[sel]))
                entry[c] = dict(n=int(sel.sum()), min_dist_over_2r=float(dist[sel].min() / (2 * r)),
                                min_delta=float(delta[sel].min()), delta_at_min=float(delta[sel][j0]),
                                base_chord_over_tau_at_min=float(chord[sel][j0] / tau_b))
            else:
                entry[c] = dict(n=0)
        nd = cls != "disc"
        entry["next_over_2r"] = float(dist[nd].min() / (2 * r)) if nd.any() else None
        entry["next_class"] = str(cls[nd][int(np.argmin(dist[nd]))]) if nd.any() else None
        res[name] = entry
    return res


def run(N0, f, depth=3):
    P = circle(N0)
    tau_b = measure(P)["tau"]
    out = []
    for d in range(1, depth + 1):
        _, Nn, B, _ = bishop_frame(P)
        r = f * tau_b
        Q = offset(P, Nn, B, r, 2, 3, 0.0)
        m = measure(Q)
        cen = level_census(P, tau_b, r, Q)
        out.append(dict(N0=N0, f=f, d=d, N=len(Q), r=r, tau_base=tau_b, tau=m["tau"], tau_over_r=m["tau"] / r, **cen))
        P, tau_b = Q, m["tau"]
    return out


def main():
    t0 = time.time()
    levels = []
    for N0 in (256, 512):
        for f in (0.25, 0.35, 0.5):
            levels += run(N0, f)
    cpu = time.process_time()
    meta = dict(seconds_wall=time.time() - t0, seconds_cpu=cpu, python=sys.version.split()[0], numpy=np.__version__)
    with open(os.path.join(ROOT, "results", "classify_pairs.json"), "w") as fh:
        json.dump(dict(meta=meta, levels=levels), fh, indent=1)
    lines = ["# RTK001 classification of doubly critical pairs, (2,3) chains (experiments/classify_pairs.py)", "",
             "Classes: disc = same base vertex; far = shorter base arc >= pi tau; k1 / k0 = different / same strand "
             "relative to the shorter base arc, arc < pi tau. Entries: count, min distance / 2r_d, min delta.", "",
             "| N0 | f | d | tau/r | test | disc | far | k1 | k0 | next non-disc / 2r (class) |",
             "|---|---|---|---|---|---|---|---|---|---|"]
    def cell(e):
        return "0" if e["n"] == 0 else f"{e['n']}; {e['min_dist_over_2r']:.4f}; {e['min_delta']:.3f}"
    for lv in levels:
        for t in ("vertex", "cell"):
            e = lv[t]
            nxt = "--" if e["next_over_2r"] is None else f"{e['next_over_2r']:.4f} ({e['next_class']})"
            lines.append(f"| {lv['N0']} | {lv['f']} | {lv['d']} | {lv['tau_over_r']:.4f} | {t} | {cell(e['disc'])} | "
                         f"{cell(e['far'])} | {cell(e['k1'])} | {cell(e['k0'])} | {nxt} |")
    lines.append("")
    lines.append(f"wall {meta['seconds_wall']:.1f} s, CPU {meta['seconds_cpu']:.1f} s")
    with open(os.path.join(ROOT, "results", "classify_pairs.md"), "w") as fh:
        fh.write("\n".join(lines) + "\n")
    print("\n".join(lines))


if __name__ == "__main__":
    main()
