#!/usr/bin/env python3
"""
Referee counterexample to the unconditional form of Corollary 3.2 (round 1, finding B1):
n = p = 2, X = I_2, y = (3, 3), mu = 1.  Columns in general position, unique minimiser
beta = (2, 2), S = {1, 2}, A = I, h_1 = h_2 = 1.  Removing either observation leaves X_{S,-i}
rank deficient, so (S, s) cannot be preserved (Proposition 3.1(a)); e_i and iota_i are undefined
and the code must return the +inf convention of Corollary 3.2.

The same instance exposed a second issue (v0.2): sklearn's lars_path returns a wrong path when two
variables enter at exactly the same penalty (it gives beta = (5, 2) here, violating the KKT
conditions); lasso_lars now checks KKT and falls back to coordinate descent.  Exits nonzero on failure.
"""
import os
import sys
import warnings

import numpy as np

warnings.filterwarnings("ignore")
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from sklearn.linear_model import lars_path
from lasso_fragility import fit_state, kkt_residuals, lasso_lars, removal_test, single_removal_indices

X = np.eye(2)
y = np.array([3.0, 3.0])
mu = 1.0
# (1) raw homotopy output on the tied instance violates KKT; the guarded solver does not
raw = lars_path(X, y, method="lasso", alpha_min=mu / 2)[2][:, -1]
act_raw, _ = kkt_residuals(X, y, raw, mu)
assert act_raw > 1e-6, ("expected the raw LARS path to fail on the exact tie", raw, act_raw)
beta = lasso_lars(X, y, mu)
assert np.allclose(beta, [2.0, 2.0]), beta
assert kkt_residuals(X, y, beta, mu)[0] < 1e-12
# (2) leverages equal one; the exact test reports rank deficiency, not preservation
st = fit_state(X, y, mu)
assert st.S.tolist() == [0, 1] and np.allclose(st.h, 1.0), (st.S, st.h)
res = removal_test(st, np.arange(2)[:, None], "C")
assert not res["preserved"].any() and not res["rank_ok"].any(), res
# (3) Corollary 3.2 convention: e_i = iota_i = +inf when h_i = 1
ind = single_removal_indices(st)
assert np.all(np.isinf(ind["e"])) and np.all(np.isinf(ind["iota"])) and ind["rank_deficient"].all(), ind
# (4) a generic instance is untouched by the convention and by the solver guard
rng = np.random.default_rng(0)
Xg = rng.standard_normal((10, 3))
yg = Xg[:, 0] + rng.standard_normal(10)
rawg = lars_path(Xg, yg, method="lasso", alpha_min=2.0 / 10)[2][:, -1]
assert np.array_equal(rawg, lasso_lars(Xg, yg, 2.0))
stg = fit_state(Xg, yg, 2.0)
indg = single_removal_indices(stg)
assert np.all(np.isfinite(indg["iota"])) and not indg["rank_deficient"].any()
assert np.allclose(indg["e"], stg.r / (1 - stg.h))
print(f"raw LARS on the tie: {raw} (active KKT error {act_raw:.1f}); guarded solver: {beta}")
print("h =", st.h, "| preserved =", res["preserved"], "| rank_ok =", res["rank_ok"], "| iota =", ind["iota"])
print("B1 check OK: h_i = 1 -> rank deficient, iota = +inf; generic instance unchanged.")
