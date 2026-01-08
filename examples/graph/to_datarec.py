from datarec.datasets import Movielens
from datarec.data.graph import GraphRec

dr = Movielens('100k').prepare_and_load()
print(dr)

gr = dr.to_graphrec()

dr = gr.to_datarec()
print(dr)

