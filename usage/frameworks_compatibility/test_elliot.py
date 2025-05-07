from datarec.datasets import MovieLens
from datarec.io import FrameworkExporter

datarec = MovieLens()

path = '../../elliot/dataset.tsv'
exporter = FrameworkExporter(output_path=path)
exporter.to_elliot(datarec.to_rawdata(), datarec.to_rawdata(), datarec.to_rawdata())

