import pytest
import pandas as pd
from datarec import DataRec
from datarec.io import RawData
from datarec.processing.temporal import FilterByTime


@pytest.fixture
def sample_data():
    data = {
        'user': [1, 2, 3, 4],
        'item': [10, 20, 30, 40],
        'rating': [2.5, 3.5, 1.5, 4.0],
        'timestamp': [100, 200, 300, 400]
    }
    return DataRec(RawData(pd.DataFrame(data), user='user', item='item', rating='rating', timestamp='timestamp'))


def test_filter_before(sample_data):
    filter_by_time = FilterByTime(time_threshold=250.0, drop='before')
    result = filter_by_time.run(sample_data)

    assert len(result.data) == 2
    assert (result.data['timestamp'] <= 250).all()


def test_filter_after(sample_data):
    filter_by_time = FilterByTime(time_threshold=250.0, drop='after')
    result = filter_by_time.run(sample_data)

    assert len(result.data) == 2
    assert (result.data['timestamp'] > 250).all()


def test_filter_after_includes_threshold(sample_data):
    filter_by_time = FilterByTime(time_threshold=200.0, drop='after')
    result = filter_by_time.run(sample_data)

    assert len(result.data) == 3
    assert (result.data['timestamp'] >= 200).all()


def test_filter_no_timestamp_column():
    data = {
        'user': [1, 2],
        'item': [10, 20],
        'rating': [2.5, 3.5]
    }
    datarec = DataRec(RawData(pd.DataFrame(data), user='user', item='item', rating='rating'))

    filter_by_time = FilterByTime(time_threshold=250.0)

    with pytest.raises(TypeError, match="This DataRec does not contain temporal information"):
        filter_by_time.run(datarec)


def test_invalid_time_threshold():
    with pytest.raises(ValueError, match="time_threshold must be positive number."):
        FilterByTime(time_threshold=-10.0)

    with pytest.raises(ValueError, match="time_threshold must be positive number."):
        FilterByTime(time_threshold="invalid")


def test_invalid_drop_value():
    with pytest.raises(ValueError, match="Drop must be \"after\" or \"before\"."):
        FilterByTime(time_threshold=250.0, drop="invalid")
