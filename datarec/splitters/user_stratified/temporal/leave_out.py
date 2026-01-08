import pandas as pd
from typing import Dict
from datarec import DataRec
from datarec.splitters.utils import max_by_col
from datarec.splitters.splitter import Splitter


class LeaveNLast(Splitter):
    """
    Splits the dataset by removing the last `n` interactions per user based on a timestamp column.

    This splitter selects the last `test_n` interactions for the test set and the last `validation_n`
    interactions for the validation set while keeping the remaining interactions in the training set.
    """
    def __init__(self, test_n: int = 0, validation_n: int = 0, seed: int = 42):
        """Initializes the LeaveNLast splitter.

        Args:
            test_n (int, optional): Number of last interactions for the test set. Defaults to 0.
            validation_n (int, optional): Number of last interactions for the validation set. Defaults to 0.
            seed (int, optional): Random seed for reproducibility. Defaults to 42.
        """

        self.params = {k: v for k, v in locals().items() if k != 'self'}

        self.test_n = test_n
        self.validation_n = validation_n
        self.seed = seed

    @property
    def test_n(self) -> int:
        """The number of last interactions per user for the test set."""
        return self._test_n

    @test_n.setter
    def test_n(self, value: int) -> None:
        """
        Sets the number of last interactions per user for the test set.

        Args:
            value (int): Number of interactions. Must be >= 0.

        Raises:
            ValueError: If `value` < 0.
            TypeError: If `value` is not an integer.
        """
        if value < 0:
            raise ValueError("test_n must be greater or equal than 0.")
        if isinstance(value, float):
            raise TypeError("test_n must be an integer.")
        self._test_n = value

    @property
    def validation_n(self) -> int:
        """The number of last interactions per user for the validation set."""
        return self._validation_n

    @validation_n.setter
    def validation_n(self, value: int) -> None:
        """
        Sets the number of last interactions per user for the validation set.

        Args:
            value (int): Number of interactions. Must be >= 0.

        Raises:
            ValueError: If `value` < 0.
            TypeError: If `value` is not an integer.
        """
        if value < 0:
            raise ValueError("validation_n must be greater or equal than 0.")
        if isinstance(value, float):
            raise TypeError("validation_n must be and integer.")
        self._validation_n = value

    def run(self, datarec: DataRec) -> Dict[str, DataRec]:
        """
        Splits the dataset into train, test, and validation sets based on the last `n` interactions.

        Args:
            datarec (DataRec): The dataset containing the interactions and timestamp column.

        Returns:
            (Dict[str, DataRec]): A dictionary with the following keys:
                - "train": The training dataset (`DataRec`).
                - "test": The test dataset (`DataRec`), if `test_n` > 0.
                - "val": The validation dataset (`DataRec`), if `val_n` > 0.

        Raises:
            TypeError: If the dataset does not contain a timestamp column.
        """

        if datarec.timestamp_col is None:
            raise TypeError('This DataRec does not contain temporal information')

        train, test, val = pd.DataFrame(), pd.DataFrame(), pd.DataFrame()

        data = datarec.data
        for u in datarec.users:

            u_train, u_val, u_test = data[data.iloc[:, 0] == u], pd.DataFrame(), pd.DataFrame()

            if self.test_n:
                for _ in range(self.test_n):
                    u_train, sample = max_by_col(u_train, datarec.timestamp_col, seed=self.seed)
                    u_test = pd.concat([u_test, sample], axis=0, ignore_index=True)

            if self.validation_n:
                for _ in range(self.validation_n):
                    u_train, sample = max_by_col(u_train, datarec.timestamp_col, seed=self.seed)
                    u_val = pd.concat([u_val, sample], axis=0, ignore_index=True)

            train = pd.concat([train, u_train], axis=0, ignore_index=True)
            test = pd.concat([test, u_test], axis=0, ignore_index=True)
            val = pd.concat([val, u_val], axis=0, ignore_index=True)

        return self.output(datarec, train, test, val,
                           step_info={'operation': self.__class__.__name__, 'params': self.params})


