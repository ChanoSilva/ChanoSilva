#!/usr/bin/env python3
"""Shared library for LMI001 (mechanical analogies for data clustering).

Objects
-------
* Pair potentials phi(d) ("springs") and lifts L: R^d -> R^D.
* The mechanical family of clustering objectives
      E_w(C) = sum_c w(|C_c|) sum_{i<j in C_c} phi(||L x_i - L x_j||),
  with w = 1/m (per-particle, "specific" energy) or w = 1 (total energy).
* The kernel k-means objective in trace form
      J_K(C) = tr K - sum_c (1/|C_c|) 1_c^T K 1_c,
  and the constants of the identity  E_{1/m}(C) = J_K(C)/2 + (n-k) phi(0)/2
  for K = -phi(D) (Theorem 3.4(b) of the manuscript).
* Optimisers that only see the kernel matrix: batch Lloyd in feature space,
  single-move descent (Hartigan-type "relaxation"), Metropolis annealing.
* A brute-force "physics" implementation of the single-move relaxation that
  only sums spring energies (used to confirm the identity along trajectories).

Everything is deterministic given a numpy Generator.
"""
from __future__ import annotations

import math
import numpy as np
from scipy.spatial.distance import pdist, squareform

MASTER_SEED = 20260930


# --------------------------------------------------------------------------- #
# Potentials and lifts
# --------------------------------------------------------------------------- #
class Potential:
    """A pair potential phi(d) on distances d >= 0.

    cnd = True means that (x, y) -> phi(||x - y||) is known to be conditionally
    negative definite on every Euclidean space because phi(d) = psi(d^2) with
    psi a Bernstein function (Proposition 3.5, Theorem 3.4(f)); it is a label,
    not a computation.
    """

    def __init__(self, name, func, phi0, cnd, tex, description):
        self.name = name
        self.func = func
        self.phi0 = float(phi0)
        self.cnd = cnd
        self.tex = tex
        self.description = description

    def __call__(self, d):
        return self.func(np.asarray(d, dtype=float))


def make_potentials(ell, rest):
    """The six potentials used in the experiments, with data-derived scales."""
    return {
        "hooke": Potential("hooke", lambda d: d ** 2, 0.0, True,
                           r"$d^2$", "Hooke spring, zero rest length"),
        "hooke_lift": Potential("hooke_lift", lambda d: d ** 2, 0.0, True,
                                r"$d^2$ on the paraboloid lift",
                                "Hooke spring on the lifted configuration (x, |x|^2/s)"),
        "rest": Potential("rest", lambda d: (d - rest) ** 2, rest ** 2, False,
                          r"$(d-r)^2$", f"Hooke spring with rest length r = {rest:.4g}"),
        "tension": Potential("tension", lambda d: d, 0.0, True,
                             r"$d$", "string under constant tension (energy = length)"),
        "gauss": Potential("gauss", lambda d: 1.0 - np.exp(-d ** 2 / (2 * ell ** 2)), 0.0, True,
                           r"$1-e^{-d^2/2\ell^2}$", f"saturating (breakable) spring, ell = {ell:.4g}"),
        "log": Potential("log", lambda d: np.log1p(d ** 2 / ell ** 2), 0.0, True,
                         r"$\log(1+d^2/\ell^2)$", f"logarithmic (soft) spring, ell = {ell:.4g}"),
    }


def paraboloid_lift(X, scale):
    """L(x) = (x, ||x||^2 / scale)."""
    return np.hstack([X, (np.sum(X ** 2, axis=1) / scale)[:, None]])


def lifted_coordinates(X, pot_name, lift_scale):
    return paraboloid_lift(X, lift_scale) if pot_name == "hooke_lift" else X


def data_scales(X, rng=None):
    """Data-derived scales: ell = median distance to the 7th nearest neighbour,
    rest = 10th percentile of all pairwise distances, lift scale = median |x|^2."""
    D = squareform(pdist(X))
    n = len(X)
    kk = min(7, n - 1)
    nn7 = np.sort(D, axis=1)[:, kk]
    ell = float(np.median(nn7))
    rest = float(np.percentile(D[np.triu_indices(n, 1)], 10))
    lift_scale = float(np.median(np.sum(X ** 2, axis=1)))
    return dict(ell=ell, rest=rest, lift_scale=lift_scale)


