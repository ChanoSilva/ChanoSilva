[EN CURSO]

# Informe de arbitraje interno independiente — SVMF001, ronda 3 (v0.4, commit 7e03402)

Árbitro: agente independiente (no participó en rondas anteriores ni en la teoría v0.4). Fecha: 03/10/2026.
Trabajo auxiliar: `scratchpad/referee3_SVMF001/` (fuera del repositorio).

## Veredicto

(pendiente)

## 0. Teoremas nuevos v0.4 (prioridad máxima)

(en curso)

### 0.1 Lectura paso a paso (notas de trabajo; se consolidan en los hallazgos)

- **Prop. 3.6 (prop:select)** (main.tex:158–169). Correcta. El bloque B=((X_i,Y_i)_{i≤n},(X,Y)) es independiente de G=σ(W_1..W_n,W,U) por la estructura producto; {I=J}∈G para cada J (ι medible en el conjunto potencia, discreto); la suma finita Σ_J 1{I=J}·P(A(S_J)(X)≠Y | G) es legítima; la independencia B⊥G da R_A(|J|). Requisitos implícitos que el enunciado no dice: (a) medibilidad conjunta de (S,x)↦A(S)(x); (b) si A es aleatorizado, su aleatoriedad debe ser independiente de todo y estar incluida en la definición de R_A (no en U); (c) "in any metric" sobre un espacio medible arbitrario no garantiza que la selección kNN sea medible (pedir métrica medible, p. ej. en R^p). Menores.
- **Lema 3.8 (lem:radius)** (main.tex:177–179; prueba 365–367). Correcto con la hipótesis "la ley de ‖X−x‖ no tiene átomos" (en ese x). Es el argumento clásico de estadísticos de orden.
- **Lema 3.9 (lem:popsign)** (181–186). Correcto (g impar y estrictamente creciente; x−t_r(x)=½[g(μ+x)−g(μ−x)]).
- **Lema 3.10 (lem:majority)** (190–192; prueba 369–371). Correcto para minimizadores exactos del objetivo ½‖w‖²+CΣhinge con sesgo sin penalizar, que es el de libsvm/`SVC(kernel="linear")` usado en `families.py:45–46,117–118` (no `LinearSVC`, que penaliza el intercepto). Cada desigualdad comprobada: F(ŵ,b̂')≤F(0,0)=Ck ⇒ ‖ŵ‖≤√(2Ck); F≤F(0,1)=2Cn₋; cota inferior por Lipschitz; Σh(y_jb')≥k para b'≤0.
- **Teorema 3.11** (194–208; prueba 373–379). (i) El paso al límite es por convergencia dominada con convergencia puntual de π_n(x) para todo x (no se necesita uniformidad en x: el integrando está acotado por 1). R_n→0 en probabilidad para cada x porque f>0; τ(r)→0 por continuidad y positividad de f en x. Frontera η=½ (x₁=0): conjunto de medida nula; allí el integrando es 0. P(S=0)=0 porque una vecindad mixta tiene k≥2 y hay al menos un punto interior con primera coordenada continua (para m=1 el punto frontera es ±1, discreto, pero no se necesita). El álgebra (a−½)(1−a^k+b^k) y la monotonía en k≥2 están verificadas a mano. (ii) Solo usa R_n<r₀ ⇒ voto mayoritario (Lema 3.10) y el acoplamiento de etiquetas; no necesita Lema 3.8. La extensión a entradas estandarizadas es correcta: radio estandarizado ≤ R_n/min σ̂_l y desplazamientos originales ≤ max σ̂_l·R_n^std.
