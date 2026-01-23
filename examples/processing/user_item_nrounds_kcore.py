from datarec.processing.kcore import UserItemNRoundsKCore
from datarec.datasets import Movielens


data = Movielens(version="1m").prepare_and_load()

flt = UserItemNRoundsKCore(rounds=2, user_core=2, item_core=2)

print(flt.run(data))
