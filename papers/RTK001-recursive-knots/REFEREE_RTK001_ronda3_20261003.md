# [EN CURSO] Informe de árbitro independiente — RTK001, ronda 3 (verificación de teoremas nuevos)

Fecha: 03/10/2026. Árbitro: independiente, nuevo (no participó en rondas 1–2).
Objeto: manuscrito v0.3 (`manuscript/main.tex`, commit e7a21ab), Lema 3.9, Prop. 3.10, Cor. 3.11, Prop. 3.12, Teo. 3.13; respuesta a la ronda 2.

(Informe en construcción; se completa de forma incremental.)

## Notas de trabajo (se reordenan al final)

- Formas cerradas recalculadas con mpmath (30 dígitos), script propio `scratchpad/referee3_RTK001/closed_forms.py`:
  τΩ̄(d=1,f=½) = 2.940383; δ_R1 = 1.0684297 (> 1.0684, margen 3·10⁻⁵); sin(δ_R1/2) = 0.5091654 (la RESPUESTA dice 0.509170: sexta cifra mal, la cota "> 0.509" es correcta); c* = 1.0183309; φ_c*(1/√2) = 0.279931 (> 0.279), φ_c*(1) = 0.410873 (> 0.410), φ'_c*(1/√2) = 1.810096 (> 1.81); δ_R2 a priori (Θ = ζ = √13/2) = 1.6773739 (> 1.677); Θ* = 1.112080 (el texto dice "needs Θ_min ≥ 1.12": falso como necesidad, debe ser 1.112); c₀′ a priori (d ≥ 2, f = ½) = 0.74363 con max(Λ, ℓ₀−2r) y 0.71478 con Λ solo; δ_R2 en d = 1, f = ½ = 0.93560 < π/3 (R1 es imprescindible en d = 1); 1/(rκ̄₁) = 0.561492 (f = ½); min Λ/r en [π/3, π) a f = ½ = 1 exactamente en δ = π/3.
