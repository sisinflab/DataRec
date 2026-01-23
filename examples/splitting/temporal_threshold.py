from datarec.splitters.uniform import TemporalThresholdSplit
from datarec.datasets import Movielens


data = Movielens(version="1m").prepare_and_load()

spl = TemporalThresholdSplit(test_threshold=1046454338, val_threshold=975768756)

print(spl.run(data))

