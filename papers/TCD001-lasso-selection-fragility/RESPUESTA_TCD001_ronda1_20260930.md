# Respuesta del autor al informe de árbitro interno — TCD001, ronda 1 (30/09/2026)

Respuesta redactada el 03/10/2026 sobre el borrador v0.1. Documento en construcción incremental: cada hallazgo se marca aquí en cuanto se atiende, para que una interrupción de la sesión deje constancia del estado real.

Convenciones: **Aceptado** = se aplicó el cambio tal como se pidió; **Aceptado con matiz** = se aplicó una versión y se explica la diferencia; **Rebatido** = no se aplica, con la demostración o el cálculo. Numeración de resultados según el PDF (Lema 2.4; Prop. 3.1; Cor. 3.2; Obs. 3.3; Prop. 3.4; Obs. 3.5; Prop. 4.1; Ej. 4.2 y 4.3; Teo. 5.1; Obs. 5.2; Conj. 5.3); se conserva idéntica en v0.2 (ver m1).

## Estado de avance (se actualiza durante la sesión)

| Paso | Estado |
|---|---|
| Lectura completa del informe, manuscrito, código, resultados, notas | hecho |
| B1: código (`single_removal_indices`, guarda KKT en `lasso_lars`) y enunciado del Cor. 3.2 | hecho |
| M3b/M4: corrida única de los cuatro scripts con la biblioteca final (03/10/2026 04:08–04:09 UTC, 84 s de CPU) | hecho |
| Edición del manuscrito (M1, M2, M3a, M5, M6, M7, menores, recortes) | hecho; ajuste final de extensión en curso |
| refs.bib (kuschnig2021 → CESifo WP 8981; Woodbury 1950 añadido y citado; broderick2020 v4) | hecho |
| README, CONTINUIDAD, ficha | pendiente |
| Compilación final, páginas, `??` = 0 | 0 errores, 0 `??`, 0 overfull; 11 páginas tras el primer recorte (objetivo ≤ 10, en curso) |

## Resumen de decisiones

(Se completa al final; ver tabla detallada abajo.)

## Hallazgo bloqueante

### B1 — Cor. 3.2 enuncia `h_i < 1` como incondicional. **Aceptado.**

El árbitro tiene razón: el enunciado era incondicional y la prueba condicional. El contraejemplo (n = p = 2, X = I₂, y = (3,3)ᵀ, μ = 1) es correcto: β̂ = (2,2)ᵀ, S = {1,2}, A = I y h₁ = h₂ = 1; quitar una observación deja X_{S,−i} con una columna nula. Cambios:

- Enunciado reescrito: la hipótesis `h_i < 1` (equivalente a rango completo de X_{S,−i}) aparece como condición; `h_i = 1` se remite al caso (a) de la Prop. 3.1 (rango deficiente, (S, s) no se conserva); convención ι_i := +∞ cuando h_i = 1, con lo que `max_i ι_i < 1 ⇒ f ≥ 2` sigue siendo válido sin excepción. Se añaden además las convenciones de m11 (Sᶜ = ∅ ⇒ γ = ∞, término 0; γ = 0 o m = 0 son fronteras).
- Código: `single_removal_indices` (`lasso_fragility.py`) ahora trata explícitamente `h_i ≥ 1 − 10⁻¹²` con `e_i = ι_i = +∞` (antes dependía de la división por cero de NumPy, que da `inf` pero daría `nan` si además r_i = 0). El contraejemplo del árbitro se añadió como comprobación ejecutable (`experiments/check_b1_counterexample.py`): `removal_test` devuelve "no conservado" por rango (det(I − H_R) = 0) para R = {1} y R = {2}, e ι = +∞ en ambas observaciones.

## Hallazgos mayores

(pendientes de redacción final; ver tabla de estado)

## Hallazgos menores

(pendientes de redacción final; ver tabla de estado)

## Lista de acciones del árbitro (13)

(pendiente)

## Números que cambiaron

(pendiente: se compara v0.1 contra la corrida única de v0.2)

## Lo que queda abierto

(pendiente)