# --------------------------------------------------------------------------- #
# Datasets
# --------------------------------------------------------------------------- #
def load_datasets(seed=MASTER_SEED, n_synthetic=300, n_digits=300):
    from sklearn.datasets import make_blobs, make_moons, make_circles, load_digits, load_iris
    from sklearn.preprocessing import StandardScaler
    rng = np.random.default_rng(seed)
    out = {}
    X, y = make_blobs(n_samples=n_synthetic, centers=3, cluster_std=0.9,
                      random_state=int(rng.integers(2 ** 31)))
    out["blobs"] = (X, y, 3)
    X, y = make_moons(n_samples=n_synthetic, noise=0.06, random_state=int(rng.integers(2 ** 31)))
    out["moons"] = (X, y, 2)
    X, y = make_circles(n_samples=n_synthetic, factor=0.45, noise=0.05,
                        random_state=int(rng.integers(2 ** 31)))
    out["circles"] = (X, y, 2)
    d = load_digits()
    idx = rng.permutation(len(d.data))[:n_digits]
    out["digits"] = (d.data[idx] / 16.0, d.target[idx], 10)
    ir = load_iris()
    out["iris"] = (StandardScaler().fit_transform(ir.data), ir.target, 3)
    return out


# --------------------------------------------------------------------------- #
# Energies and kernel objectives
# --------------------------------------------------------------------------- #
def energy_direct(D, labels, pot, w="per_particle"):
    """Mechanical energy summed spring by spring (the definition)."""
    E = 0.0
    for c in np.unique(labels):
        idx = np.flatnonzero(labels == c)
        m = len(idx)
        if m < 2:
            continue
        sub = D[np.ix_(idx, idx)]
        s = float(pot(sub[np.triu_indices(m, 1)]).sum())
        E += s / m if w == "per_particle" else s
    return E


def kernel_objective(K, labels):
    """Trace form of the kernel k-means objective, for any symmetric K."""
    J = float(np.trace(K))
    for c in np.unique(labels):
        idx = np.flatnonzero(labels == c)
        J -= float(K[np.ix_(idx, idx)].sum()) / len(idx)
    return J


def kernel_from_potential(D, pot):
    """K = -phi(D), diagonal included (K_ii = -phi(0))."""
    return -pot(D)


def psd_shift(K, margin=1e-9):
    """sigma >= 0 such that K + sigma I is positive semidefinite (numerically)."""
    lam_min = float(np.linalg.eigvalsh(K)[0])
    return max(0.0, -lam_min) + margin * max(1.0, float(np.abs(K).max())), lam_min


def cnd_kernel(Xl, D, pot):
    """Dataset-independent kernel of Theorem 3.4(f):
    K(x,y) = phi(|x|) + phi(|y|) - phi(|x-y|) - phi(0)."""
    f = pot(np.linalg.norm(Xl, axis=1))
    return f[:, None] + f[None, :] - pot(D) - pot.phi0


def theorem_constant(n, k, pot, sigma=0.0):
    """E_{1/m}(C) = J_{K + sigma I}(C)/2 + (n-k)(phi(0) - sigma)/2."""
    return 0.5 * (n - k) * (pot.phi0 - sigma)


def sse(X, labels):
    """Classical k-means objective (sum of squared distances to centroids)."""
    tot = 0.0
    for c in np.unique(labels):
        P = X[labels == c]
        tot += float(((P - P.mean(0)) ** 2).sum())
    return tot


def random_partition(rng, n, k):
    """Uniform random labels conditioned on all k clusters being non-empty."""
    while True:
        lab = rng.integers(k, size=n)
        if len(np.unique(lab)) == k:
            return lab


