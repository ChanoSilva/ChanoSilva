# Respuesta del autor al informe de arbitraje interno — SGE001, ronda 1 (30/09/2026)

Documento de trabajo. Responde punto por punto a `REFEREE_SGE001_ronda1_20260930.md` (2 bloqueantes, 8 mayores, 15 menores, 24 acciones). Escrito de forma incremental durante la sesión de respuesta (03/10/2026); las entradas marcadas "(en curso)" se completan al final. Decisiones posibles: **aceptar**, **aceptar con matiz**, **rebatir**.

Resumen de decisiones: B1 aceptar; B2 aceptar; M1 aceptar; M2 aceptar; M3 aceptar (opción a: quitar "Dynamic" del título del manuscrito, mantener el nombre de la línea en la ficha y en una nota al pie); M4 aceptar; M5 aceptar con matiz (intervalos de Wilson en la Tabla 4 y clasificación falla/limítrofe/pasa; bootstrap sobre réplicas e errores estándar de exponentes calculados en la corrida, reportados en `results/tables.md` y en macros de resumen, no columna a columna en todas las tablas); M6 aceptar; M7 aceptar; M8 aceptar; m1–m15 aceptar (m13 con matiz: el hash y la fecha se registran desde ahora; no es posible probar retroactivamente que C1/C2 se fijaron antes de la primera corrida, y se dice así). No se rebate ningún hallazgo: cada uno fue verificado contra el código o los resultados y es correcto.

Consecuencia transversal: la acción 19 (un generador por experimento con `SeedSequence.spawn`) cambia todos los sorteos, de modo que **la corrida de referencia es nueva** y todos los números del manuscrito se regeneraron. Los valores anteriores se citan abajo como "v0.1" cuando el contraste importa.

---

## Hallazgos bloqueantes

### B1 — Número erróneo en la ficha (15 de 23 celdas con capacidad)
**Decisión: aceptar.** La ficha decía "15 de 23 celdas con capacidad" y las celdas con capacidad elegibles son 20. Se corrige en ES y EN con la redacción propuesta por el árbitro, con los números de la nueva corrida (ver abajo la sección "Números que cambiaron") y con la clasificación clara/limítrofe de M5. Archivo: `FICHA_SGE001_propuesta.md`, "Principales hallazgos" / "Main findings". (en curso: cifras finales)

### B2 — El "certificado de mejora" de E1 usa el error verdadero y omite un factor 2
**Decisión: aceptar.** Es correcto que B₂ < |E₁| no es observable desde momentos y que lo certificable es 2B₂ < |Q₂| (entonces |E₂| ≤ B₂ < |Q₂| − B₂ ≤ |E₁|). Cambios:
- `experiments/frontier_aggregation.py`, E1: por réplica se evalúa `2*B2 < |Q2|`; la fila guarda `cert_obs_holds_all` y el resumen `sigma_largest_cert_observable` (mayor σ tal que se cumple en todas las réplicas para ese σ y todos los menores). El test antiguo (medianas, B₂ < |E₁|) se conserva en el JSON con el nombre `sigma_largest_bound2_le_e1_median_nonobservable` sólo como diagnóstico; no se usa en el texto.
- `make_numbers.py`: macro `\EoneCertSigma{CDLN,CDSU}` (sustituye a `\EoneBoundSigma…` en el texto).
- `main.tex`, E1 "Bounds", resumen y Sección "What can be claimed": redacción propuesta por el árbitro ("comes with a computable certificate that is very conservative…"). (en curso: valores finales; el árbitro obtuvo 0.056 LN / 0.071 SU)

---

## Hallazgos mayores

### M1 — Exponente 3.78 (CD–LN) / 3.21 (CES–LN) es efecto de N finito
**Decisión: aceptar.** La explicación de la nota de continuidad ("tercer momento log-normal O(σ⁴) solo asintóticamente") era incompleta: a N fijo el tercer momento muestral tiene una fluctuación O(σ³N^{-1/2}) que domina para σ ≲ N^{-1/2}. Cambios: nuevo bloque E1c en el código (CD–LN, N ∈ {200, 2000, 20000}, 6 réplicas, ajuste en σ ≤ 0.05; pendientes de |e₂| y |e₃|), macros `\EonecSlopeTwoN{200,2000,20000}` y `\EonecSlopeThree…`; Obs. "Orders in the dispersion" ampliada con el término muestral; E1 con la frase propuesta; resumen con "2, 4 and 4 for symmetric inputs; 1 at a crossing"; nota de continuidad corregida. (en curso: valores)

