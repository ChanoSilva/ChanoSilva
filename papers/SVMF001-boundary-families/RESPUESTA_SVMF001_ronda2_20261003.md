# SVMF001 — Respuesta del autor a la ronda 2 de revisión interna (informe del 03/10/2026)

Respuesta redactada el 03/10/2026 en una sesión de Claude Code (session_01MTmjU2K8b4sgpjjL3JTtDz), en el papel de autor. Informe atendido: `REFEREE_SVMF001_ronda2_20261003.md` (veredicto: cambios mayores, solo de texto; 0 bloqueantes, 7 mayores, 10 menores; reproducción bit a bit; ningún hallazgo cambia el veredicto del criterio).

*Documento escrito de forma incremental; las secciones se completan a medida que se aplican los cambios.*

## Decisión general sobre una nueva corrida

**No se vuelve a correr la comparación en esta ronda.** El preregistro de v0.2 comprometía una sola corrida, el árbitro pide expresamente que la ampliación de rejillas (γ de VB-RBF-SVM por arriba; C de cell-SVM y LLSVM hasta 1000) se haga "en la próxima corrida (no en esta ronda)" bajo un preregistro con commit propio, y ampliar ahora, tras haber visto qué bordes saturan, sería exactamente el tipo de elección de rejilla a posteriori que el preregistro excluye. En su lugar, todo lo afectado por la saturación se marca "measured, grid-limited" en el manuscrito, la tabla de afirmaciones, el README, la ficha, la nota de continuidad y una anotación fechada del preregistro. Ningún número de la corrida de referencia cambia; se añaden macros nuevas (recuentos de saturación por conjunto, esperanzas unilaterales, cobertura simulada del bootstrap, desglose de la celda gaussiana) generadas por `make_numbers.py` desde los mismos JSON.

## Hallazgos mayores

(en curso)

## Hallazgos menores

(en curso)

## Verificación de la ronda 1 (puntos a medias o con error nuevo)

(en curso)

## Bibliografía

(en curso)

## Extensión

(en curso)

## Cómputo usado

(en curso)

## Qué queda abierto

(en curso)
