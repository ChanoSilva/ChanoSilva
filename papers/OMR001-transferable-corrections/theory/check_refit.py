#!/usr/bin/env python3
"""OMR001 -- numerical check of theory/refit_bound.tex (refit and cross-fitted reversion).

Estimators checked (Gaussian location model of the manuscript, R = Xbar_e, any F-measurable C):
  transported refit   theta_rf = Xbar_n + A (C - R),  A = 1{Dhat <= -z_{1-alpha} s}  (level-alpha check
                      of Definition 2.1 on the m held-out points, then the correction vector C - R
                      is added to the full-data mean Xbar_n);
  cross-fitted        theta_cf = (1/K) sum_k [A_k C_k + (1 - A_k) R_k] = Xbar_n + (1/K) sum_k A_k (C_k - R_k)
                      (K = n/m folds; fold k is the held-out sample of the k-th reverting estimator).
Quantities (theory/refit_bound.tex, Theorem R and Corollary R):
  (I)   identity   E[l(theta_rf)] - E[l(Xbar_n)] = E[((1-rho)Delta + rho|w|^2) pi + rho s phi(z + Delta/s)],
        rho = m/n, w = C - R, Delta = l(C) - l(R), s = 2 sigma |w|/sqrt(m), pi = Phi(-(z + Delta/s));
  (II)  bound      <= E[s Psi_rho(rho a)] <= E[s (kbar_rho + rho a Phi(rho a - z))],  a = sqrt(m)|R-theta|/sigma;
  (III) cap        <= (sigma^2/m) E[M_rho(a)] <= closed form (uniform in theta and C);
  (IV)  cross-fit  <= average over folds of (II) / (III)   (Jensen).
Checked on (a) every configuration of experiments/safe_reversion.py (its CFG, same seed and same draws:
the script asserts that its draws reproduce sr.simulate and the 'refit' risks of results/results.json),
plus a cross-fitted run of the same design; (b) an adversarial grid of (theta, C) with >= 20 000
replicates per point.  Thresholds fixed before the first run: a bound holds if MC <= bound + 2 SE;
identity: paired |z| <= 3 where the acceptance frequency is >= 1%, Poisson 99% interval otherwise.
Output: theory/check_refit_output.txt (this script's printout) and, since v0.4, results/refit_check.json
(read by experiments/make_numbers.py after checking its SHA-256 against results/refit_check.json.sha256).
Notation: rho in this script is eta = m/n in the manuscript (rho there is the Hoeffding radius).
v0.5 (internal referee, round 3): sections (d)-(h) added -- collinear 1-D reduction of M_eta, exact worst case
of the split estimator, oracle correction C = theta, adversarial families without held-out noise (quadrature /
Rao-Blackwell), alpha = 0.5 in 36 other designs.  They use quadrature and deterministic grids only (no new random
draws), so the Monte Carlo numbers of (a)-(b') are unchanged; results/refit_check.json gains new keys only.
"""
import json
import os
import sys
import time

import numpy as np
from scipy.optimize import minimize
from scipy.special import gammaln, ndtr
from scipy.stats import norm, poisson, chi

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
sys.path.insert(0, os.path.join(ROOT, "experiments"))
import safe_reversion as sr  # noqa: E402  (reuse CFG, constants, simulate)

T0, C0 = time.time(), time.process_time()
CFG = sr.CFG
SIG, D, N, REPS = CFG["sigma"], CFG["d"], CFG["n"], CFG["R"]
ALPHAS, MGRID = CFG["alpha_grid"], CFG["m_grid"]
assert REPS >= 20000, "run without --fast"
LINES = []


def out(s=""):
    print(s, flush=True)
    LINES.append(s)


def phi(x):
    return np.exp(-0.5 * np.asarray(x, float) ** 2) / np.sqrt(2 * np.pi)


PHI0 = float(phi(0.0))
CD = sr.chi_mean(D)                                                  # E||Z||, Z ~ N(0, I_d)
MU3 = float(2 ** 1.5 * np.exp(gammaln((D + 3) / 2) - gammaln(D / 2)))  # E||Z||^3
CHI_Q = float(chi.ppf(1 - 1e-9, D))
sq = lambda v: (v ** 2).sum(axis=-1)
dot = lambda u, v: (u * v).sum(axis=-1)


def mse(x):
    x = np.asarray(x, float)
    return float(x.mean()), float(x.std(ddof=1) / np.sqrt(x.size))


