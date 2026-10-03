# SVMF001 -- results (seed 20260930)


## Condition `main`: mean accuracy per fold set

| dataset | n_train | linear | rbf | best_global | knn_svm | cell_svm | vb_rbf | llsvm |
|---|---|---|---|---|---|---|---|---|
| wine | 142 | 0.992 | 0.997 | 0.997 | 0.994 | 0.983 | 0.997 | 0.992 |
| breast_cancer | 240 | 0.960 | 0.960 | 0.965 | 0.952 | 0.962 | 0.960 | 0.962 |
| digits_parity | 320 | 0.853 | 0.975 | 0.975 | 0.982 | 0.955 | 0.976 | 0.964 |
| gauss_linear | 320 | 0.939 | 0.935 | 0.933 | 0.906 | 0.930 | 0.936 | 0.931 |
| moons_2scale | 320 | 0.845 | 0.970 | 0.970 | 0.966 | 0.932 | 0.971 | 0.896 |
| checker_2scale | 320 | 0.508 | 0.894 | 0.894 | 0.859 | 0.817 | 0.899 | 0.845 |

### Paired difference vs best global (mean [95% bootstrap CI]), `main`

| dataset | knn_svm | cell_svm | vb_rbf | llsvm |
|---|---|---|---|---|
| wine | -0.28 [-1.11, +0.56] none | -1.42 [-2.83, -0.01] neg | +0.00 [+0.00, +0.00] none | -0.57 [-1.67, +0.54] none |
| breast_cancer | -1.33 [-3.34, +0.67] none | -0.33 [-1.33, +0.50] none | -0.50 [-1.33, +0.00] none | -0.33 [-1.50, +0.67] none |
| digits_parity | +0.75 [-0.50, +2.00] none | -2.00 [-3.50, -0.37] neg | +0.13 [-0.37, +0.75] none | -1.13 [-2.25, -0.13] neg |
| gauss_linear | -2.62 [-3.88, -1.62] neg | -0.25 [-1.12, +0.50] none | +0.37 [+0.12, +0.75] pos | -0.12 [-0.87, +0.63] none |
| moons_2scale | -0.37 [-1.63, +1.00] none | -3.75 [-5.88, -1.25] neg | +0.12 [-1.25, +1.37] none | -7.38 [-9.13, -5.75] neg |
| checker_2scale | -3.50 [-6.38, -0.50] neg | -7.63 [-11.38, -3.25] neg | +0.50 [-0.50, +2.12] none | -4.88 [-7.63, -1.87] neg |

### Fraction of folds in which inner CV selected a local configuration, `main`

| dataset | best_global picks RBF | knn_svm | cell_svm | vb_rbf | llsvm |
|---|---|---|---|---|---|
| wine | 1.00 | 0.60 | 0.70 | 0.00 | 0.50 |
| breast_cancer | 0.70 | 0.40 | 0.30 | 0.30 | 0.70 |
| digits_parity | 1.00 | 1.00 | 1.00 | 0.50 | 1.00 |
| gauss_linear | 0.80 | 0.50 | 0.30 | 0.60 | 0.90 |
| moons_2scale | 1.00 | 1.00 | 1.00 | 1.00 | 1.00 |
| checker_2scale | 1.00 | 1.00 | 1.00 | 0.50 | 1.00 |

### Grid saturation (folds with the selected value at the lower/upper edge of the grid), `main`

