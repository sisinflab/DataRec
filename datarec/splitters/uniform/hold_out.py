import pandas as pd
from sklearn.model_selection import train_test_split as split
from datarec import DataRec
from datarec.splitters.splitter import Splitter


class RandomHoldOut(Splitter):

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

        train, val, test = datarec.data, None, None

        if self.test_ratio:
            train, test = split(train, test_size=self._test_ratio, random_state=42)

        if self.val_ratio:
            test, val = split(train, test_size=self._val_ratio, random_state=42)

        return self.output(datarec=datarec, train=train, test=test, validation=val)

