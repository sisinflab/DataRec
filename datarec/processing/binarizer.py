from datarec import DataRec
from datarec.io import RawData


class Binarize:
    def __init__(self, threshold: float, implicit=False,
                 over_threshold: float = 1, under_threshold: float = 0):
        """
        A class for binarizing rating values in a dataset based on a given threshold.

        This class processes a dataset wrapped in a DataRec object and modifies the rating column
        based on the specified threshold. If `implicit` is set to True, rows with ratings below
        the threshold are removed, and the rating column is dropped. Otherwise, ratings are binarized
        to either `over_threshold` or `under_threshold` values.

        Args:
            threshold (float): The threshold for binarization.
            implicit (bool): If True, removes rows below the threshold and drops the rating column.
            over_threshold (int, float): The value assigned to ratings equal to or above the threshold.
            under_threshold (int, float): The value assigned to ratings below the threshold.
        """

        self._threshold = threshold
        self._over_threshold = over_threshold
        self._under_threshold = under_threshold
        self._implicit = implicit

    def run(self, datarec: DataRec) -> DataRec:

        """
        Binarizes the rating values in the given dataset based on a threshold.

        If `implicit` is True, removes rows where the rating is below the threshold
        and drops the rating column. If `implicit` is False, replaces the rating
        values with binary values (over_threshold if >= threshold, under_threshold otherwise).

        Args:
            datarec (DataRec): The input dataset wrapped in a DataRec object.

        Returns:
            DataRec: A new DataRec object with the processed dataset.
        """

        dataset = datarec.data.copy()
        column = datarec.rating_col

        positive = dataset[column] >= self._threshold

        if self._implicit:
            dataset = dataset[positive].copy()
            dataset.drop(columns=[column], inplace=True)
            new_datarec = DataRec(RawData(dataset,
                                          user=datarec.user_col,
                                          item=datarec.item_col,
                                          timestamp=datarec.timestamp_col),
                                  derives_from=datarec)
        else:
            dataset[column] = self._over_threshold
            dataset.loc[~positive, column] = self._under_threshold
            new_datarec = DataRec(RawData(dataset,
                                          user=datarec.user_col,
                                          item=datarec.item_col,
                                          rating=column,
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
