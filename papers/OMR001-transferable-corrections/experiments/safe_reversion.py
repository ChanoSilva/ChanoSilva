#!/usr/bin/env python3
"""OMR001 -- Correction with safe reversion: simulation study (fixed seed).

Model (Gaussian location, d coordinates, known sigma):
  * source tasks s = 1..S with means theta_s ~ N(mu, tau^2 I), each observed
    through a sample mean Xbar_s ~ N(theta_s, sigma^2/n_s I);
  * one target task with mean theta_T, observed through n = n_e + m i.i.d.
    observations N(theta_T, sigma^2 I); the first n_e form the estimation
    sample (mean Xbar_e), the last m the held-out sample (mean Ybar).
Reference estimator  R = Xbar_e   (task-specific, unbiased, minimax).
Correction operators  C(x) = mu_hat + lam (x - mu_hat)  fitted on the sources:
  'eb'    lam = tau2_hat/(tau2_hat + sigma^2/n_e)  (Efron--Morris moment estimator)
  'pool'  lam = 0  (replace the task estimate by the pooled centre)
  'fixed' lam = 1/2 (fixed in advance)
Reverting estimator (Theorem B of the manuscript):
  Dhat = ||C - Ybar||^2 - ||R - Ybar||^2   (held-out loss difference),
  s    = 2 sigma ||C - R|| / sqrt(m)       (its exact conditional sd),
  use C  iff  Dhat <= - z_{1-alpha} s,  else use R.
Also evaluated (no guarantee proved in the manuscript, empirical only):
  'refit' : same check, but the final estimate is built from all n observations;
  'sure'  : no held-out sample; use C iff SURE(C) < SURE(R) on the full sample.

Predefined criteria (U and S were fixed before the runs, see manuscript Sec. 5;
the Poisson comparison used in the identity check for rare acceptance replaced a
paired z-test after a first run showed that the normal approximation fails there):
  U  useful transfer at a configuration: the lower end of the 95% CI of the
     relative gain in risk with respect to the FULL-data reference Xbar_n is
     >= 0.05 (the split cost is charged to the method);
  S  safety: the Monte Carlo excess risk of the reverting estimator over the
     estimation-sample reference R never exceeds the bound of Theorem B(ii)
     by more than two Monte Carlo standard errors;
  H  harmful-transfer event: the corrected estimate is used and its loss is
     larger than the loss of R (frequency reported).
Outputs: results/results.json, results/tables.md, figures/*.png|pdf.
"""
import json
import os
import platform
import sys
import time

import numpy as np
from scipy.optimize import minimize_scalar
from scipy.stats import norm

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
RESULTS = os.path.join(ROOT, "results")
FIGURES = os.path.join(ROOT, "figures")
os.makedirs(RESULTS, exist_ok=True)
os.makedirs(FIGURES, exist_ok=True)

SEED = 20260930
FAST = "--fast" in sys.argv

CFG = dict(
    d=5,
    sigma=1.0,
    S=30,            # number of source tasks
    n_s=60,          # observations per source task
    n=60,            # observations in the target task (estimation + held-out)
    m_default=12,    # held-out size (20% of the target sample)
    R=4000 if FAST else 20000,   # Monte Carlo replicates per configuration
    snr_grid=[0.0, 0.25, 0.5, 1.0, 2.0, 4.0, 8.0, 16.0],  # tau^2 / (sigma^2/n_e)
    alpha_grid=[0.5, 0.2, 0.1, 0.05, 0.01],
    dep_grid=[0.0, 2.0, 4.0, 6.0, 8.0, 12.0, 16.0],       # shift of the target, in units of tau
    snr_dep=1.0,     # snr used in the departure and held-out-size sweeps
    m_grid=[3, 6, 12, 24],
    useful_threshold=0.05,
    operators=["eb", "pool", "fixed"],
)
PHI0 = float(norm.pdf(0.0))
PHI1 = float(norm.pdf(1.0))   # sup_x x phi(x)


# ----------------------------------------------------------------------------
# Constants of Theorem B: kappa(alpha) = sup_u u Phi(-(z+u)) versus phi(z)
# ----------------------------------------------------------------------------
def kappa(alpha):
    z = norm.ppf(1 - alpha)
    f = lambda u: -u * norm.cdf(-(z + u))
    res = minimize_scalar(f, bounds=(0.0, 20.0), method="bounded",
                          options={"xatol": 1e-10})
    return float(-res.fun), float(res.x)


def constants_table():
    rows = []
    for a in CFG["alpha_grid"]:
        z = float(norm.ppf(1 - a))
        k, ustar = kappa(a)
        rows.append(dict(alpha=a, z=z, phi_z=float(norm.pdf(z)), kappa=k,
                         u_star=ustar, ratio_kappa_over_phi=k / float(norm.pdf(z)),
                         regret_const=z + PHI0))
    return rows


