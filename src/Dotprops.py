import navis 
import matplotlib.pyplot as plt 
from pathlib import Path 
import numpy 
PROJECT_DIR = Path.cwd() 
RESULTS_DIR = PROJECT_DIR / 'results' / 'example_navis' 
URL = "https://v2.virtualflybrain.org/data/VFB/i/0010/2926/VFB_00101567/volume.nrrd"
im, header=navis.read_nrrd(URL, output='raw') 

print('Type:', type(im)) 
print('Shape: ', im.shape) 

print('Header:')
for key, values in header.items(): 
    print(key, ":", values) 

maxproj = im.max(axis=2) 

spacing_xy = 0.5189

size_x = spacing_xy * im.shape[0]
size_y = spacing_xy * im.shape[1]

plt.figure(figsize=(10, 6))

plt.imshow(
    maxproj.T,
    extent=(
        0,
        size_x,
        size_y,
        0
    ),
    cmap="Greys_r",
    vmax=10
)

plt.xlabel("x [µm]")
plt.ylabel("y [µm]")
plt.title("LH2094 — Maximum Intensity Projection")

plt.show()