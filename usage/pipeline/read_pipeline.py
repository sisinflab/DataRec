from datarec.pipeline import Pipeline

pipeline = Pipeline.from_yaml('read_pipeline.yml')
pipeline.apply()