| dataset | linear:C | rbf:gamma_mult | rbf:C | knn_svm:k | cell_svm:M | cell_svm:C | vb_rbf:gamma_mult | vb_rbf:C | vb_rbf:beta | llsvm:M | llsvm:C |
|---|---|---|---|---|---|---|---|---|---|---|---|
| wine | 0/0 of 10 | 2/0 of 10 | 0/0 of 10 | 1/- of 10 | -/1 of 10 | 7/0 of 10 | 2/0 of 10 | 0/0 of 10 | -/0 of 10 | -/0 of 10 | 0/0 of 10 |
| breast_cancer | 0/1 of 10 | 5/0 of 10 | 0/0 of 10 | 2/- of 10 | -/0 of 10 | 3/0 of 10 | 4/0 of 10 | 0/0 of 10 | -/0 of 10 | -/1 of 10 | 0/2 of 10 |
| digits_parity | 0/2 of 10 | 0/0 of 10 | 0/0 of 10 | 8/- of 10 | -/6 of 10 | 3/0 of 10 | 0/0 of 10 | 0/0 of 10 | -/4 of 10 | -/7 of 10 | 0/10 of 10 |
| gauss_linear | 0/1 of 10 | 8/0 of 10 | 0/0 of 10 | 0/- of 10 | -/0 of 10 | 8/2 of 10 | 7/0 of 10 | 0/0 of 10 | -/2 of 10 | -/1 of 10 | 4/1 of 10 |
| moons_2scale | 0/3 of 10 | 0/0 of 10 | 0/1 of 10 | 10/- of 10 | -/4 of 10 | 0/10 of 10 | 0/6 of 10 | 0/0 of 10 | -/2 of 10 | -/9 of 10 | 0/9 of 10 |
| checker_2scale | 7/1 of 10 | 0/0 of 10 | 0/5 of 10 | 10/- of 10 | -/7 of 10 | 0/10 of 10 | 0/0 of 10 | 0/4 of 10 | -/3 of 10 | -/10 of 10 | 0/10 of 10 |

## Condition `noise20`: mean accuracy per fold set

| dataset | n_train | linear | rbf | best_global | knn_svm | cell_svm | vb_rbf | llsvm |
|---|---|---|---|---|---|---|---|---|
| wine | 142 | 0.978 | 0.977 | 0.977 | 0.949 | 0.966 | 0.972 | 0.977 |
| breast_cancer | 240 | 0.923 | 0.903 | 0.917 | 0.870 | 0.913 | 0.897 | 0.927 |
| digits_parity | 320 | 0.818 | 0.845 | 0.835 | 0.807 | 0.830 | 0.850 | 0.855 |
| gauss_linear | 320 | 0.935 | 0.933 | 0.932 | 0.885 | 0.920 | 0.930 | 0.927 |
| moons_2scale | 320 | 0.825 | 0.882 | 0.882 | 0.905 | 0.890 | 0.905 | 0.843 |
| checker_2scale | 320 | 0.502 | 0.765 | 0.765 | 0.788 | 0.730 | 0.780 | 0.768 |

### Paired difference vs best global (mean [95% bootstrap CI]), `noise20`

| dataset | knn_svm | cell_svm | vb_rbf | llsvm |
|---|---|---|---|---|
| wine | -2.83 [-5.70, -0.56] neg | -1.13 [-3.95, +1.16] none | -0.57 [-1.71, +0.00] none | +0.00 [+0.00, +0.00] none |
| breast_cancer | -4.67 [-8.00, -0.33] neg | -0.33 [-1.00, +0.00] none | -2.00 [-3.00, -1.00] neg | +1.00 [+0.00, +3.00] none |
| digits_parity | -2.75 [-4.75, -0.50] neg | -0.50 [-3.01, +1.75] none | +1.50 [+0.00, +4.00] none | +2.00 [+0.75, +3.50] pos |
| gauss_linear | -4.75 [-14.25, +0.50] none | -1.25 [-3.75, +0.50] none | -0.25 [-2.00, +1.50] none | -0.50 [-1.50, +0.00] none |
| moons_2scale | +2.25 [-1.25, +5.25] none | +0.75 [-5.50, +7.00] none | +2.25 [+0.50, +4.00] pos | -4.00 [-7.75, -0.25] neg |
| checker_2scale | +2.25 [-2.50, +7.00] none | -3.50 [-7.50, -0.00] none | +1.50 [+0.00, +3.50] none | +0.25 [-7.51, +8.25] none |

### Fraction of folds in which inner CV selected a local configuration, `noise20`

| dataset | best_global picks RBF | knn_svm | cell_svm | vb_rbf | llsvm |
|---|---|---|---|---|---|
| wine | 1.00 | 0.20 | 0.80 | 0.40 | 0.60 |
| breast_cancer | 0.40 | 0.60 | 0.60 | 0.20 | 0.40 |
| digits_parity | 0.80 | 0.80 | 0.60 | 0.40 | 1.00 |
| gauss_linear | 0.40 | 0.20 | 0.20 | 0.60 | 0.60 |
| moons_2scale | 1.00 | 1.00 | 1.00 | 0.80 | 1.00 |
| checker_2scale | 1.00 | 1.00 | 1.00 | 0.60 | 1.00 |

