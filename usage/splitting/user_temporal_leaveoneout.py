from datarec.splitters.user_stratified import LeaveOneLastItem
from datarec.datasets import MovieLens1M


data = MovieLens1M()

spl = LeaveOneLastItem()

print(spl.run(data))

