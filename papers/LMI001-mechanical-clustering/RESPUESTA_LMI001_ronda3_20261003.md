# Respuesta del autor — LMI001, ronda 3 de revisión interna (03/10/2026) [EN CURSO]

Informe atendido: `REFEREE_LMI001_ronda3_20261003.md` (veredicto: cambios menores; 0 bloqueantes, 3 mayores, 12 menores; los siete resultados nuevos de v0.4 —Prop. 3.2, Cor. 3.3, Cor. 3.6, Rem. 3.7, Prop. 4.2, Prop. 4.3, Rem. 4.5— confirmados correctos). Manuscrito resultante: **v0.5** (3 October 2026).

Documento escrito de forma incremental durante la sesión; el estado final de cada punto está en su sección.

## Plan de trabajo

1. M1: verificar por mi cuenta la cota uniforme (prueba + PL propio), añadirla como parte (b) de la Prop. 4.3 y corregir el comentario, README y CONTINUIDAD.
2. M2: texto sustituto del árbitro (tensión = normalización total; apertura de la Sección 4; *Limitations*; *Next step* (a)); coherencia de resumen, Introducción, README y FICHA.
3. M3: recortes 2–5 del árbitro (Tabla 1 fuera, E3 condensado, Teorema 3.4(f) recortado, resumen ≤ 220 palabras); la nota aparte (recorte 1) **no** se hace por decisión del autor humano: plan anotado en CONTINUIDAD.
4. Menores m1–m12.
5. Compilación, revisión visual, CONTINUIDAD, README, FICHA.

## Respuesta punto por punto

(Se completa a medida que se aplican los cambios.)

### Mayores

**M1 (Prop. 4.3: "bounds no distance" es falso para A densa) → aceptar (y la cota pasa al enunciado).**
*Verificación propia de la cota.* Con los grupos G₁,…,G₄ y el aniquilador ν de la prueba: (i) ‖ν‖₁ = Σ_t ω̂_t(Ω̂−ω̂_t) + Σ_{2+2} ω̂(X)ω̂(Y) = 2ê₂ + 2ê₂ = 4ê₂, con ê₂ = Σ_{t<u} ω̂_tω̂_u (el primer sumando es Ω̂² − Σω̂_t²; en el segundo cada par t<u aparece en exactamente dos de los tres cortes 2+2); (ii) ⟨ν, E_tot⟩ = 2Σ_{t<u} Â_tu ω̂_vω̂_z, y como {t,u} ↦ {v,z} permuta los seis pares y Â_tu = Σ_{i∈G_t, j∈G_u} A_ij ≥ min_{i≠j} A_ij (A ≥ 0), ⟨ν,E_tot⟩ ≥ 2·min A·ê₂; (iii) para g = J^ω_K + c, ⟨ν, E_tot − g⟩ = ⟨ν, E_tot⟩ y, por Hölder, max_C |E_tot − g| ≥ ⟨ν,E_tot⟩/‖ν‖₁ ≥ ½ min_{i≠j} A_ij, para todo ω ∈ (0,∞)ⁿ, K y c. Para F^w_A (grupos unitarios, w(3) ≥ w(2), w(3) > 0) el primer término del emparejamiento es ≥ 0 y el segundo ≥ 2w(3)·min A·ê₂: cota ½w(3)·min A. **La constante ½ no se puede mejorar:** con A_ij ≡ 1 y k = n−2 toda k-partición tiene un bloque de 3 o dos de 2, E_tot ∈ {2,3}, y K = 0, c = 5/2 dan exactamente ½ (lo confirma el PL: cociente 1.0000 en n = 4, 5, 6).
*Chequeo numérico propio por PL* (`experiments/check_bound_prop43.py`, salida `results/check_bound_prop43.txt`, semilla 20261003, 69 s de CPU; escrito desde cero, sin importar nada del código del paper ni de `theory/`): distancia uniforme exacta (PL HiGHS) de E_tot a 𝒢_ω + ℝ para n = 4,5,6 y k = 2,…,n−2, cuatro tipos de A densa (Hooke, cuerda φ = d, longitud de reposo, uniforme) y 55–76 vectores ω por caso (aleatorios con log ω ∈ [−6,6] y degenerados con dos pesos a 10⁻² o 10⁻⁴ o a 10² o 10⁴): cociente mínimo distancia/(½ min A) = **1.0000** sobre los 24 casos (nunca < 1; igual a 1 para A uniforme con k = n−2). Versión con pesos de tamaño w(2) = 1, w(3) = 2: cocientes ≥ 3.08. Caso con un solo resorte no nulo (n = 4, k = 2, ω = (1,1,ε,ε)): distancia por PL = ⟨ν,E⟩/‖ν‖₁ a todas las cifras, 8.3×10⁻² (ε = 1), 3.5×10⁻³, 4.8×10⁻⁵, 5.0×10⁻⁷ (ε = 10⁻³) → 0. k = n−1: E_tot ∈ 𝒢_ω (distancia 0), y 𝒢_ω + ℝ tiene dimensión = número de particiones.
*Cambios.* Prop. 4.3 dividida en (a) (el enunciado anterior) y (b) (la cota uniforme, con la versión para F^w_A y "the constant ½ cannot be improved"); estado "[proved here; (a) checked by an independent internal referee (round 3); (b) suggested by that referee, proof re-derived and checked by linear programming by the author]". Prueba de (b) añadida al Apéndice B como paso (4), con el caso de igualdad. El comentario que sigue a la proposición ya no dice "bounds no distance": dice que ‖ν‖₁ = 4Σω̂_tω̂_u da la cota cuando todas las A_ij fuera de la diagonal son positivas, y que con entradas nulas la cota puede anularse y la distancia tender a 0 (un solo resorte A₁₂, n = 4, k = 2, ω₃, ω₄ → 0). Resumen, *Contribution*, Tabla 2, README y CONTINUIDAD corregidos en el mismo sentido (se retira "pequeño cuando ω degenera" para A densa; los "residuos pequeños" del integrador con log ω de ±10 a ±30 se declaran compatibles con la cota o artefacto de condicionamiento, no evidencia en contra).
