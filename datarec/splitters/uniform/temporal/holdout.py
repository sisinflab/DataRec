from datarec import DataRec
from datarec.splitters.splitter import Splitter
from datarec.splitters.utils import temporal_holdout


class TemporaHoldOut(Splitter):

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

        if datarec.timestamp_col is None:
            raise TypeError('This DataRec does not contain temporal information')

        train, test, val = temporal_holdout(dataframe=datarec.data,
                                            test_ratio=self.test_ratio, val_ratio=self.val_ratio,
                                            temporal_col=datarec.timestamp_col)

        return self.output(datarec, train, test, val)

