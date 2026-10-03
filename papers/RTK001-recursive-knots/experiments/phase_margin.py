#!/usr/bin/env python3
"""Dependence on the normalisation of the Bishop frame (review round 3, M1).
Note (review round 4, m7): at d = 2 the scan is not refined around the minimum; by the period pi/3 and the smooth
evaluation (smooth_margin.py) the minimum is at beta_2 = 0 up to discretisation.  The joint scan of (beta_2, beta_3)
is experiments/joint_phase_sweep.py; the polygonal values here are biased upwards (see smooth_margin.py).

Rotating the initial normal N_{d-1}(0) of the closed Bishop frame by an angle beta is the same as replacing the phase
phi_d by phi_d + beta (the transport and the closing twist are linear in the initial normal), and phi_d + pi gives the
same curve for p = 2, q odd (the two strands are exchanged).  So the normalisation is scanned as beta in [0, pi).

For the default chain (2,3), f = 1/2:
  d = 2: beta_2 on 12 values in [0, pi) at N0 = 256 (the margin has period pi/3 in beta_2: 3-fold symmetry of K_1) (phi_1 = 0; at d = 1 the circle makes beta irrelevant up to a
         congruence), and at N0 = 512 for beta = 0 and for the minimising beta;
  d = 3: beta_3 on 12 values in [0, pi) at N0 = 256, with beta_2 = 0, refined by 8 values within pi/12 of the
         minimiser, and at N0 = 512 for beta_3 = 0 and the refined minimiser (a one-parameter scan, not a 2-D one).
For each: L(K_d), tau(K_d)/r_d, and the margin of Conjecture conj (3.25 in v0.5) = (smallest vertex doubly critical distance over
pairs that are not antipodal pairs of one normal disc) / (2 r_d) - 1, with the census of classify_pairs.py.
Output: results/phase_margin.json.  Deterministic; about 2 CPU minutes.
"""
import json
import os
import sys
import time

import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
sys.path.insert(0, HERE)
from classify_pairs import level_census  # noqa: E402  (also imports recursive_knots)
from recursive_knots import bishop_frame, circle, length, measure, offset  # noqa: E402

F = 0.5


def chain_to(N0, betas):
    """Build K_1..K_len(betas) with phase betas[d-1] at depth d; return per-level records of the last level."""
    P = circle(N0)
    tau_b = measure(P)["tau"]
    for d, beta in enumerate(betas, start=1):
        _, Nn, B, _ = bishop_frame(P)
        r = F * tau_b
        Q = offset(P, Nn, B, r, 2, 3, beta)
        if d == len(betas):
            m = measure(Q)
            cen = level_census(P, tau_b, r, Q)["vertex"]
            return dict(N0=N0, d=d, beta=float(beta), L=length(Q), r=r, tau_over_r=m["tau"] / r,
                        margin_pct=100 * (cen["next_over_2r"] - 1), next_class=cen["next_class"],
                        k0=cen["k0"]["n"], k1=cen["k1"]["n"])
        P, tau_b = Q, measure(Q)["tau"]


def main():
    t0, c0 = time.time(), time.process_time()
    rows = []
    for b in np.pi * np.arange(12) / 12:
        rows.append(chain_to(256, [0.0, b]))
    d2 = [x for x in rows if x["d"] == 2 and x["N0"] == 256]
    bmin = min(d2, key=lambda x: x["margin_pct"])["beta"]
    for b in sorted({0.0, bmin}):
        rows.append(chain_to(512, [0.0, b]))
    for b in np.pi * np.arange(12) / 12:
        rows.append(chain_to(256, [0.0, 0.0, b]))
    d3 = [x for x in rows if x["d"] == 3 and x["N0"] == 256]
    bmin3 = min(d3, key=lambda x: x["margin_pct"])["beta"]
    for b in bmin3 + (np.pi / 12) * (np.arange(-4, 5) / 4.5):     # refinement around the minimiser
        if abs(b - bmin3) > 1e-12:
            rows.append(chain_to(256, [0.0, 0.0, float(b % np.pi)]))
    d3 = [x for x in rows if x["d"] == 3 and x["N0"] == 256]
    bmin3 = min(d3, key=lambda x: x["margin_pct"])["beta"]
    for b in sorted({0.0, bmin3}):
        rows.append(chain_to(512, [0.0, 0.0, b]))
    summ = {}
    for d in (2, 3):
        for N0 in (256, 512):
            sel = [x for x in rows if x["d"] == d and x["N0"] == N0]
            if not sel:
                continue
            Ls = [x["L"] for x in sel]
            summ[f"d{d}_N{N0}"] = dict(n=len(sel), margin_min=min(x["margin_pct"] for x in sel),
                                      margin_max=max(x["margin_pct"] for x in sel),
                                      beta_at_min=min(sel, key=lambda x: x["margin_pct"])["beta"],
                                      tau_over_r_min=min(x["tau_over_r"] for x in sel),
                                      tau_over_r_max=max(x["tau_over_r"] for x in sel),
                                      L_rel_spread=(max(Ls) - min(Ls)) / min(Ls),
                                      k0_total=sum(x["k0"] for x in sel), k1_total=sum(x["k1"] for x in sel),
                                      classes=sorted({x["next_class"] for x in sel}))
    meta = dict(f=F, seconds_wall=time.time() - t0, seconds_cpu=time.process_time() - c0)
    with open(os.path.join(ROOT, "results", "phase_margin.json"), "w") as fh:
        json.dump(dict(meta=meta, summary=summ, rows=rows), fh, indent=1)
    for k, v in summ.items():
        print(k, {a: (round(b, 5) if isinstance(b, float) else b) for a, b in v.items()})
    print(f"wall {meta['seconds_wall']:.1f} s, CPU {meta['seconds_cpu']:.1f} s")


if __name__ == "__main__":
    main()
