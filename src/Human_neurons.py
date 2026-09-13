from pathlib import Path 
import navis 
import pandas as pd 
import matplotlib.pyplot as plt 

from Example_neurons import (
    zapisz_plik,
    podsumuj_neuron,
    analyze_topology,
    plot_neurons2D,
    plot_neurons_3d,
)

PROJECT_DIR = Path(__file__).resolve().parents[1] 

SWC_DIR = PROJECT_DIR / 'data' / 'Neuromorpho' /'raw_swc' / 'pyramidal'
RESULTS_DIR = PROJECT_DIR / 'results' / 'neuromorpho' / 'human_pyramidal' 

def zaladuj_neurony():
    """
    Wczytuje pliki .swc 
    """
    neurons = [] 
    for swc_file in sorted(SWC_DIR.glob('*.swc')):
        neuron = navis.read_swc(swc_file) 
        neuron.name = swc_file.stem 
        neurons.append(neuron) 
        print(f'Wczytano: {swc_file.name}') 

    return navis.NeuronList(neurons) 

def analyze_strahler(neuron): 
    """
    Oblicza statystki indeksu Strahlera 
    """
    neuron_copy = neuron.copy()
    navis.strahler_index(neuron_copy) 
    strahler = neuron_copy.nodes['strahler_index'] 
    return { 
        'strahler_max': strahler.max(), 
        'strahler_mean': strahler.mean(), 
        'strahler_median': strahler.median()
    }

def analyze_neuron(neurons): 
    """
    Liczy podstawowe cechy morfologiczne i topologiczne.
    """
    results = []
    for neuron in neurons:
        morphology = podsumuj_neuron(neuron)
        topology = analyze_topology(neuron)
        strahler = analyze_strahler(neuron)
        morphology.update(topology)
        morphology.update(strahler)
        results.append(morphology)
        

    return pd.DataFrame(results)

def add_metrics(df):
    """
    Dodaje metryki związane z gęstością 
    """

    df['branch_density'] = df['n_branches'] / df['cable_length'] 

    df['leaf_branch_ratio'] = df['n_leafs'] / df['n_branches'].replace(0, pd.NA) 

    return df 

def plot_each_neuron(neurons): 
    """
    Tworzy osobne:
    - PNG 2D
    - PNG Strahlera
    - HTML 3D

    dla każdego neuronu.
    """

    for neuron in neurons: 
        neuron_name = neuron.name 

        fig = plot_neurons2D(neuron, title=f'Human pyramidal neuron - {neuron_name}') 
        zapisz_plik(fig, f'{neuron_name}_2D.png', results_dir=RESULTS_DIR)
        plt.close(fig) 

        neuron_strahler = neuron.copy() 
        navis.strahler_index(neuron_strahler) 
        fig_strahler = plot_neurons2D(neuron_strahler, title=f'Strahler index - {neuron_name}', color_by='strahler_index', palette='viridis') 
        zapisz_plik(fig_strahler, f'{neuron_name}_strahler.png', results_dir=RESULTS_DIR) 
        plt.close(fig_strahler) 

        fig3D = plot_neurons_3d(neuron, title=f'Human pyramidal neuron - {neuron_name}', show_axes=False)
        zapisz_plik(fig3D, f'{neuron_name}_3D.html', results_dir=RESULTS_DIR) 

def main() ->None: 
    neurons = zaladuj_neurony() 
    print(neurons) 

    df = analyze_neuron(neurons=neurons) 
    df = add_metrics(df) 
    statistics = df[
        [
            'n_nodes', 
            "n_branches",
            "n_leafs",
            "cable_length",
            "branch_density",
            "leaf_branch_ratio",
            "strahler_max",
            "strahler_mean",
            "strahler_median",
        ]
    ].describe() 

    zapisz_plik(df,"human_pyramidal_morphology.csv",results_dir=RESULTS_DIR)
    zapisz_plik(statistics,"human_pyramidal_statistics.csv",results_dir=RESULTS_DIR) 

    fig = plot_neurons2D(neurons, title='Human pyramidal neurons') 
    zapisz_plik(fig, 'human_pyramidal_2d.png', results_dir=RESULTS_DIR) 

    fig3D = plot_neurons_3d(neurons, title='Human pyramidal neurons', show_axes=False) 
    zapisz_plik(fig3D, 'human_pyramidal_3D.html', results_dir=RESULTS_DIR) 

    plot_each_neuron(neurons) 
    

if __name__=="__main__":
    main() 