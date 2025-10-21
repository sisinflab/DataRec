import pytest
import pandas as pd
from datarec import DataRec, RawData
from datarec.splitters.user_stratified import LeaveRatioOut

@pytest.fixture
def sample_datarec():
    data = pd.DataFrame({
        'user': [1, 1, 1, 2, 2, 2, 3, 3, 3],
        'item': [10, 20, 30, 40, 50, 60, 70, 80, 90],
        'rating': [5, 4, 3, 5, 3, 4, 2, 5, 1]
    })
    return DataRec(RawData(data, user="user", item="item", rating="rating"))


def test_setter_valid():
    splitter = LeaveRatioOut(test_ratio=0.2, val_ratio=0.1)
    assert splitter.test_ratio == 0.2
    assert splitter.val_ratio == 0.1


def test_setter_invalid():
    with pytest.raises(ValueError, match="ratio must be between 0 and 1"):
        LeaveRatioOut(test_ratio=-0.2, val_ratio=0.1)

    with pytest.raises(ValueError, match="ratio must be between 0 and 1"):
        LeaveRatioOut(test_ratio=0.2, val_ratio=-0.1)

    with pytest.raises(ValueError, match="ratio must be between 0 and 1"):
        LeaveRatioOut(test_ratio=-0.2, val_ratio=-0.1)

    with pytest.raises(ValueError, match="ratio must be between 0 and 1"):
        LeaveRatioOut(test_ratio=-0.2, val_ratio=-0.1)

    with pytest.raises(ValueError, match="ratio must be between 0 and 1"):
        LeaveRatioOut(test_ratio=2, val_ratio=0.1)

    with pytest.raises(ValueError, match="sum of test_ratio and val_ratio must not exceed 1"):
        LeaveRatioOut(0.7, 0.5)

    with pytest.raises(ValueError):
        LeaveRatioOut(test_ratio=0.7, val_ratio=0.5)


def test_run_no_split(sample_datarec):
    splitter = LeaveRatioOut(test_ratio=0, val_ratio=0)
    result = splitter.run(sample_datarec)

    assert len(result["train"].data) == len(sample_datarec.data)
    assert "test" not in result or len(result["test"].data) == 0
    assert "val" not in result or len(result["val"].data) == 0


def test_user_stratification(sample_datarec):
    splitter = LeaveRatioOut(test_ratio=0.2, val_ratio=0.2)
    result = splitter.run(sample_datarec)

    train, test, val = result["train"].data, result["test"].data, result["val"].data

    for user in sample_datarec.users:
        total = len(sample_datarec.data[sample_datarec.data['user_id'] == user])
        train_count = len(train[train['user_id'] == user])
        test_count = len(test[test['user_id'] == user])
        val_count = len(val[val['user_id'] == user])

        assert train_count + test_count + val_count == total
        assert test_count == round(0.3 * total)
        assert val_count == round(0.2 * total)

