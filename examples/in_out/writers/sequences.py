import os
from datarec import DataRec
from datarec.io.readers.transactions.tabular import read_transactions_tabular
from datarec.io.writers.sequences.tabular import write_sequence_tabular_inline, write_sequence_tabular_wide, write_sequence_tabular_implicit
from datarec.io.writers.sequences.json import write_sequences_json, write_sequences_json_array
from datarec.datasets.examples import download_example_by_url

output_folder = 'data'
filename = 'dataset.tsv'
filepath = os.path.join(output_folder, filename)
print(filepath)

if not os.path.exists(output_folder):
    os.makedirs(output_folder)
download_example_by_url(output_folder=output_folder, filename=filename, url='https://raw.githubusercontent.com/sisinflab/DataRecDatasets/refs/heads/main/transactions/tabular/timestamp/dataset.tsv')

import os
print(os.path.abspath(filepath))

rawdata = read_transactions_tabular(filepath, user_col='user', item_col='item', rating_col='ratings', timestamp_col='timestamp', header=0, sep='\t')
write_sequence_tabular_inline(rawdata, os.path.join(output_folder, 'sequence_inline.tsv'), include_timestamp=True, user_col='user', sequence_col='sequence', timestamp_col='timestamp', col_sep=',', sequence_sep=' ', verbose=True)
write_sequence_tabular_wide(rawdata, os.path.join(output_folder, 'sequence_wide.tsv'), user_col='user', col_sep=',', header=True, verbose=True)
write_sequence_tabular_implicit(rawdata, os.path.join(output_folder, 'sequence_implicit.tsv'), col_sep=',', verbose=True)
write_sequences_json(rawdata, os.path.join(output_folder, 'sequence.json'), include_rating=True, include_timestamp=True, item_col='item', rating_col='rating', timestamp_col='timestamp', verbose=True)
write_sequences_json_array(rawdata, os.path.join(output_folder, 'sequence_array.json'), include_rating=True, include_timestamp=True, user_col='user', item_col='item', rating_col='rating', timestamp_col='timestamp', verbose=True)

datarec = DataRec(rawdata=rawdata)
write_sequence_tabular_inline(datarec, os.path.join(output_folder, 'sequence_inline.tsv'), include_timestamp=True, user_col='user', sequence_col='sequence', timestamp_col='timestamp', col_sep=',', sequence_sep=' ', verbose=True)
write_sequence_tabular_wide(datarec, os.path.join(output_folder, 'sequence_wide.tsv'), user_col='user', col_sep=',', header=True, verbose=True)
write_sequence_tabular_implicit(datarec, os.path.join(output_folder, 'sequence_implicit.tsv'), col_sep=',', verbose=True)
write_sequences_json(datarec, os.path.join(output_folder, 'sequence.json'), include_rating=True, include_timestamp=True, item_col='item', rating_col='rating', timestamp_col='timestamp', verbose=True)
write_sequences_json_array(datarec, os.path.join(output_folder, 'sequence_array.json'), include_rating=True, include_timestamp=True, user_col='user', item_col='item', rating_col='rating', timestamp_col='timestamp', verbose=True)
