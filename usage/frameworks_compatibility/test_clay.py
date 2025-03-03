from datarec.datasets import MovieLens1M
from datarec.io import FrameworkExporter

datarec = MovieLens1M()

path = 'clayrs.csv'
exporter = FrameworkExporter(output_path=path)
exporter.to_clayrs(datarec.to_rawdata())

