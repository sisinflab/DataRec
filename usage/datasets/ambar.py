from datarec.datasets import Ambar


def run():
    dataset = Ambar()
    dr=dataset.prepare_and_load()
    print(dr)
    print(f'{dr.dataset_name} has:\n'
                f'{dr.n_users} users\n'
                f'{dr.n_items} items\n'
                f'{dr.transactions} ratings\n')
    dataset.download_content()

if __name__ == '__main__':
    run()

