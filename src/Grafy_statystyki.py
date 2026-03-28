import networkx as nx 
import matplotlib.pyplot as plt 
import numpy as np 
Graf_small_world = nx.watts_strogatz_graph(n=20, k=4, p=0.3)
print("--- Podstawowe statystyki sieci ---")

# Liczba węzłów i krawędzi
n_nodes = Graf_small_world.number_of_nodes()
n_edges = Graf_small_world.number_of_edges()
print(f"Liczba obszarów (węzłów): {n_nodes}")
print(f"Liczba połączeń (krawędzi): {n_edges}")

# Średni stopień węzła (ile średnio połączeń ma jeden obszar)
degrees = [d for n, d in Graf_small_world.degree()]
mean_degree = np.mean(degrees)
print(f"Mean degree: {mean_degree:.2f}")

# Współczynnik klastrowania (czy sąsiedzi węzła też są ze sobą połączeni?)
# W konektomice to miara lokalnej integracji mózgu.
avg_clustering = nx.average_clustering(Graf_small_world)
print(f"Wspolczynnik klastrowania: {avg_clustering:.2f}")

# Średnia najkrótsza ścieżka (jak szybko informacja płynie przez sieć?)
if nx.is_connected(Graf_small_world):
    avg_path = nx.average_shortest_path_length(Graf_small_world)
    print(f"Srednia droga (efektywnosc): {avg_path:.2f}")

# 3. WIZUALIZACJA
plt.figure(figsize=(12, 5))

# Rysowanie grafu
plt.subplot(1, 2, 1)
nx.draw(Graf_small_world, with_labels=True, node_color='lightgreen', edge_color='gray', node_size=500)
plt.title("Wizualizacja Sieci Neuronalnej")

# Histogram stopni węzłów
plt.subplot(1, 2, 2)
plt.hist(degrees, bins=range(min(degrees), max(degrees) + 2), color='skyblue', edgecolor='black')
plt.title("Rozkład stopni węzłów")
plt.xlabel("Stopień (liczba połączeń)")
plt.ylabel("Liczba węzłów")

plt.tight_layout()
plt.show()