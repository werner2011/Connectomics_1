from pathlib import Path
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import networkx as nx
import navis


# ============================================================
# USTAWIENIA ŚCIEŻEK
# ============================================================
DATA_NEUROMORPHO = Path("data/neuromorpho/raw_swc")
OUT_DIR = Path("results/neuromorpho")
OUT_DIR.mkdir(parents=True, exist_ok=True)


# ============================================================
# FUNKCJA: wczytanie neuronów SWC
# ============================================================
def wczytaj_neurony(folder: Path) -> tuple[navis.NeuronList, list]:
    """
    Wczytuje wszystkie pliki .swc z folderu.
    Pomija błędne pliki i zapisuje listę błędów.

    Zwraca:
        neurony : navis.NeuronList
        bledy   : lista krotek (nazwa_pliku, komunikat_bledu)
    """
    swc_pliki = sorted(folder.glob("*.swc"))

    if not swc_pliki:
        raise FileNotFoundError(
            f"Brak plików .swc w folderze: {folder.resolve()}\n"
            f"Upewnij się, że masz prawdziwe pliki SWC, a nie .std."
        )

    print("=" * 70)
    print("ZNALEZIONE PLIKI SWC")
    print("=" * 70)
    for p in swc_pliki:
        print(" -", p.name)

    dobre_neurony = []
    bledy = []

    for p in swc_pliki:
        try:
            n = navis.read_swc(p)

            if isinstance(n, navis.NeuronList):
                for obj in n:
                    if getattr(obj, "name", None) in [None, "None", ""]:
                        try:
                            obj.name = p.stem
                        except Exception:
                            pass
                    dobre_neurony.append(obj)
            else:
                if getattr(n, "name", None) in [None, "None", ""]:
                    try:
                        n.name = p.stem
                    except Exception:
                        pass
                dobre_neurony.append(n)

            print(f"OK   {p.name}")

        except Exception as e:
            print(f"BLAD {p.name}: {e}")
            bledy.append((p.name, str(e)))

    neurony = navis.NeuronList(dobre_neurony)
    return neurony, bledy


# ============================================================
# FUNKCJA: budowa grafu z neuronu
# ============================================================
def zbuduj_graf(neuron):
    """
    Buduje graf NetworkX z neuronu navis.
    Każdy węzeł ma współrzędne x,y,z.
    Każda krawędź ma wagę = długość segmentu w 3D.
    """
    nodes = neuron.nodes.copy()
    graf = nx.Graph()

    # Dodanie węzłów
    for row in nodes.itertuples(index=False):
        graf.add_node(
            int(row.node_id),
            x=float(row.x),
            y=float(row.y),
            z=float(row.z),
            radius=float(getattr(row, "radius", 0.0)),
            parent_id=int(row.parent_id),
            swc_type=int(getattr(row, "type", 0)),
        )

    # Tabela współrzędnych
    coords = nodes.set_index("node_id")[["x", "y", "z"]]

    # Dodawanie krawędzi
    dlugosci = []
    valid_edges = nodes.loc[nodes["parent_id"] >= 0, ["parent_id", "node_id"]].copy()

    for row in valid_edges.itertuples(index=False):
        parent_id = int(row.parent_id)
        child_id = int(row.node_id)

        if parent_id not in coords.index or child_id not in coords.index:
            continue

        p = coords.loc[parent_id].to_numpy(dtype=float)
        c = coords.loc[child_id].to_numpy(dtype=float)

        length = float(np.linalg.norm(c - p))

        graf.add_edge(parent_id, child_id, weight=length)
        dlugosci.append(length)

    total_length = float(np.sum(dlugosci)) if dlugosci else 0.0
    return graf, total_length


# ============================================================
# FUNKCJA: znalezienie roota
# ============================================================
def find_root_id(nodes_df):
    roots = nodes_df.loc[nodes_df["parent_id"] < 0, "node_id"].tolist()
    return int(roots[0]) if roots else None


# ============================================================
# FUNKCJA: metryki grafowo-morfologiczne
# ============================================================
def metryki_grafu(neuron):
    """
    Liczy podstawowe metryki grafowe i morfologiczne dla jednego neuronu.
    """
    nodes = neuron.nodes.copy()
    G, total_cable_length = zbuduj_graf(neuron)
    root_id = find_root_id(nodes)

    degrees = dict(G.degree())
    leaf_nodes = [n for n, d in degrees.items() if d == 1 and n != root_id]
    branch_nodes = [n for n, d in degrees.items() if d >= 3]

    # Najdłuższa ścieżka od roota do liścia
    max_root_leaf = np.nan
    farthest_leaf = None

    if root_id is not None and leaf_nodes:
        path_lengths = {}
        for leaf in leaf_nodes:
            try:
                path_lengths[leaf] = nx.shortest_path_length(
                    G,
                    source=root_id,
                    target=leaf,
                    weight="weight"
                )
            except nx.NetworkXNoPath:
                continue

        if path_lengths:
            farthest_leaf = max(path_lengths, key=path_lengths.get)
            max_root_leaf = float(path_lengths[farthest_leaf])

    # Średnia długość segmentu
    edge_weights = [d["weight"] for _, _, d in G.edges(data=True)]
    mean_edge_length = float(np.mean(edge_weights)) if edge_weights else np.nan

    # Centralność pośrednictwa
    if G.number_of_nodes() > 1:
        bet = nx.betweenness_centrality(G, weight="weight", normalized=True)
        max_bet = max(bet.values()) if bet else np.nan
    else:
        max_bet = np.nan

    neuron_id = getattr(neuron, "id", None)
    neuron_name = getattr(neuron, "name", None)

    return {
        "id": neuron_id,
        "name": neuron_name,
        "n_nodes": int(len(nodes)),
        "n_edges": int(G.number_of_edges()),
        "n_leafs": int(len(leaf_nodes)),
        "n_branch_points": int(len(branch_nodes)),
        "root_id": root_id,
        "total_cable_length": total_cable_length,
        "mean_edge_length": mean_edge_length,
        "max_root_to_leaf_length": max_root_leaf,
        "farthest_leaf_id": farthest_leaf,
        "max_betweenness": max_bet,
    }


