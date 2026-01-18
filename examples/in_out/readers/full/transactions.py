import os
from datarec.io.readers.transactions.tabular import read_transactions_tabular
from datarec.io.readers.transactions.json import read_transactions_json
from datarec.io.readers.transactions.jsonl import read_transactions_jsonl
from datarec.io.readers.transactions.blocks import read_transactions_blocks
from datarec.datasets.examples import download_example_by_url

output_folder = 'data'
filename = 'dataset.tsv'


# --- TRANSACTIONAL DATASETS ---

# -- TABULAR DATASETS --

 # interactions only with header
download_example_by_url(output_folder=output_folder, filename=filename, url='https://raw.githubusercontent.com/sisinflab/DataRecDatasets/refs/heads/main/transactions/tabular/interactions/dataset.tsv')
print(read_transactions_tabular(os.path.join(output_folder, filename), user_col='user', item_col='item', header=0, sep='\t'))

 # interactions only without header
download_example_by_url(output_folder=output_folder, filename=filename, url='https://raw.githubusercontent.com/sisinflab/DataRecDatasets/refs/heads/main/transactions/tabular/interactions/dataset_no_header.tsv')
print(read_transactions_tabular(os.path.join(output_folder, filename), user_col=0, item_col=1, sep='\t'))

 # ratings with header
download_example_by_url(output_folder=output_folder, filename=filename, url='https://raw.githubusercontent.com/sisinflab/DataRecDatasets/refs/heads/main/transactions/tabular/ratings/dataset.tsv')
print(read_transactions_tabular(os.path.join(output_folder, filename), user_col='user', item_col='item', rating_col='ratings', header=0, sep='\t'))

 # ratings without header
download_example_by_url(output_folder=output_folder, filename=filename, url='https://raw.githubusercontent.com/sisinflab/DataRecDatasets/refs/heads/main/transactions/tabular/ratings/dataset_no_header.tsv')
print(read_transactions_tabular(os.path.join(output_folder, filename), user_col=0, item_col=1, rating_col=2, sep='\t'))

 # ratings and timestamp with header
download_example_by_url(output_folder=output_folder, filename=filename, url='https://raw.githubusercontent.com/sisinflab/DataRecDatasets/refs/heads/main/transactions/tabular/timestamp/dataset.tsv')
print(read_transactions_tabular(os.path.join(output_folder, filename), user_col='user', item_col='item', rating_col='ratings', timestamp_col='timestamp', header=0, sep='\t'))

 # ratings and timestamp without header
download_example_by_url(output_folder=output_folder, filename=filename, url='https://raw.githubusercontent.com/sisinflab/DataRecDatasets/refs/heads/main/transactions/tabular/timestamp/dataset_no_header.tsv')
print(read_transactions_tabular(os.path.join(output_folder, filename), user_col=0, item_col=1, rating_col=2, timestamp_col=3, sep='\t'))


# # -- JSON DATASETS --

 # interactions only
download_example_by_url(output_folder=output_folder, filename=filename, url='https://raw.githubusercontent.com/sisinflab/DataRecDatasets/refs/heads/main/transactions/json/interactions/dataset.json')
print(read_transactions_json(os.path.join(output_folder, filename), user_col='user', item_col='item'))

 # ratings
download_example_by_url(output_folder=output_folder, filename=filename, url='https://raw.githubusercontent.com/sisinflab/DataRecDatasets/refs/heads/main/transactions/json/ratings/dataset.json')
print(read_transactions_json(os.path.join(output_folder, filename), user_col='user', item_col='item', rating_col='rating'))

 # ratings with timestamp
download_example_by_url(output_folder=output_folder, filename=filename, url='https://raw.githubusercontent.com/sisinflab/DataRecDatasets/refs/heads/main/transactions/json/timestamp/dataset.json')
print(read_transactions_json(os.path.join(output_folder, filename), user_col='user', item_col='item', rating_col='rating', timestamp_col='timestamp'))


# # -- JSON LINES DATASETS --

 # interactions only
download_example_by_url(output_folder=output_folder, filename=filename, url='https://raw.githubusercontent.com/sisinflab/DataRecDatasets/refs/heads/main/transactions/jsonl/interactions/dataset.json')
print(read_transactions_jsonl(os.path.join(output_folder, filename), user_col='user', item_col='item'))

 # ratings
download_example_by_url(output_folder=output_folder, filename=filename, url='https://raw.githubusercontent.com/sisinflab/DataRecDatasets/refs/heads/main/transactions/jsonl/ratings/dataset.json')
print(read_transactions_jsonl(os.path.join(output_folder, filename), user_col='user', item_col='item', rating_col='rating'))

 # ratings with timestamp
download_example_by_url(output_folder=output_folder, filename=filename, url='https://raw.githubusercontent.com/sisinflab/DataRecDatasets/refs/heads/main/transactions/jsonl/timestamp/dataset.json')
print(read_transactions_jsonl(os.path.join(output_folder, filename), user_col='user', item_col='item', rating_col='rating', timestamp_col='timestamp'))


# # -- BLOCKS DATASETS --

 # item-wise blocks: id
download_example_by_url(output_folder=output_folder, filename=filename, url='https://raw.githubusercontent.com/sisinflab/DataRecDatasets/refs/heads/main/transactions/blocks_items/interactions/dataset.tsv')
print(read_transactions_blocks(os.path.join(output_folder, filename), block_by='item', event_layout='id', user_col='user', item_col='item', sep='\t'))

 # item-wise blocks: id,rating
download_example_by_url(output_folder=output_folder, filename=filename, url='https://raw.githubusercontent.com/sisinflab/DataRecDatasets/refs/heads/main/transactions/blocks_items/ratings/dataset.tsv')
print(read_transactions_blocks(os.path.join(output_folder, filename), block_by='item', event_layout='id,rating', user_col='user', item_col='item', rating_col='rating', sep='\t'))

 # item-wise blocks: id,rating,timestamp
download_example_by_url(output_folder=output_folder, filename=filename, url='https://raw.githubusercontent.com/sisinflab/DataRecDatasets/refs/heads/main/transactions/blocks_items/timestamp/dataset.tsv')
print(read_transactions_blocks(os.path.join(output_folder, filename), block_by='item', event_layout='id,rating,timestamp', user_col='user', item_col='item', rating_col='rating', timestamp_col='timestamp', sep='\t'))

 # user-wise blocks: id
download_example_by_url(output_folder=output_folder, filename=filename, url='https://raw.githubusercontent.com/sisinflab/DataRecDatasets/refs/heads/main/transactions/blocks_users/interactions/dataset.tsv')
print(read_transactions_blocks(os.path.join(output_folder, filename), block_by='user', event_layout='id', user_col='user', item_col='item', sep='\t'))

 # user-wise blocks: id,rating
download_example_by_url(output_folder=output_folder, filename=filename, url='https://raw.githubusercontent.com/sisinflab/DataRecDatasets/refs/heads/main/transactions/blocks_users/ratings/dataset.tsv')
print(read_transactions_blocks(os.path.join(output_folder, filename), block_by='user', event_layout='id,rating', user_col='user', item_col='item', rating_col='rating', sep='\t'))

 # user-wise blocks: id,rating,timestamp
download_example_by_url(output_folder=output_folder, filename=filename, url='https://raw.githubusercontent.com/sisinflab/DataRecDatasets/refs/heads/main/transactions/blocks_users/timestamp/dataset.tsv')
print(read_transactions_blocks(os.path.join(output_folder, filename), block_by='user', event_layout='id,rating,timestamp', user_col='user', item_col='item', rating_col='rating', timestamp_col='timestamp', sep='\t'))
