import pandas as pd
from typing import Dict
from datarec import DataRec
from datarec.splitters.utils import random_sample
from datarec.splitters.splitter import Splitter


class LeaveNOut(Splitter):
    """
    Implements the Leave-N-Out splitting strategy for recommendation datasets.

    This splitter ensures that for each user, a fixed number of interactions (`test_n` and `validation_n`)
    are randomly selected and moved to the test and validation sets, respectively. The remaining interactions
    are kept in the training set.
    """

    def __init__(self, test_n: int = 0, validation_n: int = 0, seed: int = 42):
        """Initializes the LeaveNOut splitter.
        
        Args:
            test_n (int, optional): Number of interactions to move to the test set per user. Default is 0.
            validation_n (int, optional): Number of interactions to move to the validation set per user. Default is 0.
            seed (int, optional): Random seed for reproducibility. Default is 42.

        Raises:
            ValueError: If `test_n` or `validation_n` are negative.
            TypeError: If `test_n` or `validation_n` are not integers.
        """

        self.params = {k: v for k, v in locals().items() if k != 'self'}

        self.test_n = test_n
        self.validation_n = validation_n
        self.seed = seed

    @property
    def test_n(self) -> int:
        """Number of interactions to move to the test set per user."""
        return self._test_n

    @test_n.setter
    def test_n(self, value: int) -> None:
        """
        Sets the number of interactions to move to the test set per user.

        Args:
            value (int): Number of interactions.

        Raises:
            ValueError: If `value` is negative.
            TypeError: If `value` is not an integer.
        """
        if value < 0:
            raise ValueError("test_n must be greater or equal to 0.")
        if isinstance(value, float):
            raise TypeError("test_n must be an integer.")
        self._test_n = value

    @property
    def validation_n(self) -> int:
        """Number of interactions to move to the test set per user."""
        return self._validation_n

    @validation_n.setter
    def validation_n(self, value: int) -> None:
        """
        Sets the number of interactions to move to the validation set per user.

        Args:
            value (int): Number of interactions.

        Raises:
            ValueError: If `value` is negative.
            TypeError: If `value` is not an integer.
        """
        if value < 0:
            raise ValueError("validation_n must be greater or equal to 0.")
        if isinstance(value, float):
            raise TypeError("validation_n must be an integer.")
        self._validation_n = value

    def run(self, datarec: DataRec) -> Dict[str, DataRec]:
        """
        Splits the dataset into train, validation, and test sets using a Leave-N-Out approach.

        For each user, `test_n` interactions are randomly assigned to the test set, and `validation_n`
        interactions are assigned to the validation set. The remaining interactions are used for training.

        Args:
            datarec (DataRec): The dataset to be split.

        Returns:
            (Dict[str, DataRec]): A dictionary with the following keys:
                - "train": DataRec containing the training set.
                - "test": DataRec containing the test set, if `test_n` > 0.
                - "validation": DataRec containing the validation set, if `val_n` > 0.
        """

        train, test, val = pd.DataFrame(), pd.DataFrame(), pd.DataFrame()

        data = datarec.data
        for u in datarec.users:

            u_train, u_val, u_test = data[data.iloc[:, 0] == u], pd.DataFrame(), pd.DataFrame()

            if self.test_n:
                u_train, sample = random_sample(dataframe=u_train, n_samples=self.test_n, seed=self.seed)
                u_test = pd.concat([u_test, sample], axis=0, ignore_index=True)

            if self.validation_n:
                u_train, sample = random_sample(dataframe=u_train, n_samples=self.validation_n, seed=self.seed)
                u_val = pd.concat([u_val, sample], axis=0, ignore_index=True)

            train = pd.concat([train, u_train], axis=0, ignore_index=True)
            test = pd.concat([test, u_test], axis=0, ignore_index=True)
            val = pd.concat([val, u_val], axis=0, ignore_index=True)

        return self.output(datarec, train, test, val,
                           step_info={'operation': self.__class__.__name__, 'params': self.params})


