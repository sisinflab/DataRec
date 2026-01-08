from datarec.datasets import Movielens
from datarec import from_pickle


if __name__ == '__main__':
    dataset = Movielens('100k')
    dataset.prepare()
    dr = dataset.load()
    print(dr)
    print(f'{dr.dataset_name} has:\n'
          f'{dr.n_users} users\n'
          f'{dr.n_items} items\n'
          f'{dr.transactions} ratings\n')
    
    dr.to_pickle()
    dr2 = from_pickle('movielens', '100k')

    print(dr2)
    print(f'{dr2.dataset_name} has:\n'
          f'{dr2.n_users} users\n'
          f'{dr2.n_items} items\n'
          f'{dr2.transactions} ratings\n')
    
