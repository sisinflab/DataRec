from datarec.pipeline import Pipeline
from datarec.datasets.examples import download_example_by_url
import os

input_folder = 'data'
ouput_folder = './output'
filename = 'dataset.tsv'

download_example_by_url(output_folder=input_folder, filename=filename, url='https://raw.githubusercontent.com/sisinflab/DataRecDatasets/refs/heads/main/transactions/tabular/interactions/dataset.tsv')

pipeline = Pipeline()
pipeline.add_step("read", "read_transactions_tabular", {"filename": filename, "sep": "\t", "user_col": "user", "item_col": "item", "header": 0})
pipeline.add_step("write", "write_transactions_tabular", {"filename": "transactions_tabular.tsv", "sep": "\t", "user_col": "user_id", "item_col": "item_id", "header": "True"})
res = pipeline.apply(input_folder=input_folder, output_folder=ouput_folder)
