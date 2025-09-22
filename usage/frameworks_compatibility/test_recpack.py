from datarec.datasets import MovieLens
from datarec.io import FrameworkExporter

datarec = MovieLens(version='1m')

path = '../../recpack/dataset.tsv'
exporter = FrameworkExporter(output_path=path)
exporter.to_recpack(datarec.to_rawdata())

