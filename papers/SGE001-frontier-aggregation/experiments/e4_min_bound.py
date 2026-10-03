#!/usr/bin/env python3
"""E4 (cells without capacity): share of comparisons certified by the margin condition (Proposition prop:margin) with
the smaller of the two valid bounds of Proposition prop:sharp(b), B = min(B2, |C3| + B3), in each norm and form
(round 3 of the internal review, m4; v0.5).

* Draws: exactly those of the reference run (generator 'E4' of SeedSequence(SEED).spawn(12), the same loop over sigma
  as run_E4 in frontier_aggregation.py), regenerated here.
* Bounds: the functions of theory/check_sharp_certificate.py (Lemma lem:cd4 with the corner rule, Frobenius norm of the
  entrywise suprema), imported read-only after checking that the script's SHA-256 is the frozen one in
  results/sharp_certificate.sha256 (its main() is not run, nothing is written into theory/).
* Consistency: the single-bound shares recomputed here must coincide exactly with the frozen
  theory/sharp_certificate_results.json and, for the Euclidean third-order bounds, with results/results.json.
* Output: results/e4_min_bound.json, deterministic (no timing field), so that its SHA-256, frozen in
  results/round3_checks.sha256 and checked by make_numbers.py, is reproducible bit for bit.  CPU time goes to stdout.
"""
import hashlib
import importlib.util
import json
import os
import sys
import time

sys.dont_write_bytecode = True          # no .pyc in experiments/ or theory/
import numpy as np  # noqa: E402

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
sys.path.insert(0, HERE)
import frontier_aggregation as fa  # noqa: E402  (classes, input laws, aggregate; nothing is run)

OUT_JSON = os.path.join(ROOT, "results", "e4_min_bound.json")


def frozen_hashes():
    out = {}
    for line in open(os.path.join(ROOT, "results", "sharp_certificate.sha256")):
        if line.strip():
            h, p = line.split()
            out[p] = h
    return out


def load_theory_module():
    """Import theory/check_sharp_certificate.py as a library, only if it is the frozen version."""
    path = os.path.join(ROOT, "theory", "check_sharp_certificate.py")
    got = hashlib.sha256(open(path, "rb").read()).hexdigest()
    want = frozen_hashes()["theory/check_sharp_certificate.py"]
    if got != want:
        raise SystemExit(f"e4_min_bound: theory script SHA-256 {got[:12]}... is not the frozen {want[:12]}...")
    spec = importlib.util.spec_from_file_location("check_sharp_certificate", path)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)        # defines functions only; main() is guarded by __name__ == "__main__"
    return mod


