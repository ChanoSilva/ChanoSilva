# SVMF001 -- results (seed 20260930)


## Condition `main`: mean accuracy per fold set

| dataset | n_train | linear | rbf | best_global | knn_svm | cell_svm | vb_rbf | llsvm |
|---|---|---|---|---|---|---|---|---|
| wine | 142 | 0.992 | 0.997 | 0.997 | 0.994 | 0.989 | 0.997 | 0.992 |
| breast_cancer | 240 | 0.960 | 0.962 | 0.965 | 0.963 | 0.962 | 0.962 | 0.962 |
| digits_parity | 320 | 0.853 | 0.975 | 0.975 | 0.966 | 0.941 | 0.976 | 0.934 |
| gauss_linear | 320 | 0.939 | 0.934 | 0.931 | 0.920 | 0.930 | 0.939 | 0.935 |
| moons_2scale | 320 | 0.845 | 0.975 | 0.975 | 0.869 | 0.861 | 0.969 | 0.855 |
| checker_2scale | 320 | 0.508 | 0.870 | 0.870 | 0.739 | 0.688 | 0.870 | 0.693 |

### Paired difference vs best global (mean [95% bootstrap CI]), `main`

| dataset | knn_svm | cell_svm | vb_rbf | llsvm |
|---|---|---|---|---|
| wine | -0.28 [-1.11, +0.56] none | -0.85 [-2.25, +0.55] none | +0.00 [+0.00, +0.00] none | -0.57 [-1.67, +0.54] none |
| breast_cancer | -0.17 [-1.17, +1.00] none | -0.33 [-1.33, +0.50] none | -0.33 [-1.00, +0.00] none | -0.33 [-1.67, +0.83] none |
| digits_parity | -0.87 [-3.25, +1.13] none | -3.37 [-5.63, -1.25] neg | +0.13 [-0.37, +0.75] none | -4.12 [-5.50, -2.62] neg |
| gauss_linear | -1.13 [-2.38, +0.50] none | -0.12 [-1.00, +0.75] none | +0.75 [+0.12, +1.50] pos | +0.38 [-0.25, +1.13] none |
| moons_2scale | -10.63 [-14.25, -7.13] neg | -11.38 [-13.63, -9.00] neg | -0.62 [-1.88, +0.00] none | -12.00 [-14.50, -9.50] neg |
| checker_2scale | -13.12 [-17.00, -9.50] neg | -18.25 [-21.50, -15.00] neg | +0.00 [-1.88, +1.38] none | -17.75 [-20.75, -14.50] neg |

### Fraction of folds in which inner CV selected a local configuration, `main`

| dataset | best_global picks RBF | knn_svm | cell_svm | vb_rbf | llsvm |
|---|---|---|---|---|---|
| wine | 1.00 | 0.60 | 0.50 | 0.00 | 0.50 |
| breast_cancer | 0.60 | 0.30 | 0.30 | 0.20 | 0.40 |
| digits_parity | 1.00 | 1.00 | 1.00 | 0.50 | 1.00 |
| gauss_linear | 0.80 | 0.50 | 0.30 | 0.70 | 0.80 |
| moons_2scale | 1.00 | 0.80 | 0.90 | 0.10 | 1.00 |
| checker_2scale | 1.00 | 1.00 | 1.00 | 0.40 | 1.00 |

## Condition `noise20`: mean accuracy per fold set

| dataset | n_train | linear | rbf | best_global | knn_svm | cell_svm | vb_rbf | llsvm |
|---|---|---|---|---|---|---|---|---|
| wine | 142 | 0.978 | 0.977 | 0.977 | 0.949 | 0.966 | 0.972 | 0.972 |
| breast_cancer | 240 | 0.923 | 0.903 | 0.917 | 0.870 | 0.913 | 0.897 | 0.927 |
| digits_parity | 320 | 0.818 | 0.852 | 0.842 | 0.815 | 0.818 | 0.857 | 0.845 |
| gauss_linear | 320 | 0.935 | 0.933 | 0.932 | 0.930 | 0.920 | 0.930 | 0.932 |
| moons_2scale | 320 | 0.825 | 0.893 | 0.893 | 0.870 | 0.847 | 0.853 | 0.847 |
| checker_2scale | 320 | 0.502 | 0.790 | 0.790 | 0.713 | 0.620 | 0.792 | 0.622 |

### Paired difference vs best global (mean [95% bootstrap CI]), `noise20`

| dataset | knn_svm | cell_svm | vb_rbf | llsvm |
|---|---|---|---|---|
| wine | -2.83 [-5.70, -0.56] neg | -1.13 [-3.95, +1.16] none | -0.57 [-1.71, +0.00] none | -0.56 [-1.67, +0.00] none |
| breast_cancer | -4.67 [-8.00, -0.33] neg | -0.33 [-1.00, +0.00] none | -2.00 [-3.00, -1.00] neg | +1.00 [+0.00, +3.00] none |
| digits_parity | -2.75 [-4.50, -1.00] neg | -2.50 [-4.50, -0.50] neg | +1.50 [+0.00, +4.00] none | +0.25 [-2.75, +3.25] none |
| gauss_linear | -0.25 [-1.00, +0.50] none | -1.25 [-3.75, +0.50] none | -0.25 [-2.00, +1.50] none | +0.00 [+0.00, +0.00] none |
| moons_2scale | -2.25 [-9.00, +3.51] none | -4.50 [-10.51, +2.00] none | -4.00 [-9.25, -0.25] neg | -4.50 [-9.50, -0.75] neg |
| checker_2scale | -7.75 [-12.76, -4.00] neg | -17.00 [-18.75, -15.25] neg | +0.25 [-0.50, +1.00] none | -16.75 [-19.75, -14.00] neg |