# ----------------------------------------------------------------------------------------------
# Constants: Psi_rho(x) = sup_u {(u+x) Phi(-(z+u)) + rho phi(z+u)},  M_rho(a) = sup f(omega, delta)
# ----------------------------------------------------------------------------------------------
class Const:
    XMAX, NX = 4.0, 401

    def __init__(self, alpha, m):
        self.alpha, self.m, self.n_e, self.rho = alpha, m, N - m, m / N
        z = self.z = float(norm.ppf(1 - alpha))
        self.k, self.us, self.k2 = sr.kap_all(alpha)
        rho = self.rho
        u = np.linspace(0.0, 30.0, 300001)
        self.lam1 = float((u * phi(z + u)).max())                        # sup_{u>=0} u phi(z+u)
        ug = np.linspace(-40.0, 40.0, 800001)
        self.krho = float((np.maximum(ug, 0) * ndtr(-(z + ug)) + rho * phi(z + ug)).max())
        self.kbar = max(self.k + rho * float(phi(z)), rho * PHI0)          # closed form >= krho
        uu = np.linspace(-15.0, 15.0, 12001)
        self.xg = np.linspace(0.0, self.XMAX, self.NX)
        P, F = ndtr(-(z + uu)), rho * phi(z + uu)
        self.psi = np.array([((uu + x) * P + F).max() for x in self.xg])
        self.psi0 = float(self.psi[0])
        self.psi_closed_gap = float((self.psi - (self.kbar + self.xg * ndtr(self.xg - z))).max())
        self._mgrid()
        self._caps()

    def Psi(self, x):
        x = np.asarray(x, float)
        v = np.interp(np.minimum(x, self.XMAX), self.xg, self.psi)   # chords of a convex fn: >= Psi
        return np.where(x > self.XMAX, self.kbar + x * ndtr(x - self.z), v)

    def f(self, om, c, a):
        z, rho = self.z, self.rho
        u = om / 2 + a * c
        return (om ** 2 + 2 * (1 - rho) * om * a * c) * ndtr(-(z + u)) + 2 * rho * om * phi(z + u)

    def B(self, a):
        """closed-form upper bound of M_rho(a) (max of cases A and B of the proof)."""
        z, rho, kb = self.z, self.rho, self.kbar
        A_ = 4 * a * (kb + rho * a * ndtr(rho * a - z))
        B_ = 4 * a * (kb + rho * a * self.alpha) + 4 * (self.k2 + rho * a * self.k + rho * self.lam1)
        return np.maximum(A_, B_)

    def _mgrid(self):
        amax = np.sqrt(self.m / self.n_e) * CHI_Q
        self.ag = np.linspace(0.0, amax, 81)
        Ms, oms, cs = [], [], []
        for a in self.ag:
            om = np.linspace(1e-6, 2 * a + 30.0, 401)
            cc = np.linspace(-1.0, 1.0, 161)
            O, Cc = np.meshgrid(om, cc, indexing="ij")
            fv = self.f(O, Cc, a)
            i = int(np.argmax(fv))
            x0 = [O.flat[i], Cc.flat[i]]
            res = minimize(lambda p: -float(self.f(p[0], p[1], a)), x0, method="L-BFGS-B",
                           bounds=[(1e-9, 2 * a + 60.0), (-1.0, 1.0)])
            if -res.fun > fv.flat[i]:
                Ms.append(-res.fun); oms.append(res.x[0]); cs.append(res.x[1])
            else:
                Ms.append(fv.flat[i]); oms.append(x0[0]); cs.append(x0[1])
        self.M, self.om_star, self.c_star = np.array(Ms), np.array(oms), np.array(cs)
        self.B_gap = float((self.M - self.B(self.ag)).max())   # must be <= 0

    def _caps(self):
        q = np.sqrt(self.m / self.n_e)
        x = np.linspace(1e-6, CHI_Q, 6001)
        wts = chi.pdf(x, D); wts /= np.trapezoid(wts, x)
        Ma = np.interp(q * x, self.ag, self.M)
        s2m = SIG ** 2 / self.m
        self.cap_exact = s2m * float(np.trapezoid(wts * Ma, x))
        rho, z = self.rho, self.z
        Ea, Ea2, Ea3 = CD * q, D * q ** 2, MU3 * q ** 3
        self.cap_closed = s2m * (4 * (self.kbar + rho * self.k) * Ea + 4 * rho * (self.alpha * Ea2 + rho * PHI0 * Ea3)
                                 + 4 * self.k2 + 4 * rho * self.lam1)
        self.cap_closedB = s2m * float(np.trapezoid(wts * self.B(q * x), x))
        self.split = D * SIG ** 2 * self.m / (N * self.n_e)                 # Corollary 4.4
        self.lower = 4 * self.alpha * self.split + 4 * rho * float(phi(z)) * SIG ** 2 * CD / np.sqrt(self.n_e * self.m)
        self.split_lo = self.split + 4 * SIG ** 2 * (self.k * CD / np.sqrt(self.n_e * self.m) + self.us * self.k / self.m)
        self.split_hi = self.split + 4 * SIG ** 2 * (self.k * CD / np.sqrt(self.n_e * self.m) + self.k2 / self.m)

    def worst_w(self, e):
        """an F-measurable correction attaining (on the a-grid) the sup M_rho(a): adversarial family."""
        ne = np.sqrt(sq(e))
        a = np.sqrt(self.m) * ne / SIG
        om = np.interp(a, self.ag, self.om_star)
        c = np.clip(np.interp(a, self.ag, self.c_star), -1, 1)
        eh = e / ne[..., None]
        g = np.zeros_like(e); g[..., 1] = 1.0
        g = g - dot(g, eh)[..., None] * eh
        g = g / np.sqrt(sq(g))[..., None]
        return (SIG / np.sqrt(self.m)) * om[..., None] * (c[..., None] * eh + np.sqrt(1 - c ** 2)[..., None] * g)


CONST = {(a, m): Const(a, m) for a in ALPHAS for m in MGRID}
out("OMR001 -- check of theory/refit_bound.tex (transported refit and cross-fitting)")
out(f"design: d={D}, sigma={SIG}, n={N}, m in {MGRID}, alpha in {ALPHAS}, replicates per point {REPS}, seed {sr.SEED}")
out("")
out("== Constants (rho = m/n; kbar = max(kappa + rho phi(z), rho phi(0)); caps in absolute risk units) ==")
out(" alpha   m  rho  kappa   kappa2  lambda1 kappa_rho kbar   Psi(0) | split   cap_rf(exact) cap_rf(closed) "
    "lower_rf | split+cap43 [lo, hi] (split estimator vs Xbar_n)")
for (a, m), c in CONST.items():
    out(f" {a:4.2f} {m:3d} {c.rho:4.2f} {c.k:.4f} {c.k2:.4f} {c.lam1:.4f} {c.krho:.4f}  {c.kbar:.4f} {c.psi0:.4f} | "
        f"{c.split:.4f} {c.cap_exact:.4f}        {c.cap_closed:.4f}         {c.lower:.4f}   | [{c.split_lo:.4f}, {c.split_hi:.4f}]")
gapB = max(c.B_gap for c in CONST.values())
gapP = max(c.psi_closed_gap for c in CONST.values())
out(f"validity of closed forms on the grids: max_a [M_rho(a) - B(a)] = {gapB:.2e} (<= 0 required); "
    f"max_x [Psi_rho(x) - kbar - x Phi(x-z)] = {gapP:.2e} (<= 0 required)")
out(f"max over grid of closed cap via B(a) vs exact: ratio closedB/exact in "
    f"[{min(c.cap_closedB / c.cap_exact for c in CONST.values()):.2f}, {max(c.cap_closedB / c.cap_exact for c in CONST.values()):.2f}]; "
    f"fully explicit closed/exact in [{min(c.cap_closed / c.cap_exact for c in CONST.values()):.2f}, "
    f"{max(c.cap_closed / c.cap_exact for c in CONST.values()):.2f}]")
out("")


# ----------------------------------------------------------------------------------------------
# (a) Design of experiments/safe_reversion.py: same draws as sr.simulate
# ----------------------------------------------------------------------------------------------
def sim_vec(rng, snr, dep, m, tau2=None):
    """Exact replica of sr.simulate's draws (same order), returning the vectors."""
    S, n_s = CFG["S"], CFG["n_s"]
    n_e = N - m
    se2_e, se2_n = SIG ** 2 / n_e, SIG ** 2 / N
    if tau2 is None:
        tau2 = snr * se2_e
    tau = np.sqrt(tau2)
    mu = np.zeros(D)
    theta_s = mu + tau * rng.standard_normal((REPS, S, D))
    Xs = theta_s + (SIG / np.sqrt(n_s)) * rng.standard_normal((REPS, S, D))
    mu_hat = Xs.mean(axis=1)
    v_hat = ((Xs - mu_hat[:, None, :]) ** 2).sum(axis=(1, 2)) / ((S - 1) * D)
    tau2_hat = np.maximum(v_hat - SIG ** 2 / n_s, 0.0)
    shift = np.zeros(D); shift[0] = dep * tau
    theta = mu + shift + tau * rng.standard_normal((REPS, D))
    Xe = theta + np.sqrt(se2_e) * rng.standard_normal((REPS, D))
    Yb = theta + (SIG / np.sqrt(m)) * rng.standard_normal((REPS, D))
    Xn = (n_e * Xe + m * Yb) / N
    return dict(theta=theta, Xe=Xe, Yb=Yb, Xn=Xn, mu_hat=mu_hat, tau2_hat=tau2_hat,
                lam_e=tau2_hat / (tau2_hat + se2_e), lam_n=tau2_hat / (tau2_hat + se2_n), tau=tau)


