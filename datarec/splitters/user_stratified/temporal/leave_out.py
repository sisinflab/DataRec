from datarec import DataRec
import pandas as pd
from datarec.splitters.utils import min_by_col
from datarec.splitters.splitter import Splitter


class LeaveNLast(Splitter):

    def __init__(self, test_n=0, validation_n=0):

        self.test_n = test_n
        self.validation_n = validation_n

    @property
    def test_n(self):
        return self._test_n

    @test_n.setter
    def test_n(self, value: int):
        if value < 0:
            raise ValueError
        self._test_n = value

    @property
    def validation_n(self):
        return self._validation_n

    @validation_n.setter
    def validation_n(self, value: int):
        if value < 0:
            raise ValueError
        self._validation_n = value

    def run(self, datarec: DataRec):

        if datarec.timestamp_col is None:
            raise TypeError('This DataRec does not contain temporal information')

        train, test, val = pd.DataFrame(), pd.DataFrame(), pd.DataFrame()

        data = datarec.data
        for u in datarec.users:

            u_train, u_val, u_test = data[data.iloc[:, 0] == u], pd.DataFrame(), pd.DataFrame()

            if self.test_n:
                for _ in range(self.test_n):
                    u_train, sample = min_by_col(u_train, datarec.timestamp_col)
                    u_test = pd.concat([u_test, sample], axis=0, ignore_index=True)

            if self.validation_n:
                for _ in range(self.validation_n):
                    u_train, sample = min_by_col(u_train, datarec.timestamp_col)
                    u_val = pd.concat([u_val, sample], axis=0, ignore_index=True)

            train = pd.concat([train, u_train], axis=0, ignore_index=True)
            test = pd.concat([test, u_test], axis=0, ignore_index=True)
            val = pd.concat([val, u_val], axis=0, ignore_index=True)

        return self.output(datarec, train, test, val)


class LeaveOneLastItem(LeaveNLast):

    def __init__(self, test: bool = True, validation: bool = True):

        test = 1 if test else 0
        validation = 1 if validation else 0

        super().__init__(test_n=test, validation_n=validation)