### M2 — "Four digits in the constant" es una identidad; T_u/(στ_z) no se reporta
**Decisión: aceptar.** Verificado algebraicamente: en la rama "above" con ū > c, E₂(f_c) + N T_u = E₁(f) − N(ū − f(x̄)) = 0 exactamente; en la rama "below" vale E₂(f) ≈ 10⁻⁹ relativo. Cambios: E2 calcula por réplica T_u/(στ_z) con z_i = (x_i − x̄)/σ y g = ∇f(x̄) (diseño SU: exacto; diseño LN: además T_u/(στ_z(b)) con b = (f(x̄) − c)/σ, que es el enunciado de la Observación con media desplazada); comprobación numérica de la identidad (1) como `identity_max_rel_gap`; Tabla 2 reducida a δ = 0 con columna T_u/(στ_z); texto "(1) is an identity; the two-sided bound (2) reduces to the smooth bounds B₁, B₂, which hold in every cell"; resumen con "T_u/(στ_z) = … at σ = 0.01 on symmetric inputs". (en curso: valores; el árbitro obtuvo 0.9973 SU)

### M3 — "Dynamic" en el título
**Decisión: aceptar (opción a).** Título del manuscrito: "Moment-Based Aggregation of Production Frontiers: Second-Order Corrections, Their Failure at Capacity Thresholds, and What Can Be Certified for Comparisons", con nota al pie "research line SGE001, 'dynamic aggregation of production frontiers'". El párrafo "Scope" dice que el nombre de la línea contiene "dynamic" y que este borrador no introduce ningún modelo intertemporal. La ficha conserva el nombre de la línea (es el nombre del registro público) y el README distingue "título de la línea" de "título del manuscrito". La opción (b) (trayectoria σ_t/δ_t) queda como paso siguiente en la nota de continuidad.

### M4 — Hipótesis del Cor. (cruce): SU exacto vs LN; C⁴; uniformidad en N
**Decisión: aceptar.** Se añade tras el corolario la nota propuesta (diseño SU verbatim; diseño LN → Observación con b aleatorio de orden N^{-1/2}; constantes dependen de la población sólo a través de s_z², m₃ᶻ y los supremos de derivadas sobre el casco convexo; uniformidad en N condicional a su acotación). En la Obs. "Orders": "if D³f is Lipschitz on the hull (e.g. f ∈ C⁴)" para el O(σ⁴). La medición de |f(x̄) − c|/c en LN se añade a E2 (`fxbar_minus_c_rel_med`).

### M5 — Ninguna medida de incertidumbre; C2 frágil en celdas limítrofes
**Decisión: aceptar con matiz.** Se añaden: intervalos de Wilson al 95 % para todas las tasas de la Tabla 4 (calculados en el código, `rev*_ci`); clasificación de cada celda elegible de C2 en "falla claramente" (límite inferior de rev₂ > límite superior de rev₁/5), "pasa claramente" (límite superior de rev₂ < límite inferior de rev₁/5) o "limítrofe"; intervalos bootstrap percentílicos al 95 % (1000 remuestreos de réplicas) para las medianas de E1, E2 y E3 (en el JSON y en `results/tables.md`; en el texto, el semiancho relativo máximo de los intervalos de E1 y los intervalos de las cantidades clave de E2); errores estándar bootstrap de los exponentes de E1 (remuestreo de réplicas y reajuste). Matiz: no se añaden columnas de intervalo a todas las tablas del PDF (espacio, y el objetivo de ≤ 10 páginas); las tablas completas con intervalos están en `results/tables.md`. (en curso: recuento final claro/limítrofe)

### M6 — La rama en f(x̄) = c la decide el redondeo
**Decisión: aceptar.** `aggregate` recibe `branch_at_equality` ("below" por defecto) y usa tolerancia relativa 10⁻¹² (`fb <= cap*(1+1e-12)`); en E2 (δ = 0) y E5 ("at") se reportan la fracción de réplicas con la media muestral a cada lado, la razón mínima restringida a la rama "below" y, en E2, la razón con la convención alternativa "above" (exactamente 1 por construcción). Texto de E2 con la redacción propuesta. (en curso: valores)

