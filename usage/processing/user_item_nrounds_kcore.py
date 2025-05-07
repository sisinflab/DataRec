from datarec.processing.kcore import UserItemNRoundsKCore
from datarec.datasets import MovieLens


data = MovieLens(version="1m")

flt = UserItemNRoundsKCore(cores=2, rounds=2)

print(flt.run(data))
