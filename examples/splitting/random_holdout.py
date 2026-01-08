from datarec.splitters.uniform import RandomHoldOut
from datarec.datasets import MovieLens


data = MovieLens(version="1m")

spl = RandomHoldOut(test_ratio=0.2, val_ratio=0.1)

print(spl.run(data))

