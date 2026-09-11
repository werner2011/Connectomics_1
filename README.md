# Connectomics_1
Pierwsze rzeczy z konektomiki 

3 przykładowe neurony
        ↓
navis.TreeNeuron
        ↓
 ┌───────────────┬────────────────┬─────────────────┐
 │               │                │                 │
morfologia    topologia        connectors       wizualizacja
 │               │                │                 │
length         graph           pre/post          plot2d
branches       nodes                              Strahler
leafs          edges
extent
 │
 └────────────────────→ pandas.DataFrame
                         ↓
                   porównanie neuronów


DataFrame z podstawowymi cechami
              ↓
      cechy pochodne
 branch_density
 leaf_branch_ratio
 pre_post_ratio
              ↓
          ranking
              ↓
   statystyki opisowe
              ↓
        wizualizacja
              ↓
zależność cable_length ↔ n_branches