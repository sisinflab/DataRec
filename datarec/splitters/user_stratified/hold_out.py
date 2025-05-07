import pandas as pd
from typing import Dict
from sklearn.model_selection import train_test_split as split
from datarec import DataRec
from datarec.splitters.splitter import Splitter


class UserStratifiedHoldOut(Splitter):
    """
    Implements a user-stratified holdout split for a recommendation dataset.

    This splitter ensures that each user's interactions are split into training, validation,
    and test sets while maintaining the proportion specified by `test_ratio` and `val_ratio`.

    Args:
        test_ratio (float, optional): The proportion of interactions per user to include in the test set.
            Must be between 0 and 1. Default is 0.
        val_ratio (float, optional): The proportion of interactions per user to include in the validation set.
            Must be between 0 and 1. Default is 0.
        seed (int, optional): Random seed for reproducibility. Defaults to 42.

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
        Splits the dataset into train, validation, and test sets using a user-stratified holdout approach.

        Each user's interactions are split independently according to `test_ratio` and `val_ratio`, ensuring
        that the distribution is preserved per user. The function returns a dictionary containing the three
        resulting subsets.

        Args:
            datarec (DataRec): The dataset to be split.

        Returns:
            Dict[str, DataRec]: A dictionary with the following keys:
                - "train": DataRec containing the training set.
                - "test": DataRec containing the test set, if `test_ratio` > 0.
                - "val": DataRec containing the validation set, if `val_ratio` > 0.
        """

        train, test, val = pd.DataFrame(), pd.DataFrame(), pd.DataFrame()

        data = datarec.data
        for u in datarec.users:

            u_train, u_val, u_test = data[data.iloc[:, 0] == u], pd.DataFrame(), pd.DataFrame()

            if self.test_ratio:
                u_train, u_test = split(u_train, test_size=self._test_ratio, random_state=self.seed)
            if self.val_ratio:
                u_train, u_val = split(u_train, test_size=self._val_ratio, random_state=self.seed)

            train = pd.concat([train, u_train], axis=0, ignore_index=True)
            test = pd.concat([test, u_test], axis=0, ignore_index=True)
            val = pd.concat([val, u_val], axis=0, ignore_index=True)

        return self.output(datarec=datarec, train=train, test=test, validation=val)
