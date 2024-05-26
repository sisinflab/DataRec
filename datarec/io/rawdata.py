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
        return RawData(self.data + other.data)

    def __iter__(self):
        return iter(self.data)
