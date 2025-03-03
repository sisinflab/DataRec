from datarec import DataRec
from datarec.io import RawData


class FilterByRatingThreshold:
    """
    Filters the dataset by removing interactions with a rating below a given threshold.

    Args:
        rating_threshold (float): The minimum rating required for an interaction to be kept.

    Raises:
        ValueError: If rating_threshold is not a positive number.
    """

    def __init__(self, rating_threshold: float):
        if not isinstance(rating_threshold, (int, float)):
            raise ValueError("rating_threshold must be a number.")
        if rating_threshold < 0:
            raise ValueError("rating_threshold must be non-negative.")
        self.rating_threshold = rating_threshold

    def run(self, datarec: DataRec) -> DataRec:
        """
        Filters interactions with a rating below the threshold.

        Args:
            datarec (DataRec): The input dataset wrapped in a DataRec object.

        Returns:
            DataRec: A new DataRec object with the processed dataset.
        """

        dataset = datarec.data
        filtered_data = dataset[dataset[datarec.rating_col] >= self.rating_threshold]

        new_datarec = DataRec(RawData(filtered_data,
                                      user=datarec.user_col,
                                      item=datarec.item_col,
                                      rating=datarec.rating_col,
                                      timestamp=datarec.timestamp_col),
                              derives_from=datarec)

        return new_datarec


class FilterByUserMeanRating:
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
            DataRec: A new DataRec object with the processed dataset.
        """

        dataset = datarec.data
        user_means = dataset.groupby(datarec.user_col)[datarec.rating_col].mean()

        filtered_data = dataset[
            dataset.apply(lambda row: row[datarec.rating_col] >= user_means[row[datarec.user_col]], axis=1)
        ]

        new_datarec = DataRec(RawData(filtered_data,
                                      user=datarec.user_col,
                                      item=datarec.item_col,
                                      rating=datarec.rating_col,
                                      timestamp=datarec.timestamp_col),
                              derives_from=datarec)

        return new_datarec
