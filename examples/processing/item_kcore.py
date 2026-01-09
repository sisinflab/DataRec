from datarec.processing.kcore import UserItemIterativeKCore
from datarec.datasets import Movielens


data = Movielens(version="1m").prepare_and_load()

flt = UserItemIterativeKCore(cores=2)

print(flt.run(data))
