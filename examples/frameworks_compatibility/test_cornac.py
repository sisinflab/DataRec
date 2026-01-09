from datarec.datasets import Movielens
from datarec.io import FrameworkExporter

datarec = Movielens(version='1m').prepare_and_load()

path = 'cornac.tsv'
exporter = FrameworkExporter(output_path=path)
exporter.to_cornac(datarec.to_rawdata())

