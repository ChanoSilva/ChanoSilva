#!/usr/bin/env python3
"""Optional probe: discrete curve shortening of K_1 and K_2 with renormalisation.

Each step moves every vertex towards the midpoint of its neighbours (explicit
discrete curve-shortening step with weight LAM); after the step the polygon is
measured, and the ratio L/tau is recorded (it is scale invariant, so no explicit
rescaling is needed).  The best configuration seen is kept.  This is a numerical
probe only: nothing is certified, the flow is not a gradient of L at fixed
thickness, and the knot type is only checked through tau > 0 at every step.
"""
import json
import os
import time

import numpy as np

import recursive_knots as rk

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
LAM = 0.1
STEPS = 200
N0 = 512
F = 0.5


def shrink(P, steps, lam):
    m0 = rk.measure(P)
    best = dict(m0, step=0)
    hist = [m0["Rop"]]
    lost = False
    for k in range(1, steps + 1):
        P = P + lam * (np.roll(P, 1, axis=0) + np.roll(P, -1, axis=0) - 2 * P)
        m = rk.measure(P)
        hist.append(m["Rop"])
        if not np.isfinite(m["tau"]) or m["tau"] <= 0:
            lost = True
            break
        if m["Rop"] < best["Rop"]:
            best = dict(m, step=k)
    return m0, best, hist, lost


def main():
    t0 = time.time()
    P = rk.circle(N0)
    tau_prev = 1.0
    out = {"meta": dict(lam=LAM, steps=STEPS, N0=N0, f=F, pattern=[2, 3]), "levels": []}
    for d in (1, 2):
        T, N, B, alpha = rk.bishop_frame(P)
        r = F * tau_prev
        P = rk.offset(P, N, B, r, 2, 3)
        tau_prev = rk.measure(P)["tau"]
        tc = time.time()
        m0, best, hist, lost = shrink(P.copy(), STEPS, LAM)
        out["levels"].append(dict(d=d, N=int(len(P)), Rop_start=m0["Rop"], Rop_best=best["Rop"],
                                  best_step=best["step"], tau_best=best["tau"], L_best=best["L"],
                                  Rop_end=hist[-1], steps_run=len(hist) - 1, lost_thickness=lost,
                                  improvement_pct=100 * (1 - best["Rop"] / m0["Rop"]),
                                  hist=[float(h) for h in hist], seconds=time.time() - tc))
        print(f"d={d}: N={len(P)} Rop {m0['Rop']:.2f} -> best {best['Rop']:.2f} at step {best['step']} "
              f"(end {hist[-1]:.2f}, lost={lost}, {time.time()-tc:.0f}s)", flush=True)
    out["meta"]["seconds"] = time.time() - t0
    with open(os.path.join(ROOT, "results", "results_shrink.json"), "w") as fh:
        json.dump(out, fh, indent=1)
    with open(os.path.join(ROOT, "results", "tables_shrink.md"), "w") as fh:
        fh.write("# Curve-shortening probe (uncertified)\n\n| d | N | Rop start | Rop best | step | Rop end | lost thickness |\n|---|---|---|---|---|---|---|\n")
        for lv in out["levels"]:
            fh.write(f"| {lv['d']} | {lv['N']} | {lv['Rop_start']:.2f} | {lv['Rop_best']:.2f} | {lv['best_step']} | {lv['Rop_end']:.2f} | {lv['lost_thickness']} |\n")
    print(f"done in {time.time()-t0:.0f}s")


if __name__ == "__main__":
    main()
