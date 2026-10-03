#!/usr/bin/env python3
"""
Core library for TCD001 "Fragility of Lasso variable selection".

Conventions
-----------
Lasso in *sum form*:  L(b) = (1/2)||y - X b||^2 + mu ||b||_1,  no intercept, columns as given.
scikit-learn's `alpha` equals mu / n_samples.

Penalty rule on the reduced data set D \\ R with n' = n - |R| observations:
  rule "C" (constant):      mu' = mu
  rule "P" (proportional):  mu' = mu * n'/n     (i.e. scikit-learn's alpha kept fixed)

Everything here is deterministic given the inputs; seeds are handled by the run scripts.
"""
from __future__ import annotations

import itertools
import time
import warnings
from dataclasses import dataclass, field

import numpy as np
from sklearn.linear_model import Lasso, lars_path

warnings.filterwarnings("ignore")

ZERO_TOL = 1e-10  # |coef| below this is treated as an exact zero (LARS returns exact zeros anyway)


# ----------------------------------------------------------------------------------------------
# Solvers
# ----------------------------------------------------------------------------------------------
KKT_TOL = 1e-8    # relative KKT tolerance used to guard the homotopy output (see lasso_lars)
KKT_GUARD = True  # False only for the with/without-guard comparison of exact_examples.py --no-guard

# Counter of guarded fits (round-2 finding M1).  Every call of lasso_lars on a nonempty data set is
# counted; "fallbacks" counts the fits whose homotopy output failed the KKT check and was replaced by
# coordinate descent.  Errors are relative to max(1, mu): "max_active_rel" / "max_inactive_rel" are
# the largest active-equation error and inactive violation (max_j |c_j| - mu, positive part) of the
# accepted homotopy outputs; "max_active_rel_rejected" is the largest error of a rejected one;
# "max_active_rel_fallback" / "max_inactive_rel_fallback" are those of the coordinate-descent outputs
# that replaced them.  "fallbacks_tie_at_entry" counts fallbacks in which the largest |x_j^T y| is
# attained by at least two variables exactly (an exact tie at the first entry of the path), and
# "fallbacks_full_rank" those in which X has full column rank.  The run scripts reset the counter at
# the start and store it in the "meta" field of their JSON output.
KKT_STATS = {}


def reset_kkt_stats():
    KKT_STATS.clear()
    KKT_STATS.update(calls=0, fallbacks=0, fallbacks_tie_at_entry=0, fallbacks_full_rank=0,
                     max_active_rel=0.0, max_inactive_rel=0.0, max_active_rel_rejected=0.0,
                     max_active_rel_fallback=0.0, max_inactive_rel_fallback=0.0)


def kkt_stats() -> dict:
    return dict(KKT_STATS)


reset_kkt_stats()


def lasso_lars(X: np.ndarray, y: np.ndarray, mu: float) -> np.ndarray:
    """Exact (homotopy) Lasso solution of (1/2)||y-Xb||^2 + mu||b||_1 via sklearn.lars_path.

    Guard (added in v0.2): sklearn's LARS path is wrong when two variables enter at exactly the same
    penalty (an exact tie of correlations, e.g. X = I_2, y = (3, 3): it returns (5, 2) instead of
    (2, 2)).  Ties have probability zero for continuous designs but occur in integer data, so the
    output is checked against the KKT conditions and, if they fail, recomputed by coordinate descent
    with a tight tolerance; the coordinate-descent output is checked again and an error is raised if
    it also fails.  Activations are counted in KKT_STATS.  In the v0.3 reference run the fallback was
    triggered only in the integer-data search of E0 (exact_examples.py: exact ties of |x_j^T y| at
    the first entry) and never in E1-E5 (Gaussian designs); see results/*.json, field meta.kkt_guard.
    """
    n = X.shape[0]
    if n == 0:
        return np.zeros(X.shape[1])
    alpha_min = mu / n
    _, _, coefs = lars_path(X, y, method="lasso", alpha_min=alpha_min)
    beta = coefs[:, -1].copy()
    act, inact = kkt_residuals(X, y, beta, mu)
    scale = max(1.0, mu)
    tol = KKT_TOL * scale
    KKT_STATS["calls"] += 1
    if KKT_GUARD and (act > tol or inact > tol):
        KKT_STATS["fallbacks"] += 1
        KKT_STATS["max_active_rel_rejected"] = max(KKT_STATS["max_active_rel_rejected"], act / scale)
        cxy = np.abs(X.T @ y)
        KKT_STATS["fallbacks_tie_at_entry"] += int(np.sum(cxy == cxy.max()) >= 2) if cxy.size else 0
        KKT_STATS["fallbacks_full_rank"] += int(np.linalg.matrix_rank(X) == X.shape[1])
        beta = lasso_cd(X, y, mu, tol=1e-12)
        act, inact = kkt_residuals(X, y, beta, mu)
        if act > tol or inact > tol:
            raise RuntimeError(f"KKT check failed after the coordinate-descent fallback "
                               f"(active error {act:.2e}, inactive violation {inact:.2e}, tol {tol:.1e})")
        KKT_STATS["max_active_rel_fallback"] = max(KKT_STATS["max_active_rel_fallback"], act / scale)
        KKT_STATS["max_inactive_rel_fallback"] = max(KKT_STATS["max_inactive_rel_fallback"], max(inact, 0.0) / scale)
    else:
        KKT_STATS["max_active_rel"] = max(KKT_STATS["max_active_rel"], act / scale)
        KKT_STATS["max_inactive_rel"] = max(KKT_STATS["max_inactive_rel"], max(inact, 0.0) / scale)
    return beta


