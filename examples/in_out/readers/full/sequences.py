import os
from datarec.io.readers.sequences.tabular import read_sequence_tabular_inline, read_sequence_tabular_wide, read_sequence_tabular_implicit
from datarec.io.readers.sequences.json import read_sequences_json, read_sequences_json_array, read_sequences_json_items
from datarec.datasets.examples import download_example_by_url

output_folder = 'data'
filename = 'dataset.tsv'


# --- SEQUENTIAL DATASETS ---


# --- TABULAR INLINE DATASETS ---

 # interactions only with header
download_example_by_url(output_folder=output_folder, filename=filename, url='https://raw.githubusercontent.com/sisinflab/DataRecDatasets/refs/heads/main/sequences/tabular-inline/interactions/dataset.tsv')
print(read_sequence_tabular_inline(os.path.join(output_folder, filename), user_col='user', sequence_col='item', header=0, col_sep='\t', sequence_sep=';'))

 # interactions only without header
download_example_by_url(output_folder=output_folder, filename=filename, url='https://raw.githubusercontent.com/sisinflab/DataRecDatasets/refs/heads/main/sequences/tabular-inline/interactions/dataset_no_header.tsv')
print(read_sequence_tabular_inline(os.path.join(output_folder, filename), user_col='user', sequence_col='item', col_sep='\t', sequence_sep=';', cols=['user', 'item']))

 # interactions with timestamp and header
download_example_by_url(output_folder=output_folder, filename=filename, url='https://raw.githubusercontent.com/sisinflab/DataRecDatasets/refs/heads/main/sequences/tabular-inline/timestamp/dataset.tsv')
print(read_sequence_tabular_inline(os.path.join(output_folder, filename), user_col='user', sequence_col='item', timestamp_col='timestamp', header=0, col_sep='\t', sequence_sep=';'))

 # interactions with timestamp and no header
download_example_by_url(output_folder=output_folder, filename=filename, url='https://raw.githubusercontent.com/sisinflab/DataRecDatasets/refs/heads/main/sequences/tabular-inline/timestamp/dataset_no_header.tsv')
print(read_sequence_tabular_inline(os.path.join(output_folder, filename), user_col='user', sequence_col='item', timestamp_col='timestamp', header=None, col_sep='\t', sequence_sep=';', cols=['user', 'item', 'timestamp']))


## --- TABULAR WIDE DATASETS ---

 # interactions only with header
download_example_by_url(output_folder=output_folder, filename=filename, url='https://raw.githubusercontent.com/sisinflab/DataRecDatasets/refs/heads/main/sequences/tabular-wide/interactions/dataset.tsv')
print(read_sequence_tabular_wide(os.path.join(output_folder, filename), user_col='user', item_col='item', header=0, col_sep='\t'))

 # interactions only without header
download_example_by_url(output_folder=output_folder, filename=filename, url='https://raw.githubusercontent.com/sisinflab/DataRecDatasets/refs/heads/main/sequences/tabular-wide/interactions/dataset_no_header.tsv')
print(read_sequence_tabular_wide(os.path.join(output_folder, filename), header=None, col_sep='\t'))


## --- TABULAR IMPLICIT DATASETS ---

 # interactions only with header
download_example_by_url(output_folder=output_folder, filename=filename, url='https://raw.githubusercontent.com/sisinflab/DataRecDatasets/refs/heads/main/sequences/tabular-implicit/interactions/dataset.tsv')
print(read_sequence_tabular_implicit(os.path.join(output_folder, filename), user_col='user', item_col='item', header=0, col_sep='\t'))

 # interactions only without header
download_example_by_url(output_folder=output_folder, filename=filename, url='https://raw.githubusercontent.com/sisinflab/DataRecDatasets/refs/heads/main/sequences/tabular-implicit/interactions/dataset_no_header.tsv')
print(read_sequence_tabular_implicit(os.path.join(output_folder, filename), header=None, col_sep='\t'))


## --- JSON DATASETS ---

download_example_by_url(output_folder=output_folder, filename=filename, url='https://raw.githubusercontent.com/sisinflab/DataRecDatasets/refs/heads/main/sequences/json/interactions/dataset.json')
print(read_sequences_json(os.path.join(output_folder, filename), user_col='user', item_col='item'))


download_example_by_url(output_folder=output_folder, filename=filename, url='https://raw.githubusercontent.com/sisinflab/DataRecDatasets/refs/heads/main/sequences/json-items/interactions/dataset.json')
print(read_sequences_json_items(os.path.join(output_folder, filename), user_col='user', item_col='item'))

download_example_by_url(output_folder=output_folder, filename=filename, url='https://raw.githubusercontent.com/sisinflab/DataRecDatasets/refs/heads/main/sequences/json/ratings/dataset.json')
print(read_sequences_json(os.path.join(output_folder, filename), user_col='user', item_col='item', rating_col='rating'))

download_example_by_url(output_folder=output_folder, filename=filename, url='https://raw.githubusercontent.com/sisinflab/DataRecDatasets/refs/heads/main/sequences/json/timestamp/dataset.json')
print(read_sequences_json(os.path.join(output_folder, filename), user_col='user', item_col='item', rating_col='rating', timestamp_col='timestamp'))

## --- JSON ARRAY DATASETS ---

download_example_by_url(output_folder=output_folder, filename=filename, url='https://raw.githubusercontent.com/sisinflab/DataRecDatasets/refs/heads/main/sequences/json-array/interactions/dataset.json')
print(read_sequences_json_array(os.path.join(output_folder, filename), user_col='user', item_col='item', sequence_key='sequence'))

download_example_by_url(output_folder=output_folder, filename=filename, url='https://raw.githubusercontent.com/sisinflab/DataRecDatasets/refs/heads/main/sequences/json-array/ratings/dataset.json')
print(read_sequences_json_array(os.path.join(output_folder, filename), user_col='user', item_col='item', rating_col='rating', sequence_key='sequence'))

download_example_by_url(output_folder=output_folder, filename=filename, url='https://raw.githubusercontent.com/sisinflab/DataRecDatasets/refs/heads/main/sequences/json-array/timestamp/dataset.json')
print(read_sequences_json_array(os.path.join(output_folder, filename), user_col='user', item_col='item', rating_col='rating', timestamp_col='timestamp', sequence_key='sequence'))
