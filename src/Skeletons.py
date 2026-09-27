import navis 
import matplotlib.pyplot as plt 
from pathlib import Path 
import requests 
PROJECT_DIR = Path(__file__).resolve().parents[1]
DATA_DIR = PROJECT_DIR / 'data' / 'Neuromorpho' / 'raw_swc' / 'Humback_whale' 
RESULTS_DIR = PROJECT_DIR / 'results' / 'neuromorpho' / 'whale_neurons' 
RESULTS_DIR.mkdir(exist_ok=True, parents=True)
BASE_URL = "https://neuromorpho.org/api" 
def pobierz_neuron() -> navis.TreeNeuron: 
    """
    Pobiera plik .swc z bazy Neuromorpho 
    """

def inspect_neuron(neuron: navis.TreeNeuron): 
    print('*' * 60) 
    print('ID: ', neuron.id) 
    print('Name: ', neuron.name) 
    print('')

if __name__=="__main__": 
    neuron = navis.read_swc(DATA_DIR / 'n1.swc') 
    print(neuron)
    print(type(neuron)) 
    print(neuron.nodes.head())
    print(neuron.nodes.columns) 
    print(neuron.nodes.dtypes)
    print(neuron.nodes.tail()) 