from datarec.datasets import MovieLens1M
from datarec.io import FrameworkExporter

datarec = MovieLens1M()

path = 'rechorus.tsv'
exporter = FrameworkExporter(output_path=path)
exporter.to_rechorus(datarec.to_rawdata(), datarec.to_rawdata(), datarec.to_rawdata())

