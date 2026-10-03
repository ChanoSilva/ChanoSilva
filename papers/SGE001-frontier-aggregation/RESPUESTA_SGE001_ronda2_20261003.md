# Respuesta del autor al informe de la ronda 2 — SGE001 (03/10/2026)

> Numeración de enunciados: v0.2 = v0.3 (Lema 3.3, Lema 3.4 bisagra, Prop. 3.5, Cor. 3.6, Obs. 3.7, Ej. 3.8, Prop. 3.9, Ej. 3.10); en v0.4–v0.5 se desplazan tres lugares (Lema 3.6 … Ej. 3.13). [Nota añadida en la ronda 3.]

Informe: `REFEREE_SGE001_ronda2_20261003.md` (cambios mayores acotados; 0 bloqueantes, 4 mayores, 13 menores; reproducción bit a bit).
Estado de este documento: **completo** (escrito de forma incremental mientras se aplicaban los cambios; el registro de avance se conserva abajo).

**Resumen.** 17 hallazgos nuevos (0 bloqueantes, 4 mayores, 13 menores): **13 aceptados, 4 aceptados con matiz (M3, m9, m11 y, fuera de la lista, la extensión), 0 rebatidos.** Los cuatro puntos de la ronda 1 que el árbitro marcó como aplicados a medias o con error nuevo (B2, M1, m5, m12) quedan corregidos a través de M1, M3, m12 y m2. Ningún valor puntual de E0–E6 cambió (comparación hoja a hoja con v0.2); cambian E1c (rediseñado), los intervalos bootstrap de E2 y E3 (m13) y los números nuevos que se añaden (certificados, fracciones certificadas, distribución de la razón desplazada, errores estándar). Manuscrito v0.3 (3 October 2026): 11 páginas (10 de cuerpo y apéndice + 1 de bibliografía; v0.2: 12), 0 errores, 0 referencias/citas indefinidas, 0 cajas desbordadas, 0 "??".

## Plan de trabajo

1. M1 (certificados): separar certificado con microdatos (por segmento) y certificado con momentos + rango; añadir certificado de C1 (6B₂ < |Q₂|) y fracciones certificadas de E4 con cada cota; macros.
2. M2 (C1 vs C2 en resumen y ficha).
3. M3 (E1c con 60 réplicas, errores estándar, N = 200000 si cabe).
4. M4 (razón desplazada: distribución por réplica).
5. Menores m1–m13 y recortes hasta ≤ 10 páginas.

## Respuesta punto por punto

### Mayores

