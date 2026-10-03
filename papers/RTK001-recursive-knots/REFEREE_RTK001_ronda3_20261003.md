# [EN CURSO] Informe de árbitro independiente — RTK001, ronda 3 (verificación de teoremas nuevos)

Fecha: 03/10/2026. Árbitro: independiente, nuevo (no participó en rondas 1–2).
Objeto: manuscrito v0.3 (`manuscript/main.tex`, commit e7a21ab), Lema 3.9, Prop. 3.10, Cor. 3.11, Prop. 3.12, Teo. 3.13; respuesta a la ronda 2.

(Informe en construcción; se completa de forma incremental.)

## Notas de trabajo (se reordenan al final)

- Formas cerradas recalculadas con mpmath (30 dígitos), script propio `scratchpad/referee3_RTK001/closed_forms.py`:
  τΩ̄(d=1,f=½) = 2.940383; δ_R1 = 1.0684297 (> 1.0684, margen 3·10⁻⁵); sin(δ_R1/2) = 0.5091654 (la RESPUESTA dice 0.509170: sexta cifra mal, la cota "> 0.509" es correcta); c* = 1.0183309; φ_c*(1/√2) = 0.279931 (> 0.279), φ_c*(1) = 0.410873 (> 0.410), φ'_c*(1/√2) = 1.810096 (> 1.81); δ_R2 a priori (Θ = ζ = √13/2) = 1.6773739 (> 1.677); Θ* = 1.112080 (el texto dice "needs Θ_min ≥ 1.12": falso como necesidad, debe ser 1.112); c₀′ a priori (d ≥ 2, f = ½) = 0.74363 con max(Λ, ℓ₀−2r) y 0.71478 con Λ solo; δ_R2 en d = 1, f = ½ = 0.93560 < π/3 (R1 es imprescindible en d = 1); 1/(rκ̄₁) = 0.561492 (f = ½); min Λ/r en [π/3, π) a f = ½ = 1 exactamente en δ = π/3.
- Chequeo independiente `scratchpad/referee3_RTK001/indep_check.py` (curvas lisas por muestras + derivadas espectrales FFT; marco de Bishop por RK4 sobre N' = −(N·T')T con datos en medios nodos por sobremuestreo espectral; detector de pares doblemente críticos = ceros comunes de F₁, F₂ vía cambios de signo de G = F/(|X₂−X₁| sin w), w = u₂−u₁−π, en malla desplazada medio paso — elimina los dos conjuntos degenerados (diagonal y familia antipodal) —, refinamiento de Newton sobre F/sin w con evaluación de Taylor de orden 9, clasificación por hessiana de la distancia). N = 512, 1024, 4096 en d = 1, 2, 3 (cola espectral < 2·10⁻¹⁴). 8 min de CPU (exceso sobre el presupuesto: el Newton en Python con 9 170 y 18 349 celdas candidatas en d = 3).
  Resultados (f = 0.5): τ₁/r₁ = 0.83164, par crítico k = 1, δ = 1.812 (103.8°); d = 2: τ/r = 1.0000, Θ_min = 2.1877, α = −3.027, m = 1.982, siguiente par a 2.0274 r (margen 1.37 %), minRad/r = 3.07; d = 3: τ/r = 1.0000, Θ_min = 9.598, siguiente par 2.0403 r (2.0 %), minRad/r = 5.24.
  (f = 0.35): τ/r = 1.0000 en d = 1, 2, 3; Θ_min = 0.667, 3.840, 25.80; siguiente par 5.23 r, 4.05 r, 4.17 r; minRad/r = 2.28, 5.76, 15.75.
  Censo de misma hebra (k = 0, bases distintas, δ < π): d = 1: 9 raíces (f = ½) y 9 (f = 0.35), todas silla o máximo (0 mínimos), δ ≥ 1.9669 / 2.1483, distancia ≥ 3.7014 r / 5.2346 r; d = 2, 3: ninguna (ni tampoco ningún par k = 1 con δ < π: todos los pares doblemente críticos genuinos tienen δ ≥ π). Coincide con el censo reconciliado del autor.
