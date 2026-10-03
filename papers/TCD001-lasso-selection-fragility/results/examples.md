# E0 — Exact small examples of non-monotone support change

## Example 1 (p = 1)

x = [1, 1, 1], y = [2, -2, 2], mu = 3/2, R = {1}, R' = {1,2} (1-based).

Rule C: D: mu=3/2, support=[0], exact=True; D\R: mu=3/2, support=[], exact=True; D\R': mu=3/2, support=[0], exact=True
Rule P: D: mu=3/2, support=[0], exact=True; D\R: mu=1, support=[], exact=True; D\R': mu=1/2, support=[0], exact=True

## Example 1b (p = 1, enter target)

x = [1, 1, 1, 1], y = [2, -2, 2, -2], mu = 3/2, R = {2}, R' = {2,3} (1-based).

Rule C: D: mu=3/2, support=[], exact=True; D\R: mu=3/2, support=[0], exact=True; D\R': mu=3/2, support=[], exact=True
Rule P: D: mu=3/2, support=[], exact=True; D\R: mu=9/8, support=[0], exact=True; D\R': mu=3/4, support=[], exact=True

## Example 2 (p = 2, integer data, found by seeded search)

X = [[2, -1], [0, 2], [1, 1], [2, -2], [-1, 1]], y = [2, -2, 3, -1, 0], mu = 7/2, R = [3, 4], R' = [2, 3, 4] (1-based).

| data set | mu | support | signs | beta (exact) | inactive c (exact) | marginal x^T y |
|---|---|---|---|---|---|---|
| D | 7/2 | [0] | [1] | {0: '3/20'} | {1: '-1/10'} | {0: '5', 1: '-1'} |
| D\R | 7/2 | [1] | [-1] | {1: '-5/12'} | {0: '11/4'} | {0: '4', 1: '-6'} |
| D\R' | 7/2 | [0] | [1] | {0: '1/10'} | {1: '-17/10'} | {0: '4', 1: '-2'} |

All 26 proper removal sets verified exactly: True. Non-monotone pairs for variable 1: 3.
Stability-selection frequency of variable 1 (rule P, subsamples of size 2): 9/10; fragility number of 'variable 1 leaves' under rule P: 1.

Time 0.3 s.
