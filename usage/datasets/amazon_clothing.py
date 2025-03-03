from datarec.datasets import AmazonClothing


def test():
    data = AmazonClothing()
    print(print(f'{data.dataset_name} has:\n'
                f'{data.n_users} users\n'
                f'{data.n_items} items\n'
                f'{data.transactions} ratings\n'))


if __name__ == '__main__':
    test()

