import pandas as pd
from datarec import DataRec, RawData


class KCore:

    def __init__(self, column, core, **kwargs):
        self._column = column
        self._core = core

    def run(self, dataset: pd.DataFrame):
        dataset = dataset.copy()
        groups = dataset.groupby([self._column])
        dataset = groups.filter(lambda x: len(x) >= self._core)
        return dataset


class UserKCore:

    def __init__(self, core, **kwargs):
        self.core = core

    def run(self, datarec):
        core_obj = KCore(column=datarec.user_col, core=self.core)
        result = core_obj.run(datarec.data)

        new_datarec = DataRec(RawData(result,
                                      user=datarec.user_col,
                                      item=datarec.item_col,
                                      rating=datarec.rating_col,
                                      timestamp=datarec.timestamp_col),
                              derives_from=datarec)

        return new_datarec


class ItemKCore:

    def __init__(self, core, **kwargs):
        self.core = core

    def run(self, datarec):
        core_obj = KCore(column=datarec.item_col, core=self.core)
        result = core_obj.run(datarec.data)

        new_datarec = DataRec(RawData(result,
                                      user=datarec.user_col,
                                      item=datarec.item_col,
                                      rating=datarec.rating_col,
                                      timestamp=datarec.timestamp_col),
                              derives_from=datarec)

        return new_datarec


class IterativeKCore:

    def __init__(self, columns: list, cores, **kwargs):
        self._columns = columns

        if isinstance(cores, list):
            self._cores = list(zip(columns, cores))
        elif isinstance(cores, int):
            self._cores = [(c, cores) for c in columns]
        else:
            raise ValueError

    def run(self, dataset: pd.DataFrame):
        data = dataset.copy()

        filters = {c: KCore(column=c, core=k) for c, k in self._cores}
        checks = [False for _ in self._columns]
        prev_len = len(data)

        while not all(checks):
            checks = []
            for c, f in filters.items():
                data = f.run(data)
                checks.append((prev_len - len(data)) == 0)
                prev_len = len(data)

        return data


class UserItemIterativeKCore:

    def __init__(self, cores, **kwargs):
        self._cores = cores

    def run(self, datarec):
        core_obj = IterativeKCore(columns=[datarec.user_col, datarec.item_col],
                                  cores=self._cores)
        result = core_obj.run(datarec.data)

        new_datarec = DataRec(RawData(result,
                                      user=datarec.user_col,
                                      item=datarec.item_col,
                                      rating=datarec.rating_col,
                                      timestamp=datarec.timestamp_col),
                              derives_from=datarec)

        return new_datarec


class NRoundsKCore:

    def __init__(self, columns: list, cores, rounds: int, **kwargs):

        self._columns = columns

        if isinstance(cores, list):
            self._cores = list(zip(columns, cores))
        elif isinstance(cores, int):
            self._cores = [(c, cores) for c in columns]
        else:
            raise ValueError

        self._rounds = rounds

    def run(self, dataset: pd.DataFrame):
        data = dataset.copy()

        filters = {c: KCore(column=c, core=k) for c, k in self._cores}
        checks = [False for _ in self._columns]
        prev_len = len(data)

        for _ in range(self._rounds) or all(checks):
            checks = []
            for c, f in filters.items():
                data = f.run(data)
                checks.append((prev_len - len(data)) == 0)
                prev_len = len(data)
        return data


class UserItemNRoundsKCore:

    def __init__(self, cores, rounds: int, **kwargs):
        self._cores = cores
        self._rounds = rounds

    def run(self, datarec):
        core_obj = NRoundsKCore(columns=[datarec.user_col, datarec.item_col],
                                cores=self._cores, rounds=self._rounds)
        result = core_obj.run(datarec.data)

        new_datarec = DataRec(RawData(result,
                                      user=datarec.user_col,
                                      item=datarec.item_col,
                                      rating=datarec.rating_col,
                                      timestamp=datarec.timestamp_col),
                              derives_from=datarec)

        return new_datarec
