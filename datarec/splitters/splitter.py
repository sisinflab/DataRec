import pandas as pd
from datarec import DataRec
from datarec.io import RawData


class Splitter:
    @staticmethod
    def output(datarec: DataRec, train: pd.DataFrame, test: pd.DataFrame, validation: pd.DataFrame):

        result = dict()
        for k, d in zip(['train', 'test', 'val'], [train, test, validation]):
            if len(d) > 0:
                new_datarec = DataRec(RawData(d,
                                              user=datarec.user_col,
                                              item=datarec.item_col,
                                              rating=datarec.rating_col,
                                              timestamp=datarec.timestamp_col),
                                      derives_from=datarec)
                result[k] = new_datarec
        return result