def main():
    c0 = time.process_time()
    th = load_theory_module()
    ref = json.load(open(os.path.join(ROOT, "results", "results.json")))
    refE4 = {r["sigma"]: r for r in ref["E4"]["rows"] if r["prox"] == "none"}
    frozen = json.load(open(os.path.join(ROOT, "theory", "sharp_certificate_results.json")))
    frozenE4 = {r["sigma"]: r for r in frozen["E4_no_capacity"]}

    gens = [np.random.default_rng(s) for s in np.random.SeedSequence(fa.SEED).spawn(12)]
    names = ["E0", "E1", "E1b", "E1c", "E2", "E3", "E4", "E5", "boot", "bootE2", "bootE3", "bootE1c"]
    rng = dict(zip(names, gens))["E4"]
    cd = fa.CobbDouglas()
    N, trials = 500, 1000
    xbarA = np.array([2.0, 1.0])
    deg = float(cd.al.sum())
    rows = []
    for s in [0.02, 0.05, 0.1, 0.2, 0.4, 0.8]:          # same loop and draw order as run_E4
        ZA = fa.base_noise(rng, trials, N, "LN")
        ZB = fa.base_noise(rng, trials, N, "LN")
        gamma = rng.uniform(-0.05, 0.05, size=trials)
        xbarB = xbarA[None, :] * (1.0 + gamma)[:, None] ** (1.0 / deg)
        XA = fa.inputs(xbarA, s, ZA, "LN")
        XB = fa.inputs(xbarB, s / 2.0, ZB, "LN")
        A, B = fa.aggregate(cd, XA), fa.aggregate(cd, XB)
        RA, RB = th.sharp_terms(cd, XA, "CD"), th.sharp_terms(cd, XB, "CD")
        true = np.sign(A["Y"] - B["Y"])
        d2 = A["Y2"] - B["Y2"]
        wrong = np.sign(d2) != true
        row = {"sigma": s, "rev2": float(np.mean(wrong))}
        nrev = 0
        for form in ("seg", "box", "seg_s", "box_s"):
            third = {"A": RA[f"B2{form}"], "B": RB[f"B2{form}"]}
            fourth = {"A": np.abs(RA["C3"]) + RA[f"B3{form}"], "B": np.abs(RB["C3"]) + RB[f"B3{form}"]}
            for label, bA, bB in (("third", third["A"], third["B"]), ("fourth", fourth["A"], fourth["B"]),
                                  ("min", np.minimum(third["A"], fourth["A"]), np.minimum(third["B"], fourth["B"]))):
                cert = np.abs(d2) > bA + bB
                row[f"{label}_{form}"] = float(np.mean(cert))
                nrev += int(np.sum(cert & wrong))
        # the best certificate available from each kind of information (all bounds are valid, so is their minimum)
        for info, forms in (("micro", ("seg", "seg_s")), ("moments", ("box", "box_s"))):
            bA = np.min([np.minimum(RA[f"B2{f}"], np.abs(RA["C3"]) + RA[f"B3{f}"]) for f in forms], axis=0)
            bB = np.min([np.minimum(RB[f"B2{f}"], np.abs(RB["C3"]) + RB[f"B3{f}"]) for f in forms], axis=0)
            cert = np.abs(d2) > bA + bB
            row[f"best_{info}"] = float(np.mean(cert))
            nrev += int(np.sum(cert & wrong))
        row["certified_reversals"] = nrev
        # consistency with the frozen theory run and with the reference run (exact equality of the shares)
        fz = frozenE4[s]
        for form in ("seg", "box", "seg_s", "box_s"):
            old = "old_" + form
            assert row[f"third_{form}"] == fz[old], (s, form, row[f"third_{form}"], fz[old])
            assert row[f"fourth_{form}"] == fz["new_B3" + form], (s, form)
        assert row["third_seg"] == refE4[s]["certified_frac"] and row["third_box"] == refE4[s]["certified_box_frac"], s
        assert row["rev2"] == refE4[s]["rev2"] == fz["rev2"], s
        assert nrev == 0, (s, nrev)                     # Proposition prop:margin: no certified reversal
        rows.append(row)
        print(f"sigma={s:4.2f}  " + "  ".join(f"{f}: 3rd {100*row['third_'+f]:5.1f} 4th {100*row['fourth_'+f]:5.1f} "
                                             f"min {100*row['min_'+f]:5.1f}" for f in ("seg", "seg_s", "box_s"))
              + f"  best micro {100*row['best_micro']:5.1f} best mom. {100*row['best_moments']:5.1f}", flush=True)
    out = {"meta": {"script": "experiments/e4_min_bound.py", "seed": fa.SEED, "generator": "E4 (child 6 of spawn(12))",
                    "N_per_sector": N, "trials": trials,
                    "bounds": "theory/check_sharp_certificate.py:sharp_terms (frozen SHA-256 "
                              + frozen_hashes()["theory/check_sharp_certificate.py"][:12] + ")",
                    "numpy": np.__version__, "python": sys.version.split()[0],
                    "keys": "third_<form>: B = B2; fourth_<form>: B = |C3| + B3; min_<form>: B = min of both; "
                            "best_micro / best_moments: min over seg, seg_s / box, box_s and both orders; "
                            "form: seg = segmentwise (micro data), box = coordinate box of the range (moments and range), "
                            "_s = norm scaled by S = diag(xbar)"},
           "rows": rows}
    with open(OUT_JSON, "w") as fh:
        json.dump(out, fh, indent=1, sort_keys=True)
        fh.write("\n")
    print(f"wrote {os.path.relpath(OUT_JSON, ROOT)};  CPU {time.process_time() - c0:.1f} s")


if __name__ == "__main__":
    main()
