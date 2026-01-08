from datarec.splitters.user_stratified.leave_out import LeaveNOut
from datarec.datasets import MovieLens


data = MovieLens(version="1m")

spl = LeaveNOut(test_n=2, validation_n=1)

print(spl.run(data))

