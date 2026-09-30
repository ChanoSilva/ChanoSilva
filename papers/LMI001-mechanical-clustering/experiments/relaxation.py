#!/usr/bin/env python3
"""E3 for LMI001: spring relaxation heuristics versus kernel k-means optimisers
on the same energy.

Methods (all see the same kernel matrix, i.e. the same spring network):
  lloyd        batch Lloyd in the feature space of the PSD-shifted kernel
  lloyd+relax  lloyd followed by zero-temperature single-particle relaxation
  relax        zero-temperature single-particle relaxation from the initial labels
               (this is Hartigan's method written in spring energies)
  anneal       Metropolis on the spring energy with geometric cooling, then relax
Initialisations shared by all methods: random labels, and kernel k-means++ seeds.

Predefined criteria (written before the runs):
  C3a  Every fixed point of relax and of anneal is Voronoi-stable in the feature
       space of the PSD-shifted kernel (Proposition 3 predicts 100 %).
  C3b  Same energy, so the comparison is between optimisers of one function:
       the mechanical relaxation is called "distinguishable" from the kernel
       k-means family only if its best-of-R energy is below the best-of-R energy
       of lloyd+relax by more than 1e-6 relative in some configuration, or above
       it by more than 1e-6 in some configuration (then one optimiser is better;
       either way the objective and the partitions found at equal energy are the
       same). Reported: best and median relative excess energy per method,
       fraction of restarts reaching the best energy found, ARI between the best
       partitions of relax and lloyd+relax (expected 1 when energies agree).
  C3c  The fraction of lloyd fixed points that are not single-move stable is
       reported (the inclusion of Proposition 3 is expected to be strict).
"""
from __future__ import annotations

import json
import os
import platform
import sys
import time

import numpy as np
import scipy
import sklearn
from scipy.spatial.distance import pdist, squareform
from sklearn.metrics import adjusted_rand_score

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import mechanical as M  # noqa: E402

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
RES = os.path.join(ROOT, "results")
FIG = os.path.join(ROOT, "figures")
os.makedirs(RES, exist_ok=True)
os.makedirs(FIG, exist_ok=True)

FAST = "--fast" in sys.argv
SEED = M.MASTER_SEED + 1
R = 4 if FAST else 10          # restarts per initialisation type
R_ANNEAL = 2 if FAST else 5    # annealing restarts (uses the first random inits)
N_SWEEPS_ANNEAL = 20 if FAST else 40
REL_TOL_BEST = 1e-6


def run_config(Ks, pot, n, k, sigma, rng, y_true):
    const = M.theorem_constant(n, k, pot, sigma)
    runs = []
    inits = []
    for r in range(R):
        inits.append(("random", M.random_partition(rng, n, k)))
    for r in range(R):
        inits.append(("kpp", M.kmeanspp_labels(Ks, k, rng)))
    for idx, (itype, lab0) in enumerate(inits):
        # lloyd and lloyd+relax
        st = M.KKMState(Ks, lab0, k)
        it = st.lloyd()
        E_l = 0.5 * st.objective() + const
        h_stable = st.is_hartigan_stable()
        v_stable = st.is_voronoi_stable()
        runs.append(dict(method="lloyd", init=itype, r=idx, E=E_l, iters=it, voronoi=v_stable,
                         hartigan=h_stable, labels=st.labels.copy()))
        sw, mv = st.hartigan(rng)
        runs.append(dict(method="lloyd+relax", init=itype, r=idx, E=0.5 * st.objective() + const,
                         iters=it + sw, voronoi=st.is_voronoi_stable(), hartigan=True,
                         labels=st.labels.copy(), polish_moves=mv))
        # relax from scratch
        st = M.KKMState(Ks, lab0, k)
        sw, mv = st.hartigan(rng)
        runs.append(dict(method="relax", init=itype, r=idx, E=0.5 * st.objective() + const, iters=sw,
                         voronoi=st.is_voronoi_stable(), hartigan=True, labels=st.labels.copy()))
        # anneal (random inits only, first R_ANNEAL)
        if itype == "random" and idx < R_ANNEAL:
            st = M.KKMState(Ks, lab0, k)
            T0, acc, sw = st.anneal(rng, n_sweeps=N_SWEEPS_ANNEAL)
            runs.append(dict(method="anneal", init=itype, r=idx, E=0.5 * st.objective() + const,
                             iters=N_SWEEPS_ANNEAL + sw, voronoi=st.is_voronoi_stable(), hartigan=True,
                             labels=st.labels.copy(), T0=T0, accepted=acc))
    E_best = min(r["E"] for r in runs)
    best_of = {}
    for r in runs:
        r["rel_excess"] = (r["E"] - E_best) / abs(E_best)
        r["reaches_best"] = r["rel_excess"] <= REL_TOL_BEST
        if r["method"] not in best_of or r["E"] < best_of[r["method"]]["E"]:
            best_of[r["method"]] = r
    summary = {}
    for mname in ("lloyd", "lloyd+relax", "relax", "anneal"):
        rr = [r for r in runs if r["method"] == mname]
        summary[mname] = dict(
            runs=len(rr), best_E=best_of[mname]["E"],
            best_rel_excess=(best_of[mname]["E"] - E_best) / abs(E_best),
            median_rel_excess=float(np.median([r["rel_excess"] for r in rr])),
            frac_reaching_best=float(np.mean([r["reaches_best"] for r in rr])),
            frac_voronoi_stable=float(np.mean([r["voronoi"] for r in rr])),
            frac_hartigan_stable=float(np.mean([r["hartigan"] for r in rr])),
            mean_iters=float(np.mean([r["iters"] for r in rr])),
            ari_best_vs_truth=float(adjusted_rand_score(y_true, best_of[mname]["labels"])),
        )
    ari_rl = float(adjusted_rand_score(best_of["relax"]["labels"], best_of["lloyd+relax"]["labels"]))
    ari_al = float(adjusted_rand_score(best_of["anneal"]["labels"], best_of["lloyd+relax"]["labels"]))
    best_rel = {m: summary[m]["best_rel_excess"] for m in summary}
    diff_relax = summary["relax"]["best_E"] - summary["lloyd+relax"]["best_E"]
    return dict(E_best=E_best, summary=summary, ari_best_relax_vs_lloydrelax=ari_rl,
                ari_best_anneal_vs_lloydrelax=ari_al,
                relax_minus_lloydrelax_rel=diff_relax / abs(E_best),
                distinguishable=bool(abs(diff_relax / abs(E_best)) > REL_TOL_BEST),
                best_labels={m: best_of[m]["labels"].tolist() for m in ("relax", "lloyd+relax")},
                runs=[{kk: v for kk, v in r.items() if kk != "labels"} for r in runs])


