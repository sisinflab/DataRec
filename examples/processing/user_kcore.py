from datarec.processing.kcore import UserKCore
from datarec.datasets import MovieLens


data = MovieLens(version="1m")

flt = UserKCore(core=2)

print(flt.run(data))
