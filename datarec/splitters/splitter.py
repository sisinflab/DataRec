import pandas as pd
from typing import Dict
from datarec import DataRec
from datarec.io import RawData


class Splitter:
    """
    Base class for dataset splitters.

    This class provides a common interface for splitting datasets into training,
    validation, and test sets. Subclasses should implement specific splitting strategies.
    """

    @staticmethod
    def output(datarec: DataRec, train: pd.DataFrame, test: pd.DataFrame, validation: pd.DataFrame,
               step_info: Dict[str, Dict]) -> Dict[str, DataRec]:
        """
        Creates a dictionary of `DataRec` objects for train, test, and validation splits.

        Args:
            datarec (DataRec): The original dataset wrapped in a `DataRec` object.
            train (pd.DataFrame): The training split of the dataset.
            test (pd.DataFrame): The test split of the dataset.
            validation (pd.DataFrame): The validation split of the dataset.
            step_info (Dict[str, Dict]): Metadata of the transformation.
            
        Returns:
            (Dict[str, DataRec]): A dictionary containing the split datasets:
                - 'train': The training dataset as a `DataRec` object (if not empty).
                - 'test': The test dataset as a `DataRec` object (if not empty).
                - 'val': The validation dataset as a `DataRec` object (if not empty).
        """

        pipeline = datarec.pipeline.copy()
        pipeline.add_step(name='split', operation=step_info['operation'], params=step_info['params'])

        result = dict()
        for k, d in zip(['train', 'test', 'val'], [train, test, validation]):
            if len(d) > 0:
                new_datarec = DataRec(RawData(d,
                                              user=datarec.user_col,
                                              item=datarec.item_col,
                                              rating=datarec.rating_col,
                                              timestamp=datarec.timestamp_col),
                                      derives_from=datarec,
                                      dataset_name=datarec.dataset_name,
                                      pipeline=pipeline.copy())
                result[k] = new_datarec
        return result
