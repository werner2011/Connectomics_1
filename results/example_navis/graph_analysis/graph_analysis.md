# Graph analysis of example neurons

## Cel analizy

Celem analizy było potraktowanie szkieletowej rekonstrukcji neuronu jako grafu
i zastosowanie podstawowych pojęć teorii grafów do opisu jego topologii.

Przeanalizowano trzy przykładowe neurony typu:

`DA1_lPN_R`

udostępniane przez bibliotekę NAVIS.

Każdy neuron jest reprezentowany jako graf:

\[
G = (V, E)
\]

gdzie:

- \(V\) — zbiór wierzchołków odpowiadających punktom rekonstrukcji neuronu,
- \(E\) — zbiór krawędzi odpowiadających połączeniom pomiędzy kolejnymi
  punktami szkieletu.

W analizie graf został potraktowany jako graf nieskierowany, ponieważ
interesowała nas przede wszystkim topologia drzewa neuronalnego.

---

## Analizowane metryki

Dla każdego neuronu obliczono:

- liczbę wierzchołków,
- liczbę krawędzi,
- średni stopień wierzchołka,
- liczbę węzłów końcowych,
- liczbę punktów rozgałęzień,
- sprawdzenie, czy graf jest drzewem,
- średnią liczbę krawędzi od korzenia do węzłów,
- maksymalną liczbę krawędzi od korzenia,
- betweenness centrality,
- Strahler index.

---

## Wyniki

| ID neuronu | Wierzchołki | Krawędzie | Leaf nodes | Branch nodes | Mean root hops | Max root hops | Max betweenness | Mean betweenness | Strahler max | Strahler mean |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| 1734350788 | 4465 | 4464 | 619 | 599 | 170.53 | 464 | 0.6522 | 0.02584 | 6 | 1.7599 |
| 1734350908 | 4847 | 4846 | 762 | 735 | 201.87 | 476 | 0.5857 | 0.02345 | 6 | 1.8267 |
| 722817260 | 4332 | 4331 | 657 | 633 | 313.70 | 399 | 0.6413 | 0.02498 | 6 | 1.8225 |

---

# Interpretacja wyników

## 1. Struktura drzewa

Dla wszystkich neuronów zachodzi zależność:

\[
|E| = |V| - 1
\]

Na przykład dla neuronu `1734350788`:

\[
4464 = 4465 - 1
\]

Jest to charakterystyczna własność drzewa.

Dodatkowo dla wszystkich trzech neuronów:

`is_tree = True`

Oznacza to, że analizowane szkielety tworzą spójne grafy bez cykli.

---

## 2. Średni stopień wierzchołka

Średni stopień wierzchołka wynosi około:

\[
\bar{k} \approx 2
\]

dla wszystkich trzech neuronów.

Dla drzewa:

\[
|E| = |V| - 1
\]

oraz:

\[
\sum_{v \in V} k(v) = 2|E|
\]

dlatego:

\[
\bar{k}
=
\frac{2|E|}{|V|}
=
\frac{2(|V|-1)}{|V|}
\]

Dla dużej liczby wierzchołków wartość ta dąży do:

\[
\bar{k} \rightarrow 2
\]

Uzyskane wartości są więc zgodne z topologią drzewa.

---

## 3. Końce i punkty rozgałęzień

Liczba terminalnych węzłów wynosiła:

- 619,
- 762,
- 657.

Liczba punktów rozgałęzień wynosiła odpowiednio:

- 599,
- 735,
- 633.

Neuron `1734350908` posiada największą liczbę zarówno końcowych węzłów,
jak i punktów rozgałęzień.

Może to wskazywać na bardziej rozbudowany szkielet rekonstrukcji.

Jednocześnie stosunek liczby końców do liczby punktów rozgałęzień jest
podobny dla wszystkich trzech neuronów.

Może to wskazywać na podobny ogólny sposób organizacji topologicznej
neuronów należących do tego samego typu.

---

## 4. Odległość od korzenia

`mean_root_hops` oznacza średnią liczbę krawędzi, które należy przejść
od korzenia drzewa do poszczególnych wierzchołków.

`max_root_hops` oznacza największą taką odległość.

Wyniki:

