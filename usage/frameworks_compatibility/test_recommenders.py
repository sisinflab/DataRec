from datarec.datasets import MovieLens1M
from datarec.io import FrameworkExporter

datarec = MovieLens1M()

path = '../../recommenders/dataset.tsv'
exporter = FrameworkExporter(output_path=path)
exporter.to_recommenders(datarec.to_rawdata())

