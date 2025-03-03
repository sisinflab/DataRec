import os.path

from recpack.datasets.base import Dataset
import pandas as pd
import numpy as np


class DataRec(Dataset):
    """
    Base class for DataRec Datasets
    """
    USER_IX = "userId"
    """Name of the column in the DataFrame that contains user identifiers."""
    ITEM_IX = "itemId"
    """Name of the column in the DataFrame that contains item identifiers."""
    TIMESTAMP_IX = "timestamp"
    """Name of the column in the DataFrame that contains time of interaction in seconds since epoch."""

    @property
    def DEFAULT_FILENAME(self) -> str:
        """Default filename that will be used if it is not specified by the user."""
        return f"datarec.tsv"

    def _load_dataframe(self) -> pd.DataFrame:
        """Dataset from DataRec will be loaded as a pandas DataFrame

        .. warning::

            This does not apply any preprocessing, and returns the raw dataset.

        :return: The interaction data as a DataFrame with a row per interaction.
        :rtype: pd.DataFrame
        """

        df = pd.read_csv(os.path.join(self.path, self.filename), sep='\t', header=True, dtype={
                self.USER_IX: str,
                self.TIMESTAMP_IX: np.int64,
                self.ITEM_IX: str,
            })
        return df
