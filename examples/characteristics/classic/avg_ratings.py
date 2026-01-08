from datarec.datasets import Movielens

if __name__ == '__main__':
    
    dataset = Movielens(version='100k')
    dataset.prepare()
    dr = dataset.load()
    print(f'{dr.dataset_name} has:\n'
          f'{dr.n_users} users\n'
          f'{dr.n_items} items\n'
          f'{dr.transactions} ratings\n',
          f'Ratings per User: {dr.characteristic("ratings_per_user")}\n',
          f'Ratings per User: {dr.ratings_per_user()}\n',
          f'Ratings per Item: {dr.characteristic("ratings_per_item")}\n',
          f'Ratings per Item: {dr.ratings_per_item()}\n')