def lasso_cd(X: np.ndarray, y: np.ndarray, mu: float, tol: float = 1e-12) -> np.ndarray:
    """Coordinate-descent Lasso (sklearn.Lasso) with tight tolerance; used only as a cross-check."""
    n = X.shape[0]
    m = Lasso(alpha=mu / n, fit_intercept=False, tol=tol, max_iter=200000)
    m.fit(X, y)
    return m.coef_.copy()


def support(beta: np.ndarray) -> np.ndarray:
    return np.flatnonzero(np.abs(beta) > ZERO_TOL)


def signed_pattern(beta: np.ndarray):
    S = support(beta)
    return S, np.sign(beta[S]).astype(int)


def kkt_residuals(X, y, beta, mu):
    """Return (act, inact): act = max_{j in S} |c_j - mu sgn(beta_j)| (0 if S is empty) and
    inact = max_{j not in S} |c_j| - mu (-inf if S^c is empty), with c = X^T (y - X beta).
    beta satisfies the KKT conditions iff act = 0 and inact <= 0."""
    r = y - X @ beta
    c = X.T @ r
    S = support(beta)
    act = np.max(np.abs(c[S] - mu * np.sign(beta[S]))) if len(S) else 0.0
    mask = np.ones(X.shape[1], bool)
    mask[S] = False
    inact = np.max(np.abs(c[mask])) - mu if mask.any() else -np.inf
    return act, inact


def reduced_mu(mu: float, n: int, k: int, rule: str) -> float:
    if rule == "C":
        return mu
    if rule == "P":
        return mu * (n - k) / n
    raise ValueError(rule)


# ----------------------------------------------------------------------------------------------
# Fitted state and the exact removal test (Proposition 3.1 of the manuscript)
# ----------------------------------------------------------------------------------------------
@dataclass
class LassoState:
    X: np.ndarray
    y: np.ndarray
    mu: float
    beta: np.ndarray
    S: np.ndarray            # support (sorted indices)
    s: np.ndarray            # signs on S
    Sc: np.ndarray           # complement
    betaS: np.ndarray
    Ainv: np.ndarray         # (X_S^T X_S)^{-1}
    V: np.ndarray            # X_S A^{-1}   (n x s): row i is v_i = A^{-1} x_{iS}
    h: np.ndarray            # leverages diag(X_S A^{-1} X_S^T)
    r: np.ndarray            # Lasso residual y - X beta
    c: np.ndarray            # X^T r
    Xt: np.ndarray           # (I - P_S) X_{S^c}   (n x (p-s))
    G: np.ndarray            # X_{S^c}^T X_S       ((p-s) x s)
    w: np.ndarray            # A^{-1} s
    full_rank: bool = True
    extra: dict = field(default_factory=dict)

    @property
    def n(self):
        return self.X.shape[0]

    @property
    def p(self):
        return self.X.shape[1]

    @property
    def gamma(self):
        """KKT slack of the inactive set: min_j (mu - |c_j|), +inf if S = [p]."""
        return np.min(self.mu - np.abs(self.c[self.Sc])) if len(self.Sc) else np.inf

    @property
    def m(self):
        """Minimal |coefficient| on the active set, +inf if S is empty."""
        return np.min(np.abs(self.betaS)) if len(self.S) else np.inf


