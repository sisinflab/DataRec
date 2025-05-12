from datarec.datasets import MovieLens1M
from datarec.io import FrameworkExporter

datarec = MovieLens1M()

path = 'recbole.tsv'
exporter = FrameworkExporter(output_path=path)
exporter.to_recbole(datarec.to_rawdata())

