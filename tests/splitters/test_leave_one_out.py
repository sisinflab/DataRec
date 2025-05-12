import pytest
import pandas as pd
from datarec import DataRec, RawData
from datarec.splitters.user_stratified import LeaveOneOut


@pytest.fixture
def sample_datarec():
    data = pd.DataFrame({
        'user': [1, 1, 1, 2, 2, 2, 3, 3, 3],
        'item': [10, 20, 30, 40, 50, 60, 70, 80, 90],
        'rating': [5, 4, 3, 5, 3, 4, 2, 5, 1]
    })
    return DataRec(RawData(data, user="user", item="item", rating="rating"))


def test_leave_one_out_split(sample_datarec):
    splitter = LeaveOneOut(test=True, validation=True, seed=42)
    result = splitter.run(sample_datarec)

    assert "train" in result
    assert "test" in result
    assert "val" in result

    assert isinstance(result["train"], DataRec)
    assert isinstance(result["test"], DataRec)
    assert isinstance(result["val"], DataRec)

    train_users = set(result["train"].data["user_id"])
    test_users = set(result["test"].data["user_id"])
    val_users = set(result["val"].data["user_id"])

    assert train_users == test_users == val_users

    for user in sample_datarec.users:
        total = (sample_datarec.data["user_id"] == user).sum()
        train_count = (result["train"].data["user_id"] == user).sum()
        test_count = (result["test"].data["user_id"] == user).sum()
        val_count = (result["val"].data["user_id"] == user).sum()
        assert test_count == 1
        assert val_count == 1
        assert train_count == total - 2


def test_leave_one_out_invalid():
    with pytest.raises(TypeError):
        LeaveOneOut(test=1, validation=True)

    with pytest.raises(TypeError):
        LeaveOneOut(test=True, validation=1)

    with pytest.raises(TypeError):
        LeaveOneOut(test=0.2, validation=True)

    with pytest.raises(TypeError):
        LeaveOneOut(test=True, validation=0.2)


def test_leave_one_out_empty_split(sample_datarec):
    splitter = LeaveOneOut(test=False, validation=False, seed=42)
    result = splitter.run(sample_datarec)

    assert len(result["train"].data) == len(sample_datarec.data)



