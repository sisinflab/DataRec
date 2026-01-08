from datarec.datasets import AlibabaiFashion


if __name__ == '__main__':

    dataset = AlibabaiFashion(version='v1')
    dataset.prepare()
    dr = dataset.load()
    print(dr)
    print(f'{dr.dataset_name} has:\n'
          f'{dr.n_users} users\n'
          f'{dr.n_items} items\n'
          f'{dr.transactions} ratings\n')
