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

Cable length

Całkowita długość wszystkich segmentów szkieletu neuronu.

Branch points

Liczba punktów rozgałęzień drzewa neuronalnego.

Leaf nodes

Liczba terminalnych końców szkieletu.

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