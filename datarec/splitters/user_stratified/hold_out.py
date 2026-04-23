import pandas as pd
import warnings
from math import ceil
from typing import Dict
from sklearn.model_selection import train_test_split as split
from datarec import DataRec
from datarec.splitters.splitter import Splitter


class UserStratifiedHoldOut(Splitter):
    """
    Implements a user-stratified holdout split for a recommendation dataset.

    This splitter ensures that each user's interactions are split into training, validation,
    and test sets while maintaining the proportion specified by `test_ratio` and `val_ratio`.

    """

    def __init__(self, test_ratio: float = 0, val_ratio: float = 0, seed: int = 42):
        """Initializes the UserStratifiedHoldOut splitter.
        
        Args:
            test_ratio (float, optional): The proportion of interactions per user to include in the test set.
                Must be between 0 and 1. Default is 0.
            val_ratio (float, optional): The proportion of interactions per user to include in the validation set.
                Must be between 0 and 1. Default is 0.
            seed (int, optional): Random seed for reproducibility. Defaults to 42.

         Raises:
            ValueError: If `test_ratio` or `val_ratio` is not in the range [0, 1].
        """

        self.params = {k: v for k, v in locals().items() if k != 'self'}

        self.test_ratio = test_ratio
        self.val_ratio = val_ratio
        self.seed = seed

    @property
    def test_ratio(self) -> float:
        """The proportion of interactions per user for the test set."""
        return self._test_ratio

    @test_ratio.setter
    def test_ratio(self, value: float) -> None:
        """
        Sets the proportion of interactions per user for the test set.

        Args:
            value (float): Ratio for the test set. Must be between 0 and 1.

        Raises:
            ValueError: If the ratio is not between 0 and 1.
        """
        if value < 0 or value > 1:
            raise ValueError('ratio must be between 0 and 1')
        self._test_ratio = value

    @property
    def val_ratio(self) -> float:
        """ 
        The proportion of interactions per user for the validation set.
        """
        return self._val_ratio

    @val_ratio.setter
    def val_ratio(self, value: float) -> None:
        """
        Sets the proportion of remaining interactions per user for the validation set.

        Args:
            value (float): Ratio for the validation set. Must be between 0 and 1.

        Raises:
            ValueError: If the ratio is not between 0 and 1.
        """
        if value < 0 or value > 1:
            raise ValueError('ratio must be between 0 and 1')
        self._val_ratio = value

    @staticmethod
    def _can_split(n_samples: int, ratio: float) -> bool:
        """
        Returns whether a ratio-based split can leave at least one row
        in both train and held-out partitions.
        """
        if ratio <= 0 or n_samples <= 1:
            return False

        held_out = ceil(n_samples * ratio)
        return 0 < held_out < n_samples

    def run(self, datarec: DataRec) -> Dict[str, DataRec]:
        """
        Splits the dataset into train, validation, and test sets using a user-stratified holdout approach.

        Each user's interactions are split independently according to `test_ratio` and `val_ratio`, ensuring
        that the distribution is preserved per user. The function returns a dictionary containing the three
        resulting subsets.

        Args:
            datarec (DataRec): The dataset to be split.

        Returns:
            (Dict[str, DataRec]): A dictionary with the following keys:
                - "train": DataRec containing the training set.
                - "test": DataRec containing the test set, if `test_ratio` > 0.
                - "val": DataRec containing the validation set, if `val_ratio` > 0.
        """

        data = datarec.data
        user_col = datarec.user_col
        train_parts, test_parts, val_parts = [], [], []
        skipped_test_users = 0
        skipped_val_users = 0

        for _, user_data in data.groupby(user_col, sort=False):

            u_train, u_val, u_test = user_data, pd.DataFrame(), pd.DataFrame()

            if self.test_ratio:
                if self._can_split(len(u_train), self.test_ratio):
                    u_train, u_test = split(u_train, test_size=self._test_ratio, random_state=self.seed)
                else:
                    skipped_test_users += 1
            if self.val_ratio:
                if self._can_split(len(u_train), self.val_ratio):
                    u_train, u_val = split(u_train, test_size=self._val_ratio, random_state=self.seed)
                else:
                    skipped_val_users += 1

            train_parts.append(u_train)
            if not u_test.empty:
                test_parts.append(u_test)
            if not u_val.empty:
                val_parts.append(u_val)

        empty_split = pd.DataFrame(columns=data.columns)
        train = pd.concat(train_parts, axis=0, ignore_index=True) if train_parts else empty_split.copy()
        test = pd.concat(test_parts, axis=0, ignore_index=True) if test_parts else empty_split.copy()
        val = pd.concat(val_parts, axis=0, ignore_index=True) if val_parts else empty_split.copy()

        skipped = []
        if skipped_test_users:
            skipped.append(f"{skipped_test_users} users for test")
        if skipped_val_users:
            skipped.append(f"{skipped_val_users} users for validation")
        if skipped:
            warnings.warn(
                "UserStratifiedHoldOut skipped splitting "
                + " and ".join(skipped)
                + " because those users had too few interactions.",
                UserWarning,
                stacklevel=2,
            )

        return self.output(datarec=datarec, train=train, test=test, validation=val,
                           step_info={'operation': self.__class__.__name__, 'params': self.params})
