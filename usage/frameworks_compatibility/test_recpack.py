from datarec.datasets import MovieLens1M
from datarec.io import FrameworkExporter

datarec = MovieLens1M()

path = '../../recpack/dataset.tsv'
exporter = FrameworkExporter(output_path=path)
exporter.to_recpack(datarec.to_rawdata())

