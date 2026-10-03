# E6: brute-force check of the MAX-CUT reduction (Proposition 'hardness')

Seed 20260930; eps = 0.2; 85.0 s.

| family | n | graphs | (G, k) pairs | e_N in Lambda | e_N not in Lambda | mismatches | exact max by |
|---|---|---|---|---|---|---|---|
| all_unit | 3 | 8 | 20 | 9 | 11 | 0 | faces |
| all_unit | 4 | 64 | 256 | 88 | 168 | 0 | faces |
| all_unit | 5 | 1024 | 6144 | 1840 | 4304 | 0 | vertices |
| sample_unit | 6 | 300 | 2501 | 708 | 1793 | 0 | vertices |
| sample_w123 | 6 | 300 | 4765 | 953 | 3812 | 0 | vertices |

- total pairs 13686, mismatches 0; max residual of x* 0.0e+00; strong-monotonicity constant 0.2
- vertex vs face enumeration cross-check: {'cases': 36, 'max_abs_diff': 0.0}

## Criteria

- membership_iff_maxcut_lt_k: PASS (value 0)
- other_unit_vectors_in_Lambda: PASS (value True)
- Lambda1_orthant: PASS (value True)
- residual_le_1e-12: PASS (value 0.0)
- vertices_vs_faces_le_1e-9: PASS (value 0.0)
- all_pass: PASS
