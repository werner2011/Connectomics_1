from pathlib import Path 
from urllib.parse import quote 
import requests 

PROJECT_DIR = Path(__file__).resolve().parents[1] 
DATA_DIR = PROJECT_DIR / 'data' / 'Neuromorpho' 
SWC_DIR = DATA_DIR / 'raw_swc' 

API_URL = 'https://neuromorpho.org/api' 

def znajdz_neurony(species, brain_region=None, cell_type=None, limit=10):
    params = {
        'q': f'species:{species}', 
        'size': limit
    }
    filters=[] 

    if brain_region:
        filters.append(f'brain_region:{brain_region}') 

    if cell_type:
        filters.append(f'cell_type:{cell_type}') 

    if filters:
        params['fq'] = filters 

    response = requests.get(f'{API_URL}/neuron/select', params=params, timeout=30) 
    response.raise_for_status() 

    data = response.json() 

    neurony = (
        data.get('_embedded', {}).get('neuronResources', [])
    )

    return neurony 

def pobierz_swc(neuron): 
    SWC_DIR.mkdir(parents=True, exist_ok=True) 
    neuron_name = neuron['neuron_name'] 
    archive = neuron['archive'].lower() 

    name_url = quote(neuron_name) 
    archive_url = quote(archive) 

    url=(
        "https://neuromorpho.org/dableFiles/"
        f"{archive_url}/"
        f"CNG%20version/"
        f"{name_url}.CNG.swc"
    )
    output_file = SWC_DIR / f'{neuron_name}.swc' 

    response = requests.get(url, timeout=60) 
    response.raise_for_status()

    output_file.write_bytes(response.content) 

    print(f'Pobrano: {neuron_name}') 
    return output_file 

if __name__=="__main__":
    neurons = znajdz_neurony(species='human', cell_type='pyramidal', limit=5) 

    for neuron in neurons:
        print('\n=================================') 

        print('ID: ')
        print(neuron['neuron_id']) 

        print('Name: ')
        print(neuron['neuron_name']) 

        print('Archive: ')
        print(neuron['archive']) 

        print('Brain region: ')
        print(neuron['brain_region']) 

        print('Cell type: ')
        print(neuron['cell_type']) 

        pobierz_swc(neuron)