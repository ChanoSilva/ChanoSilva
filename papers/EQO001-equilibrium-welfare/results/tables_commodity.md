# E5: commodity-weight cones in two-commodity routing

Seed 20260930; 3.9 s.

## E5a fixed instance (a0=1, b0=2, a1=1/4, b1=0, a_s=1, b_s=0)
- f* = [1.0, 0.0] (shared-edge flows of commodities 1, 2), residual 0.0e+00, C(f*) = [1.0, 0.25], Hessian determinants [-1.0, -1.0]
- directions in Lambda_1: 91/91; in Lambda: 89/91
- boundary of Lambda on lambda_2 = 1: lambda_1 = 0.02500000 (predicted 1/40 = 0.025)
- lambda = (0, 1): in Lambda False, gap 0.050000, better y = [0.0, 0.2], costs there [3.0, 0.2]
- lambda = (1, 1) in Lambda: True

## E5b random instances

- instances: 200
- corner_equilibria: 33
- dirs_in_L1_any: 90
- L1_full_orthant: 9
- witness_instances: 21
- violations_L_not_L1: 0
- tolerance_disagreements: 3
- max_tolerance_disagreement_violation: 5.114844852458846e-05
- max_residual: 3.803374282185246e-12
- max_iterations: 1225

## Criteria

- residuals_le_1e-8: PASS (value 3.803374282185246e-12)
- E5a_all_directions_in_Lambda1: PASS (value 91/91)
- E5a_boundary_ratio_1_40_to_1e-6: PASS (value 0.024999995)
- E5a_witness_gap_1_20_to_1e-9: PASS (value 0.05)
- E5b_no_direction_in_L_outside_L1: PASS (value 0)
- all_pass: PASS
