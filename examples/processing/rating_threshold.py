from datarec.processing.rating import FilterByRatingThreshold
from datarec.datasets import MovieLens


data = MovieLens(version="1m")

flt = FilterByRatingThreshold(rating_threshold=4)

print(flt.run(data))
