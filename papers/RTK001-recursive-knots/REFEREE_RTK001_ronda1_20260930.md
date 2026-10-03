# Informe de arbitraje interno — RTK001 "Geometry of Recursive Knots" (ronda 1, 30/09/2026)

Árbitro: agente independiente (no autor). Material revisado íntegramente: `README.md`, `CONTINUIDAD_RTK001_20260930.md`, `FICHA_RTK001_propuesta.md`, `PLAN.md`, `manuscript/main.tex` (270 líneas), `refs.bib`, `numbers.tex`, `table_*.tex`, `main.pdf` (10 páginas, renderizadas), `experiments/recursive_knots.py`, `shrink.py`, `make_numbers.py`, `results/results.json`, `results_shrink.json`, `tables*.md`, `run_full.log`. No se evaluó `theory/` (trabajo paralelo de otro agente). No se modificó ningún archivo del autor; los archivos de trabajo están en el scratchpad (`referee_RTK001/`: `notas_math.md`, `check_macros.py`, `verif2.py`, `analysis.py`, `analysis.out`, `repro_root/`, `repro_fast*.log`). Las referencias a líneas son de `manuscript/main.tex`.

## Veredicto

**Cambios mayores.** Los tres lemas elementales (3.1, 3.2, 3.3) y la Proposición 3.4 son correctos, los números del texto salen del JSON sin excepción y la corrida rápida reproduce los resultados publicados con diferencia relativa 0. Pero (i) la Hipótesis (H_c), tal como está enunciada (constante que depende solo de (p,q,f), para toda curva K de grosor τ), es **falsa**: se construyen contraejemplos por dos mecanismos distintos, de modo que el Corolario 3.6 es condicional a un enunciado insostenible y debe reformularse para la familia recursiva; (ii) el "criterio predefinido" (C3) con c = 1/2 no estaba predefinido (PLAN.md deja c sin fijar; la constante natural c = 1 falló y se halvó), y la afirmación repetida "c = 1 falla exactamente en un nivel" es falsa (falla en 4 de 15 niveles con f ≤ 1/2); (iii) la descripción del caso no demostrado como "geometría local de p hebras sobre un tubo curvado" contradice los propios datos: en f = 1/2, d = 1 el par doblemente crítico que fija el grosor cruza el agujero del toro (puntos base a 104°).

Recuento: 2 bloqueantes, 6 mayores, 17 menores.

## Hallazgos bloqueantes

### B1. La Hipótesis (H_c) es falsa tal como está enunciada; el Corolario 3.6 hereda el problema
- **Ubicación:** l. 103 ("Throughout, K = K_{d−1} is a closed C^∞ regular curve of thickness τ"), l. 148–153 (Hipótesis: "There is a constant c ∈ (0,1], depending only on (p,q) and on f = r/τ ≤ 1/2, such that thick(K_d) ≥ ρ_d"), l. 157–166 (Corolario), resumen (l. 55), tabla de afirmaciones l. 244, `FICHA` ("hipótesis local sobre el grosor").
- **Problema:** la construcción (3) depende de la parametrización de K (θ_d = q t/p avanza en el parámetro t, no en arco; declarado en l. 92 y en Limitaciones (3)), y (H_c) se enuncia para cualquier K parametrizada con periodo 2π. Con (p,q,f,τ) fijos, thick(K_d) puede hacerse arbitrariamente pequeño por dos vías independientes:
  1. *Paso de hélice.* Modelo de tubo recto K(t) = (0,0,vt), v = |K'|, p = 2, q impar: las hebras son A(t) = (r cos(qt/2), r sin(qt/2), vt) y B(t) = K_d(t+2π) = (−r cos(qt/2), −r sin(qt/2), vt). El punto B(t + 2π/q) = (r cos(qt/2), r sin(qt/2), vt + 2πv/q) está exactamente encima de A(t) a distancia 2πv/q, con cuerda perpendicular a ambas hebras. Luego dcsd(K_d) ≤ 2πv/q y thick(K_d) ≤ πv/q → 0 cuando v → 0. Para una K cerrada basta ralentizar la parametrización en un arco de longitud ≫ r (la geometría de K, y por tanto τ, no cambian). El texto mismo da el criterio (l. 146–147: el par antipodal es mínimo local sii h = |K'|p/q ≥ r), pero no lo convierte en hipótesis.
  2. *Derivada de la curvatura.* De (5), K_d' = aT + b m con a = |K'|(1 − r(κ̃₁cosθ + κ̃₂sinθ)), b = r(θ'+ω'), m = −sinθ N + cosθ B. En K_d' × K_d'' aparece el término b·a'·(m × T) = b a' n, y a' contiene −r|K'|(κ̃₁' cosθ + κ̃₂' sinθ). Nada en (τ, r, p, q) acota κ'. Ejemplo plano: ρ(φ) = 1 + (δ/m²) cos(mφ) tiene κ ∈ [1 − O(δ), 1 + O(δ)], grosor ≥ 1 − O(δ) y κ' ≈ δ m sin(mφ); con δ fijo y m → ∞, la componente normal de K_d' × K_d'' crece como r²(q/p) δ m y minRad(K_d) → 0 < ρ_d. (En offsets planos, θ'+ω' = 0 y el término desaparece; de ahí que la intuición "offset de curva gruesa" engañe.)
