from datarec.datasets import MovieLens


if __name__ == '__main__':

    data = MovieLens('1m').prepare_and_load()
    print(data)
    print(f'{data.dataset_name} has:\n'
                f'{data.n_users} users\n'
                f'{data.n_items} items\n'
                f'{data.transactions} ratings\n')

    print(data.metrics)
    for metric in data.metrics:
        print(metric, data.__getattribute__(metric))



