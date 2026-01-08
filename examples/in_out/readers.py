import os
from datarec.io import read_json, read_sequence_column, read_sequence_wide, read_transactions
from datarec.data.dataset import DataRec
from datarec.datasets.examples import download_example_by_url

output_folder = 'data'
filename = 'dataset.tsv'


# --- TRANSACTIONAL DATASETS ---

# -- TABULAR DATASETS --

 # transaction interactions only with header
download_example_by_url(output_folder=output_folder, filename=filename, url='https://raw.githubusercontent.com/sisinflab/DataRecDatasets/refs/heads/main/transactions/tabular/interactions/dataset.tsv')
print(read_transactions(os.path.join(output_folder, filename), user_col='user', item_col='item', header=0, sep='\t'))

 # transaction interactions only without header
download_example_by_url(output_folder=output_folder, filename=filename, url='https://raw.githubusercontent.com/sisinflab/DataRecDatasets/refs/heads/main/transactions/tabular/interactions/dataset_no_header.tsv')
print(read_transactions(os.path.join(output_folder, filename), user_col=0, item_col=1, sep='\t'))

 # transaction ratings with header
download_example_by_url(output_folder=output_folder, filename=filename, url='https://raw.githubusercontent.com/sisinflab/DataRecDatasets/refs/heads/main/transactions/tabular/ratings/dataset.tsv')
print(read_transactions(os.path.join(output_folder, filename), user_col='user', item_col='item', rating_col='ratings', header=0, sep='\t'))

 # transaction ratings without header
download_example_by_url(output_folder=output_folder, filename=filename, url='https://raw.githubusercontent.com/sisinflab/DataRecDatasets/refs/heads/main/transactions/tabular/ratings/dataset_no_header.tsv')
print(read_transactions(os.path.join(output_folder, filename), user_col=0, item_col=1, rating_col=2, sep='\t'))

 # transaction ratings and timestamp with header
download_example_by_url(output_folder=output_folder, filename=filename, url='https://raw.githubusercontent.com/sisinflab/DataRecDatasets/refs/heads/main/transactions/tabular/timestamp/dataset.tsv')
print(read_transactions(os.path.join(output_folder, filename), user_col='user', item_col='item', rating_col='ratings', timestamp_col='timestamp', header=0, sep='\t'))

 # transaction ratings and timestamp without header
download_example_by_url(output_folder=output_folder, filename=filename, url='https://raw.githubusercontent.com/sisinflab/DataRecDatasets/refs/heads/main/transactions/tabular/timestamp/dataset_no_header.tsv')
print(read_transactions(os.path.join(output_folder, filename), user_col=0, item_col=1, rating_col=2, timestamp_col=3, sep='\t'))


# -- JSON DATASETS --

 # transaction ratings and timestamp with header
download_example_by_url(output_folder=output_folder, filename=filename, url='https://raw.githubusercontent.com/sisinflab/DataRecDatasets/refs/heads/main/transactions/tabular/timestamp/dataset.tsv')
print(read_transactions(os.path.join(output_folder, filename), user_col='user', item_col='item', rating_col='ratings', timestamp_col='timestamp', header=0, sep='\t'))



# # # --- SEQUENCE COLUMN DATASETS ---

#  # sequence column only interactions with header
# download_example_by_url(output_folder=output_folder, filename=filename, url='https://raw.githubusercontent.com/sisinflab/DataRecDatasets/refs/heads/main/tabular/sequence_columns/interactions/dataset.tsv')
# print(read_sequence_column(os.path.join(output_folder, filename), user_col='user', sequence_col='item', header=0, col_sep='\t', sequence_sep=';'))

#  # sequence column only interactions without header
# download_example_by_url(output_folder=output_folder, filename=filename, url='https://raw.githubusercontent.com/sisinflab/DataRecDatasets/refs/heads/main/tabular/sequence_columns/interactions/dataset_no_header.tsv')
# print(read_sequence_column(os.path.join(output_folder, filename), user_col='user', sequence_col='item', col_sep='\t', sequence_sep=';', cols=['user', 'item']))

#  # sequence column with timestamp and header
# download_example_by_url(output_folder=output_folder, filename=filename, url='https://raw.githubusercontent.com/sisinflab/DataRecDatasets/refs/heads/main/tabular/sequence_columns/timestamp/dataset.tsv')
# print(read_sequence_column(os.path.join(output_folder, filename), user_col='user', sequence_col='item', timestamp_col='timestamp', header=0, col_sep='\t', sequence_sep=';'))

#  # sequence column with timestamp and no header
# download_example_by_url(output_folder=output_folder, filename=filename, url='https://raw.githubusercontent.com/sisinflab/DataRecDatasets/refs/heads/main/tabular/sequence_columns/timestamp/dataset_no_header.tsv')
# print(read_sequence_column(os.path.join(output_folder, filename), user_col='user', sequence_col='item', timestamp_col='timestamp', header=None, col_sep='\t', sequence_sep=';', cols=['user', 'item', 'timestamp']))


# # --- SEQUENCE WIDE DATASETS ---

#  # sequence column only interactions with header
# download_example_by_url(output_folder=output_folder, filename=filename, url='https://raw.githubusercontent.com/sisinflab/DataRecDatasets/refs/heads/main/tabular/sequence_wide/interactions/dataset.tsv')
# print(read_sequence_wide(os.path.join(output_folder, filename), user_col='user', item_col='item', header=0, col_sep='\t'))

#  # sequence column only interactions with header
# download_example_by_url(output_folder=output_folder, filename=filename, url='https://raw.githubusercontent.com/sisinflab/DataRecDatasets/refs/heads/main/tabular/sequence_wide/interactions/dataset_no_header.tsv')
# print(read_sequence_wide(os.path.join(output_folder, filename), header=None, col_sep='\t'))


# # --- JSON DATASETS ---

#  # sequence column only interactions with header
# download_example_by_url(output_folder=output_folder, filename=filename, url='https://raw.githubusercontent.com/sisinflab/DataRecDatasets/refs/heads/main/json/list/interactions/dataset.tsv')
# print(read_sequence_wide(os.path.join(output_folder, filename), user_col='user', item_col='item', header=0, col_sep='\t'))

#  # sequence column only interactions with header
# download_example_by_url(output_folder=output_folder, filename=filename, url='https://raw.githubusercontent.com/sisinflab/DataRecDatasets/refs/heads/main/json/sequence_wide/interactions/dataset_no_header.tsv')
# print(read_sequence_wide(os.path.join(output_folder, filename), header=None, col_sep='\t'))

