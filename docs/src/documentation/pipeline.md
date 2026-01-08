# Pipeline Module Reference

This section provides the API reference for modules that handle the **creation**, **management**, and **execution** of reproducible data processing workflows.
Pipelines support `load`, `read`, `process`, `split`, `export`, and `write` steps.

## On This Page

- [Minimal usage](#minimal-usage)
- [Pipeline API](#pipeline-api)

## Minimal usage

```python
from datarec.pipeline import Pipeline

pipeline = Pipeline()
pipeline.add_step("load", "registry_dataset", {"dataset_name": "movielens", "version": "1m"})
pipeline.add_step("process", "Binarize", {"threshold": 4})
pipeline.add_step("split", "RandomHoldOut", {"test_ratio": 0.2, "val_ratio": 0.1})
pipeline.add_step("export", "Elliot", {"filename": "elliot/"})
pipeline.apply(output_folder="./out")
```

## Pipeline API

::: datarec.pipeline.pipeline
::: datarec.pipeline.pipeline_step
