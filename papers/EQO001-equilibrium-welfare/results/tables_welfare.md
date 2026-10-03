# E2-E4: welfare-weight cones

Seed 20260930; 85.7 s.

## E2 two-player example
- x* = [1.0, 1.0], F(x*) = [-1.0, -1.0], residual 0.0e+00
- boundary angles (deg): [26.56505117707799, 63.43494882292201]
- 181/181 directions: closed form = first-order cone = exact QP; 73 directions inside
- witness lambda = [1.0, 3.0]: member False, gap 0.1250, better x = [0.5, 1.0]

## E2 Cournot
- interior: x* = [0.3333333333334513, 0.3333333333334513], cone nontrivial: False, grid points in Lambda: 0/61
- boundary: x* = [1.0, 1.0], cone dim 1, vertices [[0.5, 0.5]], grid agreement 61/61
- Nikaido-Isoda: x* optimal for all lambda: True (max W' over grid 2.78e-17)

## E2c non-polyhedral cone (three players)
- x* = [1.0, 1.0, 1.0], residual 0.0e+00, jointly concave: False
- slice lambda_3 = 1: 7381 points, mismatches exact test vs parabola: 0; max |bisected boundary - parabola| = 1.0e-08
- witness lambda = [0.3, 0.0, 1.0]: in Lambda_1 True, in Lambda False, gap 0.10125, better x = [0.55, 0.0, 1.0]
- strongly monotone variant eps = 0.2: boundary second differences [0.00199, 0.00194, 0.00188, 0.00183, 0.00178, 0.00174, 0.00169]

## E3/E4 random games

| N | concave | instances | nontrivial | dims | tested in L1 | of which in L | grid out L1 | out L | grid in L1 | in L | witness inst. | max resid |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| 3 | True | 100 | 28 | {'1': 4, '2': 5, '3': 19} | 115 | 115 | 8525 | 8525 | 575 | 575 | 0 | 7.7e-12 |
| 4 | True | 100 | 33 | {'1': 2, '2': 7, '3': 15, '4': 9} | 153 | 153 | 16193 | 16193 | 307 | 307 | 0 | 6.6e-12 |
| 3 | False | 100 | 57 | {'1': 13, '2': 14, '3': 30} | 206 | 162 | 8037 | 8037 | 1063 | 1025 | 23 | 2.1e-12 |
| 4 | False | 100 | 46 | {'1': 2, '2': 2, '3': 13, '4': 29} | 246 | 152 | 15163 | 15163 | 1337 | 1265 | 35 | 2.0e-12 |

## Criteria

- E2_wedge_agreement_all: PASS (value 181/181)
- E2_cournot_interior_none_in_Lambda: PASS (value 0)
- E2_cournot_boundary_agreement_all: PASS (value 61/61)
- E2_nikaido_isoda_max_le_1e-12: PASS (value 2.7755575615628914e-17)
- E2c_slice_mismatches_zero: PASS (value 0)
- E2c_bisection_vs_parabola_le_1e-7: PASS (value 1.0000000105758744e-08)
- E2c_witness_in_L1_not_L_gap_0.10125: PASS (value 0.10124999999999984)
- E3_cone_points_in_Lambda: PASS (value 268/268)
- E3_grid_in_L1_in_Lambda: PASS (value 882/882)
- E3_grid_out_L1_out_Lambda: PASS (value 24718/24718)
- E4_grid_out_L1_out_Lambda: PASS (value 23200/23200)
- E3_E4_residuals_le_1e-8: PASS (value 7.718992112160095e-12)
- all_pass: PASS
