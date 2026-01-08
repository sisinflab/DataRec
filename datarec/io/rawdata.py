import pandas as pd
from typing import Optional, TYPE_CHECKING

if TYPE_CHECKING:
    from datarec.pipeline.pipeline_step import PipelineStep


class RawData:
    """
    Container for raw datasets in DataRec.

    Wraps a `pandas.DataFrame` and stores metadata about user, item, rating, and timestamp columns.
    Provides lightweight methods for slicing, copying, and merging data.
    """
    def __init__(
            self,
            data=None,
            header=False,
            user=None,
            item=None,
            rating=None,
            timestamp=None,
            user_encoder=None,
            item_encoder=None):
        """
        Initialize a RawData object.

        Args:
            data (pd.DataFrame): DataFrame of the dataset. Defaults to None.
            header (bool): Whether the file has a header. Defaults to False.
            user (str): Column name for user IDs.
            item (str): Column name for item IDs.
            rating (str): Column name for ratings.
            timestamp (str): Column name for timestamps.
            user_encoder (dict | None): Optional user encoding mapping.
            item_encoder (dict | None): Optional item encoding mapping.
        """
        self.data = data
        self.header = header
        if data is None:
            self.data = pd.DataFrame
            self.header = header
        self.path = None

        self.user = user
        self.item = item
        self.rating = rating
        self.timestamp = timestamp
        # Aliases for consistency with DataRec naming
        self.user_col = user
        self.item_col = item
        self.rating_col = rating
        self.timestamp_col = timestamp
        # Aliases for consistency with DataRec naming
        self.user_col = user
        self.item_col = item
        self.rating_col = rating
        self.timestamp_col = timestamp
        # Aliases for consistency with DataRec naming
        self.user_col = user
        self.item_col = item
        self.rating_col = rating
        self.timestamp_col = timestamp
        # Optional encoders to support streaming/incremental loading
        self.user_encoder = user_encoder
        self.item_encoder = item_encoder

        self.pipeline_step: Optional["PipelineStep"] = None  # To track the pipeline step that produced this RawData

    def append(self, new_data) -> None:
        """
        Append new rows to the dataset.

        Args:
            new_data (pd.DataFrame): DataFrame to append.

        Returns:
            None
        """
        self.data.append(new_data)

    def copy(self, deep=True) -> "RawData":
        """
        Make a copy of the dataset.

        Args:
            deep (bool): If True, return a deep copy of the dataset.

        Returns:
            (RawData): A copy of the dataset.

        """
        return RawData(
            self.data.copy(deep=deep),
            header=self.header,
            user=self.user,
            item=self.item,
            rating=self.rating,
            timestamp=self.timestamp,
            user_encoder=self.user_encoder,
            item_encoder=self.item_encoder,
        )

    def __repr__(self):
        """
        Return a string representation of the dataset.
        """
        return repr(self.data)

    def __len__(self):
        """
        Return the length of the dataset.
        """
        return len(self.data)

    def __getitem__(self, idx):
        """
        Return the item at the given index.
        Args:
            idx: index of the item to return.

        Returns:
            (RawData): the sample at the given index.

        """
        return self.data[idx]

    def __add__(self, other):
        """
        Concatenate two RawData objects.
        Args:
            other (RawData): the other RawData to concatenate.

        Returns:
            (RawData): the concatenated RawData object.

        """
        self.__check_rawdata_compatibility__(other)
        new_data = pd.concat([self.data, other.data])
        new_rawdata = RawData(new_data, user=self.user, item=self.item, rating=self.rating,
                              timestamp=self.timestamp, header=self.header)
        return new_rawdata

    def __iter__(self):
        """
        Iterate over dataset rows.

        Returns:
            (pd.Series): Each row in the dataset.

        """
        return iter(self.data)

    def __check_rawdata_compatibility__(self, rawdata):
        """
        Check compatibility between RawData objects.
        Args:
            rawdata (RawData): RawData object to check.

        Returns:
            (bool): True if compatibility is verified.

        """
        return __check_rawdata_compatibility__(self, rawdata)


def __check_rawdata_compatibility__(rawdata1: RawData, rawdata2: RawData):
    """
    Check compatibility between two RawData objects.
    Args:
        rawdata1 (RawData): First RawData object to check.
        rawdata2 (RawData): Second RawData object to check.

    Returns:
        (bool): True if compatibility is verified.

    """
    if rawdata1.user != rawdata2.user:
        raise ValueError('User columns are not compatible')
    if rawdata1.item != rawdata2.item:
        raise ValueError('Item columns are not compatible')
    if rawdata1.rating != rawdata2.rating:
        raise ValueError('Rating columns are not compatible')
    if rawdata1.timestamp != rawdata2.timestamp:
        raise ValueError('Timestamp columns are not compatible')
    if rawdata1.header != rawdata2.header:
        raise ValueError('Header is not compatible')
    return True
