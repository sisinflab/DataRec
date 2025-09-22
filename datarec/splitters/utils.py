import pandas as pd
from typing import Tuple


def random_sample(dataframe: pd.DataFrame, seed: int, n_samples: int = 1) -> Tuple[pd.DataFrame, pd.DataFrame]:
    """
    Randomly selects a specified number of samples from a given DataFrame.

    This function splits the input DataFrame into two subsets:
    - One containing `n_samples` randomly selected rows.
    - One containing the remaining rows after the selection.

    Args:
        dataframe (pd.DataFrame): The input DataFrame from which to sample.
        seed (int): Random seed for reproducibility.
        n_samples (int, optional): The number of samples to extract. Must be at least 1. Default is 1.

    Returns:
        (Tuple[pd.DataFrame, pd.DataFrame]):
            - The first DataFrame contains the remaining data after sampling.
            - The second DataFrame contains the randomly selected samples.

    Raises:
        ValueError: If `n_samples` is less than 1 or lesser/greater than the number of rows in the DataFrame.
    """

    if n_samples < 1:
        raise ValueError('number of samples must be greater than 1.')

    if n_samples > len(dataframe):
        raise ValueError('number of samples greater than the number of samples in the DataFrame.')

    samples = dataframe.sample(n=n_samples, random_state=seed)

    if len(samples) != n_samples:
        raise ValueError('number of samples lesser or greater than the number of rows in the DataFrame.')
    else:
        return dataframe.drop(samples.index), samples


def max_by_col(dataframe: pd.DataFrame, discriminative_column: str, seed: int) -> Tuple[pd.DataFrame, pd.DataFrame]:
    """
    Selects the row with the minimum value in the specified column from the given DataFrame.
    If multiple rows have the same minimum value, one is randomly selected.

    Args:
        dataframe (pd.DataFrame): The input DataFrame.
        discriminative_column (str): The column used to determine the minimum value.
        seed (int): Random seed for reproducibility.

    Returns:
        (Tuple[pd.DataFrame, pd.DataFrame]):
        - The first DataFrame contains the remaining rows after removing the selected row.
        - The second DataFrame contains the selected row with the minimum value.

    Raises:
        ValueError: If the specified column is not present in the DataFrame.
        ValueError: If no candidates are found (should not happen unless DataFrame is empty).
        ValueError: If the random selection fails to return exactly one row.
    """

    if discriminative_column not in dataframe:
        raise ValueError(f'Column \'{discriminative_column}\' must be in the dataframe.')

    max_value = dataframe[discriminative_column].max()
    candidates = dataframe.loc[dataframe[discriminative_column] == max_value]
    n_candidates = len(candidates)

    if n_candidates == 0:
        raise ValueError('No candidate.')
    elif n_candidates == 1:
        return dataframe.drop(candidates.index), candidates
    else:
        candidates = candidates.sample(n=1, random_state=seed)
        if len(candidates) != 1:
            raise ValueError('Number of candidates lesser or greater than 1.')
        return dataframe.drop(candidates.index), candidates


def temporal_holdout(dataframe: pd.DataFrame, test_ratio: float, val_ratio: float, temporal_col: str) \
        -> Tuple[pd.DataFrame, pd.DataFrame, pd.DataFrame]:
    """
    Splits a dataset into training, validation, and test sets based on temporal ordering.

    The function sorts the dataset according to a specified timestamp column and assigns
    the oldest interactions to the training set, followed by the validation set (if applicable),
    and the most recent interactions to the test set.

    Args:
        dataframe (pd.DataFrame): The input dataset containing interaction data.
        test_ratio (float): The proportion of the dataset to allocate to the test set. Must be between 0 and 1.
        val_ratio (float): The proportion of the dataset to allocate to the validation set. Must be between 0 and 1.
        temporal_col (str): The name of the column containing timestamp information.

    Returns:
        (Tuple[pd.DataFrame, pd.DataFrame, pd.DataFrame]): A tuple containing the train, validation, and test sets.

    Raises:
        ValueError: If `test_ratio` or `val_ratio` are not in the range [0, 1].
    """

    if test_ratio < 0 or test_ratio > 1:
        raise ValueError('test ratio must be between 0 and 1.')

    if val_ratio < 0 or val_ratio > 1:
        raise ValueError('val ratio must be between 0 and 1.')

    train, test, val = pd.DataFrame(), pd.DataFrame(), pd.DataFrame()

    total_samples = len(dataframe)

    test_samples = round(total_samples * test_ratio)
    train_samples = total_samples - test_samples
    val_samples = round(train_samples * val_ratio)

    train_samples = total_samples - test_samples - val_samples

    assert (train_samples + val_samples + test_samples) == total_samples

    ordered = dataframe.sort_values(by=temporal_col)

    train = ordered.iloc[:train_samples]
    if val_samples:
        val = ordered.iloc[train_samples:(train_samples + val_samples)]
    if test_samples:
        test = ordered.iloc[(train_samples + val_samples):]

    assert len(train) == train_samples
    assert len(val) == val_samples
    assert len(test) == test_samples

    return train, test, val