def fit_state(X: np.ndarray, y: np.ndarray, mu: float, beta: np.ndarray | None = None) -> LassoState:
    n, p = X.shape
    if beta is None:
        beta = lasso_lars(X, y, mu)
    S, s = signed_pattern(beta)
    Sc = np.setdiff1d(np.arange(p), S)
    XS = X[:, S]
    A = XS.T @ XS
    full_rank = True
    if len(S):
        try:
            Ainv = np.linalg.inv(A)
        except np.linalg.LinAlgError:
            Ainv = np.linalg.pinv(A)
            full_rank = False
    else:
        Ainv = np.zeros((0, 0))
    V = XS @ Ainv
    h = np.einsum("ij,ij->i", V, XS) if len(S) else np.zeros(n)
    r = y - X @ beta
    c = X.T @ r
    G = X[:, Sc].T @ XS
    Xt = X[:, Sc] - V @ G.T
    w = Ainv @ s if len(S) else np.zeros(0)
    return LassoState(X, y, mu, beta, S, s, Sc, beta[S].copy(), Ainv, V, h, r, c, Xt, G, w, full_rank)


def removal_test(st: LassoState, R_batch: np.ndarray, rule: str = "C", det_tol: float = 1e-12):
    """
    Exact test of Proposition 3.1, vectorised over a batch of removal sets.

    R_batch : int array (m, k) of observation indices.
    Returns dict with
      preserved : bool (m,)   True iff the signed pattern (S, s) is the signed support of the
                              (unique) Lasso solution on D \\ R under the given rule
                              (up to the measure-zero boundary cases).
      beta_new  : (m, s)      candidate coefficients on S
      c_new     : (m, p-s)    candidate inactive correlations
      sign_ok, kkt_ok, rank_ok : the three conditions separately
    """
    R_batch = np.atleast_2d(np.asarray(R_batch, dtype=int))
    m, k = R_batch.shape
    n, p = st.n, st.p
    S, s = st.S, st.s
    sdim = len(S)
    mu_new = reduced_mu(st.mu, n, k, rule)
    delta = st.mu - mu_new
    if sdim == 0:
        # empty support: pattern preserved iff all inactive correlations on the reduced data
        # stay below mu'. c_j on reduced data = c_j - X_{R,j}^T y_R (beta = 0 so r = y).
        XR = st.X[R_batch]                     # (m,k,p)
        yR = st.y[R_batch]                     # (m,k)
        c_new = st.c[None, :] - np.einsum("mkq,mk->mq", XR, yR)
        kkt_ok = np.all(np.abs(c_new) < mu_new, axis=1)
        return dict(preserved=kkt_ok, beta_new=np.zeros((m, 0)), c_new=c_new,
                    sign_ok=np.ones(m, bool), kkt_ok=kkt_ok, rank_ok=np.ones(m, bool), mu_new=mu_new)
    U = st.X[:, S][R_batch]                    # (m,k,s)   rows x_{iS}, i in R
    VR = st.V[R_batch]                         # (m,k,s)   rows v_i
    H = np.einsum("mks,mls->mkl", U, VR)       # H_R = U A^{-1} U^T   (m,k,k)
    IH = np.eye(k)[None] - H
    det = np.linalg.det(IH)
    rank_ok = det > det_tol
    IH_safe = np.where(rank_ok[:, None, None], IH, np.eye(k)[None])
    rR = st.r[R_batch]                         # (m,k)
    e = np.linalg.solve(IH_safe, rR[..., None])[..., 0]          # multiple-deletion residuals
    beta_new = st.betaS[None, :] - np.einsum("mks,mk->ms", VR, e)  # (m,s)
    XtR = st.Xt[R_batch]                       # (m,k,p-s)
    c_new = st.c[st.Sc][None, :] - np.einsum("mkq,mk->mq", XtR, e)
    if delta != 0.0:
        # proportional rule: add delta * A'^{-1} s to the coefficients, where
        # A'^{-1} s = w + V_R^T (I-H_R)^{-1} U w  (Woodbury), and subtract
        # delta * X_{j,-R}^T X_{S,-R} A'^{-1} s from the inactive correlations.
        Uw = np.einsum("mks,s->mk", U, st.w)
        t = np.linalg.solve(IH_safe, Uw[..., None])[..., 0]
        z = st.w[None, :] + np.einsum("mks,mk->ms", VR, t)        # (m,s)
        beta_new = beta_new + delta * z
        Uz = np.einsum("mks,ms->mk", U, z)                          # (m,k)
        XScR = st.X[:, st.Sc][R_batch]                              # (m,k,p-s)
        c_new = c_new - delta * (z @ st.G.T - np.einsum("mkq,mk->mq", XScR, Uz))
    sign_ok = np.all(beta_new * s[None, :] > 0, axis=1)
    kkt_ok = np.all(np.abs(c_new) < mu_new, axis=1) if len(st.Sc) else np.ones(m, bool)
    preserved = sign_ok & kkt_ok & rank_ok
    return dict(preserved=preserved, beta_new=beta_new, c_new=c_new, sign_ok=sign_ok,
                kkt_ok=kkt_ok, rank_ok=rank_ok, mu_new=mu_new)