# ----------------------------------------------------------------------------
# One batch of replicates
# ----------------------------------------------------------------------------
def simulate(rng, snr, dep_over_tau, m, tau2=None):
    """One batch.  By default tau^2 = snr * sigma^2/n_e with n_e = n - m; the held-out
    size sweep passes tau2 explicitly so that the task distribution does not move with m
    (referee round 1, M1)."""
    d, sigma, S, n_s, n, R = (CFG[k] for k in ("d", "sigma", "S", "n_s", "n", "R"))
    n_e = n - m
    se2_e = sigma ** 2 / n_e
    se2_n = sigma ** 2 / n
    if tau2 is None:
        tau2 = snr * se2_e
    tau = np.sqrt(tau2)
    mu = np.zeros(d)  # the operators estimate mu; the risks do not depend on it

    # sources
    theta_s = mu + tau * rng.standard_normal((R, S, d))
    Xs = theta_s + (sigma / np.sqrt(n_s)) * rng.standard_normal((R, S, d))
    mu_hat = Xs.mean(axis=1)                                   # (R, d)
    v_hat = ((Xs - mu_hat[:, None, :]) ** 2).sum(axis=(1, 2)) / ((S - 1) * d)
    tau2_hat = np.maximum(v_hat - sigma ** 2 / n_s, 0.0)
    lam_e = tau2_hat / (tau2_hat + se2_e)
    lam_n = tau2_hat / (tau2_hat + se2_n)

    # target
    shift = np.zeros(d)
    shift[0] = dep_over_tau * tau
    theta = mu + shift + tau * rng.standard_normal((R, d))
    Xe = theta + np.sqrt(se2_e) * rng.standard_normal((R, d))
    Yb = theta + (sigma / np.sqrt(m)) * rng.standard_normal((R, d))
    Xn = (n_e * Xe + m * Yb) / n

    sq = lambda v: (v ** 2).sum(axis=1)
    out = dict(L_Re=sq(Xe - theta), L_Rn=sq(Xn - theta), lam_e=lam_e, tau2=tau2,
               dist_center=np.sqrt(sq(Xe - mu_hat)), ops={})
    lams = {"eb": (lam_e, lam_n),
            "pool": (np.zeros(R), np.zeros(R)),
            "fixed": (0.5 * np.ones(R), 0.5 * np.ones(R))}
    for name in CFG["operators"]:
        le, ln = lams[name]
        b = mu_hat + le[:, None] * (Xe - mu_hat)
        bn = mu_hat + ln[:, None] * (Xn - mu_hat)
        L_b, L_bn = sq(b - theta), sq(bn - theta)
        Delta = L_b - out["L_Re"]
        Dhat = sq(b - Yb) - sq(Xe - Yb)
        s = 2.0 * sigma * np.sqrt(sq(b - Xe)) / np.sqrt(m)
        # SURE on the full sample: risk(C_n) - risk(R_n) is estimated without bias by
        # (1-lam)[(1-lam)||Xn-mu_hat||^2 - 2 d sigma^2/n]
        sure_diff = (1 - ln) * ((1 - ln) * sq(Xn - mu_hat) - 2 * d * se2_n)
        acc_sure = sure_diff < 0
        out["ops"][name] = dict(L_b=L_b, L_bn=L_bn, Delta=Delta, Dhat=Dhat, s=s,
                                L_sure=out["L_Rn"] + (L_bn - out["L_Rn"]) * acc_sure,
                                acc_sure=acc_sure, Delta_n=L_bn - out["L_Rn"])
    return out


# ----------------------------------------------------------------------------
# Summaries
# ----------------------------------------------------------------------------
def mse(x):
    x = np.asarray(x, dtype=float)
    return float(x.mean()), float(x.std(ddof=1) / np.sqrt(x.size))


def rel_gain(L_ref, L):
    """Relative gain (risk_ref - risk)/risk_ref with a paired 95% CI (delta method,
    denominator treated as fixed; its relative SE is < 1% in all runs)."""
    diff = L_ref - L
    md, sd = mse(diff)
    ref = float(L_ref.mean())
    return dict(gain=md / ref, lo=(md - 1.96 * sd) / ref, hi=(md + 1.96 * sd) / ref)


