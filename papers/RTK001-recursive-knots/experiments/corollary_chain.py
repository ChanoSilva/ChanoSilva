#!/usr/bin/env python3
"""The chain actually used by the Corollary (review round 2, m6): r_d = f rho_{d-1}, rho_d = gamma rho_{d-1}, rho_0 = 1,
gamma = min(1 - f, c f sin(pi/p)) with c = 1/2, (p, q) = (2, 3).  Measures tau_d (polygonal proxy of Section 2.4),
checks (H_c) with c = 1/2 along this chain, and compares L/tau with the conditional bound 2 pi Lambda^d.
Output: results/corollary_chain.json.  Deterministic; about 30 CPU seconds.
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
from recursive_knots import bishop_frame, circle, measure, offset  # noqa: E402


def run(N0, f, depth=3, c=0.5, p=2, q=3):
    gamma = min(1 - f, c * f * np.sin(np.pi / p))
    A = p * (1 + f) + f * (q + p / 2)
    Lam = A / gamma
    P = circle(N0)
    tau_prev = measure(P)["tau"]
    rho = 1.0
    out = []
    for d in range(1, depth + 1):
        _, Nn, B, _ = bishop_frame(P)
        r = f * rho
        Q = offset(P, Nn, B, r, p, q, 0.0)
        m = measure(Q)
        rho_hc = min(tau_prev - r, c * r * np.sin(np.pi / p))
        out.append(dict(d=d, N=len(Q), r=r, f_eff=r / tau_prev, tau=m["tau"], tau_over_rho_d=m["tau"] / (gamma * rho),
                        tau_over_rho_hc=m["tau"] / rho_hc, Rop=m["L"] / m["tau"], bound=2 * np.pi * Lam ** d))
        P, tau_prev, rho = Q, m["tau"], gamma * rho
    return dict(N0=N0, f=f, gamma=gamma, A=A, Lambda=Lam, levels=out)


def main():
    t0 = time.time()
    chains = [run(N0, f) for N0 in (256, 512) for f in (0.25, 0.35, 0.5)]
    meta = dict(seconds_wall=time.time() - t0, seconds_cpu=time.process_time())
    json.dump(dict(meta=meta, chains=chains), open(os.path.join(ROOT, "results", "corollary_chain.json"), "w"), indent=1)
    for ch in chains:
        print(f"N0={ch['N0']} f={ch['f']} Lambda={ch['Lambda']:.2f}: " + "; ".join(
            f"d={lv['d']} tau/rho_d={lv['tau_over_rho_d']:.3f} tau/rho_Hc={lv['tau_over_rho_hc']:.3f} L/tau={lv['Rop']:.1f} "
            f"bound={lv['bound']:.0f}" for lv in ch["levels"]))
    print(f"wall {meta['seconds_wall']:.1f} s, CPU {meta['seconds_cpu']:.1f} s")


if __name__ == "__main__":
    main()