def single_removal_indices(st: LassoState, h_tol: float = 1e-12):
    """
    Corollary 3.2 quantities (constant rule) for every observation i with h_i < 1:
      e_i = r_i/(1-h_i), iota_i = |e_i| * max(||v_i||_inf / m, ||xt_i||_inf / gamma).
    Convention (Corollary 3.2): when h_i >= 1 - h_tol the matrix X_{S,-i} is rank deficient
    (Proposition 3.1(a): removing i cannot preserve (S, s)) and e_i = iota_i = +inf.
    max_i iota_i < 1 certifies that no single removal changes the signed support.
    gamma = +inf when S^c is empty (the second term is then 0).
    """
    n = st.n
    ok = st.h < 1.0 - h_tol
    with np.errstate(divide="ignore", invalid="ignore"):
        e = np.where(ok, st.r / np.where(ok, 1.0 - st.h, 1.0), np.inf)
    vinf = np.max(np.abs(st.V), axis=1) if len(st.S) else np.zeros(n)
    xinf = np.max(np.abs(st.Xt), axis=1) if len(st.Sc) else np.zeros(n)
    m, g = st.m, st.gamma
    a = vinf / m if np.isfinite(m) else np.zeros(n)
    b = xinf / g if np.isfinite(g) else np.zeros(n)
    iota = np.where(ok, np.abs(e) * np.maximum(a, b), np.inf)
    return dict(e=e, iota=iota, vinf=vinf, xinf=xinf, rank_deficient=~ok)


def certificate_k(st: LassoState, kmax: int | None = None) -> int:
    """
    Proposition 3.4 (constant rule): largest k such that the top-k-sum bounds certify that no removal
    of <= k observations changes the signed support.  Returns 0 if not even k=1 is certified.

    With T_k(a) = sum of the k largest entries of a >= 0, and e_R = r_R + H_R e_R:
      |Delta beta_j| <= T_k(|v_.j| |r|) + sqrt(T_k(v_.j^2)) sqrt(T_k(r^2)) T_k(h) / (1 - T_k(h)),
      |Delta c_j|    <= T_k(|xt_.j| |r|) + sqrt(T_k(xt_.j^2)) sqrt(T_k(r^2)) T_k(h) / (1 - T_k(h)),
    valid whenever T_k(h) < 1.
    """
    n = st.n
    if kmax is None:
        kmax = n - 1
    absr = np.abs(st.r)
    h = np.sort(st.h)[::-1]
    r2 = np.sort(st.r ** 2)[::-1]
    V2 = np.sort(st.V ** 2, axis=0)[::-1]            # (n,s)
    VR = np.sort(np.abs(st.V) * absr[:, None], axis=0)[::-1]
    Xt2 = np.sort(st.Xt ** 2, axis=0)[::-1]          # (n,p-s)
    XtR = np.sort(np.abs(st.Xt) * absr[:, None], axis=0)[::-1]
    slack = st.mu - np.abs(st.c[st.Sc])
    kstar = 0
    for k in range(1, kmax + 1):
        Th = h[:k].sum()
        if Th >= 1.0:
            break
        Rk = np.sqrt(r2[:k].sum())
        fac = Th / (1.0 - Th)
        ok = True
        if len(st.S):
            bound = VR[:k].sum(axis=0) + np.sqrt(V2[:k].sum(axis=0)) * Rk * fac
            ok &= bool(np.all(bound < np.abs(st.betaS)))
        if len(st.Sc):
            bound = XtR[:k].sum(axis=0) + np.sqrt(Xt2[:k].sum(axis=0)) * Rk * fac
            ok &= bool(np.all(bound < slack))
        if not ok:
            break
        kstar = k
    return kstar


