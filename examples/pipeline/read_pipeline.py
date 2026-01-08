from pathlib import Path

from datarec.pipeline import Pipeline

pipeline_path = Path(__file__).with_name("read_pipeline.yml")
pipeline = Pipeline.from_yaml(str(pipeline_path))
pipeline.apply()
