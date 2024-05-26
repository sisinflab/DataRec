from datarec.splitters.user_stratified.leave_out import LeaveNOut
from datarec.datasets import MovieLens1M


data = MovieLens1M()

spl = LeaveNOut(test_n=2, validation_n=1)

print(spl.run(data))