- **Evidencia numérica de que dentro de la familia sí es plausible:** en las cadenas calculadas min_t |K_{d−1}'| crece como (p/2)^{d−1} mientras r_d → 0, y minRad(K_d)/r_d ≥ 1.147 en los 36 niveles (`verif2.py`), es decir, la curvatura nunca es la que fija τ.
- **Corrección concreta:** reenunciar (H_c) como hipótesis sobre la familia: "Sea (K_d) la familia de la Definición 2.1 construida desde el círculo con patrón (p,q) fijo y r_d ≤ f·thick(K_{d−1}), f ≤ 1/2. Existe c = c(p,q,f) ∈ (0,1] tal que, para todo d ≥ 1, thick(K_d) ≥ min(thick(K_{d−1}) − r_d, c r_d sin(π/p))". Si se quiere mantener un enunciado para K general, añadir explícitamente las hipótesis (a) min_t |K'(t)|·p/q ≥ r (paso de hélice) y (b) una cota explícita de |κ'| (o de |K'''|) de K, y decir que c depende de ellas. Cambiar en l. 103 "Throughout" para que diga que la parametrización de K es la heredada de la construcción. Cambiar el status del Corolario a "conditional on (H_c) for the family". Reescribir el resumen (l. 55) y la `FICHA` en consecuencia.

### B2. El criterio (C3) no estaba predefinido, y la afirmación "c = 1 falla exactamente en un nivel" es falsa
- **Ubicación:** l. 184 (párrafo "Predefined criteria", C3 con c = 1/2), l. 155–156 ("with c=1 the inequality fails in exactly one level (f=1/2, d=1, ratio 0.83), so c=1 is not the right constant on a bent tube"), l. 186 ("fails in one default level"), l. 244 (tabla de afirmaciones: "c=1 fails in one level"); `README.md` ("con c = 1 falla exactamente en un nivel"); `CONTINUIDAD` ("Constante c de la hipótesis (H_c)" y "Resultados de referencia").
- **Evidencia (a) sobre la predefinición:** `PLAN.md` (escrito antes del código) fija "thick(K_d) ≥ ρ_d = min(τ_{d−1} − r_d, c · s_d), s_d = strand separation … Justify c": la constante no estaba fijada, y la unidad era la cuerda completa s_d. `CONTINUIDAD` reconoce que "una primera versión del código calculaba, por error de convención, la variante c = 1 bajo el nombre c = 1/2": esa variante es exactamente c_PLAN = 1/2 (media cuerda = r sin(π/p)), la cota natural y la única que es ajustada en tubo recto (l. 155). Esa cota falla en (2,3), f = 1/2, d = 1 (0.832). Tras verlo, el manuscrito redefine ρ con c·r sin(π/p) y elige c = 1/2 (cuarto de cuerda), con lo que (C3) pasa con margen 1.66. Sea cual sea la intención, la constante de (C3) se fijó después de ver los datos.
- **Evidencia (b) sobre el recuento** (`check_macros.py`, `verif2.py`, resolución fina, f ≤ 1/2, 15 niveles): con c = 1 fallan 4: (2,3) f=0.5 d=1 (τ/ρ₁ = 0.832); (3,2) d=1 (0.968); (3,2) d=2 (0.9989); (2,5) d=1 (0.564). Además en (3,2) d = 2, 3 se tiene τ/r = 0.865/0.866 = sin(π/3): c = 1 se *alcanza* (par de hebras adyacentes del mismo disco), no se cumple con margen. La macro `\AllMinTauOverRhoOne` = 0.56 ya lo delata, pero el texto la acompaña de "fails in one default level".
- **Corrección concreta:** (i) retitular l. 184 "Criteria" y escribir: "(C1), (C2) y (C4) se fijaron en PLAN.md antes de las corridas; la constante c = 1/2 de (C3) se fijó después de que una primera corrida con la constante natural c = 1 fallara en (f = 1/2, d = 1)". (ii) Sustituir en l. 155–156, l. 186, l. 244, `README` y `CONTINUIDAD` por: "con c = 1 la desigualdad falla en 4 de los 15 niveles con f ≤ 1/2 (uno de la familia por defecto, tres de los otros patrones) y se alcanza con igualdad en (3,2), d = 2, 3". (iii) Presentar (H_c) con la constante natural c = 1 y reportar la tabla de cocientes τ_d/ρ_d observados; el valor c = 1/2 es entonces una elección empírica, no un criterio.

## Hallazgos mayores

### M1. El caso no cubierto no es "local": el par crítico en f = 1/2 cruza el agujero del toro
- **Ubicación:** l. 146–147 ("pairs whose base points are close but distinct (the local geometry of p strands on a bent tube) … the bending of K changes this by relative terms of order rκ ≤ 1/2"), l. 155 ("c = 1 is not the right constant on a bent tube"), l. 188 ("the bending of the base torus bringing inner strands closer"), l. 257 (Limitaciones (1): "the local case on a bent tube"), l. 259–260 (Next steps (1): "the antipodal-pair analysis for p = 2 (h ≥ r) is the natural start"), resumen l. 55 ("the remaining local case"), `FICHA` ("hipótesis local").
- **Evidencia** (`verif2.py`, N₀ = 512): para f = 0.5, d = 1 el par doblemente crítico que realiza dcsd = 0.8316 tiene puntos base separados 104.1° sobre K₀ (distancia euclídea entre bases 1.577 < 2τ₀ = 2), ambos a radio cilíndrico 0.511 y alturas z = ±0.104: se miran a través del agujero del toro. Para f = 0.35 el par es el antipodal del mismo disco (τ = r). Obsérvese además que para d = 1 (K₀ círculo unidad, τ₀ = 1) la condición de la Prop. 3.4(b), |K(t₁) − K(t₂)| ≥ 2τ₀ = 2, solo la cumplen los pares antipodales: en profundidad 1 el caso (b) es prácticamente vacío y "el tercer caso" es casi todo. Un análisis de hélice local (h ≥ r) no puede demostrar (H_c) en f = 1/2, d = 1.
- **Corrección:** reescribir l. 146: "Not covered: pairs with 0 < |K(t₁) − K(t₂)| < 2τ. These include (i) nearby base points (local helix geometry) and (ii) base points on different arcs of K at distance < 2τ, e.g. across the hole of a torus; at f = 1/2, d = 1 the doubly critical pair is of type (ii) (base points 104° apart)". Quitar "local" del resumen, de Limitaciones (1) y de la `FICHA`. Reorientar Next steps (1): en d = 1 el problema es un cálculo explícito y certificable (distancia mínima entre las hebras de T(p,q) sobre el toro de radios (1, r) en función de r); el análisis h ≥ r solo decide si el par antipodal es mínimo local (y predice correctamente τ₁ = r₁ sii r ≤ p/(p+q) = 0.4 para (2,3), coherente con los cuatro valores de f).

### M2. La Conjetura 3.9 es en gran parte trivial, y la mitad "≤" de thick(K_d) = r_d es demostrable
- **Ubicación:** l. 176–178 (Conjetura: "Rop(K_d) grows like Θ(Λ_*^d) with Λ_* ≈ 4.00"), l. 168–170 (Remark: "growth factor per depth is about 4.06–4.00 against Λ = 20"), `README`/`CONTINUIDAD` ("Λ_* ≈ 4.0 … conjeturas").
- **Evidencia:** Rop_d/Rop_{d−1} = (L_d/L_{d−1})·(τ_{d−1}/τ_d). En el JSON los cocientes de longitud tienden a p (f = 1/2: 2.538, 2.028, 2.001; (3,2): 3.183, 3.004, 3.000) y los de grosor valen f (o f sin(π/3) para (3,2)), de modo que los cocientes de Rop tienden a p/f: 8.0, 5.715, 4.0 para f = 0.25, 0.35, 0.5 y 6.93 = 3/(0.5·sin(π/3)) para (3,2). L_d/L_{d−1} → p porque r_d κ_max(K_{d−1}) ≤ r_d/minRad(K_{d−1}) → 0 (minRad se mantiene en [0.49, 0.86] mientras r_d → 0). Λ_* = p/f no es una constante empírica nueva: es consecuencia de τ_d = r_d. Además, para p = 2, thick(K_d) ≤ r_d **se demuestra en dos líneas**: la cuerda entre K_d(t) y K_d(t + 2π) es −2r(cosθ N + sinθ B), ortogonal a T y a m = −sinθ N + cosθ B, luego ortogonal a K_d' en ambos extremos por (5); por Gonzalez–Maddocks (l. 73) thick(K_d) ≤ ρ_pt = r. Con la cota inferior |K_d'| ≥ |K'|(1 − rκ) (misma ecuación (5)) se obtiene también L(K_d) ≥ p L(K_{d−1})(1 − r_d κ_max) y, dentro de la familia, Rop(K_d) ≥ L(K_d)/r_d: una cota inferior gratuita que el texto dice no tener (l. 172–174, Limitaciones (6)).
- **Corrección:** sustituir la Conjetura por una Proposición (p = 2: thick(K_d) ≤ r_d; L(K_d) ≥ pL(K_{d−1})(1 − r_dκ_max); por tanto Rop(K_d) ≥ L(K_d)/r_d) más una observación ("si τ_d = r_d para todo d grande, entonces Rop_d/Rop_{d−1} → p/f"), y dejar como conjetura solo "thick(K_d) = r_d para f pequeño". Actualizar la tabla de afirmaciones (l. 251) y la `FICHA` ("no se derivan cotas inferiores nuevas" pasa a "solo cotas inferiores internas a la familia").

### M3. Lema 3.2: caso semientero, cálculo robusto de Lk y cita de la convención de cable
- **Ubicación:** l. 116–121; l. 188–189 ("The measured α_d agrees with 2π frac(Wr K_{d−1}) … (e.g. α₂ = −3.027)"); `recursive_knots.py:214` (`n_frame = int(np.rint(out[-1]["writhe"]))`); `FICHA` ("el writhe del trébol cruza 3.5").
- **Evidencia:** el signo es correcto: con ω = −αt/2π, Tw = (1/2π)∫B·N' = −α/2π y Lk = Wr − α/2π; con α ∈ (−π, π] esto es round(Wr) (semienteros redondean hacia abajo). Comprobado en los 36 niveles (`check_macros.py`): max |Wr_{d−1} − α_d/2π − n| = 1.1·10⁻³ a resolución fina (4.5·10⁻³ en (3,2) N₀ = 256, d = 3); con el signo opuesto la cantidad nunca es casi entera (3.036 en f = 1/2). Pero: (i) la cláusula "well defined when α ≠ π" es innecesaria si el lema afirma Lk = Wr − α/2π (válido también en α = π, donde Lk = Wr − 1/2 y la construcción sigue siendo válida); (ii) el código toma n = rint(Wr) del writhe numérico solo, en lugar de rint(Wr − α/2π), que es casi entero por construcción y cuyo residuo es un test de consistencia; el texto solo ejemplifica α₂ y no reporta el residuo máximo; (iii) la cita "[Lickorish, Ch. 1]" para la definición del cable (p, q+pn) con p longitudinal no ha podido verificarse (ver Bibliografía); la convención está declarada en el texto, pero conviene hacerla autocontenida (Lk(K_d, K) = pn + q = Lk(cable (p,q'), K) = q'); (iv) "writhe del trébol" (FICHA) es impreciso: el writhe no es invariante del nudo, es el writhe de la configuración K₁ sobre el toro de radios (1, r); el cruce ocurre en r* ≈ 0.490 (bisección, N₀ = 512).
- **Corrección:** enunciar "Lk = Wr − α/2π ∈ Z; si Wr ∉ Z + 1/2, Lk = round(Wr)"; en el código calcular `n_frame = rint(Wr − α/2π)` y guardar el residuo; añadir macro con el residuo máximo; en la FICHA escribir "el writhe de la configuración de profundidad 1 cruza 3.5 (en r ≈ 0.49)".

### M4. La precisión declarada del writhe (10⁻³) no se cumple en todas las cadenas
- **Ubicación:** l. 247 (tabla de afirmaciones: "Wr to 10⁻³"), l. 257–258 (Limitaciones (5): "their agreement to 10⁻³ under doubling of N is the only accuracy check").
- **Evidencia** (`verif2.py`): |Wr_grueso − Wr_fino| = 0.031 en (3,2) d = 3; 0.0044 en (2,5) d = 3; 0.0022 en (2,3) f = 0.25 d = 3; ≤ 10⁻⁴ en d = 1 de (2,3). La doble suma con regla del punto medio converge despacio en las cadenas largas. Las decisiones de tipo de nudo no se ven afectadas (márgenes ≥ 0.16 salvo f = 1/2, d = 1: 0.018 frente a error ≤ 10⁻⁴).
- **Corrección:** escribir "≤ 10⁻⁴ for Wr(K₁) in the default family, up to 3·10⁻² at depth 3 of (3,2)"; mejor, sustituir la regla del punto medio por el writhe poligonal exacto (Levitt 1983; Klenin–Langowski 2000), de igual coste O(N²).

### M5. Corolario 3.6: dos imprecisiones lógicas
- **Ubicación:** l. 157–166.
- **Problema:** (i) "ρ_d = γ^d" / "ρ_d = ρ_{d−1} min(1−f, cf sin(π/p))": (H_c) con el grosor real τ_{d−1} ≥ ρ_{d−1} da thick(K_d) ≥ min(τ_{d−1} − r_d, c r_d sin(π/p)) ≥ γ ρ_{d−1}, una desigualdad; ρ_d debe *definirse* como γρ_{d−1} (cota garantizada), no deducirse como igualdad de (7). (ii) (H_c) se invoca con cociente r_d/thick(K_{d−1}) = fρ_{d−1}/τ_{d−1} ≤ f, no = f; (H_c) debe pedirse para todo r ≤ fτ (c función de una cota superior de r/τ).
- **Corrección:** "Define ρ₀ = 1, ρ_d := γρ_{d−1}, r_d := fρ_{d−1}. Under (H_c) (stated for all r ≤ fτ), thick(K_d) ≥ ρ_d by induction, and …".

### M6. Afirmaciones de README/CONTINUIDAD/manuscrito que no coinciden con los artefactos
- `README` tabla y `CONTINUIDAD` §"Qué se produjo": "9 páginas"; `main.pdf` tiene 10.
- l. 182 ("total time 4.6 CPU-minutes") y `README` ("4.6 min de CPU"): `meta.seconds` = 278 s es tiempo de pared (así lo dice el apéndice, l. 266); con NumPy multihilo el tiempo de CPU es mayor. Decir "wall time" en ambos sitios.
- l. 191 (sonda): "at depth two from 155.6 to 155.6 at step 0 (0.0% …)" es formalmente cierto y confuso: el mejor polígono es el inicial. Escribir "at depth two no step improves L/τ, which rises monotonically to 156.3".
- `CONTINUIDAD` §"Decisiones": "Se comprobó numéricamente que α = 2π·frac(Wr K_{d−1})" — correcto, pero el único número citado es α₂; añadir el residuo máximo (M3).

## Hallazgos menores
- m1. l. 77–79, ec. (2): N, B es el marco girado, pero se escriben κ₁, κ₂ del marco de Bishop; los coeficientes correctos son κ̃₁ = κ₁cosω + κ₂sinω, κ̃₂ = −κ₁sinω + κ₂cosω (misma norma κ). Añadir una frase.
- m2. l. 105–114, Lema 3.1: la prueba solo usa r < τ (coeficiente tangencial ≥ |K'|(1 − r/τ) > 0 y discos disjuntos). Enunciar con r < τ y reservar r ≤ τ/2 para la constante 1/2 del Lema 3.3/Corolario.
- m3. l. 103: "maximal curvature κ_max ≤ 1/τ" es automático (thick ≤ minRad, l. 74); decir "(automatic)".
- m4. l. 133–135, Remark sobre el término p|α|r: "is needed" se lee como necesidad numérica; la cota sin ese término también se cumple en los 36 niveles (cociente mínimo cota/L = 1.255, `analysis.out`). Escribir "needed for the proof via (5); numerically the bound without it also holds in all levels".
- m5. l. 146–147: la frase "the antipodal pair (p=2) is a local minimum of the strand distance exactly when h ≥ r" es correcta (verificada: d² = 4r²cos²(qu/4) + v²u², mínimo local sii v ≥ rq/2 ⇔ h ≥ r) pero no dice de qué paso h se trata en la familia; para d = 1 el paso relevante en el ecuador interior es (1 − r)p/q.
- m6. l. 188–189: "consistent with the crossover 1 − f ≈ cf in (8)": con c = 1/2 el cruce de γ está en f = 2/3, no en 0.5; con c = 1 sí está en 0.5. Quitar la frase o usar c = 1.
- m7. l. 184, (C1) "less than 1 %": el umbral no está en PLAN.md (que solo dice "convergence check in N (N and 2N) at d = 1, 2"); decir que el umbral y la extensión a d = 3 se fijaron al escribir el manuscrito. Lo mismo para (C4) (τ_pt no aparece en el PLAN).
- m8. l. 72–73: la fórmula de LSDR se atribuye a curvas C² "(see [CKS2002] for the C^{1,1} case)"; correcto, pero la sección usa después K C^∞; unificar.
- m9. l. 74: "Rop(K) ≥ 2π … with equality only for the circle": citar Fenchel (1929) o decir "by Fenchel's theorem".
- m10. l. 93–95 (medidas poligonales): decir explícitamente que el test de mínimo local podría omitir pares doblemente críticos de tipo silla y que τ_pt (sin test de criticidad) es la salvaguarda; añadir el contraste segmento–segmento (hecho aquí: min dist. entre segmentos con separación de índice > 100 / dcsd de vértices = 0.99994–0.999997 en d = 1, 0.99973 en d = 2, N = 1024).
- m11. Tabla 1: las filas f = 0.6 están fuera de la hipótesis r ≤ τ/2 (declarado en l. 182) pero la tabla no lo marca; añadir nota al pie o separar.
- m12. Tabla 4: las cadenas teórica y numérica difieren mucho en r_d (teórica f = 1/2: 0.5, 0.125, 0.031 frente a 0.5, 0.208, 0.104); la comparación "indicativa" (caption) aporta poco; pasar a una frase.
- m13. Figura 1: tres proyecciones xy no muestran la estructura 3D; reducir a 0.6\textwidth o eliminar.
- m14. Apéndice: caja desbordada de 17 pt (declarada en CONTINUIDAD); añadir `\sloppy` local o cortar la línea de nombres de archivo.
- m15. `refs.bib`: `Rawdon2003` y `Chern1967` no se citan; eliminar o citar (Rawdon es pertinente en l. 93–95 para el grosor poligonal). Añadir DOI a Pierański (10.12921/cmst.1998.04.01.09-23) y a CKS (10.1007/s00222-002-0234-y).
- m16. l. 172–174: "the best known numerical ropelength is about 32.7 [Pieranski1998, CKS2002]": CKS citan 32.66; valores posteriores más precisos (≈ 32.74, Ashton–Cantarella–Piatek–Rawdon 2011) existen; o citar uno de ellos o escribir "≈ 32.7 (numerical, uncertified)".
- m17. `make_numbers.py:36–37`: `MetaMinutes` se construye a partir de `seconds` (pared) y se imprime como "CPU-minutes" (M6); corregir el texto, no el script.

Estadística: no aplica (cálculo determinista sin intervalos ni tests). Alcance frente a la ficha pública: coherente, salvo "hipótesis local" (M1) y "writhe del trébol" (M3); la FICHA no afirma aplicaciones ni resultados sobre poblaciones.

## Bibliografía

Red: `api.crossref.org` bloqueado por el proxy (403, también vía WebFetch); solo fue posible WebSearch. "Coherente" = los campos coinciden con el conocimiento del árbitro pero no se verificaron en línea en esta sesión.

| Entrada | Estado | Corrección / nota |
|---|---|---|
| BuckSimon1999 | verificada (WebSearch: Topology Appl. 91(3), 245–257, 1999) | — |
| CKS2002 | verificada (Invent. Math. 150, 257–286, 2002; DOI 10.1007/s00222-002-0234-y) | respalda existencia/regularidad C^{1,1} y cotas por conos; menciona trébol ≈ 32.66 |
| LSDR1999 | verificada (Topology Appl. 91(3), 233–244, 1999) | respalda ec. (1) para C² |
| GonzalezMaddocks1999 | coherente, no verificada en línea | PNAS 96(9), 4769–4773 |
| Bishop1975 | coherente, no verificada en línea | Amer. Math. Monthly 82(3), 246–251 |
| Calugareanu1961 | coherente, no verificada en línea | Czechoslovak Math. J. 11(86), 588–625 |
| White1969 | coherente, no verificada en línea | Amer. J. Math. 91(3), 693–728 |
| Fuller1971 | coherente, no verificada en línea | PNAS 68(4), 815–819 |
| Lickorish1997 | entrada correcta (GTM 175); **cita "[Ch. 1]" para la definición de cable (p, q+pn) no verificable** | hacer la convención autocontenida o citar Rolfsen, *Knots and Links*, §4D |
| Pieranski1998 | **verificada** (cmst.eu: Comput. Methods Sci. Technol. 4, 9–23, 1998) | añadir DOI 10.12921/cmst.1998.04.01.09-23 |
| Rawdon2003 | no citada en el texto; datos coherentes (Experiment. Math. 12(3), 287–302) | citar en §2.4 o eliminar |
| Chern1967 | no citada; coherente | eliminar |

Resumen: 4 verificadas, 0 corregidas, 7 coherentes/no verificables (1 cita de capítulo no verificable), 2 sin uso.

## Verificación computacional

- **Reproducción rápida** (copia de `recursive_knots.py` en el scratchpad, `--fast`, un hilo): 53.5 s de pared, 34.7 s user + 18.4 s sys. Cadenas comunes con `results/results.json` (N₀ = 512 para (2,3) y (2,5); 256 para (3,2)): diferencia relativa máxima **0** en L, τ, Rop, Wr, minRad, dcsd, τ_pt, α, Lk, slope, ρ_pred, L_bound. Las cadenas a media resolución (N₀ = 256; 128 para (3,2)) difieren de las finas publicadas en ≤ 0.05 % ((3,2) d = 3: 2295.4 frente a 2296.46). Una corrida anterior en el mismo scratchpad (91.6 s pared, 51 s user, multihilo) dio el mismo resultado.
- **Macros vs JSON** (`check_macros.py`): 72 macros muestreadas (Rop, τ, Wr, α, slope, L de los 12 niveles por defecto a N₀ = 1024): 0 discrepancias. Tablas 1–4 coinciden con `tables.md`. `results_shrink.json` coincide con las macros `Shrink*` y con `tables_shrink.md`.
- **Consistencia CWF** (`check_macros.py`): max |Wr_{d−1} − α_d/2π − n| = 1.1·10⁻³ (fina), 4.5·10⁻³ ((3,2) N₀ = 256 d = 3); con signo opuesto no hay enteros. Signo del Lema 3.2 confirmado.
- **(H_c) con c = 1** (`verif2.py`): falla en 4 de 15 niveles (f ≤ 1/2, fina); con c = 1/2 margen mínimo 1.129 ((2,5) d = 1), 1.663 en la familia por defecto. minRad/r_d ≥ 1.147 en 36/36 niveles.
- **Par crítico** (`verif2.py`, `analysis.out`): f = 0.5 d = 1: separación de bases 104.1°, distancia de bases 1.577, radio cilíndrico 0.511, z = ±0.104; f = 0.25/0.35: par antipodal del mismo disco. (2,5) f = 0.5: 65.4°; (3,2) f = 0.5: 20.4°, dcsd = 0.838 < s = 0.866.
- **Posible sobreestimación de τ por el proxy de vértices:** distancia mínima segmento–segmento (separación de índice > 100) / dcsd de vértices = 0.99994 (f = 0.25), 0.999997 (f = 0.5), 0.999996 (f = 0.6) en d = 1 y 0.99973 en d = 2 (N = 1024). Curva analítica T(2,3), r = 0.5, remuestreada con n = 16384: τ = 0.41582, Rop = 38.356 (iguales a 5 cifras). Sin sobreestimación relevante.
- **Writhe:** Wr(K₁; r) = 3.0009 (r = 0.02) … 3.5182 (r = 0.5); cruce de 3.5 en r* ≈ 0.4904; Wr(r = 0.5, N₀ = 2048) = 3.51823. Diferencias grueso/fino: hasta 0.031 ((3,2) d = 3).
- **Cota de longitud sin el término de giro:** se cumple en 36/36 (cociente mínimo 1.255).
- **Cocientes Rop_d/Rop_{d−1}:** 8.559/8.007/8.000 (f = 0.25), 6.489/5.728/5.715 (0.35), 6.105/4.056/4.002 (0.5), 7.594/6.946/6.929 ((3,2)), 11.517/4.027/4.002 ((2,5)): tienden a p/f (o p/(f sin(π/p)) cuando el par crítico es de hebras adyacentes).
- Presupuesto usado: ≈ 1.5 min de CPU en esta sesión (más ≈ 2.5 min de la sesión previa en el mismo scratchpad).

## Recortes propuestos (el PDF tiene 10 páginas; objetivo ≤ 10 tras incorporar las correcciones)
1. Tabla 3 (convergencia, 18 filas) → `results/tables.md`; dejar una frase con el cambio relativo máximo (ya existe como macro).
2. Fusionar Tablas 1 y 2 (mismas columnas) y eliminar las columnas minRad y dcsd/2 de la Tabla 1 (minRad nunca fija τ: una frase basta).
3. Tabla 4 → una frase (M12).
4. Figura 1 → 0.6\textwidth o eliminar; Figura 2 basta.
5. Fusionar §6 Limitaciones y §7 Next steps en una sección con dos listas; eliminar las repeticiones con el párrafo l. 146–147.
6. Reducir el párrafo de la sonda de acortamiento (l. 191) a tres líneas; los detalles están en `tables_shrink.md`.
7. Mover el párrafo "Protocol" (l. 182) al apéndice de reproducibilidad, que ya repite la mitad.

## Lista de acciones (por prioridad)
1. Reenunciar (H_c) como hipótesis sobre la familia recursiva (o añadir hipótesis explícitas de paso h = |K'|p/q ≥ r y de cota de κ'), y corregir resumen, status del Corolario, tabla de afirmaciones y FICHA (B1).
2. Sustituir "exactly one level" / "one default level" / "falla exactamente en un nivel" por "4 de 15 niveles con f ≤ 1/2, con igualdad en (3,2) d = 2, 3" en l. 155, 186, 244, README y CONTINUIDAD (B2).
3. Retitular "Predefined criteria" y declarar que c = 1/2 se fijó tras fallar c = 1; presentar (H_c) con c = 1 y la tabla de cocientes observados (B2).
4. Reescribir l. 146–147, Limitaciones (1), resumen y FICHA: el caso no cubierto es "distancia de bases < 2τ", incluye pares globales, y en f = 1/2, d = 1 es el par a través del agujero (M1).
5. Reorientar Next steps (1) hacia el cálculo explícito de la distancia entre hebras de T(p,q) sobre el toro (1, r) en d = 1 (M1).
6. Añadir la Proposición thick(K_d) ≤ r_d (p = 2) y L(K_d) ≥ pL(K_{d−1})(1 − r_dκ_max); reducir la Conjetura 3.9 a "thick(K_d) = r_d para f pequeño" y presentar Λ_* = p/f como consecuencia (M2).
7. Enunciar el Lema 3.2 como Lk = Wr − α/2π (válido en α = π); calcular `n_frame = rint(Wr − α/2π)` y reportar el residuo máximo como macro (M3).
8. Hacer autocontenida la convención de cable (p longitudinal, q meridional respecto al marco de Seifert) o cambiar la cita de Lickorish por una verificada (M3, Bibliografía).
9. Corregir la precisión declarada del writhe (≤ 10⁻⁴ en d = 1 por defecto, hasta 3·10⁻² en (3,2) d = 3) o implementar el writhe poligonal exacto (M4).
10. Reescribir el Corolario 3.6 con ρ_d := γρ_{d−1} y (H_c) para todo r ≤ fτ (M5).
11. Corregir "9 páginas" → 10, "CPU-minutes" → "wall time", y la frase de la sonda en d = 2 (M6).
12. Corregir ec. (2) con los coeficientes del marco girado (m1) y enunciar el Lema 3.1 con r < τ (m2).
13. Matizar la Remark del término de giro (m4) y eliminar o corregir la frase del "crossover" (m6).
14. Declarar que el umbral 1 % de (C1), la extensión a d = 3 y (C4) no estaban en PLAN.md (m7).
15. Añadir en §2.4 la salvaguarda τ_pt frente a pares de tipo silla y el contraste segmento–segmento (m10).
16. Marcar f = 0.6 en la Tabla 1 como fuera de hipótesis (m11); aplicar los recortes 1–7.
17. Limpiar `refs.bib` (quitar Rawdon2003/Chern1967 o citarlos; añadir DOIs) y precisar la cita del 32.7 (m15, m16).
18. Cambiar en la FICHA "hipótesis local" → "hipótesis sobre el grosor del nivel siguiente" y "writhe del trébol" → "writhe de la configuración de profundidad 1" (M1, M3).
