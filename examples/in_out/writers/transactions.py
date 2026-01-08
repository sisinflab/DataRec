import os
from datarec import DataRec
from datarec.io.readers.transactions.tabular import read_transactions_tabular
from datarec.io.writers.transactions.tabular import write_transactions_tabular
from datarec.io.writers.transactions.json import write_transactions_json
from datarec.io.writers.transactions.jsonl import write_transactions_jsonl
from datarec.io.writers.sequences.tabular import write_sequence_tabular_inline, write_sequence_tabular_wide, write_sequence_tabular_implicit
from datarec.io.writers.sequences.json import write_sequences_json, write_sequences_json_array
from datarec.datasets.examples import download_example_by_url

output_folder = 'data'
filename = 'dataset.tsv'
filepath = os.path.join(output_folder, filename)
print(filepath)

if not os.path.exists(output_folder):
    os.makedirs(output_folder)
if not os.path.exists(filepath):
    download_example_by_url(output_folder=output_folder, filename=filename, url='https://raw.githubusercontent.com/sisinflab/DataRecDatasets/refs/heads/main/transactions/tabular/timestamp/dataset.tsv')

rawdata = read_transactions_tabular(filepath, user_col='user', item_col='item', rating_col='ratings', timestamp_col='timestamp', header=0, sep='\t')

write_transactions_tabular(rawdata, os.path.join(output_folder, 'transactions.tsv'), include_rating=True, include_timestamp=True, user_col='user', item_col='item', rating_col='rating', timestamp_col='timestamp', sep='\t', header=True, verbose=True)
write_transactions_json(rawdata, os.path.join(output_folder, 'transactions.json'), include_rating=True, include_timestamp=True, user_col='user', item_col='item', rating_col='rating', timestamp_col='timestamp', verbose=True)
write_transactions_jsonl(rawdata, os.path.join(output_folder, 'transactions.jsonl'), include_rating=True, include_timestamp=True, user_col='user', item_col='item', rating_col='rating', timestamp_col='timestamp', verbose=True)

datarec = DataRec(rawdata=rawdata)
write_transactions_tabular(datarec, os.path.join(output_folder, 'transactions.tsv'), include_rating=True, include_timestamp=True, user_col='user', item_col='item', rating_col='rating', timestamp_col='timestamp', sep='\t', header=True, verbose=True)
write_transactions_json(datarec, os.path.join(output_folder, 'transactions.json'), include_rating=True, include_timestamp=True, user_col='user', item_col='item', rating_col='rating', timestamp_col='timestamp', verbose=True)
write_transactions_jsonl(datarec, os.path.join(output_folder, 'transactions.jsonl'), include_rating=True, include_timestamp=True, user_col='user', item_col='item', rating_col='rating', timestamp_col='timestamp', verbose=True)
