from datarec.splitters.user_stratified import LeaveNLast
from datarec.datasets import Movielens


data = Movielens(version="1m").prepare_and_load()

spl = LeaveNLast(test_n=2, validation_n=1)

print(spl.run(data))