# ----------------------------------------------------------------------------------------------
# Targets
# ----------------------------------------------------------------------------------------------
def target_holds(target: str, S0: np.ndarray, s0: np.ndarray, S_new: np.ndarray, s_new: np.ndarray,
                 j: int | None = None) -> bool:
    if target == "any_signed":
        return not (len(S0) == len(S_new) and np.array_equal(S0, S_new) and np.array_equal(s0, s_new))
    if target == "any":
        return not np.array_equal(S0, S_new)
    if target == "leave":
        return j not in set(S_new.tolist())
    if target == "enter":
        return j in set(S_new.tolist())
    raise ValueError(target)


def refit_pattern(X, y, mu, R, rule, n_full):
    keep = np.ones(n_full, bool)
    keep[list(R)] = False
    mu_new = reduced_mu(mu, n_full, len(R), rule)
    beta = lasso_lars(X[keep], y[keep], mu_new)
    return signed_pattern(beta)


# ----------------------------------------------------------------------------------------------
# Exhaustive search for minimal witnesses
# ----------------------------------------------------------------------------------------------
def fragility_exact(st: LassoState, target: str, rule: str = "C", j: int | None = None,
                    kmax: int | None = None, max_witnesses: int = 50, batch: int = 20000):
    """
    Minimal |R| (proper subsets, |R| <= kmax) such that S(D \\ R) exhibits `target`.
    Uses the exact removal test to skip refits whenever the signed pattern is preserved;
    refits (LARS) only the flagged sets when the target needs the new support.
    For target "any_signed" a flagged set is recorded as a witness without refitting: this
    identifies a witness in the sense of Definition 2.2 provided the minimiser on D \\ R is unique,
    which holds with probability one for designs with a continuous distribution (general position);
    for integer data uniqueness must be certified separately (see exact_examples.py).
    Returns dict(f, witnesses (list of tuples, at most max_witnesses), n_oracle, n_refit, seconds,
                 found).  f = None if no witness up to kmax.
    """
    n = st.n
    if kmax is None:
        kmax = n - 1
    kmax = min(kmax, n - 1)
    t0 = time.perf_counter()
    n_oracle = n_refit = 0
    S0, s0 = st.S, st.s
    for k in range(1, kmax + 1):
        combos = itertools.combinations(range(n), k)
        witnesses = []
        while True:
            chunk = np.fromiter(itertools.chain.from_iterable(itertools.islice(combos, batch)),
                                dtype=int)
            if chunk.size == 0:
                break
            Rb = chunk.reshape(-1, k)
            res = removal_test(st, Rb, rule)
            n_oracle += len(Rb)
            flagged = np.flatnonzero(~res["preserved"])
            if target == "any_signed":
                for idx in flagged:
                    witnesses.append(tuple(Rb[idx].tolist()))
                    if len(witnesses) >= max_witnesses:
                        break
            else:
                for idx in flagged:
                    R = tuple(Rb[idx].tolist())
                    S_new, s_new = refit_pattern(st.X, st.y, st.mu, R, rule, n)
                    n_refit += 1
                    if target_holds(target, S0, s0, S_new, s_new, j):
                        witnesses.append(R)
                        if len(witnesses) >= max_witnesses:
                            break
            if len(witnesses) >= max_witnesses:
                break
        if witnesses:
            return dict(f=k, witnesses=witnesses, n_oracle=n_oracle, n_refit=n_refit,
                        seconds=time.perf_counter() - t0, found=True, kmax=kmax)
    return dict(f=None, witnesses=[], n_oracle=n_oracle, n_refit=n_refit,
                seconds=time.perf_counter() - t0, found=False, kmax=kmax)


