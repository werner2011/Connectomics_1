import navis 
import matplotlib.pyplot as plt 
import plotly 
from pathlib import Path 
import numpy as np 
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

def zbuduj_mesh(): 
    """Buduje strukture mesh""" 
    vertices = np.array([
        [0,1,0], 
        [1,0,1], 
        [1,0,0], 
        [1,0,0]
    ])

    faces = np.array(
        [
            [0,1,2]
        ]
    )
    my_mesh = navis.MeshNeuron({'vertices': vertices, 'faces': faces}, name='my_mesh', id=1, units='micrometers') 
    print(my_mesh.name) 
    fig = navis.plot3d(my_mesh) 
    fig.show()


def inspect_TreeNeuron(neuron: navis.TreeNeuron): 
    print('*' * 60) 
    print('ID: ', neuron.id) 
    print('Name: ', neuron.name) 
    print('Nodes: ', neuron.nodes) 
    print('Branches: ', neuron.n_branches) 
    print('Leafs: ', neuron.n_leafs) 
    print('Type: ', type(neuron))
    print('Root: ', neuron.root) 
    print('Soma: ', neuron.soma) 
    print('Cable length: ', neuron.cable_length) 
    print('Units: ', neuron.units) 

    print('\nNode columns: ')
    print(neuron.nodes.columns) 

    print("\n Node types") 
    print(neuron.nodes['type'].value_counts()) 

def Mesh_neuron(neuron: navis.TreeNeuron) -> navis.MeshNeuron: 
    """Funkcja zamienia format TreeNeuron na MeshNeuron"""
    return navis.mesh(neuron)

def inspect_MeshNeuron(neuron: navis.MeshNeuron): 
    print('*' * 60) 
    print('Vertices and faces: ', neuron.vertices) 
    print('Volume: ', neuron.volume) 
    print('Pozycja somy: ', neuron.soma_pos)

def Voxel_neuron(neuron: navis.TreeNeuron) -> navis.VoxelNeuron: 
    """Funkcja zamienia typ neuronu na VoxelNeuron""" 
    return navis.voxelize(neuron, pitch=0.5) 

def inspect_VoxelNeuron(neuron: navis.VoxelNeuron): 
    print('*' * 60) 
    print('Voxels: ', neuron.voxels) 
    print('Grid: ', neuron.grid) 

def Dotprops_neuron(neuron:navis.TreeNeuron): 
    return navis.make_dotprops(neuron) 

def inspectDotprops(neuron: navis.Dotprops):
    print('Points: ', neuron.points) 
    print('Vect: ', neuron.vect) 

if __name__=="__main__": 
    neuron = navis.read_swc(DATA_DIR / 'n1.swc') 
    inspect_TreeNeuron(neuron=neuron)
    mesh_neuron = Mesh_neuron(neuron=neuron) 
    inspect_MeshNeuron(mesh_neuron)
    voxel_n = Voxel_neuron(neuron=neuron) 
    inspect_VoxelNeuron(voxel_n) 
    dotprops_neu = Dotprops_neuron(neuron=neuron) 
    inspectDotprops(dotprops_neu) 

    zbuduj_mesh() 