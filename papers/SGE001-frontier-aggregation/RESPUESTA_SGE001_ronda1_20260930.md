# Respuesta del autor al informe de arbitraje interno — SGE001, ronda 1 (30/09/2026)

Responde punto por punto a `REFEREE_SGE001_ronda1_20260930.md` (2 bloqueantes, 8 mayores, 15 menores, 24 acciones). Escrito de forma incremental durante la sesión de respuesta (03/10/2026). Decisiones posibles: **aceptar**, **aceptar con matiz**, **rebatir**.

**Recuento:** 2 bloqueantes aceptados; 8 mayores: 7 aceptados, 1 con matiz (M5); 15 menores: 14 aceptados, 1 con matiz (m13); 0 rebatidos. Cada hallazgo se verificó contra el código o los resultados antes de aceptarlo; los cálculos del árbitro (certificado observable, $T_u/(\sigma\tau_z)$, Wilson, ramas) se reprodujeron con los nuestros.

**Consecuencia transversal.** La acción 19 (un generador por experimento con `SeedSequence.spawn`) cambia todos los sorteos, de modo que **la corrida de referencia es nueva (v0.2)** y todos los números del manuscrito se regeneraron con `make_numbers.py`. La corrida tardó 30 s de pared / 26 s de CPU (script SHA-256 con prefijo `44f421345df7`, 03/10/2026 04:23 UTC). Los valores de v0.1 se citan abajo cuando el contraste importa. La numeración de enunciados cambió al fusionar observaciones: Obs. 3.2+3.3 → Obs. 3.2; Lem. 3.4 → 3.3; Lem. 3.5 → 3.4; Prop. 3.6 → 3.5; Cor. 3.7 → 3.6; Obs. 3.8 (+ nota de M4) → Obs. 3.7; Ej. 3.9 → 3.8; Prop. 3.10 → 3.9; Ej. 3.11 → 3.10; Obs. 3.12 → 3.11. Abajo se usa la numeración del informe (v0.1) salvo indicación.

---

## Hallazgos bloqueantes

### B1 — Número erróneo en la ficha (15 de 23 celdas con capacidad)
**Aceptar.** La ficha decía "15 de 23 celdas con capacidad" y las celdas elegibles con capacidad son 20. Corregido en ES y EN (`FICHA_SGE001_propuesta.md`, "Principales hallazgos" / "Main findings") con la redacción propuesta: "falla en 15 de las 20 celdas elegibles con capacidad del experimento de decisión (23 elegibles en total; las 3 sin capacidad pasan)", añadiendo por M5: "14 de ellas claramente a la resolución de 1000 ensayos y 1 de forma limítrofe, como lo es una de las celdas sin capacidad". Los recuentos de la nueva corrida coinciden con los de v0.1 (23 / 3 / 20 / 15 / 0).

### B2 — El "certificado de mejora" de E1 usa el error verdadero y omite un factor 2
**Aceptar.** Correcto: $B_2<|E_1|$ no es observable desde momentos y lo certificable es $2B_2<|Q_2|$ (entonces $|E_2|\le B_2<|Q_2|-B_2\le|E_1|$). Cambios:
- `frontier_aggregation.py`, E1: por réplica se evalúa `2*B2 < |Q2|`; la fila guarda `cert_obs_holds_all`, `cert_obs_frac`; el resumen `sigma_largest_cert_observable` (mayor σ tal que se cumple en todas las réplicas para ese σ y todos los menores). El test antiguo se conserva en el JSON como `sigma_largest_bound2_le_e1_median_nonobservable`, sólo diagnóstico.
- Resultado: **σ ≤ 0.056 (LN) / 0.071 (SU)**, exactamente los puntos de malla que obtuvo el árbitro; el test no observable de v0.1 daba 0.10 / 0.12.
- Manuscrito: el certificado se enuncia como Prop. 3.1(e) (una línea, con su demostración); E1 "Bounds and certificate" con la redacción propuesta y una frase que explica por qué el test antiguo no es un certificado; resumen: "a very conservative certificate (valid up to σ = 0.056 …)"; tabla de afirmaciones y conclusión actualizadas. En E4 el certificado $|\hat Y_2^A-\hat Y_2^B|>B_2^A+B_2^B$ no se tocó, como indica el árbitro.

