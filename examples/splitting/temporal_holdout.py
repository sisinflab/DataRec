from datarec.splitters.uniform import TemporalHoldOut
from datarec.datasets import MovieLens


data = MovieLens(version="1m")

spl = TemporalHoldOut(test_ratio=0.2, val_ratio=0.1)

print(spl.run(data))

