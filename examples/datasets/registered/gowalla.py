from datarec.datasets import Gowalla


if __name__ == '__main__':
    dataset = Gowalla('checkins')
    dataset.prepare()
    dr = dataset.load()
    print(dr)
    print(f'{dr.dataset_name} has:\n'
                f'{dr.n_users} users\n'
                f'{dr.n_items} items\n'
                f'{dr.transactions} ratings\n')

    dataset = Gowalla('friendships')
    dataset.prepare()
    dr = dataset.load()
    print(dr)
    print(f'{dr.dataset_name} has:\n'
                f'{dr.n_users} users\n'
                f'{dr.n_items} items\n'
                f'{dr.transactions} ratings\n')