| neuron | mean root hops | max root hops |
|---|---:|---:|
| 1734350788 | 170.53 | 464 |
| 1734350908 | 201.87 | 476 |
| 722817260 | 313.70 | 399 |

Największą średnią wartość uzyskano dla neuronu:

`722817260`

mimo że jego maksymalna liczba kroków od korzenia jest mniejsza niż
w przypadku dwóch pozostałych neuronów.

Oznacza to, że duża część jego wierzchołków znajduje się relatywnie
daleko od korzenia w sensie topologicznym.

Warto jednak podkreślić, że `root_hops` oznacza liczbę krawędzi,
a nie fizyczną odległość w przestrzeni.

Wartość może więc zależeć również od gęstości punktów użytych
w rekonstrukcji neuronu.

---

## 5. Betweenness centrality

Betweenness centrality opisuje, jak często dany wierzchołek znajduje się
na najkrótszych ścieżkach pomiędzy innymi parami wierzchołków.

Dla wierzchołka \(v\):

\[
C_B(v)
=
\sum_{s \neq v \neq t}
\frac{\sigma_{st}(v)}
{\sigma_{st}}
\]

gdzie:

- \(\sigma_{st}\) — liczba najkrótszych ścieżek pomiędzy \(s\) i \(t\),
- \(\sigma_{st}(v)\) — liczba tych ścieżek przechodzących przez \(v\).

Największe wartości `max_betweenness` wynosiły około:

\[
0.59 - 0.65
\]

Oznacza to, że w każdym neuronie istnieją węzły zajmujące bardzo istotne
pozycje topologiczne.

Takie węzły łączą duże fragmenty drzewa i mogą być traktowane jako
elementy topologicznego szkieletu neuronu.

Średnia wartość betweenness była podobna dla wszystkich neuronów
i wynosiła około:

\[
0.023 - 0.026
\]

co wskazuje na podobny ogólny rozkład centralności.

---

## 6. Strahler index

Maksymalny indeks Strahlera wyniósł:

\[
S_{max} = 6
\]

dla wszystkich trzech neuronów.

Oznacza to, że wszystkie analizowane neurony osiągają podobny maksymalny
poziom hierarchii rozgałęzień.

Średnie wartości Strahlera również są podobne:

| neuron | Strahler mean |
|---|---:|
| 1734350788 | 1.760 |
| 1734350908 | 1.827 |
| 722817260 | 1.822 |

Pod względem hierarchii rozgałęzień analizowane neurony są więc do siebie
bardzo podobne.

Jest to zgodne z faktem, że wszystkie trzy należą do tego samego typu
neuronalnego `DA1_lPN_R`.

---

# Podsumowanie

Analiza pokazuje, że trzy neurony typu `DA1_lPN_R` posiadają podobną
ogólną organizację topologiczną.

Wspólne cechy obejmują:

- strukturę drzewa,
- średni stopień wierzchołka bliski 2,
- podobny stosunek liczby końców do liczby punktów rozgałęzień,
- identyczny maksymalny indeks Strahlera,
- podobną średnią betweenness centrality.

Jednocześnie obserwowane są różnice w rozmieszczeniu węzłów względem
korzenia.

Najbardziej wyróżnia się neuron `722817260`, który posiada znacznie
większą średnią liczbę kroków od korzenia, mimo mniejszej maksymalnej
głębokości drzewa.

Pokazuje to, że pojedyncza metryka nie jest wystarczająca do pełnego
opisu topologii neuronu.

Rozmiar grafu, hierarchia rozgałęzień oraz rozmieszczenie węzłów
względem korzenia opisują różne właściwości struktury neuronalnej.

---

## Ograniczenia

Analiza ma charakter eksploracyjny.

Badane są tylko trzy neurony należące do tego samego typu, dlatego
na podstawie tych wyników nie należy formułować ogólnych wniosków
biologicznych dotyczących całej populacji neuronów.

Dodatkowo `root_hops` opisuje liczbę krawędzi, a nie rzeczywistą długość
ścieżki w jednostkach fizycznych.

Metryki grafowe należy więc interpretować przede wszystkim jako opis
topologii rekonstrukcji neuronalnej.