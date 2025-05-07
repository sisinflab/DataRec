from datarec import DataRec
from datarec.io import RawData


class FilterByTime:
    """
    Filters the dataset based on a time threshold and specified drop condition.

    This class allows filtering a dataset by a time threshold, either dropping
    records before or after the specified time.

    Args:
        time_threshold (float): The time threshold used for filtering. The dataset
                                 will be filtered based on this value.
        drop (str, optional): Specifies whether to drop records 'before' or 'after' the time threshold.

    Raises:
        ValueError: If time_threshold is negative or not a float, or if drop is
                    neither 'after' nor 'before'.
    """

    def __init__(self, time_threshold: float = 0, drop: str = 'after'):

        if not isinstance(time_threshold, (int, float)):
            raise ValueError('time_threshold must be positive number.')
        if isinstance(time_threshold, float) and time_threshold < 0:
            raise ValueError('time_threshold must be positive number.')
        self.time_threshold = time_threshold

        if drop not in ['after', 'before']:
            raise ValueError(f'Drop must be "after" or "before".')
        self.drop = drop

    def run(self, datarec: DataRec):
        """
        Filters the dataset of the given DataRec based on the specified time threshold
        and drop condition, returning a new DataRec object with the filtered data.


        Args:
            datarec (DataRec): The input dataset wrapped in a DataRec object.

        Raises:
            TypeError: If the DataRec does not contain temporal information.

        Returns:
            DataRec: A new DataRec object with the processed dataset.
        """

        if datarec.timestamp_col is None:
            raise TypeError('This DataRec does not contain temporal information')

        dataset = datarec.data

        if self.drop == 'before':
            data = dataset[dataset[datarec.timestamp_col] < self.time_threshold]
        else:
            data = dataset[dataset[datarec.timestamp_col] >= self.time_threshold]

        new_datarec = DataRec(RawData(data,
                                      user=datarec.user_col,
                                      item=datarec.item_col,
                                      rating=datarec.rating_col,
                                      timestamp=datarec.timestamp_col),
                              derives_from=datarec)

        return new_datarec
