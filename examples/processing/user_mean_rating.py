from datarec.processing.rating import FilterByUserMeanRating
from datarec.datasets import Movielens


data = Movielens(version="1m").prepare_and_load()

flt = FilterByUserMeanRating()

print(flt.run(data))
