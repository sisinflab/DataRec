from datarec.processing import ItemKCore
import os
from datarec.datasets.examples import download_example_by_url
from datarec.io.readers.sequences.json import read_sequences_json

input_folder = './data'
output_folder = './output'
filename = 'dataset.json'

if __name__ == '__main__':

    download_example_by_url(output_folder=input_folder, filename=filename, url='https://raw.githubusercontent.com/sisinflab/DataRecDatasets/refs/heads/main/sequences/json/interactions/dataset.json')
    datarec = read_sequences_json(filepath=os.path.join(input_folder, filename), user_col='user', item_col='item', dataset_name='Test', version_name='v1')

    print(f"Original dataset: {datarec.n_users} users, {datarec.n_items} items, {len(datarec)} interactions.")
    print(f"Original pipeline length: {len(datarec.pipeline.steps)}\n")
    
    k_core_filter = ItemKCore(core=2)
    datarec_filtered = k_core_filter.run(datarec)
    print(f"Dataset after iterative k-Core: {datarec_filtered.n_users} users, {datarec_filtered.n_items} items, {len(datarec_filtered)} interactions.")
    print(f"Pipeline length: {len(datarec_filtered.pipeline.steps)}")

    print(datarec_filtered)
    print(datarec_filtered.pipeline)

    dr = datarec_filtered.pipeline.apply(input_folder=input_folder, output_folder=output_folder)
    print(dr.dataset_name, dr.version_name)

    print(dr)
    