---

## Hallazgos mayores

### M1 — Exponente 3.78 (CD–LN) / 3.21 (CES–LN) como "predicho"; explicación de la nota incorrecta
**Aceptar.** La explicación de la nota ("tercer momento log-normal O(σ⁴) sólo asintóticamente") era incompleta: a N fijo el tercer momento muestral fluctúa en $O(\sigma^3N^{-1/2})$ y domina para σ ≲ N^{-1/2} ≈ 0.022, dentro de la ventana de ajuste. Cambios: nuevo bloque **E1c** (CD–LN, N ∈ {200, 2000, 20000}, 6 réplicas, ajuste en σ ≤ 0.05): pendiente de $|e_2|$ = **3.2 / 3.3 / 4.2**, pendiente de $|e_3|$ = 4.01 / 4.00 / 4.00 (el orden 3 elimina el momento muestral exactamente). Con el nuevo flujo aleatorio, el exponente de E1 a N = 2000 es 3.12 (CD) y 3.18 (CES), con errores estándar bootstrap 0.26 y 0.24 (M5): la cifra 3.78 de v0.1 era una realización particular de ese régimen de cruce. Obs. 3.2 ampliada con el término muestral; E1 con la frase propuesta y los valores de E1c; resumen: "2, 4 and 4 for symmetric inputs; 1 at a crossing; 3.12–3.18 … a finite-N effect of the sample third moment"; README y nota corregidos. Matiz de honestidad: a N = 200 la pendiente medida es 3.2 (no 2.9 como en la corrida del árbitro); con 6 réplicas y una ventana de 6 puntos la pendiente a N pequeño es ruidosa, y lo que se afirma es el régimen (≈3 para N ≤ 2000, ≈4 a N = 20000).

### M2 — "To four digits in the constant" es una identidad; $T_u/(\sigma\tau_z)$ no se reporta
**Aceptar.** Verificado algebraicamente: en la rama "sobre" con $\bar u>c$, $E_2(f_c)+NT_u=E_1(f)-N(\bar u-f(\bar x))=0$ exactamente; en la rama "bajo" vale $E_2(f)\approx10^{-9}$ relativo. Cambios: E2 calcula por réplica $T_u/(\sigma\tau_z)$ con $z_i=(x_i-\bar x)/\sigma$, $g=\nabla f(\bar x)$, y la versión desplazada $T_u/(\sigma\tau_z(b))$, $b=(f(\bar x)-c)/\sigma$ (Obs. 3.7(i)); comprobación numérica de la identidad (1) (`identity_rel_gap_max` = 2×10⁻¹⁵). Resultados: **SU: 0.9973 [0.9973, 0.9974] en σ = 0.01**, 0.975 en 0.1, 0.929 en 0.316 (desviación lineal en σ, como dice el corolario); **LN: 0.993 sin desplazar y 1.000 (desviación 3×10⁻⁷) con $b$** en σ = 0.01, 0.976 / 0.910 en 0.1 / 0.316 — lo que verifica también la Obs. 3.7(i). Tabla 2 reducida a δ = 0 con columnas $-E_2/(NT_u)$, $T_u/(\sigma\tau_z)$, $T_u/(\sigma\tau_z(b))$; texto: "(1) is an identity …; the two-sided bound (2) reduces to $B_1$, $B_2$, which hold in every cell"; la macro "1.0000" se retiró del texto y de la tabla de afirmaciones; resumen con "$T_u/(\sigma\tau_z)=0.997$ at σ = 0.01 on symmetric inputs".

