# E7: three commodities, non-polyhedral commodity-weight cone

2.3 s.

- y* (solver) = [0.0, 0.0, 1.0], residual 0.0e+00, costs at y* [0.25, 0.25, 1.0]
- Lambda_1 = orthant on all 203 tested directions: True
- slice lambda_2 = 1, lambda_1 in [0.7, 1.45] (16 points): max |bisected boundary - psi| = 1.0e-08; psi second differences all positive: True
- competitor points (face y_3 = 0): [[0.0168, 0.1886, 0.0], [0.0995, 0.1224, 0.0], [0.1504, 0.0677, 0.0], [0.192, 0.0118, 0.0]]
- description {lambda_3 + m >= 0} vs exact test: 0 mismatches in 1878 grid points (44 skipped within 1e-6 of the boundary)
- witness lambda = (1, 1, 1/20): gap 0.0055555556 (1/180 = 0.0055555556) at y = [0.111111, 0.111111, 0.0]

## Criteria

- residual_le_1e-8: PASS (value 0.0)
- Lambda1_orthant: PASS (value 203)
- boundary_vs_psi_le_1e-7: PASS (value 9.999999994736442e-09)
- description_mismatches_zero: PASS (value 0/1878)
- witness_gap_1_180_to_1e-9: PASS (value 0.00555555555555555)
- all_pass: PASS
