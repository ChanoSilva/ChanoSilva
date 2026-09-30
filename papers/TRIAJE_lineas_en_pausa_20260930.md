# Triaje de las líneas de investigación en pausa y archivadas (30/09/2026)

Fuente: fichas públicas de `investigacion.html` / `research-en.html` (CV web). Sesión de Claude Code `session_01MTmjU2K8b4sgpjjL3JTtDz`, rama `claude/charming-pasteur-2cajqb`. Ninguna línea contaba con manuscrito previo accesible desde este entorno (GitHub y Drive revisados; Gmail sin autorizar), así que todo avance parte de la ficha y se declara como reconstrucción.

Criterio de triaje: una línea es **tractable aquí** si su siguiente paso es una demostración, un contraejemplo o un cómputo reproducible sin datos externos, sin sujetos humanos y sin ejecuciones de modelos de lenguaje. En caso contrario se anota el bloqueo y el paso mínimo que lo levantaría.

## A. Avanzadas en esta sesión (carpeta propia en `papers/`)

| Código | Línea | Avance | Carpeta |
|---|---|---|---|
| MRT001 | Invariantes y fundamentos geométricos | Manuscrito v0.4 (18 pp.), 5 proposiciones nuevas, 6 familias de experimentos (E1–E5e), dos rondas de revisión interna aplicadas | `MRT001-foundational-geometry/` |
| SPD001 | Geometría del soporte y vecinos cercanos | **Hecho:** comparación aislante con criterio predefinido (5/8 exigidas), resultado negativo 0/8; HKNN = combinación exacta de ortogonal + tangencial (demostrado); propuesta de cierre de la línea | `SPD001-support-geometry-knn/` |
| LMI001 | Analogías mecánicas para agrupamiento | **Hecho:** teorema "agrupamiento mecánico = agrupamiento por kernels" (potenciales de pares, levantamiento, tensión, relajación = Hartigan) que explica el cribado nulo; certificados exactos de qué ingredientes salen de la familia; vía dinámica formulada como problema abierto; borrador v0.1 (15 pp.) | `LMI001-mechanical-clustering/` |
| TCD001 | Fragilidad de la selección con Lasso | **Hecho:** test exacto de eliminación en forma cerrada (KKT + Woodbury), no monotonía de los testigos, NP-completitud de la deselección con p = 1 (Subset Sum), números de fragilidad exactos hasta n = 34; criterio predefinido de ventaja computacional de las heurísticas no cumplido; borrador v0.1 (15 pp.) | `TCD001-lasso-selection-fragility/` |
| SGE001 | Agregación dinámica de fronteras productivas | **Hecho:** identidades de resto y cotas en régimen suave; en cruces de capacidad el error de segundo orden es −N·T_u (demostrado) y el segundo orden no aporta; condición de margen para comparaciones; criterio predefinido de mejora 5× no se cumple en general; borrador v0.1 (15 pp.) | `SGE001-frontier-aggregation/` |
| RTK001 | Geometría de nudos recursivos | En curso (segundo intento; el primero no produjo archivos): cables iterados por marcos de Bishop, espesor poligonal numérico para d = 1, 2, 3, lema de condición suficiente con recursión de la cota | `RTK001-recursive-knots/` |
| HQF001 | Resolución local e incertidumbre | **Hecho:** comparación controlada de clasificación selectiva (8 conjuntos, 7 referencias) con criterio predefinido, resultado negativo (0/8 mejor, 6/8 peor); proposición exacta que aísla qué podría aportar la anisotropía; propuesta de cierre; borrador v0.1 (11 pp.) | `HQF001-resolution-fields-abstention/` |
| EQO001 | Operadores de equilibrio y bienestar | **Hecho:** nota "qué es y qué no es teorema" (potencial, monotonía, precio de la anarquía, condición de cono para óptimos de bienestar) con problemas abiertos; v0.1 (13 pp.) | `EQO001-equilibrium-welfare/` |

El estado detallado (qué se demostró, qué se midió, qué no se afirma) está en el `CONTINUIDAD_*.md` de cada carpeta. Cada resultado es una reconstrucción a partir de la ficha; si existe material previo del autor, debe fusionarse.

## B. Tractables en principio, pero dependientes de artefactos originales que no están aquí

| Código | Línea | Qué falta | Paso mínimo |
|---|---|---|---|
| EKS001 | Aceleración exacta de trayectorias de muestreo | El código y el diseño de las 72 corridas (qué certificado de reutilización, qué muestreador) | Publicar en el repo el script original; entonces puede intentarse (a) un modelo de coste que prediga cuándo la reutilización exacta paga y (b) una reimplementación con estructuras de datos distintas |
| HFN001 | Neuronas funcionales y crecimiento de modelos | La gramática de operadores y las referencias emparejadas del criterio primario | Documentar la gramática y el presupuesto de cómputo; la comparación puede reproducirse en CPU con MLP pequeños |
| SVMF001 | Familias de fronteras de clasificación | Las variantes concretas evaluadas y los regímenes | **Hecho en esta sesión como reconstrucción** (`SVMF001-boundary-families/`, v0.1, 14 pp.): enunciado exacto de cuándo la adaptación local no puede ayudar; comparación controlada de cuatro familias con criterio predefinido, ninguna lo cumple. Si aparecen las variantes originales, basta situarlas en la misma comparación |
| OMR001 | Correcciones transferibles entre tareas de estimación | La definición del operador de corrección y de la "referencia segura" | **Hecho en esta sesión como reconstrucción** (`OMR001-transferable-corrections/`, v0.1, 14 pp.): teorema de imposibilidad para correcciones aprendidas en fuentes y cota explícita de no-daño para la reversión validada, que es una garantía de selección y no del operador. Si aparecen las definiciones originales, solo hay que calcular E‖C−R‖ |
| PVS001 | Trazabilidad y reproducción de procesos | Nada técnico: la ficha ya concluye que no hay contribución científica independiente | Mantener como infraestructura (los scripts `make_numbers.py` de estas carpetas son un ejemplo operativo); no reabrir como paper |

