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
def analyze_graph(neuron: navis.TreeNeuron,G, betweenness): 
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



def plot_betweenness(neuron:navis.TreeNeuron, betweenness): 
    """
    Koloruje neuron według betweenness centrality.
    """
    neuron_copy = neuron.copy()  
    neuron_copy.nodes['betweenness'] = neuron_copy.nodes['node_id'].map(betweenness).fillna(0) 
    fig = plot_neurons2D(neuron_copy, title=f"Betweenness - {neuron.name}", color_by='betweenness', palette='viridis') 

    return fig 

def analyze_bottleneck(G, betweenness):  
    bottleneck_node = max(betweenness, key=betweenness.get) 

    bottleneck_value = betweenness[bottleneck_node] 
    G_removed = G.copy() 
    G_removed.remove_node(bottleneck_node) 

    components = list(nx.connected_components(G_removed)) 

    component_sizes = sorted(
        [len(component) for component in components], 
        reverse=True
    ) 

    return {
        "bottleneck_node": bottleneck_node,
        "bottleneck_betweenness": bottleneck_value,
        "n_components_after_removal": len(components),
        "largest_component": component_sizes[0],
        "second_component": (
            component_sizes[1]
            if len(component_sizes) > 1
            else 0
        ),
    }

def plot_bottleneck(neuron: navis.TreeNeuron,G, betweenness, radius=20):
    """
    Pokazuje lokalny podgraf wokół węzła
    o największym betweenness.
    """
    bottleneck_node = max(betweenness, key=betweenness.get)

    subgraph = nx.ego_graph(G, bottleneck_node, radius=radius) 
    nodes = neuron.nodes.set_index('node_id') 

    pos = {
        node: (
            nodes.loc[node, 'x'], 
            nodes.loc[node, 'z']
        )
        for node in subgraph.nodes 
    }

    fig, ax = plt.subplots(figsize=(8,8)) 

    nx.draw_networkx_edges(subgraph, pos, ax=ax, width=1)
    nx.draw_networkx_nodes(subgraph, pos, ax=ax, node_size=12)
    nx.draw_networkx_nodes(subgraph, pos, nodelist=[bottleneck_node], ax=ax, node_size=100) 

    ax.set_title(f'Bottleneck region - {neuron.id}') 
    ax.axis('equal')
    ax.axis('off') 

    return fig 

def main() -> None: 
    neurony = navis.example_neurons(n=3, kind='skeleton') 
    results = []
    for neuron in neurony:
        G= neuron.graph.to_undirected()
        betweenness = nx.betweenness_centrality(G) 
        metrics = analyze_graph(neuron, G, betweenness) 
        bottleneck = analyze_bottleneck(G, betweenness)
        metrics.update(bottleneck)
        results.append(metrics) 

        fig = plot_betweenness(neuron, betweenness) 
        zapisz_plik(fig, f'betweenness_{neuron.id}.png', results_dir=RESULTS_DIR) 
        plt.close(fig) 

        fig = plot_bottleneck(neuron, G, betweenness, radius=20)
        zapisz_plik(fig, f'bottleneck_{neuron.id}.png', results_dir=RESULTS_DIR)
        plt.close(fig) 

    df = pd.DataFrame(results) 
    print(df) 
    zapisz_plik(df, 'graph_metrics.csv', results_dir=RESULTS_DIR) 

if __name__=="__main__":
    main()  