def lams(v, name):
    if name == "eb":
        return v["lam_e"], v["lam_n"]
    if name == "pool":
        return np.zeros(REPS), np.zeros(REPS)
    return 0.5 * np.ones(REPS), 0.5 * np.ones(REPS)


# consistency with sr.simulate
o1 = sr.simulate(np.random.default_rng(sr.SEED), 1.0, 4.0, 12)
v1 = sim_vec(np.random.default_rng(sr.SEED), 1.0, 4.0, 12)
dmax = max(float(np.abs(o1["L_Re"] - sq(v1["Xe"] - v1["theta"])).max()),
           float(np.abs(o1["L_Rn"] - sq(v1["Xn"] - v1["theta"])).max()))
for name in CFG["operators"]:
    le, ln = lams(v1, name)
    C = v1["mu_hat"] + le[:, None] * (v1["Xe"] - v1["mu_hat"])
    Cn = v1["mu_hat"] + ln[:, None] * (v1["Xn"] - v1["mu_hat"])
    dmax = max(dmax, float(np.abs(o1["ops"][name]["Dhat"] - (sq(C - v1["Yb"]) - sq(v1["Xe"] - v1["Yb"]))).max()),
               float(np.abs(o1["ops"][name]["L_bn"] - sq(Cn - v1["theta"])).max()))
out(f"== (a) Simulation design ==\nreplica of sr.simulate (same seed): max |difference| of L_Re, L_Rn, Dhat, L(C_n) = {dmax:.1e}")
del o1, v1

RES = json.load(open(os.path.join(ROOT, "results", "results.json")))
rng = np.random.default_rng(sr.SEED)
configs = [("structure", i, snr, 0.0, CFG["m_default"], None) for i, snr in enumerate(CFG["snr_grid"])]
configs += [("departure", i, CFG["snr_dep"], dep, CFG["m_default"], None) for i, dep in enumerate(CFG["dep_grid"])]
tau2_fixed = CFG["snr_dep"] * SIG ** 2 / (N - CFG["m_default"])
j = 0
for m in MGRID:
    for dep in [0.0, 8.0]:
        configs.append(("m_sweep", j, CFG["snr_dep"], dep, m, tau2_fixed)); j += 1
KEY = {"structure": "structure_sweep", "departure": "departure_sweep", "m_sweep": "m_sweep"}

rows, repro = [], 0.0
for (sweep, idx, snr, dep, m, t2) in configs:
    v = sim_vec(rng, snr, dep, m, t2)
    theta, Xe, Yb, Xn, mu_hat = v["theta"], v["Xe"], v["Yb"], v["Xn"], v["mu_hat"]
    e, h, en = Xe - theta, Yb - theta, Xn - theta
    L_Re, L_Rn = sq(e), sq(en)
    a_ = np.sqrt(m) * np.sqrt(sq(e)) / SIG
    for name in CFG["operators"]:
        le, ln = lams(v, name)
        C = mu_hat + le[:, None] * (Xe - mu_hat)
        Cn = mu_hat + ln[:, None] * (Xn - mu_hat)
        w = C - Xe
        ww = sq(w)
        Delta = ww + 2 * dot(w, e)
        s = 2 * SIG * np.sqrt(ww) / np.sqrt(m)
        Dhat = sq(C - Yb) - sq(Xe - Yb)
        gain_tr = ww + 2 * dot(w, en)                 # l(Xbar_n + w) - l(Xbar_n)
        Delta_n = sq(Cn - theta) - L_Rn               # simulation's refit (operator re-applied)
        for al in ALPHAS:
            c = CONST[(al, m)]
            z, rho = c.z, c.rho
            A = Dhat <= -z * s
            with np.errstate(divide="ignore", invalid="ignore"):
                u = np.where(s > 0, Delta / np.where(s > 0, s, 1.0), 0.0)
            pi = np.where(s > 0, ndtr(-(z + u)), 0.0)
            rb = np.where(s > 0, ((1 - rho) * Delta + rho * ww) * pi + rho * s * phi(z + u), 0.0)
            ex = A * gain_tr
            exm = mse(ex)
            idm = mse(ex - rb)
            b2 = float((s * c.Psi(rho * a_)).mean())
            b2c = float((s * (c.kbar + rho * a_ * ndtr(rho * a_ - z))).mean())
            simrf = mse(A * Delta_n)
            split = mse(L_Re - L_Rn + A * Delta)
            risk_refit_repro = float((L_Rn + A * Delta_n).mean())
            ref = RES[KEY[sweep]][idx]["ops"][name]["rev"][str(al)]["risk_refit"][0]
            repro = max(repro, abs(risk_refit_repro - ref))
            acc = float(A.mean())
            if acc >= 0.01:
                idz, idok = (idm[0] / idm[1] if idm[1] > 0 else 0.0), None
                idok = abs(idz) <= 3
            else:
                eacc = float(pi.sum()); nacc = int(A.sum())
                lo, hi = poisson.ppf(0.005, eacc), poisson.ppf(0.995, eacc)
                idz, idok = None, (lo <= nacc <= hi) if eacc > 0 else (nacc == 0)
            rows.append(dict(sweep=sweep, snr=snr, dep=dep, m=m, op=name, alpha=al, ex=exm, rb=float(rb.mean()),
                             idz=idz, idok=bool(idok), b2=b2, b2c=b2c, cap=c.cap_exact, capc=c.cap_closed,
                             simrf=simrf, split=split, acc=acc,
                             Es=float(s.mean())))
    del v

ok = lambda r, key: r["ex"][0] <= r[key] + 2 * r["ex"][1]
nrow = len(rows)
out(f"configurations x operators x alpha: {nrow}; refit risks reproduce results.json: max |diff| = {repro:.1e}")
for key, lab in [("b2", "(II) E[s Psi]"), ("b2c", "(II) closed"), ("cap", "(III) cap exact"), ("capc", "(III) cap closed")]:
    hold = sum(ok(r, key) for r in rows)
    mx = max(r["ex"][0] / r[key] for r in rows if r[key] > 0)
    out(f"  transported refit vs Xbar_n <= {lab:18s}: holds in {hold}/{nrow}; max MC/bound = {mx:.3f}")
zs = [abs(r["idz"]) for r in rows if r["idz"] is not None]
out(f"  identity (I): paired z in {len(zs)} combinations, max |z| = {max(zs):.2f}; Poisson in {nrow - len(zs)}; "
    f"failures: {sum(not r['idok'] for r in rows)}")
