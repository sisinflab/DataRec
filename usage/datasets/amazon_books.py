from datarec.datasets import AmazonBooks


def test():
    data = AmazonBooks()
    print(data)
    print(print(f'{data.dataset_name} has:\n'
                f'{data.n_users} users\n'
                f'{data.n_items} items\n'
                f'{data.transactions} ratings\n'))


if __name__ == '__main__':
    test()

