from datarec.datasets import Movielens
from datarec import from_pickle


if __name__ == '__main__':
    dataset = Movielens('100k')

    dataset.free_cache()

    # saving to cache
    dataset.prepare()
    dr = dataset.load(to_cache=True)
    print(dr)
    print(f'{dr.dataset_name} has:\n'
          f'{dr.n_users} users\n'
          f'{dr.n_items} items\n'
          f'{dr.transactions} ratings\n')
    
    # loading from cache
    dr2 = dataset.prepare_and_load()
    print(dr2)
    print(f'{dr2.dataset_name} has:\n'
            f'{dr2.n_users} users\n'
            f'{dr2.n_items} items\n'
            f'{dr2.transactions} ratings\n')
    
    # free cache
    dataset.free_cache()

    # load without cache
    dr3 = dataset.load(use_cache=False, to_cache=False)
    print(dr3)
    print(f'{dr3.dataset_name} has:\n'
            f'{dr3.n_users} users\n'
            f'{dr3.n_items} items\n'
            f'{dr3.transactions} ratings\n')

    