# Signed ANY target with p >= 2 and S(D) nonempty: two identities (TCD001, v0.6)

Companion to `manuscript/main.tex` v0.6 (end of Section 5, after Proposition 5.12). These are the parts of
`theory/signed_any.tex` (Lemma "Cauchy--Binet form" and Remark "why the gadgets do not adapt") that the paper
does not print, for lack of space. Full derivation, in Spanish, with the routes explored and not closed:
`theory/signed_any_derivation.md`.

**Status.** Proved here (the identities are exact, with complete proofs below); the conclusions concern the
gadget families described, and are **not** lower or upper bounds for the signed fragility number. Not yet
refereed. Checked in exact arithmetic by `experiments/check_signed_any.py` (counts copied from
`results/signed_any.json`; frozen log `results/check_signed_any_output.txt`, SHA-256 prefix `b80f98cc974cbd05` since v0.7, `c3e7244d5c447f90` in v0.6; the v0.7 log only appends the counters of the certificate R*_j of Proposition 5.12 to part A, and the counts of parts B and C quoted here are unchanged). Proposition 5.12 itself was checked by the internal referee of round 5; these notes were not.

Notation as in the paper: K = [n] \ R, mu' = mu_{|R|}, G = X_K^T X_K, q = X_K^T y_K.

## 1. Why S(D) nonempty is different

When S(D) is nonempty a signed witness needs one preservation condition of Proposition 3.1 to fail. For p = 2,
S = {1}, s = +1 the conditions are q_1 > mu' (one-sided and linear in the kept rows, hence solved by sorting as
in Theorem 5.1(c)) and |c_2| <= mu' with c_2 = q_2 - G_12 (q_1 - mu') / G_11, a two-sided condition whose form
is the following.

## 2. Lemma (Cauchy--Binet form)

If G_11 > 0, then with m_il = x_i1 x_l2 - x_l1 x_i2 and m'_il = x_i1 y_l - x_l1 y_i,

    G_11 (c_2 - mu') = sum_{i<l in K} m_il m'_il  -  mu' sum_{i in K} x_i1 (x_i1 - x_i2),

and G_11 (c_2 + mu') is the same with `+ mu' sum_{i in K} x_i1 (x_i1 + x_i2)`. In particular, if the kept rows
other than a fixed set of anchor rows are *items* x_i = (1, 1 + e b_i), y_i = y_0 + y_1 b_i with numbers b_i,
the item--item part equals e y_1 (N sum_i b_i^2 - sigma^2), with N the number and sigma the sum of the kept b_i.

*Proof.* G_11 c_2 = G_11 q_2 - G_12 (q_1 - mu'), and G_11 q_2 - G_12 q_1 = det([X_K1, X_K2]^T [X_K1, y_K]),
which by the Cauchy--Binet formula is the stated sum of products of 2x2 minors; the mu' terms are
mu' (G_12 - G_11) (resp. mu' (G_12 + G_11)). For the items, m_il = e (b_l - b_i), m'_il = y_1 (b_l - b_i) and
sum_{i<l} (b_l - b_i)^2 = N sum b_i^2 - sigma^2. QED

Exact check: the identity holds on 295/295 random subsamples; the item form on 200/200 random item families.

## 3. Remark (why the gadgets of Theorems 5.4 and 5.8 do not adapt)

(i) **Theorem 5.4 (p = 2).** There the window Delta = 0 is produced by the kink at which variable 1 becomes
active, so every kept family with Delta <= 0 already changes the signed support (variable 1 leaves); a window
for the signed target must come from a smooth (rational) dependence on a *fixed* signed support. By the Lemma,
with items affine in their numbers the quadratic part of the only two-sided condition is
e y_1 (N sum b_i^2 - sigma^2): it is concave in sigma only together with the term e y_1 N sum b_i^2, which is
not a function of (N, sigma) and dominates the curvature (sigma^2 <= N sum b_i^2). An anchor row
(alpha_g, beta_g) adds e y_1 alpha_g^2 b_i^2 >= 0 per kept item, so the coefficient of sum b_i^2 is
e y_1 (N + sum_g alpha_g^2) and never cancels: c_2 >= mu' is not a threshold on (N, sigma) in this family.
More generally, if the item rows and responses are polynomials in b_i, the item--item part is
sum_{i<l} Psi(b_i, b_l) with Psi symmetric and Psi(b, b) = 0 (the minors vanish on equal rows), which excludes
Psi(b, b') = -2 b b' + k_1 (b + b') + k_0, the form that -(sigma - t)^2 would need.

(ii) **Theorem 5.8 (X3C).** Consider an X3C-type gadget with uniform triple rows (target entry theta,
incidence vector, response 3 b_0 + gamma) and L unit anchor rows per element (target entry phi, response
b_0 + mu / L), all anchors kept, rule C. The candidate on the fixed signed support (U, +) has triple residuals
gamma (I + M_K / L)^{-1} 1 and

    c_0 = 3 q phi mu + gamma L (theta - 3 phi) f(K),     f(K) = 1^T (L I + M_K)^{-1} 1,

where M_K = C_K C_K^T is the matrix of intersection sizes of the kept triples (C_K their incidence matrix).
*Proof.* G_UU = L I + C_K^T C_K and q_U - mu 1 = L b_0 1 + (3 b_0 + gamma) C_K^T 1; since C_K 1 = 3 * 1,
beta_U = b_0 1 + gamma C_K^T (L I + M_K)^{-1} 1 (push-through identity), the triple residuals are
gamma [1 - M_K (L I + M_K)^{-1} 1] = gamma L (L I + M_K)^{-1} 1, the anchor residuals of e are
b_0 + mu / L - beta_e, and c_0 = theta 1^T r_triples + phi L sum_e (b_0 + mu / L - beta_e) gives the formula,
using C_K 1 = 3 * 1 once more. QED
Every threshold on c_0 is therefore a threshold on the single scalar f(K). The mechanism of Theorem 5.8, which
isolates exact covers through absorbers changing status, is precisely a signed-support change.

Exact check: the identity for c_0 and the residual formula hold on 344/344 kept families of random gadgets
with q = 2; in none of the 9 gadgets that have an exact cover is an exact cover the strict maximiser or the
strict minimiser of f among the kept families with N >= q (0 and 0).

Neither observation is a lower or an upper bound for the signed target with S(D) nonempty; that question
remains open (paper, Remark 5.2(iv) and Next steps in Section 7).
