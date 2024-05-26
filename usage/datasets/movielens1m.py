from datarec.datasets import MovieLens1M
from datarec.splitters.hold_out import HoldOut

def test():
    data = MovieLens1M()
    print(data)
    print(print(f'{data.dataset_name} has:\n'
                f'{data.n_users} users\n'
                f'{data.n_items} items\n'
                f'{data.transactions} ratings\n'))

    splitter = HoldOut(test_ratio=0.5, val_ratio=0.5)

    data.to_rawdata()

    #r = splitter.run(data)

    #print(r)


if __name__ == '__main__':
    test()

