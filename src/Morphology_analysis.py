from pathlib import Path 
import navis 
import numpy as np 
import pandas as pd 
import matplotlib.pyplot as plt 

from Example_neurons import zapisz_plik 
RESULTS_DIR = Path.cwd() / 'results' / 'example_navis' / 'morphology_analysis' 
RESULTS_DIR.mkdir(parents=True, exist_ok=True) 

def analyze_segments(neuron:navis.TreeNeuron):
    """
    Analiza liniowych segmentów neuronu.

    NAVIS zwraca m.in.:
    - length
    - tortuosity
    - root_dist
    - strahler_index
    """
    segments = navis.segment_analysis(neuron) 
    segments.insert(0, 'segment_id', range(len(segments))) 
    return segments 

def analyze_geodesic_distance(neuron: navis.TreeNeuron): 
    """
    Oblicza geodezyjną odległość każdego węzła od korzenia.

    weight='weight' oznacza wykorzystanie rzeczywistych
    długości krawędzi zamiast liczby krawędzi.
    """
    distances = navis.dist_to_root(neuron,weight="weight")

    df = neuron.nodes[
        ["node_id", "type"]
    ].copy()

    df["distance_to_root"] = (
        df["node_id"].map(distances)
    )

    return df

def analyze_angles(neuron: navis.TreeNeuron):
    """
    Analizuje:
    - branch angles
    - path angles
    """
    branch_angles = navis.branch_angles(neuron)
    path_angles = navis.path_angles(neuron)

    return branch_angles, path_angles

def analyze_sholl(neuron: navis.TreeNeuron, n_radii=30):
    """
    Klasyczna analiza Sholla.
    Liczy przecięcia arboru z koncentrycznymi
    sferami wokół somy/root.
    """
    if neuron.has_soma:
        center = "soma"
    elif len(neuron.root) == 1:
        center = "root"
    else:
        center = "centermass"

    sholl = navis.sholl_analysis(neuron,center=center,radii=n_radii)
    return sholl

def summarize_morphology(neuron,segments,geodesic,branch_angles,path_angles,sholl):
    """
    Tworzy jeden wiersz podsumowania dla neuronu.
    """
    tortuosity = segments["tortuosity"].replace([np.inf, -np.inf], np.nan)

    if not sholl.empty:
        max_intersections = (
            sholl["intersections"].max()
        )
        peak_radius = (
            sholl["intersections"].idxmax()
        )

    else:
        max_intersections = np.nan
        peak_radius = np.nan

    return {
        "id": neuron.id,
        "name": neuron.name,
        "units": str(neuron.units),
        # Segmenty
        "n_segments":len(segments),
        "segment_length_mean":segments["length"].mean(),
        "segment_length_median":segments["length"].median(),
        "segment_length_max":segments["length"].max(),

        # Geodesic
        "geodesic_mean":geodesic["distance_to_root"].mean(),
        "geodesic_max":geodesic["distance_to_root"].max(),

        # Tortuosity
        "tortuosity_mean":tortuosity.mean(),
        "tortuosity_median": tortuosity.median(),
        "tortuosity_max": tortuosity.max(),

        # Branch angles
        "branch_angle_mean": branch_angles["branch_angle"].mean(),
        "branch_angle_median": branch_angles["branch_angle"].median(),

        # Path angles
        "path_angle_mean": path_angles["path_angle"].mean(),
        "path_angle_median": path_angles["path_angle"].median(),

        # Sholl
        "sholl_max_intersections": max_intersections,
        "sholl_peak_radius": peak_radius,
    }

def plot_distribution(df,column,title, xlabel):
    """
    Prosty histogram rozkładu wybranej cechy.
    """
    values = (
        df[column]
        .replace([np.inf, -np.inf], np.nan)
        .dropna()
    )

    if len(values) == 0:
        return None

    fig, ax = plt.subplots(figsize=(7, 5))

    ax.hist(values,bins=30)
    ax.set_title(title)
    ax.set_xlabel(xlabel)
    ax.set_ylabel("Count")
    fig.tight_layout()
    return fig

def plot_sholl(sholl,neuron):
    """
    Wykres liczby przecięć w funkcji promienia.
    """
    fig, ax = plt.subplots(figsize=(7, 5))

    ax.plot(sholl.index,sholl["intersections"],marker="o",markersize=3)
    ax.set_xlabel(f"Radius [{neuron.units}]")
    ax.set_ylabel("Number of intersections")
    ax.set_title(f"Sholl analysis - {neuron.id}")
    fig.tight_layout()
    return fig

def main() -> None:
    neurony = navis.example_neurons(n=3,kind="skeleton")
    summary = []
    for neuron in neurony:
        segments = analyze_segments(neuron)
        zapisz_plik(segments,f"segments_{neuron.id}.csv",results_dir=RESULTS_DIR)

        geodesic = analyze_geodesic_distance(neuron)
        zapisz_plik(geodesic,f"geodesic_{neuron.id}.csv",results_dir=RESULTS_DIR)

        branch_angles, path_angles = (analyze_angles(neuron))
        zapisz_plik(branch_angles,f"branch_angles_{neuron.id}.csv",results_dir=RESULTS_DIR)
        zapisz_plik(path_angles,f"path_angles_{neuron.id}.csv",results_dir=RESULTS_DIR)

        sholl = analyze_sholl(neuron, n_radii=30)
        sholl_to_save = ( sholl.reset_index())
        zapisz_plik( sholl_to_save,f"sholl_{neuron.id}.csv",results_dir=RESULTS_DIR)
        row = summarize_morphology(neuron, segments, geodesic, branch_angles, path_angles, sholl)
        summary.append(row)
        fig = plot_distribution(segments,"length",f"Segment length - {neuron.id}",f"Segment length [{neuron.units}]" )

        if fig is not None:
            zapisz_plik( fig, f"segment_length_{neuron.id}.png",results_dir=RESULTS_DIR)
            plt.close(fig)

        fig = plot_distribution(segments,"tortuosity",f"Tortuosity - {neuron.id}","Tortuosity" )
        if fig is not None:
            zapisz_plik( fig, f"tortuosity_{neuron.id}.png", results_dir=RESULTS_DIR)

            plt.close(fig)

        fig = plot_distribution(geodesic, "distance_to_root", f"Distance to root - {neuron.id}",f"Geodesic distance [{neuron.units}]")

        if fig is not None:
            zapisz_plik(fig,f"geodesic_{neuron.id}.png",results_dir=RESULTS_DIR)
            plt.close(fig)

        fig = plot_distribution(branch_angles,"branch_angle",f"Branch angles - {neuron.id}","Branch angle [degrees]" )
        if fig is not None:
            zapisz_plik( fig,f"branch_angles_{neuron.id}.png",results_dir=RESULTS_DIR)
            plt.close(fig)
        fig = plot_distribution( path_angles, "path_angle", f"Path angles - {neuron.id}", "Path angle [degrees]")

        if fig is not None:
            zapisz_plik(fig, f"path_angles_{neuron.id}.png", results_dir=RESULTS_DIR)
            plt.close(fig)

        fig = plot_sholl(sholl,neuron)
        zapisz_plik(fig,f"sholl_{neuron.id}.png",results_dir=RESULTS_DIR)
        plt.close(fig)

    summary_df = pd.DataFrame(summary)
    print()
    print(summary_df)
    zapisz_plik(summary_df,"morphology_summary.csv",results_dir=RESULTS_DIR)


if __name__ == "__main__":
    main()