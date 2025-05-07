from datarec.pipeline import Pipeline


pipeline = Pipeline()
pipeline.add_step("load", "MovieLens", {"version": "1m"})
pipeline.add_step("process", "Binarize", {"threshold": 4})
pipeline.add_step("process", "UserItemIterativeKCore", {"cores": 2})
pipeline.add_step("split", "RandomHoldOut", {"test_ratio": 0.2, "val_ratio": 0.1})
pipeline.add_step("export", "Elliot", {"output_path": "./elliot/"})
pipeline.to_yaml("./create_pipeline.yml")
pipeline.apply()
