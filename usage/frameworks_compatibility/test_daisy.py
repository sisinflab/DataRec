from datarec.datasets import MovieLens
from datarec.io import FrameworkExporter

datarec = MovieLens(version='1m')

path = 'daisy.tsv'
exporter = FrameworkExporter(output_path=path)
exporter.to_daisyrec(datarec.to_rawdata())

