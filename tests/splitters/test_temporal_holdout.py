import pytest
import pandas as pd
from datarec.splitters.uniform import TemporalHoldOut
from datarec import DataRec, RawData


@pytest.fixture
def sample_datarec():
    data = pd.DataFrame({
        'user': [1, 2, 3, 4, 5],
        'item': [10, 20, 30, 40, 50],
        'rating': [5, 4, 3, 5, 2],
        'timestamp': [100, 200, 300, 400, 500]
    })
    return DataRec(RawData(data, user='user', item='item', rating='rating', timestamp='timestamp'))


@pytest.fixture
def no_timestamp_datarec():
    data = pd.DataFrame({
        'user': [1, 2, 3, 4, 5],
        'item': [10, 20, 30, 40, 50],
        'rating': [5, 4, 3, 5, 2]
    })
    return DataRec(RawData(data, user='user', item='item', rating='rating', timestamp=None))


def test_setter_valid():
    splitter = TemporalHoldOut(0.2, 0.1)
    assert splitter.test_ratio == 0.2
    assert splitter.val_ratio == 0.1


def test_setter_invalid_test():
    with pytest.raises(ValueError, match="ratio must be between 0 and 1"):
        TemporalHoldOut(-0.2, 0.1)


def test_setter_invalid_val():
    with pytest.raises(ValueError, match="ratio must be between 0 and 1"):
        TemporalHoldOut(0.2, -0.1)


def test_setter_invalid():
    with pytest.raises(ValueError, match="ratio must be between 0 and 1"):
        TemporalHoldOut(-0.2, -0.1)


def test_temporal_holdout_splitter(sample_datarec):
    splitter = TemporalHoldOut(test_ratio=0.4, val_ratio=0.25)
    splits = splitter.run(sample_datarec)

    assert 'train' in splits and 'test' in splits and 'val' in splits


def test_temporal_holdout_invalid_timestamp(no_timestamp_datarec):
    splitter = TemporalHoldOut(test_ratio=0.4, val_ratio=0.25)

    with pytest.raises(TypeError):
        splitter.run(no_timestamp_datarec)