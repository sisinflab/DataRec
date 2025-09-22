from datarec import DataRec
from datarec.processing.processor import Processor


class FilterByRatingThreshold(Processor):
    """
    Filters the dataset by removing interactions with a rating below a given threshold.
    """

    def __init__(self, rating_threshold: float):
        """
        Initializes the FilterByRatingThreshold object.
        
        Args:
            rating_threshold (float): The minimum rating required for an interaction to be kept.

        Raises:
            ValueError: If `rating_threshold` is a negative number.
        """
        if not isinstance(rating_threshold, (int, float)):
            raise ValueError("rating_threshold must be a number.")
        if rating_threshold < 0:
            raise ValueError("rating_threshold must be non-negative.")

        self.params = {k: v for k, v in locals().items() if k != 'self'}

        self.rating_threshold = rating_threshold

    def run(self, datarec: DataRec) -> DataRec:
        """
        Filters interactions with a rating below the threshold.

        Args:
            datarec (DataRec): The input dataset wrapped in a DataRec object.

        Returns:
            (DataRec): A new DataRec object with the processed dataset.
        """

        dataset = datarec.data
        filtered_data = dataset[dataset[datarec.rating_col] >= self.rating_threshold]

        return self.output(datarec, filtered_data, {'operation': self.__class__.__name__, 'params': self.params})


class FilterByUserMeanRating(Processor):
    """
    Filters the dataset by removing interactions with a rating below the user's average rating.

    This filter calculates the average rating given by each user and removes
    interactions where the rating is below that average.
    """

    def run(self, datarec: DataRec) -> DataRec:
        """
        Filters interactions with a rating below the user's mean rating.

        Args:
            datarec (DataRec): The input dataset wrapped in a DataRec object.

        Returns:
            (DataRec): A new DataRec object with the processed dataset.
        """

        dataset = datarec.data
        user_means = dataset.groupby(datarec.user_col)[datarec.rating_col].mean()

        filtered_data = dataset[
            dataset.apply(lambda row: row[datarec.rating_col] >= user_means[row[datarec.user_col]], axis=1)
        ]

        return self.output(datarec, filtered_data, {'operation': self.__class__.__name__, 'params': ''})


class FilterOutDuplicatedInteractions(Processor):
    """
    Filters a dataset by removing duplicated (user, item) interactions based on a specified strategy.
    """

    STRATEGIES = ['first', 'last', 'earliest', 'latest', 'random']

    def __init__(self, keep='first', random_seed=42):
        """
        Initializes the FilterOutDuplicatedInteractions object.
        
        Args:
            keep (str): Strategy to determine which interaction to keep when duplicates are found.
                Must be one of ['first', 'last', 'earliest', 'latest', 'random'].
            random_seed (int): Random seed used for reproducibility when using the 'random' strategy.

        Raises:
            ValueError: If the provided strategy (`keep`) is not among the supported options.
        """
        
        if keep not in self.STRATEGIES:
            raise ValueError(f"Invalid strategy '{keep}'. Choose from {self.STRATEGIES}.")

        self.params = {k: v for k, v in locals().items() if k != 'self'}

        self.keep = keep
        self.random_seed = random_seed

    def run(self, datarec: DataRec, verbose=True) -> DataRec:
        """
        Filter out duplicated (user, item) interactions in the dataset using the specified strategy.

        Args:
            datarec (DataRec): An object containing the dataset and metadata (user, item, timestamp columns, etc.)
            verbose (bool): Whether to print logging information during execution.

        Returns:
            (DataRec): A new DataRec object with duplicated (user, item) interactions removed according to the selected strategy.
        
        Raises:
            ValueError: If Date colum is not provided for 'earliest' and 'latest' strategies.
            ValueError: If the provided strategy (`keep`) is not among the supported options.
        """
        
        if verbose:
            print(f'Running filter-out duplicated interactions with strategy {self.keep}')
            print(f'Filtering DataRec: {datarec.dataset_name}')

        dataset = datarec.data
        subset = [datarec.user_col, datarec.item_col]

        # Random strategy
        if self.keep == 'random':
            dataset = dataset.sample(frac=1, random_state=self.random_seed).drop_duplicates(subset=subset, keep='first')

        # Ordering-based strategies
        elif self.keep in ['first', 'last']:
            dataset = dataset.drop_duplicates(subset=subset, keep=self.keep)

        # Temporal strategies
        elif self.keep in ['earliest', 'latest']:
            if datarec.timestamp_col is None:
                raise ValueError(f"Date column is required for '{self.keep}' strategy.")
            dataset = dataset.sort_values(by=datarec.timestamp_col, ascending=True)
            if self.keep == 'earliest':
                dataset = dataset.drop_duplicates(subset=subset, keep='first')
            else:
                dataset = dataset.drop_duplicates(subset=subset, keep='last')
        else:
            raise ValueError(f"Invalid strategy '{self.keep}'. Choose from {self.STRATEGIES}.")

        dataset = dataset.sort_values(by=[datarec.user_col, datarec.item_col], ascending=True)

        return self.output(datarec, dataset, {'operation': self.__class__.__name__, 'params': self.params})

