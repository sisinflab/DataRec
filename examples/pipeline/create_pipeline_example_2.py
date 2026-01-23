from datarec.pipeline import Pipeline

pipeline = Pipeline()
pipeline.add_step("load", "registry_dataset", {"dataset_name":"movielens", "version": "100k"})
pipeline.add_step("process", "Binarize", {"threshold": 4})
pipeline.add_step("process", "UserItemIterativeKCore", {"user_core": 2, "item_core": 2})
pipeline.add_step("split", "RandomHoldOut", {"test_ratio": 0.2, "val_ratio": 0.1})
pipeline.add_step("write", "write_transactions_tabular", {"filename": "transactions_tabular.tsv", "sep": "\t", "user_col": "user_id", "item_col": "item_id", "header": "True"})
res = pipeline.apply(input_folder="./data", output_folder="./output")