### M3 — "Dynamic" en el título
**Aceptar (opción a).** Título del manuscrito: "Moment-Based Aggregation of Production Frontiers: Second-Order Corrections, Their Failure at Capacity Thresholds, and What Can Be Certified for Comparisons", con nota al pie "Research line SGE001, recorded as 'dynamic aggregation of production frontiers'. This draft contains no intertemporal model, so the word is not used in its title". El párrafo "Scope" lo explica. La ficha conserva el nombre de la línea (es el nombre del registro público) y el README distingue título de la línea y del manuscrito. La opción (b) (trayectoria $\sigma_t$/$\delta_t$ que la Prop. 3.5 y la Obs. 3.7(i) ya cubren) queda como paso siguiente (d) del manuscrito y punto 1 de los pendientes de la nota.

### M4 — Hipótesis del Cor. 3.7 y de la Obs. 3.2: SU vs LN; C⁴; uniformidad en N
**Aceptar.** Nueva Obs. 3.7 (ii)–(iii) con el texto propuesto (SU verbatim; LN → (i) con $b$ aleatorio de orden $N^{-1/2}$; constantes dependientes sólo de $s_z^2$, $m_3^z$, $M_2$, $M_3$; uniformidad en N condicional, con la advertencia sobre el casco $\sqrt{\log N}$ y la divergencia de las derivadas Cobb–Douglas en el borde). Obs. 3.2: "if $D^3f$ is Lipschitz on the convex hull (for instance $f\in C^4$, as Cobb–Douglas and CES are)". E2 mide $|f(\bar x)-c|/c$ en LN: hasta 2.9×10⁻⁴ en σ = 0.01 y 9.3×10⁻³ en σ = 0.316 (el árbitro midió 3.6×10⁻⁴ y 1.1×10⁻² con el flujo de v0.1).

### M5 — Ninguna medida de incertidumbre; C2 frágil en celdas limítrofes
**Aceptar con matiz.** Añadido en el código y en el JSON: intervalos de Wilson al 95 % para todas las tasas de E4 (`rev*_ci`); veredicto por celda elegible ("fail" si el límite inferior de rev₂ supera un quinto del límite superior de rev₁; "pass" en el caso espejo; "borderline" si no); intervalos bootstrap percentílicos (1000 remuestreos de réplicas) para las medianas de E1, E2 y E3; errores estándar bootstrap de los exponentes de E1 (500 remuestreos con reajuste). Resultado: **14 fallos claros (todos con capacidad), 2 limítrofes (sin capacidad σ = 0.4: rev₁ 18.1 % [15.8, 20.6], rev₂ 2.4 % [1.6, 3.5]; +50 % σ = 0.4: 27.0 % vs 6.5 % [5.1, 8.2]) y 7 pasan claramente** — la misma estructura que anticipó el árbitro. Texto de E4, resumen, tabla de afirmaciones, README y ficha reformulados ("fails clearly in 14 … two cells are borderline"). Tabla 4 con intervalos para rev₁ y rev₂. Semiancho relativo máximo de los intervalos de las medianas de E1: 70 % (CD–LN, orden 2, σ ≈ 0.03) y 52 % (CES–LN), ≤ 3 % con SU — se dice en E1 y explica por qué el exponente LN es ruidoso. **Matiz:** no se añadieron columnas de intervalo a todas las tablas del PDF (espacio y objetivo de extensión); las tablas completas con intervalos están en `results/tables.md`, y el texto cita los intervalos de las cantidades clave (error con capacidad en σ = 0.01, $T_u/(\sigma\tau_z)$, ganancia máxima de E3).

### M6 — La rama en $f(\bar x)=c$ la decide el redondeo
**Aceptar.** `aggregate(..., branch_at_equality="below")` con tolerancia relativa 10⁻¹² (`fb <= cap*(1+1e-12)`); en E2 (δ = 0) se reportan `frac_reps_mean_above`, `r21_min_below_branch`, `r21_min_above_branch` y la convención alternativa (`r21_min_alt_branch_above`); en E5 lo mismo para "at". Resultados: SU 0 % de réplicas "sobre" con la convención (100 % con la opuesta, razón exactamente 1.00); LN 40–55 % "sobre" por muestreo; razón mínima en la rama "bajo" **1.005 (LN y SU) en σ = 0.01** (el árbitro obtuvo 1.003 con v0.1), creciente con σ (Tabla 2). Texto de E2 con la redacción propuesta; Def. 2.4 y README lo declaran.

