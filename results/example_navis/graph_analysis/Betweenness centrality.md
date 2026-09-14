## Betweenness centrality

Betweenness centrality opisuje, jak często dany wierzchołek znajduje się
na najkrótszych ścieżkach pomiędzy innymi parami wierzchołków.

Dla wierzchołka \(v\):

$$ C_B(v) = \sum_{s \neq v \neq t} \frac{\sigma_{st}(v)} {\sigma_{st}} $$

gdzie: 

* **$\sigma_{st}$** — liczba najkrótszych ścieżek między $s$ i $t$,
* **$\sigma_{st}(v)$** — liczba tych ścieżek przechodzących przez $v$.

W przypadku drzewa pomiędzy każdą parą wierzchołków istnieje dokładnie
jedna ścieżka.

Węzeł o wysokiej wartości betweenness często łączy duże fragmenty drzewa.

# Wyniki betweenness centrality
| Neuron       | Max betweenness | Mean betweenness |
| ------------ | --------------: | ---------------: |
| `1734350788` |      **0.6522** |      **0.02584** |
| `1734350908` |          0.5857 |          0.02345 |
| `722817260`  |          0.6413 |          0.02498 |


Najwyższą maksymalną centralność uzyskano dla neuronu 1734350788.

Średnie wartości są natomiast bardzo podobne dla wszystkich trzech neuronów:

$$ C_B^{mean} \approx 0.023 - 0.026 $$

Sugeruje to zbliżony ogólny rozkład centralności w analizowanych drzewach.

### Neuron 1734350788

![Betweenness centrality — neuron 1734350788](betweenness_1734350788.png)

### Neuron 1734350908

![Betweenness centrality — neuron 1734350908](betweenness_1734350908.png)

### Neuron 722817260

![Betweenness centrality — neuron 722817260](betweenness_722817260.png)