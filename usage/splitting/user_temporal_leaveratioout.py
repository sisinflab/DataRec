from datarec.splitters.user_stratified import LeaveRatioLast
from datarec.datasets import MovieLens


data = MovieLens(version="1m")

spl = LeaveRatioLast(test_ratio=0.2, val_ratio=0.1)

print(spl.run(data))

