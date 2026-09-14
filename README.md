# Structural connectomics

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

Leaf branch ratio = leaf_branch_ratio = n_leafs / n_branches

`Prosta charakterystyka relacji między liczbą końców a liczbą rozgałęzień.`

Pre_post ratio = pre_post_ratio = n_pre / n_post

`Opisuje proporcję konektorów presynaptycznych do postsynaptycznych.`

# Topologia

Każdy TreeNeuron może być analizowany jako graf.

W projekcie wykorzystywane są:

 - liczba węzłów grafu,
 - liczba krawędzi grafu.

# Strahler index


**Strahler index** (Strahler order) jest miarą topologiczną opisującą
hierarchię rozgałęzień struktury drzewiastej.

Metoda została pierwotnie opracowana do opisu sieci rzecznych, ale może
być stosowana do dowolnych struktur drzewiastych, w tym szkieletów neuronów.

Neuron reprezentowany jako `TreeNeuron` może być traktowany jako graf
drzewiasty, w którym:

- wierzchołki odpowiadają punktom rekonstrukcji neuronu,
- krawędzie odpowiadają fragmentom neurytów,
- root reprezentuje początek drzewa,
- leaf nodes reprezentują końcowe fragmenty drzewa,
- branch points reprezentują miejsca rozgałęzień.

Strahler order jest wyznaczany od końców drzewa w kierunku jego korzenia.

Dla klasycznej definicji:

1. Końcowym gałęziom drzewa przypisywany jest rząd 1.
2. Jeżeli w węźle łączą się dwie gałęzie o takim samym rzędzie `k`,
   gałąź powyżej otrzymuje rząd `k + 1`.
3. Jeżeli spotykają się gałęzie o różnych rzędach, zachowywany jest
   większy z tych rzędów.

Przykład:

        1       1
         \     /
          \   /
            2
            |
        1   |   1
         \  |  /
          \ | /
            2
            |
            2

Im większy maksymalny indeks Strahlera, tym bardziej hierarchicznie
rozbudowana jest struktura drzewa.

W analizie neuronów Strahler index może służyć do:

- opisu hierarchii drzewa dendrytycznego lub aksonalnego,
- identyfikacji głównych i peryferyjnych gałęzi,
- porównywania złożoności topologicznej neuronów,
- oddzielania głównego szkieletu neuronu od cienkich końcowych gałęzi,
- wizualizacji organizacji arboru neuronalnego.

W NAVIS indeks Strahlera można obliczyć:

```python
navis.strahler_index(neuron)

W projekcie indeks Strahlera jest wykorzystywany do kolorowania struktury neuronu w wizualizacji 2D.

# Wizualizacje

Projekt generuje kilka typów wykresów:

 - morfologia wszystkich neuronów w 2D,
 - osobne wizualizacje Strahlera,
 - porównanie cable_length i n_branches,
 - interaktywne wizualizacje neuronów w 3D.

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