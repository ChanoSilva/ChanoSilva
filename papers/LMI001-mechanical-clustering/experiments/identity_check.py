#!/usr/bin/env python3
"""E1, E2 and E4 for LMI001: the mechanical energies coincide with kernel
objectives (E1), the mechanical and the kernel implementation of the same
relaxation produce identical trajectories (E2), and exact-arithmetic
non-representability of the ingredients that leave the family (E4).

Predefined criteria (written before the runs):
  E1  For every tested partition and every potential,
        | E_direct - ( J_K/2 + (n-k)(phi(0)-sigma)/2 ) | <= 1e-9 * max(1, |E_direct|)
      for K in { -phi(D), -phi(D)+sigma I, and the dataset-independent kernel
      K~ of Theorem 3.4(f) (indefinite for the rest-length potential) }.
      Pass = 100 % of checks. The partitions tested per configuration are
      random ones, the output of Lloyd and of the single-move relaxation on
      the canonical kernel K~ (minimally shifted if indefinite), and the
      ground-truth labels when they have k classes.
      In addition, for Hooke springs the per-particle energy equals the k-means
      SSE to the same tolerance, and the total (w=1) energy differs from the
      per-particle one by the factor n/k exactly when all clusters have equal
      size (checked on equal-size partitions) and otherwise by a ratio that is
      not constant across partitions (reported).
  E2  Brute-force spring relaxation and kernel single-move descent, started
      from the same labels with the same sweep order, must produce identical
      label vectors after every sweep and equal final energies to 1e-9
      relative, in 100 % of runs. For Hooke springs, alternating equilibration
      of hub-anchored springs must reproduce scikit-learn's Lloyd k-means
      (identical labels, inertia equal to the spring energy) in 100 % of runs.
  E4  With exact rational arithmetic on two 7-point integer configurations
      (drawn from a dedicated generator, default_rng(SEED + 2), so that they do
      not depend on --fast or on the state left by E1-E2) and k = 2: an energy
      is "representable" in the pairwise family with normalisation w if it
      equals sum_c w(|C_c|) sum_{i<j in C_c} A_ij + const for some symmetric A.
      Representable iff the exact least-squares residual is zero. Expected:
      fixed pair potentials representable under their own w; cross-
      normalisation, the cluster-mean rest length, the triangle-area
      three-body term and the per-spring average not (Theorem 4.1).
"""
from __future__ import annotations

import itertools
import json
import os
import platform
import sys
import time
from fractions import Fraction

import numpy as np
import scipy
import sklearn
from scipy.spatial.distance import pdist, squareform
from sklearn.cluster import KMeans

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import mechanical as M  # noqa: E402

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
RES = os.path.join(ROOT, "results")
os.makedirs(RES, exist_ok=True)

FAST = "--fast" in sys.argv
SEED = M.MASTER_SEED
TOL = 1e-9


def rel_err(a, b):
    return abs(a - b) / max(1.0, abs(a))


