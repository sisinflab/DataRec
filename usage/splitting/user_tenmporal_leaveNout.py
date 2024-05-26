from datarec.splitters.user_stratified import LeaveNLast
from datarec.datasets import MovieLens1M


data = MovieLens1M()

spl = LeaveNLast(test_n=2, validation_n=1)

print(spl.run(data))

