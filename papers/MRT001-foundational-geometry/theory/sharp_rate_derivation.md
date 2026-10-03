# Sharp first-order rates in the realizer law (MRT001 v0.6, Thm 5.6 / Prop 5.7)

Working notes, written incrementally. Notation as in `manuscript/main.tex`, Section 5 and
Appendix B: `pi` uniform in `S_n`, `N = N_n` = number of descending successions
(`pi(i+1) = pi(i) - 1`), `R = R_n` = realizers modulo the swap, `Z ~ Po(1)`,
`p_k = P(N_n = k)`, `pi_k = e^{-1}/k!` (with `pi_k = 0` for `k < 0`), `I_k` = number of
intervals of `pi` with `k` elements. Numerical check: `theory/check_sharp_rate.py`, output in
`theory/check_sharp_rate_output.txt`.

Short answer:

* `n d_TV(N_n, Po(1)) -> c_1 = e^{-1}` **exactly**, and the convergence is super-exponentially
  fast: `|d_TV(N_n, Po(1)) - e^{-1}/n| < 2/(n * n!)` for every `n >= 4`. There is no `n^{-2}`
  term at all.
* `d_TV(R_n, 2^Z) = c_2/n + O(n^{-2})` with `c_2 = 1 + 1/(2e) = 1.18394...`.
* For `n >= 20`: `P(R_n != 2^{N_n}) <= 5/n + 220/n^2` and
  `d_TV(R_n, 2^Z) <= (5 + e^{-1})/n + 221/n^2` (vs `(10 + e^2)/n + 167/n^2` in v0.6).
* Open: an explicit constant `C` in `|d_TV(R_n, 2^Z) - c_2/n| <= C/n^2` (the proof below gives
  every error term in closed form, but they were not all bounded by explicit numbers).

---

## 1. The law of `N_n` to all orders

**Exact law.** Step 3 of Appendix B gives `E[(N_n)_r] = 1 - r/n` for `0 <= r <= n-1` (and the
`r = n` moment is `0`, consistent with `1 - n/n`). Inversion of factorial moments
(`N_n <= n-1`, so the sum is finite) gives, for `0 <= k <= n-1`,

    p_k = (1/k!) * sum_{s=0}^{n-1-k} (-1)^s/s! * (1 - (k+s)/n).                       (1.1)

Equivalently (checked in rational arithmetic for `n <= 60`, plus brute force `n <= 8` and an
insertion recurrence), `p_k = C(n-1,k) (D_{n-k} + D_{n-k-1}) / n!` with `D_m` the derangement
numbers; in particular `P(N_n = 0) = (D_n + D_{n-1})/n!` (Kaplansky 1945; Roselle 1968 for the
`k`-succession numbers).

**Infinite series.** `sum_{s>=0} (-1)^s/s! = e^{-1}` and `sum_{s>=0} (-1)^s s/s! = -e^{-1}`, so

    sum_{s>=0} (-1)^s/s! (1 - (k+s)/n) = e^{-1}(1 - k/n) + e^{-1}/n = e^{-1}(1 - (k-1)/n).

**Remainder.** Write `p_k = (1/k!) [ e^{-1}(1 - (k-1)/n) - T_k ]` with
`T_k = sum_{s >= n-k} (-1)^s/s! (1 - (k+s)/n)`. The `s = n-k` term vanishes; with `s = n-k+m`,

    T_k = -(1/n) sum_{m>=1} (-1)^{n-k+m} m/(n-k+m)!.

The terms `a_m = m/(n-k+m)!` decrease (`a_{m+1}/a_m = (m+1)/(m(n-k+m+1)) <= 2/(n-k+2) <= 1`), so
the alternating-series bound gives `|T_k| <= a_1/n = 1/(n (n-k+1)!)`.

**Lemma A (expansion of the law).** For `n >= 1` and `0 <= k <= n-1`,

    p_k = pi_k (1 - (k-1)/n) + r_{n,k},        |r_{n,k}| <= 1 / (n k! (n-k+1)!).

Since `pi_k (1 - (k-1)/n) = pi_k + (pi_k - pi_{k-1})/n` (because `k pi_k = pi_{k-1}`), the law of
`N_n` is `Po(1) + (1/n) nu` up to a super-exponentially small error, with

    nu(k) = pi_k - pi_{k-1} = -(k-1) pi_k.

