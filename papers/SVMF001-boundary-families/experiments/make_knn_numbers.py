#!/usr/bin/env python3
"""SVMF001 v0.4 -- macros of the neighbourhood-localisation results for the manuscript.

Reads the FROZEN output theory/knn_localisation_results.json (written by
theory/check_knn_localisation.py, seed 20261003) and writes manuscript/knn_numbers.tex.
No simulation is run and nothing under theory/ is written.

Checks, in order:
  1. the SHA-256 of theory/knn_localisation_results.json equals the digest frozen in
     results/knn_localisation_results.sha256 (so the numbers cannot drift silently);
  2. the 51 macros stored under the key "macros" are re-derived from the raw results with
     make_macros() of theory/check_knn_localisation.py and must coincide exactly.
Then it emits the stored macros plus a few macros with DIRECTED rounding for the sentences
that state a bound ("within ...", "at least ...", "between ... and ..."), because the
stored values round to nearest and four of them would make the bound false by the letter:
  \\KLPtwoMaxZUp     ceil(max |risk - Rinf| / se, n = 20000, k <= 5), 1 decimal
  \\KLPtwoMaxDiffUp  ceil(max |risk - Rinf|, n = 20000, k <= 20), 4 decimals
  \\KLPtwoMinGapDown floor(min (risk - R_nc(n)) over the 36 cases), 3 decimals
  \\KLPtwoDallMaxUp  ceil(max risk, neighbourhoods in all d coordinates, n = 2000), 3 decimals
  \\KLPtwoDallMinDown floor(min of the same), 3 decimals
  \\KLSelMaxZUp      ceil(max |z| of P1, 1 < k <= n), 1 decimal            (v0.5)
v0.5 (round 3 of internal review, m7): the stored nearest-rounded versions of these bounds
(NOT_EMITTED below) are still re-derived and checked, but no longer written to
knn_numbers.tex, so that nobody can use them as bounds by mistake.
v0.5 (round 3, M2): descriptive macros of the k = rho n block (P4), rounded to nearest:
  \\KLRatioQuarterHardA/B  ratio +- se at mu = 0.5, rho = 1/4, n = 2000 / 8000
  \\KLZQuarterHardC, \\KLZQuarterMainC  z = (ratio - Q(1/4)) / se at the largest n
  \\KLGapQuarterHardPct, \\KLGapQuarterMainPct  100 (1 - ratio / Q(1/4)) at the largest n
  \\KLHalfMaxZUp  ceil(max |ratio - Q(1/2)| / se over mu and n), 1 decimal (directed: a bound)
Usage: python3 experiments/make_knn_numbers.py   (from any directory)
"""
import hashlib
import importlib.util
import json
import math
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
SRC = os.path.join(ROOT, "theory", "knn_localisation_results.json")
SHA = os.path.join(ROOT, "results", "knn_localisation_results.sha256")
OUT = os.path.join(ROOT, "manuscript", "knn_numbers.tex")


def sha256(path):
    h = hashlib.sha256()
    with open(path, "rb") as f:
        h.update(f.read())
    return h.hexdigest()


def frozen_digest():
    with open(SHA) as f:
        return f.read().split()[0]


def load_make_macros():
    sys.dont_write_bytecode = True          # do not create theory/__pycache__
    spec = importlib.util.spec_from_file_location(
        "check_knn_localisation", os.path.join(ROOT, "theory", "check_knn_localisation.py"))
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)            # module level only defines functions/constants
    return mod.make_macros


def ceil_to(x, dec):
    f = 10 ** dec
    return f"{math.ceil(x * f - 1e-12) / f:.{dec}f}"


def floor_to(x, dec):
    f = 10 ** dec
    return f"{math.floor(x * f + 1e-12) / f:.{dec}f}"


def directed(res):
    d1 = res["P2"]["d1"]
    nbig = max(r["n"] for r in d1)
    M = {}
    M["KLPtwoMaxZUp"] = ceil_to(max(abs(r["risk_mc"] - r["Rinf_nc_k"]) / r["se"]
                                    for r in d1 if r["n"] == nbig and r["k"] <= 5), 1)
    M["KLPtwoMaxDiffUp"] = ceil_to(max(abs(r["risk_mc"] - r["Rinf_nc_k"]) for r in d1 if r["n"] == nbig), 4)
    M["KLPtwoMinGapDown"] = floor_to(min(r["risk_mc"] - r["R_nc_n"] for r in d1), 3)
    dall = [r["risk_mc"] for r in res["P2"]["dall"] if r["n"] == 2000]
    M["KLPtwoDallMinDown"] = floor_to(min(dall), 3)
    M["KLPtwoDallMaxUp"] = ceil_to(max(dall), 3)
    sel = [r for r in res["P1"]["nc"] if 1 < r["k"] <= r["n"]]
    M["KLSelMaxZUp"] = ceil_to(max(abs(r["z"]) for r in sel), 1)
    return M


