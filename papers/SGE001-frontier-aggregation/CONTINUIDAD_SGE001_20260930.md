# SGE001 — Continuidad interna, 30/09/2026

Documento de trabajo interno. No incorporar al manuscrito ni a entregas institucionales.

## Proyecto y alcance
Línea SGE001, "Agregación dinámica de fronteras productivas" / "Dynamic aggregation of production frontiers", área Estadística y medición, estado en el CV web: "En pausa". Ficha pública: estudio de momentos superiores y aproximaciones de segundo orden en fronteras productivas jerárquicas; objetivo: reducir errores de agregación y evaluar su impacto en comparaciones y decisiones; hallazgos: las aproximaciones mejoran en regímenes suaves pero pueden fallar en cruces de umbral, y una calibración posterior tampoco cumplió el criterio predefinido; alcance: no se establece una mejora certificada general para decisiones de política.

Pedido de la sesión (Claude Code, session_01MTmjU2K8b4sgpjjL3JTtDz, repositorio ChanoSilva): dar a la línea un núcleo matemático preciso y una simulación controlada, con entregables idénticos a los de MRT001, sin usar git.

## Supuestos reconstruidos (no existe manuscrito previo; verificar con el autor)
1. **Objeto matemático.** Se interpretó "agregación de fronteras productivas" como la sustitución del agregado exacto $Y=\sum_i f(x_i)$ por aproximaciones basadas en momentos de los insumos (orden 1: unidad representativa; orden 2: Hessiano × covarianza; orden 3: tercer momento), con frontera cóncava común y conocida. Es la lectura más simple compatible con "momentos superiores y aproximaciones de segundo orden".
2. **"Dinámica".** No hay dimensión temporal en la ficha. Se leyó como el comportamiento del error a lo largo de un barrido continuo de dispersión y a través de niveles jerárquicos (unidades → firmas → sector). Si el autor tenía en mente dinámica intertemporal (acumulación de capital, entrada/salida de unidades), habría que añadirla.
3. **"Jerárquica".** Dos niveles (firmas dentro de un sector), con tres estimadores de segundo orden: agrupado (pooled), ascendente (bottom-up, firma a firma) y descendente en dos etapas (top-down). Se demuestra que el descendente coincide con el agrupado (ley de covarianza total), así que solo hay dos estimadores distintos.
4. **"Cruces de umbral".** Se modelaron como una restricción de capacidad $\min(f,c)$ (quiebre de primera derivada a lo largo de una hipersuperficie). La demostración cubre cualquier quiebre de ese tipo, no cambios de régimen que alteren el nivel.
5. **"Calibración posterior".** Desconocida. Se reconstruyó como la variante más simple: reescalar el término de segundo orden, $\hat Y_\lambda=\hat Y_1+\lambda Q_2$, con $\lambda$ ajustado por mínimos cuadrados en un diseño de entrenamiento, global o por régimen de proximidad a la capacidad, y evaluado fuera de muestra. Si la calibración original era otra, E5 es solo un análogo.
6. **"Criterio predefinido".** Desconocido. Se fijaron antes de correr: C1 (mejora ≥ 5× del orden 2 sobre el orden 1, mínimo sobre réplicas, uniforme en el barrido) y C2 (en cada celda con ≥ 2 % de reversiones de orden 1, el orden 2 reduce la tasa al menos 5×).
7. **Términos de eficiencia.** Se incluyeron como $y_i=\theta_i f(x_i)$ con $\theta_i$ independientes de los insumos (Farrell), solo en un experimento (E1b) y una observación elemental (piso de covarianza).

## Qué se produjo (todo en `papers/SGE001-frontier-aggregation/`)
1. Manuscrito LaTeX `manuscript/main.tex` (inglés, ~14 páginas con 4 figuras y 6 tablas; el objetivo eran 5–10 y no se logró sin sacrificar demostraciones o tablas), bibliografía de 25 entradas (`refs.bib`), compilado a `main.pdf` sin errores ni referencias indefinidas.
2. `experiments/frontier_aggregation.py` (E0–E6, semilla 20260930, ~42 s de CPU en la corrida de referencia; `--fast` ~10 s) y `experiments/make_numbers.py` (202 macros + 7 cuerpos de tabla). Ningún número del texto está escrito a mano.
3. README y esta nota.

