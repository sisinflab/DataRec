from datarec.datasets import Epinions


if __name__ == '__main__':

    print('Loading Epinions dataset...')
    dataset = Epinions(version='v1')
    dataset.prepare()
    dr = dataset.load()
    print(dr)
    print(f'{dr.dataset_name} has:\n'
          f'{dr.n_users} users\n'
          f'{dr.n_items} items\n'
          f'{dr.transactions} ratings\n')