from datarec.processing.temporal import FilterByTime
from datarec.datasets import Movielens


data = Movielens(version="1m").prepare_and_load()

flt = FilterByTime(time_threshold=956704887, drop='before')

print(flt.run(data))
