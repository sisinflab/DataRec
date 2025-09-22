from typing import Dict
from datarec import DataRec
from datarec.splitters.splitter import Splitter
from datarec.splitters.utils import temporal_holdout


class TemporalHoldOut(Splitter):
    """
    Implements a temporal hold-out splitting strategy for recommendation datasets.

    This splitter partitions a dataset into training, validation, and test sets based on
    the timestamps associated with interactions. The training set contains the oldest interactions,
    while the test set contains the most recent ones.

    """

    def __init__(self, test_ratio: float = 0, val_ratio: float = 0):
        
        """
        Initializes the TemporalHoldOut object.
        Args:
            test_ratio (float, optional): The proportion of the dataset to allocate to the test set.
                Must be between 0 and 1. Default is 0.
            val_ratio (float, optional): The proportion of the dataset to allocate to the validation set.
                Must be between 0 and 1. Default is 0.

        Raises:
            ValueError: If `test_ratio` or `val_ratio` are not in the range [0, 1].
        """

        self.params = {k: v for k, v in locals().items() if k != 'self'}

        self.test_ratio = test_ratio
        self.val_ratio = val_ratio

    @property
    def test_ratio(self) -> float:
        "The proportion of the dataset allocated to the test set."
        return self._test_ratio

    @test_ratio.setter
    def test_ratio(self, value: float) -> None:
        """
        Sets the test ratio.

        Args:
            value (float): The proportion of the dataset to allocate to the test set.
                Must be between 0 and 1.

        Raises:
            ValueError: If `value` is not in the range [0, 1].
        """
        if value < 0 or value > 1:
            raise ValueError('ratio must be between 0 and 1')
        self._test_ratio = value

    @property
    def val_ratio(self) -> float:
        """
        The proportion of the dataset allocated to the validation set.
        """
        return self._val_ratio

    @val_ratio.setter
    def val_ratio(self, value: float) -> None:
        """
        Sets the validation ratio.

        Args:
            value (float): The proportion of the dataset to allocate to the validation set.
                Must be between 0 and 1.

        Raises:
            ValueError: If `value` is not in the range [0, 1].
        """
        if value < 0 or value > 1:
            raise ValueError('ratio must be between 0 and 1')
        self._val_ratio = value

    def run(self, datarec: DataRec) -> Dict[str, DataRec]:
        """
        Splits the dataset using a temporal hold-out strategy.

        This method partitions the dataset into training, validation, and test sets based on
        the timestamps present in the `datarec` object. The split is performed such that the
        training set contains older interactions, while the test set contains more recent ones.

        Args:
            datarec (DataRec): A DataRec object containing the dataset and a timestamp column.

        Returns:
            (Dict[str, DataRec]): A dictionary with three keys:
                - `'train'`: A DataRec object containing the training set.
                - `'val'`: A DataRec object containing the validation set (if `val_ratio` > 0).
                - `'test'`: A DataRec object containing the test set (if `test_ratio` > 0).

        Raises:
            TypeError: If the `datarec` object does not contain a timestamp column.
        """

        if datarec.timestamp_col is None:
            raise TypeError('This DataRec does not contain temporal information')

        train, test, val = temporal_holdout(dataframe=datarec.data,
                                            test_ratio=self.test_ratio, val_ratio=self.val_ratio,
                                            temporal_col=datarec.timestamp_col)

        return self.output(datarec, train, test, val,
                           step_info={'operation': self.__class__.__name__, 'params': self.params})

