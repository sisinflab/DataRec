from datarec.processing.rating import FilterByRatingThreshold
from datarec.datasets import Movielens


data = Movielens(version="1m").prepare_and_load()

flt = FilterByRatingThreshold(rating_threshold=4)

print(flt.run(data))