# --------------------------------------------------------------------------- #
# Kernel-side optimisers (see only K)
# --------------------------------------------------------------------------- #
class KKMState:
    """Incremental bookkeeping for kernel k-means with k non-empty clusters.

    S[i, c] = sum_{j in C_c} K_ij ;  Q[c] = sum_{i, j in C_c} K_ij ;  size[c] = |C_c|.
    The objective is J = tr K - sum_c Q_c / size_c, and moving point i from its
    cluster a to cluster c changes J by
        Delta J = size_c/(size_c+1) * d2(i,c) - size_a/(size_a-1) * d2(i,a),
    where d2(i,c) = K_ii - 2 S[i,c]/size_c + Q_c/size_c^2 (the squared feature
    distance to the centroid when K is PSD; an algebraic identity otherwise).
    """

    def __init__(self, K, labels, k):
        self.K = K
        self.n = len(labels)
        self.k = k
        self.diag = np.diag(K).copy()
        self.rebuild(labels)

    def rebuild(self, labels):
        self.labels = np.asarray(labels).copy()
        M = np.zeros((self.n, self.k))
        M[np.arange(self.n), self.labels] = 1.0
        self.S = self.K @ M
        self.size = M.sum(0)
        self.Q = np.einsum("ic,ic->c", self.S, M)

    def objective(self):
        return float(np.trace(self.K) - np.sum(self.Q / self.size))

    def d2_all(self):
        return self.diag[:, None] - 2.0 * self.S / self.size[None, :] + (self.Q / self.size ** 2)[None, :]

    def d2_row(self, i):
        return self.diag[i] - 2.0 * self.S[i] / self.size + self.Q / self.size ** 2

    def delta_row(self, i):
        """Delta J for moving i to each cluster (0 for its own cluster; +inf if it
        would empty a cluster)."""
        a = self.labels[i]
        na = self.size[a]
        if na <= 1:
            return None
        d2 = self.d2_row(i)
        delta = (self.size / (self.size + 1.0)) * d2 - (na / (na - 1.0)) * d2[a]
        delta[a] = 0.0
        return delta

    def move(self, i, c):
        a = self.labels[i]
        Ki = self.K[i]
        Sia, Sic, Kii = self.S[i, a], self.S[i, c], self.diag[i]
        self.S[:, a] -= Ki
        self.S[:, c] += Ki
        self.Q[a] += -2.0 * Sia + Kii
        self.Q[c] += 2.0 * Sic + Kii
        self.size[a] -= 1
        self.size[c] += 1
        self.labels[i] = c

    # ---- single-move descent ("mechanical relaxation at zero temperature") ----
    def hartigan(self, rng, tol_rel=1e-10, max_sweeps=500):
        scale = max(1.0, abs(self.objective()))
        tol = tol_rel * scale
        sweeps = 0
        moves_total = 0
        while sweeps < max_sweeps:
            sweeps += 1
            moves = 0
            for i in rng.permutation(self.n):
                delta = self.delta_row(i)
                if delta is None:
                    continue
                c = int(np.argmin(delta))
                if delta[c] < -tol:
                    self.move(i, c)
                    moves += 1
            moves_total += moves
            if moves == 0:
                break
        return sweeps, moves_total

    def is_hartigan_stable(self, tol_rel=1e-9):
        scale = max(1.0, abs(self.objective()))
        for i in range(self.n):
            delta = self.delta_row(i)
            if delta is not None and delta.min() < -tol_rel * scale:
                return False
        return True

    def is_voronoi_stable(self, tol_rel=1e-9):
        """Each point is assigned to a nearest centroid in the feature space of K."""
        d2 = self.d2_all()
        own = d2[np.arange(self.n), self.labels]
        scale = max(1.0, float(np.abs(d2).max()))
        return bool(np.all(own <= d2.min(1) + tol_rel * scale))

    # ---- batch Lloyd in feature space ----
    def lloyd(self, max_iter=300):
        it = 0
        while it < max_iter:
            it += 1
            d2 = self.d2_all()
            new = d2.argmin(1)
            # keep k non-empty clusters: refill an emptied cluster with the worst-fitted point
            counts = np.bincount(new, minlength=self.k)
            for c in np.flatnonzero(counts == 0):
                cand = np.flatnonzero(np.bincount(new, minlength=self.k)[new] > 1)
                i = cand[np.argmax(d2[cand, new[cand]])]
                new[i] = c
            if np.array_equal(new, self.labels):
                break
            self.rebuild(new)
        return it

    # ---- Metropolis sweeps at temperature T on the energy E = J/2 ----
    def metropolis_sweep(self, rng, T):
        accepted = 0
        for i in rng.permutation(self.n):
            delta = self.delta_row(i)
            if delta is None:
                continue
            a = self.labels[i]
            c = int(rng.integers(self.k - 1))
            if c >= a:
                c += 1
            dE = 0.5 * delta[c]
            if dE <= 0 or rng.random() < math.exp(-dE / T):
                self.move(i, c)
                accepted += 1
        return accepted

    def anneal(self, rng, n_sweeps=40, T_ratio=1e-3):
        # initial temperature: median |Delta E| of random single moves at the start
        samp = []
        for i in rng.permutation(self.n)[: min(self.n, 100)]:
            delta = self.delta_row(i)
            if delta is not None:
                a = self.labels[i]
                c = int(rng.integers(self.k - 1))
                c += c >= a
                samp.append(abs(0.5 * delta[c]))
        T0 = max(float(np.median(samp)), 1e-12)
        Ts = T0 * (T_ratio ** (np.arange(n_sweeps) / max(n_sweeps - 1, 1)))
        acc = 0
        for T in Ts:
            acc += self.metropolis_sweep(rng, float(T))
        sweeps, moves = self.hartigan(rng)
        return T0, acc, sweeps