for key, lab in [("b2", "(II) E[s Psi]"), ("cap", "(III) cap exact")]:
    hold = sum(r["simrf"][0] <= r[key] + 2 * r["simrf"][1] for r in rows)
    mx = max(r["simrf"][0] / r[key] for r in rows if r[key] > 0)
    out(f"  [not covered] simulation's refit (C re-applied to Xbar_n, lambda_n) vs Xbar_n <= {lab}: "
        f"{hold}/{nrow}; max MC/bound = {mx:.3f}")
out("")
out("EB operator, alpha = 0.1, excess risk over Xbar_n (MC +- SE): split reversion (Cor. 4.4) | transported refit | "
    "simulation's refit | bounds (II) and (III) for the refit")
for r in rows:
    if r["op"] == "eb" and r["alpha"] == 0.1:
        tag = f"{r['sweep'][:4]} snr={r['snr']:<5} dep={r['dep']:<4} m={r['m']:<2}"
        out(f"  {tag}: split {r['split'][0]:+.4f} | refit {r['ex'][0]:+.4f}+-{r['ex'][1]:.4f} | sim-refit "
            f"{r['simrf'][0]:+.4f} | (II) {r['b2']:.4f} (closed {r['b2c']:.4f}) | cap {r['cap']:.4f} (closed {r['capc']:.4f})")
out("")


# ----------------------------------------------------------------------------------------------
# (a') Cross-fitted run of the same design (fresh seed; K = n/m folds; m must divide n)
# ----------------------------------------------------------------------------------------------
def sim_cf(rng, snr, dep, m, tau2=None):
    S, n_s, K = CFG["S"], CFG["n_s"], N // m
    n_e = N - m
    if tau2 is None:
        tau2 = snr * SIG ** 2 / n_e
    tau = np.sqrt(tau2)
    theta_s = tau * rng.standard_normal((REPS, S, D))
    Xs = theta_s + (SIG / np.sqrt(n_s)) * rng.standard_normal((REPS, S, D))
    mu_hat = Xs.mean(axis=1)
    v_hat = ((Xs - mu_hat[:, None, :]) ** 2).sum(axis=(1, 2)) / ((S - 1) * D)
    tau2_hat = np.maximum(v_hat - SIG ** 2 / n_s, 0.0)
    shift = np.zeros(D); shift[0] = dep * tau
    theta = shift + tau * rng.standard_normal((REPS, D))
    Yk = theta[:, None, :] + (SIG / np.sqrt(m)) * rng.standard_normal((REPS, K, D))
    return theta, Yk, mu_hat, tau2_hat / (tau2_hat + SIG ** 2 / n_e)


def cf_eval(theta, Yk, wfun, m, al):
    """cross-fitted excess over Xbar_n for corrections w_k = wfun(R_k, e_k) (vectors (REPS,K,D))."""
    K = Yk.shape[1]
    Xn = Yk.mean(axis=1)
    Rk = (K * Xn[:, None, :] - Yk) / (K - 1)
    ek, hk, en = Rk - theta[:, None, :], Yk - theta[:, None, :], Xn - theta
    wk = wfun(Rk, ek) if callable(wfun) else wfun
    c = CONST[(al, m)]
    z, rho = c.z, c.rho
    ww = sq(wk)
    s = 2 * SIG * np.sqrt(ww) / np.sqrt(m)
    Ck = Rk + wk
    A = (sq(Ck - Yk) - sq(Rk - Yk)) <= -z * s
    W = (A[..., None] * wk).mean(axis=1)
    ex = sq(en + W) - sq(en)
    jensen = (A * (ww + 2 * dot(wk, en[:, None, :]))).mean(axis=1)    # average of per-fold refits
    ak = np.sqrt(m) * np.sqrt(sq(ek)) / SIG
    b2 = float((s * c.Psi(rho * ak)).mean())
    return mse(ex), mse(jensen), b2, c


out("== (a') Cross-fitted reversion on the same design (fresh seed 20260930+7; K = n/m) ==")
rng = np.random.default_rng(sr.SEED + 7)
cf_cfg = [(snr, 0.0, 12, None) for snr in CFG["snr_grid"]] + [(CFG["snr_dep"], dep, 12, None) for dep in CFG["dep_grid"]]
cf_cfg += [(CFG["snr_dep"], dep, m, tau2_fixed) for m in MGRID if N % m == 0 and m != 12 for dep in (0.0, 8.0)]
cf_rows = []
for (snr, dep, m, t2) in cf_cfg:
    theta, Yk, mu_hat, lam = sim_cf(rng, snr, dep, m, t2)
    for name in CFG["operators"]:
        lm = lam if name == "eb" else (np.zeros(REPS) if name == "pool" else 0.5 * np.ones(REPS))
        wfun = lambda Rk, ek: (1 - lm)[:, None, None] * (mu_hat[:, None, :] - Rk)
        for al in ALPHAS:
            exm, jm, b2, c = cf_eval(theta, Yk, wfun, m, al)
            cf_rows.append(dict(snr=snr, dep=dep, m=m, op=name, alpha=al, ex=exm, jen=jm, b2=b2,
                                cap=c.cap_exact, capc=c.cap_closed, split=c.split))
ncf = len(cf_rows)
out(f"configurations x operators x alpha: {ncf} (m in {sorted(set(r['m'] for r in cf_rows))}; m = 24 does not divide n = 60)")
for key, lab in [("b2", "(IV) fold-average of E[s Psi]"), ("cap", "(IV) cap exact"), ("capc", "(IV) cap closed")]:
    hold = sum(r["ex"][0] <= r[key] + 2 * r["ex"][1] for r in cf_rows)
    mx = max(r["ex"][0] / r[key] for r in cf_rows)
    out(f"  cross-fit vs Xbar_n <= {lab:30s}: holds in {hold}/{ncf}; max MC/bound = {mx:.3f}")
out(f"  Jensen step: cross-fit excess <= fold-average of per-fold refit excesses in "
    f"{sum(r['ex'][0] <= r['jen'][0] + 1e-12 for r in cf_rows)}/{ncf} (pathwise inequality)")
out("EB operator, alpha = 0.1: cross-fit excess over Xbar_n vs split cost (what the split estimator always pays)")
for r in cf_rows:
    if r["op"] == "eb" and r["alpha"] == 0.1:
        out(f"  snr={r['snr']:<5} dep={r['dep']:<4} m={r['m']:<2}: cross-fit {r['ex'][0]:+.4f}+-{r['ex'][1]:.4f} | "
            f"split cost {r['split']:.4f} | (IV) {r['b2']:.4f} | cap {r['cap']:.4f}")
gain_rows = [r for r in cf_rows if r["op"] == "eb" and r["alpha"] == 0.1 and r["dep"] == 0.0 and r["m"] == 12]
out("")


