from datarec.splitters.uniform import TemporalThresholdSplit
from datarec.datasets import MovieLens


data = MovieLens(version="1m")

spl = TemporalThresholdSplit(test_threshold=1046454338, val_threshold=975768756)

print(spl.run(data))

