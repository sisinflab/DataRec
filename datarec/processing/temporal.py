import numpy as np
from datarec import DataRec
from datarec.io import RawData


class FilterByTime:

    def __init__(self, min_time: float = 0, max_time: float = np.inf):

        if max_time < min_time:
            raise ValueError

        self.min_time = min_time
        self.max_time = max_time

    def run(self, datarec: DataRec):

        if datarec.timestamp_col is None:
            raise TypeError('This DataRec does not contain temporal information')

        dataset = datarec.data
        before = dataset[dataset[dataset.timestamp_col] < self.min_time]
        after = dataset[dataset[dataset.timestamp_col] >= self.min_time]

        before_datarec = DataRec(RawData(before,
                                         user=datarec.user_col,
                                         item=datarec.item_col,
                                         rating=datarec.rating_col,
                                         timestamp=datarec.timestamp_col),
                                 derives_from=datarec)

        after_datarec = DataRec(RawData(after,
                                        user=datarec.user_col,
                                        item=datarec.item_col,
                                        rating=datarec.rating_col,
                                        timestamp=datarec.timestamp_col),
                                derives_from=datarec)

        return before_datarec, after_datarec
