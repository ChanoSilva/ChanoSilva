#!/usr/bin/env python3
"""CES frontier, E1: how far the certificates of Propositions prop:smooth(e) and prop:sharp(c) would reach if the
derivative suprema over the coordinate box of the population were known exactly (round 3 of the internal review, m6;
v0.5).  NOT a bound: the supremum of each entry of D^k f over the box is *estimated* by its maximum on a 33 x 33
geometric grid, which can only be smaller than any valid enclosure.  The comparison with the certified dispersions of
the frozen theory run (interval enclosures) shows how much of the CES gap is due to the looseness of the enclosure.

* Draws: those of the reference run (generator 'E1' of SeedSequence(SEED).spawn(12), the same order of draws as
  run_E1 in frontier_aggregation.py: CD-LN, CD-SU, CES-LN, CES-SU), regenerated here.
* Derivatives: ces_deriv of theory/check_sharp_certificate.py (Faa di Bruno), imported read-only after checking the
  script's frozen SHA-256 (its main() is not run, nothing is written into theory/).
* Output: results/ces_grid_estimate.json, deterministic (no timing field); SHA-256 frozen in
  results/round3_checks.sha256 and checked by make_numbers.py.  CPU time goes to stdout.
"""
import json
import math
import os
import sys
import time

sys.dont_write_bytecode = True
import numpy as np  # noqa: E402

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
sys.path.insert(0, HERE)
import frontier_aggregation as fa  # noqa: E402
from e4_min_bound import load_theory_module  # noqa: E402  (hash-checked import of the frozen theory script)

OUT_JSON = os.path.join(ROOT, "results", "ces_grid_estimate.json")
NG = 33


def grid_sup(th, front, k, lo, hi, s):
    """Frobenius norm of the entrywise maxima of |D^k f| (columns scaled by s) on an NG x NG geometric grid of each
    box [lo, hi] (T, 2).  An estimate from below of the quantity the enclosures bound."""
    u = np.linspace(0.0, 1.0, NG)
    r = hi / lo
    g0 = lo[:, None, 0] * r[:, None, 0] ** u[None, :]
    g1 = lo[:, None, 1] * r[:, None, 1] ** u[None, :]
    P = np.stack(np.broadcast_arrays(g0[:, :, None], g1[:, None, :]), axis=-1).reshape(lo.shape[0], NG * NG, 2)
    D = np.abs(th.ces_deriv(front, P, k)).max(axis=1)           # (T, 2, ..., 2)
    if s is not None:
        for ax in range(k):
            shp = [1] * (k + 1)
            shp[0], shp[ax + 1] = s.shape[0], 2
            D = D * s.reshape(shp)
    return np.sqrt(np.sum(D.reshape(D.shape[0], -1) ** 2, axis=1))


def largest_uniform(sigmas, flags):
    out = 0.0
    for s, f in zip(sigmas, flags):
        if not f:
            break
        out = float(s)
    return out


def main():
    c0 = time.process_time()
    th = load_theory_module()
    frozen = json.load(open(os.path.join(ROOT, "theory", "sharp_certificate_results.json")))
    gens = [np.random.default_rng(s) for s in np.random.SeedSequence(fa.SEED).spawn(12)]
    rngE1 = gens[1]                                             # generator 'E1'
    N, R = 2000, 20
    xbar = np.array([2.0, 1.0])
    grids = {"LN": np.logspace(-2, 0, 17), "SU": np.logspace(-2, math.log10(0.5), 15)}
    Zs = {}
    for fname in ("CD", "CES"):                                 # same order of draws as run_E1
        for law in ("LN", "SU"):
            Zs[(fname, law)] = fa.base_noise(rngE1, R, N, law)
    ces = fa.CES()
    out = {"meta": {"script": "experiments/ces_grid_estimate.py", "seed": fa.SEED, "generator": "E1 (child 1 of spawn(12))",
                    "N": N, "reps": R, "grid": f"{NG} x {NG} geometric grid on the coordinate box of each population",
                    "note": "grid maxima are estimates from below of the derivative suprema: NOT a certificate",
                    "numpy": np.__version__, "python": sys.version.split()[0]}}
    for law in ("LN", "SU"):
        flags = {f"{o}{sc}_k{k}": [] for o in ("third", "fourth") for sc in ("", "_s") for k in (1, 5)}
        for s in grids[law]:
            X = fa.inputs(xbar, s, Zs[("CES", law)], law)
            A = fa.aggregate(ces, X, bounds=False)
            Q2, C3 = A["Q2"], A["Y3"] - A["Y2"]
            xb = X.mean(axis=1)
            H = X - xb[:, None, :]
            hn = np.sqrt(np.sum(H ** 2, axis=2))
            vn = np.sqrt(np.sum((H / xb[:, None, :]) ** 2, axis=2))
            lo, hi = X.min(axis=1), X.max(axis=1)
            for sc, scale, nrm in (("", None, hn), ("_s", xb, vn)):
                B2 = N / 6.0 * grid_sup(th, ces, 3, lo, hi, scale) * np.mean(nrm ** 3, axis=1)
                B3 = N / 24.0 * grid_sup(th, ces, 4, lo, hi, scale) * np.mean(nrm ** 4, axis=1)
                for k in (1, 5):
                    flags[f"third{sc}_k{k}"].append(bool(np.all((k + 1) * B2 < np.abs(Q2))))
                    flags[f"fourth{sc}_k{k}"].append(bool(np.all((k + 1) * (np.abs(C3) + B3) < np.abs(Q2))))
        summ = {key: largest_uniform(grids[law], f) for key, f in flags.items()}
        # an estimate from below of the suprema cannot certify less than the rigorous enclosures of the theory run
        fz = frozen["E1"][f"CES-{law}"]["summary"]
        for k in (1, 5):
            assert summ[f"third_k{k}"] >= fz[f"sigma_cert{k}|B2box"] and summ[f"fourth_k{k}"] >= fz[f"sigma_cert{k}|B3box"], (law, k)
            assert summ[f"third_s_k{k}"] >= fz[f"sigma_cert{k}|B2box_s"] and summ[f"fourth_s_k{k}"] >= fz[f"sigma_cert{k}|B3box_s"], (law, k)
        out[f"CES-{law}"] = summ
        print(f"CES-{law}: grid estimate of the largest certified sigma (moments and range): {summ};  enclosure (frozen): "
              f"third {fz['sigma_cert1|B2box']:.3f}, fourth {fz['sigma_cert1|B3box']:.3f}, fourth scaled {fz['sigma_cert1|B3box_s']:.3f} (k=1)",
              flush=True)
    with open(OUT_JSON, "w") as fh:
        json.dump(out, fh, indent=1, sort_keys=True)
        fh.write("\n")
    print(f"wrote {os.path.relpath(OUT_JSON, ROOT)};  CPU {time.process_time() - c0:.1f} s")


if __name__ == "__main__":
    main()
