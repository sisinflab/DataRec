import pytest
import pandas as pd
from datarec.splitters.utils import random_sample


@pytest.fixture
def sample_dataframe():
    return pd.DataFrame({"A": range(10)})


def test_random_sample_correct_split(sample_dataframe):
    remaining, sampled = random_sample(sample_dataframe, seed=42, n_samples=3)

    assert len(sampled) == 3
    assert len(remaining) == 7
    assert set(sampled.index).isdisjoint(set(remaining.index))


def test_random_sample_reproducibility(sample_dataframe):
    _, sampled1 = random_sample(sample_dataframe, seed=42, n_samples=3)
    _, sampled2 = random_sample(sample_dataframe, seed=42, n_samples=3)

    pd.testing.assert_frame_equal(sampled1, sampled2)


def test_random_sample_invalid_n_samples(sample_dataframe):
    with pytest.raises(ValueError, match='number of samples must be greater than 1.'):
        random_sample(sample_dataframe, seed=42, n_samples=0)

    with pytest.raises(ValueError,
                       match='number of samples greater than the number of samples in the DataFrame.'):
        random_sample(sample_dataframe, seed=42, n_samples=11)
