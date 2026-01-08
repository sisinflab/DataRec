from datarec.processing.kcore import UserItemIterativeKCore
from datarec.datasets import MovieLens


data = MovieLens(version="1m")

flt = UserItemIterativeKCore(cores=2)

print(flt.run(data))
