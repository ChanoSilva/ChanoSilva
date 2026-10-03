# Informe de árbitro interno — TCD001 (ronda 1, 30/09/2026)

Objeto: `manuscript/main.tex` (v0.1, 15 pp.), `experiments/*.py`, `results/*`, `README.md`, `CONTINUIDAD_TCD001_20260930.md`, `FICHA_TCD001_propuesta.md`. Numeración de resultados según el PDF compilado (Lema 2.4; Prop. 3.1; Cor. 3.2; Obs. 3.3; Prop. 3.4; Obs. 3.5; Prop. 4.1; Ej. 4.2 y 4.3; Teo. 5.1; Obs. 5.2; Conj. 5.3). Archivos de trabajo del árbitro: `scratchpad/referee_TCD001/` (notas, réplicas, compilación).

## Veredicto

**Cambios mayores.** Ningún resultado numérico queda invalidado y las demostraciones centrales (Prop. 3.1 bajo ambas reglas, Prop. 3.4, Teo. 5.1, Ejemplos 4.2–4.3) son correctas; pero el Cor. 3.2 afirma algo falso tal como está escrito, el paso "el test falla ⇒ R es testigo" omite la hipótesis de unicidad que exige la Def. 2.2, un archivo de resultados no corresponde al script que lo genera, hay decisiones tomadas tras ver resultados que el manuscrito no declara, la introducción y la ficha "cierran" más de lo que el cuerpo establece, y el texto tiene 15 páginas frente a las ≤ 10 del objetivo.

## Hallazgos bloqueantes

**B1. Cor. 3.2 enuncia `h_i < 1` como hecho incondicional; es falso y la prueba no lo demuestra.**
Ubicación: `main.tex:157` ("Under the constant rule, for R={i} one has h_i<1, e_i=r_i/(1−h_i)") y prueba en `main.tex:168` ("I−H_R is nonsingular because h_i<1 when X_{S,−i} has full column rank").
Problema: `h_i = 1` ocurre exactamente cuando quitar la observación i deja `X_{S,−i}` sin rango completo. Contraejemplo: n = p = 2, X = I₂, y = (3,3)ᵀ, μ = 1. Las columnas están en posición general, el minimizador es único, β̂ = (2,2)ᵀ, S = {1,2}, A = I, y h₁ = h₂ = 1; `e_i` no está definido. La prueba es condicional ("when X_{S,−i} has full column rank") mientras el enunciado es incondicional.
Corrección: reescribir el enunciado como "Under the constant rule, for R={i} with h_i<1 (equivalently, X_{S,−i} of full column rank; h_i=1 is the rank-deficient case of Proposition 3.1(a), in which (S,s) is not preserved), put e_i=r_i/(1−h_i). Then …". En la cláusula del índice: "with ι_i := +∞ when h_i = 1". El código ya se comporta así (`e = r/(1−h)` da `inf`, `single_removal_indices`, `lasso_fragility.py:217`).

## Hallazgos mayores

**M1. El test exacto decide "(S,s) se conserva", no "R es testigo"; falta la unicidad en D∖R que exige la Def. 2.2.**
Ubicación: Def. 2.2 (`main.tex:93`: el testigo requiere "a unique minimiser" en D∖R); Prop. 3.1 (`main.tex:118–130`); Sec. 6 Protocolo (`main.tex:261`: "decide the signed target with Proposition 3.1"); Apéndice "Exact test" (`main.tex:421`: det ≤ 10⁻¹² "treated as … a change"); código `fragility_exact`, `lasso_fragility.py:323–326` (para `any_signed` todo conjunto no conservado se registra como testigo sin reajuste).
Problema: si el test falla, la Prop. 3.1 solo garantiza que (S,s) no es el soporte con signos de ningún minimizador en D∖R; R es testigo de ANY solo si además el minimizador en D∖R es único. Lo mismo para el caso (a) (I−H_R singular). En los diseños gaussianos la unicidad en D∖R vale casi seguramente (columnas en posición general, Tibshirani 2013, Lema 4), pero el texto no lo dice, y en datos enteros (Ej. 4.3) no vale en general.
Corrección: añadir tras la Prop. 3.1 (o en el Protocolo): "For the signed ANY target, failure of the test identifies a witness provided the minimiser on D∖R is unique; for designs with a continuous distribution this holds for every R with probability one (general position), which is how the exhaustive searches of Section 6 use the test. For integer data (Example 4.3) uniqueness is certified separately in exact arithmetic." Añadir la misma salvedad al apartado "Limitations".