def evaluate(sim, m):
    """Per-operator, per-alpha summaries for one batch."""
    L_Re, L_Rn = sim["L_Re"], sim["L_Rn"]
    thr = CFG["useful_threshold"]
    res = dict(risk_Re=mse(L_Re), risk_Rn=mse(L_Rn),
               mean_lam_eb=float(sim["lam_e"].mean()), ops={})
    for name, o in sim["ops"].items():
        Delta, Dhat, s = o["Delta"], o["Dhat"], o["s"]
        Dplus = np.maximum(Delta, 0.0)
        always = dict(risk=mse(o["L_b"]), gain_vs_Rn=rel_gain(L_Rn, o["L_b"]),
                      gain_vs_Re=rel_gain(L_Re, o["L_b"]),
                      excess_vs_Re=mse(Delta), harm_freq=float((Delta > 0).mean()),
                      mean_norm_CminusR=float((s * np.sqrt(m) / (2 * CFG["sigma"])).mean()),
                      mean_Dplus=float(Dplus.mean()),
                      risk_refit_always=mse(o["L_bn"]),
                      gain_refit_always_vs_Rn=rel_gain(L_Rn, o["L_bn"]))
        always["useful"] = bool(always["gain_vs_Rn"]["lo"] >= thr)
        # practical always-correct: the operator applied to the full-data estimate (no split)
        always_full = dict(risk=mse(o["L_bn"]), gain_vs_Rn=rel_gain(L_Rn, o["L_bn"]),
                           harm_freq=float((o["Delta_n"] > 0).mean()),
                           excess_vs_Rn=mse(o["Delta_n"]))
        always_full["useful"] = bool(always_full["gain_vs_Rn"]["lo"] >= thr)
        oracle = dict(risk_min=mse(np.minimum(L_Re, o["L_b"])))
        sure = dict(risk=mse(o["L_sure"]), gain_vs_Rn=rel_gain(L_Rn, o["L_sure"]),
                    accept_freq=float(o["acc_sure"].mean()),
                    harm_freq=float((o["acc_sure"] & (o["Delta_n"] > 0)).mean()))
        sure["useful"] = bool(sure["gain_vs_Rn"]["lo"] >= thr)
        rev = {}
        for a in CFG["alpha_grid"]:
            z = float(norm.ppf(1 - a))
            acc = Dhat <= -z * s
            L_rev = L_Re + Delta * acc
            with np.errstate(divide="ignore", invalid="ignore"):
                p_acc = np.where(s > 0, norm.cdf(-(Delta + z * s) / np.where(s > 0, s, 1.0)), 0.0)
            L_rev_rb = L_Re + Delta * p_acc            # Rao-Blackwell (identity B(i))
            L_refit = L_Rn + o["Delta_n"] * acc
            ex_mc = mse(Delta * acc)
            ex_rb = mse(Delta * p_acc)
            bound_alpha = a * float(Dplus.mean())
            bound_phi = float(norm.pdf(z)) * float(s.mean())
            bound_tight = float((Dplus * p_acc).mean())
            regret_bound = (z + PHI0) * float(s.mean())
            # uniform cap (Corollary 'uniform cap' of the manuscript): for ANY F-measurable C
            # and every theta,  E[Delta^+ pi] <= 4 sigma phi(z) E||R-theta|| / sqrt(m) + 4 phi(1) sigma^2 / m,
            # with E||R-theta|| <= sigma_e sqrt(d).  Closed form below (no Monte Carlo input).
            n_e = CFG["n"] - m
            sig = CFG["sigma"]
            bound_uniform = 4 * sig ** 2 * (float(norm.pdf(z)) * np.sqrt(CFG["d"] / (n_e * m)) + PHI1 / m)
            r = dict(alpha=a, z=z, risk=mse(L_rev), risk_rb=mse(L_rev_rb),
                     gain_vs_Rn=rel_gain(L_Rn, L_rev), gain_vs_Re=rel_gain(L_Re, L_rev),
                     excess_vs_Re=ex_mc, excess_vs_Re_rb=ex_rb,
                     bound_alpha=bound_alpha, bound_phi=bound_phi, bound_tight=bound_tight,
                     regret_vs_oracle=mse(L_rev - np.minimum(L_Re, o["L_b"])),
                     regret_bound=regret_bound, bound_uniform=bound_uniform,
                     accept_freq=float(acc.mean()),
                     harm_freq=float((acc & (Delta > 0)).mean()),
                     accept_given_harmful=float(acc[Delta > 0].mean()) if (Delta > 0).any() else 0.0,
                     risk_refit=mse(L_refit), gain_refit_vs_Rn=rel_gain(L_Rn, L_refit),
                     harm_freq_refit=float((acc & (o["Delta_n"] > 0)).mean()))
            r["useful"] = bool(r["gain_vs_Rn"]["lo"] >= thr)
            r["useful_refit"] = bool(r["gain_refit_vs_Rn"]["lo"] >= thr)
            r["safe_phi"] = bool(ex_mc[0] <= bound_phi + 2 * ex_mc[1])
            r["safe_alpha"] = bool(ex_mc[0] <= bound_alpha + 2 * ex_mc[1])
            r["safe_tight"] = bool(ex_mc[0] <= bound_tight + 2 * ex_mc[1])
            r["safe_uniform"] = bool(ex_mc[0] <= bound_uniform + 2 * ex_mc[1])
            hf = r["harm_freq"]; hb = a * always["harm_freq"]     # Corollary: P(harmful event) <= alpha P(Delta>0)
            r["harm_freq_bound"] = hb
            r["safe_harm_freq"] = bool(hf <= hb + 2 * np.sqrt(max(hf * (1 - hf), 1e-12) / Delta.size))
            # identity B(i): E[Delta 1_A] = E[Delta P(A|F)].  Paired z-test where acceptance is
            # frequent (>= 1%); where it is rare, compare the acceptance count with its expected
            # value sum(p_acc) through a Poisson 99% interval (the CLT does not apply there).
            idm, ids = mse(Delta * (acc - p_acc))
            n_acc, e_acc = int(acc.sum()), float(p_acc.sum())
            r["accept_count"], r["accept_expected"] = n_acc, e_acc
            if acc.mean() >= 0.01:
                r["identity_z"] = float(idm / ids) if ids > 0 else 0.0
                r["identity_ok"] = bool(abs(r["identity_z"]) <= 3.0)
            else:
                from scipy.stats import poisson
                lo, hi = poisson.ppf(0.005, e_acc), poisson.ppf(0.995, e_acc)
                r["identity_z"] = None
                r["identity_ok"] = bool(lo <= n_acc <= hi) if e_acc > 0 else bool(n_acc == 0)
            rev[str(a)] = r
        res["ops"][name] = dict(always=always, always_full=always_full, oracle=oracle, sure=sure, rev=rev)
    return res