**M1 (certificado "desde los momentos" calculado con la cota por segmento; comparación con el umbral de C1). Aceptar.** El árbitro tiene razón en las dos partes: el $B_2$ por segmento necesita cada $x_i$, y el certificado $2B_2<|Q_2|$ certifica razón > 1, no la razón ≥ 5 de C1. Cambios:
- Prop. 3.1(e) reescrita como "(Certificates; under the hypothesis of (c).)": forma graduada $(k+1)B_2<|Q_2|\Rightarrow|E_1|>k|E_2|$ (prueba en el enunciado: $|E_1|\ge|Q_2|-B_2>kB_2\ge k|E_2|$); $k=1$ certifica la mejora, $k=5$ la de C1. Se nombran sin ambigüedad los dos certificados: **moment-and-range certificate** (forma de momentos $B_2\le\frac N6M_3m_3$ con $M_3$ sobre una región conocida que contiene la población, p. ej. la caja del rango coordenado; usa $\bar x$, $\Sigma$, $m_3$ y esa región) y **micro-data certificate** (cota por segmento; necesita los $x_i$ pero no $f$ en las unidades; se dice que es un diagnóstico, porque quien tiene los $x_i$ y $f$ calcula $Y$).
- Código (`run_E1`): `cert_box_*` ($2B_2^{\rm box}<|Q_2|$), `cert_c1_*` ($6B_2<|Q_2|$), `cert_c1_box_*` y la mayor σ con razón observada > 1 en todas las réplicas (`sigma_largest_r21_gt1_uniform`), todas uniformes desde la σ más pequeña; comentario de la l. 348 corregido. `run_E4`: fracción certificada y reversiones con la cota de momentos + rango.
- Resultados recalculados (mismos sorteos que v0.2), LN / SU: moment-and-range $k=1$: **σ ≤ 0.042 / 0.053**; micro-data $k=1$: 0.056 / 0.071 (sin cambio); $k=5$ (C1): **0.018 / 0.023** con ambas cotas; razón observada > 1 en todas las réplicas hasta **σ = 0.75** (LN, ambas fronteras; todo el barrido SU). Matiz numérico: el árbitro da 0.054 para SU; el valor de malla es 0.05347, que con tres decimales es 0.053 (mismo punto de malla). E4, fracción certificada (segmento / momentos + rango): 100/100 (σ = 0.02), 99.7/99.6 (0.05), 97.0/94.4 (0.1), **70.9/6.5 (0.2)**, 0/0 (0.4); 0 reversiones certificadas con ambas (las certificadas con la cota de caja son un subconjunto de las otras, porque $B_2^{\rm box}\ge B_2$).
- Texto: resumen ("certifiable from the input moments, their range and a derivative bound … σ ≤ 0.042 … against an observed improvement up to σ = 0.75 and a fivefold one up to σ = 0.42"); l. 198 (comparaciones: forma de momentos frente a forma por segmento); E1 (párrafo "Bounds and certificates" con las tres cifras y la comparación correcta 0.75 / 0.42); E4 (ambas fracciones; "the one available without the micro data"); conclusión; Tabla 6 (claims); próximos pasos (a); apéndice (definición de ambas formas). Macros nuevas: `\EoneCertBoxSigma*`, `\EoneCertConeSigma*`, `\EoneCertConeBoxSigma*`, `\EoneRatioGtOneSigma*`, `\EfourCertBoxFrac*`. Ficha ES/EN y README: "desde los momentos y el rango de los insumos", σ ≈ 0.04 (≈ 0.06 con microdatos) frente a 0.75 y 0.42.

**M2 (C1 y C2 fundidos en resumen y ficha). Aceptar.** Resumen: "Two criteria were fixed in advance. A uniform fivefold error reduction (C1) holds for symmetric inputs and fails for log-normal inputs beyond σ = 0.42 and at crossings; a scalar recalibration … does not restore it. A fivefold reduction of rank reversals in a decision experiment (C2) fails clearly in 14 of its 20 eligible capacity cells, with 1 capacity cell and 1 cell without capacity borderline at 1000 trials." (todas las cifras por macro, incluidas las nuevas `\EfourBorderlineCapped`, `\EfourBorderlineSmooth`, `\EfourCappedCells` = 30). Ficha ES/EN con el texto propuesto ("20 celdas elegibles con capacidad, de 30; una celda con capacidad y una sin capacidad son limítrofes"); se retiró la frase contradictoria "las 3 sin capacidad pasan". Tabla de afirmaciones y párrafo de C2 de E4 ("20 of the 30 with it") con la misma separación; la conclusión dice ahora "neither predefined criterion was met".

**M3 (E1c demasiado pequeño; 3.12–3.18 como "predichos"). Aceptar con matiz.** `run_E1c` usa ahora **60 réplicas para cada N ∈ {200, 2000, 20000, 200000}** (en bloques de 6 réplicas por memoria; coste ≈ 19 s de CPU, dentro del presupuesto, por eso no hizo falta bajar a 40/10 como proponía el informe), error estándar bootstrap (500 remuestreos, generador propio) y mediana de $|E_2-E_3|/Y$ en σ = 0.01. Resultados (semilla de la corrida de referencia): pendiente de $|e_2|$ = **3.16 (0.09), 3.50 (0.10), 4.05 (0.10), 3.96 (0.02)**; de $|e_3|$ = 4.00 en todos (s.e. ≤ 0.006); término de tercer momento 8.0, 2.3, 2.3, 2.6 ×10⁻⁹. El matiz: con otra semilla el árbitro obtuvo 2.96 (0.08), 3.54 (0.09), 3.97 (0.09), 4.02 (0.03); las diferencias (0.20, 0.04, 0.08, 0.06) están en 0.3–1.7 errores estándar combinados, y el patrón (≈ 3 a N pequeño, ≈ 4 a N grande, término de tercer momento que baja con N sobre un piso) es el mismo; el texto usa las cifras de nuestra corrida, por macro. El 4.05 en N = 20000 queda a 0.5 s.e. de 4, de modo que el "4.2 > 4" de v0.2 era ruido de 6 réplicas. Resumen: se quitaron 3.12–3.18 de los exponentes predichos; ahora "on log-normal inputs the second-order exponent lies between 3 and 4 and moves towards 4 as N grows (3.16 at N = 200, 3.96 at N = 200000), a finite-N effect of the sample third moment". E1, tabla de afirmaciones, README y nota actualizados; `tables.md` lista E1c con errores estándar.