The coefficient of `n^{-2}` in the expansion of `p_k` is **zero** for every `k`: the expansion
"up to `O(n^{-2})`" asked for is exact up to `O(1/(n k! (n-k+1)!))`. (Check: the ratio
`|r_{n,k}| n k! (n-k+1)!` has maximum 0.9685 over `4 <= n <= 60`, all `k`.)

Heuristic reading: the factorial moments `1 - r/n` agree to first order with those of
`Po(1 - 1/n)` (`(1 - 1/n)^r = 1 - r/n + O(r^2/n^2)`), i.e. to first order `N_n` is a Poisson
variable with the exact mean `1 - 1/n`. Numerically `n^2 d_TV(N_n, Po(1 - 1/n)) -> 3/(4e)`
(0.2760 at `n = 1000` vs 0.27591), which is what the second-order term
`-(pi_k/2n^2)(k^2 - 3k + 1)` predicts (`sum_k |k^2-3k+1|/k! = 3`). Not proved; not claimed.

**Theorem A (sharp TV distance).** For `n >= 4`,

    d_TV(N_n, Po(1)) = (p_0 - pi_0) + (p_1 - pi_1)^+ = e^{-1}/n - T_0 + (-T_1)^+,

hence `|d_TV(N_n, Po(1)) - e^{-1}/n| <= 1/(n (n+1)!) + 1/(n n!) < 2/(n n!)`, and

    c_1 = lim n d_TV(N_n, Po(1)) = (e^{-1}/2) sum_{k>=0} |k-1|/k! = e^{-1}.

*Proof.* `d_TV = sum_k (p_k - pi_k)^+`. For `k >= n`, `p_k = 0 < pi_k`. For `2 <= k <= n-1`,

    p_k - pi_k = -(1/(n k!)) [ e^{-1}(k-1) + n T_k ],   |n T_k| <= 1/(n-k+1)!.

If `k <= n-2` then `|n T_k| <= 1/6 < e^{-1} <= e^{-1}(k-1)`; if `k = n-1 >= 3` then
`|n T_k| <= 1/2 < 2e^{-1} <= e^{-1}(k-1)`. So `p_k < pi_k` for all `k >= 2`. At `k = 0`:
`p_0 - pi_0 = e^{-1}/n - T_0 > 0` since `|T_0| <= 1/(n (n+1)!)`. At `k = 1`:
`p_1 - pi_1 = -T_1` with `|T_1| <= 1/(n n!)`. Hence the identity and the bound. The constant:
`sum_k (k-1)/k! = e - e = 0`, so `sum_k |k-1|/k! = 2 * 1 = 2` (the only negative term is `k = 0`). ∎

So the numerical value `n d_TV = 0.368` "at every `n` tested" in v0.6 is not a coincidence:
`n d_TV(N_n, Po(1)) - e^{-1}` is `+2.2e-2` at `n = 4`, `+2.1e-7` at `n = 10`, `+3.6e-19` at
`n = 20`, and `n! (n d_TV - e^{-1})` stays in `[0.03, 0.96]` for `4 <= n <= 60`. The v0.6 bound
`e^2/n + (2^n+1)/(2 n!)` is `e^{2+1} = 20.1` times too large.

---

## 2. First-order law of `R_n`

**Exceptional occurrences.** Call an *occurrence* `omega` one of:

* a 3-element interval `J = [i, i+2]` of `pi` with a fixed window of values `[v, v+2]` and
  pattern `p in {321, 231, 312}` (factor `c_omega = 3/2` for 321, `2` for 231, 312);
* the event `pi(1) = n`, or the event `pi(n) = 1` (factor `c_omega = 2`).

`P(omega) = (n-3)!/n!` for a fixed 3-interval occurrence, so each pattern has total weight
`(n-2)^2 (n-3)!/n! = (n-2)/(n(n-1))`; `P(pi(1) = n) = P(pi(n) = 1) = 1/n`.