**M2. Sobreafirmación de cierre en introducción y ficha; omisión de dos salvedades que el propio cuerpo contiene.**
Ubicación: `main.tex:62` ("settles, in the negative where that is the honest answer, the three points that were left open"); `FICHA_TCD001_propuesta.md`, "Principales hallazgos" (español e inglés): "En diseños sintéticos con n ≤ 14 el soporte cambia al quitar una sola observación en el 52–92% de las instancias; tres heurísticas … no alcanzan el criterio de ventaja computacional fijado de antemano"; resumen (`main.tex:55`: "no heuristic is cheaper than one tenth of the exhaustive search").
Problema: (i) la novedad no se "cierra", se declina ("no novelty is claimed"); la ventaja computacional solo se cierra en negativo a n ≤ 14, donde el criterio de coste (≤ 10 %) es inalcanzable por construcción: una heurística necesita al menos un reajuste (569 μs medidos) y la búsqueda exhaustiva de ANY tarda 2 ms de media en la familia A (`results/fragility.json`, `t_any_C`), de modo que ninguna heurística basada en reajustes puede bajar de ≈ 0.3; el propio E4 muestra coste 0.07 con exactitud 89 % a n = 34. (ii) Las familias A y B se eligieron tras un barrido previo no incluido que miró precisamente la fragilidad (CONTINUIDAD, "Decisiones tomadas": "A es la más estable que se encontró sin que el soporte sea siempre el verdadero"); el 52 %/92 % no describe nada fuera de esa elección.
Corrección: en `main.tex:62` sustituir por "gives the line a precise core: it proves what can be proved, reports which certificates are loose, and shows that on small synthetic instances the predefined advantage criterion is not met because exhaustive search with the closed-form test is already cheap; novelty is not claimed." En la ficha: "En dos familias sintéticas elegidas tras un barrido piloto, con n ≤ 14, el soporte cambia al quitar una sola observación en el 52 % y 92 % de las instancias; tres heurísticas no cumplen el criterio de ventaja computacional fijado de antemano, en parte porque a esos tamaños la búsqueda exhaustiva con el test cerrado es ya barata (a n = 34 el greedy cuesta el 7 % con 89 % de exactitud)." En el resumen añadir "at n ≤ 14" tras "one tenth of the exhaustive search".

