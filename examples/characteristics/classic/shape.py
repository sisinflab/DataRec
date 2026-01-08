from datarec.datasets import Movielens

if __name__ == '__main__':
    
    dataset = Movielens(version='100k')
    dataset.prepare()
    dr = dataset.load()
    print(f'{dr.dataset_name} has:\n'
          f'{dr.n_users} users\n'
          f'{dr.n_items} items\n'
          f'{dr.transactions} ratings\n',
          f'Shape: {dr.characteristic("shape")}\n',
          f'Shape: {dr.shape()}\n',
          f'Shape Log: {dr.characteristic("shape_log")}\n',
          f'Shape Log: {dr.shape_log()}\n')
