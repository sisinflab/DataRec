from datarec.splitters.uniform import RandomHoldOut
from datarec.datasets import MovieLens1M


data = MovieLens1M()

spl = RandomHoldOut(test_ratio=0.2, val_ratio=0.1)

print(spl.run(data))

