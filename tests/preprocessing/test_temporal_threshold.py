import pytest
import pandas as pd
from datarec import DataRec, RawData
from datarec.splitters.uniform import TemporalThresholdSplit


@pytest.fixture
def sample_data():
    data = pd.DataFrame({
        'user': [1, 1, 2, 3, 3, 3, 4, 4],
        'item': [10, 20, 30, 40, 50, 60, 70, 80],
        'rating': [5, 4, 3, 5, 2, 1, 4, 5],
        'timestamp': [100, 150, 200, 250, 300, 350, 400, 450]
    })
    return DataRec(RawData(data, user='user', item='item', rating='rating', timestamp='timestamp'))


def test_temporal_threshold_split(sample_data):
    splitter = TemporalThresholdSplit(val_threshold=200, test_threshold=350)
    split_data = splitter.run(sample_data)

    assert set(split_data.keys()) == {'train', 'val', 'test'}
    assert set(split_data['train'].data['timestamp']) == {100, 150}
    assert set(split_data['val'].data['timestamp']) == {200, 250, 300}
    assert set(split_data['test'].data['timestamp']) == {350, 400, 450}


def test_temporal_threshold_split_invalid_threshold():
    with pytest.raises(ValueError, match="val_threshold must be strictly less than test_threshold"):
        TemporalThresholdSplit(val_threshold=300, test_threshold=200)


def test_temporal_threshold_split_no_timestamp():
    data = pd.DataFrame({'user': [1, 2], 'item': [10, 20], 'rating': [5, 3]})
    datarec = DataRec(RawData(data, user='user', item='item', rating='rating'))

    splitter = TemporalThresholdSplit(val_threshold=100, test_threshold=200)

    with pytest.raises(TypeError, match="This DataRec does not contain temporal information"):
        splitter.run(datarec)