# ============================================================
# FUNKCJA: zapis tabel węzłów
# ============================================================
def zapisz_tabele_wezlow(neurony, out_dir: Path):
    node_tables_dir = out_dir / "node_tables"
    node_tables_dir.mkdir(exist_ok=True)

    for idx, n in enumerate(neurony):
        df = n.nodes.copy()
        fname = f"neuron_{idx:03d}_nodes.csv"
        df.to_csv(node_tables_dir / fname, index=False)


# ============================================================
# FUNKCJA: zapis wykresów
# ============================================================
def zapisz_wykresy(neurony, summary_df, out_dir: Path):
    if len(neurony) > 0:
        n_show = min(6, len(neurony))
        fig, ax = plt.subplots(figsize=(10, 10))
        navis.plot2d(neurony[:n_show], ax=ax, radius=False)
        ax.set_title(f"Pierwsze {n_show} neurony z NeuroMorpho")
        plt.tight_layout()
        plt.savefig(out_dir / "neurons_2d.png", dpi=220)
        plt.close()

    if not summary_df.empty:
        fig, ax = plt.subplots(figsize=(10, 5))
        ax.bar(range(len(summary_df)), summary_df["total_cable_length"])
        ax.set_xlabel("Neuron index")
        ax.set_ylabel("Total cable length")
        ax.set_title("Porównanie całkowitej długości neuritu")
        plt.tight_layout()
        plt.savefig(out_dir / "total_cable_length_barplot.png", dpi=220)
        plt.close()


# ============================================================
# FUNKCJA: opcjonalna macierz geodezyjna
# ============================================================
def zapisz_geodesic_matrix(neurony, out_dir: Path):
    try:
        if len(neurony) == 0:
            return

        first = neurony[0]
        geo = navis.geodesic_matrix(first)
        pd.DataFrame(geo).to_csv(
            out_dir / "first_neuron_geodesic_matrix.csv",
            index=False
        )
        print("Zapisano geodesic matrix dla pierwszego neuronu.")
    except Exception as e:
        print("Nie udało się policzyć geodesic_matrix:", e)


# ============================================================
# FUNKCJA: opcjonalny wykres 3D
# ============================================================
def zapisz_3d_html(neurony, out_dir: Path):
    try:
        if len(neurony) == 0:
            return

        fig3d = navis.plot3d(neurony[:min(3, len(neurony))], backend="plotly")
        fig3d.write_html(out_dir / "neurons_3d.html")
        print("Zapisano interaktywne 3D:", out_dir / "neurons_3d.html")
    except Exception as e:
        print("Nie udało się zapisać 3D HTML:", e)


# ============================================================
# GŁÓWNA CZĘŚĆ PROGRAMU
# ============================================================
def main():
    neurony, bledy = wczytaj_neurony(DATA_NEUROMORPHO)

    print("\n" + "=" * 70)
    print("PODSUMOWANIE WCZYTYWANIA")
    print("=" * 70)
    print(f"Wczytano poprawnie: {len(neurony)} neuronów")
    print(f"Błędnych plików: {len(bledy)}")

    if bledy:
        df_bledy = pd.DataFrame(bledy, columns=["filename", "error"])
        df_bledy.to_csv(OUT_DIR / "bledne_pliki.csv", index=False)
        print("Lista błędów zapisana do:", OUT_DIR / "bledne_pliki.csv")

    if len(neurony) == 0:
        raise RuntimeError("Nie udało się wczytać żadnego poprawnego neuronu.")

    print("\nObiekt NeuronList:")
    print(neurony)

    # Analiza metryk
    rows = []
    for i, n in enumerate(neurony):
        print(f"\nAnaliza neuronu {i+1}/{len(neurony)}")
        print("id:", getattr(n, "id", None), "name:", getattr(n, "name", None))

        try:
            row = metryki_grafu(n)
            rows.append(row)
        except Exception as e:
            print(f"Błąd analizy neuronu {i+1}: {e}")

    summary_df = pd.DataFrame(rows)
    summary_df.to_csv(OUT_DIR / "summary_metrics.csv", index=False)

    print("\nPODSUMOWANIE METRYK:")
    print(summary_df)

    # Zapis tabel węzłów
    zapisz_tabele_wezlow(neurony, OUT_DIR)

    # Wykresy
    zapisz_wykresy(neurony, summary_df, OUT_DIR)

    # Opcjonalnie geodesic matrix
    zapisz_geodesic_matrix(neurony, OUT_DIR)

    # Opcjonalnie interaktywne 3D
    zapisz_3d_html(neurony, OUT_DIR)

    print("\nGotowe. Wyniki zapisane w:", OUT_DIR.resolve())


if __name__ == "__main__":
    main()