### M7 — "above" y "at" en E5
**Aceptar.** Tabla 5: filas "above" → n/a; filas "at" desdobladas en "all replications" y "below branch only" (LN: 20–30 % de réplicas "sobre"; SU: rama "bajo" por convención). Resumen de C1 en E5 calculado excluyendo "above" (`*-C1-holds-excl-above`); conclusión apoyada en "smooth" (0.44 global) y "below" (0.47 por régimen); en "at" las razones de la rama "bajo" son 1.02 / 1.04 / 0.98 (LN).

### M8 — Etiquetas de estado demasiado generosas
**Aceptar.** Tabla de afirmaciones: Prop. 3.1 → "classical (Taylor), assembled here; verified"; exponentes → "consequence of Prop. 3.1; verified"; Lem. 3.4(i) → "elementary (total covariance); by construction of Def. 2.3"; Lem. 3.4(ii), Lem. 3.5, Prop. 3.10, Obs. 3.12 → "elementary"; se mantiene "proved here" para Prop. 3.6, Cor. 3.7 y Ej. 3.9; el pie dice que lo original es la combinación Prop. 3.6 + Cor. 3.7 + Ej. 3.9 + experimentos. Def. 2.3 dice que TD se define evaluando la corrección intra-firma en la media sectorial, que por eso coincide con el agrupado y que sólo hay dos estimadores distintos, que es lo que compara E3. La nota de continuidad distingue clásico / elemental / demostrado aquí.

---

## Hallazgos menores

| id | decisión | cambio |
|---|---|---|
| m1 | aceptar | E4: las celdas con capacidad que pasan se listan desde el JSON (`C2_passing_cells`: +50 % σ = 0.2; +50/+20/+10/+5 % σ = 0.8) y se explica que la media muestral de A queda bajo la capacidad en ≥ 96 % de los ensayos (`fracA_mean_below_cap`), por lo que las filas +50/+20/+10 % en σ = 0.8 son casi idénticas |
| m2 | aceptar | Ej. 3.9: "mean c, variance σ², third central moment 0 (they differ in the fourth, σ⁴ against 2σ⁴)"; "first three moments" en el enunciado, resumen, tabla de afirmaciones, README y ficha |
| m3 | aceptar | Leyendas de figuras y comentarios del código sin números de proposición (que además cambian al fusionar observaciones): "certified bound $B_2/Y$", "error against the crossing term $NT_u$", comentarios "remainder-bound proposition", "capacity proposition" |
| m4 | aceptar | `table_e1b.tex`, `table_e3.tex` y `table_e5b.tex` ya no se generan (make_numbers los borra si existen); E1b es un párrafo dentro de E1; E3 y E5 por σ están en `results/tables.md` |
| m5 | aceptar | `meta` guarda `seconds` (pared) y `cpu_seconds`; PDF: "30 s wall (26 s CPU)"; README y nota: "30 s en la máquina de referencia (30–50 s según la máquina)" |
| m6 | aceptar | "the second-order rate stays between 31.1 % and 65.7 %" (sin "coin toss") |
| m7 | aceptar | Macro `C1_first_failing_sigma`: "holds at σ = 0.42 and fails at the next grid point, σ = 0.56"; resumen: "beyond σ = 0.42" |
| m8 | aceptar | `SeedSequence(SEED).spawn(9)`: un generador por experimento (E0, E1, E1b, E1c, E2, E3, E4, E5) más uno para el bootstrap; nueva corrida de referencia declarada en README, nota y PDF |
| m9 | aceptar | harris2020 (26 autores) y virtanen2020 (34 autores + SciPy 1.0 Contributors) con listas completas y DOI; Nataf sin cambios; houthakker1955 se deja con año 1955 (el árbitro lo marcó como opcional) |
| m10 | aceptar | README y resumen incluyen CES–LN y "finite-N effect" |
| m11 | aceptar | Obs. 3.12: "of order σ³–σ⁴ (Remark 3.2)" |
| m12 | aceptar | Panel derecho de la figura de umbral con eje [−0.6, 1.6] y pie que declara el punto recortado (δ = −0.30, σ ≈ 0.15, razón −3.2, donde $NT_u$ es menor que el error suave); `sci()` muestra 0 para |x| < 10⁻¹⁴ (la fila δ = +0.10 ya no está en la tabla del PDF, pero sí en `results/tables.md`) |
| m13 | aceptar con matiz | Hash SHA-256 y fecha del script guardados en `meta` desde v0.2 y registrados en la nota (v0.1: `8cc641bf…781a`; v0.2: `44f421345df7…`); el texto dice que no existe registro fechado de v0.1. La frase "σ ≤ 0.2 … at least 34/69/33/63" se eliminó del texto (era un resaltado descriptivo posterior); la macro ya no se genera. Matiz: no es posible probar retroactivamente que C1/C2 se fijaron antes de la primera corrida; sólo cabe decirlo y registrarlo de aquí en adelante |
| m14 | aceptar | Def. 2.4: "At f(x̄) = c the Hessian of f_c does not exist; 'second-order approximation' there means, by convention, the one-sided derivatives of the 'below capacity' branch (a convention about the estimator, not a property of f_c)" |
| m15 | aceptar | E2: "its lower-bound form … is informative exactly when $NT_u$ exceeds the smooth bounds, which at δ = 0 (LN) happens for σ ≤ 0.15 and in 33 of the 168 cells overall; outside that range (1) remains an exact identity" |

