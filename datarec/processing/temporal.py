from datarec import DataRec
from datarec.processing.processor import Processor


class FilterByTime(Processor):
    """
    Filters the dataset based on a time threshold and specified drop condition.

    This class allows filtering a dataset by a time threshold, either dropping
    records before or after the specified time.
    """

    def __init__(self, time_threshold: float = 0, drop: str = 'after'):
        """  
        Initializes the FilterByTime object.
         
        Args:
            time_threshold (float): The time threshold used for filtering. The dataset
                                    will be filtered based on this value.
            drop (str, optional): Specifies whether to drop records 'before' or 'after' the time threshold.

        Raises:
            ValueError: If `time_threshold` is negative or not a float, or if drop is
                        neither 'after' nor 'before'.
        """
        if not isinstance(time_threshold, (int, float)):
            raise ValueError('time_threshold must be positive number.')
        if isinstance(time_threshold, float) and time_threshold < 0:
            raise ValueError('time_threshold must be positive number.')

        if drop not in ['after', 'before']:
            raise ValueError(f'Drop must be "after" or "before".')

        self.params = {k: v for k, v in locals().items() if k != 'self'}
        self.time_threshold = time_threshold
        self.drop = drop

    def run(self, datarec: DataRec) -> DataRec:
        """
        Filters the dataset of the given DataRec based on the specified time threshold
        and drop condition, returning a new DataRec object with the filtered data.

        Args:
            datarec (DataRec): The input dataset wrapped in a DataRec object.

        Returns:
            (DataRec): A new DataRec object with the processed dataset.
             
        Raises:
            TypeError: If the DataRec does not contain temporal information.
        """

        if datarec.timestamp_col is None:
            raise TypeError('This DataRec does not contain temporal information')

        dataset = datarec.data

        if self.drop == 'before':
            data = dataset[dataset[datarec.timestamp_col] < self.time_threshold]
        else:
            data = dataset[dataset[datarec.timestamp_col] >= self.time_threshold]

        return self.output(datarec, data, {'operation': self.__class__.__name__, 'params': self.params})