**M4 (el "1.000" de la razón desplazada es un artefacto de mediana). Aceptar.** Verificado con los sorteos de la referencia: en LN, σ = 0.01, la razón $T_u/(\sigma\tau_z(b))$ está en [0.99701, 1.00291] réplica a réplica, $P_u<Q_u$ en exactamente el 50 % de las réplicas, desviación mediana |·−1| = 0.0028 frente a 0.0027 en SU; la mediana 0.9999997 cae entre dos grupos. `run_E2` guarda ahora mínimo, máximo, mediana de |razón − 1| (desplazada y sin desplazar) y la fracción con $P_u<Q_u$. La última columna de la Tabla 2 es ahora $\mathrm{med}|T_u/(\sigma\tau_z(b))-1|$ (0.0028, 0.0087, 0.0243, 0.0901 en LN; 0.0027… en SU). Texto de E2: "at σ = 0.01 it lies in [0.997, 1.003] in every replication, with the sign of the deviation set by the side of the capacity on which the sample mean falls (P_u < Q_u in 50 % of the replications, so the median falls between two groups and says nothing), and its median absolute deviation from 1 is 0.0028, the same O(σ) deviation as on symmetric inputs (0.0027)". README y nota corregidos; en `RESPUESTA_SGE001_ronda1_20260930.md` se añadió una nota de corrección junto a "1.000 (desviación 3×10⁻⁷)" (no se reescribió el texto histórico).

### Menores

