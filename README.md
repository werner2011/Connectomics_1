# Connectomics_1

Ćwiczeniowy projekt z analizy morfologii neuronów w Pythonie z użyciem biblioteki **NAVis**.

Projekt służy do nauki podstaw konektomiki strukturalnej, reprezentacji neuronów jako drzewiastych szkieletów oraz ekstrakcji prostych cech morfologicznych i topologicznych.

## Zakres projektu

Analizowane są przykładowe neurony typu `navis.TreeNeuron`.

Dla każdego neuronu wyznaczane są m.in.:

- liczba węzłów,
- liczba punktów rozgałęzień,
- liczba terminalnych końców,
- całkowita długość szkieletu,
- rozpiętość w osiach `x`, `y`, `z`,
- liczba konektorów,
- liczba połączeń pre- i postsynaptycznych,
- liczba węzłów i krawędzi grafu.

Na podstawie tych danych tworzone są również cechy pochodne:

- `branch_density`
- `leaf_branch_ratio`
- `pre_post_ratio`

`Cable length:` całkowita długość wszystkich segmentów szkieletu neuronu.

`Branch points:` liczba punktów rozgałęzień drzewa neuronalnego.

`Leaf nodes:` liczba terminalnych końców szkieletu.

Branch density = branch_density = n_branches / cable_length

`Opisuje liczbę punktów rozgałęzień w odniesieniu do całkowitej długości neuronu.`

Leaf - branch ratio leaf_branch_ratio = n_leafs / n_branches

`Prosta charakterystyka relacji między liczbą końców a liczbą rozgałęzień.`

Pre / post ratio pre_post_ratio = n_pre / n_post

`Opisuje proporcję konektorów presynaptycznych do postsynaptycznych.`

# Topologia

Każdy TreeNeuron może być analizowany jako graf.

W projekcie wykorzystywane są:

 - liczba węzłów grafu,
 - liczba krawędzi grafu.

## Pipeline analizy

```text
Example neurons
      ↓
navis.TreeNeuron
      ↓
┌───────────────────────────────────────────────┐
│                                               │
│  morphology     topology      connectors      │
│                                               │
│  cable length   graph nodes   pre/post        │
│  branches       graph edges                   │
│  leafs                                        │
│  extent x/y/z                                 │
│                                               │
└───────────────────────────────────────────────┘
      ↓
pandas.DataFrame
      ↓
derived features
      ↓
ranking
      ↓
descriptive statistics
      ↓
visualization