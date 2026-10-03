"""Linear-programming check of Proposition 4.3(b) (manuscript v0.5; added in round 3 of internal review).

Claim: for 2 <= k <= n-2, A symmetric with A_ij >= 0 off the diagonal, every
omega in (0,inf)^n, every symmetric K and every constant c,
    max_C |E_tot(C) - J^omega_K(C) - c| >= 1/2 * min_{i != j} A_ij.
Size-weight version (3 <= k <= n-2 or (n,k)=(4,2), w(3) >= w(2), w(3) > 0):
    max_C |F^w_A(C) - J^omega_K(C) - c| >= 1/2 * w(3) * min_{i != j} A_ij.
The uniform distance from b to span(G) is computed by an LP (HiGHS).
Written from scratch; imports nothing from the paper's code or theory/.
Output: results/check_bound_prop43.txt (python3 experiments/check_bound_prop43.py > results/check_bound_prop43.txt).
The bound is proved in Appendix B; this script only checks it on random and degenerate weights.
"""
import itertools, time
import numpy as np
from scipy.optimize import linprog

t0 = time.process_time()
rng = np.random.default_rng(20261003)


def partitions(n, k):
    """All partitions of range(n) into exactly k non-empty blocks (restricted growth strings)."""
    out = []
    def rec(i, lab, m):
        if i == n:
            if m == k:
                out.append(list(lab))
            return
        for c in range(min(m + 1, k)):
            if n - i - 1 < k - max(m, c + 1):
                continue
            lab.append(c); rec(i + 1, lab, max(m, c + 1)); lab.pop()
    rec(0, [], 0)
    return [[[i for i in range(n) if l[i] == c] for c in range(k)] for l in out]


def J(K, om, P):
    v = float(np.sum(om * np.diag(K)))
    for B in P:
        o = om[B]
        v -= o @ K[np.ix_(B, B)] @ o / o.sum()
    return v


def F(A, w, P):
    return sum(w(len(B)) * sum(A[i, j] for i, j in itertools.combinations(B, 2)) for B in P)


def design(n, om, parts):
    cols = []
    for a in range(n):
        for b in range(a, n):
            K = np.zeros((n, n)); K[a, b] += 1; K[b, a] += 1 if a != b else 0
            cols.append([J(K, om, P) for P in parts])
    cols.append([1.0] * len(parts))
    G = np.array(cols).T
    return G / np.maximum(np.abs(G).max(axis=0), 1e-300)


def unif_dist(G, b):
    m = G.shape[1]
    c = np.zeros(m + 1); c[-1] = 1
    Aub = np.block([[G, -np.ones((len(b), 1))], [-G, -np.ones((len(b), 1))]])
    bub = np.concatenate([b, -b])
    r = linprog(c, A_ub=Aub, b_ub=bub, bounds=[(None, None)] * m + [(0, None)], method="highs")
    assert r.status == 0, r.message
    return r.x[-1]


def spring(n, d, phi):
    X = rng.normal(size=(n, d))
    D = np.linalg.norm(X[:, None] - X[None], axis=2)
    A = phi(D); np.fill_diagonal(A, phi(0.0))
    return A


def omegas(n, nrand=40):
    """Random and deliberately degenerate point weights (log-omega within +-6)."""
    L = [np.ones(n)]
    for _ in range(nrand):
        L.append(np.exp(rng.uniform(-6, 6, n)))
    for s in (1e-2, 1e-4):
        for idx in itertools.combinations(range(n), 2):
            o = np.ones(n); o[list(idx)] = s; L.append(o)
            o = np.ones(n); o[list(idx)] = 1 / s; L.append(o)
    return L

PHIS = {"hooke": lambda d: d ** 2, "string": lambda d: d, "rest": lambda d: (d - 0.5) ** 2,
        "uniform": lambda d: np.where(d > 0, 1.0, 0.0)}

print("== Part 1: E_tot, dense A, min over omega of uniform distance / (1/2 min A) ==")
worst = np.inf
for n, k in [(4, 2), (5, 2), (5, 3), (6, 2), (6, 3), (6, 4)]:
    parts = partitions(n, k)
    for name, phi in PHIS.items():
        A = spring(n, 2, phi)
        bound = 0.5 * min(A[i, j] for i in range(n) for j in range(n) if i != j)
        b = np.array([F(A, lambda m: 1.0, P) for P in parts])
        ratios = []
        for om in omegas(n, nrand=15 if n == 6 else 30):
            ratios.append(unif_dist(design(n, om, parts), b) / bound)
        r = min(ratios); worst = min(worst, r)
        print(f"n={n} k={k} {name:8s} #part={len(parts):3d} #omega={len(ratios):3d} min dist/bound = {r:.4f}")
print(f"worst ratio over all dense cases: {worst:.4f} (claim: >= 1)")

print("== Part 2: size weight w(2)=1, w(3)=2 (w(3)>=w(2)), bound 1/2 w(3) min A ==")
for n, k in [(5, 3), (6, 3), (4, 2)]:
    parts = partitions(n, k)
    A = spring(n, 2, PHIS["string"])
    w = lambda m: {1: 0.0, 2: 1.0, 3: 2.0, 4: 2.5}[m]
    bound = 0.5 * w(3) * min(A[i, j] for i in range(n) for j in range(n) if i != j)
    b = np.array([F(A, w, P) for P in parts])
    r = min(unif_dist(design(n, om, parts), b) / bound for om in omegas(n, nrand=20))
    print(f"n={n} k={k} min dist/bound = {r:.4f}")

print("== Part 3: a single non-zero spring, n=4, k=2: distance -> 0 as omega_3, omega_4 -> 0 ==")
parts = partitions(4, 2)
A = np.zeros((4, 4)); A[0, 1] = A[1, 0] = 1.0
b = np.array([F(A, lambda m: 1.0, P) for P in parts])
for eps in (1.0, 1e-1, 1e-2, 1e-3):
    om = np.array([1.0, 1.0, eps, eps])
    e2 = sum(om[i] * om[j] for i, j in itertools.combinations(range(4), 2))
    pred = 2 * 1.0 * om[2] * om[3] / (4 * e2)  # <nu,E>/||nu||_1, exact when the annihilator is unique
    print(f"eps={eps:g}: LP uniform distance = {unif_dist(design(4, om, parts), b):.3e}; <nu,E>/||nu||_1 = {pred:.3e}")

print("== Part 4: k = n-1 (E_tot is in G_omega; Prop. 4.2 holds trivially) ==")
for n in (4, 5, 6):
    parts = partitions(n, n - 1)
    om = np.exp(rng.uniform(-2, 2, n))
    G = design(n, om, parts)
    A = spring(n, 2, PHIS["hooke"])
    b = np.array([F(A, lambda m: 1.0, P) for P in parts])
    print(f"n={n}: #partitions={len(parts)}, rank G_omega+1 = {np.linalg.matrix_rank(G)}, "
          f"uniform distance of E_tot = {unif_dist(G, b):.2e}")

print(f"CPU {time.process_time() - t0:.1f} s")
