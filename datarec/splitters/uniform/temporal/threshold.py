from typing import Dict
from datarec import DataRec
from datarec.splitters.splitter import Splitter


class TemporalThresholdSplit(Splitter):
    """
    Splits a dataset into training, validation, and test sets based on two timestamp thresholds.

    The dataset is divided such that:
    - The training set contains interactions occurring strictly before `val_threshold`.
    - The validation set contains interactions occurring between `val_threshold` (inclusive)
      and `test_threshold` (exclusive).
    - The test set contains interactions occurring at or after `test_threshold`.
    """

    def __init__(self, val_threshold: float, test_threshold: float):
        """Initializes the TemporalThresholdSplit object.
        
        Args:
            val_threshold (float): The timestamp value that defines the split between training and validation.
            test_threshold (float): The timestamp value that defines the split between validation and test.

        Raises:
            ValueError: If `val_threshold` is not strictly less than `test_threshold`.
        """
        
        if val_threshold >= test_threshold:
            raise ValueError('val_threshold must be strictly less than test_threshold')

        self.params = {k: v for k, v in locals().items() if k != 'self'}

        self.val_threshold = val_threshold
        self.test_threshold = test_threshold

    def run(self, datarec: DataRec) -> Dict[str, DataRec]:
        """
        Splits the dataset into training, validation, and test sets based on two thresholds.

        Args:
            datarec (DataRec): A DataRec object containing the dataset with a timestamp column.

        Returns:
            Dict[str, DataRec]: A dictionary with:
                - `'train'`: Training set (timestamps < `val_threshold`).
                - `'val'`: Validation set (timestamps between `val_threshold` and `test_threshold`).
                - `'test'`: Test set (timestamps >= `test_threshold`).

        Raises:
            TypeError: If the `datarec` object does not contain a timestamp column.
        """

        if datarec.timestamp_col is None:
            raise TypeError('This DataRec does not contain temporal information')

        dataset = datarec.data

        train = dataset[dataset[datarec.timestamp_col] < self.val_threshold]

        val = dataset[(dataset[datarec.timestamp_col] >= self.val_threshold) &
                      (dataset[datarec.timestamp_col] < self.test_threshold)]

        test = dataset[dataset[datarec.timestamp_col] >= self.test_threshold]

        return self.output(datarec, train, test, val,
                           step_info={'operation': self.__class__.__name__, 'params': self.params})
