from datarec.splitters.user_stratified import LeaveNLast
from datarec.datasets import MovieLens


data = MovieLens(version="1m")

spl = LeaveNLast(test_n=2, validation_n=1)

print(spl.run(data))