## C. Bloqueadas por datos, sujetos humanos o ejecuciones de modelos

Para cada una se deja un esqueleto de pre-registro mínimo, como propuesta para discutir, no como diseño validado.

### CTG001 — Clarificación de estimandos con modelos de lenguaje
- Bloqueo: requiere ejecutar modelos de lenguaje (no hay API en este entorno) y el conjunto de 360 corridas original.
- Esqueleto: unidad = tarea estadística ambigua; brazos = pedir aclaración con lista de verificación / pedir o actuar genérico / actuar; desenlace primario = estimando correcto y ejecución correcta (dos indicadores separados, como ya distingue la ficha); criterio predefinido = diferencia de proporciones con IC 95% que excluya 0 en una muestra calculada a priori; registrar el prompt y la versión del modelo.

### SQA001 — Verificación semántica de afirmaciones cuantitativas
- Bloqueo: el conjunto confirmatorio reservado sigue sin abrirse y no está en el repositorio.
- Esqueleto: abrir el conjunto solo tras fijar por escrito la regla de decisión (qué cuenta como "afirmación sostenida por su evidencia"), el estadístico y el umbral; reportar tasa de acuerdo con anotación humana e IC; comparar con al menos un método de verificación existente con el mismo protocolo.

### HDP001 — Predicción de abandono en educación superior
- Bloqueo: sin población, desenlace ni datos admisibles definidos; requiere gobernanza de datos institucional.
- Esqueleto: población = cohortes de ingreso de una unidad académica; desenlace = no matrícula en dos ciclos consecutivos (definir censura); predictores admisibles = solo los disponibles al cierre del primer ciclo; validación temporal (cohortes posteriores); métricas = AUC y calibración por subgrupo; criterio de utilidad = mejora sobre una regla simple (promedio ponderado del primer ciclo) con IC; revisión ética previa.

### GHT001 — Diálogos con IA generativa en educación superior
- Bloqueo: definiciones de constructo y condiciones de uso de datos pendientes; requiere consentimiento.
- Esqueleto: definir "uso de IA" por tipo de acto (consulta, redacción, verificación), medir por registros con consentimiento, no por autorreporte; diseño longitudinal por curso con al menos dos mediciones; preinscribir las hipótesis sobre relación con actividades de aprendizaje; plan de anonimización.

### MIM001 — Imaginación moral en comunidades de videojuegos
- Bloqueo: esquema de codificación no validado; sin controles comparables.
- Esqueleto: corpus multilingüe con muestreo estratificado por plataforma y franquicia; libro de códigos con doble codificación y kappa mínimo predefinido (por ejemplo 0.70); controles = hilos no morales de las mismas comunidades para separar nostalgia y evaluación emocional; análisis preinscrito.

### TQC001 — Medición de la calidad docente
- Bloqueo: constructos, instrumentos y gobernanza de datos por definir.
- Esqueleto: separar tres dimensiones (planificación, interacción en aula, resultados de aprendizaje ajustados); instrumentos existentes validados en español cuando los haya; diseño multinivel (estudiante en curso en docente); no usar encuestas de satisfacción como único indicador; acuerdo institucional sobre uso de datos antes de recolectar.

## D. Archivadas (cerradas por decisión previa; no se reabren)

| Código | Línea | Motivo del cierre según la ficha |
|---|---|---|
| EDC001 | Robustez del desacoplamiento emisiones–crecimiento | La evaluación no sostuvo la afirmación central |
| NLOC001 | Modelos log-odds anidados | Cota que impedía alcanzar el criterio de avance (23 de 36 resultados) |
| CTS001 | Acarreos y sincronización aritmética | Reducción a identidades conocidas |
| HRM001 | Representaciones armónicas y riemannianas | Sin contribución principal independiente |

## E. Otras líneas en pausa sin acción en esta sesión

| Código | Línea | Motivo |
|---|---|---|
| OIF001 | Orden de observaciones e inferencia | La ficha ya identifica solapamiento con pruebas establecidas; un avance requeriría una hipótesis nueva concreta, no más simulación |
| ORS001 | Sensibilidad al orden en evaluación de algoritmos | Igual que OIF001; el incremento independiente no está definido |
| IHA001 | Identificabilidad en búsqueda de arquitecturas | Requiere fijar la clase de arquitecturas y el modelo observacional; sin eso cualquier "certificado" sería trivial o inverificable |
| RRS001 | Covarianza digital en multiplicadores racionales | La ficha declara fórmulas exactas ya verificadas y antecedentes conocidos; sin las notas originales no puede identificarse la parte nueva |