## Resultados matemáticos (todos con demostración completa en el manuscrito)
- Prop. 3.1: identidades de resto (Lagrange e integral) para $E_1$ y $E_2$; cotas $B_1=\tfrac12\sum_i M_2^{(i)}\|h_i\|^2$, $B_2=\tfrac16\sum_i M_3^{(i)}\|h_i\|^3$ con supremos por segmento; versión con módulo de continuidad del Hessiano (solo $C^2$); si $D^2f\preceq-\lambda I$, $|E_2|/|E_1|\le M_3\rho/(3\lambda)$.
- Obs. 3.2 (heurística para las constantes, consecuencia de 3.1 para los órdenes): $E_2=O(\sigma^4)$ si los terceros momentos muestrales son nulos; para log-normales los terceros momentos son $O(\sigma^4)$, luego el orden 3 no está garantizado mejorar al orden 2.
- Obs. 3.3: constantes calculables para Cobb–Douglas (supremos en esquinas de cajas coordenadas; norma de Frobenius domina la norma de operador).
- Lema 3.4: descendente en dos etapas = agrupado; error ascendente = suma de errores intra-firma; exactitud para polinomios de grado ≤ 2.
- Lema 3.5 (identidad de bisagra): $\sum(u_i-c)_+-N(\bar u-c)_+=\min(P,Q)$.
- Prop. 3.6: $E_2(f_c)=-N T_u+E_2(f)+Q_2\mathbf 1\{f(\bar x)>c\}-N[(\bar u-c)_+-(f(\bar x)-c)_+]$ y cota bilateral $|E_2(f_c)+N T_u|\le B_2+B_1+|Q_2|\mathbf 1\{\cdot\}$.
- Cor. 3.7: con $f(\bar x)=c$ y $x_i=\bar x+\sigma z_i$, $T_u=\sigma\tau_z+O(\sigma^2)$ con $\tau_z=\tfrac1{2N}\sum|\nabla f(\bar x)\cdot z_i|$; error relativo $\Theta(\sigma)$; $|E_1|/|E_2|\to1$; $|E_2(f_c)|/|E_2(f)|\to\infty$.
- Ej. 3.9: dos poblaciones con iguales media y varianza y agregados que difieren en $(1-\sqrt2/2)\sigma$ por unidad: ningún estimador función de $(\bar x,\Sigma)$ es exacto en un cruce.
- Prop. 3.10: condición de margen $|\hat Y^A-\hat Y^B|>B^A+B^B$ ⇒ orden preservado. Ej. 3.11: reversión en frontera con quiebre (todos los órdenes) y reversión de orden 1 corregida por el orden 2 en $\sqrt x$ (números calculados en E6).
- Obs. 3.12: piso de covarianza $\mathrm{sd}(\theta)\,\mathrm{CV}_u/(\bar\theta\sqrt N)$, de orden $\sigma/\sqrt N$, con eficiencias independientes.

