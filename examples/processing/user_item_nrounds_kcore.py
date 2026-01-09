from datarec.processing.kcore import UserItemNRoundsKCore
from datarec.datasets import Movielens


data = Movielens(version="1m").prepare_and_load()

flt = UserItemNRoundsKCore(cores=2, rounds=2)

print(flt.run(data))
