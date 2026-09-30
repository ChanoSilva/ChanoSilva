# OMR001 — Continuidad interna, 30/09/2026

Documento de trabajo interno. No incorporar al manuscrito ni a entregas institucionales.

## Proyecto y alcance
Línea OMR001, "Correcciones transferibles entre tareas de estimación" / "Transferable corrections across estimation tasks", área Estadística y medición, estado en el CV web: en pausa. Ficha pública: propuesta de operadores de corrección post-estimación con opción de revertir a una referencia segura; objetivo: evaluar correcciones en tareas retenidas y establecer condiciones de transferencia; hallazgo: no se ha demostrado diferenciación suficiente frente a combinaciones de modelos y correcciones basadas en operadores ya existentes; alcance: no se afirma mejora general de exactitud ni garantía de transferencia.

Pedido de la sesión (brief común, segunda tanda): formalizar "corrección con reversión segura", demostrar qué garantía puede y no puede tener, y hacer una simulación pequeña con criterio predefinido.

## Supuesto central (verificar con el autor)
No existe manuscrito previo ni definición original de los operadores ni de la "referencia segura". Todo lo que sigue es una **reconstrucción autónoma** a partir de la ficha:
- **Modelo:** localización gaussiana en $d$ coordenadas con varianza conocida. Se eligió porque en él todo es explícito (riesgo minimax, admisibilidad, distribución exacta del chequeo). Si los operadores originales actuaban sobre coeficientes de regresión, el mismo análisis aplica al vector de coeficientes con covarianza conocida; no se hizo.
- **Referencia segura:** la media muestral de la tarea (insesgada, minimax). Se descartó una referencia sesgada (sesgo de instrumento compartido) porque la muestra retenida del objetivo tendría el mismo sesgo y el chequeo no podría ver la corrección; ese caso requiere datos de calibración y queda fuera.
- **Operador de corrección:** afín, $C=\hat\mu+\lambda(R-\hat\mu)$, con $(\hat\mu,\lambda)$ estimados en las tareas fuente (regla de Bayes empírico de Efron–Morris por momentos), o $\lambda$ fijo, o $\lambda=0$ (agrupamiento total). Es la familia más natural de "corrección aprendida entre tareas"; una corrección aditiva fija también aparece (Teorema A(b) y Proposición de optimalidad).
- **Reversión:** test unilateral de nivel $\alpha$ sobre la diferencia de pérdidas en una muestra retenida independiente de tamaño $m$; $\alpha=1/2$ es la selección por muestra retenida sin margen.
- **Estructura compartida:** modelo jerárquico $\theta_t\sim N(\mu,\tau^2 I)$, con intensidad $\mathrm{snr}=\tau^2/(\sigma^2/n_e)$; la violación de la estructura se modela desplazando el centro del objetivo $\kappa\tau$ en una coordenada.

## Qué se produjo (todo en `papers/OMR001-transferable-corrections/`)
1. Manuscrito LaTeX (inglés, 13 páginas) con 1 teorema de imposibilidad (4 partes), 1 lema, 1 teorema de garantía (4 partes), 1 corolario, 1 proposición de optimalidad de la constante, 1 proposición de equivalencia con selección penalizada, 3 observaciones, 7 tablas generadas, 3 figuras, tabla de afirmaciones con estado, apéndice de reproducibilidad. Bibliografía de 18 entradas reales. Compilado a `main.pdf` sin errores ni referencias indefinidas.
2. `experiments/safe_reversion.py` (semilla fija, ~17 s) y `experiments/make_numbers.py`; cada número del texto es una macro generada.
3. README, esta nota y una propuesta de ficha.

