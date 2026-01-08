from datarec.datasets import Movielens
from datarec.data.graph import GraphRec

dr = Movielens('100k').prepare_and_load()

gr = dr.to_graphrec()

print(gr)
print(f"num_edges: {gr.num_edges}")
print(f"num_nodes: {gr.num_nodes}")
print(f"user_nodes: {gr.user_nodes}")
print(f"item_nodes: {gr.item_nodes}")
print(f"n_user_nodes: {gr.n_user_nodes}")
print(f"n_item_nodes: {gr.n_item_nodes}")
