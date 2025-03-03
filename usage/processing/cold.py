from datarec.processing.cold import ColdFilter
from datarec.datasets import MovieLens


data = MovieLens(version="1m")

flt = ColdFilter(interactions=50)

print(flt.run(data))