def main():
    t_start = time.time()
    rng = np.random.default_rng(SEED)
    datasets = M.load_datasets(M.MASTER_SEED, n_synthetic=150 if FAST else 300, n_digits=150 if FAST else 300)
    configs = []
    for dname, (X, y, k) in datasets.items():
        sc = M.data_scales(X)
        pots = M.make_potentials(sc["ell"], sc["rest"])
        for pname, pot in pots.items():
            t0 = time.time()
            Xl = M.lifted_coordinates(X, pname, sc["lift_scale"])
            D = squareform(pdist(Xl))
            n = len(Xl)
            K = M.kernel_from_potential(D, pot)
            sigma, lam_min = M.psd_shift(K)
            Ks = K + sigma * np.eye(n)
            out = run_config(Ks, pot, n, k, sigma, rng, y)
            # independent check of the energy of the best partition, spring by spring
            lab = np.array(out["best_labels"]["relax"])
            E_direct = M.energy_direct(D, lab, pot, "per_particle")
            out["direct_check_rel_err"] = abs(E_direct - out["summary"]["relax"]["best_E"]) / max(1.0, abs(E_direct))
            out.update(dataset=dname, potential=pname, n=n, k=k, sigma=sigma, lam_min_K=lam_min,
                       seconds=time.time() - t0)
            configs.append(out)
            s = out["summary"]
            print(f"E3 {dname:8s} {pname:11s} E*={out['E_best']:.6g} "
                  f"relax:{s['relax']['best_rel_excess']:.1e}/{s['relax']['frac_reaching_best']:.2f} "
                  f"lloyd+relax:{s['lloyd+relax']['best_rel_excess']:.1e}/{s['lloyd+relax']['frac_reaching_best']:.2f} "
                  f"lloyd:{s['lloyd']['best_rel_excess']:.1e}/{s['lloyd']['frac_reaching_best']:.2f} "
                  f"anneal:{s['anneal']['best_rel_excess']:.1e} vor(relax)={s['relax']['frac_voronoi_stable']:.2f} "
                  f"hart(lloyd)={s['lloyd']['frac_hartigan_stable']:.2f} ARI={out['ari_best_relax_vs_lloydrelax']:.2f} "
                  f"[{out['seconds']:.1f}s]")
    # aggregate
    agg = {}
    for m in ("lloyd", "lloyd+relax", "relax", "anneal"):
        agg[m] = dict(
            configs=len(configs),
            n_runs=sum(c["summary"][m]["runs"] for c in configs),
            frac_voronoi_stable=float(np.mean([c["summary"][m]["frac_voronoi_stable"] for c in configs])),
            n_voronoi_stable=int(round(sum(c["summary"][m]["frac_voronoi_stable"] * c["summary"][m]["runs"] for c in configs))),
            frac_hartigan_stable=float(np.mean([c["summary"][m]["frac_hartigan_stable"] for c in configs])),
            n_hartigan_stable=int(round(sum(c["summary"][m]["frac_hartigan_stable"] * c["summary"][m]["runs"] for c in configs))),
            configs_reaching_best=int(sum(c["summary"][m]["best_rel_excess"] <= REL_TOL_BEST for c in configs)),
            median_of_median_rel_excess=float(np.median([c["summary"][m]["median_rel_excess"] for c in configs])),
            max_best_rel_excess=float(max(c["summary"][m]["best_rel_excess"] for c in configs)),
            mean_frac_reaching_best=float(np.mean([c["summary"][m]["frac_reaching_best"] for c in configs])),
        )
    agg["distinguishable_configs"] = int(sum(c["distinguishable"] for c in configs))
    agg["relax_better_configs"] = int(sum(c["relax_minus_lloydrelax_rel"] < -REL_TOL_BEST for c in configs))
    agg["lloydrelax_better_configs"] = int(sum(c["relax_minus_lloydrelax_rel"] > REL_TOL_BEST for c in configs))
    agg["max_abs_relax_minus_lloydrelax_rel"] = float(max(abs(c["relax_minus_lloydrelax_rel"]) for c in configs))
    agg["ari_relax_vs_lloydrelax_min"] = float(min(c["ari_best_relax_vs_lloydrelax"] for c in configs))
    agg["ari_relax_vs_lloydrelax_equal_one"] = int(sum(c["ari_best_relax_vs_lloydrelax"] > 1 - 1e-12 for c in configs))
    agg["direct_check_max_rel_err"] = float(max(c["direct_check_rel_err"] for c in configs))
    res = dict(meta=dict(seed=SEED, fast=FAST, R=R, R_anneal=R_ANNEAL, anneal_sweeps=N_SWEEPS_ANNEAL,
                         rel_tol_best=REL_TOL_BEST, python=platform.python_version(), numpy=np.__version__,
                         scipy=scipy.__version__, sklearn=sklearn.__version__, seconds=time.time() - t_start),
               aggregate=agg, configs=configs)
    with open(os.path.join(RES, "results_relaxation.json"), "w") as fh:
        json.dump(res, fh, indent=1, default=float)
    L = ["# E3 tables (generated by experiments/relaxation.py)", "",
         f"seed = {SEED}; fast = {FAST}; R = {R} per init type; anneal R = {R_ANNEAL}; runtime = {res['meta']['seconds']:.1f} s", "",
         "Per configuration: best relative excess energy over E* (best found by any method) / fraction of restarts reaching E* (rel. 1e-6).", "",
         "| dataset | potential | E* | relax | lloyd+relax | lloyd | anneal | Voronoi-stable (relax, anneal) | single-move-stable (lloyd) | ARI relax vs lloyd+relax | ARI best vs truth |",
         "|---|---|---|---|---|---|---|---|---|---|---|"]
    for c in configs:
        s = c["summary"]
        f = lambda m: f"{s[m]['best_rel_excess']:.1e} / {s[m]['frac_reaching_best']:.2f}"
        L.append(f"| {c['dataset']} | {c['potential']} | {c['E_best']:.6g} | {f('relax')} | {f('lloyd+relax')} | {f('lloyd')} | {f('anneal')} | "
                 f"{s['relax']['frac_voronoi_stable']:.2f}, {s['anneal']['frac_voronoi_stable']:.2f} | {s['lloyd']['frac_hartigan_stable']:.2f} | "
                 f"{c['ari_best_relax_vs_lloydrelax']:.3f} | {s['relax']['ari_best_vs_truth']:.2f} |")
    L += ["", "## Aggregate", ""]
    for m in ("lloyd", "lloyd+relax", "relax", "anneal"):
        a = agg[m]
        L.append(f"- {m}: {a['n_runs']} runs; Voronoi-stable {a['n_voronoi_stable']}/{a['n_runs']}; single-move-stable {a['n_hartigan_stable']}/{a['n_runs']}; "
                 f"reaches E* in {a['configs_reaching_best']}/{a['configs']} configurations; median rel. excess {a['median_of_median_rel_excess']:.2e}; "
                 f"max best rel. excess {a['max_best_rel_excess']:.2e}")
    L.append(f"- distinguishable configurations (|E*_relax - E*_lloyd+relax| > 1e-6 rel.): {agg['distinguishable_configs']}/{len(configs)} "
             f"(relax better: {agg['relax_better_configs']}, lloyd+relax better: {agg['lloydrelax_better_configs']}, max |diff| {agg['max_abs_relax_minus_lloydrelax_rel']:.2e})")
    L.append(f"- ARI(best relax, best lloyd+relax) = 1 in {agg['ari_relax_vs_lloydrelax_equal_one']}/{len(configs)} configurations (min {agg['ari_relax_vs_lloydrelax_min']:.3f})")
    L.append(f"- spring-by-spring recomputation of the best energies: max rel. err {agg['direct_check_max_rel_err']:.1e}")
    with open(os.path.join(RES, "tables_relaxation.md"), "w") as fh:
        fh.write("\n".join(L) + "\n")
    print(f"done in {res['meta']['seconds']:.1f} s")


if __name__ == "__main__":
    main()
