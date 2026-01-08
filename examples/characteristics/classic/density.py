from datarec.datasets import Movielens

if __name__ == '__main__':
    
    dataset = Movielens(version='100k')
    dataset.prepare()
    dr = dataset.load()
    print(f'{dr.dataset_name} has:\n'
          f'{dr.n_users} users\n'
          f'{dr.n_items} items\n'
          f'{dr.transactions} ratings\n',
          f'Density: {dr.characteristic("density")}\n',
          f'Density: {dr.density()}\n',
          f'Density Log: {dr.characteristic("density_log")}\n',
          f'Density Log: {dr.density_log()}\n')