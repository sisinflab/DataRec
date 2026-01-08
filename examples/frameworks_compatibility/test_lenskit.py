from datarec.datasets import MovieLens
from datarec.io import FrameworkExporter

datarec = MovieLens(version='1m')

path = 'lenskit.tsv'
exporter = FrameworkExporter(output_path=path)
exporter.to_lenskit(datarec.to_rawdata())

