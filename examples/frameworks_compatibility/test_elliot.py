from datarec.datasets import Movielens
from datarec.io import FrameworkExporter

datarec = Movielens(version='1m').prepare_and_load()

path = '../../elliot'
exporter = FrameworkExporter(output_path=path)
exporter.to_elliot(datarec, datarec, datarec)

