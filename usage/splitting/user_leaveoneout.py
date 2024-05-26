from datarec.splitters.user_stratified.leave_out import LeaveOneOut
from datarec.datasets import MovieLens1M


data = MovieLens1M()

spl = LeaveOneOut()

print(spl.run(data))