### Grid saturation (folds with the selected value at the lower/upper edge of the grid), `noise20`

| dataset | linear:C | rbf:gamma_mult | rbf:C | knn_svm:k | cell_svm:M | cell_svm:C | vb_rbf:gamma_mult | vb_rbf:C | vb_rbf:beta | llsvm:M | llsvm:C |
|---|---|---|---|---|---|---|---|---|---|---|---|
| wine | 0/0 of 5 | 1/0 of 5 | 0/0 of 5 | 0/- of 5 | -/0 of 5 | 4/0 of 5 | 2/0 of 5 | 0/0 of 5 | -/1 of 5 | -/0 of 5 | 2/0 of 5 |
| breast_cancer | 0/0 of 5 | 3/0 of 5 | 0/0 of 5 | 0/- of 5 | -/0 of 5 | 5/0 of 5 | 3/0 of 5 | 0/0 of 5 | -/0 of 5 | -/0 of 5 | 2/0 of 5 |
| digits_parity | 0/0 of 5 | 2/0 of 5 | 0/0 of 5 | 1/- of 5 | -/1 of 5 | 4/1 of 5 | 2/0 of 5 | 0/0 of 5 | -/1 of 5 | -/2 of 5 | 0/2 of 5 |
| gauss_linear | 0/0 of 5 | 4/0 of 5 | 0/0 of 5 | 1/- of 5 | -/0 of 5 | 3/1 of 5 | 3/0 of 5 | 0/0 of 5 | -/1 of 5 | -/1 of 5 | 1/0 of 5 |
| moons_2scale | 0/0 of 5 | 0/0 of 5 | 0/1 of 5 | 2/- of 5 | -/2 of 5 | 1/4 of 5 | 0/1 of 5 | 0/0 of 5 | -/1 of 5 | -/2 of 5 | 0/1 of 5 |
| checker_2scale | 3/0 of 5 | 0/0 of 5 | 0/0 of 5 | 3/- of 5 | -/4 of 5 | 0/4 of 5 | 0/0 of 5 | 0/0 of 5 | -/2 of 5 | -/5 of 5 | 0/5 of 5 |

## Condition `sub25`: mean accuracy per fold set

| dataset | n_train | linear | rbf | best_global | knn_svm | cell_svm | vb_rbf | llsvm |
|---|---|---|---|---|---|---|---|---|
| wine | 40 | 0.983 | 0.989 | 0.989 | 0.967 | 0.989 | 0.989 | 0.983 |
| breast_cancer | 60 | 0.953 | 0.963 | 0.960 | 0.940 | 0.933 | 0.950 | 0.960 |
| digits_parity | 80 | 0.800 | 0.912 | 0.912 | 0.915 | 0.887 | 0.918 | 0.857 |
| gauss_linear | 80 | 0.897 | 0.903 | 0.900 | 0.907 | 0.885 | 0.912 | 0.910 |
| moons_2scale | 80 | 0.833 | 0.858 | 0.855 | 0.830 | 0.905 | 0.910 | 0.880 |
| checker_2scale | 80 | 0.483 | 0.735 | 0.735 | 0.597 | 0.630 | 0.738 | 0.677 |

### Paired difference vs best global (mean [95% bootstrap CI]), `sub25`

