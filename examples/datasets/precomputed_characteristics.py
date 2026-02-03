from datarec.datasets import *
from datarec import available_datasets


dr = Movielens('100k')
print(dr.n_users)

for char in dr.characteristics:
    print(f"{char}: {dr.characteristics[char]}")