import pandas as pd


class RawData:
    def __init__(self, data=None, header=False, user=None, item=None, rating=None, timestamp=None):
        self.data = data
        self.header = header
        if data is None:
            self.data = pd.DataFrame
            self.header = header
        self.path = None

        self.user = user
        self.item = item
        self.rating = rating
        self.timestamp = timestamp

    def append(self, new_data):
        self.data.append(new_data)

    def copy(self, deep=True):
        self.data.copy(deep=deep)

    def __repr__(self):
        return repr(self.data)

    def __len__(self):
        return len(self.data)

    def __getitem__(self, idx):
        return self.data[idx]

    def __add__(self, other):
        self.__check_rawdata_compatibility__(other)
        new_data = pd.concat([self.data, other.data])
        new_rawdata = RawData(new_data, user=self.user, item=self.item, rating=self.rating,
                              timestamp=self.timestamp, header=self.header)
        return new_rawdata

    def __iter__(self):
        return iter(self.data)

    def __check_rawdata_compatibility__(self, rawdata):
        return __check_rawdata_compatibility__(self, rawdata)


def __check_rawdata_compatibility__(rawdata1: RawData, rawdata2: RawData):
    if rawdata1.user != rawdata2.user:
        raise ValueError('User columns are not compatible')
    if rawdata1.item != rawdata2.item:
        raise ValueError('Item columns are not compatible')
    if rawdata1.rating != rawdata2.rating:
        raise ValueError('Rating columns are not compatible')
    if rawdata1.timestamp != rawdata2.timestamp:
        raise ValueError('Timestamp columns are not compatible')
    if rawdata1.header != rawdata2.header:
        raise ValueError('Header is not compatible')
    return True
