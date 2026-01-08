from datarec.datasets import Movielens
from datarec.data.graph import GraphRec

dr = Movielens('100k').prepare_and_load()

gr = dr.to_graphrec()

print(gr)