# ----------------------------------------------------------------------------
# Sweeps
# ----------------------------------------------------------------------------
def run_all():
    rng = np.random.default_rng(SEED)
    m0 = CFG["m_default"]
    n_e0 = CFG["n"] - m0
    structure, departure, msweep = [], [], []
    for snr in CFG["snr_grid"]:
        sim = simulate(rng, snr, 0.0, m0)
        r = evaluate(sim, m0)
        r.update(snr=snr, m=m0, n_e=n_e0, lam_oracle=snr / (1 + snr), tau2=sim["tau2"],
                 tau=float(np.sqrt(snr * CFG["sigma"] ** 2 / n_e0)),
                 bayes_oracle_risk=CFG["d"] * CFG["sigma"] ** 2 / n_e0 * snr / (1 + snr))
        structure.append(r)
        print(f"structure snr={snr:5.2f}  R_e={r['risk_Re'][0]:.4f} R_n={r['risk_Rn'][0]:.4f} "
              f"always={r['ops']['eb']['always']['risk'][0]:.4f} "
              f"rev(0.1)={r['ops']['eb']['rev']['0.1']['risk'][0]:.4f}", flush=True)
    for dep in CFG["dep_grid"]:
        sim = simulate(rng, CFG["snr_dep"], dep, m0)
        r = evaluate(sim, m0)
        r.update(snr=CFG["snr_dep"], dep_over_tau=dep, m=m0, n_e=n_e0, tau2=sim["tau2"],
                 tau=float(np.sqrt(CFG["snr_dep"] * CFG["sigma"] ** 2 / n_e0)))
        departure.append(r)
        print(f"departure dep={dep:5.1f}tau always={r['ops']['eb']['always']['risk'][0]:.4f} "
              f"rev(0.1)={r['ops']['eb']['rev']['0.1']['risk'][0]:.4f} "
              f"excess={r['ops']['eb']['rev']['0.1']['excess_vs_Re'][0]:.5f} "
              f"bound_phi={r['ops']['eb']['rev']['0.1']['bound_phi']:.4f}", flush=True)
    # held-out size sweep: tau^2 is held at its m = m_default value (sigma^2/48 here) for
    # every m, so that only the split moves; 'snr' in these rows is relative to n_e0
    tau2_fixed = CFG["snr_dep"] * CFG["sigma"] ** 2 / n_e0
    for m in CFG["m_grid"]:
        for dep in [0.0, 8.0]:
            sim = simulate(rng, CFG["snr_dep"], dep, m, tau2=tau2_fixed)
            r = evaluate(sim, m)
            r.update(snr=CFG["snr_dep"], dep_over_tau=dep, m=m, n_e=CFG["n"] - m,
                     tau2=tau2_fixed, tau2_fixed_at_m=m0,
                     snr_vs_own_ne=tau2_fixed / (CFG["sigma"] ** 2 / (CFG["n"] - m)))
            msweep.append(r)
            print(f"m-sweep m={m:3d} dep={dep:4.1f} rev(0.1)={r['ops']['eb']['rev']['0.1']['risk'][0]:.4f} "
                  f"R_n={r['risk_Rn'][0]:.4f}", flush=True)
    return structure, departure, msweep


def summarize(structure, departure, msweep, consts):
    alphas = [str(a) for a in CFG["alpha_grid"]]
    allrev = [(r, name, a, r["ops"][name]["rev"][a])
              for r in structure + departure + msweep
              for name in CFG["operators"] for a in alphas]
    summary = dict(
        n_configs_rev=len(allrev),
        safe_phi_all=all(x[3]["safe_phi"] for x in allrev),
        safe_alpha_all=all(x[3]["safe_alpha"] for x in allrev),
        safe_tight_all=all(x[3]["safe_tight"] for x in allrev),
        safe_harm_freq_all=all(x[3]["safe_harm_freq"] for x in allrev),
        safe_uniform_all=all(x[3]["safe_uniform"] for x in allrev),
        max_excess_over_bound_uniform=max(x[3]["excess_vs_Re"][0] / x[3]["bound_uniform"] for x in allrev),
        max_bound_phi_over_uniform=max(x[3]["bound_phi"] / x[3]["bound_uniform"] for x in allrev),
        useful_structure_always_full_eb=[r["snr"] for r in structure if r["ops"]["eb"]["always_full"]["useful"]],
        harmful_vs_Rn_always_full_eb_structure=[r["snr"] for r in structure
                                                if r["ops"]["eb"]["always_full"]["gain_vs_Rn"]["hi"] < 0],
        harmful_vs_Rn_always_full_eb_departure=[r["dep_over_tau"] for r in departure
                                                if r["ops"]["eb"]["always_full"]["gain_vs_Rn"]["hi"] < 0],
        harmful_vs_Rn_sure_eb_departure=[r["dep_over_tau"] for r in departure
                                         if r["ops"]["eb"]["sure"]["gain_vs_Rn"]["hi"] < 0],
        harmful_vs_Rn_refit_eb_departure={a: [r["dep_over_tau"] for r in departure
                                              if r["ops"]["eb"]["rev"][a]["gain_refit_vs_Rn"]["hi"] < 0]
                                          for a in alphas},
        max_identity_abs_z=max(abs(x[3]["identity_z"]) for x in allrev if x[3]["identity_z"] is not None),
        n_identity_clt=sum(1 for x in allrev if x[3]["identity_z"] is not None),
        n_identity_poisson=sum(1 for x in allrev if x[3]["identity_z"] is None),
        identity_ok_all=all(x[3]["identity_ok"] for x in allrev),
        n_identity_fail=sum(1 for x in allrev if not x[3]["identity_ok"]),
        max_excess_over_bound_phi=max(x[3]["excess_vs_Re"][0] / x[3]["bound_phi"]
                                      for x in allrev if x[3]["bound_phi"] > 0),
        max_regret_over_bound=max(x[3]["regret_vs_oracle"][0] / x[3]["regret_bound"]
                                  for x in allrev if x[3]["regret_bound"] > 0),
        useful_structure_eb={a: [r["snr"] for r in structure if r["ops"]["eb"]["rev"][a]["useful"]]
                             for a in alphas},
        useful_structure_always_eb=[r["snr"] for r in structure if r["ops"]["eb"]["always"]["useful"]],
        useful_structure_sure_eb=[r["snr"] for r in structure if r["ops"]["eb"]["sure"]["useful"]],
        useful_structure_refit_eb={a: [r["snr"] for r in structure if r["ops"]["eb"]["rev"][a]["useful_refit"]]
                                   for a in alphas},
        harmful_vs_Rn_always_eb_departure=[r["dep_over_tau"] for r in departure
                                           if r["ops"]["eb"]["always"]["gain_vs_Rn"]["hi"] < 0],
        harmful_vs_Rn_rev_eb_departure={a: [r["dep_over_tau"] for r in departure
                                            if r["ops"]["eb"]["rev"][a]["gain_vs_Rn"]["hi"] < 0]
                                        for a in alphas},
        max_harm_freq_rev_eb={a: max(r["ops"]["eb"]["rev"][a]["harm_freq"] for r in structure + departure)
                              for a in alphas},
        max_harm_freq_always_eb=max(r["ops"]["eb"]["always"]["harm_freq"] for r in structure + departure),
        max_accept_given_harmful_eb={a: max(r["ops"]["eb"]["rev"][a]["accept_given_harmful"]
                                            for r in structure + departure) for a in alphas},
        worst_always_eb_departure=max(departure, key=lambda r: r["ops"]["eb"]["always"]["risk"][0]),
    )
    w = summary.pop("worst_always_eb_departure")
    summary["worst_departure"] = dict(dep_over_tau=w["dep_over_tau"],
                                      always_risk=w["ops"]["eb"]["always"]["risk"][0],
                                      risk_Re=w["risk_Re"][0], risk_Rn=w["risk_Rn"][0],
                                      rev={a: w["ops"]["eb"]["rev"][a]["risk"][0] for a in alphas},
                                      excess={a: w["ops"]["eb"]["rev"][a]["excess_vs_Re"][0] for a in alphas},
                                      bound_phi={a: w["ops"]["eb"]["rev"][a]["bound_phi"] for a in alphas},
                                      bound_alpha={a: w["ops"]["eb"]["rev"][a]["bound_alpha"] for a in alphas})
    summary["constants"] = consts
    return summary


