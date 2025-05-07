from datarec.datasets import MovieLens1M
from datarec.io import write_tabular, write_json

datarec = MovieLens1M()
print(datarec)

path = 'datalol_,.tsv'
write_tabular(datarec.to_rawdata(), path, sep=",")

path = 'datalol_;.tsv'
write_tabular(datarec.to_rawdata(), path, header=False, sep=";")

path = 'datalol_t.tsv'
write_tabular(datarec.to_rawdata(), path, sep="\t")

path = 'datalol_js.tsv'
write_json(datarec.to_rawdata(), path)