| id | decisión | cambio |
|---|---|---|
| m1 ("jerárquica") | aceptar | Scope: "The record also speaks of 'hierarchical' frontiers; we read this as two-level aggregation (units, firms, sector) under a common frontier (Lemma 3.3, E3), not as frontiers that differ by level". Resumen y ficha ES/EN: frase sobre la jerarquía (1.15–4473×; confina el fallo a las firmas que cruzan, sin eliminarlo). Ficha: "Estado: En desarrollo — borrador v0.3", alineado con la nota; "Alcance actual" con la lectura de "jerarquía". |
| m2 ("to a relative 0") | aceptar | `sci(..., zero_below=None)` para `\EtwoIdentityGap` y `\EthreeLemmaGap`: el texto dice ahora 2×10⁻¹⁵ (E2, también en la Tabla de afirmaciones) y 2×10⁻¹⁶ (E3). El redondeo a 0 queda sólo para celdas de tablas. |
| m3 (definición de $B_1$) | aceptar | Prop. 3.1(a): "$|E_1|\le\frac12\sum_iM_2^{(i)}\|h_i\|^2=:B_1\le\frac N2M_2s^2$", coherente con el código, el apéndice y la prueba del Cor. 3.6. |
| m4 ((e) hereda $C^3$; forma graduada) | aceptar | Véase M1: "(Certificates; under the hypothesis of (c).)" y $(k+1)B_2<|Q_2|\Rightarrow|E_1|/|E_2|>k$. |
| m5 ("like the inverse dispersion") | aceptar | Resumen: "grows at least like the inverse dispersion (like its square for symmetric inputs)"; Obs. 3.2: "grows at least like 1/σ" y "grows like σ⁻²" con terceros momentos nulos; conclusión: "a factor of order at least 1/σ"; README y ficha igual. |
| m6 (errores estándar en E2) | aceptar | Bootstrap (500 remuestreos, generador propio) de los exponentes de E2: 1.01 (0.003) LN con capacidad, 3.52 (0.21) sin capacidad, 1.00 (0.0001) y 4.00 (10⁻⁵) en SU, pendiente transitoria 8.8 (0.11). En el texto y en el JSON. |
| m7 (E5: σ = 0.6; 1/(λ−1)) | aceptar | Párrafo final de E5 reescrito con macros: en el régimen suave el factor por régimen cumple C1 para σ ≤ 0.3 (mín. 9.23) y falla sólo en σ = 0.6 (3.39), donde ni el orden 2 lo cumple (2.22); bajo capacidad sin unidades que crucen la razón es 1/(λ−1) por construcción (0.80 global, 0.47 por régimen), porque los regímenes se definen por la posición de la media; donde hay cruces el orden 2 gana a lo sumo 2.88 y el factor por régimen cumple en σ ∈ {0.15, 0.3} (9.76, 6.47) pero no en 0.6 (1.53); el fallo sustantivo está en la capacidad (1.02, 1.04, 0.98). |
| m8 (atribución "σ_W only"; l. 144) | aceptar | E3: "depends essentially on σ_W only, by Lemma 3.3(ii) and the homogeneity of the Cobb–Douglas frontier under multiplicative shocks ($f(\bar x_g\odot v)=f(\bar x_g)f(v)$, so a firm's relative error does not depend on its mean)" ("essentially": el agregado pondera las firmas por su producto). L. 144: "evaluating f and its Hessian at the firm means". |
| m9 (E1b: 0.81–0.92 frente a 0.67) | aceptar con matiz | El párrafo de E1b y la Obs. 3.11 salieron del cuerpo por el recorte 1 (queda una frase en Limitaciones con σ = 0.18 a N = 2000). El error estándar de una mediana de |Z| con 20 réplicas (≈ 0.18) se guarda en `E1b.summary` (`se_median_abs_normal_R` = 0.176, `median_abs_normal` = 0.674) y aparece en `tables.md`: 0.81–0.92 está a menos de 1.4 errores estándar de 0.67. |
| m10 ("as the condition guarantees") | aceptar | Resumen: "no reversal occurred among certified comparisons, as it guarantees"; E4: "as Proposition 3.9 guarantees". |
| m11 (números tecleados) | aceptar con matiz | "50–1000" → macros `\EoneLooseMin` = 56 (menor factor $B_2/|E_2|$ en cualquier réplica) y `\EoneLooseMax` = 1064 (mayor factor mediano); "σ ≈ 0.1" (E4) sustituido por las tasas a σ = 0.05/0.1/0.2 con capacidad +10 % (macros); "σ = 0.6" en E5 → `\EfiveTestSigmaMax`; "0.67" desapareció con E1b. Matiz: se mantienen tecleados los parámetros de diseño (mallas, σ = 0.1, 0.316, 10⁻¹², 2 %, 5) y constantes cerradas; la frase de l. 62 dice ahora "Every measured number" y el apéndice lo explicita. |
| m12 (tiempos) | aceptar | `meta` guarda `seconds`/`cpu_seconds` (cálculo) y `seconds_total`/`cpu_seconds_total` (con tablas y figuras); el JSON se escribe al final. PDF: "52 s of wall time for the computation and 56 s including tables and figures (53 and 57 s of CPU; interpreter start-up excluded)" por macros; README y nota con las mismas cifras; recuento de macros corregido (356 en v0.3; v0.2 tenía 291, no 287). En la respuesta de la ronda 1 se añadió una nota de corrección sobre "30 s wall". |
| m13 (bootstrap compartido) | aceptar | `SeedSequence(SEED).spawn(12)`: los 9 primeros hijos son los de v0.2 (sorteos de E0–E5 y bootstrap de E1 sin cambio) y E1c, E2 y E3 reciben generadores de bootstrap propios. Cambian sólo intervalos de E2/E3 (p. ej. el intervalo de $T_u/(\sigma\tau_z)$ en SU sigue siendo [0.997, 0.997]). |

### Verificación de la ronda 1 (puntos a medias o con error nuevo)

