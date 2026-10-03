# Respuesta del autor — TCD001, ronda 2 de revisión interna (03/10/2026)

Objeto: informe `REFEREE_TCD001_ronda2_20261003.md` (cambios menores; 0 bloqueantes, 3 mayores, 13 menores; verificación de la ronda 1: 22 bien, 2 a medias, 1 con error nuevo). Versión resultante: borrador v0.3 (3 October 2026).

Estado de esta respuesta: EN CURSO (se escribe de forma incremental; la sección final "Resumen" se completa al terminar).

## Registro de trabajo

- [inicio] Leídos los briefs, el informe y `main.tex` v0.2.
- [código] `lasso_fragility.py`: contador `KKT_STATS` (llamadas, retrocesos, clasificación de retrocesos —empate exacto en la entrada, rango completo—, errores KKT relativos máximos de las salidas aceptadas, rechazadas y de descenso por coordenadas), segunda verificación KKT tras el retroceso con `RuntimeError` si falla (m11), docstring de `kkt_residuals` corregido (m11). Los cuatro scripts reinician el contador y lo vuelcan en `meta.kkt_guard` de su JSON. `exact_examples.py --no-guard` escribe `results/examples_noguard.json` para la comparación con y sin guarda. Nuevo `snapshot_cost_ratios.py`: archivó los cocientes de coste de la corrida v0.2 en `results/cost_ratios_previous_run.json` antes de volver a correr (M2(v)). IQR de los cocientes de coste en `fragility.md` y `scaling.md` (m13).
- [corrida] Corrida de referencia v0.3 completa en una sola sesión (03/10/2026 10:00:07–10:02:00 UTC, `results/run_session_v03.txt`): E0 1.6 s, E0 sin guarda 1.5 s, E1 9.8 s, E2/E3/E5 50.9 s, E4 45.5 s de pared. Contadores: E0 950 ajustes, 91 retrocesos (91 con empate exacto de |x_jᵀy| en la entrada, 91 con X de rango completo), error activo máximo de una salida rechazada 6.2·max(1, μ); E1 0/16 191; E2/E3/E5 0/117 708; E4 0/10 365; error activo máximo aceptado en E1–E5: 3.6·10⁻¹⁴ relativo a max(1, μ). `examples.json` idéntico con y sin guarda e idéntico al de v0.2. Coinciden exactamente con la tabla de M1 del árbitro.
