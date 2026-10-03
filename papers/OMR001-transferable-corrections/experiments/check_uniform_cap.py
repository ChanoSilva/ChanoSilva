#!/usr/bin/env python3
"""Independent numerical checks of Corollary 4.3 (uniform cap) and Proposition 4.5(b) (v0.3).

(1) Pointwise inequality behind Corollary 4.3, in its sharp form (referee round 2, M2):
    for every a = ||C-R|| > 0, e = ||R-theta|| >= 0 and every Delta in [a^2 - 2ae, a^2 + 2ae]
    (the full range allowed by Cauchy--Schwarz), with s = 2 sigma a / sqrt(m),
        Delta^+ Phi(-(Delta + z s)/s) <= (4 sigma e / sqrt m) kappa + (4 sigma^2 / m) kappa2,
    kappa = sup_u u Phi(-(z+u)),  kappa2 = sup_u u^2 Phi(-(z+u)).
    Also checks the closed form kappa <= phi(z), kappa2 <= phi(1) and the old phi-form.
(2) The fixed-n_e construction of Proposition 4.5(b) (referee round 2, M1):
    C = theta0 - (1+t)(R-theta0), t = 2 sigma u*/(sqrt(m) ||R-theta0||), evaluated at theta = theta0.
    Monte Carlo excess risk (held-out draws simulated, not Rao--Blackwellised) against
    (4 sigma/sqrt m) kappa E||R-theta|| + (4 sigma^2/m) u* kappa  (exact value) and the cap.
Runs in a few seconds; seed fixed.  Not used by make_numbers.py (the manuscript quotes only the
analytic values, which safe_reversion.py computes); this script is an independent check.
"""
import numpy as np
from scipy.optimize import minimize_scalar
from scipy.special import gammaln
from scipy.stats import norm

sigma = 1.0


def kap(alpha, p):
    z = norm.ppf(1 - alpha)
    r = minimize_scalar(lambda u: -(u ** p) * norm.cdf(-(z + u)), bounds=(0, 30), method="bounded",
                        options={"xatol": 1e-12})
    return float(-r.fun), float(r.x)


print("== (1) pointwise inequality, sharp constants (ratio must be <= 1; e = 0 row attains 1)")
a = np.exp(np.linspace(np.log(1e-3), np.log(1e3), 200))[:, None, None]
e = np.concatenate([[0.0], np.exp(np.linspace(np.log(1e-4), np.log(50), 120))])[None, :, None]
t = np.linspace(-1, 1, 81)[None, None, :]
worst_sharp = worst_phi = 0.0
for m in (1, 3, 12, 100):
    for alpha in (0.5, 0.2, 0.1, 0.05, 0.01):
        z = norm.ppf(1 - alpha)
        k1, _ = kap(alpha, 1); k2, _ = kap(alpha, 2)
        assert k1 <= norm.pdf(z) + 1e-12 and k2 <= norm.pdf(1.0) + 1e-12
        Delta = a ** 2 + 2 * a * e * t
        s = 2 * sigma * a / np.sqrt(m)
        lhs = np.maximum(Delta, 0) * norm.cdf(-(Delta + z * s) / s)
        rhs_sharp = (4 * sigma * e / np.sqrt(m)) * k1 + (4 * sigma ** 2 / m) * k2
        rhs_phi = (4 * sigma * e / np.sqrt(m)) * norm.pdf(z) + (4 * sigma ** 2 / m) * norm.pdf(1.0)
        rs, rp = float((lhs / rhs_sharp).max()), float((lhs / rhs_phi).max())
        r0 = float((lhs[:, 0, :] / rhs_sharp[:, 0, :]).max())
        worst_sharp, worst_phi = max(worst_sharp, rs), max(worst_phi, rp)
        print(f"m={m:4d} alpha={alpha:5.2f} kappa={k1:.4f} kappa2={k2:.4f}  max ratio sharp={rs:.4f} "
              f"(e=0: {r0:.4f})  phi-form={rp:.4f}")
print(f"overall max ratio, sharp form: {worst_sharp:.4f};  phi form: {worst_phi:.4f}")

print("== (2) fixed-n_e construction of Proposition 4.5(b), Monte Carlo vs exact value")
rng = np.random.default_rng(20261003)
N = 400_000
for d, n_e in ((5, 48), (1, 48), (20, 200)):
    c_d = np.sqrt(2) * np.exp(gammaln((d + 1) / 2) - gammaln(d / 2))   # E||Z||, Z ~ N(0, I_d)
    Ee = sigma * c_d / np.sqrt(n_e)
    for m in (3, 12, 48):
        for alpha in (0.5, 0.1, 0.01):
            z = norm.ppf(1 - alpha)
            k1, ustar = kap(alpha, 1); k2, _ = kap(alpha, 2)
            theta0 = np.zeros(d)
            R = theta0 + sigma / np.sqrt(n_e) * rng.standard_normal((N, d))
            nr = np.linalg.norm(R - theta0, axis=1)
            tt = 2 * sigma * ustar / (np.sqrt(m) * nr)
            C = theta0 - (1 + tt)[:, None] * (R - theta0)
            Yb = theta0 + sigma / np.sqrt(m) * rng.standard_normal((N, d))
            Dhat = ((C - Yb) ** 2).sum(1) - ((R - Yb) ** 2).sum(1)
            s = 2 * sigma * np.linalg.norm(C - R, axis=1) / np.sqrt(m)
            Delta = ((C - theta0) ** 2).sum(1) - ((R - theta0) ** 2).sum(1)
            acc = Dhat <= -z * s
            ex = Delta * acc
            exact = (4 * sigma / np.sqrt(m)) * k1 * Ee + (4 * sigma ** 2 / m) * ustar * k1
            cap = (4 * sigma / np.sqrt(m)) * k1 * Ee + (4 * sigma ** 2 / m) * k2
            print(f"d={d:2d} n_e={n_e:3d} m={m:2d} alpha={alpha:4}: MC excess={ex.mean():.5f} +- {ex.std(ddof=1)/np.sqrt(N):.5f}"
                  f"  exact={exact:.5f}  cap(exact E|e|)={cap:.5f}  ratio exact/cap={exact/cap:.3f}"
                  f"  excess*sqrt(m)={exact*np.sqrt(m):.4f}")