# ----------------------------------------------------------------------------------------------
# Greedy heuristics
# ----------------------------------------------------------------------------------------------
def _score_candidates(st: LassoState, target: str, j: int | None, rule: str, idx: np.ndarray):
    """Score every single removal i in idx (indices into the *current* data) for the target.
    Lower is better (closer to the target).  Uses the exact single-removal formula."""
    res = removal_test(st, idx[:, None], rule)
    beta_new, c_new, mu_new = res["beta_new"], res["c_new"], res["mu_new"]
    if target == "leave":
        pos = int(np.flatnonzero(st.S == j)[0])
        score = beta_new[:, pos] * st.s[pos]           # want <= 0
    elif target == "enter":
        pos = int(np.flatnonzero(st.Sc == j)[0])
        score = mu_new - np.abs(c_new[:, pos])          # want < 0
    else:  # any / any_signed : fraction of the smallest normalised margin remaining
        parts = []
        if len(st.S):
            parts.append((beta_new * st.s[None, :]) / np.abs(st.betaS)[None, :])
        if len(st.Sc):
            parts.append((mu_new - np.abs(c_new)) / (st.mu - np.abs(st.c[st.Sc]))[None, :])
        score = np.min(np.concatenate(parts, axis=1), axis=1)
    if target in ("any", "any_signed"):
        # any break of the current pattern reaches the target: give it the most negative score
        score = np.where(res["preserved"], score, np.minimum(score, -1e300))
    # for targeted changes the score is the predicted target margin itself, whether or not the
    # candidate removal also breaks the pattern elsewhere
    return score


def greedy_witness(X, y, mu, target, rule="C", j=None, method="onestep", budget=None):
    """
    Greedy heuristics.  Returns dict(f, R, n_refit, seconds, found).
      method="onestep": at each step remove the observation whose exact single-removal effect
                        (on the current fit) brings the target closest; refit; repeat.
      method="cook":    remove in order of Cook's distance of the active-set regression
                        (target-agnostic); refit; repeat.
      method="sorted":  AMIP-style: score all observations once on the full data with the exact
                        single-removal effect, remove the top-k in that fixed order and refit until
                        the target holds (no re-scoring).
    """
    n = X.shape[0]
    if budget is None:
        budget = n - 1
    budget = min(budget, n - 1)
    t0 = time.perf_counter()
    beta0 = lasso_lars(X, y, mu)
    S0, s0 = signed_pattern(beta0)
    n_refit = 1
    removed = []
    remaining = np.arange(n)
    if method == "sorted":
        st = fit_state(X, y, mu, beta0)
        score = _score_candidates(st, target, j, rule, np.arange(n))
        order = np.argsort(score, kind="stable")
        for k in range(1, budget + 1):
            R = tuple(sorted(order[:k].tolist()))
            S_new, s_new = refit_pattern(X, y, mu, R, rule, n)
            n_refit += 1
            if target_holds(target, S0, s0, S_new, s_new, j):
                return dict(f=k, R=R, n_refit=n_refit, seconds=time.perf_counter() - t0, found=True)
        return dict(f=None, R=None, n_refit=n_refit, seconds=time.perf_counter() - t0, found=False)
    Xc, yc, betac = X, y, beta0
    for step in range(1, budget + 1):
        nc = Xc.shape[0]
        mu_c = reduced_mu(mu, n, n - nc, rule)
        st = fit_state(Xc, yc, mu_c, betac)
        if method == "onestep":
            # the target is checked after every removal, so here j is still in S (leave) or
            # still outside S (enter): the target is always defined for the current pattern
            score = _score_candidates(st, target, j, rule, np.arange(nc))
            pick = int(np.argmin(score))
        elif method == "cook":
            if len(st.S):
                e = st.r / (1 - st.h)
                cook = st.h * e ** 2
            else:
                cook = st.r ** 2
            pick = int(np.argmax(cook))
        else:
            raise ValueError(method)
        removed.append(int(remaining[pick]))
        remaining = np.delete(remaining, pick)
        Xc = np.delete(Xc, pick, axis=0)
        yc = np.delete(yc, pick, axis=0)
        mu_c = reduced_mu(mu, n, len(removed), rule)
        betac = lasso_lars(Xc, yc, mu_c)
        n_refit += 1
        S_new, s_new = signed_pattern(betac)
        if target_holds(target, S0, s0, S_new, s_new, j):
            return dict(f=len(removed), R=tuple(sorted(removed)), n_refit=n_refit,
                        seconds=time.perf_counter() - t0, found=True)
    return dict(f=None, R=None, n_refit=n_refit, seconds=time.perf_counter() - t0, found=False)


