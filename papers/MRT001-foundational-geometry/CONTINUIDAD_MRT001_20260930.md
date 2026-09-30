# MRT001 — Continuidad interna, 30/09/2026

Documento de trabajo interno. No incorporar al manuscrito ni a entregas institucionales.

## Proyecto y alcance
Línea MRT001, "Invariantes y fundamentos geométricos" / "Invariants and geometric foundations", área Matemáticas y estructuras, estado en el CV web: "En pausa — Desarrollo conceptual suspendido". Objetivo declarado en la ficha: precisar qué afirmaciones pueden formularse y contrastarse dentro de marcos matemáticos definidos. Alcance declarado: sin teoría física contrastada; no se presenta como teoría unificada ni como evidencia experimental.

Pedido del usuario en la sesión de Claude Code (session_01MTmjU2K8b4sgpjjL3JTtDz, repositorio ChanoSilva/ChanoSilva, rama `claude/charming-pasteur-2cajqb`): "Seguir con el Paper: Foundational Geometry", luego "sigamos todo … con todo".

## Supuesto central (verificar con el autor)
No se encontró ningún manuscrito previo titulado "Foundational Geometry". Se asumió que el paper corresponde a la línea MRT001 y se redactó un **borrador nuevo desde cero** a partir de la ficha del CV. Si existe un manuscrito anterior (en la Biblioteca de ChatGPT, en un chat de Claude.ai o en archivos locales), este borrador debe fusionarse con él, no reemplazarlo.

## Dónde se buscó el manuscrito original (sin éxito)
- GitHub: `ChanoSilva/ChanoSilva` y `ChanoSilva/Colab`, ambos vacíos en el remoto. Resto de repositorios: forks o tesis 2015–2020.
- Google Drive: título y texto completo ("Foundational Geometry", "Geometr", "invariantes", "fundamentos geométricos", `.tex`, `.bib`, Google Docs y Markdown recientes, carpetas de papers). Único hallazgo relacionado: la ficha MRT001 en `CV_Web/investigacion.html` (Drive) y en el sitio publicado `luciano-silva-alarco.luxian80.chatgpt.site`.
- Artifacts, Claude Docs y sesiones previas de Claude Code: ninguno.
- Web (arXiv, Zenodo, SSRN): nada con ese título a nombre del autor.
- Gmail: el conector exigía reautorización; no se pudo revisar correo.
- Observación: en Drive existe `Information.txt` con datos personales de cuentas al alcance del conector; no se usó ni se copió.

## Qué se produjo (todo en `papers/MRT001-foundational-geometry/`)
1. Manuscrito LaTeX `manuscript/main.tex` (inglés, ~13 páginas) con bibliografía real de 34 entradas (`refs.bib`), compilado a `main.pdf`.
2. Dos scripts de experimentos con semilla fija y salida JSON/Markdown, más `make_numbers.py`, que inyecta cada número del texto como macro LaTeX. Ningún número del paper está escrito a mano.
3. Este README y esta nota.

## Resultados de referencia (corrida completa, semilla 20260930)
- E1 (aritmética exacta int64, rejilla 2^30): 0 instancias de betweenness y 0 de congruencia en 4000 configuraciones aleatorias (n ∈ {5,10,20,50}, d ∈ {2,3}); rejillas enteras 3×3/4×4/5×5: 8/44/152 betweenness y 138/976/4242 congruencias.
- E2 (MDS no métrico sobre rangos + Procrustes): disparidad mediana en el plano 8.6e-3 (n=8) → 2.7e-8 (n=256); en el espacio 4.3e-2 (n=8) → 2.2e-7 (n=128). E2b: distorsión monótona D^p deja idéntica la reconstrucción ordinal y cambia la métrica (disparidad mediana 0.045).
- E3: en la recta, 4 puntos realizan 120 de los 720 órdenes de sus 6 distancias; en el plano y el espacio, los 720. Ejemplos: {0,1,3} vs {0,1,2.5}; triángulos (3,4,5) vs (3,4,6).
- E4 (300 ensayos, n=30): MST, grafo k-NN, grafo de vecindad relativa y par diametral invariantes bajo distorsión monótona (fracción 1.00); diámetro (0.00), dimensión afín (0.35) y grafo de Gabriel (0.03) no.
- E5a: 200/200 reparametrizaciones conformes (que cambian los tiempos propios en una mediana del 23%) y 200/200 boosts preservan el orden; la rotación euclidiana cambia la relación de ~20% de los pares.
- E5b: fracción de pares comparables 0.499/0.230/0.101 frente a 0.500/0.229/0.100 esperado (D=2,3,4); estimación de dimensión 2.00±0.05, 3.00±0.09, 4.00±0.14.
- E5c: correlación L–τ 0.967 (n=250) → 0.990 (n=2000); pendiente L/(√n τ) 1.73 → 1.85 (límite 2); error relativo mediano de τ̂ (τ>1/4) 14% → 8% frente a τ, pero 23% → 17% frente al τ' de la configuración reparametrizada (el conteo fija el factor conforme).
- E5d: RMSE de coordenadas 0.073 (n=250) → 0.031 (n=2000); RMSE·√n entre 1.15 y 1.40; desacuerdo de orden 7.7% → 3.7%.

## Decisiones tomadas
- Objetos etiquetados en todos los formalismos (sin cociente por reetiquetado), para mantener las demostraciones elementales.
- E1 con aritmética exacta y no con tolerancia flotante: la tolerancia 1e-9 produce ~1 triple espurio por configuración en n=50 (la brecha de betweenness es cuadrática en la distancia a la recta). Se menciona en el texto como advertencia metodológica.
- Cadena lorentziana solo en 1+1 y fondo plano, presentada como modelo matemático; la sección deja explícito qué no se afirma.
- Idioma del manuscrito: inglés (los títulos de la línea en el CV están en inglés); README y nota de continuidad en español.

## Pendientes y próximos pasos sugeridos
1. Confirmar con el autor la identificación paper ≡ MRT001 y si existe un manuscrito previo que deba integrarse.
2. Revisión del autor de las Proposiciones 3.2, 3.4 y 5.1 y de la redacción del Teorema 3.5 (enunciado informal de Kleindessner–von Luxburg; cotejar con el enunciado exacto del artículo).
3. Cota finita para el diámetro de las clases ordinales bajo muestreo uniforme (explicaría la caída ~n^-3.6 observada en E2).
4. Extender E5d a 2+1 dimensiones (grupo conforme finito-dimensional) y a densidades no uniformes.
5. Decidir destino: arXiv (math.MG / math.HO) o revista; ajustar formato.
6. Actualizar la ficha MRT001 del CV web: de "En pausa" a "En desarrollo — borrador v0.1".
