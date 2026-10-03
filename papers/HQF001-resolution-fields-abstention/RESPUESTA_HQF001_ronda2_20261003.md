# Respuesta del autor — HQF001, ronda 2 de revisión interna (03/10/2026)

Objeto: informe `REFEREE_HQF001_ronda2_20261003.md` sobre el borrador v0.2. Resultado: borrador v0.3 (3 October 2026).

Estado de este archivo: en redacción (se escribe de forma incremental; la versión final sustituye esta línea).

## Bitácora (orden de trabajo)

1. 10:02 UTC — v0.2 conservada en `results/v02/` (`results.json`, `tables.md`, `run_log_v02.txt`; sha256 de `results.json` = `a6c8103f…`).
2. 10:02 — `selective_benchmark.py` v0.3: rejilla del campo ampliada (K_m ∈ {20, 40, 80, 160, 320}, α ∈ {0.05, 0.2, 0.5, 0.7, 0.9}), regla de empate para K_m recortado, función `grid_saturation` y sección de saturación en `tables.md`. Prueba de humo: 2 pliegues de iris, campo idéntico a v0.2 en ambos (3.4 s de CPU).
3. 10:03 — `PREREGISTRO_HQF001_rejilla_20261003.md` escrito antes de lanzar la corrida (sha256 del script `35aefc57…`). Corrida completa v0.3 lanzada a las 10:03:18 UTC (log `results/run_log_v03.txt`).
4. Mientras corre: verificación en git (solo lectura) de R2-M2; `CRITERIO_HQF001.md` reescrito; `experiments/spectrum_scan.py` (R2-M3, 0.3 s de CPU).

## Respuesta punto por punto

(se completa abajo)

### R2-M2 — Registro de la predefinición. **Aceptar.**
Verifiqué con comandos de solo lectura (`git show 31398e3 --stat`, `git ls-tree -r 31398e3`/`0c3bde3`, `git diff 31398e3 0c3bde3`, `git diff e776acc 2040e2b`, `sha256sum` de cada versión): todo lo que dice el árbitro es exacto. `31398e3` (30/09 08:29:24 UTC) contiene el script con el código del criterio y no contiene `results/results.json`, que aparece en `0c3bde3` (08:44:39 UTC); entre ambos, repeticiones 4 → 3, LogReg C {0.01, 0.1, 1, 10, 100} → {0.1, 1, 10}, QDA sin `reg_param = 0`; el hash registrado en v0.2 (`ad5322…`) es el del script de `2040e2b`, posterior a la corrida; el que corrió es el de `e776acc` (`40280a3e…`). Cambios: `CRITERIO_HQF001.md` reescrito (historia en 6 puntos: registro `31398e3`, prueba rápida previa con veredicto impreso sobre datos reducidos, cambios de repeticiones y rejillas, cambios de B y sembrado entre v0.1 y v0.2, regeneración de synth-classcov, v0.3; tabla de hashes de cada corrida, incluida la v0.1 `841839…` y su re-resumen `51017d…`); "fixed before the run" pasa a "fixed before the first run" en el manuscrito y el párrafo "Predefined criterion" declara lo mismo.
