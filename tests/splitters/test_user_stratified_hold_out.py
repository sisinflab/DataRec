import pytest
import pandas as pd
from math import ceil
from datarec import DataRec, RawData
from datarec.splitters.user_stratified.hold_out import UserStratifiedHoldOut


@pytest.fixture
def sample_datarec():
    data = pd.DataFrame({
        'user': [1, 1, 1, 1, 2, 2, 2, 2, 2, 3, 3, 3, 3, 3, 3],
        'item': [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15],
        'rating': [5, 4, 3, 2, 5, 4, 3, 2, 1, 5, 4, 3, 2, 1, 5]
    })
    return DataRec(RawData(data, user="user", item="item", rating="rating"))


@pytest.fixture
def too_small_dataset():
    data = pd.DataFrame({
        'user': [1, 1, 1, 2, 2, 3, 3, 3, 3],
        'item': [1, 2, 3, 4, 5, 6, 7, 8, 9],
        'rating': [5, 4, 3, 5, 4, 3, 2, 1, 5]
    })
    return DataRec(RawData(data, user="user", item="item", rating="rating"))


def test_setter_valid():
    splitter = UserStratifiedHoldOut(0.2, 0.1)
    assert splitter.test_ratio == 0.2
    assert splitter.val_ratio == 0.1


def test_setter_invalid_test():
    with pytest.raises(ValueError, match="ratio must be between 0 and 1"):
        UserStratifiedHoldOut(-0.2, 0.1)


def test_setter_invalid_val():
    with pytest.raises(ValueError, match="ratio must be between 0 and 1"):
        UserStratifiedHoldOut(0.2, -0.1)


def test_setter_invalid():
    with pytest.raises(ValueError, match="ratio must be between 0 and 1"):
        UserStratifiedHoldOut(-0.2, -0.1)


def test_run_no_split(sample_datarec):
    splitter = UserStratifiedHoldOut(test_ratio=0, val_ratio=0)
    result = splitter.run(sample_datarec)

    assert len(result["train"].data) == len(sample_datarec.data)
    assert len(result.get("test", pd.DataFrame())) == 0
    assert len(result.get("val", pd.DataFrame())) == 0


def test_empty_train_set(too_small_dataset):
    splitter = UserStratifiedHoldOut(test_ratio=0.01, val_ratio=0.01)

    with pytest.raises(ValueError):
        splitter.run(too_small_dataset)


def test_run_splitting(sample_datarec):
    splitter = UserStratifiedHoldOut(test_ratio=0.2, val_ratio=0.2, seed=42)
    result = splitter.run(sample_datarec)

    assert len(result["train"].data) + len(result["test"].data) + len(result["val"].data) == len(
        sample_datarec.data)

    for user in sample_datarec.users:
        original_count = sample_datarec.data[sample_datarec.data["user_id"] == user].shape[0]
        train_count = result["train"].data[result["train"].data["user_id"] == user].shape[0]
        test_count = result["test"].data[result["test"].data["user_id"] == user].shape[0]
        val_count = result["val"].data[result["val"].data["user_id"] == user].shape[0]

        assert test_count == ceil(original_count * 0.2)
        assert ceil((original_count - test_count) * 0.2)
        assert train_count + test_count + val_count == original_count









