from datarec.datasets import MovieLens
#from datarec.splitters.hold_out import HoldOut


def test():
    data = MovieLens('1m')
    print(data)
    print(f'{data.dataset_name} has:\n'
                f'{data.n_users} users\n'
                f'{data.n_items} items\n'
                f'{data.transactions} ratings\n')

    print(data.metrics)
    for metric in data.metrics:
        print(metric, data.__getattribute__(metric))

    # splitter = HoldOut(test_ratio=0.5, val_ratio=0.5)

    # data.to_rawdata()

    #r = splitter.run(data)

    #print(r)


if __name__ == '__main__':
    test()


