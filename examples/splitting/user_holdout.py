from datarec.splitters.user_stratified.hold_out import UserStratifiedHoldOut
from datarec.datasets import Movielens


data = Movielens(version="1m").prepare_and_load()

spl = UserStratifiedHoldOut(test_ratio=0.2, val_ratio=0.1)

print(spl.run(data))