| id (ronda 1) | estado según el árbitro | corrección en v0.3 |
|---|---|---|
| B2 (certificado observable) | con error nuevo | M1: dos certificados nombrados, cifras 0.042/0.053 y 0.056/0.071, certificado de C1 0.018/0.023, comparación con 0.75 (razón > 1) y 0.42 (C1). |
| M1 (exponente LN, N finito) | a medias | M3: E1c con 60 réplicas, cuatro N, errores estándar; resumen sin 3.12–3.18 como "predichos". |
| M2 (lectura de la razón desplazada) | lectura errónea nueva | M4: distribución por réplica. |
| m5 (tiempos) | a medias | m12. |
| m12 (ceros por formateo) | con error nuevo | m2. |
| m13 (intro "criteria fixed in advance") | matiz | La introducción remite ahora a la Sección 4, que dice qué está y qué no está documentado sobre cuándo se fijaron. |
| m15 (contigüidad de `EtwoLowerSigmaLN`) | inocuo | Implementada la contigüidad desde la σ más pequeña; el valor no cambia (0.15). |
| m8 (bootstrap compartido) | matiz | m13. |
| Acción 24 (recortes) | a medias | Véase "Extensión". |

### Extensión (acción 11). Aceptar con matiz.

Se aplicaron los seis recortes propuestos: (1) Def. 2.5, Obs. 3.11 y párrafo de E1b fuera del cuerpo (una frase en Limitaciones; números en `results/tables.md`; fila de la tabla de afirmaciones conservada); (2) E2 reducido a dos párrafos (ramas e identidad condensadas); (3) Figura 3 (decisión) fuera del manuscrito (sigue generándose como material suplementario; la serie +10 % se cita en el texto con macros); (4) Ej. 3.10 reducido a la parte (ii) con una frase que remite al Ej. 3.8; (5) constantes de Cobb–Douglas de la Obs. 3.2 al apéndice; (6) intervalos de E3 fuera del texto. Además: filas CES de la Tabla 1 a `tables.md`, Tabla 5 (E5) con LN y SU lado a lado, frase de E1 sobre semiancho de intervalos a `tables.md`, figuras algo más pequeñas, duplicaciones del apéndice eliminadas, `\bibsep` reducido y márgenes de 1 in a 0.85 in. Resultado: **12 → 11 páginas**, con cuerpo y apéndice en 10 y la bibliografía en la 11 (≈ 0.6 p.). El matiz: el texto nuevo que pide esta misma ronda (dos certificados, E1c con errores estándar, distribución de la razón desplazada, lectura de E5) consumió ≈ 0.5 p. de lo ganado; bajar a 10 páginas en total exigiría quitar una demostración, la tabla de afirmaciones o tablas con números verificables, y no se hizo.

### Bibliografía (acción 12). Aceptar.

Nota de continuidad actualizada: las 18 entradas citadas están verificadas (8 en la ronda 1, 10 en la ronda 2); las 7 no citadas no requieren cotejo. Se añadieron los DOI verificados por el árbitro de farrell1957 (10.2307/2343100) y jensen1906 (10.1007/BF02418571).

### Lista de acciones del árbitro → estado

| acción | estado |
|---|---|
| 1 (certificados) | hecha (M1) |
| 2 (C1/C2 en resumen y ficha) | hecha (M2) |
| 3 (E1c) | hecha con matiz (M3: 60 réplicas en los cuatro N) |
| 4 (razón desplazada) | hecha (M4) |
| 5 (jerarquía en Scope/resumen/ficha; Estado) | hecha (m1) |
| 6 (formateo de huecos; $B_1$; (e)) | hecha (m2, m3, m4) |
| 7 ("at least like") | hecha (m5) |
| 8 (errores estándar de E2) | hecha (m6) |
| 9 (E5, σ_W, E1b, "as the condition guarantees") | hecha (m7, m8, m9 con matiz, m10) |
| 10 (50–1000, tiempos, bootstrap) | hecha (m11 con matiz, m12, m13) |
| 11 (recortes ≤ 10 páginas) | hecha con matiz (11 páginas; 10 de cuerpo y apéndice) |
| 12 (nota de continuidad: bibliografía) | hecha |

### Qué cambió en los números

