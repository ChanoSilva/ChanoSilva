#!/usr/bin/env python3
"""Independent numerical check of Corollary 'uniform cap' (manuscript Cor. 4.3; referee round 1, M2).

For every a = ||C-R|| > 0, e = ||R-theta|| >= 0 and every Delta in [a^2 - 2ae, a^2 + 2ae]
(the full range allowed by Cauchy-Schwarz), with s = 2 sigma a / sqrt(m):
    Delta^+ Phi(-(Delta + z s)/s)  <=  (4 sigma e / sqrt m) phi(z) + (4 sigma^2 / m) phi(1).
Prints the largest ratio lhs/rhs on a log grid; it must be <= 1.  Runs in a few seconds.
"""
import numpy as np
from scipy.stats import norm

sigma = 1.0
worst = 0.0
a = np.exp(np.linspace(np.log(1e-3), np.log(1e3), 160))[:, None, None]
e = np.concatenate([[0.0], np.exp(np.linspace(np.log(1e-3), np.log(50), 80))])[None, :, None]
t = np.linspace(-1, 1, 61)[None, None, :]
for m in (3, 6, 12, 24, 100):
    for alpha in (0.5, 0.2, 0.1, 0.05, 0.01):
        z = norm.ppf(1 - alpha)
        Delta = a ** 2 + 2 * a * e * t
        s = 2 * sigma * a / np.sqrt(m)
        lhs = np.maximum(Delta, 0) * norm.cdf(-(Delta + z * s) / s)
        rhs = (4 * sigma * e / np.sqrt(m)) * norm.pdf(z) + (4 * sigma ** 2 / m) * norm.pdf(1.0)
        ratio = float((lhs / rhs).max())
        worst = max(worst, ratio)
        print(f"m={m:4d} alpha={alpha:5.2f}  max lhs/rhs = {ratio:.4f}")
print(f"overall max ratio (must be <= 1): {worst:.4f}")
x = np.linspace(0, 10, 100001)
print(f"sup_x x phi(x) = {(x * norm.pdf(x)).max():.6f}   phi(1) = {norm.pdf(1.0):.6f}")
d, n_e, m = 5, 48, 12
for alpha in (0.5, 0.2, 0.1, 0.05, 0.01):
    z = norm.ppf(1 - alpha)
    cap = 4 * (norm.pdf(z) * np.sqrt(d / (n_e * m)) + norm.pdf(1.0) / m)
    print(f"design d={d}, n_e={n_e}, m={m}, alpha={alpha}: cap = {cap:.4f}  (risk of R = {d / n_e:.4f})")