Let `E` (the bad event) be: some interval with between 4 and `n-2` elements, or
`I_3 + I_{n-1} >= 2`. The proof of Proposition 5.7 shows: on `E^c`, `R = 2^N` unless exactly
one occurrence `omega` happens, and then `R = c_omega 2^N`. (On `E^c` there is at most one
interval of size 3..n-1; the non-exceptional patterns 123, 132, 213 and `pi(1) = 1`,
`pi(n) = n` give `R = 2^N`.)

**Lemma B (bad event).**
(a) For `n >= 20`, `P(E) <= 172/n^2 + 51/n^2 = 223/n^2`.
(b) `E[#omega ; E] = O(n^{-2})`, where `#omega` is the number of occurrences that happen.

*Proof of (a).* `sum_{k=4}^{n-2} E I_k <= (24+19+6+3+120)/n^2 = 172/n^2` by Step 2 of
Appendix B. `P(I_3 + I_{n-1} >= 2) <= E[C(I_3,2)] + E[I_3 I_{n-1}] + E[C(I_{n-1},2)]` with the
exact values (all three checked by exhaustive enumeration at `n = 8, 9`)

* `E[C(I_3,2)] = 18(n-4)(n-5)/(n(n-1)(n-2)(n-3)) + 4(n-3)/(n(n-1)(n-2)) + 8(n-4)/(n(n-1)(n-2)(n-3))`
  (disjoint pairs; pairs overlapping in two points, whose union has one of the 4 patterns
  1234, 1324, 4231, 4321; pairs overlapping in one point, 8 patterns of length 5);
  `<= (18 + 4 + 1)/n^2` for `n >= 20` (`n(n-4)(n-5) <= (n-1)(n-2)(n-3)` iff `3n^2-9n-6 >= 0`;
  `n(n-3) <= (n-1)(n-2)`; the last term is `<= 8/(n(n-1)(n-2)) <= 1/n^2`);
* `E[I_3 I_{n-1}] = 4(6n-16)/(n(n-1)(n-2)) <= 25/n^2` (given `pi(1) = 1`, the rest is uniform
  in `S_{n-1}`: `6(n-3)/((n-1)(n-2))` 3-intervals inside, plus `[1,3]` with probability
  `2/((n-1)(n-2))`; four symmetric cases; `25n(n-1)(n-2) - 4(6n-16)n^2 = n(n^2-11n+50) > 0`);
* `E[C(I_{n-1},2)] = 2/(n(n-1)) <= 3/n^2`.

Total `23 + 25 + 3 = 51`. ∎

*Proof of (b).* For a 3-interval occurrence `omega` (positions `[i,i+2]`, values fixed),
contract `J` to one point `j*`: the contracted permutation `sigma` is uniform on `S_m`,
`m = n-2`, whatever `omega` is. On `omega ∩ E` there is an interval `K != J` with
`3 <= |K| <= n-1`. Either `K ∩ J = ∅` (then `K` is an interval of `sigma` of size `3..m-1` not
containing `j*`), or `K ⊋ J` (an interval of `sigma` of size `2..m-1` containing `j*`), or `K`
overlaps `J` partially; then `U = J ∪ K` is an interval strictly containing `J` with `J` at one
end of `U` and `K = U` minus one or two points of `J`, so at most 2 such `K` per `U`; if
`U != [1,n]`, `U` is an interval of `sigma` of size `2..m-1` containing `j*`; if `U = [1,n]`,
then `i in {1, n-2}`. Hence

    P(omega ∩ E) <= P(omega) [ s_m + 3 h_m + 2 * 1{i in {1, n-2}} ],