# ----------------------------------------------------------------------------------------------
# (b) Adversarial grid of (theta, C): theta = theta_0 = 0 w.l.o.g. (translation), C = R + w(e)
# ----------------------------------------------------------------------------------------------
def families(c, e):
    """dict name -> w (same shape as e); every w is a measurable function of (R, fixed vectors)."""
    m, n_e = c.m, c.n_e
    se = SIG / np.sqrt(n_e)
    e1 = np.zeros(e.shape[-1]); e1[0] = 1.0
    F = {}
    for t in (0.1, 0.5, 1.0, 1.5, 1.8, 2.0, 2.2, 3.0):
        F[f"reflect t={t}"] = -t * e
    for r in (0.25, 0.5, 1.0, 2.0, 4.0, 8.0):
        F[f"fixed |v|={r}sig/sqrt(m)"] = np.broadcast_to(r * SIG / np.sqrt(m) * e1, e.shape).copy()
    for lam in (0.0, 0.5):
        for k in (0, 1, 2, 4, 8, 16):
            F[f"shrink lam={lam} |mu-theta|={k}sig_e"] = (1 - lam) * (k * se * e1 - e)
    ne = np.sqrt(sq(e))[..., None]
    F["Prop4.5b"] = -2 * e - (2 * SIG * c.us / np.sqrt(m)) * e / ne
    F["worst(M_rho)"] = c.worst_w(e)
    return F


out("== (b) Adversarial grid (theta, C), transported refit, %d replicates per point ==" % REPS)
rng = np.random.default_rng(sr.SEED + 11)
adv, worst_ratio = [], []
for m in MGRID:
    n_e = N - m
    e = (SIG / np.sqrt(n_e)) * rng.standard_normal((REPS, D))
    h = (SIG / np.sqrt(m)) * rng.standard_normal((REPS, D))
    rho = m / N
    en = (1 - rho) * e + rho * h
    a_ = np.sqrt(m) * np.sqrt(sq(e)) / SIG
    for al in ALPHAS:
        c = CONST[(al, m)]
        for fam, w in families(c, e).items():
            ww = sq(w)
            s = 2 * SIG * np.sqrt(ww) / np.sqrt(m)
            Delta = ww + 2 * dot(w, e)
            Dhat = sq(e + w - h) - sq(e - h)
            A = Dhat <= -c.z * s
            ex = A * (ww + 2 * dot(w, en))
            with np.errstate(divide="ignore", invalid="ignore"):
                u = np.where(s > 0, Delta / np.where(s > 0, s, 1.0), 0.0)
            rb = np.where(s > 0, ((1 - rho) * Delta + rho * ww) * ndtr(-(c.z + u)) + rho * s * phi(c.z + u), 0.0)
            exm = mse(ex); idm = mse(ex - rb)
            b2 = float((s * c.Psi(rho * a_)).mean())
            adv.append(dict(m=m, alpha=al, fam=fam, ex=exm, rb=float(rb.mean()),
                            z=idm[0] / idm[1] if idm[1] > 0 else 0.0, acc=float(A.mean()),
                            b2=b2, cap=c.cap_exact, capc=c.cap_closed, split=c.split, lower=c.lower))
nadv = len(adv)
for key, lab in [("b2", "(II) E[s Psi]"), ("cap", "(III) cap exact"), ("capc", "(III) cap closed")]:
    hold = sum(r["ex"][0] <= r[key] + 2 * r["ex"][1] for r in adv)
    mx = max(adv, key=lambda r: r["ex"][0] / r[key])
    out(f"  refit vs Xbar_n <= {lab:16s}: holds in {hold}/{nadv}; max MC/bound = {mx['ex'][0] / mx[key]:.3f} "
        f"({mx['fam']}, m={mx['m']}, alpha={mx['alpha']})")
zz = [abs(r["z"]) for r in adv if r["acc"] >= 0.01]
out(f"  identity (I): max |paired z| over {len(zz)} points with acceptance >= 1% = {max(zz):.2f}")
out("  sharpness of the cap: refit excess of the family 'worst(M_rho)' / exact cap, and family 'reflect t=2.0'"
    " (C = 2 theta_0 - R) / lower bound 4 alpha split + 4 rho phi(z) sigma^2 c_d / sqrt(n_e m):")
for m in MGRID:
    parts = []
    for al in ALPHAS:
        rw = [r for r in adv if r["m"] == m and r["alpha"] == al and r["fam"] == "worst(M_rho)"][0]
        rr = [r for r in adv if r["m"] == m and r["alpha"] == al and r["fam"] == "reflect t=2.0"][0]
        parts.append(f"a={al}: {rw['ex'][0] / rw['cap']:.3f} / {rr['ex'][0] / rr['lower']:.3f}")
    out(f"    m={m:2d}: " + "; ".join(parts))
out("")

out("== (b') Adversarial grid, cross-fitted (same families applied in every fold), %d replicates per point ==" % REPS)
rng = np.random.default_rng(sr.SEED + 13)
advcf = []
for m in [mm for mm in MGRID if N % mm == 0]:
    K = N // m
    theta = np.zeros((REPS, D))
    Yk = (SIG / np.sqrt(m)) * rng.standard_normal((REPS, K, D))
    Rk0 = (K * Yk.mean(axis=1)[:, None, :] - Yk) / (K - 1)
    for al in ALPHAS:
        c = CONST[(al, m)]
        for fam, wk in families(c, Rk0 - theta[:, None, :]).items():
            exm, jm, b2, _ = cf_eval(theta, Yk, wk, m, al)
            advcf.append(dict(m=m, alpha=al, fam=fam, ex=exm, jen=jm, b2=b2, cap=c.cap_exact, capc=c.cap_closed,
                              split=c.split))
nacf = len(advcf)
for key, lab in [("b2", "(IV) fold-avg E[s Psi]"), ("cap", "(IV) cap exact"), ("capc", "(IV) cap closed")]:
    hold = sum(r["ex"][0] <= r[key] + 2 * r["ex"][1] for r in advcf)
    mx = max(advcf, key=lambda r: r["ex"][0] / r[key])
    out(f"  cross-fit vs Xbar_n <= {lab:22s}: holds in {hold}/{nacf}; max MC/bound = {mx['ex'][0] / mx[key]:.3f} "
        f"({mx['fam']}, m={mx['m']}, alpha={mx['alpha']})")
mxs = max(advcf, key=lambda r: r["ex"][0] / r["split"])
out(f"  largest cross-fit excess / split cost on the grid: {mxs['ex'][0] / mxs['split']:.3f} "
    f"({mxs['fam']}, m={mxs['m']}, alpha={mxs['alpha']}); per-fold refit average (Jensen) for that point: "
    f"{mxs['jen'][0] / mxs['split']:.3f}")