# ----------------------------------------------------------------------------
# Markdown tables
# ----------------------------------------------------------------------------
def write_tables(structure, departure, msweep, consts, summary, path):
    alphas = [str(a) for a in CFG["alpha_grid"]]
    L = ["# OMR001 -- safe reversion: tables (seed %d, R=%d)\n" % (SEED, CFG["R"])]
    L.append("Risks are mean squared errors (d=%d coordinates); +- is one Monte Carlo SE. "
             "'gain' is relative to the full-data reference Xbar_n; U = useful (lower 95%% CI of gain >= %.2f).\n"
             % (CFG["d"], CFG["useful_threshold"]))
    L.append("## T1. Structure sweep (EB operator, target from the hierarchy, m=%d)\n" % CFG["m_default"])
    L.append("| snr | lam* | R_e | R_n | always_e | always_n | gain_n | harm%_n | " + " | ".join(f"rev a={a}" for a in alphas) +
             " | " + " | ".join(f"gain a={a}" for a in alphas) + " | SURE | refit a=0.1 |")
    L.append("|" + "---|" * (9 + 2 * len(alphas) + 2))
    for r in structure:
        e = r["ops"]["eb"]
        L.append(f"| {r['snr']:.2f} | {r['lam_oracle']:.2f} | {r['risk_Re'][0]:.4f} | {r['risk_Rn'][0]:.4f} | "
                 f"{e['always']['risk'][0]:.4f} | {e['always_full']['risk'][0]:.4f} | {100*e['always_full']['gain_vs_Rn']['gain']:+.1f}%{'U' if e['always_full']['useful'] else ''} | "
                 f"{100*e['always_full']['harm_freq']:.1f} | " +
                 " | ".join(f"{e['rev'][a]['risk'][0]:.4f}" for a in alphas) + " | " +
                 " | ".join(f"{100*e['rev'][a]['gain_vs_Rn']['gain']:+.1f}%{'U' if e['rev'][a]['useful'] else ''}" for a in alphas) +
                 f" | {e['sure']['risk'][0]:.4f} ({100*e['sure']['gain_vs_Rn']['gain']:+.1f}%{'U' if e['sure']['useful'] else ''})"
                 f" | {e['rev']['0.1']['risk_refit'][0]:.4f} ({100*e['rev']['0.1']['gain_refit_vs_Rn']['gain']:+.1f}%{'U' if e['rev']['0.1']['useful_refit'] else ''}) |")
    L.append("\n## T2. Departure sweep (EB operator, snr=%.1f, target shifted by dep x tau, m=%d)\n" % (CFG["snr_dep"], CFG["m_default"]))
    L.append("| dep/tau | R_e | R_n | always_e | always_n | harm%_e | " + " | ".join(f"rev a={a}" for a in alphas) + " | " +
             " | ".join(f"harm% a={a}" for a in alphas) + " | excess a=0.1 (MC) | bound tight | bound phi | bound alpha | SURE | refit a=0.1 |")
    L.append("|" + "---|" * (12 + 2 * len(alphas)))
    for r in departure:
        e = r["ops"]["eb"]
        q = e["rev"]["0.1"]
        L.append(f"| {r['dep_over_tau']:.0f} | {r['risk_Re'][0]:.4f} | {r['risk_Rn'][0]:.4f} | {e['always']['risk'][0]:.4f} | {e['always_full']['risk'][0]:.4f} | "
                 f"{100*e['always']['harm_freq']:.1f} | " +
                 " | ".join(f"{e['rev'][a]['risk'][0]:.4f}" for a in alphas) + " | " +
                 " | ".join(f"{100*e['rev'][a]['harm_freq']:.1f}" for a in alphas) +
                 f" | {q['excess_vs_Re'][0]:+.5f} +- {q['excess_vs_Re'][1]:.5f} | {q['bound_tight']:.5f} | {q['bound_phi']:.4f} | {q['bound_alpha']:.4f}"
                 f" | {e['sure']['risk'][0]:.4f} | {q['risk_refit'][0]:.4f} |")
    L.append("\n## T3. Held-out size (EB operator, tau^2 fixed at snr=%.1f relative to n_e=%d, alpha=0.1)\n"
             % (CFG["snr_dep"], CFG["n"] - CFG["m_default"]))
    L.append("| m | n_e | dep/tau | R_e | R_n | always_e | always_n | rev | gain rev | excess (MC) | bound phi | refit | SURE |")
    L.append("|---|---|---|---|---|---|---|---|---|---|---|---|---|")
    for r in msweep:
        e = r["ops"]["eb"]; q = e["rev"]["0.1"]
        L.append(f"| {r['m']} | {r['n_e']} | {r['dep_over_tau']:.0f} | {r['risk_Re'][0]:.4f} | {r['risk_Rn'][0]:.4f} | "
                 f"{e['always']['risk'][0]:.4f} | {e['always_full']['risk'][0]:.4f} | {q['risk'][0]:.4f} | {100*q['gain_vs_Rn']['gain']:+.1f}% | "
                 f"{q['excess_vs_Re'][0]:+.5f} | {q['bound_phi']:.4f} | {q['risk_refit'][0]:.4f} | {e['sure']['risk'][0]:.4f} |")
    L.append("\n## T4. Other operators (alpha=0.1, m=%d, target from the hierarchy)\n" % CFG["m_default"])
    L.append("| snr | operator | always | harm% | rev | harm% rev | excess (MC) | bound phi | bound alpha |")
    L.append("|---|---|---|---|---|---|---|---|---|")
    for r in structure:
        if r["snr"] not in (0.0, 1.0, 4.0, 16.0):
            continue
        for name in CFG["operators"]:
            e = r["ops"][name]; q = e["rev"]["0.1"]
            L.append(f"| {r['snr']:.0f} | {name} | {e['always']['risk'][0]:.4f} | {100*e['always']['harm_freq']:.1f} | "
                     f"{q['risk'][0]:.4f} | {100*q['harm_freq']:.1f} | {q['excess_vs_Re'][0]:+.5f} | {q['bound_phi']:.4f} | {q['bound_alpha']:.4f} |")
    L.append("\n## T5. Constants of Theorem B\n")
    L.append("| alpha | z | phi(z) | kappa(alpha) | u* | kappa/phi | z+phi(0) |")
    L.append("|---|---|---|---|---|---|---|")
    for c in consts:
        L.append(f"| {c['alpha']} | {c['z']:.3f} | {c['phi_z']:.4f} | {c['kappa']:.4f} | {c['u_star']:.3f} | {c['ratio_kappa_over_phi']:.3f} | {c['regret_const']:.3f} |")
    L.append("\n## Summary checks\n")
    for k in ("n_configs_rev", "safe_phi_all", "safe_alpha_all", "safe_tight_all", "safe_harm_freq_all",
              "safe_uniform_all", "max_excess_over_bound_uniform", "max_bound_phi_over_uniform", "max_identity_abs_z",
              "n_identity_clt", "n_identity_poisson", "identity_ok_all", "n_identity_fail",
              "max_excess_over_bound_phi", "max_regret_over_bound",
              "useful_structure_eb", "useful_structure_always_eb", "useful_structure_always_full_eb", "useful_structure_sure_eb",
              "harmful_vs_Rn_always_full_eb_structure", "harmful_vs_Rn_always_full_eb_departure",
              "harmful_vs_Rn_sure_eb_departure", "harmful_vs_Rn_refit_eb_departure",
              "useful_structure_refit_eb", "harmful_vs_Rn_always_eb_departure", "harmful_vs_Rn_rev_eb_departure",
              "max_harm_freq_rev_eb", "max_harm_freq_always_eb", "max_accept_given_harmful_eb", "worst_departure",
              "identity_recheck"):
        L.append(f"- {k}: {json.dumps(summary[k])}")
    with open(path, "w") as fh:
        fh.write("\n".join(L) + "\n")


