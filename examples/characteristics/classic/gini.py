from datarec.datasets import Movielens

if __name__ == '__main__':
    
    dataset = Movielens(version='100k')
    dataset.prepare()
    dr = dataset.load()
    print(f'{dr.dataset_name} has:\n'
          f'{dr.n_users} users\n'
          f'{dr.n_items} items\n'
          f'{dr.transactions} ratings\n',
          f'Gini User: {dr.characteristic("gini_user")}\n',
          f'Gini User: {dr.gini_user()}\n',
          f'Gini Item: {dr.characteristic("gini_item")}\n',
          f'Gini Item: {dr.gini_item()}\n')
