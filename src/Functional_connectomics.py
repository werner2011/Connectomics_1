import numpy as np 
import pandas as pd 
import matplotlib.pyplot as plt 
import seaborn as sns 
import scipy 
import networkx as nx 
import bct 
from nilearn import datasets, input_data, plotting, connectome 
from nilearn.connectome import ConnectivityMeasure 
#pobranie atlasu i danych fMRI 
atlas = datasets.fetch_atlas_schaefer_2018(n_rois=100) 
data=datasets.fetch_development_fmri(n_subjects=1) 
functional_data=data.func[0] 
confounds_file=data.confounds[0] 
#wydobycie sygnalow czasowych 
masker = input_data.NiftiLabelsMasker(
    labels_img=atlas.maps, 
    standardize='zscore_sample', 
    memory="nilearn_cache"
) 
#wyodrebnienie sygnalow z uwzglednieniem szumow 
time_series=masker.fit_transform(functional_data, confounds=confounds_file)
#Obliczenie connnectivity matrix 
pomiar_korelacji=ConnectivityMeasure(kind='correlation')
macierz_korelacji=pomiar_korelacji.fit_transform([time_series])[0]

np.fill_diagonal(macierz_korelacji, 0) 
plt.figure(figsize=(10,8))
sns.heatmap(macierz_korelacji, cmap='RdBu_r', center=0) 
plt.title("Macierz Korelacji Funkcjonalnej") 
plt.show() 

#Graf 
prog_polaczen = np.percentile(macierz_korelacji, 80) 
adj_matrix=(macierz_korelacji > prog_polaczen).astype(int) 

#miary wierzcholkow grafu: 
stopnie=bct.degrees_und(adj_matrix) 
clustering=bct.clustering_coef_bu(adj_matrix) 

G=nx.from_numpy_array(adj_matrix) 
print(f"Wspolczynnik klstrowaia: {np.mean(clustering):.3f}") 

df_results=pd.DataFrame({
    'ROI_ID':range(1,101), 
    'Degree':stopnie, 
    'Clustering': clustering 
})
                        