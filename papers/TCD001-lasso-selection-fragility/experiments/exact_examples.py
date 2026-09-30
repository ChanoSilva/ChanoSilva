#!/usr/bin/env python3
"""
E0: explicit small examples of non-monotone support changes, verified with exact rational
arithmetic (Python fractions): the KKT system on the candidate signed support is solved exactly and
all inequalities are checked strictly, which (with full column rank) certifies the unique Lasso
solution and its support.

  Example 1 (p = 1, by hand):  x = (1,1,1), y = (2,-2,2), mu = 3/2.
  Example 2 (p = 2, found by seeded search over small integer data): variable 1 is selected, is
     driven out by variable 2 after removing R, and returns after removing R' ⊃ R, although its
     marginal correlation on D \\ R still exceeds the penalty (the exclusion is due to competition).

Writes results/examples.json and results/examples.md.
"""
import itertools
import json
import os
import sys
import time
from fractions import Fraction as F

import numpy as np

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from lasso_fragility import lasso_lars, reduced_mu, signed_pattern

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
SEED = 20260930


def exact_solve(A, rhs):
    """Gaussian elimination over Fractions. Returns solution or None if singular."""
    k = len(rhs)
    M = [row[:] + [rhs[a]] for a, row in enumerate(A)]
    for col in range(k):
        piv = next((r for r in range(col, k) if M[r][col] != 0), None)
        if piv is None:
            return None
        M[col], M[piv] = M[piv], M[col]
        pv = M[col][col]
        M[col] = [v / pv for v in M[col]]
        for r in range(k):
            if r != col and M[r][col] != 0:
                f = M[r][col]
                M[r] = [a - f * b for a, b in zip(M[r], M[col])]
    return [M[a][k] for a in range(k)]


def exact_pattern_check(Xq, yq, muq, S, s):
    """Exact certificate that (S, s) is the signed support of the unique Lasso solution of
    (1/2)||y - X b||^2 + mu ||b||_1 on rational data (Xq, yq).  Returns dict with ok, beta, c."""
    n = len(yq)
    p = len(Xq[0])
    S = [int(v) for v in S]
    s = [int(v) for v in s]
    k = len(S)
    if k == 0:
        c = {j: sum(Xq[i][j] * yq[i] for i in range(n)) for j in range(p)}
        return dict(ok=all(abs(cj) < muq for cj in c.values()), beta={}, c=c)
    A = [[sum(Xq[i][S[a]] * Xq[i][S[b]] for i in range(n)) for b in range(k)] for a in range(k)]
    rhs = [sum(Xq[i][S[a]] * yq[i] for i in range(n)) - muq * s[a] for a in range(k)]
    beta = exact_solve(A, rhs)
    if beta is None:
        return dict(ok=False, beta=None, c=None, reason="X_S rank deficient")
    if not all(beta[a] * s[a] > 0 for a in range(k)):
        return dict(ok=False, beta=dict(zip(S, beta)), c=None, reason="sign")
    resid = [yq[i] - sum(Xq[i][S[a]] * beta[a] for a in range(k)) for i in range(n)]
    c = {j: sum(Xq[i][j] * resid[i] for i in range(n)) for j in range(p) if j not in S}
    return dict(ok=all(abs(cj) < muq for cj in c.values()), beta=dict(zip(S, beta)), c=c)


def fr(x):
    return str(x) if isinstance(x, F) else x


def support_float(X, y, mu):
    return signed_pattern(lasso_lars(X, y, mu))


def analyse_example(X, y, mu, R, Rp, rule="C", j=0):
    """Exact analysis of the three data sets D, D\\R, D\\R' (mu, mu', mu'' by the rule)."""
    n = X.shape[0]
    Xq = [[F(int(v)) for v in row] for row in X]
    yq = [F(int(v)) for v in y]
    muq = F(mu)
    out = []
    for name, RR in [("D", ()), ("D\\R", tuple(R)), ("D\\R'", tuple(Rp))]:
        keep = [i for i in range(n) if i not in RR]
        mu_k = muq if rule == "C" else muq * F(len(keep), n)
        Xs = [Xq[i] for i in keep]
        ys = [yq[i] for i in keep]
        S, s = support_float(X[keep], y[keep], float(mu_k))
        chk = exact_pattern_check(Xs, ys, mu_k, S, s)
        marg = {jj: sum(Xs[i][jj] * ys[i] for i in range(len(keep))) for jj in range(X.shape[1])}
        out.append(dict(name=name, removed=list(RR), kept=keep, mu=str(mu_k), support=[int(v) for v in S],
                        signs=[int(v) for v in s], exact_ok=bool(chk["ok"]),
                        beta={int(k): str(v) for k, v in (chk["beta"] or {}).items()},
                        inactive_c={int(k): str(v) for k, v in (chk["c"] or {}).items()},
                        marginal_xy={int(k): str(v) for k, v in marg.items()}))
    return out


