# PLAN — RTK001 Geometry of recursive knots (2026-09-30)

Budget: 75 min wall clock, ~10 CPU-min of numerics. Status of the line: paused; no previous manuscript.

## Object
Iterated cables by frame offsets. K_0 = circle radius R_0 = 1. For d >= 1, reparametrise K_{d-1}
to period 2*pi, take its closed rotation-minimising (Bishop) frame (N,B) with a linear twist added so it
is periodic, and set
  K_d(t) = K_{d-1}(t mod 2pi) + r_d [cos(q_d t/p_d + phi_d) N(t) + sin(q_d t/p_d + phi_d) B(t)],
  t in [0, 2 pi p_d), gcd(p_d,q_d)=1, p_d >= 2. Default (p,q) = (2,3) at every depth.

## Numerics (experiments/recursive_knots.py)
- Polygon with N vertices per depth. Compute: length L, minRad (circumradius of consecutive triples),
  dcsd = min distance between non-adjacent segments, tau = min(minRad, dcsd/2), Rop = L/tau.
- Grid over r_d = f * tau_{d-1} with f in {0.25, 0.35, 0.5} (fraction of previous polygonal thickness),
  depth d = 1, 2, 3. Convergence check in N (N and 2N) at d=1,2.
- Optional: gradient shrink of length with tau >= 1 at d=1,2 (numerical, uncertified).
- Outputs: results/results.json, results/tables.md, figures/*.png|pdf.
- make_numbers.py -> manuscript/numbers.tex, manuscript/table_*.tex.

## Theory (elementary, generous constants)
- Lemma A (embedding + thickness lower bound): if K_{d-1} is C^2 with thickness tau_{d-1}, curvature <= kappa_{d-1},
  and r_d <= tau_{d-1}/2, then K_d is embedded and thick(K_d) >= rho_d = min(tau_{d-1} - r_d, c * s_d),
  with s_d = strand separation on the torus of radius r_d with p_d strands. Justify c.
- Lemma B (length): |K_d'| <= |K_{d-1}'| (1 + r_d kappa_{d-1}) + r_d |theta'| gives
  L_d <= p_d L_{d-1} (1 + r_d kappa_{d-1}) + 2 pi q_d r_d.
- Corollary: recursion for Rop_d = L_d / rho_d; solve with r_d = f tau_{d-1}: multiplicative growth with explicit constant.
- Lower bounds: cite Buck–Simon 1999 and CKS 2002 only; crossing number of iterated cables not known in general -> no new lower bound.
- Everything else (stationarity, optimality, flow law) stated as conjecture / not claimed.

## Deliverables
README.md, CONTINUIDAD_RTK001_20260930.md, FICHA_RTK001_propuesta.md, manuscript/{main.tex, refs.bib, build.sh, numbers.tex, table_*.tex, main.pdf}, experiments/, results/, figures/.

## Time plan
09:05 start. 09:10 script written. 09:25 numerics done. 09:55 manuscript compiled. 10:10 README/CONTINUIDAD/FICHA. 10:20 hand back.
