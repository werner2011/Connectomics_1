import navis
from pathlib import Path 
import pandas as pd
import matplotlib.pyplot as plt 
"""
Użycie TreeNeuron - ten typ danych reprezentuje neuron jako szkielet drzewiasty. 
Jest to DAG. 
"""
def podsumuj_neuron(neuron: navis.TreeNeuron):
    """
    Zwraca cechy morfologiczne pojedynczego neuronu
    """
    coords = neuron.nodes[['x', 'y', 'z']] # z tabeli wybieram współrzędne trójwymiarowe
    mins = coords.min()
    maxs = coords.max() 
    extent = maxs-mins #obliczenie rozpiętości przestrzennej neuronu 
    """
    Jest to różnica między najbardziej skrajnymi punktami w danej osi
    """
    result = {
        "id": neuron.id,
        "name": neuron.name,
        "n_nodes": neuron.n_nodes,
        "n_branches": neuron.n_branches,
        "n_leafs": neuron.n_leafs,
        "cable_length": neuron.cable_length, #zsumowanie długości wszystkich segmentów
        "extent_x": extent["x"], #szerokość 
        "extent_y": extent["y"], #wysokość 
        "extent_z": extent["z"], # głębokość 
    }
    #connectors
    """
    Odnosi się do cyfrowych punktów reprezentujących synapsy i inne połączenia między neuronami
    Tabela .connectors grupuje wszystkie punkty kontaktu. 
    NAVis wykorzystuje connectors do reprezentowania m.in. synaps pre- i postsynaptycznych, ale system pozwala też reprezentować 
    inne rodzaje konektorów
    """
    if neuron.connectors is not None: #gdy connectors istnieje i nie jest None
        result['n_connectors'] = len(neuron.connectors) #nowy klucz do słownika

        if 'type' in neuron.connectors.columns:  #czy w DataFrame istnieje kolumna o nazwie type? 
            counts = neuron.connectors['type'].value_counts() 
            #counts jest obiektem Series
            #zapis liczby pre i post 

            result['n_pre'] = counts.get('pre', 0) #określa rolę w synapsie 
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

    print("Liczba wierzchołków:", neuron.n_nodes) #z ilu punktów składa się szkielet? 
    print("Branch points:", neuron.n_branches) # liczba punktów rozgałęziających drzewo 
    print("Leaf nodes:", neuron.n_leafs) #liczba liści szkieletu komórki 
    print("Cable length:", neuron.cable_length) # całkowita długość wszystkich fragmentów szkieletu 
    print("Soma:", neuron.soma) #.soma przechowuje ID węzła (node ID) odpowiadającego ciału komórki
    print("Units:", neuron.units)

    print("\nTypy węzłów:")
    """
    neuron.nodes jest tabelą pandas.DataFrame
    NAVis różnie klasyfikuje węzły: 
    root jest początkiem drzewa.
    branch to miejsce rozgałęzienia.
    end to terminalny koniec.
    slab to zwykły punkt leżący gdzieś na przebiegu neurytu
    """
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
    Strahler index/order to metoda przypisywania gałęziom drzewa numerów 
    opisujących ich pozycję w hierarchii rozgałęzień.
    Jest miarą hierarchii struktury drzewa.
    """
    neuron_copy = neuron.copy() 

    navis.strahler_index(neuron_copy) # analiza topologii drzewa neuronu 
    print(
        neuron_copy.nodes[['node_id', 'type', 'strahler_index']].head(20)
    )
    navis.plot2d(neuron_copy, color_by='strahler_index', palette="viridis", view=('x', '-z'), method='2d') 
    # Pokoloruj strukturę neuronu zależnie od wartości indeksu Strahlera.
    plt.title(f"Strahler index - {neuron.name}") 
    plt.tight_layout()
    plt.show() 

def main() ->None: 
    neurons = navis.example_neurons(n=3, kind='skeleton') #podanie neuronów o reprezentacji szieletowej
    #Neurony pochodzą z drosophili, dostaję kolekcję NeuronList (gdzie poszczególne elementy są TreeNeuron) 
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
    """
    Utworzenie nowych kolumn: 
    - branch_density - liczba rozgałęzień / długość neuronu 
    - leaf_branch_ratio - charakterystyka struktury drzewa 
    liczba końcówek neuronu / liczba rozgałęzień 
    """
    df["branch_density"] = df["n_branches"]/ df["cable_length"]

    df["leaf_branch_ratio"] = df["n_leafs"]/ df["n_branches"]

    if "n_pre" in df.columns and "n_post" in df.columns:

        df["pre_post_ratio"] = (df["n_pre"]/ df["n_post"].replace(0, pd.NA)) #zabezpieczenie przed dzieleniem przez zero 

    print("\n============================================")
    print("MORPHOLOGICAL RANKING")
    print("============================================")

    ranking = df.sort_values("branch_density",ascending=False) #sortowanie według branch_density 
    # czyli według gęstości rozgałęzień od największej do najmniejszej 

    print(ranking[["id","cable_length","n_branches","branch_density"]]) #wybór najważniejszych kolumn 
    print("\n============================================")
    print("DESCRIPTIVE STATISTICS")
    print("============================================")

    print(df[["n_nodes","n_branches","n_leafs","cable_length"]].describe())
    #describe() - automatycznie oblicza podstawowe statystyki dla kolumn numerycznych.

    plot_neurons(neurons)

    for neuron in neurons: #wykonanie dla każdego neuronu Strahlera
        plot_strahler(neuron)

    plt.figure(figsize=(6, 5))
    plt.scatter(df["cable_length"],df["n_branches"])


    """
    Podkreślenie _ jest konwencją Pythona:
    - dostaję tę wartość, ale nie jest mi potrzebna.
    """
    for neuron_id, x, y in zip(df['id'], df['cable_length'], df['n_branches']): 
        plt.annotate(str(neuron_id), (x,y)) 

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