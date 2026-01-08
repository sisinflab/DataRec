import os
from datarec.io.readers.transactions.tabular import read_transactions_tabular
from datarec.io.readers.transactions.json import read_transactions_json
from datarec.io.readers.transactions.jsonl import read_transactions_jsonl
from datarec.datasets.examples import download_example_by_url

output_folder = 'data'
filename = 'dataset.tsv'


# --- TRANSACTIONAL DATASETS (chunked examples where supported) ---

# -- TABULAR DATASETS --

 # interactions only with header (stream)
download_example_by_url(output_folder=output_folder, filename=filename, url='https://raw.githubusercontent.com/sisinflab/DataRecDatasets/refs/heads/main/transactions/tabular/interactions/dataset.tsv')
print(read_transactions_tabular(os.path.join(output_folder, filename), user_col='user', item_col='item', header=0, sep='\t', stream=True))

 # interactions only without header (stream)
download_example_by_url(output_folder=output_folder, filename=filename, url='https://raw.githubusercontent.com/sisinflab/DataRecDatasets/refs/heads/main/transactions/tabular/interactions/dataset_no_header.tsv')
print(read_transactions_tabular(os.path.join(output_folder, filename), user_col=0, item_col=1, sep='\t', stream=True))

 # ratings with header (stream)
download_example_by_url(output_folder=output_folder, filename=filename, url='https://raw.githubusercontent.com/sisinflab/DataRecDatasets/refs/heads/main/transactions/tabular/ratings/dataset.tsv')
print(read_transactions_tabular(os.path.join(output_folder, filename), user_col='user', item_col='item', rating_col='ratings', header=0, sep='\t', stream=True))

 # ratings without header (stream)
download_example_by_url(output_folder=output_folder, filename=filename, url='https://raw.githubusercontent.com/sisinflab/DataRecDatasets/refs/heads/main/transactions/tabular/ratings/dataset_no_header.tsv')
print(read_transactions_tabular(os.path.join(output_folder, filename), user_col=0, item_col=1, rating_col=2, sep='\t', stream=True))

 # ratings and timestamp with header (stream)
download_example_by_url(output_folder=output_folder, filename=filename, url='https://raw.githubusercontent.com/sisinflab/DataRecDatasets/refs/heads/main/transactions/tabular/timestamp/dataset.tsv')
print(read_transactions_tabular(os.path.join(output_folder, filename), user_col='user', item_col='item', rating_col='ratings', timestamp_col='timestamp', header=0, sep='\t', stream=True))

 # ratings and timestamp without header (stream)
download_example_by_url(output_folder=output_folder, filename=filename, url='https://raw.githubusercontent.com/sisinflab/DataRecDatasets/refs/heads/main/transactions/tabular/timestamp/dataset_no_header.tsv')
print(read_transactions_tabular(os.path.join(output_folder, filename), user_col=0, item_col=1, rating_col=2, timestamp_col=3, sep='\t', stream=True))


# # -- JSON LINES DATASETS --

 # interactions only
download_example_by_url(output_folder=output_folder, filename=filename, url='https://raw.githubusercontent.com/sisinflab/DataRecDatasets/refs/heads/main/transactions/jsonl/interactions/dataset.json')
print(read_transactions_jsonl(os.path.join(output_folder, filename), user_col='user', item_col='item', stream=True))

 # ratings
download_example_by_url(output_folder=output_folder, filename=filename, url='https://raw.githubusercontent.com/sisinflab/DataRecDatasets/refs/heads/main/transactions/jsonl/ratings/dataset.json')
print(read_transactions_jsonl(os.path.join(output_folder, filename), user_col='user', item_col='item', rating_col='rating', stream=True))

 # ratings with timestamp
download_example_by_url(output_folder=output_folder, filename=filename, url='https://raw.githubusercontent.com/sisinflab/DataRecDatasets/refs/heads/main/transactions/jsonl/timestamp/dataset.json')
print(read_transactions_jsonl(os.path.join(output_folder, filename), user_col='user', item_col='item', rating_col='rating', timestamp_col='timestamp', stream=True))
