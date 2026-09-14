# Graph Analysis of Example Neurons

## Overview

Celem analizy jest opisanie morfologii szkieletowej neuronów za pomocą
podstawowych pojęć teorii grafów.

Przeanalizowano trzy przykładowe neurony typu:

`DA1_lPN_R`

udostępniane przez bibliotekę **NAVIS**.

W analizie neuron traktowany jest jako graf:

$$
G = (V,E)
$$

gdzie:

- $V$ — zbiór wierzchołków reprezentujących punkty rekonstrukcji,
- $E$ — zbiór krawędzi reprezentujących połączenia pomiędzy kolejnymi
  punktami szkieletu.

Do analizy topologicznej wykorzystano graf nieskierowany.

---

# 1. Model grafowy neuronu

Szkielet neuronu można interpretować jako drzewo:

```text
                        terminal node
                             ●
                            /
                           /
             branch ●─────●
                   /       \
                  /         \
                 ●           ● terminal node
                /
               /
root ●────────●
```

# 2. Wyniki analizy grafowej

Dla każdego neuronu obliczono podstawowe metryki topologiczne opisujące
strukturę szkieletu.

## 2.1 Zestawienie wyników

| ID neuronu | Nodes | Edges | Mean degree | Leaf nodes | Branch nodes | Mean root hops | Max root hops | Max betweenness | Mean betweenness | Strahler max | Strahler mean |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| `1734350788` | 4465 | 4464 | 1.99955 | 619 | 599 | 170.53 | 464 | 0.6522 | 0.02584 | 6 | 1.7599 |
| `1734350908` | 4847 | 4846 | 1.99959 | 762 | 735 | 201.87 | 476 | 0.5857 | 0.02345 | 6 | 1.8267 |
| `722817260` | 4332 | 4331 | 1.99954 | 657 | 633 | 313.70 | 399 | 0.6413 | 0.02498 | 6 | 1.8225 |

Wszystkie trzy neurony należą do typu `DA1_lPN_R`.

---

# 3. Struktura drzewa

Dla wszystkich neuronów zachodzi zależność:

$$
|E| = |V| - 1
$$

Na przykład dla neuronu `1734350788`:

$$
4464 = 4465 - 1
$$

Dodatkowo dla wszystkich trzech rekonstrukcji:

```text
is_tree = True
``` 

# 4. Stopień wierzchołka

Stopień wierzchołka oznacza liczbę krawędzi połączonych z danym węzłem.

Średni stopień wyniósł około:

$$ \bar{k} \approx 2 $$

dla wszystkich trzech neuronów.

Dla grafu:

$$ \sum_{v \in V} k(v) = 2|E| $$

więc:

$$ \bar{k} = \frac{2|E|}{|V|} $$

Ponieważ dla drzewa:

$$ |E| = |V| - 1 $$

otrzymujemy:

$$ \bar{k} = \frac{2(|V|-1)}{|V|} $$

Dla dużej liczby wierzchołków wartość ta dąży do:

$$ \bar{k} \rightarrow 2 $$

Uzyskane wartości są więc zgodne z oczekiwaną topologią drzewa.

# 5. Węzły końcowe i punkty rozgałęzień
| Neuron       | Leaf nodes | Branch nodes |
| ------------ | ---------: | -----------: |
| `1734350788` |        619 |          599 |
| `1734350908` |        762 |          735 |
| `722817260`  |        657 |          633 | 

Największą liczbę terminalnych zakończeń oraz punktów rozgałęzień posiada neuron 1734350908.

Może to wskazywać na bardziej rozbudowaną strukturę jego szkieletu.

Liczba końców i punktów rozgałęzień jest proporcjonalnie
podobna dla wszystkich trzech neuronów.

Stosunek:

$$ \frac{N_{leaf}}{N_{branch}} $$

wynosi w przybliżeniu:

| Neuron       | Leaf / branch |
| ------------ | ------------: |
| `1734350788` |         1.033 |
| `1734350908` |         1.037 |
| `722817260`  |         1.038 |

# 6. Strahler index

Strahler index opisuje hierarchię rozgałęzień struktury drzewiastej.

Terminalne gałęzie otrzymują najniższy rząd.

Jeżeli dwie gałęzie o tym samym rzędzie \(k\) łączą się:

    k + k → k + 1

Wyniki: 

| Neuron       | Strahler max | Strahler mean |
| ------------ | -----------: | ------------: |
| `1734350788` |            6 |         1.760 |
| `1734350908` |            6 |         1.827 |
| `722817260`  |            6 |         1.822 |

Wszystkie trzy neurony osiągają:

$$ S_{max} = 6 $$

Oznacza to, że osiągają podobny maksymalny poziom hierarchii rozgałęzień.

Również średnie wartości Strahlera są bardzo podobne.

Może to wskazywać na wspólny ogólny plan organizacji topologicznej neuronów typu DA1_lPN_R.