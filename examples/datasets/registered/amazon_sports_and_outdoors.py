from datarec.datasets import AmazonSportsOutdoors

if __name__ == '__main__':

    dataset = AmazonSportsOutdoors(version='2023')
    dataset.prepare()
    dr = dataset.load()
    print(dr)
    print(f'{dr.dataset_name} has:\n'
          f'{dr.n_users} users\n'
          f'{dr.n_items} items\n'
          f'{dr.transactions} ratings\n')