**M3. Decisiones tomadas tras ver resultados que el manuscrito no declara; corrida de referencia producida con dos versiones de la biblioteca.**
Evidencia (mtimes UTC, sin git): `run_fragility.py` 08:40:11 (contiene `CRIT_EXACT=0.90`, `CRIT_COST=0.10`, líneas 31–33); `examples.json` 08:43:11; `validation.json` 08:43:25; `scaling.json` 08:45:34; **`lasso_fragility.py` 08:51:01**; `fragility.json` 08:51:58; **`exact_examples.py` 09:00:28**. CONTINUIDAD ("Decisiones tomadas") confirma: el greedy de un paso se modificó tras una primera corrida completa de E2/E3/E5 y solo se repitieron E2/E3/E5; las familias se eligieron tras un barrido no incluido.
Qué se sostiene: las constantes del criterio preceden a todos los resultados almacenados y quedan registradas en `fragility.json: meta.criterion`; no hay indicio de que el umbral se moviera. Repliqué instancia a instancia 120 instancias de E4 (familia A, n ∈ {10,14,18}, semilla 20260931) con la biblioteca actual: 0 discrepancias en f_C, f_P, g_onestep, g_sorted, k_pred y k* frente a `scaling.json`; es decir, el cambio de las 08:51 no altera E4 (el objetivo `any_signed` no usa la rama modificada). E1 no se replicó instancia a instancia (su modo rápido es coherente).
Problema: el manuscrito dice "Two families are fixed" y "criterion fixed before the runs" sin mencionar el barrido piloto ni la modificación de una heurística evaluada después de una corrida completa; y `results/` mezcla salidas de dos versiones del código.
Corrección: (a) añadir en Sec. 6 un párrafo "Pre-specification and changes": criterio fijado en el código antes de toda corrida; familias elegidas tras un barrido piloto (describirlo en una frase: rango de c, n ≤ 14, casi todas f = 1 con c ≤ 1); el greedy de un paso se corrigió tras una primera corrida (describir el cambio: puntuación por el margen del objetivo en vez de cualquier ruptura) y se repitió E2/E3/E5; (b) regenerar los cuatro JSON con la biblioteca final en una sola corrida (`exact_examples`, `run_validation`, `run_fragility`, `run_scaling`, `make_numbers`, `build.sh`) para que `results/` sea consistente.

**M4. `results/examples.json` no corresponde al script actual: falta el Ejemplo 1b (ENTER) que el manuscrito dice verificado por el script.**
Ubicación: `main.tex:204` ("Both examples are also checked in exact arithmetic by the script of Appendix A"); `exact_examples.py:134–145` (bloque `example1b`); `results/examples.json` (claves: `seed, example1, example2, seconds`; no hay `example1b`); `results/log_exact_examples.txt` (sin la línea "Example 1b").
Evidencia: al ejecutar el script actual (1.8 s, copia en scratchpad) se imprime "Example 1b (enter) verified exactly under both rules" y el Ejemplo 2 reaparece idéntico (11 ensayos, misma instancia, 26 subconjuntos, 3 pares).
Corrección: volver a correr `exact_examples.py` y regenerar `examples.json/.md` y el log (incluido en M3b); opcionalmente exponer una macro `\ExOnebOk` y citarla.

**M5. E3: las fracciones de exactitud son estimaciones puntuales a 1–2 errores típicos del umbral, y la contabilidad de tiempos es asimétrica.**
Ubicación: `main.tex:302` ("It thus meets the accuracy part … but not for ENTER"); Tabla 4; `lasso_fragility.py:391–393` y `308` (cronómetros).
Evidencia: con n = 206/209 instancias, ENTER one-step = 0.859 ± 0.024 (A) y 0.876 ± 0.023 (B) (ET binomial): 1.7 y 1.0 ET por debajo de 0.90. El cronómetro de la búsqueda exhaustiva empieza después de `fit_state` (precomputación O(nps₀)) y del ajuste inicial; el de las heurísticas incluye su ajuste inicial (`n_refit = 1`), que es ≈ 0.57 ms de los 2.26 ms medios del greedy en A (media de 2.79 reajustes por instancia).
Problema: la frase "not for ENTER" se presenta como hecho; el cociente de coste está sesgado contra las heurísticas en ≈ 25 % a n ≤ 14. La conclusión (0/18) sobrevive a ambas correcciones (ni restando el ajuste inicial se baja de 0.10).
Corrección: añadir a `main.tex:302`: "these are point estimates on 206–240 instances with standard errors of 1–2.5 points; the ENTER shortfall (86 %/88 % against 90 %) is within two standard errors of the threshold"; y al Protocolo: "exhaustive-search times exclude the O(nps₀) precomputation and the initial fit, which the heuristic times include (≈ 0.6 ms); this does not change any verdict". Añadir a la Tabla 4 una columna con el ET o con el intervalo de Wilson.

