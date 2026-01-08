from datarec.splitters.user_stratified import LeaveOneLast
from datarec.datasets import MovieLens


data = MovieLens(version="1m")

spl = LeaveOneLast()

print(spl.run(data))

