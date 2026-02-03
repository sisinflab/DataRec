from datarec.datasets import Movielens
import random

dr = Movielens('100k').prepare_and_load()
items = dr.items
picked_items = random.choices(items, k=10)
for item in picked_items:
    item_interactions = dr.get_item_interactions(item)
    print(f'Item {item} interactions:\n {item_interactions}')


