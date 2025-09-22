from datarec.datasets import MovieLens
from datarec.io import FrameworkExporter

datarec = MovieLens(version='1m')

path = 'rechorus.tsv'
exporter = FrameworkExporter(output_path=path)
exporter.to_rechorus(datarec.to_rawdata(), datarec.to_rawdata(), datarec.to_rawdata())