- Sin cambio: todos los valores puntuales de E0, E1, E1b, E2, E3, E4, E5 y E6 (8782 valores comunes comparados hoja a hoja con v0.2).
- Cambian: E1c (rediseñado: 3.16/3.50/4.05/3.96 con s.e. en lugar de 3.2/3.3/4.2 sin s.e.); intervalos bootstrap de E2 y E3 (generadores propios); `\EtwoIdentityGap` y `\EthreeLemmaGap` se imprimen con su valor (2×10⁻¹⁵, 2×10⁻¹⁶) en lugar de 0; columna final de la Tabla 2 (mediana de |razón − 1| en lugar de la mediana de la razón).
- Nuevos: certificados (0.042/0.053; 0.018/0.023; 0.75), fracciones certificadas de E4 con la cota de momentos + rango (100/99.6/94.4/6.5/0 %), distribución de la razón desplazada ([0.997, 1.003], 0.0028), errores estándar de E2, factores de holgura 56 y 1064, lecturas de E5, tiempos de cálculo y totales.
- Corrida: SHA-256 del script `5b309162009c…` (coincide con `sha256sum`), 03/10/2026 10:04 UTC, 52 s de cálculo / 56 s total de pared, 53 / 57 s de CPU.

### Qué queda abierto

1. Extensión: 11 páginas (10 de cuerpo y apéndice); el objetivo de 10 en total no se alcanzó sin sacrificar contenido verificable.
2. Las dos celdas limítrofes de C2 (sin capacidad σ = 0.4; +50 % σ = 0.4) siguen indecisas con 1000 ensayos.
3. Un certificado más fino que explote la cancelación (tensor del tercer momento + resto de cuarto orden) para ampliar la región certificada desde los momentos más allá de σ ≈ 0.04; cota numérica para CES.
4. Confirmar con el autor las lecturas de "dinámica", "jerárquica" y "calibración posterior".
5. Actualizar la ficha del CV web con `FICHA_SGE001_propuesta.md`.

### Cómputo usado en esta ronda

Prueba de E1c (≈ 20 s de CPU), dos corridas de referencia completas (≈ 57 s de CPU cada una; la primera antes de cambiar la cadena `meta.rng`, que alteró el hash), compilaciones (≈ 15 s en total): ≈ 2.5 minutos de CPU, dentro del presupuesto de 10.

### Registro de avance (código y corrida)

- [hecho] Copia de seguridad de v0.2 (resultados, manuscrito, scripts) en el scratchpad de la sesión (`sge001_r2/`).
- [hecho] `frontier_aggregation.py`: (M1) certificados con la cota por segmento (microdatos) y con la cota de momento + rango (`B2box`), para k = 1 (`2B₂<|Q₂|`) y k = 5 (`6B₂<|Q₂|`), y mayor σ con razón observada > 1 en todas las réplicas; fracción certificada en E4 con ambas cotas; comentario del código corregido. (M3) E1c con 60 réplicas para N = 200, 2000, 20000, 200000 (en bloques de 6 réplicas), errores estándar bootstrap (500 remuestreos) y mediana de |E₂−E₃|/Y en σ = 0.01. (M4) E2 guarda mínimo, máximo y mediana de |T_u/(στ_z(b))−1| y la fracción de réplicas con P_u<Q_u. (m6) errores estándar bootstrap de los exponentes de E2. (m13) un generador de bootstrap por experimento (`spawn(12)`; los 9 primeros hijos son los de v0.2). (m15) contigüidad en `LN_delta0_lower_informative_largest_sigma`. (m12) `meta` guarda cálculo y total (con tablas y figuras), pared y CPU.
- [hecho] Corrida de referencia v0.3 completa (sin `--fast`): 51.6 s de cálculo / 55.5 s con tablas y figuras (pared), 53.4 / 57.3 s de CPU; SHA-256 `5b309162009c…` (coincide con `sha256sum` del script en disco). Comparación hoja a hoja con v0.2 (8782 valores comunes): **todos los valores puntuales de E0, E1, E1b, E2, E3, E4, E5, E6 son idénticos**; cambian sólo E1c (rediseñado) y los intervalos bootstrap de E2 y E3 (nuevo generador de bootstrap, m13), como estaba previsto.