def kmeanspp_labels(K, k, rng):
    """Kernel k-means++ seeding in the feature space of K, then nearest-seed labels."""
    n = len(K)
    diag = np.diag(K)
    seeds = [int(rng.integers(n))]
    d2 = diag + diag[seeds[0]] - 2 * K[:, seeds[0]]
    d2 = np.maximum(d2, 0)
    while len(seeds) < k:
        p = d2 / d2.sum() if d2.sum() > 0 else np.full(n, 1.0 / n)
        s = int(rng.choice(n, p=p))
        seeds.append(s)
        d2 = np.minimum(d2, np.maximum(diag + diag[s] - 2 * K[:, s], 0))
    Dseed = diag[:, None] + diag[seeds][None, :] - 2 * K[:, seeds]
    lab = Dseed.argmin(1)
    for c in range(k):  # guarantee non-empty clusters
        if not np.any(lab == c):
            lab[seeds[c]] = c
    return lab


# --------------------------------------------------------------------------- #
# Physics-side optimiser (sees only springs)
# --------------------------------------------------------------------------- #
def hartigan_bruteforce(D, pot, labels, k, rng, w="per_particle", tol_rel=1e-10,
                        max_sweeps=500, record=None, scale=None):
    """Single-particle relaxation that recomputes the total spring energy from
    scratch for every candidate move. Same decision rule as KKMState.hartigan
    (move to the argmin cluster if it lowers the energy by more than tol)."""
    labels = np.asarray(labels).copy()
    E = energy_direct(D, labels, pot, w)
    if scale is None:
        scale = max(1.0, abs(E))
    tol = tol_rel * scale
    sweeps = 0
    while sweeps < max_sweeps:
        sweeps += 1
        moves = 0
        for i in rng.permutation(len(labels)):
            a = labels[i]
            if np.sum(labels == a) <= 1:
                continue
            Es = np.empty(k)
            for c in range(k):
                if c == a:
                    Es[c] = E
                else:
                    trial = labels.copy()
                    trial[i] = c
                    Es[c] = energy_direct(D, trial, pot, w)
            c = int(np.argmin(Es - E))
            if Es[c] - E < -tol:
                labels[i] = c
                E = Es[c]
                moves += 1
        if record is not None:
            record.append(labels.copy())
        if moves == 0:
            break
    return labels, E, sweeps


def hartigan_kernel_traced(K, labels, k, rng, tol_rel=1e-10, max_sweeps=500, scale=None):
    """Kernel-side single-move descent recording the labels after every sweep,
    with the same sweep orders as hartigan_bruteforce for the same rng state."""
    st = KKMState(K, labels, k)
    if scale is None:
        scale = max(1.0, abs(0.5 * st.objective()))
    tol = tol_rel * scale
    rec = []
    sweeps = 0
    while sweeps < max_sweeps:
        sweeps += 1
        moves = 0
        for i in rng.permutation(st.n):
            delta = st.delta_row(i)
            if delta is None:
                continue
            c = int(np.argmin(delta))
            if 0.5 * delta[c] < -tol:
                st.move(i, c)
                moves += 1
        rec.append(st.labels.copy())
        if moves == 0:
            break
    return st, rec, sweeps