## Resultados de referencia (corrida completa, semilla 20260930)
- E0: derivadas analíticas frente a diferencias centrales: desviación relativa máxima 1.8×10⁻¹⁰ (CD), 1.9×10⁻⁹ (CES).
- E1 (N = 2000, 20 réplicas, σ ∈ [0.01, 1] LN / [0.01, 0.5] SU): exponentes 2.00 / 3.78 (LN) 4.00 (SU) / 4.00. C1: SU cumple en todo el barrido (mín. 5.97 CD, 5.65 CES); LN cumple hasta σ = 0.42 y en σ = 1 la razón mínima es 0.75 (CD) / 0.65 (CES). Para σ ≤ 0.2, razón mínima ≥ 34 (CD-LN), 69 (CD-SU), 33 y 63 (CES). Orden 3 peor que orden 2 (mediana) en 17/17 celdas CD-LN y 14/17 CES-LN; razón mínima 0.008. Cotas $B_2$ (segmento) y de caja única se cumplen en el 100 % de réplicas; $|E_2|/B_2\le0.020$; $B_2<|E_1|$ solo hasta σ = 0.10 (LN) / 0.12 (SU); cota de caja única hasta 7339× mayor que la de segmento.
- E1b: sd(θ)/θ̄ = 0.19; el término de covarianza domina a $e_2$ hasta σ = 0.18; en σ = 0.01 es 8.9×10³ veces mayor; su mediana es 0.70–0.86 de la sd predicha (mediana de |Z| = 0.67).
- E2 (N = 2000, 20 réplicas, δ ∈ {−0.3, −0.1, −0.03, 0, 0.03, 0.1, 0.3}, LN y SU): en δ = 0, exponente 1.00 (LN) y 1.00 (SU) frente a 3.36 / 4.00 sin capacidad; $-E_2/(NT_u)$ = 1.0000 en σ = 0.01, rango [0.85, 1.08]; amplificación 7×10⁵; razón $|E_1|/|E_2|$ = 1.00. Cota bilateral: 168/168 celdas; cota inferior informativa en 32; celdas con cruce en todas las réplicas: 107. Con δ = −0.3 el régimen es suave a σ pequeño (razón mínima 286 para σ ≤ 0.05) y cambia al de cruce cuando la cola alcanza la capacidad; con δ = −0.03 la transición cae dentro de la ventana de ajuste (pendiente transitoria 8.5).
- E3 (G = 40, n = 50, 20 réplicas): identidad descendente = agrupado a 2×10⁻¹⁶; ascendente mejor en 16/16 celdas suaves, ganancia 1.16–4005; cotas se cumplen; con capacidad, ascendente/agrupado ∈ [0.008, 0.92], firmas que cruzan 20–100 %, aporte de las que no cruzan ≤ 4.2×10⁻³.
- E4 (N = 500 por sector, 1000 pares por celda, γ ∈ ±5 %, σ_B = σ_A/2): sin capacidad rev1 hasta 45.2 %, rev2 ≤ 3.3 %; 0 reversiones entre pares certificados (orden 2 y orden 1); fracción certificada 100 % (σ = 0.02), 70.8 % (0.2), 0 % (0.4); capacidad en la media: rev1 hasta 70.1 %, rev2 28.1–65.3 %; orden 3 en σ = 0.8: 89.2 % (sobre-corrección por terceros momentos log-normales). C2: 23 celdas elegibles (3 suaves, 20 con capacidad); fallan 15, todas con capacidad.
- E5 (entrenamiento σ ∈ {0.05, 0.1, 0.2, 0.4} LN; prueba σ ∈ {0.03, 0.07, 0.15, 0.3, 0.6} LN y SU): λ global 2.68; por régimen 0.90 / 3.11 / 4.65; sobre capacidad $Q_2\equiv0$. Razones mínimas fuera de muestra (LN): orden 2 → 2.80 suave (falla en σ = 0.6), 1.35 bajo, 1.00 en; global → 0.38 / 0.59 / 1.00; por régimen → 4.65 / 0.47 / 1.00. Ninguna variante cumple C1.
- E6: quiebre: ε = 0.05, σ = 0.2 ⇒ $Y^A/N$ = 0.95 > 0.90 = $Y^B/N$, aproximación B ≻ A; raíz: δ = 0.01, σ = 0.3 ⇒ $Y^B/N$ = 0.9936 < 1, $\hat Y_1^B/N$ = 1.0050 (invertido), $\hat Y_2^B/N$ = 0.9939 (correcto).

## Decisiones tomadas
- Frontera conocida y fija (no estimada); insumos bidimensionales con correlación 0.5; dos frontera (Cobb–Douglas α = 0.3, β = 0.5; CES ρ = −1, ν = 0.8) y dos leyes (log-normal; uniforme simétrica con pares antitéticos para anular exactamente los terceros momentos muestrales y observar el exponente 4).
- Números comunes a lo largo del barrido (mismos choques para todo σ) para curvas suaves y exponentes limpios.
- Cotas: se prefirió la versión por segmento (rigurosa y más ajustada) a la de caja única; solo para Cobb–Douglas, donde los supremos tienen forma cerrada. Para CES no se certifica ninguna cota.
- Convención en $f(\bar x)=c$: rama "bajo capacidad". Solo afecta al caso de medida cero δ = 0, donde en la práctica la media muestral cae a un lado u otro.
- Criterios C1 y C2 fijados antes de las corridas (umbral 5, elegibilidad 2 %). El resultado negativo sobre C1 en LN (σ > 0.42) y sobre C2 en los cruces se reporta tal cual.
- Idioma: manuscrito en inglés; README y esta nota en español.