# --------------------------------------------------------------------------- #
# E1: identity of energies and kernel objectives
# --------------------------------------------------------------------------- #
def run_e1(datasets, rng):
    n_random = 50 if FAST else 200
    rows = []
    checks = 0
    failures = 0
    worst = 0.0
    hooke_sse_worst = 0.0
    total_vs_specific = []
    cnd_eigs = []
    for dname, (X, y, k) in datasets.items():
        sc = M.data_scales(X)
        pots = M.make_potentials(sc["ell"], sc["rest"])
        for pname, pot in pots.items():
            Xl = M.lifted_coordinates(X, pname, sc["lift_scale"])
            D = squareform(pdist(Xl))
            n = len(Xl)
            K = M.kernel_from_potential(D, pot)
            sigma, lam_min = M.psd_shift(K)
            Ks = K + sigma * np.eye(n)
            Kc = M.cnd_kernel(Xl, D, pot)
            lam_c = np.linalg.eigvalsh(Kc)
            cnd_eigs.append(dict(dataset=dname, potential=pname, cnd_label=pot.cnd,
                                 lam_min_K=lam_min, lam_min_cnd_kernel=float(lam_min_c := lam_c[0]),
                                 lam_max_cnd_kernel=float(lam_c[-1]),
                                 cnd_kernel_psd=bool(lam_min_c >= -1e-9 * max(1.0, lam_c[-1]))))
            # partitions: random ones, plus the outputs of Lloyd and of the relaxation on the
            # canonical kernel K~ (shifted minimally only if indefinite, as in E3), and the ground truth
            if lam_min_c >= -1e-9 * max(1.0, lam_c[-1]):
                Kopt = Kc
            else:
                Kopt = Kc + (-lam_min_c + 1e-9 * max(1.0, lam_c[-1])) * np.eye(n)
            parts = [M.random_partition(rng, n, k) for _ in range(n_random)]
            st = M.KKMState(Kopt, M.kmeanspp_labels(Kopt, k, rng), k)
            st.lloyd()
            parts.append(st.labels.copy())
            st.hartigan(rng)
            parts.append(st.labels.copy())
            if len(np.unique(y)) == k:
                parts.append(np.unique(y, return_inverse=True)[1])
            w_max = 0.0
            for lab in parts:
                kk = len(np.unique(lab))
                E = M.energy_direct(D, lab, pot, "per_particle")
                pred = 0.5 * M.kernel_objective(K, lab) + M.theorem_constant(n, kk, pot)
                pred_s = 0.5 * M.kernel_objective(Ks, lab) + M.theorem_constant(n, kk, pot, sigma)
                pred_c = 0.5 * M.kernel_objective(Kc, lab) + M.theorem_constant(n, kk, pot)
                for p in (pred, pred_s, pred_c):
                    e = rel_err(E, p)
                    checks += 1
                    failures += e > TOL
                    w_max = max(w_max, e)
                if pname == "hooke":
                    e = rel_err(E, M.sse(Xl, lab))
                    checks += 1
                    failures += e > TOL
                    hooke_sse_worst = max(hooke_sse_worst, e)
                Et = M.energy_direct(D, lab, pot, "total")
                total_vs_specific.append(Et / E if E > 0 else np.nan)
            worst = max(worst, w_max)
            rows.append(dict(dataset=dname, potential=pname, n=n, k=k, partitions=len(parts),
                             max_rel_err=w_max, sigma=sigma, lam_min_K=lam_min))
            print(f"E1 {dname:8s} {pname:11s} partitions={len(parts):4d} max rel err={w_max:.2e} "
                  f"lam_min(K)={lam_min:.3g}")
    # equal-size check of the n/k factor on blobs (n = 300, k = 3)
    X, y, k = datasets["blobs"]
    sc = M.data_scales(X)
    pot = M.make_potentials(sc["ell"], sc["rest"])["hooke"]
    D = squareform(pdist(X))
    n = len(X)
    eq_worst = 0.0
    for _ in range(20):
        lab = rng.permutation(np.repeat(np.arange(k), n // k))
        Et = M.energy_direct(D, lab, pot, "total")
        Es = M.energy_direct(D, lab, pot, "per_particle")
        eq_worst = max(eq_worst, rel_err(Et, (n / k) * Es))
    ratios = np.array([r for r in total_vs_specific if np.isfinite(r)])
    return dict(rows=rows, checks=checks, failures=failures, max_rel_err=worst,
                hooke_sse_max_rel_err=hooke_sse_worst, equal_size_factor_max_rel_err=eq_worst,
                total_over_specific_ratio_min=float(ratios.min()),
                total_over_specific_ratio_max=float(ratios.max()),
                cnd_eigs=cnd_eigs, n_random_partitions=n_random)


# --------------------------------------------------------------------------- #
# E2: same optimiser, same initialisation -> same trajectory
# --------------------------------------------------------------------------- #
def run_e2(datasets, rng):
    n_sub = 80 if FAST else 120
    n_inits = 2 if FAST else 3
    rows = []
    runs = 0
    identical = 0
    worst_E = 0.0
    for dname, (X, y, k) in datasets.items():
        idx = rng.permutation(len(X))[:n_sub]
        Xs = X[idx]
        sc = M.data_scales(Xs)
        pots = M.make_potentials(sc["ell"], sc["rest"])
        for pname, pot in pots.items():
            Xl = M.lifted_coordinates(Xs, pname, sc["lift_scale"])
            D = squareform(pdist(Xl))
            n = len(Xl)
            K = M.kernel_from_potential(D, pot)
            for r in range(n_inits):
                lab0 = M.random_partition(rng, n, k)
                seed_run = int(rng.integers(2 ** 31))
                scale = max(1.0, abs(M.energy_direct(D, lab0, pot)))
                rec_phys = []
                t0 = time.time()
                lab_p, E_p, sw_p = M.hartigan_bruteforce(D, pot, lab0, k, np.random.default_rng(seed_run),
                                                         record=rec_phys, scale=scale)
                t_phys = time.time() - t0
                t0 = time.time()
                st, rec_k, sw_k = M.hartigan_kernel_traced(K, lab0, k, np.random.default_rng(seed_run),
                                                           scale=scale)
                t_kern = time.time() - t0
                E_k = 0.5 * st.objective() + M.theorem_constant(n, k, pot)
                same = (sw_p == sw_k) and all(np.array_equal(a, b) for a, b in zip(rec_phys, rec_k))
                e = rel_err(E_p, E_k)
                worst_E = max(worst_E, e)
                runs += 1
                identical += bool(same and e <= TOL)
                rows.append(dict(dataset=dname, potential=pname, init=r, n=n, k=k, sweeps=sw_p,
                                 identical_trajectory=bool(same), rel_err_energy=e,
                                 seconds_physics=t_phys, seconds_kernel=t_kern))
            print(f"E2 {dname:8s} {pname:11s} identical={sum(r['identical_trajectory'] for r in rows[-n_inits:])}/{n_inits}")
    # Hooke springs anchored at hubs, equilibrated alternately == Lloyd's k-means (sklearn)
    anchored = []
    for dname, (X, y, k) in datasets.items():
        D = squareform(pdist(X))
        pot = M.make_potentials(1.0, 0.0)["hooke"]
        K = M.kernel_from_potential(D, pot)
        n = len(X)
        for r in range(n_inits):
            lab0 = M.random_partition(rng, n, k)
            C0 = np.vstack([X[lab0 == c].mean(0) for c in range(k)])
            km = KMeans(n_clusters=k, init=C0, n_init=1, tol=0.0, max_iter=1000, algorithm="lloyd").fit(X)
            # mechanical side: hubs at the equilibrium of their springs (centroids), particles
            # re-attached to the hub of least spring energy, repeated to a fixed point
            lab = M.KKMState(K, lab0, k)
            lab.lloyd()
            E_spring = M.energy_direct(D, lab.labels, pot, "per_particle")
            same = np.array_equal(km.labels_, lab.labels) or (
                len(np.unique(km.labels_)) == k and
                abs(M.sse(X, km.labels_) - E_spring) <= TOL * max(1.0, E_spring) and
                np.array_equal(np.unique(km.labels_, return_inverse=True)[1],
                               np.unique(lab.labels, return_inverse=True)[1]))
            anchored.append(dict(dataset=dname, init=r, identical_labels=bool(same),
                                 rel_err_inertia=rel_err(km.inertia_, E_spring),
                                 sklearn_iter=int(km.n_iter_)))
    print(f"E2 anchored Hooke vs sklearn Lloyd: identical={sum(a['identical_labels'] for a in anchored)}/{len(anchored)}")
    return dict(rows=rows, runs=runs, identical=identical, max_rel_err_energy=worst_E, n_sub=n_sub,
                anchored=anchored, anchored_identical=sum(a["identical_labels"] for a in anchored),
                anchored_runs=len(anchored),
                anchored_max_rel_err_inertia=max(a["rel_err_inertia"] for a in anchored))


# --------------------------------------------------------------------------- #
# E4: exact-arithmetic representability in the pairwise family
# --------------------------------------------------------------------------- #
def frac_lstsq_residual(A, b):
    """Exact least squares over Q: solve the normal equations by Gaussian elimination
    (with a rank-revealing pivot) and return (residual vector, rank)."""
    m, p = len(A), len(A[0])
    AtA = [[sum(A[r][i] * A[r][j] for r in range(m)) for j in range(p)] for i in range(p)]
    Atb = [sum(A[r][i] * b[r] for r in range(m)) for i in range(p)]
    # augmented elimination
    aug = [AtA[i] + [Atb[i]] for i in range(p)]
    piv_cols = []
    row = 0
    for col in range(p):
        pr = next((r for r in range(row, p) if aug[r][col] != 0), None)
        if pr is None:
            continue
        aug[row], aug[pr] = aug[pr], aug[row]
        pv = aug[row][col]
        aug[row] = [v / pv for v in aug[row]]
        for r in range(p):
            if r != row and aug[r][col] != 0:
                f = aug[r][col]
                aug[r] = [vr - f * vrow for vr, vrow in zip(aug[r], aug[row])]
        piv_cols.append(col)
        row += 1
        if row == p:
            break
    x = [Fraction(0)] * p
    for r, col in enumerate(piv_cols):
        x[col] = aug[r][p]
    resid = [b[r] - sum(A[r][j] * x[j] for j in range(p)) for r in range(m)]
    return resid, len(piv_cols)


def run_e4(n_configs=2):
    """Exact representability test on n_configs configurations drawn from a dedicated
    generator (independent of --fast and of the generator state after E1-E2)."""
    rng = np.random.default_rng(SEED + 2)
    out = dict(seed=SEED + 2, n=7, k=2, configs=[])
    for _ in range(n_configs):
        out["configs"].append(e4_one_configuration(rng))
    first = out["configs"][0]
    out.update(points=first["points"], partitions=first["partitions"], unknowns=first["unknowns"],
               results=first["results"])
    # agreement of the yes/no pattern across configurations, cell by cell
    pattern = [[r["representable"] for r in c["results"]] for c in out["configs"]]
    out["cells"] = len(pattern[0])
    out["cells_same_pattern"] = sum(len(set(col)) == 1 for col in zip(*pattern))
    return out


def e4_one_configuration(rng):
    n, k = 7, 2
    pts = [(Fraction(int(a)), Fraction(int(b))) for a, b in rng.integers(0, 11, size=(n, 2))]
    while len(set(pts)) < n:
        pts = [(Fraction(int(a)), Fraction(int(b))) for a, b in rng.integers(0, 11, size=(n, 2))]
    d2 = [[(pts[i][0] - pts[j][0]) ** 2 + (pts[i][1] - pts[j][1]) ** 2 for j in range(n)] for i in range(n)]
    rho_fixed = sum(d2[i][j] for i in range(n) for j in range(i + 1, n)) / Fraction(n * (n - 1) // 2)
    # all partitions into two non-empty blocks (point 0 in block 0)
    partitions = []
    for bits in itertools.product([0, 1], repeat=n - 1):
        lab = (0,) + bits
        if 1 in lab:
            partitions.append(lab)
    pairs = [(i, j) for i in range(n) for j in range(i + 1, n)]

    def blocks(lab):
        return [[i for i in range(n) if lab[i] == c] for c in range(k)]

    def design(w):
        rows = []
        for lab in partitions:
            row = []
            size = {c: lab.count(c) for c in range(k)}
            for (i, j) in pairs:
                if lab[i] == lab[j]:
                    m = size[lab[i]]
                    row.append(Fraction(1) if w == "total" else Fraction(1, m))
                else:
                    row.append(Fraction(0))
            row.append(Fraction(1))  # additive constant
            rows.append(row)
        return rows

    def e_pairwise(lab, w, pot):
        E = Fraction(0)
        for B in blocks(lab):
            m = len(B)
            if m < 2:
                continue
            s = sum(pot(d2[i][j]) for a, i in enumerate(B) for j in B[a + 1:])
            E += s if w == "total" else s / m
        return E

    def e_adaptive(lab):
        E = Fraction(0)
        for B in blocks(lab):
            m = len(B)
            if m < 2:
                continue
            ds = [d2[i][j] for a, i in enumerate(B) for j in B[a + 1:]]
            rho = sum(ds) / len(ds)
            E += sum((s - rho) ** 2 for s in ds) / m
        return E

    def e_threebody(lab):
        E = Fraction(0)
        for B in blocks(lab):
            m = len(B)
            if m < 3:
                continue
            s = Fraction(0)
            for i, j, l in itertools.combinations(B, 3):
                det = (pts[j][0] - pts[i][0]) * (pts[l][1] - pts[i][1]) - (pts[j][1] - pts[i][1]) * (pts[l][0] - pts[i][0])
                s += det ** 2
            E += s / m
        return E

    def e_perspring(lab):
        E = Fraction(0)
        for B in blocks(lab):
            m = len(B)
            if m < 2:
                continue
            s = sum(d2[i][j] for a, i in enumerate(B) for j in B[a + 1:])
            E += s / Fraction(m * (m - 1) // 2)
        return E

    energies = {
        "hooke_specific": lambda lab: e_pairwise(lab, "per_particle", lambda s: s),
        "hooke_total": lambda lab: e_pairwise(lab, "total", lambda s: s),
        "rest_fixed_specific": lambda lab: e_pairwise(lab, "per_particle", lambda s: (s - rho_fixed) ** 2),
        "rest_adaptive_specific": e_adaptive,
        "threebody_specific": e_threebody,
        "hooke_per_spring": e_perspring,
    }
    out = dict(n=n, k=k, points=[[int(a), int(b)] for a, b in pts], partitions=len(partitions),
               unknowns=len(pairs) + 1, results=[])
    for ename, ef in energies.items():
        b = [ef(lab) for lab in partitions]
        for w in ("per_particle", "total"):
            A = design(w)
            resid, rank = frac_lstsq_residual(A, b)
            r2 = sum(r * r for r in resid)
            b2 = sum(v * v for v in b)
            out["results"].append(dict(energy=ename, family_w=w, rank=rank,
                                       residual_norm2_exact=str(r2), representable=bool(r2 == 0),
                                       relative_residual=float((r2 / b2) ** Fraction(1, 2)) if b2 > 0 else 0.0))
            print(f"E4 {ename:24s} w={w:12s} rank={rank:2d} representable={r2 == 0} rel.resid={float((r2 / b2) ** 0.5) if b2 > 0 else 0:.3g}")
    return out


def main():
    t_start = time.time()
    rng = np.random.default_rng(SEED)
    datasets = M.load_datasets(SEED, n_synthetic=150 if FAST else 300, n_digits=150 if FAST else 300)
    res = dict(meta=dict(seed=SEED, fast=FAST, python=platform.python_version(), numpy=np.__version__,
                         scipy=scipy.__version__, sklearn=sklearn.__version__,
                         datasets={d: dict(n=len(v[0]), k=v[2], dim=v[0].shape[1]) for d, v in datasets.items()}))
    res["E1"] = run_e1(datasets, rng)
    res["E2"] = run_e2(datasets, rng)
    res["E4"] = run_e4()
    res["meta"]["seconds"] = time.time() - t_start
    with open(os.path.join(RES, "results_identity.json"), "w") as fh:
        json.dump(res, fh, indent=1, default=float)
    # Markdown summary
    L = ["# E1, E2, E4 (generated by experiments/identity_check.py)", "",
         f"seed = {SEED}; fast = {FAST}; runtime = {res['meta']['seconds']:.1f} s", "",
         f"## E1: identity checks: {res['E1']['checks'] - res['E1']['failures']}/{res['E1']['checks']} passed, "
         f"max relative error {res['E1']['max_rel_err']:.2e}; Hooke vs SSE max rel err {res['E1']['hooke_sse_max_rel_err']:.2e}; "
         f"total/specific ratio range [{res['E1']['total_over_specific_ratio_min']:.2f}, {res['E1']['total_over_specific_ratio_max']:.2f}]", "",
         "| dataset | potential | n | k | partitions | max rel err | sigma | lam_min(K) |", "|---|---|---|---|---|---|---|---|"]
    for r in res["E1"]["rows"]:
        L.append(f"| {r['dataset']} | {r['potential']} | {r['n']} | {r['k']} | {r['partitions']} | {r['max_rel_err']:.1e} | {r['sigma']:.3g} | {r['lam_min_K']:.3g} |")
    L += ["", "| dataset | potential | negative-type label | lam_min of the Theorem-3.2(f) kernel | lam_max | PSD |", "|---|---|---|---|---|---|"]
    for r in res["E1"]["cnd_eigs"]:
        L.append(f"| {r['dataset']} | {r['potential']} | {r['cnd_label']} | {r['lam_min_cnd_kernel']:.3g} | {r['lam_max_cnd_kernel']:.3g} | {r['cnd_kernel_psd']} |")
    L += ["", f"## E2: identical trajectories {res['E2']['identical']}/{res['E2']['runs']}, max rel err of final energy {res['E2']['max_rel_err_energy']:.2e}; "
          f"anchored Hooke vs sklearn Lloyd identical {res['E2']['anchored_identical']}/{res['E2']['anchored_runs']}", "",
          "| dataset | potential | init | sweeps | identical | rel err E | s (physics) | s (kernel) |", "|---|---|---|---|---|---|---|---|"]
    for r in res["E2"]["rows"]:
        L.append(f"| {r['dataset']} | {r['potential']} | {r['init']} | {r['sweeps']} | {r['identical_trajectory']} | {r['rel_err_energy']:.1e} | {r['seconds_physics']:.2f} | {r['seconds_kernel']:.3f} |")
    L += ["", f"## E4: exact representability, n={res['E4']['n']}, k={res['E4']['k']}, {res['E4']['partitions']} partitions, "
          f"{res['E4']['unknowns']} unknowns, {len(res['E4']['configs'])} configurations (seed {res['E4']['seed']}); "
          f"yes/no pattern identical across configurations in {res['E4']['cells_same_pattern']}/{res['E4']['cells']} cells"]
    for ci, cfg in enumerate(res["E4"]["configs"], 1):
        L += ["", f"### Configuration P{ci}: points {cfg['points']}", "",
              "| energy | family w | rank | representable | relative residual |", "|---|---|---|---|---|"]
        for r in cfg["results"]:
            L.append(f"| {r['energy']} | {r['family_w']} | {r['rank']} | {r['representable']} | {r['relative_residual']:.3g} |")
    with open(os.path.join(RES, "tables_identity.md"), "w") as fh:
        fh.write("\n".join(L) + "\n")
    print(f"done in {res['meta']['seconds']:.1f} s")


if __name__ == "__main__":
    main()