### M7 — "above" y "at" en E5 no informan sobre la recalibración
**Decisión: aceptar.** Tabla 5: filas "above" → "n/a (Q₂ ≡ 0)"; filas "at" desdobladas en "all replications" y "below branch", con la fracción de réplicas en cada rama; el resumen de C1 en E5 se calcula excluyendo "above" (`*-C1-holds-excl-above`) y la conclusión se apoya en "smooth" y "below".

### M8 — Etiquetas de estado demasiado generosas en la Tabla de afirmaciones
**Decisión: aceptar.** Tabla de afirmaciones: Prop. (resto) → "classical (Taylor), assembled here"; Lema (jerarquía)(i) → "elementary (law of total covariance); by construction of the definition"; Lema (bisagra) → "elementary"; se mantiene "proved here" para la proposición del cruce, el corolario, el ejemplo de momentos y la condición de margen. Def. de jerarquía: se dice que TD se define evaluando la corrección intra-firma en la media sectorial, que por eso coincide con el agrupado, y que sólo hay dos estimadores distintos (agrupado y ascendente), que es lo que compara E3. Nota de continuidad: "Resultados matemáticos (todos con demostración completa)" → se distingue clásico / elemental / demostrado aquí.

---

## Hallazgos menores

(en curso — se completa tras la corrida y la compilación)

| id | decisión | cambio |
|---|---|---|
| m1 | aceptar | frase de E4 sobre las celdas que pasan reescrita a partir de la lista `C2_passing_cells` del JSON y de la fracción de ensayos con la media bajo la capacidad (`fracA_mean_below_cap`) |
| m2 | aceptar | Ej. (momentos): "identical first three moments" (tercer momento central 0 en ambas; cuarto σ⁴ vs 2σ⁴); resumen igual |
| m3 | aceptar | leyendas de figuras y comentarios del código sin números de proposición (que cambian al fusionar observaciones); se nombran por contenido |
| m4 | aceptar | `table_e1b.tex` y `table_e5b.tex` eliminadas (E1b pasa a un párrafo dentro de E1; E5 por σ queda en `results/tables.md`) |
| m5 | aceptar | `meta` guarda pared y CPU; README, nota y PDF usan la misma cifra con "según la máquina" |
| m6 | aceptar | "between 28 % and 70 % at every order" |
| m7 | aceptar | macro `\EoneConeFirstFail…` (primer punto de malla que falla); "holds at σ = 0.42 and fails at the next grid point, 0.56" |
| m8 | aceptar | `SeedSequence(SEED).spawn()` con un generador por experimento (E0, E1, E1b, E1c, E2, E3, E4, E5, bootstrap); nueva corrida de referencia |
| m9 | aceptar | listas completas de autores de harris2020 y virtanen2020 (BibTeX oficial); Nataf sin cambios |
| m10 | aceptar | README y resumen incluyen CES–LN y "finite-N effect" |
| m11 | aceptar | Obs. (eficiencias): "of order σ³–σ⁴" |
| m12 | aceptar | eje derecho de la figura de umbral sin recorte fijo (nota en el pie); `sci()` muestra 0 para |x| < 10⁻¹⁴ |
| m13 | aceptar con matiz | fecha y SHA-256 del script con C1/C2 registrados en la nota antes de la nueva corrida (y en `meta.script_sha256`); la frase "σ ≤ 0.2" se elimina del texto (era descriptiva y posterior) |
| m14 | aceptar | Def. (capacidad): la "aproximación de segundo orden" en f(x̄) = c es una convención (derivada lateral), no una propiedad de f_c |
| m15 | aceptar | E2: la cota inferior es informativa exactamente cuando N T_u > B₁ + B₂ (+|Q₂|1{·}); macro con el mayor σ en que ocurre a δ = 0 (LN); fuera de ese rango (1) sigue siendo identidad exacta |

---

## Bibliografía
(en curso)

## Recortes a ≤ 10 páginas
(en curso)

## Números que cambiaron (v0.1 → v0.2)
(en curso)

## Estado de compilación
(en curso)

## Lo que queda abierto
(en curso)
