from nilearn.datasets import fetch_atlas_harvard_oxford
from nilearn import plotting 
import matplotlib.pyplot as plt 
atlas = fetch_atlas_harvard_oxford("cort-maxprob-thr25-2mm") 
print("Sciezka do pliku atlasu:", atlas.maps) 
print("10 regioow z atlasu") 

for i, label in enumerate(atlas.labels[:10]): 
    print(f'{i}: {label}') 

#wizualizacja atlasu 
plotting.plot_roi(
    atlas.maps, 
    title = "Atlas Harvard-Oxford - kora",  
    display_mode="ortho", 
    cut_coords = (0, -20, 20), 
    colorbar=True 
)
plt.show() 