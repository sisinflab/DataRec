from datarec.datasets import MovieLens1M
from datarec.io import FrameworkExporter

datarec = MovieLens1M()

path = 'cornac.tsv'
exporter = FrameworkExporter(output_path=path)
exporter.to_cornac(datarec.to_rawdata())

