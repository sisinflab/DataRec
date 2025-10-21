import pytest
import pandas as pd
from datarec import DataRec, RawData
from datarec.splitters.user_stratified import LeaveOneLastItem


@pytest.fixture
def sample_datarec():
    data = pd.DataFrame({
        'user': [1, 1, 1, 2, 2, 2, 3, 3, 3],
        'item': [10, 20, 30, 40, 50, 60, 70, 80, 90],
        'rating': [5, 4, 3, 5, 3, 4, 2, 5, 1],
        "timestamp": [100, 200, 300, 110, 210, 310, 410, 510, 610]
    })
    return DataRec(RawData(data, user="user", item="item", rating="rating", timestamp="timestamp"))


def test_leave_one_last_item_initialization():
    with pytest.raises(TypeError):
        LeaveOneLastItem(test="True")
    with pytest.raises(TypeError):
        LeaveOneLastItem(validation=1)


def test_leave_one_last_item_splitting(sample_datarec):
    splitter = LeaveOneLastItem(test=True, validation=True)
    result = splitter.run(sample_datarec)

    test = result["test"].data
    val = result["val"].data

    assert "train" in result and "test" in result and "val" in result
    assert result["test"].data["timestamp"].max() == 610
    assert result["val"].data["timestamp"].max() == 510

    for user in sample_datarec.users:
        assert len(val[val['user_id'] == user]) == 1
        assert len(test[test['user_id'] == user]) == 1
