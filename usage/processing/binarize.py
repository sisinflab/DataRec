from datarec.processing.binarizer import Binarize
from datarec.datasets import MovieLens


data = MovieLens(version="1m")

flt = Binarize(threshold=4)

print(flt.run(data))

