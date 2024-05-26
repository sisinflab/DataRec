import pandas as pd


def random_sample(dataframe: pd.DataFrame, n_samples: int = 1) -> (pd.DataFrame, pd.DataFrame):
    if n_samples < 1:
        raise ValueError

    samples = dataframe.sample(n=n_samples)

    if len(samples) != n_samples:
        raise ValueError
    else:
        return dataframe.drop(samples.index), samples


def min_by_col(dataframe: pd.DataFrame, discriminative_column) -> (pd.DataFrame, pd.DataFrame):
    if discriminative_column not in dataframe:
        raise ValueError

    min_value = dataframe[discriminative_column].min()
    candidates = dataframe.loc[dataframe[discriminative_column] == min_value]
    n_candidates = len(candidates)

    if n_candidates == 0:
        raise ValueError
    elif n_candidates == 1:
        return dataframe.drop(candidates.index), candidates
    else:
        candidates = candidates.sample(n=1)
        if len(candidates) != 1:
            raise ValueError
        return dataframe.drop(candidates.index), candidates


def temporal_holdout(dataframe: pd.DataFrame, test_ratio: float, val_ratio: float, temporal_col: str):
    print(test_ratio, print(val_ratio))
    if test_ratio < 0 or test_ratio > 1:
        raise ValueError

    if val_ratio < 0 or val_ratio > 1:
        raise ValueError

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
