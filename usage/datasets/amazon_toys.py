from datarec.datasets import AmazonToysGames


def test():
    data = AmazonToysGames()
    print(data)
    print(print(f'{data.dataset_name} has:\n'
                f'{data.n_users} users\n'
                f'{data.n_items} items\n'
                f'{data.transactions} ratings\n'))


if __name__ == '__main__':
    test()

