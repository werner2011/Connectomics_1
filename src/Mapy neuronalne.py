import navis 
import matplotlib.pyplot as plt 
import networkx as nx 
import numpy as np 

def DAG_neuron(): 
    """
    Opis formy TreeNeuron
    """
    neuron = navis.example_neurons(n=1, kind='skeleton') 
    print(neuron.nodes.head()) 

def Mesh_neuron():
    """
    Neuron w formie siatki
    """
    neuron = navis.example_neurons(n=1, kind='mesh') 
    print(neuron.vertices[1]) 
    print(neuron.faces[0])


if __name__=="__main__": 
    DAG_neuron() 
    Mesh_neuron()