| dataset | knn_svm | cell_svm | vb_rbf | llsvm |
|---|---|---|---|---|
| wine | -2.22 [-3.89, -0.56] neg | +0.00 [+0.00, +0.00] none | +0.00 [+0.00, +0.00] none | -0.56 [-1.67, +0.00] none |
| breast_cancer | -2.00 [-3.67, -0.33] neg | -2.67 [-5.00, -0.33] neg | -1.00 [-3.00, +0.00] none | +0.00 [+0.00, +0.00] none |
| digits_parity | +0.25 [-2.25, +3.00] none | -2.50 [-5.75, +0.25] none | +0.50 [-1.50, +3.50] none | -5.50 [-8.75, -2.00] neg |
| gauss_linear | +0.75 [-2.75, +5.50] none | -1.50 [-4.00, +1.00] none | +1.25 [-1.00, +3.50] none | +1.00 [-2.50, +4.51] none |
| moons_2scale | -2.50 [-5.25, +0.00] none | +5.00 [+2.25, +8.00] pos | +5.50 [+2.25, +9.00] pos | +2.50 [-0.00, +4.75] none |
| checker_2scale | -13.75 [-20.75, -8.00] neg | -10.50 [-16.25, -4.75] neg | +0.25 [-1.75, +2.00] none | -5.75 [-10.75, -1.00] neg |

### Fraction of folds in which inner CV selected a local configuration, `sub25`

| dataset | best_global picks RBF | knn_svm | cell_svm | vb_rbf | llsvm |
|---|---|---|---|---|---|
| wine | 0.60 | 0.40 | 0.20 | 0.40 | 0.00 |
| breast_cancer | 0.40 | 0.80 | 0.60 | 0.20 | 0.40 |
| digits_parity | 1.00 | 1.00 | 1.00 | 0.60 | 1.00 |
| gauss_linear | 0.80 | 0.60 | 0.80 | 0.60 | 0.80 |
| moons_2scale | 0.60 | 0.40 | 0.80 | 0.80 | 0.80 |
| checker_2scale | 1.00 | 0.80 | 1.00 | 0.60 | 1.00 |

### Grid saturation (folds with the selected value at the lower/upper edge of the grid), `sub25`

| dataset | linear:C | rbf:gamma_mult | rbf:C | knn_svm:k | cell_svm:M | cell_svm:C | vb_rbf:gamma_mult | vb_rbf:C | vb_rbf:beta | llsvm:M | llsvm:C |
|---|---|---|---|---|---|---|---|---|---|---|---|
| wine | 0/0 of 5 | 2/0 of 5 | 0/0 of 5 | 2/- of 5 | -/0 of 5 | 4/0 of 5 | 2/0 of 5 | 0/0 of 5 | -/1 of 5 | -/0 of 5 | 0/0 of 5 |
| breast_cancer | 0/0 of 5 | 2/0 of 5 | 0/0 of 5 | 1/- of 5 | -/0 of 5 | 0/1 of 5 | 2/0 of 5 | 0/0 of 5 | -/1 of 5 | -/0 of 5 | 1/0 of 5 |
| digits_parity | 0/1 of 5 | 1/0 of 5 | 0/1 of 5 | 4/- of 5 | -/5 of 5 | 3/0 of 5 | 0/0 of 5 | 0/0 of 5 | -/2 of 5 | -/3 of 5 | 0/1 of 5 |
| gauss_linear | 0/0 of 5 | 2/0 of 5 | 0/0 of 5 | 0/- of 5 | -/0 of 5 | 5/0 of 5 | 2/0 of 5 | 0/0 of 5 | -/2 of 5 | -/0 of 5 | 0/0 of 5 |
| moons_2scale | 0/2 of 5 | 1/1 of 5 | 0/3 of 5 | 0/- of 5 | -/3 of 5 | 5/0 of 5 | 0/3 of 5 | 0/1 of 5 | -/4 of 5 | -/2 of 5 | 0/0 of 5 |
| checker_2scale | 1/1 of 5 | 0/2 of 5 | 0/0 of 5 | 3/- of 5 | -/3 of 5 | 4/0 of 5 | 0/1 of 5 | 0/0 of 5 | -/1 of 5 | -/5 of 5 | 0/3 of 5 |

## Predefined criterion (main condition)

- **knn_svm**: CI>0 on 0/6 datasets, CI<0 on 2; majority criterion not met; named regimes none; added value: **no**
- **cell_svm**: CI>0 on 0/6 datasets, CI<0 on 4; majority criterion not met; named regimes none; added value: **no**
- **vb_rbf**: CI>0 on 1/6 datasets, CI<0 on 0; majority criterion not met; named regimes ['linear']; added value: **yes**
- **llsvm**: CI>0 on 0/6 datasets, CI<0 on 3; majority criterion not met; named regimes none; added value: **no**
