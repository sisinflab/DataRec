from datarec.processing.rating import FilterByUserMeanRating
from datarec.datasets import MovieLens


data = MovieLens(version="1m")

flt = FilterByUserMeanRating()

print(flt.run(data))
