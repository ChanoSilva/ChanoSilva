# SVMF001 — Respuesta del autor a la ronda 3 de revisión interna (informe del 03/10/2026)

**[EN CURSO]**

Respuesta redactada el 03/10/2026 en una sesión de Claude Code (session_01MTmjU2K8b4sgpjjL3JTtDz), en el papel de autor. Informe atendido: `REFEREE_SVMF001_ronda3_20261003.md` (veredicto: cambios menores, solo de texto; 0 bloqueantes, 3 mayores, 10 menores; Prop. 3.6, Cor. 3.7, Lemas 3.8–3.10, Teorema 3.11 y Cor. 3.12 de v0.4 confirmados correctos; Obs. 3.13 heurística). Manuscrito v0.4 → **v0.5** (fecha fija 3 October 2026).

## Decisión general

No se vuelve a correr la comparación ni `theory/check_knn_localisation.py` (no se ejecuta en su sitio; `theory/` no se toca). Todos los cambios son de texto, salvo `experiments/make_knn_numbers.py` (m7 y macros nuevas para M2), que sigue leyendo el JSON congelado y comprobando su SHA-256.

(Se completa abajo, punto por punto.)