for m in [mm for mm in MGRID if N % mm == 0]:
    parts = []
    for al in ALPHAS:
        rr = [r for r in advcf if r["m"] == m and r["alpha"] == al]
        best = max(rr, key=lambda r: r["ex"][0])
        parts.append(f"a={al}: {best['ex'][0]:.4f} ({best['ex'][0] / best['split']:.2f} split; {best['fam']})")
    out(f"    m={m:2d} worst family: " + "; ".join(parts))
out("")


# ----------------------------------------------------------------------------------------------
# (c) v0.4 addition: the route "use C if the check passes, otherwise Xbar_n" (Remark rem:refitcost(c)).
# Exact limit of its excess over Xbar_n for C = R - t (R - theta_0), t -> 0, by quadrature over
# xi = sqrt(m/n_e) chi_d (no Monte Carlo):  (sigma^2/m) E[ Phi(xi-z)((2 eta - eta^2) xi^2 - eta^2 d)
#   + 2 eta (1-eta) xi phi(z-xi) - eta^2 (z-xi) phi(z-xi) ].
# ----------------------------------------------------------------------------------------------
from scipy.integrate import quad  # noqa: E402

out("== (c) Route 'C if the check passes, else Xbar_n': exact limit of the excess for a vanishing correction ==")
V1 = {}
for (al, m), c in CONST.items():
    q, eta, z = np.sqrt(m / c.n_e), c.rho, c.z
    integrand = lambda r: (ndtr(q * r - z) * ((2 * eta - eta ** 2) * (q * r) ** 2 - eta ** 2 * D)
                           + 2 * eta * (1 - eta) * q * r * phi(z - q * r)
                           - eta ** 2 * (z - q * r) * phi(z - q * r)) * chi.pdf(r, D)
    lim = SIG ** 2 / m * quad(integrand, 0.0, 60.0, limit=200)[0]
    V1[(al, m)] = lim
out("  limit / split cost:  " + "; ".join(f"a={al}, m={m}: {V1[(al, m)] / CONST[(al, m)].split:.3f}"
                                         for (al, m) in CONST))
out("")


# ----------------------------------------------------------------------------------------------
# v0.5 additions (internal referee, round 3).  Quadrature / deterministic grids only: no new random
# draws, so every Monte Carlo number of sections (a)-(b') is unchanged.
#  (d) collinear reduction of M_eta (Theorem thm:refit(iv), referee m2): for fixed u = delta/(2 omega),
#      f_eta is a convex quadratic in omega on (2(u-xi)^+, 2(u+xi)], so the sup is at c = -1 or c = +1;
#      M_eta is recomputed as a one-dimensional sup and compared with the 2-D search of Const.
#  (e) exact worst case of the split estimator (Proposition prop:sharp(c), referee m1):
#      sup_{theta, C} risk(rev) - risk(Xbar_n) = split + (sigma^2/m) E[M_0(alpha; xi)],
#      M_0(alpha; xi) = 4 sup_{u>=0} (u^2 + xi u) Phi(-(z+u)).
#  (f) oracle correction C = theta (referee M1): exact excess over Xbar_n of the transported refit,
#      (sigma^2/m) E[-(1-2 eta) xi^2 Phi(xi/2 - z) + 2 eta xi phi(z - xi/2)], and of the split estimator,
#      split + (sigma^2/m) E[-xi^2 Phi(xi/2 - z)].
#  (g) adversarial families without held-out noise (referee m4): exact quadrature for the families that
#      depend on R only through xi (reflections, Prop. 4.5(b), worst(M_eta)); Rao-Blackwellised MC
#      (variance from e only; the 'rb' column of section (b)) for all families.
#  (h) alpha = 0.5 in other designs (referee m6): worst case of the refit vs exact worst case of the split.
# ----------------------------------------------------------------------------------------------
UG = np.linspace(0.0, 40.0, 40001)


def M0_split(al, xis):
    """M_0(alpha; xi) = 4 sup_{u >= 0} (u^2 + xi u) Phi(-(z+u))  (split estimator, eta = 0)."""
    z = float(norm.ppf(1 - al))
    P = ndtr(-(z + UG))
    A_, B_ = UG ** 2 * P, UG * P
    return np.array([4.0 * float((A_ + x * B_).max()) for x in np.atleast_1d(xis)])


def M_1d(al, eta, xis, du=0.002):
    """M_eta(alpha; xi) through the collinear reduction: endpoints omega = 2(u + xi) (c = -1, u > -xi)
    and omega = 2(u - xi) (c = +1, u > xi); the value 0 (omega -> 0) is included."""
    z = float(norm.ppf(1 - al))
    res = []
    for x in np.atleast_1d(xis):
        u = np.arange(-x, x + z + 40.0, du)
        P, F = ndtr(-(z + u)), phi(z + u)
        om = 2 * (u + x)
        a = eta * P * om ** 2 + 2 * om * ((1 - eta) * u * P + eta * F)
        k = u > x
        omb = 2 * (u[k] - x)
        b = eta * P[k] * omb ** 2 + 2 * omb * ((1 - eta) * u[k] * P[k] + eta * F[k])
        res.append(max(0.0, float(a.max()), float(b.max()) if b.size else 0.0))
    return np.array(res)


def chi_grid(m, n_e, npts=6001, d=D):
    """grid and normalised chi_d weights used for E over xi = sqrt(m/n_e) chi_d (same rule as Const._caps)."""
    x = np.linspace(1e-6, float(chi.ppf(1 - 1e-9, d)), npts)
    w = chi.pdf(x, d)
    return x, w / np.trapezoid(w, x), np.sqrt(m / n_e)


out("== (d) Collinear reduction of M_eta (1-D sup over c = +-1) vs the 2-D search ==")
RED = {}
for (al, m), c in CONST.items():
    M1 = M_1d(al, c.rho, c.ag)
    x, wts, q = chi_grid(m, c.n_e)
    cap1 = SIG ** 2 / m * float(np.trapezoid(wts * np.interp(q * x, c.ag, M1), x))
    big = c.M > 1e-12
    RED[(al, m)] = dict(d2_minus_d1=float((c.M - M1).max()), d1_minus_d2=float((M1 - c.M).max()),
                        cap_1d=cap1, cap_rel_diff=float(abs(cap1 - c.cap_exact) / c.cap_exact),
                        min_abs_c=float(np.abs(c.c_star[big]).min()))
out(f"  max over grid of [M_2D - M_1D] = {max(r['d2_minus_d1'] for r in RED.values()):.2e}; "
    f"max [M_1D - M_2D] = {max(r['d1_minus_d2'] for r in RED.values()):.2e}; "
    f"max relative difference of the exact cap = {max(r['cap_rel_diff'] for r in RED.values()):.1e}; "
    f"min |c| at the 2-D maximiser = {min(r['min_abs_c'] for r in RED.values()):.4f}")
out("")

