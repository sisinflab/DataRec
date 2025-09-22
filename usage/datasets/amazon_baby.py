from datarec.datasets import AmazonBaby


if __name__ == '__main__':

    data = AmazonBaby(version='2023').prepare_and_load()
    print(data)

    print(data)
    print(f'{data.dataset_name} has:\n'
          f'{data.n_users} users\n'
          f'{data.n_items} items\n'
          f'{data.transactions} ratings\n')

    print(f'Metrics:')
    for metric in data.metrics:
        print(metric, data.__getattribute__(metric))