## Resultados matemáticos (estado)
- **Teorema A (no free lunch).** (a) Ningún estimador que use datos fuente cuya ley no dependa de $\theta$ baja el riesgo minimax $d\sigma_e^2$ [clásico; demostración incluida vía riesgo de Bayes con prior $N(0,\tau^2 I)$ y $\tau\to\infty$]. (b) Una corrección aditiva fija $X-b(D)$ tiene riesgo $d\sigma_e^2+E\|b\|^2$ en todo $\theta$ [demostrado]. (c) Para $d\le2$, toda regla que difiera de $X$ con probabilidad positiva es peor que $d\sigma_e^2$ en algún $\theta$ [admisibilidad de Blyth 1951 / Stein 1956 + argumento de convexidad estricta y Rao–Blackwell sobre la aleatorización $D$; demostrado]. (d) James–Stein para $d\ge3$ [literatura].
- **Lema 1.** $\hat D-\Delta=-2\langle C-R,\bar Y-\theta\rangle$; condicionalmente $\hat D\sim N(\Delta,s^2)$ con $s=2\sigma\|C-R\|/\sqrt m$ [demostrado].
- **Teorema B (do no harm).** (i) $\mathcal R(\hat\theta_{\rm rev})-\mathcal R(R)=E[\Delta\pi]$ (identidad exacta). (ii) $\le\min\{\alpha E\Delta^+,\ \varphi(z_{1-\alpha})\,2\sigma E\|C-R\|/\sqrt m\}$ y $P(\text{usa }C,\ \Delta>0)\le\alpha P(\Delta>0)$ [Mills ratio; demostrado]. (iii) Versión Hoeffding para observaciones acotadas: $2\rho E\|C-R\|/\sqrt{em}$ [demostrado]. (iv) Regret frente al mejor candidato $\le(z_{1-\alpha}+\varphi(0))\,2\sigma E\|C-R\|/\sqrt m$ [demostrado].
- **Corolario (precio de la partición).** Frente a la media con todos los datos se paga además $d\sigma^2 m/(n n_e)$, fracción $m/n_e$ del riesgo de referencia [aritmética].
- **Proposición (optimalidad).** $\kappa(\alpha)=\sup_u u\Phi(-(z+u))\le\varphi(z)$ y existe un par $(R,C)$ (corrección aditiva fija, $n_e\to\infty$) que alcanza $(\kappa(\alpha)-\varepsilon)\,2\sigma E\|C-R\|/\sqrt m$; el daño no es $o(m^{-1/2})$ uniformemente en operadores [demostrado; $\kappa/\varphi$ = 0.43, 0.16, 0.11, 0.08, 0.05 para $\alpha$ = 0.5, 0.2, 0.1, 0.05, 0.01, calculado].
- **Proposición (equivalencia).** $\hat\theta_{\rm rev}=\arg\min_{\delta\in\{R,C\}}\{\hat L_m(\delta)+c\,1\{\delta=C\}\}$ [una línea]. Consecuencia: la garantía es de selección (caso $K=2$ de las cotas de hold-out), indiferente a cómo se obtuvo el operador; la ganancia es solo cuestión de estructura compartida y de detectabilidad (potencia $\Phi(-z+|\Delta|/s)$, independiente de $d$ en el ejemplo de desplazamiento).
- **Observaciones no demostradas en detalle:** test $t$ con $\sigma$ desconocida (la forma $\alpha$ se mantiene por monotonía de la potencia; se cita Lehmann–Romano), versión Chebyshev, y que nada usa que $C$ sea función de $R$.

## Resultados de referencia (semilla 20260930, $R=20\,000$, $d=5$, $S=30$, $n_s=60$, $n=60$, $m=12$, $\sigma=1$)
- Referencia con todos los datos $\bar X_n$: 0.0833; con la muestra de estimación $R$: ≈0.104 (costo de partición 25 %).
- Barrido de estructura (objetivo dentro de la jerarquía), ganancia relativa a $\bar X_n$: corregir siempre (todos los datos) +96 % (snr 0), +42 % (snr 1), +16 % (snr 4), +4 % (snr 16). Reversión con garantía, $\alpha=0.5$: +65, +22, −4, −17 %; $\alpha=0.1$: +8, −7, −17, −22 %; $\alpha=0.01$: −20 … −25 %. Reajuste tras chequeo ($\alpha=0.1$): +16, +6, +2.5, +0.6 %. SURE: +79, +33, +13, +3 %. Criterio U (≥5 % con IC 95 %): siempre: snr ≤ 8; rev 0.5: ≤ 2; rev 0.2: ≤ 0.5; rev 0.1: solo 0; rev ≤0.05: nunca; refit 0.1: ≤ 1; SURE: ≤ 8.
- Barrido de desviación (snr = 1, desplazamiento $\kappa\tau$): corregir siempre es dañino desde $\kappa=4$ (1.41× la referencia) y llega a 13.8× en $\kappa=16$. Reversión $\alpha=0.1$: entre 1.07× y 1.30× de $\bar X_n$; exceso sobre $R$ en $\kappa=8$: +0.0042 ± 0.0003 frente a cotas 0.0044 (identidad), 0.063 ($\varphi$), 0.030 ($\alpha$). Frecuencia de eventos dañinos máxima: 25.3 % ($\alpha=0.5$), 7.7 % (0.2), 3.4 % (0.1), 1.5 % (0.05), 0.25 % (0.01); frecuencia condicional de usar $C$ cuando daña ≤ $\alpha$ siempre (máx. 8.4 % con $\alpha=0.1$).
- Tamaño retenido ($\alpha=0.1$, snr 1): $m=3$: +3.6 % ($\kappa=0$) / −18 % ($\kappa=8$), exceso +0.010 frente a cota 0.116; $m=6$: +0.8 / −20 %; $m=12$: −6.5 / −30 %; $m=24$: −29 / −68 %.
- Otros operadores ($\alpha=0.1$): agrupamiento total en snr 16 pasa de riesgo 1.73 (99.5 % de casos dañinos) a 0.106 (0.4 %) con reversión; $\lambda$ fijo de 0.46 a 0.107.
- Verificaciones: 345 combinaciones, todas las cotas se cumplen (máx. exceso/cota $\varphi$ = 0.42; máx. regret/cota = 0.42). Identidad: 273 combinaciones con $z$ pareado ($|z|_{\max}$ 2.96), 72 con conteo de Poisson, 2 fuera del 99 % (mismo lote: pooling, $\alpha=0.05$, $m=6$, $\kappa=8$: 26 aceptaciones frente a 48 esperadas); re-simulación con 50 semillas: 2488 frente a 2426, $z=+1.27$; chequeo condicional directo con 200 000 sorteos: $|z|_{\max}=1.72$.
- Tiempo total de cómputo: ≈17 s (más ≈30 s de pruebas ad hoc durante el desarrollo).

