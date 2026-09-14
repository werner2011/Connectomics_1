# Graph Analysis of Example Neurons

## Cel analizy

Celem analizy było potraktowanie szkieletowej rekonstrukcji neuronu jako grafu
i zastosowanie podstawowych pojęć teorii grafów do opisu jego topologii.

Przeanalizowano trzy przykładowe neurony typu `DA1_lPN_R`
udostępniane przez bibliotekę NAVIS.

Każdy neuron reprezentowany jest jako graf:

\[
G = (V, E)
\]

gdzie:

- \(V\) — zbiór wierzchołków odpowiadających punktom rekonstrukcji neuronu,
- \(E\) — zbiór krawędzi odpowiadających połączeniom pomiędzy kolejnymi punktami szkieletu.

W analizie wykorzystano graf nieskierowany, ponieważ interesowała nas przede wszystkim
topologia drzewa neuronalnego, a nie kierunek przebiegu krawędzi.

---

## Analizowane metryki

Dla każdego neuronu obliczono:

- liczbę wierzchołków,
- liczbę krawędzi,
- średni stopień wierzchołka,
- liczbę węzłów końcowych,
- liczbę punktów rozgałęzień,
- informację, czy graf spełnia własności drzewa,
- średnią liczbę krawędzi od korzenia do węzłów,
- maksymalną liczbę krawędzi od korzenia,
- betweenness centrality,
- Strahler index.

---

## Wyniki

| ID neuronu | Wierzchołki | Krawędzie | Leaf nodes | Branch nodes | Mean root hops | Max root hops | Max betweenness | Mean betweenness | Strahler max | Strahler mean |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| `1734350788` | 4465 | 4464 | 619 | 599 | 170.53 | 464 | 0.6522 | 0.02584 | 6 | 1.7599 |
| `1734350908` | 4847 | 4846 | 762 | 735 | 201.87 | 476 | 0.5857 | 0.02345 | 6 | 1.8267 |
| `722817260` | 4332 | 4331 | 657 | 633 | 313.70 | 399 | 0.6413 | 0.02498 | 6 | 1.8225 |

---

# Interpretacja wyników

## 1. Struktura drzewa

Dla wszystkich trzech neuronów zachodzi zależność:

\[
|E| = |V| - 1
\]

Na przykład dla neuronu `1734350788`:

\[
4464 = 4465 - 1
\]

Jest to charakterystyczna własność drzewa.

Dodatkowo dla wszystkich trzech rekonstrukcji otrzymano:

```text
is_tree = True