def stability_selection_exact(X, y, mu, j, rule="P"):
    """Selection frequency of variable j over all subsamples of size floor(n/2) (exact enumeration),
    with the penalty rule used for the subsamples."""
    n = X.shape[0]
    m = n // 2
    cnt = tot = 0
    for K in itertools.combinations(range(n), m):
        K = list(K)
        mu_k = reduced_mu(mu, n, n - m, rule)
        S, _ = support_float(X[K], y[K], mu_k)
        cnt += int(j in set(S.tolist()))
        tot += 1
    return cnt, tot


def main():
    t0 = time.time()
    res = {"seed": SEED}

    # ---------------- Example 1: p = 1 ----------------
    X1 = np.array([[1.0], [1.0], [1.0]])
    y1 = np.array([2.0, -2.0, 2.0])
    ex1 = {}
    for rule in ["C", "P"]:
        ex1[rule] = analyse_example(X1, y1, F(3, 2), (0,), (0, 1), rule)
        assert ex1[rule][0]["support"] == [0] and ex1[rule][1]["support"] == [] and ex1[rule][2]["support"] == [0]
        assert all(e["exact_ok"] for e in ex1[rule])
    res["example1"] = dict(X=X1.astype(int).tolist(), y=y1.astype(int).tolist(), mu="3/2", R=[0], Rp=[0, 1], analysis=ex1)
    print("Example 1 verified exactly under both rules.")

    # ---------------- Example 1b: p = 1, non-monotone pair for the 'enter' target ----------------
    # x = (1,1,1,1), y = (2,-2,2,-2), mu = 3/2: not selected on D (x^T y = 0); enters after removing
    # observation 2 (x^T y = 2); not selected after removing {2,3} (x^T y = 0). Both rules.
    X1b = np.ones((4, 1))
    y1b = np.array([2.0, -2.0, 2.0, -2.0])
    ex1b = {}
    for rule in ["C", "P"]:
        ex1b[rule] = analyse_example(X1b, y1b, F(3, 2), (1,), (1, 2), rule)
        assert ex1b[rule][0]["support"] == [] and ex1b[rule][1]["support"] == [0] and ex1b[rule][2]["support"] == []
        assert all(e["exact_ok"] for e in ex1b[rule])
    res["example1b"] = dict(X=X1b.astype(int).tolist(), y=y1b.astype(int).tolist(), mu="3/2", R=[1], Rp=[1, 2], analysis=ex1b)
    print("Example 1b (enter) verified exactly under both rules.")

    # ---------------- Example 2: p = 2, seeded search ----------------
    rng = np.random.default_rng(SEED)
    n, p = 5, 2
    vals = [-2, -1, 0, 1, 2]
    mus = [F(1, 2), F(3, 2), F(5, 2), F(7, 2)]
    found = None
    trials = 0
    while found is None and trials < 200000:
        trials += 1
        X = rng.choice(vals, size=(n, p)).astype(float)
        y = rng.choice([-3, -2, -1, 0, 1, 2, 3], size=n).astype(float)
        if np.linalg.matrix_rank(X) < p:
            continue
        for muq in mus:
            mu = float(muq)
            S0, _ = support_float(X, y, mu)
            if 0 not in S0:
                continue
            subs = {}
            for k in range(1, n - 1):
                for R in itertools.combinations(range(n), k):
                    keep = np.ones(n, bool)
                    keep[list(R)] = False
                    subs[R] = support_float(X[keep], y[keep], mu)[0]
            hit = None
            for R, S in subs.items():
                if 0 in S or 1 not in S:
                    continue
                keep = np.ones(n, bool)
                keep[list(R)] = False
                if abs(X[keep, 0] @ y[keep]) <= mu:      # exclusion must be due to variable 2
                    continue
                for Rp, Sp in subs.items():
                    if set(R) < set(Rp) and 0 in Sp and 1 not in Sp:
                        hit = (R, Rp)
                        break
                if hit:
                    break
            if hit is None:
                continue
            an = analyse_example(X, y, muq, hit[0], hit[1], "C")
            if not all(e["exact_ok"] for e in an):
                continue
            # exact check of the mechanism: |x_0^T y| on D\R exceeds mu
            if not abs(F(an[1]["marginal_xy"][0])) > muq:
                continue
            # require that *every* proper removal set is exactly verifiable (no KKT ties)
            Xq = [[F(int(v)) for v in row] for row in X]
            yq = [F(int(v)) for v in y]
            table = []
            for k in range(0, n - 1):
                for R in itertools.combinations(range(n), k):
                    keep = [i for i in range(n) if i not in R]
                    S, s = support_float(X[keep], y[keep], mu)
                    chk = exact_pattern_check([Xq[i] for i in keep], [yq[i] for i in keep], muq, S, s)
                    table.append(dict(R=list(R), support=[int(v) for v in S], exact_ok=bool(chk["ok"])))
            if all(t["exact_ok"] for t in table):
                found = dict(X=X.astype(int).tolist(), y=y.astype(int).tolist(), mu=str(muq),
                             R=list(hit[0]), Rp=list(hit[1]), analysis=an, trials=trials,
                             all_subsets=table, all_subsets_exact_ok=True)
                break
    assert found is not None, "no exactly verified example found"
    Xf = np.array(found["X"], float)
    yf = np.array(found["y"], float)
    muq = F(found["mu"])
    table = found["all_subsets"]
    # non-monotone pairs (R subset R') for variable 0 among all subsets
    pairs = 0
    sup = {tuple(t["R"]): set(t["support"]) for t in table}
    for R, S in sup.items():
        for Rp, Sp in sup.items():
            if set(R) < set(Rp) and 0 not in S and 0 in Sp:
                pairs += 1
    found["nonmonotone_pairs_var0"] = pairs
    # stability-selection frequency of variable 0 (rule P, subsample size floor(n/2))
    cnt, tot = stability_selection_exact(Xf, yf, float(muq), 0, "P")
    found["stability_selection_var0"] = dict(selected=cnt, subsamples=tot, rule="P")
    # fragility number of 'variable 0 leaves' under rule P (exact, all proper subsets)
    f_leave_P = None
    for k in range(1, n):
        for R in itertools.combinations(range(n), k):
            keep = [i for i in range(n) if i not in R]
            S, _ = support_float(Xf[keep], yf[keep], reduced_mu(float(muq), n, k, "P"))
            if 0 not in S:
                f_leave_P = k
                break
        if f_leave_P:
            break
    found["f_leave_var0_rule_P"] = f_leave_P
    res["example2"] = found
    print("Example 2 found after", trials, "trials:", found["X"], found["y"], found["mu"], found["R"], found["Rp"])
    for e in found["analysis"]:
        print("  ", e["name"], "support", e["support"], "signs", e["signs"], "exact", e["exact_ok"], "beta", e["beta"], "c", e["inactive_c"], "marg", e["marginal_xy"])
    print("  all subsets exact:", found["all_subsets_exact_ok"], "nonmonotone pairs:", pairs,
          "stab. sel. var0:", found["stability_selection_var0"], "f_leave(P)=", f_leave_P)
    res["seconds"] = time.time() - t0
    os.makedirs(os.path.join(ROOT, "results"), exist_ok=True)
    with open(os.path.join(ROOT, "results", "examples.json"), "w") as fh:
        json.dump(res, fh, indent=1)
    L = ["# E0 — Exact small examples of non-monotone support change", "",
         "## Example 1 (p = 1)", "", f"x = {X1[:,0].astype(int).tolist()}, y = {y1.astype(int).tolist()}, mu = 3/2, R = {{1}}, R' = {{1,2}} (1-based).", ""]
    for rule in ["C", "P"]:
        L.append(f"Rule {rule}: " + "; ".join(f"{e['name']}: mu={e['mu']}, support={e['support']}, exact={e['exact_ok']}" for e in ex1[rule]))
    L += ["", "## Example 1b (p = 1, enter target)", "", f"x = {X1b[:,0].astype(int).tolist()}, y = {y1b.astype(int).tolist()}, mu = 3/2, R = {{2}}, R' = {{2,3}} (1-based).", ""]
    for rule in ["C", "P"]:
        L.append(f"Rule {rule}: " + "; ".join(f"{e['name']}: mu={e['mu']}, support={e['support']}, exact={e['exact_ok']}" for e in ex1b[rule]))
    f2 = res["example2"]
    L += ["", "## Example 2 (p = 2, integer data, found by seeded search)", "",
          f"X = {f2['X']}, y = {f2['y']}, mu = {f2['mu']}, R = {[i+1 for i in f2['R']]}, R' = {[i+1 for i in f2['Rp']]} (1-based).", "",
          "| data set | mu | support | signs | beta (exact) | inactive c (exact) | marginal x^T y |", "|---|---|---|---|---|---|---|"]
    for e in f2["analysis"]:
        L.append(f"| {e['name']} | {e['mu']} | {e['support']} | {e['signs']} | {e['beta']} | {e['inactive_c']} | {e['marginal_xy']} |")
    L += ["", f"All {len(f2['all_subsets'])} proper removal sets verified exactly: {f2['all_subsets_exact_ok']}. Non-monotone pairs for variable 1: {f2['nonmonotone_pairs_var0']}.",
          f"Stability-selection frequency of variable 1 (rule P, subsamples of size 2): {f2['stability_selection_var0']['selected']}/{f2['stability_selection_var0']['subsamples']}; fragility number of 'variable 1 leaves' under rule P: {f2['f_leave_var0_rule_P']}.",
          "", f"Time {res['seconds']:.1f} s."]
    with open(os.path.join(ROOT, "results", "examples.md"), "w") as fh:
        fh.write("\n".join(L) + "\n")


if __name__ == "__main__":
    main()