---

## Bibliografía
- Correcciones aplicadas: listas de autores completas de harris2020 y virtanen2020 (m9).
- Recorte de la introducción (propuesta 1 del árbitro): ya no se citan klein1946, hildenbrand1994, stoker1993, jones2005, meeusen1977, ccr1978, kumbhakarlovell2000; siguen en `refs.bib` por si se recuperan. Se citan 18 entradas.
- Las 13 entradas "no verificables en línea" quedan marcadas como tales en la nota de continuidad (sección "Bibliografía: estado"); no se inventó ni se borró ninguna.

## Recortes de extensión
Aplicados: (1) introducción con 8–10 citas; (2) Obs. 3.2 y 3.3 fusionadas, prueba de la Prop. 3.1 en cinco líneas, prueba del Lema 3.4 en dos, Obs. 3.8 fusionada con la nota de M4; (3) Tabla 2 reducida a δ = 0 (ahora con las columnas de M2/M6), Tabla 3 (E3) y las tablas por σ a `results/tables.md`, Figuras 2 y 3 fusionadas en una 2×2, Figura 4 a tres paneles, Figura 1 a dos paneles (Cobb–Douglas; los números CES están en la Tabla 1), E1b como párrafo, "Common protocol" fusionado con el apéndice; (4) apéndice sin las fórmulas de derivadas (están en el código y las comprueba E0); (5) tabla de afirmaciones a 13 filas; (6) cuerpo a 10pt y resumen de ~450 a ~300 palabras. Resultado: **15 → 12 páginas** (≈10.3 de cuerpo, 0.6 de apéndice, 1 de bibliografía), 0 referencias indefinidas, 0 cajas desbordadas. No se llegó a ≤ 10: lo que falta exigiría quitar demostraciones (Prop. 3.1, Prop. 3.5, Cor. 3.6), la tabla de afirmaciones o tablas con números verificables, y se decidió no hacerlo; se deja constancia en la nota (pendiente 6).