## Limitaciones y lo que NO se afirma
- No se afirma nada sobre sectores reales, fronteras estimadas ni política. Todo es un diseño controlado.
- Las cotas son conservadoras (factor 50–1000) porque usan el tercer momento absoluto donde el error real cancela a cuarto orden; la región certificada (σ ≤ 0.1) es mucho menor que la región donde la mejora se observa (σ ≤ 0.42).
- Los exponentes son medidos en σ ≤ 0.05 por mínimos cuadrados; el 3.78 de CD-LN es intermedio entre 3 y 4 porque el tercer momento log-normal es $O(\sigma^4)$ solo asintóticamente.
- E5 no reproduce la calibración original (desconocida); solo muestra el mecanismo por el que un reescalado de $Q_2\propto\sigma^2$ no puede absorber un error $\propto\sigma$.
- La ley de eficiencias es independiente de los insumos; con correlación, el término $C$ tendría media no nula y habría que modelarla.
- Longitud del manuscrito (~14 págs.) por encima del objetivo de 5–10.

## Bibliografía: entradas con datos que conviene cotejar
Todas las referencias son reales y conocidas, pero los siguientes detalles se escribieron de memoria y deben verificarse antes de cualquier envío: Nataf (1948) volumen/páginas (Econometrica 16(3), 232–244); van Garderen, Lee y Pesaran (2000) volumen/páginas (J. Econometrics 95(2), 285–331); Lewbel (1992) páginas (RES 59(3), 635–642); Houthakker (1955) a veces citado como 1955–56 (RES 23(1), 27–31); Cobb y Douglas (1928) número "1, Supplement"; Harris et al. (2020) y Virtanen et al. (2020) con listas de autores truncadas ("and others"). La caracterización de cada trabajo en la introducción es deliberadamente genérica.

## Pendientes y próximos pasos sugeridos
1. Confirmar con el autor las lecturas de "dinámica", "jerárquica" y "calibración" (supuestos 2, 3 y 5) y si existe algún material previo (notas, hojas de cálculo) que deba integrarse.
2. Cota más fina que explote la cancelación (tercer momento tensorial + resto de cuarto orden) para ampliar la región certificada más allá de σ ≈ 0.1.
3. Estimar $T_u$ (la brecha de Jensen de la bisagra) dentro de una familia paramétrica ajustada a $(\bar x,\Sigma)$ y probarlo fuera de familia; el Ejemplo 3.9 es el peor caso.
4. Eficiencias correlacionadas con los insumos.
5. Si la línea quiere hablar de un sector real: frontera estimada y su error muestral primero; nada de lo hecho aquí autoriza ese paso.
6. Actualizar la ficha SGE001 del CV web: de "En pausa" a "En desarrollo — borrador v0.1", manteniendo el alcance ("no se establece una mejora certificada general para decisiones de política", que ahora es un resultado con criterio y números, no una reserva).

## Propuesta de texto para la ficha (español)
- **Estado:** En desarrollo — Borrador v0.1 (manuscrito en LaTeX con simulación reproducible).
- **Objetivo:** Precisar el error de las aproximaciones de agregación basadas en momentos (unidad representativa y corrección de segundo orden) sobre una frontera cóncava común, en régimen suave y en cruces de umbral, y determinar cuándo puede certificarse el orden de dos agregados.
- **Principales hallazgos:** En régimen suave el error de segundo orden está acotado por el tercer momento absoluto de los insumos y el factor de mejora sobre la unidad representativa crece como el inverso de la dispersión (demostrado; verificado con exponentes 2 / 3.8–4 / 4). En un cruce de capacidad el error de segundo orden es igual al término de cruce $-N T_u$, lineal en la dispersión, y el orden 2 no mejora al orden 1 (demostrado; verificado a cuatro cifras). Una condición de margen certifica comparaciones; entre las certificadas no hubo reversiones, pero el certificado solo existe a dispersión baja y nunca en un cruce. El criterio predefinido de mejora uniforme ≥ 5× se cumple con insumos simétricos, falla con log-normales por encima de σ ≈ 0.4 y en los cruces; una recalibración escalar no lo restaura.
- **Alcance actual:** Frontera conocida y diseño simulado; sin datos reales ni afirmaciones de política.
