# E2-E4: welfare-weight cones

Seed 20260930; 127.9 s.

## E2 two-player example
- x* = [1.0, 1.0], F(x*) = [-1.0, -1.0], residual 0.0e+00
- boundary angles (deg): [26.56505117707799, 63.43494882292201]
- 181/181 directions: closed form = first-order cone = exact QP; 73 directions inside
- witness lambda = [1.0, 3.0]: member False, gap 0.1250, better x = [0.5, 1.0]

## E2 Cournot
- interior: x* = [0.3333333333334513, 0.3333333333334513], cone nontrivial: False, grid points in Lambda: 0/61
- boundary: x* = [1.0, 1.0], cone dim 1, vertices [[0.5, 0.5]], grid agreement 61/61
- Nikaido-Isoda: x* optimal for all lambda: True (max W' over grid 2.78e-17)

## E3/E4 random games

| N | concave | instances | nontrivial | dims | tested in L1 | of which in L | grid out L1 | out L | grid in L1 | in L | witness inst. | max resid |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| 3 | True | 100 | 28 | {'1': 4, '2': 5, '3': 19} | 115 | 115 | 8525 | 8525 | 575 | 575 | 0 | 7.7e-12 |
| 4 | True | 100 | 33 | {'1': 2, '2': 7, '3': 15, '4': 9} | 153 | 153 | 16193 | 16193 | 307 | 307 | 0 | 6.6e-12 |
| 3 | False | 100 | 57 | {'1': 13, '2': 14, '3': 30} | 206 | 162 | 8037 | 8037 | 1063 | 1025 | 23 | 2.1e-12 |
| 4 | False | 100 | 46 | {'1': 2, '2': 2, '3': 13, '4': 29} | 246 | 152 | 15163 | 15163 | 1337 | 1265 | 35 | 2.0e-12 |
