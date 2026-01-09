from datarec.processing.binarizer import Binarize
from datarec.datasets import Movielens


data = Movielens(version="1m").prepare_and_load()

flt = Binarize(threshold=4)

print(flt.run(data))

