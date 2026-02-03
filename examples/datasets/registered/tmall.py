from datarec.datasets import Tmall


if __name__ == '__main__':
    dataset = Tmall('v1')
    dataset.prepare_interactions(only_required=False)
    dr = dataset.load(resource_name='train')
    print(dr)
    print(f'{dr.dataset_name} has:\n'
          f'{dr.n_users} users\n'
          f'{dr.n_items} items\n'
          f'{dr.transactions} ratings\n')
    print(dataset.load(resource_name='test'))