class LeaveOneOut(LeaveNOut):
    """
    Implements the Leave-One-Out splitting strategy for recommendation datasets.

    This splitter ensures that for each user, at most one interaction is randomly selected and moved
    to the test and/or validation set, depending on the specified parameters. The remaining interactions
    are kept in the training set.

    This is a special case of `LeaveNOut` where `test_n=1` and/or `validation_n=1` if `test` and `validation`
    are set to `True`, respectively.
    """

    def __init__(self, test: bool = True, validation: bool = True, seed: int = 42):
        """Initializes the LeaveOneOut splitter.
        
        Args:
            test (bool, optional): Whether to include a test set. Defaults to True.
            validation (bool, optional): Whether to include a validation set. Defaults to True.
            seed (int, optional): Random seed for reproducibility. Default is 42.
            
        Raises:
            TypeError: If `test` or `validation` is not a boolean.
        """
        if not isinstance(test, bool):
            raise TypeError("test must be a boolean.")
        if not isinstance(validation, bool):
            raise TypeError("validation must be an boolean.")

        test = 1 if test else 0
        validation = 1 if validation else 0

        super().__init__(test_n=test, validation_n=validation, seed=seed)


class LeaveRatioOut(Splitter):
    """
    Splits the dataset into training, test, and validation sets based on a ratio instead of a fixed number of samples.

    This splitter selects a fraction of interactions for each user to be assigned to the test and validation sets,
    ensuring that the splits are proportional to the user's total number of interactions.
    """

    def __init__(self, test_ratio: float = 0, val_ratio: float = 0, seed: int = 42):
        """Initializes the LeaveRatioOut splitter.
        
        Args:
            test_ratio (float, optional): Proportion of each user's interactions assigned to the test set. Default is 0.
            val_ratio (float, optional): Proportion of each user's interactions assigned to the validation set. Default is 0.
            seed (int, optional): Random seed for reproducibility. Default is 42.

        Raises:
            ValueError: If `test_ratio` or `val_ratio` are not in the range [0, 1].
            ValueError: If the sum of `test_ratio` and `val_ratio` exceeds 1.
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
         Splits the dataset into train, test, and validation sets based on the specified ratios.

         The interactions of each user are sampled proportionally to create the test and validation sets.
         The remaining interactions are used as the training set.

         Args:
             datarec (DataRec): The dataset containing interactions and user-item relationships.

         Returns:
             (Dict[str, DataRec]): A dictionary containing the following keys:
                 - `"train"` (`DataRec`): The training dataset.
                 - `"test"` (`DataRec`): The test dataset, if `test_ratio` > 0.
                 - `"val"` (`DataRec`): The validation dataset, if `val_ratio` > 0.

         Raises:
             ValueError: If an empty dataset is encountered after sampling.
         """

        train, test, val = pd.DataFrame(), pd.DataFrame(), pd.DataFrame()

        data = datarec.data
        for u in datarec.users:
            u_train, u_val, u_test = data[data.iloc[:, 0] == u], pd.DataFrame(), pd.DataFrame()

            user_total = len(u_train)

            test_n_samples = round(self.test_ratio * user_total)
            val_n_samples = round(self.val_ratio * user_total)

            if test_n_samples > 0:
                u_train, sample = random_sample(dataframe=u_train, n_samples=min(test_n_samples, len(u_train)),
                                                seed=self.seed)
                u_test = pd.concat([u_test, sample], axis=0, ignore_index=True)

            if val_n_samples > 0:
                u_train, sample = random_sample(dataframe=u_train, n_samples=min(val_n_samples, len(u_train)),
                                                seed=self.seed)
                u_val = pd.concat([u_val, sample], axis=0, ignore_index=True)

            train = pd.concat([train, u_train], axis=0, ignore_index=True)
            test = pd.concat([test, u_test], axis=0, ignore_index=True)
            val = pd.concat([val, u_val], axis=0, ignore_index=True)

        return self.output(datarec, train, test, val,
                           step_info={'operation': self.__class__.__name__, 'params': self.params})
