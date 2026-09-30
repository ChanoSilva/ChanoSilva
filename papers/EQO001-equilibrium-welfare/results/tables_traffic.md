# E1: traffic (Pigou, affine price of anarchy, marginal-cost tolls)

Seed 20260930; 3.9 s.

## E1a Pigou, c_1 = 1, c_2 = x^d

| d | optimum flow on link 2 | optimum cost | PoA |
|---|---|---|---|
| 1 | 0.500000 | 0.750000 | 1.333333 |
| 2 | 0.577350 | 0.615100 | 1.625752 |
| 4 | 0.668740 | 0.465008 | 2.150502 |
| 8 | 0.759836 | 0.324591 | 3.080805 |
| 16 | 0.837716 | 0.211561 | 4.726765 |

## E1b/E1c random affine parallel links

- instances: 200
- PoA max 1.209428, mean 1.030508, median 1.002717
- bound violations (PoA > 4/3): 0
- max VI residual: 3.39e-11
- max |solver - water-filling|: 8.83e-11
- max |tolled equilibrium - optimum|: 2.22e-16
- max iterations: 2649
- fraction of instances with PoA > 1.01: 0.410; > 1.10: 0.120
