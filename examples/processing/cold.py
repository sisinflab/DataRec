from datarec.processing.cold import ColdFilter
from datarec.datasets import Movielens


data = Movielens(version="1m").prepare_and_load()

flt = ColdFilter(interactions=50)

print(flt.run(data))
