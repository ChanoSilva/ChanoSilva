#!/usr/bin/env python3
"""Joint sweep of the two frame normalisations that affect K_3 (Conjecture conj, review round 3).

Rotating the initial normal of the Bishop frame of K_{d-1} by beta is the same as phi_d -> phi_d + beta, and
phi_d + pi gives the same curve (p = 2, q odd); the normalisation of the frame of K_0 only moves K_1 by a congruence.
So the d = 3 margin of Conjecture conj is a function of (beta_1, beta_2) in [0, pi)^2, where beta_1 = phi_2 (frame of
K_1) and beta_2 = phi_3 (frame of K_2).  experiments/phase_margin.py scanned beta_2 with beta_1 = 0 only.

Margin (identical to phase_margin.py / classify_pairs.py, vertex census): smallest distance over doubly critical
vertex pairs of K_3 that are NOT antipodal pairs of one normal disc of K_2, divided by 2 r_3, minus 1, in percent.
A negative margin would mean tau(K_3) < r_3 for that normalisation.

Protocol (fixed before running): default chain (2,3), f = 1/2, r_d = f tau(K_{d-1}) (polygonal tau, as in the paper).
  1. coarse grid at N0 = 256: beta_1 = k pi/18 (k < 18), beta_2 = k pi/24 (k < 24);
  2. two local refinements around the best grid point (9 x 9 grid with steps h/4, then 9 x 9 with steps h/16);
  3. N0 = 512 at the final minimiser, at the 1-D minimiser of phase_margin.py (0, 0.4654) and at (0, 0);
  4. consistency: the coarse rows (0, 0) and the 1-D minimiser are recomputed and compared with phase_margin.json.
Output: joint_phase_sweep.json (+ stdout saved as joint_phase_sweep_output.txt).  Deterministic.  CPU <= 4 min.
"""
import json
import os
import sys
import time

import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
sys.path.insert(0, os.path.join(ROOT, "experiments"))
from classify_pairs import classify, dist_matrix, vertex_dc  # noqa: E402
from recursive_knots import bishop_frame, circle, measure, min_rad, offset  # noqa: E402

F = 0.5


class Chain:
    """Caches K_1 (and its frame), K_2(beta_1) (and its frame, tau) at a given N0."""

    def __init__(self, N0):
        self.N0 = N0
        P0 = circle(N0)
        tau0 = measure(P0)["tau"]
        _, N, B, _ = bishop_frame(P0)
        self.K1 = offset(P0, N, B, F * tau0, 2, 3, 0.0)
        self.tau1 = measure(self.K1)["tau"]
        _, self.N1, self.B1, self.alpha2 = bishop_frame(self.K1)
        self.cache = {}

    def level2(self, b1):
        key = round(float(b1), 12)
        if key not in self.cache:
            K2 = offset(self.K1, self.N1, self.B1, F * self.tau1, 2, 3, float(b1))
            m2 = measure(K2)
            _, N2, B2, alpha3 = bishop_frame(K2)
            self.cache[key] = dict(K2=K2, tau2=m2["tau"], r2=F * self.tau1, N2=N2, B2=B2, alpha3=alpha3)
        return self.cache[key]

    def margin3(self, b1, b2):
        L2 = self.level2(b1)
        r3 = F * L2["tau2"]
        K3 = offset(L2["K2"], L2["N2"], L2["B2"], r3, 2, 3, float(b2))
        n = len(K3)
        D = dist_matrix(K3)
        mask = vertex_dc(D)
        I, J = np.nonzero(np.triu(mask, 1) | np.tril(mask, -1).T)
        cls, delta, chord = classify(L2["K2"], L2["tau2"], n, I, J)
        dist = D[I, J]
        nd = cls != "disc"
        j = int(np.argmin(np.where(nd, dist, np.inf)))
        tau3 = min(min_rad(K3), float(dist.min()) / 2)
        return dict(N0=self.N0, beta1=float(b1), beta2=float(b2), r3=r3, tau3_over_r3=tau3 / r3,
                    margin_pct=100 * (float(dist[j]) / (2 * r3) - 1), next_class=str(cls[j]),
                    delta_next=float(delta[j]), tau2_over_r2=L2["tau2"] / L2["r2"])


