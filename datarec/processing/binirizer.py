from datarec import DataRec
from datarec.io import RawData


class Binarize:
    def __init__(self, threshold, drop=True, replace=True,
                 over_threshold=1, under_threshold=0,):
        super(Binarize, self).__init__()
        self._threshold = threshold
        self._binary_dataset = None
        self._over_threshold = over_threshold
        self._under_threshold = under_threshold
        self._drop = drop
        self._replace = replace

    def run(self, datarec: DataRec,
            *args, **kwargs) -> DataRec:

        dataset = datarec.data.copy()
        column = datarec.rating_col

        positive = dataset[column] >= self._threshold
        negative = ~positive

        new_col = column + '_bin'

        dataset[new_col] = self._over_threshold
        dataset.loc[negative, new_col] = self._under_threshold

        if self._drop:
            dataset.drop(columns=[column], inplace=True)
        if self._replace:
            dataset.rename(columns={new_col: column}, inplace=True)
            new_col = column

        new_datarec = DataRec(RawData(dataset,
                                      user=datarec.user_col,
                                      item=datarec.item_col,
                                      rating=new_col,
                                      timestamp=datarec.timestamp_col),
                              derives_from=datarec)

        return new_datarec

    @property
    def binary_threshold(self):
        return self._threshold

    @property
    def over_threshold(self):
        return self._over_threshold

    @property
    def under_threshold(self):
        return self._under_threshold

    @property
    def drop(self):
        return self._drop

    @property
    def replace(self):
        return self._replace

