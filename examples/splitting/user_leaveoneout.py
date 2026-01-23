from datarec.splitters.user_stratified.leave_out import LeaveOneOut
from datarec.datasets import Movielens


data = Movielens(version="1m").prepare_and_load()

spl = LeaveOneOut()

print(spl.run(data))

