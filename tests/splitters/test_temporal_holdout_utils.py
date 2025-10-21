import pytest
import pandas as pd
from datarec.splitters.utils import temporal_holdout


@pytest.fixture
def sample_dataframe():
    return pd.DataFrame({
        'user': [1, 2, 3, 4, 5],
        'item': [10, 20, 30, 40, 50],
        'rating': [5, 4, 3, 5, 2],
        'timestamp': [100, 200, 300, 400, 500]
    })


def test_temporal_holdout_valid_splits(sample_dataframe):
    train, test, val = temporal_holdout(sample_dataframe, test_ratio=0.4, val_ratio=0.25, temporal_col='timestamp')

    assert len(train) == 2
    assert len(val) == 1
    assert len(test) == 2
    assert train['timestamp'].max() < val['timestamp'].min()
    assert val['timestamp'].max() < test['timestamp'].min()


def test_temporal_holdout_edge_cases(sample_dataframe):

    # Test with 0% test and validation
    train, test, val = temporal_holdout(sample_dataframe, test_ratio=0, val_ratio=0, temporal_col='timestamp')
    assert len(train) == 5
    assert len(test) == 0
    assert len(val) == 0

    # Test with full test set
    train, test, val = temporal_holdout(sample_dataframe, test_ratio=1, val_ratio=0, temporal_col='timestamp')
    assert len(train) == 0
    assert len(test) == 5
    assert len(val) == 0

    # Test invalid ratios
    with pytest.raises(ValueError):
        temporal_holdout(sample_dataframe, test_ratio=-0.1, val_ratio=0, temporal_col='timestamp')

    with pytest.raises(ValueError):
        temporal_holdout(sample_dataframe, test_ratio=1.2, val_ratio=0, temporal_col='timestamp')