**M6. La Tabla 8 (`[H]`) desborda la página 12: pisa el folio y trunca la leyenda.**
Evidencia: compilación en scratchpad: `Overfull \vbox (83.88197pt too high) has occurred while \output is active` en la p. 12; en el PDF la leyenda termina en "…of Appendix A with the" y el número de página aparece dentro de la tabla (`scratchpad/referee_TCD001/p-12.png`).
Corrección: quitar `[H]` (usar `[t]` o `[p]`) o, mejor, suprimir la tabla (véase "Recortes") y conservar solo la frase de alcance.

**M7. Obs. 3.5 atribuye a Meinshausen–Bühlmann la regla P.**
Ubicación: `main.tex:194` ("refits on subsamples … with the same per-observation penalty (rule P)").
Problema: en Meinshausen–Bühlmann (2010) el Lasso se escribe, a mi entender, en forma suma ‖Y−Xβ‖² + λ‖β‖₁ y las submuestras de tamaño ⌊n/2⌋ usan "el mismo λ", lo que en la notación del manuscrito es la regla C, no la P; la regla P corresponde a implementaciones con factor 1/n (p. ej. glmnet). No pude verificar la fórmula en red (dominios bloqueados); verificar con el PDF del artículo.
Corrección: "Stability selection refits on subsamples of size ⌊n/2⌋ with a fixed penalty; whether this is rule C or rule P depends on the parametrisation (sum form in the original paper, per-observation form in common software). Under whichever rule is used, f_leave(j) > ⌈n/2⌉ implies Π_j = 1."

## Hallazgos menores

**m1.** Numeración desfasada: README, CONTINUIDAD y los docstrings del código hablan de "Prop. 3.2 / Cor. 3.3 / Prop. 3.5 / Obs. 3.6" y "Proposition 1 / Corollary 2 / Proposition 3"; el PDF tiene Prop. 3.1 / Cor. 3.2 / Prop. 3.4 / Obs. 3.5. Unificar (o usar etiquetas simbólicas en README).

**m2.** Prop. 3.4, coste "O(nps₀ + n log n)" (`main.tex:181`): calcular T_k para los p vectores exige ordenar p+1 vectores: O(nps₀ + p n log n) (o O(np) con selección). Corregir.

**m3.** Teo. 5.1(a), "(equivalently f_ANY, since for p=1 every change is a deselection)" (`main.tex:241`): cierto solo para ANY sin signos (notación del texto); con signos, p = 1 puede cambiar de signo sin salir (en la propia reducción, R = [m] deja K = {m+1} con suma −t < −½). Escribir "unsigned f_ANY".

**m4.** `main.tex:141` cita la identidad de Woodbury a Sherman–Morrison (1950, caso de rango uno) y Hager (1989). Añadir Woodbury, M. A. (1950), *Inverting modified matrices*, Memorandum Report 42, Statistical Research Group, Princeton, 4 pp., o escribir "Sherman–Morrison–Woodbury identity".

**m5.** `main.tex:60` incluye a Kuschnig–Zens–Crespo Cuaresma entre los "exact or certified algorithms for the sign of a regression coefficient"; ese trabajo propone algoritmos adaptativos (heurísticos) para conjuntos influyentes y el problema de enmascaramiento. Moverlo a la frase sobre AMIP/heurísticas. Entrada bibliográfica: véase tabla.

**m6.** E1 (`main.tex:266`): "15 instances each" pero la parte C (Cor. 3.2 y Prop. 3.4) usa 30 instancias nuevas por celda (`run_validation.py:113`, `reps*2`; Tabla 2, columna "instances" = 30). Decirlo. En la Tabla 2 la celda (12,24) imprime "--%" (`make_numbers.py:119`): imprimir "--".

**m7.** E4 (`main.tex:319`): "(mean f/n ≈ 0.028)" es g/n (cota greedy; macro `EfourAFourhundredMeanOverN` se calcula de `g_onestep_C_mean_over_n`); README repite "f/n ≈ 0.028". Escribir g/n. En la misma frase, "over all family-A instances with n ≥ 22 the median cost ratio is 0.690" se calcula sobre las 113 con f finita (`make_numbers.py`, `rr`); sobre las 120 es 0.56. Precisar "with finite f".

