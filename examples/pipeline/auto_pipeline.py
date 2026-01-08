from datarec.datasets import Movielens
from datarec.pipeline.pipeline import Pipeline
from datarec.processing import Binarize, UserItemIterativeKCore
from datarec.splitters import UserStratifiedHoldOut
from datarec.io import FrameworkExporter
import os


if __name__ == '__main__':

    datarec = Movielens(version='1m').prepare_and_load()

    print(f"Original dataset: {datarec.n_users} users, {datarec.n_items} items, {len(datarec)} interactions.")
    print(f"Original pipeline length: {len(datarec.pipeline.steps)}\n")

    binarizer = Binarize(threshold=4, implicit=False)
    datarec_binarized = binarizer.run(datarec)
    print(f"Binarized dataset: {len(datarec_binarized)} interactions.")
    print(f"Pipeline length: {len(datarec_binarized.pipeline.steps)}")

    k_core_filter = UserItemIterativeKCore(cores=5)
    datarec_filtered = k_core_filter.run(datarec_binarized)
    print(f"Dataset after iterative k-Core: {datarec_filtered.n_users} users, {datarec_filtered.n_items} items, {len(datarec_filtered)} interactions.")
    print(f"Pipeline length: {len(datarec_filtered.pipeline.steps)}")

    splitter = UserStratifiedHoldOut(test_ratio=0.25, val_ratio=0.25, seed=42)
    split_result = splitter.run(datarec_filtered)

    train_data = split_result['train']
    test_data = split_result['test']
    val_data = split_result['val']

    print(f"Train set: {len(train_data)} interactions.")
    print(f"Test set: {len(test_data)} interactions.")
    print(f"Validation set: {len(val_data)} interactions.")
    print(f"Pipeline length: {len(train_data.pipeline.steps)}\n")

    exporter = FrameworkExporter(output_path='./elliot')
    exporter.to_elliot(train_data=train_data, test_data=test_data, val_data=val_data)

    print(f"Pipeline length: {len(train_data.pipeline.steps)}\n")

    config_filepath = "experiment_config.yaml"
    print(f"Saving pipeline configuration in '{config_filepath}'...")
    train_data.save_pipeline(config_filepath)
    print(f"Pipeline saved in '{config_filepath}'")

    print(f"Loading pipeline from '{config_filepath}'...")
    repro_pipeline = Pipeline.from_yaml(config_filepath)
    print("Loading completed.")
    print(f"Number of pipeline steps to reproduce: {len(repro_pipeline.steps)}")

    print(repro_pipeline)    
    res = repro_pipeline.apply()
