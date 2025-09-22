from datarec.datasets import MovieLens
from datarec.io import FrameworkExporter

datarec = MovieLens(version='1m')

path = '../../recommenders/dataset.tsv'
exporter = FrameworkExporter(output_path=path)
exporter.to_recommenders(datarec.to_rawdata())