**m8.** E4: la "media de f sobre las instancias dentro del tope" es una media censurada (excluir las no encontradas sesga hacia abajo al crecer n). Llamarla así o usar la mediana (ya en Tabla 5).

**m9.** Resumen de ≈ 450 palabras (una página). Reducir a ≤ 200.

**m10.** Tabla 5, columna "cost ratio" para n ≤ 18: cocientes 4–10 con tiempos exhaustivos de 0.00 s están dominados por la resolución del cronómetro. Indicarlo o suprimir la columna para n ≤ 18.

**m11.** Cor. 3.2: convenciones cuando Sᶜ = ∅ (γ = ∞, término 0: el código lo hace) o γ = 0 (frontera): una frase.

**m12.** Def. 2.2: R = ∅ es subconjunto propio; añadir "nonempty" (f ≥ 1).

**m13.** Lema 2.4 sin etiqueta `\status{}` mientras la Tabla 8 lo marca "literature" y el texto da prueba propia: añadir `\status{classical}`.

**m14.** Tabla 3, leyenda "up to 20 minimal witnesses" y Apéndice "up to 50 collected": decir "20 of the (up to 50) collected".

**m15.** Obs. 3.3 y texto del Cor. 3.2: precisar qué residuo es r: "r = y − X_S β̂_S is the residual of the Lasso fit on D, which differs from the least-squares residual of y on X_S by μ X_S A⁻¹ s; e_i = r_i/(1−h_i) is the leave-one-out residual of the fixed-support Lasso". La afirmación "una eliminación = DFBETA con el residuo Lasso" es correcta solo bajo la regla C (el Cor. lo dice; la ficha y el resumen no).

**m16.** Compilación: `Overfull \hbox` de 4–5 pt en la Tabla 1 (líneas 219–228), en la tabla de la Sec. 7 (386–408) y en la prueba de la Prop. 3.4 (187–189); aviso de fuente `T1/lmr/m/scit` (×10): `\textsc` dentro de `\emph`; usar `\textsc` sin cursiva.

**m17.** Obs. 5.2(i) explica bien "débil"; añadir una frase: "strong NP-hardness (hardness with numbers polynomially bounded in n) is excluded by the pseudo-polynomial DP unless P = NP".

## Verificación matemática (resumen por resultado)

- Lema 2.4: correcto. Prop. 3.1(a)/(b): álgebra verificada paso a paso (Woodbury, identidad y_R + (I−H)⁻¹H y_R = (I−H)⁻¹y_R, bloque R del residuo = e_R, término δ en β̃ y en c̃); la fórmula bajo la regla P es correcta (`removal_test`, `lasso_fragility.py:192–202`, implementa exactamente (3)–(4)) y E1 la contrasta con 3600 reajustes bajo P sin desacuerdos. Salvedad M1.
- Cor. 3.2: B1; el índice ι_i es correcto (desigualdad triangular). Prop. 3.4: correcta (λ_max(H_R) ≤ tr H_R, e_R = r_R + H_R e_R, cotas con T_k); monótona en k; coste m2.
- Ej. 4.2: verificado a mano, ambas reglas, tres objetivos. Ej. 4.3: recalculado a mano (β̂₁ = 3/20, c₂ = −1/10; en D∖{3,4}: β̂₂ = −5/12, c₁ = 11/4 < 7/2 con |x₁ᵀy| = 4 > 7/2; en D∖{2,3,4}: β̂₁ = 1/10, c₂ = −17/10) y reproducido en exacto.
- Teo. 5.1(a): reducción polinomial (n = m+1 enteros de tamaño polinomial), pertenencia a NP justificada (certificado R, suma y comparación), ambas reglas cubiertas (μ_k ∈ (0, ½] y suma entera ⇒ |Σ| ≤ μ_k ⇔ Σ = 0), R propio garantizado por t < Σb_i, unicidad en D∖R trivial para p = 1. "Débil" explicado correctamente (DP en (suma, cardinalidad)). (b) correcto. Salvedad m3.
- Obs. 3.5: implicación correcta bajo la regla que se use; atribución M7.

