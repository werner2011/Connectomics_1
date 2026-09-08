import navis
from pathlib import Path 
import pandas as pd
import matplotlib.pyplot as plt 
def podsumuj_neuron(neuron: navis.TreeNeuron):
    """
    Zwraca cechy morfologiczne pojedynczego neuronu
    """
    coords = neuron.nodes[['x', 'y', 'z']] 
    mins = coords.min()
    maxs = coords.max() 
    extent = maxs-mins
    result = {
        "id": neuron.id,
        "name": neuron.name,
        "n_nodes": neuron.n_nodes,
        "n_branches": neuron.n_branches,
        "n_leafs": neuron.n_leafs,
        "cable_length": neuron.cable_length,
        "extent_x": extent["x"],
        "extent_y": extent["y"],
        "extent_z": extent["z"],
    }
    #connectors
    if neuron.connectors is not None:
        result['n_connectors'] = len(neuron.connectors) 

        if 'type' in neuron.connectors.columns: 
            counts = neuron.connectors['type'].value_counts() 

            result['n_pre'] = counts.get('pre', 0)
            result['n_post'] = counts.get('post', 0)

    return result 

def analyze_topology(neuron:navis.TreeNeuron): 
    graf = neuron.graph
    return{
        'graph_nodes' : len(graf.nodes), 
        'graf_edges': len(graf.edges)
    }

def print_neuron_details(neuron: navis.TreeNeuron): 
    """
    Podsumowanie pojedynczego neuronu
    """
    print("\n" + "=" * 60)
    print(f"Neuron: {neuron.name}")
    print(f"ID: {neuron.id}")
    print("=" * 60)

    print("Liczba nodes:", neuron.n_nodes)
    print("Branch points:", neuron.n_branches)
    print("Leaf nodes:", neuron.n_leafs)
    print("Cable length:", neuron.cable_length)
    print("Soma:", neuron.soma)
    print("Units:", neuron.units)

    print("\nTypy węzłów:")
    print(neuron.nodes["type"].value_counts())

    if neuron.connectors is not None:
        print("\nConnectors:")
        print("Liczba:", len(neuron.connectors))

        if "type" in neuron.connectors.columns:
            print(neuron.connectors["type"].value_counts())

def plot_neurons(neurons:navis.TreeNeuron): 
    navis.plot2d(neurons, view=('x', '-z'), method='2d') 
    plt.title('Example neurons - morphology') 
    plt.tight_layout()
    plt.show() 

def plot_strahler(neuron:navis.TreeNeuron): 
    """
    Wizualizacja hierarchii rozgałęzień.
    """
    neuron_copy = neuron.copy() 

    navis.strahler_index(neuron_copy)
    navis.plot2d(neuron_copy, color_by='strahler_index', palette="viridis", view=('x', '-z'), method='2d') 
    plt.title(f"Strahler index - {neuron.name}") 
    plt.tight_layout()
    plt.show() 

def main() ->None: 
    neurons = navis.example_neurons(n=3, kind='skeleton') 
    print("\nLiczba neuronów:", len(neurons))
    print("Typ:", type(neurons))

    print("\nPodstawowe podsumowanie NAVis:")
    print(neurons)

    wyniki = []
    for neuron in neurons: 
        print_neuron_details(neuron=neuron) 
        morphology = podsumuj_neuron(neuron) 
        topology = analyze_topology(neuron) 

        morphology.update(topology) 
        wyniki.append(morphology) 

    df = pd.DataFrame(wyniki) 
    print("\n============================================")
    print("MORPHOLOGICAL SUMMARY")
    print("============================================")

    print(df)

    df["branch_density"] = (df["n_branches"]/ df["cable_length"])

    df["leaf_branch_ratio"] = (df["n_leafs"]/ df["n_branches"])

    if "n_pre" in df.columns and "n_post" in df.columns:

        df["pre_post_ratio"] = (df["n_pre"]/ df["n_post"].replace(0, pd.NA))

    print("\n============================================")
    print("MORPHOLOGICAL RANKING")
    print("============================================")

    ranking = df.sort_values("branch_density",ascending=False)

    print(ranking[["id","cable_length","n_branches","branch_density"]])
    # ---------------------------------------------------------
    # 6. Statystyki opisowe
    # ---------------------------------------------------------

    print("\n============================================")
    print("DESCRIPTIVE STATISTICS")
    print("============================================")

    print(df[["n_nodes","n_branches","n_leafs","cable_length"]].describe())

    plot_neurons(neurons)

    for neuron in neurons:
        plot_strahler(neuron)

    plt.figure(figsize=(6, 5))
    plt.scatter(df["cable_length"],df["n_branches"])

    for _, row in df.iterrows():

        plt.annotate(str(row["id"]),(row["cable_length"],row["n_branches"]))

    plt.xlabel("Cable length")
    plt.ylabel("Number of branch points")
    plt.title("Morphology comparison")

    plt.tight_layout()
    plt.show()

    df.to_csv("example_neurons_morphology.csv",index=False)

    print(
        "\nWyniki zapisano do:"
        "\nexample_neurons_morphology.csv"
    )


if __name__ == "__main__":
    main()