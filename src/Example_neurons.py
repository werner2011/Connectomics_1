import navis
from pathlib import Path 
import pandas as pd
import matplotlib.pyplot as plt 
from plotly.graph_objects import Figure as PlotlyFigure
"""
Użycie TreeNeuron - ten typ danych reprezentuje neuron jako szkielet drzewiasty. 
Jest to DAG. 
"""
RESULTS_DIR = Path.cwd() / 'results' / 'example_navis' 
def zapisz_plik(data, filename: str, results_dir: Path=RESULTS_DIR): 
    """
    Zapisuje wyniki analizy do katalogu results.

    Obsługiwane typy:
    - pandas.DataFrame -> .csv
    - str -> .txt
    - matplotlib Figure -> .png, .jpg, .pdf
    - Plotly Figure -> HTML
    """
    results_dir.mkdir(parents=True, exist_ok=True)
    file_path = results_dir / filename 

    if isinstance(data, pd.DataFrame): 
        data.to_csv(file_path, index=False) 
    elif isinstance(data, str):
        file_path.write_text(data) 
    elif isinstance(data, plt.Figure): 
        data.savefig(file_path, bbox_inches='tight', dpi=300)
    elif isinstance(data, PlotlyFigure):
        data.write_html(file_path,include_plotlyjs="cdn")
    else: 
        raise TypeError(f'Nieobsługiwany typ danych: {type(data)} ! ')

    print(f'Zapisano: {file_path}') 

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

def plot_neurons2D(neurons:navis.TreeNeuron, title: str, color_by=None, palette=None, view=('x', 'z'), method='2d'):
    """
    Uniwersalna funkcja do wizualizacji neuronów
    za pomocą navis.plot2d().
    """
    plot_options = {
        'view': view, 
        'method': method
    }
    if color_by is not None:
        plot_options['color_by'] = color_by 

    if palette is not None: 
        plot_options['palette'] = palette
    fig, ax = navis.plot2d(neurons, **plot_options) 

    ax.set_title(title)
    fig.tight_layout() 
    return fig 

def plot_neurons_3d(
    neurons,
    title="Neurons - 3D morphology",
    show_axes=False
):
    """
    Interaktywna wizualizacja neuronów 3D
    przy użyciu backendu Plotly.
    """

    fig = navis.plot3d(
        neurons,
        backend="plotly"
    )

    axis_options = dict(
        visible=show_axes,
        showgrid=show_axes,
        zeroline=False,
        showbackground=show_axes
    )

    fig.update_layout(

        title=title,

        scene=dict(

            # Zachowanie proporcji wynikających z danych
            aspectmode="data",

            xaxis=axis_options,
            yaxis=axis_options,
            zaxis=axis_options,

            # Obracanie sceny jak obiektu
            dragmode="orbit",

            # Początkowa pozycja kamery
            camera=dict(
                eye=dict(
                    x=1.4,
                    y=1.4,
                    z=1.0
                )
            )
        ),

        # Minimalizacja pustych marginesów
        margin=dict(
            l=0,
            r=0,
            b=0,
            t=50
        ),

        legend=dict(
            x=0.82,
            y=0.95
        )
    )

    return fig

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
    fig = plt.figure(figsize=(8,6))
    navis.plot2d(neuron_copy, color_by='strahler_index', palette="viridis", view=('x', '-z'), method='2d') 
    # Pokoloruj strukturę neuronu zależnie od wartości indeksu Strahlera.
    plt.title(f"Strahler index - {neuron.name}") 
    plt.tight_layout()

    return fig 

def main() -> None: 
    #podanie neuronów o reprezentacji szieletowej 
    #Neurony pochodzą z drosophili, dostaję kolekcję NeuronList (gdzie poszczególne elementy są TreeNeuron)
    neurony = navis.example_neurons(n=3, kind='skeleton') 
    print(f"Liczba neuronów: {len(neurony)}") 
    print('Typ', type(neurony))

    print("\n Podsumowanie NAVis: \n")
    print(neurony)

    wyniki = []
    for neuron in neurony: 
        print_neuron_details(neuron)
        morfologia = podsumuj_neuron(neuron)
        topologia = analyze_topology(neuron) 

        morfologia.update(topologia) 

        wyniki.append(morfologia) 

    df = pd.DataFrame(wyniki) 
    print(df) 
    # Dodatkowe cechy: 
    """ Utworzenie nowych kolumn: 
    - branch_density - liczba rozgałęzień / długość neuronu 
    - leaf_branch_ratio - charakterystyka struktury drzewa liczba końcówek neuronu / liczba rozgałęzień 
    """

    df["branch_density"] = df["n_branches"]/ df["cable_length"]

    df["leaf_branch_ratio"] = df["n_leafs"] / df["n_branches"].replace(0, pd.NA)

    if "n_pre" in df.columns and "n_post" in df.columns:
        df["pre_post_ratio"] = df["n_pre"]/ df["n_post"].replace(0, pd.NA)
        #zabezpieczenie przed dzieleniem przez zero

    ranking = df.sort_values('branch_density', ascending=False)
    statistics = df[['n_nodes', 'n_branches', 'n_leafs', 'cable_length']].describe() 

    zapisz_plik(df, 'example_neurons_morphology.csv')
    zapisz_plik(ranking, 'morphological_ranking.csv')
    zapisz_plik(statistics, 'descriptive_statistics.csv')

    # --------------------------------------------------------
    # 8. Wszystkie neurony razem - 2D
    # --------------------------------------------------------

    fig = plot_neurons2D(neurony,title="Example neurons - morphology")
    zapisz_plik(fig,"examples_morphology_2d.png")

    # --------------------------------------------------------
    # 9. Strahler index - każdy neuron osobno
    # --------------------------------------------------------

    for neuron in neurony:
        neuron_copy = neuron.copy()
        navis.strahler_index(neuron_copy)

        fig = plot_neurons2D(neuron_copy,title=(f"Strahler index - {neuron.name} ({neuron.id})"),color_by="strahler_index",palette="viridis")

        zapisz_plik(fig,f"strahler_{neuron.id}.png")
    # --------------------------------------------------------
    # 10. Cable length vs liczba rozgałęzień
    # --------------------------------------------------------

    fig, ax = plt.subplots(figsize=(7, 5))

    ax.scatter(df["cable_length"],df["n_branches"])
    for neuron_id, x, y in zip(df["id"],df["cable_length"],df["n_branches"]):
        ax.annotate(str(neuron_id),(x, y))

    ax.set_xlabel("Cable length")
    ax.set_ylabel("Number of branch points")

    ax.set_title("Morphology comparison")
    fig.tight_layout()
    zapisz_plik(fig, "morphology_comparison.png")
    # -------------------------------------------------------
    # 11. Wszystkie neurony razem - interaktywne 3D
    # --------------------------------------------------------

    fig3d = plot_neurons_3d(neurony,title="Example neurons - 3D morphology",show_axes=False)

    zapisz_plik(fig3d,"examples_morphology_3d.html")

    # Ten widok otwieramy automatycznie
    fig3d.show()


    # --------------------------------------------------------
    # 12. Każdy neuron osobno - interaktywne 3D
    # --------------------------------------------------------

    for neuron in neurony:

        fig3d = plot_neurons_3d(
            neuron,
            title=(
                f"3D morphology - "
                f"{neuron.name} ({neuron.id})"
            ),show_axes=False
        )

        zapisz_plik(fig3d,f"neuron_3d_{neuron.id}.html")

if __name__ == "__main__":
    main()