out("== (e) Exact worst case of the split estimator over theta and C (excess over Xbar_n; Prop. 4.5(c)) ==")
SPX = {}
for (al, m), c in CONST.items():
    x, wts, q = chi_grid(m, c.n_e)
    xg = np.linspace(0.0, q * x[-1], 401)
    over_R = SIG ** 2 / m * float(np.trapezoid(wts * np.interp(q * x, xg, M0_split(al, xg)), x))
    SPX[(al, m)] = dict(over_R=over_R, total=c.split + over_R)
for al in ALPHAS:
    out(f"  a={al}: " + "; ".join(f"m={m}: split {SPX[(al, m)]['total']:.4f} (over R {SPX[(al, m)]['over_R']:.4f} in "
                                  f"[{CONST[(al, m)].split_lo - CONST[(al, m)].split:.4f}, "
                                  f"{CONST[(al, m)].split_hi - CONST[(al, m)].split:.4f}]) vs refit {CONST[(al, m)].cap_exact:.4f}"
                                  for m in MGRID))
out("")

out("== (f) Oracle correction C = theta: exact excess over Xbar_n (quadrature) ==")
ORA = {}
for (al, m), c in CONST.items():
    q, eta, z = np.sqrt(m / c.n_e), c.rho, c.z
    g_rf = lambda r: (-(1 - 2 * eta) * (q * r) ** 2 * ndtr(q * r / 2 - z) + 2 * eta * q * r * phi(z - q * r / 2)) * chi.pdf(r, D)
    g_sp = lambda r: (-(q * r) ** 2 * ndtr(q * r / 2 - z)) * chi.pdf(r, D)
    ORA[(al, m)] = dict(refit=SIG ** 2 / m * quad(g_rf, 0.0, 60.0, limit=200)[0],
                        split=c.split + SIG ** 2 / m * quad(g_sp, 0.0, 60.0, limit=200)[0])
for al in ALPHAS:
    out(f"  a={al}: " + "; ".join(f"m={m}: refit {ORA[(al, m)]['refit']:+.4f}, split {ORA[(al, m)]['split']:+.4f}"
                                  for m in MGRID))
out(f"  (risk of Xbar_n = {D * SIG ** 2 / N:.4f}; accepting the oracle always: excess d sigma^2 (m - n_e)/(n n_e))")
out("")

out("== (g) Adversarial families without held-out noise ==")
FAMX = []
for (al, m), c in CONST.items():
    x, wts, q = chi_grid(m, c.n_e)
    a = q * x
    fams = {f"reflect t={t}": (t * a, -np.ones_like(a)) for t in (0.1, 0.5, 1.0, 1.5, 1.8, 2.0, 2.2, 3.0)}
    fams["Prop4.5b"] = (2 * a + 2 * c.us, -np.ones_like(a))
    fams["worst(M_rho)"] = (np.interp(a, c.ag, c.om_star), np.clip(np.interp(a, c.ag, c.c_star), -1, 1))
    for fam, (om, cc) in fams.items():
        ex = SIG ** 2 / m * float(np.trapezoid(wts * c.f(om, cc, a), x))
        FAMX.append(dict(m=m, alpha=al, fam=fam, ex=ex, over_cap=ex / c.cap_exact, over_lower=ex / c.lower))
fx = lambda fam: [r for r in FAMX if r["fam"] == fam]
out(f"  exact (quadrature): worst(M_eta)/cap in [{min(r['over_cap'] for r in fx('worst(M_rho)')):.4f}, "
    f"{max(r['over_cap'] for r in fx('worst(M_rho)')):.4f}]; Prop4.5b/cap in [{min(r['over_cap'] for r in fx('Prop4.5b')):.4f}, "
    f"{max(r['over_cap'] for r in fx('Prop4.5b')):.4f}]; reflection t=2 / closed-form value of (iv) in "
    f"[{min(r['over_lower'] for r in fx('reflect t=2.0')):.6f}, {max(r['over_lower'] for r in fx('reflect t=2.0')):.6f}]; "
    f"largest ratio to the cap over these families {max(r['over_cap'] for r in FAMX):.4f}")
rbmax = max(adv, key=lambda r: r["rb"] / r["cap"])
COLL = {"Prop4.5b", "worst(M_rho)"} | {f for f in (r["fam"] for r in adv) if f.startswith("reflect")}
rbnc = max((r for r in adv if r["fam"] not in COLL), key=lambda r: r["rb"] / r["cap"])
out(f"  Rao-Blackwellised MC (held-out sample integrated out): max rb/cap = {rbmax['rb'] / rbmax['cap']:.4f} "
    f"({rbmax['fam']}, m={rbmax['m']}, alpha={rbmax['alpha']}); over the families that are not functions of xi: "
    f"{rbnc['rb'] / rbnc['cap']:.4f} ({rbnc['fam']}, m={rbnc['m']}, alpha={rbnc['alpha']})")
out(f"  expected number of |z| > 3 among {len(zz)} paired tests if identity (I) holds exactly: "
    f"{len(zz) * 2 * norm.sf(3):.2f}; observed {sum(x > 3 for x in zz)}")
out("")

out("== (h) alpha = 0.5: worst case of the transported refit vs exact worst case of the split, other designs ==")
GEN = []
for dd in (1, 2, 5, 50):
    for ne in (2, 10, 1000):
        for mm in (1, 3, 30):
            nn = ne + mm
            x, wts, q = chi_grid(mm, ne, npts=2001, d=dd)
            xg = np.linspace(0.0, q * x[-1], 121)
            rf_ = SIG ** 2 / mm * float(np.trapezoid(wts * np.interp(q * x, xg, M_1d(0.5, mm / nn, xg, du=0.003)), x))
            sc_ = dd * SIG ** 2 * mm / (nn * ne)
            sp_ = sc_ + SIG ** 2 / mm * float(np.trapezoid(wts * np.interp(q * x, xg, M0_split(0.5, xg)), x))
            GEN.append(dict(d=dd, n_e=ne, m=mm, refit=rf_, split=sp_, ratio=rf_ / sp_))
out(f"  {len(GEN)} designs (d in 1,2,5,50; n_e in 2,10,1000; m in 1,3,30): refit worse in "
    f"{sum(r['ratio'] > 1 for r in GEN)}; ratio refit/split in [{min(r['ratio'] for r in GEN):.3f}, "
    f"{max(r['ratio'] for r in GEN):.3f}]")
out("")
out(f"done in {time.time() - T0:.1f} s wall, {time.process_time() - C0:.1f} s CPU")

with open(os.path.join(HERE, "check_refit_output.txt"), "w") as fh:
    fh.write("\n".join(LINES) + "\n")


# ----------------------------------------------------------------------------------------------
# v0.4: machine-readable summary for experiments/make_numbers.py (frozen in results/, SHA-256 recorded)
# ----------------------------------------------------------------------------------------------
def _hold(rs, key, val="ex"):
    return int(sum(r[val][0] <= r[key] + 2 * r[val][1] for r in rs))


def _maxr(rs, key, val="ex"):
    return float(max(r[val][0] / r[key] for r in rs if r[key] > 0))


