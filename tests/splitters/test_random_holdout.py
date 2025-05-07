import pytest
import pandas as pd
import numpy as np
from datarec import DataRec, RawData
from datarec.splitters.uniform import RandomHoldOut


@pytest.fixture
def sample_datarec():
    data = pd.DataFrame({
        "user": np.arange(100),
        "item": np.arange(100),
        "rating": np.ones(100),
        "timestamp": np.arange(100)
    })
    return DataRec(RawData(data, user="user", item="item", rating="rating", timestamp="timestamp"))


def test_setter_valid():
    splitter = RandomHoldOut(0.2, 0.1)
    assert splitter.test_ratio == 0.2
    assert splitter.val_ratio == 0.1


def test_setter_invalid_test():
    with pytest.raises(ValueError, match="ratio must be between 0 and 1"):
        RandomHoldOut(-0.2, 0.1)


def test_setter_invalid_val():
    with pytest.raises(ValueError, match="ratio must be between 0 and 1"):
        RandomHoldOut(0.2, -0.1)


def test_setter_invalid():
    with pytest.raises(ValueError, match="ratio must be between 0 and 1"):
        RandomHoldOut(-0.2, -0.1)


def test_run_no_split(sample_datarec):
    splitter = RandomHoldOut(test_ratio=0, val_ratio=0)
    result = splitter.run(sample_datarec)

    assert len(result["train"].data) == 100
    assert "test" not in result
    assert "val" not in result


def test_run_only_test_split(sample_datarec):
    splitter = RandomHoldOut(test_ratio=0.2, val_ratio=0)
    result = splitter.run(sample_datarec)

    assert len(result["train"].data) == 80
    assert len(result["test"].data) == 20
    assert "val" not in result


def test_run_test_and_validation_split(sample_datarec):
    splitter = RandomHoldOut(test_ratio=0.2, val_ratio=0.1)
    result = splitter.run(sample_datarec)

    assert len(result["train"].data) == 72
    assert len(result["test"].data) == 20
    assert len(result["val"].data) == 8
