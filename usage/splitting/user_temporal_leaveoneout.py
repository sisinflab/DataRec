from datarec.splitters.user_stratified import LeaveOneLastItem
from datarec.datasets import MovieLens


data = MovieLens(version="1m")

spl = LeaveOneLastItem()

print(spl.run(data))

