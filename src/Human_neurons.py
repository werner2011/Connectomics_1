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

def analyze_neuron(neurons): 
    """
    Liczy podstawowe cechy morfologiczne i topologiczne.
    """
    results = []
    for neuron in neurons:
        morphology = podsumuj_neuron(neuron)
        topology = analyze_topology(neuron)
        morphology.update(topology)
        results.append(morphology)

    return pd.DataFrame(results)

def add_metrics(df):
    """
    Dodaje metryki związane z gęstością 
    """

    df['branch_density'] = df['n_branches'] / df['cable_length'] 

    df['leaf_branch_ratio'] = df['n_leafs'] / df['n_branches'].replace(0, pd.NA) 

    return df 

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
        ]
    ].describe() 

    zapisz_plik(df,"human_pyramidal_morphology.csv",results_dir=RESULTS_DIR)
    zapisz_plik(statistics,"human_pyramidal_statistics.csv",results_dir=RESULTS_DIR) 

    fig = plot_neurons2D(neurons, title='Human pyramidal neurons') 
    zapisz_plik(fig, 'human_pyramidal_2d.png', results_dir=RESULTS_DIR) 

    fig3D = plot_neurons_3d(neurons, title='Human pyramidal neurons', show_axes=False) 
    zapisz_plik(fig3D, 'human_pyramidal_3D.html', results_dir=RESULTS_DIR) 

    fig3D.show() 

if __name__=="__main__":
    main() 