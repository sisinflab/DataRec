from datarec.datasets import MovieLens
from datarec.io import FrameworkExporter

datarec = MovieLens(version='1m')

path = 'cornac.tsv'
exporter = FrameworkExporter(output_path=path)
exporter.to_cornac(datarec.to_rawdata())

