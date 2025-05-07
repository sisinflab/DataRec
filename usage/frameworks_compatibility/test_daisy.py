from datarec.datasets import MovieLens1M
from datarec.io import FrameworkExporter

datarec = MovieLens1M()

path = 'daisy.tsv'
exporter = FrameworkExporter(output_path=path)
exporter.to_daisyrec(datarec.to_rawdata())

