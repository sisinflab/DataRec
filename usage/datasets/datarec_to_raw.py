from datarec.datasets import MovieLens1M
from datarec.splitters.hold_out import HoldOut


def test():
    data = MovieLens1M()
    print('converting dataset in raw format')
    print(data.to_rawdata())
    print(data.copy())



if __name__ == '__main__':
    test()

