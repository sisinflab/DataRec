from datarec.datasets import MovieLens1M
from datarec.io import FrameworkExporter

datarec = MovieLens1M()

path = '../../elliot/dataset.tsv'
exporter = FrameworkExporter(output_path=path)
exporter.to_elliot(datarec.to_rawdata(), datarec.to_rawdata(), datarec.to_rawdata())