# stored macros that round a stated bound to nearest (round 3, m7): checked, not emitted
NOT_EMITTED = ("KLSelMaxZ", "KLPtwoMaxZ", "KLPtwoMaxDiff", "KLPtwoMinGap",
               "KLPtwoDallMin", "KLPtwoDallMax")


def rho_block(res):
    """Descriptive macros of P4 (k = rho n) used by Remark rem:rho / Appendix B (round 3, M2)."""
    p4 = res["P4"]
    mu0, mh = res["meta"]["mu_main"], res["meta"]["mu_hard"]
    nb4 = max(r["n"] for r in p4)

    def r4(mu, n, rho):
        return [r for r in p4 if r["mu"] == mu and r["n"] == n and r["rho"] == rho][0]

    M = {}
    for n, tag in ((2000, "A"), (8000, "B")):
        a = r4(mh, n, 0.25)
        M[f"KLRatioQuarterHard{tag}"] = f"{a['ratio']:.0f}\\pm{a['ratio_se']:.0f}"
    for mu, tag in ((mh, "Hard"), (mu0, "Main")):
        a = r4(mu, nb4, 0.25)
        M[f"KLZQuarter{tag}C"] = f"{(a['ratio'] - a['Q_heuristic']) / a['ratio_se']:.1f}"
        M[f"KLGapQuarter{tag}Pct"] = f"{100 * (1 - a['ratio'] / a['Q_heuristic']):.0f}"
    half = [r for r in p4 if r["rho"] == 0.5]
    M["KLHalfMaxZUp"] = ceil_to(max(abs(r["ratio"] - r["Q_heuristic"]) / r["ratio_se"] for r in half), 1)
    return M


def main():
    got, want = sha256(SRC), frozen_digest()
    if got != want:
        sys.exit(f"SHA-256 mismatch for {SRC}:\n  found  {got}\n  frozen {want}\n"
                 "The theory results changed: re-verify them before updating the frozen digest.")
    with open(SRC) as f:
        res = json.load(f)
    stored = res["macros"]
    recomputed = load_make_macros()(res)
    if recomputed != stored:
        bad = sorted(k for k in set(stored) | set(recomputed) if stored.get(k) != recomputed.get(k))
        sys.exit(f"stored macros differ from those re-derived from the raw results: {bad}")
    extra = directed(res)
    rho = rho_block(res)
    assert not set(extra) & set(stored) and not set(rho) & (set(stored) | set(extra))
    assert set(NOT_EMITTED) <= set(stored)
    emitted = {k: v for k, v in stored.items() if k not in NOT_EMITTED}
    lines = ["% generated by experiments/make_knn_numbers.py from theory/knn_localisation_results.json",
             f"% (SHA-256 {got}, checked against results/knn_localisation_results.sha256);",
             f"% {len(stored)} macros re-derived from the raw results and equal to the stored key 'macros';",
             f"% {len(emitted)} of them emitted (the {len(NOT_EMITTED)} nearest-rounded bounds are not: "
             + ", ".join(NOT_EMITTED) + "),",
             f"% plus {len(extra)} with directed rounding for stated bounds and {len(rho)} for the k = rho n block.",
             "% Do not edit by hand."]
    lines += [f"\\newcommand{{\\{k}}}{{{v}}}" for k, v in emitted.items()]
    lines += [f"\\newcommand{{\\{k}}}{{{v}}}" for k, v in extra.items()]
    lines += [f"\\newcommand{{\\{k}}}{{{v}}}" for k, v in rho.items()]
    with open(OUT, "w") as f:
        f.write("\n".join(lines) + "\n")
    print(f"wrote {OUT}: {len(emitted)} of {len(stored)} stored + {len(extra)} directed + "
          f"{len(rho)} rho-block macros; SHA-256 ok")


if __name__ == "__main__":
    main()
