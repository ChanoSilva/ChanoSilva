# Respuesta del autor al informe de la ronda 2 — SGE001 (03/10/2026)

Informe: `REFEREE_SGE001_ronda2_20261003.md` (cambios mayores acotados; 0 bloqueantes, 4 mayores, 13 menores; reproducción bit a bit).
Estado de este documento: **en redacción** (se escribe de forma incremental mientras se aplican los cambios).

## Plan de trabajo

1. M1 (certificados): separar certificado con microdatos (por segmento) y certificado con momentos + rango; añadir certificado de C1 (6B₂ < |Q₂|) y fracciones certificadas de E4 con cada cota; macros.
2. M2 (C1 vs C2 en resumen y ficha).
3. M3 (E1c con 60 réplicas, errores estándar, N = 200000 si cabe).
4. M4 (razón desplazada: distribución por réplica).
5. Menores m1–m13 y recortes hasta ≤ 10 páginas.

## Respuesta punto por punto

(se completa a medida que se aplican los cambios)

### Registro de avance (código y corrida)

- [hecho] Copia de seguridad de v0.2 (resultados, manuscrito, scripts) en el scratchpad de la sesión (`sge001_r2/`).
- [hecho] `frontier_aggregation.py`: (M1) certificados con la cota por segmento (microdatos) y con la cota de momento + rango (`B2box`), para k = 1 (`2B₂<|Q₂|`) y k = 5 (`6B₂<|Q₂|`), y mayor σ con razón observada > 1 en todas las réplicas; fracción certificada en E4 con ambas cotas; comentario del código corregido. (M3) E1c con 60 réplicas para N = 200, 2000, 20000, 200000 (en bloques de 6 réplicas), errores estándar bootstrap (500 remuestreos) y mediana de |E₂−E₃|/Y en σ = 0.01. (M4) E2 guarda mínimo, máximo y mediana de |T_u/(στ_z(b))−1| y la fracción de réplicas con P_u<Q_u. (m6) errores estándar bootstrap de los exponentes de E2. (m13) un generador de bootstrap por experimento (`spawn(12)`; los 9 primeros hijos son los de v0.2). (m15) contigüidad en `LN_delta0_lower_informative_largest_sigma`. (m12) `meta` guarda cálculo y total (con tablas y figuras), pared y CPU.
- [hecho] Corrida de referencia v0.3 completa (sin `--fast`): 51.6 s de cálculo / 55.5 s con tablas y figuras (pared), 53.4 / 57.3 s de CPU; SHA-256 `5b309162009c…` (coincide con `sha256sum` del script en disco). Comparación hoja a hoja con v0.2 (8782 valores comunes): **todos los valores puntuales de E0, E1, E1b, E2, E3, E4, E5, E6 son idénticos**; cambian sólo E1c (rediseñado) y los intervalos bootstrap de E2 y E3 (nuevo generador de bootstrap, m13), como estaba previsto.
