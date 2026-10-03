#!/usr/bin/env python3
"""(H_3) data nu, mu, kappa_max of the SMOOTH default chain (2,3), f = 1/2, depths 1-4 (review round 4, m3).

Uses the smooth construction of smooth_margin.py (spectral Bishop frame, normalisation of Definition def:family,
phases 0); r_1 = 1/2, r_2 = f tau(K_1) with the N_0 = 512 polygonal tau, r_{d+1} = r_d/2.  Spectral derivatives;
nu = sup|v'|/v^2, mu = sup|Pi_perp d(kappa)/dt|/v.  Also the left-hand side of eq:tol at d = 3, 4 with these data.
Smooth evaluation at the samples (spectral accuracy), not a certified bound.  Output: results/smooth_H3.json.
"""
import json
import os
import time

import numpy as np

from smooth_margin import D, ROOT, build, dot, frame, nrm, tail


def data(X):
    X1, X2 = D(X, 1), D(X, 2)
    v = nrm(X1)
    T = X1 / v[:, None]
    vp = dot(X1, X2) / v
    kap = (X2 - vp[:, None] * T) / (v ** 2)[:, None]
    dk = D(kap, 1)
    kpar = dk - dot(dk, T)[:, None] * T
    return dict(nu=float(np.max(np.abs(vp) / v ** 2)), mu=float(np.max(nrm(kpar) / v)), kappa_max=float(nrm(kap).max()))


def main():
    t0 = time.process_time()
    res = json.load(open(os.path.join(ROOT, "results", "results.json")))
    ch = [c for c in res["chains"] if c["pattern"] == "(2,3)" and c["f"] == 0.5 and c["N0"] == 512][0]
    tau1 = [lv for lv in ch["levels"] if lv["d"] == 1][0]["tau"]
    RS = [0.5, 0.5 * tau1, 0.25 * tau1, 0.125 * tau1]
    M0 = 1024
    s = 2 * np.pi * np.arange(M0) / M0
    X = np.stack([np.cos(s), np.sin(s), 0 * s], 1)
    e1 = np.tile([0, 0, 1.0], (M0, 1))
    rows = []
    for d in range(4):
        N, B, al = frame(X, e1)
        X, e1 = build(X, N, B, RS[d])
        row = dict(d=d + 1, r=RS[d], samples=len(X), spectral_tail=tail(X), **data(X))
        rows.append(row)
        print(row, flush=True)
    s13 = np.sqrt(13.0)
    lhs = {str(d): 96 / s13 * 4.0 ** -d * rows[d - 2]["nu"] + 64 / s13 * 8.0 ** -d * rows[d - 2]["mu"] for d in (3, 4)}
    print("LHS of eq:tol with smooth data:", lhs)
    with open(os.path.join(ROOT, "results", "smooth_H3.json"), "w") as fh:
        json.dump(dict(rows=rows, tol_lhs=lhs, seconds_cpu=time.process_time() - t0), fh, indent=1)


if __name__ == "__main__":
    main()
