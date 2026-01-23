from datarec.splitters.user_stratified import LeaveOneLast
from datarec.datasets import Movielens


data = Movielens(version="1m").prepare_and_load()

spl = LeaveOneLast()

print(spl.run(data))

