from datarec.pipeline import Pipeline
from datarec.datasets.examples import download_example_by_url

output_folder = 'data'
filename = 'dataset.tsv'

download_example_by_url(output_folder=output_folder, filename=filename, url='https://raw.githubusercontent.com/sisinflab/DataRecDatasets/refs/heads/main/transactions/tabular/interactions/dataset.tsv')

pipeline = Pipeline()
pipeline.add_step("read", "read_transactions_tabular", {"filename": "transactions_tabular.tsv", "sep": "\t", "user_col": "user_id", "item_col": "item_id", "header": 0})
pipeline.add_step("write", "write_transactions_tabular", {"filename": "transactions_tabular.tsv", "sep": "\t", "user_col": "user_id", "item_col": "item_id", "header": "True"})
res = pipeline.apply(input_folder=output_folder, output_folder="./output")