# ----------------------------------------------------------------------------
# Figures (palette: dataviz reference instance; text never wears series colour)
# ----------------------------------------------------------------------------
def make_figures(structure, departure):
    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt
    C = dict(blue="#2a78d6", orange="#eb6834", aqua="#1baf7a", yellow="#eda100",
             violet="#4a3aa7", green="#008300", grid="#e6e5e1", text="#0b0b0b", text2="#52514e")
    plt.rcParams.update({"font.size": 9, "axes.edgecolor": C["text2"], "axes.labelcolor": C["text"],
                         "xtick.color": C["text2"], "ytick.color": C["text2"], "axes.spines.top": False,
                         "axes.spines.right": False, "legend.frameon": False})
    mk = dict(marker="o", markersize=6, markeredgecolor="white", markeredgewidth=1.5, linewidth=2)

    def style(ax):
        ax.grid(True, axis="y", color=C["grid"], linewidth=1.0)
        ax.set_axisbelow(True)

    def get(r, kind, a=None, field="risk"):
        e = r["ops"]["eb"]
        if kind == "rev":
            return e["rev"][a][field][0]
        if kind == "refit":
            return e["rev"][a]["risk_refit"][0]
        return e[kind]["risk"][0]

    left = [("always correct, all data", "always_full", None, C["orange"]),
            (r"revert, $\alpha$=0.5 (plain hold-out)", "rev", "0.5", C["aqua"]),
            (r"revert, $\alpha$=0.1", "rev", "0.1", C["blue"]),
            (r"revert, $\alpha$=0.01", "rev", "0.01", C["violet"])]
    right = [("always correct, all data", "always_full", None, C["orange"]),
             (r"refit after check, $\alpha$=0.1", "refit", "0.1", C["aqua"]),
             ("SURE reversion, no split", "sure", None, C["blue"])]

    def panel_pair(rows, x, xlabel, fname, title, xscale=None, yscale=None, legend_loc="best"):
        Rn = np.array([r["risk_Rn"][0] for r in rows])
        fig, axes = plt.subplots(1, 2, figsize=(8.4, 3.5), sharey=True)
        for ax, series, sub in zip(axes, (left, right),
                                   ("(a) with the guarantee of Theorem B", "(b) without guarantee (empirical)")):
            ax.axhline(1.0, color=C["text2"], linewidth=1.0)
            if sub.startswith("(a)"):
                ax.plot(x, [r["risk_Re"][0] for r in rows] / Rn, color=C["text2"], linewidth=2,
                        linestyle=(0, (4, 3)), label="reference on estimation sample (split cost)")
            for lab, kind, a, col in series:
                y = np.array([get(r, kind, a) for r in rows]) / Rn
                ax.plot(x, y, color=col, label=lab, **mk)
            if xscale == "symlog":
                ax.set_xscale("symlog", linthresh=0.25)
                ax.set_xticks(x); ax.set_xticklabels([f"{v:g}" for v in x])
            if yscale:
                ax.set_yscale(yscale)
            ax.set_title(sub, loc="left", color=C["text"], fontsize=9)
            ax.legend(fontsize=7.5, loc=legend_loc)
            style(ax)
        axes[0].set_ylabel("risk / risk of full-data reference" + (" (log)" if yscale else ""))
        fig.suptitle(title, x=0.01, ha="left", color=C["text"], fontsize=10)
        fig.supxlabel(xlabel, fontsize=9, color=C["text"])
        fig.tight_layout()
        fig.savefig(os.path.join(FIGURES, fname + ".png"), dpi=200)
        fig.savefig(os.path.join(FIGURES, fname + ".pdf"))
        plt.close(fig)

    panel_pair(structure, [r["snr"] for r in structure],
               r"shared structure: snr $=\tau^2/(\sigma^2/n_e)$ (smaller = tasks more alike)",
               "structure_sweep", "Structure sweep: target drawn from the hierarchy (EB operator, m = %d)" % CFG["m_default"],
               xscale="symlog", legend_loc="lower right")
    panel_pair(departure, [r["dep_over_tau"] for r in departure],
               r"departure of the target from the shared centre, in units of $\tau$ (snr = 1)",
               "departure_sweep", "Departure sweep: negative transfer and its cap (EB operator, m = %d)" % CFG["m_default"],
               yscale="log", legend_loc="upper left")

    # Combined figure for the manuscript (one row): guaranteed estimators on both sweeps
    fig, axes = plt.subplots(1, 2, figsize=(8.4, 3.4))
    for ax, rows, xx, xlabel, sub, xscale, yscale, loc in (
            (axes[0], structure, [r["snr"] for r in structure],
             r"snr $=\tau^2/(\sigma^2/n_e)$ (smaller = tasks more alike)",
             "(a) structure sweep: target from the hierarchy", "symlog", None, "lower right"),
            (axes[1], departure, [r["dep_over_tau"] for r in departure],
             r"departure of the target from the centre, in units of $\tau$ (snr = 1)",
             "(b) departure sweep: negative transfer and its cap (log)", None, "log", "upper left")):
        Rn = np.array([r["risk_Rn"][0] for r in rows])
        ax.axhline(1.0, color=C["text2"], linewidth=1.0)
        ax.plot(xx, [r["risk_Re"][0] for r in rows] / Rn, color=C["text2"], linewidth=2,
                linestyle=(0, (4, 3)), label="reference on estimation sample (split cost)")
        for lab, kind, a, col in left:
            y = np.array([get(r, kind, a) for r in rows]) / Rn
            ax.plot(xx, y, color=col, label=lab, **mk)
        if xscale == "symlog":
            ax.set_xscale("symlog", linthresh=0.25)
            ax.set_xticks(xx); ax.set_xticklabels([f"{v:g}" for v in xx])
        if yscale:
            ax.set_yscale(yscale)
        ax.set_title(sub, loc="left", color=C["text"], fontsize=9)
        ax.set_xlabel(xlabel, fontsize=9, color=C["text"])
        ax.legend(fontsize=7.5, loc=loc)
        style(ax)
    axes[0].set_ylabel("risk / risk of full-data reference")
    fig.suptitle("Reverting estimators with the guarantee of Theorem B (EB operator, m = %d)" % CFG["m_default"],
                 x=0.01, ha="left", color=C["text"], fontsize=10)
    fig.tight_layout()
    fig.savefig(os.path.join(FIGURES, "sweeps.png"), dpi=200)
    fig.savefig(os.path.join(FIGURES, "sweeps.pdf"))
    plt.close(fig)

    # Figure 3: excess over the reference versus the bounds of Theorem B (alpha = 0.1)
    fig, ax = plt.subplots(figsize=(6.0, 3.6))
    x = np.array([r["dep_over_tau"] for r in departure])
    q = [r["ops"]["eb"]["rev"]["0.1"] for r in departure]
    ex = np.array([v["excess_vs_Re"][0] for v in q]); se = np.array([v["excess_vs_Re"][1] for v in q])
    ax.plot(x, [v["bound_alpha"] for v in q], color=C["yellow"], label=r"bound $\alpha\,E[\Delta^+]$", **mk)
    ax.plot(x, [v["bound_phi"] for v in q], color=C["orange"], label=r"bound $\varphi(z_{1-\alpha})\,E[s]$", **mk)
    ax.plot(x, [v["bound_tight"] for v in q], color=C["aqua"], label=r"bound $E[\Delta^+\Phi(-(\Delta^+ + c)/s)]$", **mk)
    pos = ex > 0
    ax.errorbar(x[pos], ex[pos], yerr=2 * se[pos], color=C["blue"], capsize=2,
                label=r"Monte Carlo excess risk ($\pm$2 SE); shown only where $>0$", **mk)
    ax.set_yscale("log")
    ax.set_xlabel(r"departure of the target, in units of $\tau$ (snr = 1, $\alpha$ = 0.1)")
    ax.set_ylabel("excess risk over reference $R$ (log)")
    ax.set_title("Do no harm: excess risk of the reverting estimator vs. Theorem B", loc="left", color=C["text"])
    ax.legend(fontsize=7.5, loc="lower right")
    style(ax)
    fig.tight_layout()
    fig.savefig(os.path.join(FIGURES, "excess_vs_bounds.png"), dpi=200)
    fig.savefig(os.path.join(FIGURES, "excess_vs_bounds.pdf"))
    plt.close(fig)


