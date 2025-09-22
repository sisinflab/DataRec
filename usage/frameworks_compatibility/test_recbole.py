from datarec.datasets import MovieLens
from datarec.io import FrameworkExporter

datarec = MovieLens(version='1m')

path = 'recbole.tsv'
exporter = FrameworkExporter(output_path=path)
exporter.to_recbole(datarec.to_rawdata())