with `s_m = sum_{l=3}^{m-1} E I_l(m)` and `h_m = sum_{l=2}^{m-1} min(l, m-l+1) (m-l+1) l! (m-l)!/m!`
(expected number of intervals of size `2..m-1` of a uniform `sigma in S_m` containing a fixed
point). For `omega = {pi(1) = n}`, `pi' = pi|_{[2,n]}` is uniform in `S_{n-1}`; another interval
is either an interval of `pi'` of size `3..n-2` or `[1,k]`, `3 <= k <= n-1`, in which case
`[2,k]` is a prefix interval of `pi'` of size `2..n-2`; so
`P(omega ∩ E) <= (1/n)(s_{n-1} + g_{n-1})`, `g_m = sum_{l=2}^{m-1} (m-l+1) l! (m-l)!/m! <= h_m`.
Same for `pi(n) = 1`. Summing (`sum_{i in {1,n-2}} P(omega) = 6/(n(n-1))` over the three patterns):

    E[#omega ; E] <= (3(n-2)/(n(n-1))) (s_{n-2} + 3 h_{n-2}) + 12/(n(n-1)) + (2/n)(s_{n-1} + g_{n-1}).

Finally `s_m = O(1/m)` (Step 2: `10/m + O(m^{-2})`) and
`h_m <= 4/m + 3 E I_3(m)/(m-2) + sum_{l=4}^{m-1} E I_l(m) = 8/m + O(m^{-2})` (the `l = 2` term is
`2 * 2/m`; for `l >= 4` the factor `min(l, m-l+1)/(m-l+1) <= 1` when `l >= (m+1)/2`, and the other
`l` contribute `O(m^{-2})`), so the right-hand side is `O(n^{-2})`. ∎

(For orientation: the leading terms give `E[#omega ; E] ~ (3/n)(10 + 24)/n + 12/n^2 + 28/n^2
~ 142/n^2`; this is an estimate, not a proved constant.)

**Lemma C (conditional law of `N`).** Given a 3-interval occurrence `omega` with pattern `p`,
`N(pi) = N(p) + N(sigma) + delta` where `delta != 0` only if `sigma` has a descending
succession involving `j*` (a descending succession of `pi` with exactly one point in `J`
forces one of `sigma` at `j*`, and a descending succession of `sigma` not involving `j*` is
one of `pi`, because two consecutive integers cannot straddle the value window of `J`); so
`P(delta != 0 | omega) <= 2/m`, and `N(sigma)` has the law of `N_m`, `m = n-2`. Given
`pi(1) = n`, `N(pi) = N(pi') + 1{pi(2) = n-1}`, `P(pi(2) = n-1 | pi(1) = n) = 1/(n-1)`. ∎

**Theorem B.** For every set `A` of positive reals,

    P(R_n in A) = P(2^Z in A) + mu(A)/n + eps_n(A),        sup_A |eps_n(A)| = O(n^{-2}),

where `mu` is the signed measure (total mass 0)

    mu = nu_{2^N} + [ L(6 * 2^Z) - L(4 * 2^Z) ] + 4 [ L(2^{Z+1}) - L(2^Z) ],
    mu({2^k})     = -3 pi_k + 3 pi_{k-1} - pi_{k-2} = -(e^{-1}/k!)(k-1)(k-3),   k >= 0,
    mu({3 * 2^k}) = pi_{k-1} = e^{-1}/(k-1)!,                                 k >= 1,

(`nu_{2^N}` is the image of `nu` under `k -> 2^k`; `L(.)` denotes a law). Consequently

    d_TV(R_n, 2^Z) = c_2/n + O(n^{-2}),     c_2 = |mu|/2 = 1 + 1/(2e) = 1.183939...

*Proof.* `P(R in A) - P(2^Z in A) = [P(2^N in A) - P(2^Z in A)] + E[1{R in A} - 1{2^N in A}]`.

1. By Lemma A the first bracket is `nu_{2^N}(A)/n + rho_1(A)`, with
   `|rho_1| <= sum_{k<n} |r_{n,k}| + sum_{k>=n} pi_k k/n <= 2^{n+1}/(n (n+1)!) + 1/n!`.
2. On `E^c`, `1{R in A} - 1{2^N in A} = sum_omega 1_omega (1{c_omega 2^N in A} - 1{2^N in A})`.
   So the second term equals `sum_omega E[1_omega g_omega(N)] + rho_2(A)` with
   `g_omega(N) = 1{c_omega 2^N in A} - 1{2^N in A}` and `|rho_2| <= P(E) + E[#omega ; E] = O(n^{-2})`
   (Lemma B).
3. By Lemma C, `|E[g_omega(N) | omega] - E g_omega(N(p) + N_m)| <= 2 P(delta != 0 | omega)`, which
   is `<= 4/(n-2)` (3-intervals) or `<= 2/(n-1)` (boundary events); and replacing `N_m` by `Z`
   costs `2 d_TV(N_m, Z) <= 2 e^{-1}/m + 4/(m m!)` (Theorem A).
4. Summing over `omega` with total weights `3(n-2)/(n(n-1)) = 3/n - 3/(n(n-1))` (three patterns)
   and `2/n` (two boundary events), and `|g| <= 1`, the second term is
   `(1/n) sum_types E g_type(N(p) + Z) + O(n^{-2})`, where the types contribute:
   321: `N(p) = 2`, `c = 3/2`, so `L(6 * 2^Z) - L(4 * 2^Z)`;
   231, 312, `pi(1) = n`, `pi(n) = 1`: `N(p) = 0`, `c = 2`, so `4 [L(2^{Z+1}) - L(2^Z)]`.
   All error terms are uniform in `A`.

Then `d_TV(R_n, 2^Z) = sup_A |P(R_n in A) - P(2^Z in A)| = sup_A |mu(A)|/n + O(n^{-2}) = |mu|/(2n) + O(n^{-2})`
since `mu` has total mass 0. ∎

**Computation of `c_2`.** `3 pi_{k-1} - 3 pi_k - pi_{k-2} = (e^{-1}/k!)(3k - 3 - k(k-1)) = -(e^{-1}/k!)(k-1)(k-3)`.
`sum_k (k-1)(k-3)/k! = sum_k (k^2 - 4k + 3)/k! = 2e - 4e + 3e = e`; the only negative term is
`k = 2` (value `-1/2`), so `sum_k |(k-1)(k-3)|/k! = e + 2 * (1/2) = e + 1`. The atoms `3 * 2^k`
carry total mass `sum_{k>=1} pi_{k-1} = 1` and are disjoint from the powers of 2. Hence
`|mu| = e^{-1}(e+1) + 1 = 2 + e^{-1}` and `c_2 = 1 + 1/(2e)`.

Equivalently, the positive part of `mu` is: the new atoms `3 * 2^k` (mass 1: the 321 exceptions,
`R = 6 * 2^{N-2}`) plus the atom `4` (mass `e^{-1}/2`). The exceptions with ratio 2 (mass `4/n`)
mostly land on atoms that `2^Z` already charges, which is why `c_2 = 1.18` is much smaller than
the coupling value `5 + e^{-1}`.

**Corollaries (first order, `O(n^{-2})` errors).**
`P(R_n = 1) = e^{-1}(1 - 3/n)`, `P(R_n = 2) = e^{-1}`, `P(R_n = 4) = e^{-1}(1/2 + 1/(2n))`,
`P(R_n = 6) = P(R_n = 12) = e^{-1}/n`, `P(R_n <= 8) = (8/3)e^{-1} - (3/2)e^{-1}/n`,
`P(R_n not a power of 2) = 1/n`.

---

## 3. Explicit bounds for `n >= 20`

* `|d_TV(N_n, Po(1)) - e^{-1}/n| < 2/(n n!)` for `n >= 4` (Theorem A).
* `P(R_n != 2^{N_n}) <= 5/n + 220/n^2` for `n >= 20`: on `E^c`, `R != 2^N` requires one occurrence,
  of expected number `3(n-2)/(n(n-1)) + 2/n <= 5/n - 3/n^2`; add `P(E) <= 223/n^2` (Lemma B(a)).
  (Evaluated without rounding, the pieces give `5/n + c/n^2` with `c <= 106.4` on `[20, 3000]`.)
* `d_TV(R_n, 2^Z) <= P(R_n != 2^{N_n}) + d_TV(N_n, Z) <= (5 + e^{-1})/n + 221/n^2` for `n >= 20`
  (`2/(n n!) <= 1/n^2`). This improves `(10 + e^2)/n + 167/n^2` for every `n >= 5`.

The asymptotically sharp version `|d_TV(R_n, 2^Z) - c_2/n| <= C/n^2` with explicit `C` would
follow by bounding `s_m, h_m, g_m` explicitly in Lemma B(b) (rough size `C ~ 400`); not done.

---

## 4. Numerical verification (`check_sharp_rate.py`)

See `theory/check_sharp_rate_output.txt` for the numbers quoted here (filled in after the run).