## Bibliografía

Red: arxiv.org, api.crossref.org y projecteuclid.org bloqueados por el proxy; WebSearch operativo. "Estándar" = datos coinciden con los de uso común, sin verificación directa posible aquí.

| Entrada | Estado | Corrección / nota |
|---|---|---|
| moitra2022 | verificada | arXiv 2205.14284; ICLR 2023. Correcta. |
| freund2023 | verificada | arXiv 2307.16315 (2023). Correcta. Existe continuación "Robustness Auditing for Linear Regression: To Singularity and Beyond" (arXiv 2410.07916, ICLR 2025), pertinente para la Obs. 5.2(iii); comprobar autores antes de citar. |
| broderick2020 | verificada | Título actual y número 2011.14999 correctos; última revisión jul. 2023: añadir "v4 (2023)" o año de la versión usada. |
| kuschnig2021 | corregida | No es "arXiv preprint": CESifo Working Paper No. 8981, Múnich, 2021 (también SSRN 3819102; EconStor 10419/235351). Sustituir `note`. Atribución en el texto: m5. |
| meinshausen2010 | verificada | JRSS-B 72(4), 417–473. Correcta. Forma del Lasso en el artículo: no verificable en red (M7). |
| tibshirani2013 | verificada | EJS 7, 1456–1490 (2013). Correcta. |
| tibshirani1996, efron2004, osborne2000, zhao2006, wainwright2009, cook1977, hampel1974, pedregosa2011, amaldi1995, amaldi1998, sherman1950, hager1989 | no verificables en red; estándar | Volúmenes y páginas coinciden con los habituales. |
| buhlmann2011, belsley1980, garey1979, karp1972 | no verificables en red; estándar | Correctas en apariencia. |
| (falta) Woodbury 1950 | añadir | Ver m4. |

Uso de las citas: cada cita respalda la afirmación para la que se usa salvo kuschnig2021 (m5) y meinshausen2010 en la Obs. 3.5 (M7).

## Verificación computacional

Todo en copias dentro de `scratchpad/referee_TCD001/` (no se tocó `results/`). CPU total ≈ 35 s.

| Qué | Tiempo | Resultado |
|---|---|---|
| `exact_examples.py` (completo) | 1.8 s | Ejemplo 2 idéntico al publicado; aparece Ejemplo 1b, ausente en `examples.json` (M4). |
| `run_validation.py --fast` | 3.8 s | 40/40 acuerdos por celda y regla; coeficientes a ≤ 1.1·10⁻¹⁴; Cor. 3.2 nunca certifica una eliminación inestable (assert); throughput 2.0 μs vs 578 μs por subconjunto (×296; publicado 1.4/569, ×395: misma magnitud, máquina compartida). |
| `run_fragility.py --fast` (5 inst./celda) | 8.8 s | B: P(f=1) = 0.8–1.0; A: media f 1.4–3.0. Coherente con E2. |
| `run_scaling.py --fast` (3 inst./celda) | 18.2 s | A n=400: mediana g = 9, k* = 5 (publicado 10/5). Coherente. |
| Réplica exacta E4 (A, n=10,14,18, 120 inst.) | 1.7 s | 0 discrepancias con `scaling.json` en seis magnitudes (M3). |
| Macros vs JSON (muestreo de >60 macros con Python) | — | Todas coinciden; única imprecisión textual m7. |
| Compilación `latexmk` | — | 15 pp., 0 errores; 1 `Overfull \vbox` 84 pt (M6), 3 `\hbox` 4–5 pt, aviso de fuente (m16). |

