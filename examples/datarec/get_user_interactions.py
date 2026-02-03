from datarec.datasets import Movielens
import random

dr = Movielens('100k').prepare_and_load()
users = dr.users
picked_users = random.choices(users, k=10)
for user in picked_users:
    user_interactions = dr.get_user_interactions(user)
    print(f'User {user} interactions:\n {user_interactions}')


