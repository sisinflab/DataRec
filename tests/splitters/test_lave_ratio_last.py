import pytest
import pandas as pd
from datarec import DataRec, RawData
from datarec.splitters.user_stratified import LeaveRatioLast


@pytest.fixture
def sample_datarec():
    data = pd.DataFrame({
        'user': [1, 1, 1, 2, 2, 2, 3, 3, 3],
        'item': [10, 20, 30, 40, 50, 60, 70, 80, 90],
        'rating': [5, 4, 3, 5, 3, 4, 2, 5, 1],
        "timestamp": [10, 20, 30, 40, 50, 60, 70, 80, 90]
    })
    return DataRec(RawData(data, user="user", item="item", rating="rating", timestamp="timestamp"))


def test_setter_valid():
    splitter = LeaveRatioLast(test_ratio=0.2, val_ratio=0.1)
    assert splitter.test_ratio == 0.2
    assert splitter.val_ratio == 0.1


def test_setter_invalid():
    with pytest.raises(ValueError, match="ratio must be between 0 and 1"):
        LeaveRatioLast(test_ratio=-0.2, val_ratio=0.1)

    with pytest.raises(ValueError, match="ratio must be between 0 and 1"):
        LeaveRatioLast(test_ratio=0.2, val_ratio=-0.1)

    with pytest.raises(ValueError, match="ratio must be between 0 and 1"):
        LeaveRatioLast(test_ratio=-0.2, val_ratio=-0.1)

    with pytest.raises(ValueError, match="ratio must be between 0 and 1"):
        LeaveRatioLast(test_ratio=-0.2, val_ratio=-0.1)

    with pytest.raises(ValueError, match="ratio must be between 0 and 1"):
        LeaveRatioLast(test_ratio=2, val_ratio=0.1)

    with pytest.raises(ValueError, match="sum of test_ratio and val_ratio must not exceed 1"):
        LeaveRatioLast(0.7, 0.5)


def test_no_timestamp():
    data = pd.DataFrame({
        "user": [1, 1, 1, 2, 2, 3],
        "item": [101, 102, 103, 201, 202, 301],
        "rating": [1, 1, 1, 1, 1, 1],
    })
    sample_datarec = DataRec(RawData(data, user="user", item="item", rating="rating"))
    with pytest.raises(TypeError, match="This DataRec does not contain temporal information"):
        splitter = LeaveRatioLast(0.1, 0.1)
        splitter.run(sample_datarec)


def test_run_no_split(sample_datarec):
    splitter = LeaveRatioLast(test_ratio=0, val_ratio=0)
    result = splitter.run(sample_datarec)

    assert len(result["train"].data) == len(sample_datarec.data)
    assert "test" not in result or len(result["test"].data) == 0
    assert "val" not in result or len(result["val"].data) == 0


def test_run_test_and_validation_split(sample_datarec):
    splitter = LeaveRatioLast(test_ratio=0.3, val_ratio=0.2)
    result = splitter.run(sample_datarec)

    train = result["train"].data
    test = result["test"].data
    val = result["val"].data

    for user in sample_datarec.users:
        user_data = sample_datarec.data[sample_datarec.data['user_id'] == user]
        train_set = set(train[train['user_id'] == user]['timestamp'])
        test_set = set(test[test['user_id'] == user]['timestamp'])
        val_set = set(val[val['user_id'] == user]['timestamp'])

        assert len(train_set | test_set | val_set) == len(user_data)
        assert train_set.isdisjoint(test_set) and train_set.isdisjoint(val_set) and test_set.isdisjoint(val_set)

