import pandas as pd
from sklearn.model_selection import train_test_split as split
from datarec import DataRec
from datarec.splitters.splitter import Splitter


class UserStratifiedHoldOut(Splitter):

    def __init__(self, test_ratio=0, val_ratio=0):

        self.test_ratio = test_ratio
        self.val_ratio = val_ratio

    @property
    def test_ratio(self):
        return self._test_ratio

    @test_ratio.setter
    def test_ratio(self, value):
        if value < 0 or value > 1:
            raise ValueError('ratio must be between 0 and 1')
        self._test_ratio = value

    @property
    def val_ratio(self):
        return self._val_ratio

    @val_ratio.setter
    def val_ratio(self, value):
        if value < 0 or value > 1:
            raise ValueError('ratio must be between 0 and 1')
        self._val_ratio = value

    def run(self, datarec: DataRec):

        train, test, val = pd.DataFrame(), pd.DataFrame(), pd.DataFrame()

        data = datarec.data
        for u in datarec.users:

            u_train, u_val, u_test = data[data.iloc[:, 0] == u], pd.DataFrame(), pd.DataFrame()

            if self.test_ratio:
                u_train, u_test = split(u_train, test_size=self._test_ratio, random_state=42)
            if self.val_ratio:
                u_train, u_val = split(u_train, test_size=self._val_ratio, random_state=42)

            train = pd.concat([train, u_train], axis=0, ignore_index=True)
            test = pd.concat([test, u_test], axis=0, ignore_index=True)
            val = pd.concat([val, u_val], axis=0, ignore_index=True)

        return self.output(datarec=datarec, train=train, test=test, validation=val)