## Números que cambiaron (v0.1 → v0.2; nueva corrida por m8)
| Cantidad | v0.1 | v0.2 |
|---|---|---|
| Exponente orden 2, CD–LN / CES–LN (N = 2000) | 3.78 / 3.21 | 3.12 (±0.26) / 3.18 (±0.24) |
| Exponente orden 2 vs N (E1c, nuevo) | — | 3.2 / 3.3 / 4.2 (N = 200 / 2000 / 20000) |
| Razón mínima en σ = 1, CD / CES (LN) | 0.75 / 0.65 | 0.31 / 0.48 |
| Orden 3 peor que orden 2 (mediana), CD / CES | 17/17 / 14/17 | 15/17 / 13/17 |
| Certificado de mejora, LN / SU | 0.10 / 0.12 (test no observable) | 0.056 / 0.071 (2B₂ < |Q₂| en todas las réplicas) |
| |E₂|/B₂ máximo (LN / SU) | 0.020 / 0.016 | 0.018 / 0.016 |
| E1b: razón en σ = 0.01; mediana/sd predicha | 9×10³; 0.70–0.86 | 7×10³; 0.81–0.92 |
| E2: exponente con capacidad LN / SU; suave LN | 1.00 / 1.00; 3.36 | 1.01 / 1.00; 3.52 |
| E2: amplificación en σ = 0.01 | 7×10⁵ | 1×10⁶ |
| E2: $T_u/(\sigma\tau_z)$ SU en σ = 0.01 (nuevo) | — | 0.997 |
| E2: razón mínima rama "bajo" en σ = 0.01 (nuevo) | — | 1.005 (LN y SU) |
| E2: cota inferior informativa (celdas) | 32 | 33 |
| E3: ganancia ascendente | 1.16–4005 | 1.15–4473 |
| E3: aporte de firmas que no cruzan | ≤ 4.2×10⁻³ | ≤ 6.9×10⁻³ |
| E4: rev₁ máx. suave / rev₂ máx. suave | 45.2 % / 3.3 % | 46.1 % / 2.8 % |
| E4: certificado en σ = 0.2 | 70.8 % | 70.9 % |
| E4: rev₂ con capacidad en la media | 28.1–65.3 % | 31.1–65.7 % |
| E4: orden 3 en σ = 0.8 | 89.2 % | 90.8 % |
| E4: C2 | 15 de 23 fallan | 15 de 23 (puntual); 14 claros, 2 limítrofes, 7 pasan |
| E5: λ global; por régimen | 2.68; 0.90 / 3.11 / 4.65 | 2.25; 0.89 / 3.14 / 4.72 |
| E5: razones mínimas LN (orden 2 / global / régimen, suave) | 2.80 / 0.38 / 4.65 | 2.22 / 0.44 / 3.39 |
| Tiempo de la corrida | 36–48 s según la máquina | 30 s pared / 26 s CPU |
Sin cambio: C1 LN se cumple en 0.42 y falla en 0.56; C1 SU en todo el barrido; E2 168/168 celdas; E3 16/16; E4 0 reversiones certificadas; 23/3/20/15/0 en C2; E6.

## Estado de compilación
`manuscript/build.sh` (make_numbers + latexmk): 0 errores, 0 referencias/citas indefinidas, `pdftotext main.pdf - | grep -c "??"` = 0, 0 `Overfull`, **12 páginas** (antes 15). Páginas con tablas y figuras renderizadas y revisadas (Tabla 2 con τ y ramas, Tabla 4 con Wilson, Tabla 5 con n/a, figuras fusionadas).

## Lo que queda abierto
1. Confirmar con el autor la opción (b) de M3 (trayectoria dinámica) y las lecturas de "jerárquica" y "calibración".
2. Dos celdas limítrofes de C2 necesitan más ensayos (≥ 10⁴ por celda) para un veredicto; la conclusión cualitativa no depende de ellas.
3. Exponente LN del orden 2 con error estándar 0.26 a N = 2000; se reporta como régimen de N finito, no como constante.
4. Extensión: 12 páginas frente al objetivo ≤ 10.
5. 13 entradas bibliográficas por cotejar en línea antes de cualquier envío.
6. Cota más fina (cancelación) y cota numérica para CES; estimación paramétrica de $T_u$; eficiencias correlacionadas.

## Tiempo de cómputo de la sesión
Experimentos: corrida rápida de depuración 9.4 s, corrida completa 28.8 s, corrida completa final (hash definitivo) 29.7 s, regeneración de figuras < 5 s: ≈ 75 s de CPU. Compilaciones LaTeX: 10 (≈ 20 s cada una).