Código: no se encontró fuga de información, ajuste con datos de prueba ni semillas mal fijadas; umbrales (10⁻¹⁰ ceros, 10⁻¹² determinante, desigualdades estrictas) declarados; los casos frontera se cuentan como desacuerdo. Observaciones: cronómetros asimétricos (M5); el `fallback` a "any" en el greedy (`lasso_fragility.py:414–418`) es inalcanzable (el objetivo se comprueba tras cada eliminación) y puede eliminarse.

## Recortes propuestos (15 → ≤ 10 páginas)

1. Resumen: de ≈ 450 a ≤ 200 palabras (−0.6 p.).
2. Introducción: suprimir la lista numerada (duplica el resumen); dejar un párrafo de aportes con referencias a secciones (−0.4 p.).
3. Tablas 2 (E1b), 3 (E2), 5 (E4 exacto), 6 (E4b) y 7 (E5) a un apéndice de una página en letra pequeña o a `results/*.md` con una frase de referencia; en el cuerpo quedan la Tabla 1 (Ej. 4.3) y la Tabla 4 (E3) (−2.5 p.).
4. Fusionar las Figuras 1 y 2 en una figura de dos paneles (−0.4 p.).
5. Suprimir la Tabla 8 (repite resumen, introducción y etiquetas `\status`); conservar los párrafos "Limitations" y "Next steps" (−0.8 p.; resuelve M6).
6. Fusionar Obs. 3.3 en el enunciado del Cor. 3.2 (una frase) y Obs. 5.2(iii) en la introducción (−0.3 p.).
7. Apéndice A: dejar solo "Solver" y "Exact test"; el resto está en README (−0.4 p.).
8. E2 y E3: no repetir en el texto los números que ya están en las tablas conservadas (−0.4 p.).

## Alcance

Coherente con la ficha pública (estudio metodológico; sin datos reales; sin aplicaciones). Pendiente solo M2 (redacción de la ficha y de la introducción).

## Lista de acciones (por prioridad)

1. Reescribe el Cor. 3.2 con la hipótesis h_i < 1 y la convención ι_i = ∞ si h_i = 1 (B1).
2. Añade tras la Prop. 3.1 y en "Limitations" la salvedad de unicidad en D∖R y su justificación por posición general (M1).
3. Vuelve a correr los cuatro scripts con la biblioteca final en una sola sesión, regenera `results/`, `numbers.tex`, tablas, figuras y PDF (M3b, M4).
4. Añade en la Sec. 6 el párrafo "Pre-specification and changes" (criterio, barrido piloto de familias, corrección del greedy tras una primera corrida) (M3a).
5. Sustituye `main.tex:62` y los párrafos de "Principales hallazgos" de la ficha por los textos propuestos en M2; añade "at n ≤ 14" en el resumen.
6. Añade a E3 los errores típicos y la nota sobre la contabilidad de tiempos (M5).
7. Elimina la Tabla 8 o quítale `[H]` (M6).
8. Reformula la Obs. 3.5 sin atribuir la regla P a Meinshausen–Bühlmann; comprueba la fórmula del artículo (M7).
9. Corrige la entrada kuschnig2021 (CESifo WP 8981, 2021) y muévela a la frase sobre heurísticas; añade Woodbury 1950 (m4, m5).
10. Escribe "unsigned f_ANY" en el Teo. 5.1(a); corrige el coste de la Prop. 3.4; escribe g/n y "with finite f" en E4; "30 fresh instances" en E1; "nonempty R" en la Def. 2.2 (m2, m3, m6, m7, m12).
11. Unifica la numeración de resultados en README, CONTINUIDAD y docstrings con la del PDF (m1).
12. Aplica los recortes 1–8 hasta ≤ 10 páginas y reduce el resumen a ≤ 200 palabras (m9).
13. Arregla "--%" en la Tabla 2, la columna "cost ratio" para n ≤ 18, las cajas desbordadas y el `\textsc` en cursiva (m6, m10, m16).