# ----------------------------------------------------------------------------
# Re-checks of identity B(i) with their own random streams (the sweeps are unchanged)
# ----------------------------------------------------------------------------
def identity_recheck(structure, departure, msweep):
    """(a) one fixed triple (R, C, theta) and many independent held-out draws: the
    acceptance frequency must match Phi(-(Delta + z s)/s);  (b) the rare-event
    configuration with the largest count deficit in the main run is re-simulated with
    independent seeds and the acceptance count is compared with sum(p_acc)."""
    d, sigma = CFG["d"], CFG["sigma"]
    rng = np.random.default_rng(SEED + 1)
    m, n_e = CFG["m_default"], CFG["n"] - CFG["m_default"]
    theta = np.zeros(d); theta[0] = 8 * np.sqrt(sigma ** 2 / n_e)
    a = theta + np.sqrt(sigma ** 2 / n_e) * rng.standard_normal(d)
    b = np.full(d, 0.02)
    Delta = float(((b - theta) ** 2).sum() - ((a - theta) ** 2).sum())
    s = 2 * sigma * float(np.linalg.norm(b - a)) / np.sqrt(m)
    ndraw = 50000 if FAST else 200000
    Yb = theta + (sigma / np.sqrt(m)) * rng.standard_normal((ndraw, d))
    Dhat = ((b - Yb) ** 2).sum(1) - ((a - Yb) ** 2).sum(1)
    cond = []
    for al in CFG["alpha_grid"]:
        z = float(norm.ppf(1 - al)); f = float((Dhat <= -z * s).mean()); pth = float(norm.cdf(-(Delta + z * s) / s))
        cond.append(dict(alpha=al, empirical=f, formula=pth, z=(f - pth) / np.sqrt(pth * (1 - pth) / ndraw)))
    # (b)
    worst, wkey = None, 0.0
    for sw, rows in (("structure", structure), ("departure", departure), ("m", msweep)):
        for r in rows:
            for name in CFG["operators"]:
                for al, q in r["ops"][name]["rev"].items():
                    if q["identity_z"] is None and q["accept_expected"] > 0:
                        key = (q["accept_count"] - q["accept_expected"]) / np.sqrt(q["accept_expected"])
                        if key < wkey:
                            wkey, worst = key, dict(sweep=sw, snr=r["snr"], dep_over_tau=r.get("dep_over_tau", 0.0),
                                                    m=r["m"], operator=name, alpha=float(al),
                                                    tau2=r.get("tau2"),   # the m sweep fixes tau2; re-simulate with the same value
                                                    count=q["accept_count"], expected=q["accept_expected"], z_main=key)
    rec = dict(conditional=cond, conditional_max_abs_z=max(abs(c["z"]) for c in cond))
    if worst is not None:
        nseeds = 10 if FAST else 50
        cnt = exp = var = 0.0
        z = float(norm.ppf(1 - worst["alpha"]))
        for i in range(nseeds):
            rng_i = np.random.default_rng(SEED + 1000 + i)
            sim = simulate(rng_i, worst["snr"], worst["dep_over_tau"], worst["m"], tau2=worst["tau2"])
            o = sim["ops"][worst["operator"]]
            acc = o["Dhat"] <= -z * o["s"]
            p = norm.cdf(-(o["Delta"] + z * o["s"]) / o["s"])
            cnt += acc.sum(); exp += p.sum(); var += (p * (1 - p)).sum()
        worst.update(recheck_seeds=nseeds, recheck_count=int(cnt), recheck_expected=float(exp),
                     recheck_z=float((cnt - exp) / np.sqrt(var)))
    rec["worst_rare_config"] = worst
    return rec


