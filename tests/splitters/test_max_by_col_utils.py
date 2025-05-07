import pytest
import pandas as pd
from datarec.splitters.utils import max_by_col


@pytest.fixture
def sample_dataframe():
    return pd.DataFrame({"user": [3, 1, 2, 1, 4], "item": [0, 1, 0, 2, 2]})


def test_max_by_col_correct_selection(sample_dataframe):
    remaining, selected = max_by_col(sample_dataframe, "user", seed=42)

    assert selected["user"].iloc[0] == 4
    assert len(selected) == 1
    assert len(remaining) == 4
    assert set(selected.index).isdisjoint(set(remaining.index))


def test_max_by_col_reproducibility(sample_dataframe):
    _, selected1 = max_by_col(sample_dataframe, "user", seed=42)
    _, selected2 = max_by_col(sample_dataframe, "user", seed=42)

    pd.testing.assert_frame_equal(selected1, selected2)


def test_max_by_col_non_existent_column(sample_dataframe):
    with pytest.raises(ValueError, match="Column 'timestamp' must be in the dataframe"):
        max_by_col(sample_dataframe, "timestamp", seed=42)


def test_max_by_col_empty_dataframe():
    empty = pd.DataFrame(columns=["user"])
    with pytest.raises(ValueError, match="No candidate."):
        max_by_col(empty, "user", seed=42)

