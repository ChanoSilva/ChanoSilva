# POST-HOC: paired differences against the oracle best global reference (max(linear, RBF) per fold)

Defined after seeing the main results; a sensitivity check, not the predefined criterion.


## `main`

| dataset | oracle acc | knn_svm | cell_svm | vb_rbf | llsvm |
|---|---|---|---|---|---|
| wine | 1.000 | -0.56 [-1.39, +0.00] none | -1.70 [-2.83, -0.57] neg | -0.28 [-0.83, +0.00] none | -0.85 [-1.70, +0.00] none |
| breast_cancer | 0.967 | -1.50 [-3.50, +0.17] none | -0.50 [-1.33, +0.33] none | -0.67 [-1.33, +0.00] none | -0.50 [-1.67, +0.50] none |
| digits_parity | 0.975 | +0.75 [-0.37, +2.00] none | -2.00 [-3.38, -0.50] neg | +0.13 [-0.37, +0.75] none | -1.13 [-2.25, -0.13] neg |
| gauss_linear | 0.943 | -3.62 [-5.37, -2.13] neg | -1.25 [-2.37, -0.13] neg | -0.62 [-2.00, +0.25] none | -1.12 [-2.37, +0.00] none |
| moons_2scale | 0.970 | -0.37 [-1.63, +1.00] none | -3.75 [-5.88, -1.25] neg | +0.12 [-1.25, +1.37] none | -7.38 [-9.13, -5.75] neg |
| checker_2scale | 0.894 | -3.50 [-6.63, -0.75] neg | -7.63 [-11.37, -3.13] neg | +0.50 [-0.50, +2.12] none | -4.88 [-7.63, -2.00] neg |

## `noise20`

| dataset | oracle acc | knn_svm | cell_svm | vb_rbf | llsvm |
|---|---|---|---|---|---|
| wine | 0.983 | -3.40 [-6.27, -1.13] neg | -1.70 [-3.98, +0.00] none | -1.14 [-2.29, +0.00] none | -0.57 [-1.71, +0.00] none |
| breast_cancer | 0.923 | -5.33 [-8.00, -2.33] neg | -1.00 [-2.33, +0.00] none | -2.67 [-3.33, -2.00] neg | +0.33 [+0.00, +1.00] none |
| digits_parity | 0.847 | -4.00 [-7.75, -0.75] neg | -1.75 [-6.00, +1.50] none | +0.25 [-0.50, +1.00] none | +0.75 [-2.50, +3.26] none |
| gauss_linear | 0.940 | -5.50 [-14.75, -0.25] neg | -2.00 [-4.25, -0.25] neg | -1.00 [-2.25, +0.25] none | -1.25 [-2.75, +0.00] none |
| moons_2scale | 0.882 | +2.25 [-1.25, +5.25] none | +0.75 [-5.50, +7.25] none | +2.25 [+0.50, +4.00] pos | -4.00 [-7.75, -0.25] neg |
| checker_2scale | 0.765 | +2.25 [-2.50, +6.75] none | -3.50 [-7.50, -0.00] none | +1.50 [+0.00, +3.50] none | +0.25 [-7.75, +8.25] none |

## `sub25`

| dataset | oracle acc | knn_svm | cell_svm | vb_rbf | llsvm |
|---|---|---|---|---|---|
| wine | 0.989 | -2.22 [-3.89, -0.56] neg | +0.00 [+0.00, +0.00] none | +0.00 [+0.00, +0.00] none | -0.56 [-1.67, +0.00] none |
| breast_cancer | 0.963 | -2.33 [-4.00, -1.00] neg | -3.00 [-5.33, -1.00] neg | -1.33 [-4.00, +0.00] none | -0.33 [-1.00, +0.00] none |
| digits_parity | 0.912 | +0.25 [-2.25, +3.00] none | -2.50 [-6.00, +0.25] none | +0.50 [-1.50, +3.50] none | -5.50 [-8.75, -2.00] neg |
| gauss_linear | 0.920 | -1.25 [-3.00, +0.50] none | -3.50 [-6.50, -0.50] neg | -0.75 [-2.51, +1.00] none | -1.00 [-2.75, +1.50] none |
| moons_2scale | 0.858 | -2.75 [-5.50, -0.25] neg | +4.75 [+2.00, +7.25] pos | +5.25 [+2.25, +8.00] pos | +2.25 [-0.25, +4.75] none |
| checker_2scale | 0.735 | -13.75 [-20.75, -8.00] neg | -10.50 [-16.25, -4.75] neg | +0.25 [-1.75, +2.00] none | -5.75 [-10.25, -0.99] neg |