def amip_witness(X, y, mu, target, rule="C", j=None, budget=None):
    """
    AMIP-style heuristic (sorted one-shot influence scores, in the spirit of Broderick, Giordano and
    Meager 2020, with the exact single-removal effect of Proposition 3.1 in place of the influence
    function).  For every 'direction' in which the target can be reached (an active coefficient
    pushed to zero, or an inactive correlation pushed to +mu or -mu), score every observation once on
    the full data, sort, and predict the number of removals k_pred as the smallest k whose cumulative
    score covers the margin.  The direction with the smallest k_pred is chosen; observations are then
    removed in that fixed order, refitting after each removal, until the target holds.
    Returns dict(f, R, k_pred, n_refit, seconds, found).
    """
    n = X.shape[0]
    if budget is None:
        budget = n - 1
    budget = min(budget, n - 1)
    t0 = time.perf_counter()
    beta0 = lasso_lars(X, y, mu)
    S0, s0 = signed_pattern(beta0)
    n_refit = 1
    st = fit_state(X, y, mu, beta0)
    res = removal_test(st, np.arange(n)[:, None], rule)
    dirs = []
    if target in ("leave", "any", "any_signed"):
        for pos, jj in enumerate(st.S):
            if target == "leave" and jj != j:
                continue
            phi = st.s[pos] * (st.betaS[pos] - res["beta_new"][:, pos])
            dirs.append((phi, st.s[pos] * st.betaS[pos]))
    if target in ("enter", "any", "any_signed"):
        for pos, jj in enumerate(st.Sc):
            if target == "enter" and jj != j:
                continue
            for sign in (1.0, -1.0):
                phi = sign * (res["c_new"][:, pos] - st.c[jj])
                dirs.append((phi, st.mu - sign * st.c[jj]))
    best = None
    for phi, M in dirs:
        order = np.argsort(-phi, kind="stable")
        cum = np.cumsum(phi[order])
        hit = np.flatnonzero(cum >= M)
        k_pred = int(hit[0]) + 1 if len(hit) else n
        if best is None or k_pred < best[0]:
            best = (k_pred, order)
    if best is None:
        return dict(f=None, R=None, k_pred=None, n_refit=n_refit, seconds=time.perf_counter() - t0, found=False)
    k_pred, order = best
    for k in range(1, budget + 1):
        R = tuple(sorted(order[:k].tolist()))
        S_new, s_new = refit_pattern(X, y, mu, R, rule, n)
        n_refit += 1
        if target_holds(target, S0, s0, S_new, s_new, j):
            return dict(f=k, R=R, k_pred=k_pred, n_refit=n_refit, seconds=time.perf_counter() - t0, found=True)
    return dict(f=None, R=None, k_pred=k_pred, n_refit=n_refit, seconds=time.perf_counter() - t0, found=False)


def heuristic(X, y, mu, target, rule="C", j=None, method="onestep", budget=None):
    if method == "amip":
        return amip_witness(X, y, mu, target, rule, j, budget)
    return greedy_witness(X, y, mu, target, rule, j, method, budget)


# ----------------------------------------------------------------------------------------------
# Synthetic instances
# ----------------------------------------------------------------------------------------------
def make_instance(rng: np.random.Generator, n: int, p: int, s0: int = 2, b: float = 1.5,
                  rho: float = 0.3, sigma: float = 1.0, c: float = 0.5):
    """Gaussian design with Toeplitz correlation rho^|i-j|, beta* = b on the first s0 coordinates
    with alternating signs, noise N(0, sigma^2), penalty mu = c * sigma * sqrt(2 n log p)."""
    idx = np.arange(p)
    Sigma = rho ** np.abs(idx[:, None] - idx[None, :])
    L = np.linalg.cholesky(Sigma)
    X = rng.standard_normal((n, p)) @ L.T
    beta_star = np.zeros(p)
    beta_star[:s0] = b * np.array([(-1) ** i for i in range(s0)])
    y = X @ beta_star + sigma * rng.standard_normal(n)
    mu = c * sigma * np.sqrt(2 * n * np.log(p))
    return X, y, mu, beta_star


# ----------------------------------------------------------------------------------------------
# Instance families used throughout the experiments
# ----------------------------------------------------------------------------------------------
FAMILIES = {
    "A": dict(p=4, s0=2, b=4.0, rho=0.0, c=1.5),   # "stable": strong signal, larger penalty, independent design
    "B": dict(p=8, s0=2, b=2.0, rho=0.5, c=1.0),   # "noisy": weaker signal, smaller penalty, correlated design
}


def make_family_instance(rng, n, fam):
    f = FAMILIES[fam]
    return make_instance(rng, n, f["p"], f["s0"], f["b"], f["rho"], 1.0, f["c"])
