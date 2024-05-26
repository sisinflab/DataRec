from datarec.splitters.uniform import TemporaHoldOut
from datarec.datasets import MovieLens1M


data = MovieLens1M()

spl = TemporaHoldOut(test_ratio=0.2, val_ratio=0.1)

print(spl.run(data))