### Fraction of folds in which inner CV selected a local configuration, `noise20`

| dataset | best_global picks RBF | knn_svm | cell_svm | vb_rbf | llsvm |
|---|---|---|---|---|---|
| wine | 1.00 | 0.20 | 0.80 | 0.40 | 0.40 |
| breast_cancer | 0.40 | 0.60 | 0.60 | 0.20 | 0.40 |
| digits_parity | 0.80 | 0.80 | 0.40 | 0.40 | 1.00 |
| gauss_linear | 0.40 | 0.00 | 0.20 | 0.60 | 0.60 |
| moons_2scale | 1.00 | 0.80 | 0.80 | 0.60 | 1.00 |
| checker_2scale | 1.00 | 1.00 | 1.00 | 0.60 | 1.00 |

## Condition `sub25`: mean accuracy per fold set

| dataset | n_train | linear | rbf | best_global | knn_svm | cell_svm | vb_rbf | llsvm |
|---|---|---|---|---|---|---|---|---|
| wine | 40 | 0.983 | 0.989 | 0.989 | 0.972 | 0.989 | 0.989 | 0.983 |
| breast_cancer | 60 | 0.953 | 0.960 | 0.960 | 0.953 | 0.930 | 0.960 | 0.960 |
| digits_parity | 80 | 0.800 | 0.922 | 0.922 | 0.825 | 0.785 | 0.918 | 0.832 |
| gauss_linear | 80 | 0.897 | 0.903 | 0.900 | 0.907 | 0.885 | 0.907 | 0.910 |
| moons_2scale | 80 | 0.833 | 0.847 | 0.850 | 0.830 | 0.847 | 0.892 | 0.835 |
| checker_2scale | 80 | 0.483 | 0.720 | 0.720 | 0.527 | 0.583 | 0.738 | 0.583 |

### Paired difference vs best global (mean [95% bootstrap CI]), `sub25`

| dataset | knn_svm | cell_svm | vb_rbf | llsvm |
|---|---|---|---|---|
| wine | -1.67 [-2.78, -0.56] neg | +0.00 [+0.00, +0.00] none | +0.00 [+0.00, +0.00] none | -0.56 [-1.67, +0.00] none |
| breast_cancer | -0.67 [-2.00, +0.00] none | -3.00 [-5.33, -0.67] neg | +0.00 [-1.00, +1.00] none | +0.00 [+0.00, +0.00] none |
| digits_parity | -9.75 [-11.75, -7.25] neg | -13.75 [-19.75, -8.25] neg | -0.50 [-1.50, +0.50] none | -9.00 [-11.75, -6.50] neg |
| gauss_linear | +0.75 [-2.75, +5.50] none | -1.50 [-4.00, +1.00] none | +0.75 [-1.25, +3.00] none | +1.00 [-2.50, +4.51] none |
| moons_2scale | -2.00 [-4.00, +0.00] none | -0.25 [-1.75, +1.25] none | +4.25 [-1.75, +9.00] none | -1.50 [-3.50, +0.25] none |
| checker_2scale | -19.25 [-22.75, -15.50] neg | -13.75 [-21.25, -6.25] neg | +1.75 [-0.25, +3.75] none | -13.75 [-22.75, -4.75] neg |

### Fraction of folds in which inner CV selected a local configuration, `sub25`

| dataset | best_global picks RBF | knn_svm | cell_svm | vb_rbf | llsvm |
|---|---|---|---|---|---|
| wine | 0.60 | 0.40 | 0.20 | 0.40 | 0.00 |
| breast_cancer | 0.40 | 0.60 | 0.40 | 0.00 | 0.40 |
| digits_parity | 1.00 | 0.40 | 0.60 | 0.60 | 1.00 |
| gauss_linear | 0.80 | 0.60 | 0.80 | 0.40 | 0.80 |
| moons_2scale | 0.60 | 0.40 | 0.40 | 1.00 | 0.80 |
| checker_2scale | 1.00 | 0.80 | 1.00 | 1.00 | 0.80 |

## Predefined criterion (main condition)

- **knn_svm**: CI>0 on 0/6 datasets, CI<0 on 2; majority criterion not met; named regimes none; added value: **no**
- **cell_svm**: CI>0 on 0/6 datasets, CI<0 on 3; majority criterion not met; named regimes none; added value: **no**
- **vb_rbf**: CI>0 on 1/6 datasets, CI<0 on 0; majority criterion not met; named regimes ['linear']; added value: **yes**
- **llsvm**: CI>0 on 0/6 datasets, CI<0 on 3; majority criterion not met; named regimes none; added value: **no**
