from datarec.datasets import MovieLens1M
from datarec.io import FrameworkExporter

datarec = MovieLens1M()

path = 'lenskit.tsv'
exporter = FrameworkExporter(output_path=path)
exporter.to_lenskit(datarec.to_rawdata())