class LeaveOneLast(LeaveNLast):
    """
    Special case of LeaveNLast that removes only the last interaction per user for test and validation.

    This class sets `test_n` and `validation_n` to 1 if their corresponding boolean parameters are True.

    """

    def __init__(self, test: bool = True, validation: bool = True, seed: int = 42):
        """
        Initializes the LeaveOneLast splitter.

        Args:
            test (bool, optional): Whether to remove the last interaction for the test set. Defaults to True.
            validation (bool, optional): Whether to remove the last interaction for the validation set. Defaults to True.
            seed (int, optional): Random seed for reproducibility. Default is 42.

        Raises:
            TypeError: If `test` or `validation` are not boolean.
        """
        if not isinstance(test, bool):
            raise TypeError("test must be a boolean.")
        if not isinstance(validation, bool):
            raise TypeError("validation must be an boolean.")

        test = 1 if test else 0
        validation = 1 if validation else 0

        super().__init__(test_n=test, validation_n=validation, seed=seed)

        self.params = {
            "test": test,
            "validation": validation,
            "seed": seed,
        }


class LeaveRatioLast(Splitter):
    """
    Splits the dataset into training, test, and validation sets by selecting the most recent interactions
    for each user based on a specified ratio.

    Unlike `LeaveNLast`, which selects a fixed number of interactions, this splitter chooses a fraction
    of the total interactions per user, preserving temporal order.

    """

    def __init__(self, test_ratio: float = 0, val_ratio: float = 0, seed: int = 42):
        """
        Args:
            test_ratio (float, optional): Proportion of each user's interactions assigned to the test set. Default is 0.
            val_ratio (float, optional): Proportion of each user's interactions assigned to the validation set. Default is 0.
            seed (int, optional): Random seed for reproducibility. Default is 42.

        Raises:
            ValueError: If `test_ratio` or `val_ratio` are not in the range [0, 1].
            ValueError: If `test_ratio + val_ratio` > 1.
        """
        if not (0 <= test_ratio <= 1):
            raise ValueError('ratio must be between 0 and 1')
        if not (0 <= val_ratio <= 1):
            raise ValueError('ratio must be between 0 and 1')
        if test_ratio + val_ratio > 1:
            raise ValueError("sum of test_ratio and val_ratio must not exceed 1")

        self.params = {k: v for k, v in locals().items() if k != 'self'}

        self.test_ratio = test_ratio
        self.val_ratio = val_ratio
        self.seed = seed

    def run(self, datarec: DataRec) -> Dict[str, DataRec]:
        """
        Splits the dataset into train, test, and validation sets by selecting the last interactions
        (in chronological order) for each user.

        The most recent interactions are removed first for the test set, then for the validation set,
        leaving the remaining interactions for training.

        Args:
            datarec (DataRec): The dataset containing interactions with a timestamp column.

        Returns:
            (Dict[str, DataRec]): A dictionary containing the following keys:
                - `"train"` (`DataRec`): The training dataset.
                - `"test"` (`DataRec`): The test dataset, if `test_ratio` > 0.
                - `"val"` (`DataRec`): The validation dataset, if `val_ratio` > 0.

        Raises:
            TypeError: If the dataset does not contain a timestamp column.
        """

        if datarec.timestamp_col is None:
            raise TypeError('This DataRec does not contain temporal information')

        train, test, val = pd.DataFrame(), pd.DataFrame(), pd.DataFrame()

        data = datarec.data
        for u in datarec.users:
            u_train, u_val, u_test = data[data.iloc[:, 0] == u], pd.DataFrame(), pd.DataFrame()

            user_total = len(u_train)

            test_n_samples = round(self.test_ratio * user_total)
            val_n_samples = round(self.val_ratio * user_total)

            if test_n_samples > 0:
                for _ in range(min(test_n_samples, len(u_train))):
                    u_train, sample = max_by_col(u_train, datarec.timestamp_col, seed=self.seed)
                    u_test = pd.concat([u_test, sample], axis=0, ignore_index=True)

            if val_n_samples > 0:
                for _ in range(min(val_n_samples, len(u_train))):
                    u_train, sample = max_by_col(u_train, datarec.timestamp_col, seed=self.seed)
                    u_val = pd.concat([u_val, sample], axis=0, ignore_index=True)

            train = pd.concat([train, u_train], axis=0, ignore_index=True)
            test = pd.concat([test, u_test], axis=0, ignore_index=True)
            val = pd.concat([val, u_val], axis=0, ignore_index=True)

        return self.output(datarec, train, test, val,
                           step_info={'operation': self.__class__.__name__, 'params': self.params})