## Decisiones tomadas
- Un solo modelo (gaussiano de localización) y una sola familia estructural (jerárquica), para que todo sea demostrable y las tablas legibles; se descartó un segundo diseño con sesgo de instrumento por la razón dada arriba.
- Las comparaciones prácticas se hacen contra la media con **todos** los datos (la referencia natural de "no hacer nada"), cargando la partición al método; la comparación teórica (Teorema B) es contra la referencia de la muestra de estimación. Ambas se reportan.
- Criterio U fijado antes de mirar resultados: ganancia relativa ≥ 5 % con extremo inferior del IC 95 % (pareado).
- Se incluyeron dos variantes sin garantía (reajuste tras chequeo; reversión por SURE) porque son las que un practicante usaría y porque muestran que la ganancia práctica está en construcciones clásicas; se marcan explícitamente como empíricas.
- La verificación de la identidad en régimen de eventos raros usa un intervalo de Poisson en lugar del test $z$ (el TCL no aplica); la primera versión del script daba $|z|$ enormes por esa razón, no por un error en la identidad.

## Revisión adversarial propia (antes de cerrar)
- Se eliminó del resumen cualquier lectura de "el método es útil": el texto dice que la garantía es de selección, que la utilidad ocurre solo con tareas casi idénticas en este diseño y que las variantes útiles no tienen garantía aquí.
- Teorema A(c): se añadió el paso de Rao–Blackwell sobre $D$ para que la admisibilidad (enunciada para estimadores de $X$) cubra estimadores $\delta(X,D)$.
- Proposición de optimalidad: se exige $n_e\to\infty$ y se usa convergencia en $L^2$ + continuidad con $|g(x)|\le|x|$; el enunciado es "para todo $\varepsilon$ existe", no "se alcanza".
- Teorema B(iii): constantes de Hoeffding recalculadas (rango $2B$, exponente $mt^2/(2B^2)$).
- Tabla de constructos: James–Stein de parte positiva revierte hacia el *objetivo del encogimiento*, no hacia la referencia; se dice explícitamente.
- Citas: solo obras que se conocen con certeza. Duda menor: paginación de Li–Cai–Li (JRSSB 84(1), 2022) tomada de memoria; verificar antes de enviar. La atribución de la admisibilidad en $d=1$ a Blyth (1951) y en $d=2$ a Stein (1956) sigue a Lehmann–Casella.

## Pendientes y próximos pasos concretos
1. Confirmar con el autor si existen definiciones originales de los operadores; si existen, ubicarlas en la tabla de constructos y calcular $E\|C-R\|$ (es todo lo que necesita el análisis de seguridad).
2. Demostrar una cota finita para la variante con reajuste (o una versión con cross-fitting): ahí se recuperaría el costo de la partición con garantía.
3. Cota de selección para la reversión por SURE con operador afín (región de aceptación esférica; el riesgo no es SURE por la discontinuidad).
4. Extender el Lema 1 y el Teorema B al test $t$ (forma $\varphi$) y a covarianza desconocida.
5. Decidir si la línea se cierra con esta nota (recomendación: sí, salvo que 2–3 den algo nuevo) y actualizar la ficha del CV web según `FICHA_OMR001_propuesta.md`.