def main():
    t0, c0 = time.time(), time.process_time()
    rows = []
    C256 = Chain(256)
    # 1. coarse grid
    B1 = np.pi * np.arange(18) / 18
    B2 = np.pi * np.arange(24) / 24
    grid = np.full((18, 24), np.nan)
    for i, b1 in enumerate(B1):
        for j, b2 in enumerate(B2):
            r = C256.margin3(b1, b2)
            r["stage"] = "coarse"
            rows.append(r)
            grid[i, j] = r["margin_pct"]
    print(f"coarse grid 18 x 24 at N0 = 256: min margin {np.nanmin(grid):.4f} %, max {np.nanmax(grid):.4f} %  "
          f"(CPU {time.process_time() - c0:.0f} s)")
    i0, j0 = np.unravel_index(np.nanargmin(grid), grid.shape)
    best = (B1[i0], B2[j0])
    print(f"  coarse minimiser beta_1 = {best[0]:.4f}, beta_2 = {best[1]:.4f}: {grid[i0, j0]:.4f} %")
    rowmin = np.nanmin(grid, axis=1)
    print("  min over beta_2 for each beta_1 (period pi/3 expected => rows k, k+6, k+12 equal):")
    print("   ", " ".join(f"{x:.3f}" for x in rowmin))
    per = float(np.max(np.abs(rowmin[:6] - rowmin[6:12])) if True else 0)
    per2 = float(np.max(np.abs(rowmin[:6] - rowmin[12:18])))
    print(f"  max |rowmin(k) - rowmin(k+6)| = {per:.4f}, |rowmin(k) - rowmin(k+12)| = {per2:.4f}")
    # 2. refinements
    h1, h2 = np.pi / 18, np.pi / 24
    for stage, fac in (("refine1", 4), ("refine2", 16)):
        cand = []
        for a in range(-4, 5):
            for b in range(-4, 5):
                b1 = (best[0] + a * h1 / fac) % np.pi
                b2 = (best[1] + b * h2 / fac) % np.pi
                r = C256.margin3(b1, b2)
                r["stage"] = stage
                rows.append(r)
                cand.append(r)
        rb = min(cand, key=lambda x: x["margin_pct"])
        best = (rb["beta1"], rb["beta2"])
        print(f"  {stage}: minimiser beta_1 = {best[0]:.5f}, beta_2 = {best[1]:.5f}: {rb['margin_pct']:.4f} %  "
              f"(class {rb['next_class']}, delta {rb['delta_next']:.3f}; CPU {time.process_time() - c0:.0f} s)")
    # 4. consistency with phase_margin.py at N0 = 256
    pm = json.load(open(os.path.join(ROOT, "results", "phase_margin.json")))
    ref = {(round(x["beta"], 6)): x["margin_pct"] for x in pm["rows"] if x["d"] == 3 and x["N0"] == 256}
    chk = []
    for b2 in (0.0, 0.4654211338651545):
        r = C256.margin3(0.0, b2)
        chk.append(dict(beta2=b2, here=r["margin_pct"], phase_margin=ref.get(round(b2, 6))))
    print("  consistency with phase_margin.json (beta_1 = 0):", [(round(c["here"], 6), round(c["phase_margin"], 6)) for c in chk])
    # 3. N0 = 512
    C512 = Chain(512)
    fine = []
    for (b1, b2, tag) in ((best[0], best[1], "joint minimiser"), (0.0, 0.4654211338651545, "1-D minimiser"),
                          (0.0, 0.0, "default")):
        r = C512.margin3(b1, b2)
        r["stage"] = "N512:" + tag
        r256 = C256.margin3(b1, b2)
        rows.append(r)
        fine.append(dict(tag=tag, beta1=b1, beta2=b2, margin_256=r256["margin_pct"], margin_512=r["margin_pct"],
                         tau3_over_r3_512=r["tau3_over_r3"], class_512=r["next_class"]))
        print(f"  {tag:16s} (beta_1, beta_2) = ({b1:.5f}, {b2:.5f}): margin {r256['margin_pct']:.4f} % (N0=256), "
              f"{r['margin_pct']:.4f} % (N0=512); tau_3/r_3 = {r['tau3_over_r3']:.6f}")
    sel = [x for x in rows if x["N0"] == 256]
    summ = dict(n_evals_256=len(sel), min_margin_256=min(x["margin_pct"] for x in sel),
                max_margin_256=max(x["margin_pct"] for x in sel),
                argmin_256=dict(beta1=best[0], beta2=best[1]),
                min_tau3_over_r3=min(x["tau3_over_r3"] for x in rows), max_tau3_over_r3=max(x["tau3_over_r3"] for x in rows),
                negative_margin_found=any(x["margin_pct"] < 0 for x in rows),
                classes=sorted({x["next_class"] for x in rows}),
                rowmin_over_beta2=[float(x) for x in rowmin], period_check=dict(k_k6=per, k_k12=per2),
                fine=fine, consistency=chk, coarse_grid_beta1=[float(x) for x in B1], coarse_grid_beta2=[float(x) for x in B2],
                coarse_grid_margin_pct=grid.tolist())
    meta = dict(f=F, seconds_wall=time.time() - t0, seconds_cpu=time.process_time() - c0)
    with open(os.path.join(ROOT, "results", "joint_phase_sweep.json"), "w") as fh:
        json.dump(dict(meta=meta, summary=summ, rows=rows), fh, indent=1)
    print(f"summary: {summ['n_evals_256']} evaluations at N0 = 256, min margin {summ['min_margin_256']:.4f} %, "
          f"negative margin found: {summ['negative_margin_found']}, tau_3/r_3 in [{summ['min_tau3_over_r3']:.6f}, "
          f"{summ['max_tau3_over_r3']:.6f}], classes {summ['classes']}")
    print(f"wall {meta['seconds_wall']:.1f} s, CPU {meta['seconds_cpu']:.1f} s")


if __name__ == "__main__":
    main()