summary = dict(
    meta=dict(seed=int(sr.SEED), replicates=int(REPS), d=int(D), n=int(N), sigma=float(SIG),
              seconds=float(time.time() - T0), seconds_cpu=float(time.process_time() - C0),
              note="eta = m/n is called rho in this script"),
    constants=[dict(alpha=float(al), m=int(m), eta=float(c.rho), z=float(c.z), kappa=float(c.k), kappa2=float(c.k2),
                    kappa_phi=float(c.lam1), kbar=float(c.kbar), psi0=float(c.psi0), split=float(c.split),
                    cap_exact=float(c.cap_exact), cap_closed=float(c.cap_closed), lower=float(c.lower),
                    split_lo=float(c.split_lo), split_hi=float(c.split_hi), v1_limit=float(V1[(al, m)]),
                    # v0.5 (round 3): exact split worst case (m1), oracle C = theta (M1), 1-D reduction (m2)
                    split_exact=float(SPX[(al, m)]["total"]), split_exact_over_R=float(SPX[(al, m)]["over_R"]),
                    oracle_refit=float(ORA[(al, m)]["refit"]), oracle_split=float(ORA[(al, m)]["split"]),
                    cap_1d=float(RED[(al, m)]["cap_1d"]))
               for (al, m), c in CONST.items()],
    reduction=dict(max_M2d_minus_M1d=float(max(r["d2_minus_d1"] for r in RED.values())),
                   max_M1d_minus_M2d=float(max(r["d1_minus_d2"] for r in RED.values())),
                   max_cap_rel_diff=float(max(r["cap_rel_diff"] for r in RED.values())),
                   min_abs_c_at_2d_argmax=float(min(r["min_abs_c"] for r in RED.values()))),
    general_alpha_half=[dict(d=int(r["d"]), n_e=int(r["n_e"]), m=int(r["m"]), refit=float(r["refit"]),
                             split=float(r["split"]), ratio=float(r["ratio"])) for r in GEN],
    closed_gap_M=float(gapB), closed_gap_Psi=float(gapP),
    closed_over_exact=[float(min(c.cap_closed / c.cap_exact for c in CONST.values())),
                       float(max(c.cap_closed / c.cap_exact for c in CONST.values()))],
    design=dict(n=int(nrow), repro_max_diff=float(repro), replica_max_diff=float(dmax),
                hold={k: _hold(rows, k) for k in ("b2", "b2c", "cap", "capc")},
                max_ratio={k: _maxr(rows, k) for k in ("b2", "b2c", "cap", "capc")},
                identity_n_z=int(len(zs)), identity_max_z=float(max(zs)), identity_n_poisson=int(nrow - len(zs)),
                identity_fail=int(sum(not r["idok"] for r in rows)),
                identity_fail_at=[dict(sweep=r["sweep"], snr=float(r["snr"]), dep=float(r["dep"]), m=int(r["m"]),
                                       op=r["op"], alpha=float(r["alpha"])) for r in rows if not r["idok"]],
                simrefit_hold={k: _hold(rows, k, "simrf") for k in ("b2", "cap")},
                simrefit_max_ratio={k: _maxr(rows, k, "simrf") for k in ("b2", "cap")},
                eb10=[dict(sweep=r["sweep"], snr=float(r["snr"]), dep=float(r["dep"]), m=int(r["m"]),
                           split=float(r["split"][0]), ex=list(map(float, r["ex"])), simrf=float(r["simrf"][0]),
                           b2=float(r["b2"]), b2c=float(r["b2c"]), cap=float(r["cap"]), capc=float(r["capc"]))
                      for r in rows if r["op"] == "eb" and r["alpha"] == 0.1]),
    crossfit=dict(n=int(ncf), m_values=sorted(set(int(r["m"]) for r in cf_rows)),
                  hold={k: _hold(cf_rows, k) for k in ("b2", "cap", "capc")},
                  max_ratio={k: _maxr(cf_rows, k) for k in ("b2", "cap", "capc")},
                  jensen_hold=int(sum(r["ex"][0] <= r["jen"][0] + 1e-12 for r in cf_rows)),
                  eb10=[dict(snr=float(r["snr"]), dep=float(r["dep"]), m=int(r["m"]), ex=list(map(float, r["ex"])),
                             split=float(r["split"]), b2=float(r["b2"]), cap=float(r["cap"]))
                        for r in cf_rows if r["op"] == "eb" and r["alpha"] == 0.1]),
    adversarial=dict(n=int(nadv), hold={k: _hold(adv, k) for k in ("b2", "cap", "capc")},
                     max_ratio={k: _maxr(adv, k) for k in ("b2", "cap", "capc")},
                     identity_n=int(len(zz)), identity_max_z=float(max(zz)),
                     identity_n_above3=int(sum(x > 3 for x in zz)),
                     worst_over_cap=[float(r["ex"][0] / r["cap"]) for r in adv if r["fam"] == "worst(M_rho)"],
                     reflect_over_lower=[float(r["ex"][0] / r["lower"]) for r in adv if r["fam"] == "reflect t=2.0"],
                     # v0.5 (round 3, m3/m4): expected exceedances, Rao-Blackwellised and exact ratios
                     identity_expected_above3=float(len(zz) * 2 * norm.sf(3)),
                     rb_max_over_cap=float(rbmax["rb"] / rbmax["cap"]),
                     rb_max_over_cap_at=dict(m=int(rbmax["m"]), alpha=float(rbmax["alpha"]), family=rbmax["fam"]),
                     rb_max_over_cap_noncollinear=float(rbnc["rb"] / rbnc["cap"]),
                     rb_max_over_cap_noncollinear_at=dict(m=int(rbnc["m"]), alpha=float(rbnc["alpha"]), family=rbnc["fam"]),
                     exact_families=[dict(m=int(r["m"]), alpha=float(r["alpha"]), family=r["fam"], ex=float(r["ex"]),
                                          over_cap=float(r["over_cap"]), over_lower=float(r["over_lower"])) for r in FAMX]),
    adversarial_crossfit=dict(n=int(nacf), hold={k: _hold(advcf, k) for k in ("b2", "cap", "capc")},
                              max_ratio={k: _maxr(advcf, k) for k in ("b2", "cap", "capc")},
                              max_over_split=float(mxs["ex"][0] / mxs["split"]),
                              max_over_split_at=dict(m=int(mxs["m"]), alpha=float(mxs["alpha"]), family=mxs["fam"]),
                              worst=[dict(m=int(m), alpha=float(al),
                                          ex=float(max(r["ex"][0] for r in advcf if r["m"] == m and r["alpha"] == al)),
                                          split=float(CONST[(al, m)].split))
                                     for m in sorted(set(r["m"] for r in advcf)) for al in ALPHAS]),
)
with open(os.path.join(ROOT, "results", "refit_check.json"), "w") as fh:
    json.dump(summary, fh, indent=1)
