from datarec.processing.temporal import FilterByTime
from datarec.datasets import MovieLens


data = MovieLens(version="1m")

flt = FilterByTime(time_threshold=956704887, drop='before')

print(flt.run(data))
