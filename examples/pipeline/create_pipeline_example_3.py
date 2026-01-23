from datarec.pipeline import Pipeline

pipeline = Pipeline()
pipeline.add_step("load", "registry_dataset", {"dataset_name": "movielens", "version": "1m"})
pipeline.add_step("process", "Binarize", {"threshold": 4})
pipeline.add_step("process", "UserItemIterativeKCore", {"user_core": 2, "item_core": 2})
pipeline.add_step("split", "RandomHoldOut", {"test_ratio": 0.2, "val_ratio": 0.1})
pipeline.add_step("export", "Elliot", {"filename": "movielens"})
pipeline.to_yaml("./create_pipeline.yml")
pipeline.apply(input_folder="./data", output_folder="./elliot")
