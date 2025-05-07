import pandas as pd
from typing import Dict
from sklearn.model_selection import train_test_split as split
from datarec import DataRec
from datarec.splitters.splitter import Splitter


class RandomHoldOut(Splitter):
    """
    Implements a random holdout split for recommendation datasets.

    This splitter partitions the dataset into training, validation, and test sets
    using a random sampling approach. The proportions of the dataset allocated to
    the validation and test sets are controlled by `val_ratio` and `test_ratio`, respectively.

    Args:
        test_ratio (float, optional): The proportion of the dataset to include in the test set.
            Must be between 0 and 1. Default is 0.
        val_ratio (float, optional): The proportion of the dataset to include in the validation set.
            Must be between 0 and 1. Default is 0.
        seed (int, optional): The random seed for reproducibility. Defaults to 42.

    Raises:
        ValueError: If `test_ratio` or `val_ratio` is not in the range [0, 1].
    """

    def __init__(self, test_ratio: float = 0, val_ratio: float = 0, seed: int = 42):

        self.test_ratio = test_ratio
        self.val_ratio = val_ratio
        self.seed = seed

    @property
    def test_ratio(self) -> float:
        return self._test_ratio

    @test_ratio.setter
    def test_ratio(self, value: float) -> None:
        if value < 0 or value > 1:
            raise ValueError('ratio must be between 0 and 1')
        self._test_ratio = value

    @property
    def val_ratio(self) -> float:
        return self._val_ratio

    @val_ratio.setter
    def val_ratio(self, value: float) -> None:
        if value < 0 or value > 1:
            raise ValueError('ratio must be between 0 and 1')
        self._val_ratio = value

    def run(self, datarec: DataRec) -> Dict[str, DataRec]:
        """
        Splits the dataset into training, validation, and test sets according to the specified ratios.

        Args:
            datarec (DataRec): The dataset to be split.

        Returns:
            Dict[str, DataRec]: A dictionary with the following keys:
                - "train": The training dataset (`DataRec`).
                - "test": The test dataset (`DataRec`), if `test_ratio` > 0.
                - "val": The validation dataset (`DataRec`), if `val_ratio` > 0.
        """

        train, val, test = datarec.data, pd.DataFrame(), pd.DataFrame()

        if self.test_ratio:
            train, test = split(train, test_size=self._test_ratio, random_state=self.seed)

        if self.val_ratio:
            train, val = split(train, test_size=self._val_ratio, random_state=self.seed)

        return self.output(datarec=datarec, train=train, test=test, validation=val)

