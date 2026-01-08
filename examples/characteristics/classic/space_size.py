from datarec.datasets import Movielens

if __name__ == '__main__':
    
    dataset = Movielens(version='100k')
    dataset.prepare()
    dr = dataset.load()
    print(f'{dr.dataset_name} has:\n'
          f'{dr.n_users} users\n'
          f'{dr.n_items} items\n'
          f'{dr.transactions} ratings\n',
          f'Space Size: {dr.characteristic("space_size")}\n',
          f'Space Size: {dr.space_size()}\n',
          f'Space Size Log: {dr.characteristic("space_size_log")}\n',
          f'Space Size Log: {dr.space_size_log()}\n')
