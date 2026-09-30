# TCD001 — Continuidad interna, 30/09/2026

Documento de trabajo interno. No incorporar al manuscrito ni a entregas institucionales.

## Proyecto y alcance
Línea TCD001, "Fragilidad de la selección de variables con Lasso" / "Fragility of Lasso variable selection", área Estadística y medición, estado en el CV web: "En pausa". Ficha pública: "Estudio de cómo cambia el conjunto de variables seleccionadas al eliminar observaciones. Objetivo: caracterizar testigos combinatorios de cambio y evaluar su costo computacional. Hallazgos: se identifican cambios no monótonos y conexiones con problemas combinatorios conocidos. Alcance: la novedad, la ventaja computacional y algunos certificados no quedaron suficientemente establecidos para continuar la candidatura."

Pedido de la sesión (coordinador, Claude Code, 30/09/2026): dar a la línea un núcleo preciso y verificable, siguiendo el brief común y el ejemplo MRT001; cómputo ≤ ~10 min de CPU; sin git.

## Supuestos (qué hubo que reconstruir de la ficha)
1. **No existe manuscrito previo.** Todo el contenido se redactó desde cero a partir de la ficha. Si el autor conserva notas o código de la línea (en particular los "testigos combinatorios" y la "conexión con problemas combinatorios conocidos" mencionados en la ficha), hay que cotejarlos: es posible que la reducción y los ejemplos originales fueran otros.
2. **Definición del objeto.** Se fijó: Lasso en forma suma (½‖y − Xβ‖² + μ‖β‖₁, sin intercepto, columnas tal cual), soporte = variables con coeficiente no nulo, soporte con signos (S, s). Se definieron dos reglas para la penalización en submuestras: constante (C, μ fijo) y proporcional (P, `alpha` de scikit-learn fijo). La teoría principal está enunciada para ambas reglas en la Prop. 3.2 y solo para la regla C en el Cor. 3.3 y la Prop. 3.5; los experimentos usan la regla C por defecto y reportan la P donde se indica. Esta elección es una decisión, no viene de la ficha.
3. **Objetivos de cambio.** Tres: "cualquier cambio" (con y sin signos), "sale la variable seleccionada más débil" (menor |β̂_j|) y "entra la variable inactiva más fuerte" (mayor |c_j|). Un testigo es un subconjunto propio R con solución única en D∖R; el número de fragilidad es el mínimo |R| (∞ si no hay testigo).
4. **"No monotonía".** Se interpretó como: la familia de testigos no es cerrada por superconjuntos (una variable sale al quitar R y vuelve al quitar R' ⊃ R). Es la lectura más natural de la ficha, pero es una interpretación.
5. **"Conexión con problemas combinatorios conocidos".** Se materializó como una reducción directa desde Subset Sum para p = 1 (existencia de testigo de deselección). No se sabe si la conexión que tenía en mente la ficha era esta u otra (p. ej. sistemas máximos factibles de Amaldi–Kann).

## Qué se produjo (todo en `papers/TCD001-lasso-selection-fragility/`)
1. Manuscrito LaTeX (`manuscript/main.tex`, inglés, 14–15 páginas) con 22 referencias reales, compilado sin errores ni referencias indefinidas.
2. Biblioteca `experiments/lasso_fragility.py` y cuatro scripts de experimentos con semillas fijas (20260930 para E0–E3/E5, 20260931 para E4), salida JSON + Markdown, `make_numbers.py` (422 macros) y `make_figures.py`. Ningún número del manuscrito está escrito a mano.
3. README, esta nota y una propuesta de ficha.

## Resultados principales y su estado
- **Prop. 3.2 (test exacto de eliminación) — demostrada.** Si (S, s) es el soporte con signos en D y X_S tiene rango completo, para cualquier R con I − H_R no singular el candidato sobre D∖R es β̃_S = β̂_S − V_R^T (I − H_R)^{-1} r_R (+ δ·A'^{-1}s si la penalización cambia) y las correlaciones inactivas tienen fórmula análoga; (S, s) se conserva sii el candidato cumple KKT. Verificado contra reajustes: 2760/2760 eliminaciones individuales y 7200/7200 múltiples, ambas reglas, coeficientes a 10⁻¹⁵. Costo 1.4 μs por subconjunto (vectorizado) frente a 569 μs por reajuste.
- **Cor. 3.3 (una eliminación) — demostrado.** Fórmula DFBETA con el residuo del Lasso; índice de inestabilidad ι_i; certificado O(np) de f ≥ 2. La condición suficiente cubre el 58% de las eliminaciones individuales realmente estables.
- **Prop. 3.5 (certificado para k eliminaciones) — demostrada, holgada.** Requiere T_k(h) < 1; certifica k* ≥ 1 solo en el 30% de las instancias de la familia A con f ≥ 2 (n ≤ 14), brecha media 1.2; a n = 400 la horquilla [k*+1, greedy] tiene razón media 0.57 (A).
- **Ejemplos de no monotonía.** p = 1: x = (1,1,1), y = (2,−2,2), μ = 3/2, R = {1}, R' = {1,2}, ambas reglas (demostrado a mano). p = 2: X = [[2,−1],[0,2],[1,1],[2,−2],[−1,1]], y = (2,−2,3,−1,0), μ = 7/2, R = {3,4}, R' = {2,3,4}: la variable 1 sale por competencia con la 2 (su correlación marginal en D∖R es 4 > 7/2 pero la residual es 11/4 < 7/2) y vuelve en D∖R'. Los 26 subconjuntos propios se verifican en aritmética racional exacta; 3 pares no monótonos.
- **Teorema 5.1 — demostrado.** (a) Existencia de testigo de deselección NP-completa para p = 1 (reducción desde Subset Sum con x_i = 1, y = (b_1,…,b_m, −t), μ = 1/2; funciona con ambas reglas). (b) Testigo mínimo de selección para p = 1 en O(n log n). Observaciones: dureza débil (DP pseudo-polinomial); para p ≥ 2 solo se hereda la dureza de "sale"/"cualquiera" y no hay nada para "entra" (Conjetura 5.3).
- **Observación 3.6 (stability selection) — demostrada, trivial.** f_leave(j) > ⌈n/2⌉ ⇒ frecuencia de selección 1 bajo la regla P; el recíproco no se sigue de las definiciones por la no monotonía. No se buscó un contraejemplo explícito del recíproco.
- **Experimentos (verificados, solo en dos familias sintéticas).** Ver README para las cifras. Lo esencial: a n ≤ 14 el soporte cambia con una sola eliminación en el 92% (familia ruidosa) y el 52% (familia con señal fuerte) de las instancias; los testigos mínimos son mayoritariamente eventos simples; 0 de 18 combinaciones heurística×objetivo×familia cumplen el criterio predefinido de ventaja computacional (el greedy de un paso cumple la parte de exactitud para "cualquiera" y "sale", pero nunca la de costo, porque la búsqueda exhaustiva con el test cerrado es barata a estos tamaños; a n = 34 el costo baja a 0.067 pero la exactitud a 89%); pares no monótonos en el 51–72% de las instancias.

## Decisiones tomadas
- Solver: `lars_path` (homotopía, exacta salvo redondeo) como referencia; descenso por coordenadas solo como control cruzado (0 desacuerdos de soporte en 104 reajustes). Umbral de cero 10⁻¹⁰ sobre los ceros exactos de LARS.
- Casos frontera (igualdades KKT): probabilidad cero en diseños continuos; se cuentan como desacuerdo si aparecen (no apareció ninguno). En datos enteros son reales: la búsqueda del ejemplo 2 exige que los 26 subconjuntos sean verificables en exacto sin empates.
- Rango deficiente en D∖R (det(I − H_R) ≤ 10⁻¹²): se trata como cambio, porque por el Lema 2.4 ningún minimizador único puede tener soporte S en ese caso.
- Búsquedas exhaustivas: por tamaño creciente, con tope |R| ≤ 5 en los objetivos dirigidos (n ≤ 14), |R| ≤ n − 2 para "cualquiera" (n ≤ 14) y |R| ≤ 6 en E4. Un tope alcanzado se reporta como "no encontrado", nunca como valor. Se guardan hasta 50 testigos mínimos por instancia.
- Heurísticas: el greedy de un paso puntúa con el margen objetivo predicho por la fórmula exacta de eliminación individual sobre el ajuste actual (una primera versión priorizaba cualquier ruptura del patrón aunque no fuera la buscada; se corrigió antes de la corrida de referencia y se volvió a correr E2/E3/E5 completo). La heurística "AMIP" usa el efecto exacto de una eliminación como puntaje (no la función de influencia) y reajusta a lo largo del orden fijo desde k = 1; su predicción lineal k_pred se reporta aparte.
- Criterio de "ventaja computacional" fijado antes de correr: exactitud ≥ 90% y costo mediano ≤ 10% del exhaustivo.
- Familias: A (p=4, s0=2, b=4, ρ=0, c=1.5) y B (p=8, s0=2, b=2, ρ=0.5, c=1.0), elegidas tras un barrido previo (no incluido) que mostró que con c ≤ 1 y n ≤ 14 casi todas las instancias tienen f = 1; A es la más estable que se encontró sin que el soporte sea siempre el verdadero.
- Idioma: manuscrito en inglés; README y nota en español.

## Limitaciones y lo que NO se afirma
- No se afirma novedad de la fórmula cerrada (es Woodbury + KKT, en la tradición de Cook/Belsley y de la unicidad de Tibshirani 2013) ni de la reducción (dos líneas desde Subset Sum). Es plausible que ambas existan en la literatura de auditoría de OLS (Moitra–Rohatgi; Freund–Hopkins) o en notas no publicadas.
- La dureza es débil y solo para p = 1; no dice nada sobre instancias típicas, en las que la búsqueda exhaustiva fue rápida.
- El certificado de la Prop. 3.5 es holgado; no se afirma ninguna tasa de f/n con n (la caída observada de g/n es empírica y de estas familias).
- Los porcentajes de los experimentos son específicos de dos familias gaussianas sintéticas, un solver y un tope de búsqueda; no se afirma nada sobre datos reales ni sobre poblaciones.
- Los cocientes de costo dependen de la implementación (test vectorizado en NumPy frente a un bucle Python de reajustes).
- Bibliografía: dos entradas arXiv (Moitra–Rohatgi 2205.14284; Freund–Hopkins 2307.16315) y la de Kuschnig–Zens–Crespo Cuaresma (2021, sin número arXiv) se citan de memoria; verificar números, títulos definitivos y sedes de publicación antes de cualquier envío. El título de Broderick–Giordano–Meager cambió entre versiones del arXiv; se usó el de las versiones posteriores con el número 2011.14999.

## Pendientes y próximos pasos concretos
1. Confirmar con el autor que la interpretación de la ficha (testigos, no monotonía, reducción) coincide con la idea original; integrar notas previas si existen.
2. Conjetura 5.3: NP-completitud del testigo de selección para p ≥ 2; y dureza fuerte de "sale" con p fijo ≥ 2 (la reducción actual solo da dureza débil).
3. Apretar la Prop. 3.5 (estructura de signos del término de interacción; relajación SDP pequeña) y medir la brecha con f en E4.
4. Reglas dependientes de los datos (μ por validación cruzada): el testigo debe incluir el cambio de μ.
5. Extender el test exacto a elastic net y square-root Lasso (KKT lineales sobre soporte con signos fijo).
6. Buscar un contraejemplo explícito del recíproco de la Observación 3.6 (frecuencia de stability selection 1 con f_leave ≤ ⌈n/2⌉).
7. Decidir destino (arXiv stat.ME / math.OC) y recortar a 10 páginas si se exige.
8. Actualizar la ficha TCD001 del CV web según `FICHA_TCD001_propuesta.md`.
