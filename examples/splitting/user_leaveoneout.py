from datarec.splitters.user_stratified.leave_out import LeaveOneOut
from datarec.datasets import MovieLens


data = MovieLens(version="1m")

spl = LeaveOneOut()

print(spl.run(data))

