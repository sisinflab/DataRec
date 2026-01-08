from datarec.datasets import Movielens

if __name__ == '__main__':
    
    dataset = Movielens(version='100k')
    dataset.prepare()
    dr = dataset.load()
    print('\n',
          f'N. users: {dr.characteristic("n_users")}\n',
          f'N. items: {dr.characteristic("n_items")}\n',
          f'N. interactions: {dr.characteristic("n_interactions")}\n')
