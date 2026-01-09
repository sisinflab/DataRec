from datarec.processing.kcore import UserKCore
from datarec.datasets import Movielens


data = Movielens(version="1m").prepare_and_load()

flt = UserKCore(core=2)

print(flt.run(data))