# ----------------------------------------------------------------------------
def main():
    t0 = time.time()
    consts = constants_table()
    structure, departure, msweep = run_all()
    summary = summarize(structure, departure, msweep, consts)
    summary["identity_recheck"] = identity_recheck(structure, departure, msweep)
    seconds = time.time() - t0
    import scipy, matplotlib
    meta = dict(seed=SEED, fast=FAST, seconds=seconds, python=platform.python_version(),
                numpy=np.__version__, scipy=scipy.__version__, matplotlib=matplotlib.__version__,
                date="2026-10-03", version="v0.2 (referee round 1 applied)")
    out = dict(meta=meta, config=CFG, criteria=dict(
        useful="lower end of the paired 95% CI of the relative risk gain with respect to the full-data reference Xbar_n is >= useful_threshold",
        safe="Monte Carlo excess risk over the estimation-sample reference <= bound + 2 SE, for every configuration and alpha",
        harmful_event="corrected estimate used and its loss exceeds the loss of the reference"),
        constants=consts, structure_sweep=structure, departure_sweep=departure,
        m_sweep=msweep, summary=summary)
    with open(os.path.join(RESULTS, "results.json"), "w") as fh:
        json.dump(out, fh, indent=1)
    write_tables(structure, departure, msweep, consts, summary, os.path.join(RESULTS, "tables.md"))
    make_figures(structure, departure)
    print(json.dumps({k: summary[k] for k in ("safe_phi_all", "safe_alpha_all", "safe_tight_all", "safe_harm_freq_all",
                                                "safe_uniform_all", "max_excess_over_bound_uniform",
                                                "max_identity_abs_z", "identity_ok_all", "n_identity_fail",
                                                "max_excess_over_bound_phi", "max_regret_over_bound")}, indent=1))
    print(f"done in {seconds:.1f} s")


if __name__ == "__main__":
    main()
