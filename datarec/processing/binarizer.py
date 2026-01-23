from typing import Optional

from datarec import DataRec
from datarec.processing.processor import Processor


class Binarize(Processor):
    
    """
    A class for binarizing rating values in a dataset based on a given threshold.

    This class processes a dataset wrapped in a DataRec object and modifies the rating column
    based on the specified threshold. Filtering and rating-column dropping are controlled via
    `keep` and `drop_rating_col`. The legacy `implicit` flag is still supported: if True and
    `keep`/`drop_rating_col` are not provided, it behaves as keep='positive' and drop_rating_col=True.
    If `keep` or `drop_rating_col` are provided, they take precedence over `implicit`.
    """
    
    def __init__(self, threshold: float, implicit: bool = False,
                 over_threshold: float = 1, under_threshold: float = 0,
                 keep: Optional[str] = None, drop_rating_col: Optional[bool] = None):
        """
        Initializes the Binarize object.
        
        Args:
            threshold (float): The threshold for binarization.
            implicit (bool): Legacy flag. If True and `keep`/`drop_rating_col` are not provided,
                keeps only positive interactions and drops the rating column.
            over_threshold (int, float): The value assigned to ratings equal to or above the threshold.
            under_threshold (int, float): The value assigned to ratings below the threshold.
            keep (str, optional): Which interactions to keep: 'all', 'positive', or 'negative'.
            drop_rating_col (bool, optional): Whether to drop the rating column after filtering.
        """
        self.params = {k: v for k, v in locals().items() if k != 'self'}
        if keep is not None or drop_rating_col is not None:
            self.params.pop('implicit', None)

        self._threshold = threshold
        self._over_threshold = over_threshold
        self._under_threshold = under_threshold
        self._implicit = implicit

        if keep is None and drop_rating_col is None and implicit:
            keep = 'positive'
            drop_rating_col = True

        if keep is None:
            keep = 'all'
        if drop_rating_col is None:
            drop_rating_col = False

        if keep not in {'all', 'positive', 'negative'}:
            raise ValueError("keep must be one of: 'all', 'positive', 'negative'")

        self._keep = keep
        self._drop_rating_col = drop_rating_col

    def run(self, datarec: DataRec) -> DataRec:

        """
        Binarizes the rating values in the given dataset based on a threshold.

        If `keep` is 'positive' or 'negative', rows are filtered accordingly. If `drop_rating_col`
        is True, the rating column is removed; otherwise, ratings are binarized to
        `over_threshold` or `under_threshold`.

        Args:
            datarec (DataRec): The input dataset wrapped in a DataRec object.

        Returns:
            (DataRec): A new DataRec object with the processed dataset.
        """

        dataset = datarec.data.copy()
        column = datarec.rating_col

        positive = dataset[column] >= self._threshold

        if self._keep == 'positive':
            dataset = dataset[positive].copy()
        elif self._keep == 'negative':
            dataset = dataset[~positive].copy()

        if self._drop_rating_col:
            dataset.drop(columns=[column], inplace=True)
        else:
            positive = dataset[column] >= self._threshold
            dataset[column] = self._over_threshold
            dataset.loc[~positive, column] = self._under_threshold

        result = self.output(datarec, dataset,
                             step_info={'operation': self.__class__.__name__, 'params': self.params})

        return result

    @property
    def binary_threshold(self) -> float:
        """
        Returns the rating threshold used to distinguish positive interactions.
        """
        return self._threshold

    @property
    def over_threshold(self) -> float:
        """
        Returns the value assigned to ratings at or above the threshold.
        """
        return self._over_threshold

    @property
    def under_threshold(self) -> float:
        """
        Returns the value assigned to ratings below the threshold.
        """
        return self._under_threshold
