from datarec.datasets import Movielens
from datarec.io import FrameworkExporter

datarec = Movielens(version='1m').prepare_and_load()

path = 'recbole.tsv'
exporter = FrameworkExporter(output_path=path)
exporter.to_recbole(datarec.to_rawdata())

