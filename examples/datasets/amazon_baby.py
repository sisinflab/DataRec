from datarec.datasets import AmazonBaby


if __name__ == '__main__':

    dataset = AmazonBaby(version='2023')
    dataset.prepare()
    dr = dataset.load()
    print(dr)
    print(f'{dr.dataset_name} has:\n'
          f'{dr.n_users} users\n'
          f'{dr.n_items} items\n'
          f'{dr.transactions} ratings\n')


