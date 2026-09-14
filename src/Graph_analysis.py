from pathlib import Path 
import navis 
import numpy as np 
import pandas as pd 
import networkx as nx 
import matplotlib.pyplot as plt 

from Example_neurons import(
    zapisz_plik, 
    plot_neurons2D 
)
RESULTS_DIR = Path.cwd() / 'results' / 'example_navis' / 'graph_analysis' 
RESULTS_DIR.mkdir(parents=True, exist_ok=True) 
def analyze_graph(neuron: navis.TreeNeuron): 
    """
    Analiza grafowa neuronu 
    """
    G = neuron.graph.to_undirected() 
    n_nodes = G.number_of_nodes() 
    n_edges = G.number_of_edges() 
    degrees = dict(G.degree()) 
    mean_degree = np.mean(
        list(degrees.values())
    )
    leaf_nodes = [
        node for node, degree in degrees.items() if degree == 1
    ]
    branch_nodes = [
        node for node, degree in degrees.items() if degree >=3 
    ]
    is_tree = nx.is_tree(G) 

    #Korzeń 
    root_rows=neuron.nodes[
        neuron.nodes['type'] == 'root'
    ]
    if len(root_rows)>0:
        root_id = int(root_rows.iloc[0]['node_id'])

    else:
        root_id=None 

    mean_root_hops = np.nan 
    max_root_hops = np.nan 

    if root_id is not None: 
        distances = nx.single_source_shortest_path_length(G,root_id) 
        distances_values = list(distances.values()) 
        mean_root_hops = np.mean(distances_values)
        max_root_hops = np.max(distances_values) 

        betweenness = nx.betweenness_centrality(G) 
        max_betw = max(betweenness.values()) 
        mean_betw = np.mean(list(betweenness.values())) 

        neuron_copy = neuron.copy() 
        navis.strahler_index(neuron_copy) 
        strahler = neuron_copy.nodes['strahler_index'] 

        strahler_max = strahler.max()
        strahler_mean = strahler.mean() 

        return{
            "id": neuron.id,
            "name": neuron.name,
            "n_nodes": n_nodes,
            "n_edges": n_edges,
            "mean_degree": mean_degree,
            "n_leafs": len(leaf_nodes),
            "n_branch_nodes": len(branch_nodes),
            "is_tree": is_tree,
            "mean_root_hops": mean_root_hops,
            "max_root_hops": max_root_hops,
            "max_betweenness": max_betw,
            "mean_betweenness": mean_betw,
            "strahler_max": strahler_max,
            "strahler_mean": strahler_mean,
        } 



def plot_betweenness(neuron:navis.TreeNeuron): 
    """
    Koloruje neuron według betweenness centrality.
    """
    neuron_copy = neuron.copy() 
    G = neuron_copy.graph.to_undirected() 
    betweenness = nx.betweenness_centrality(G) 
    neuron_copy.nodes['betweenness'] = neuron_copy.nodes['node_id'].map(betweenness).fillna(0) 
    fig = plot_neurons2D(neuron_copy, title=f"Betweenness - {neuron.name}", color_by='betweenness', palette='viridis') 

    return fig 

def main() -> None: 
    neurony = navis.example_neurons(n=3, kind='skeleton') 
    results = []
    for neuron in neurony:
        metrics = analyze_graph(neuron) 
        results.append(metrics) 

    df = pd.DataFrame(results) 
    print(df) 
    zapisz_plik(df, 'graph_metrics.csv', results_dir=RESULTS_DIR) 

    for neuron in neurony:
        fig = plot_betweenness(neuron) 
        zapisz_plik(fig, f'betweenness_{neuron.id}.png', results_dir=RESULTS_DIR) 
        plt.close(fig) 

if __name__=="__main__":
    main()  
