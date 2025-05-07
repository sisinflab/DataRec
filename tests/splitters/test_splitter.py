import pytest
import pandas as pd
import numpy as np
from datarec import DataRec, RawData
from datarec.splitters.splitter import Splitter


@pytest.fixture
def sample_datarec():
    data = pd.DataFrame({
        "user": np.arange(10),
        "item": np.arange(10),
        "rating": np.ones(10),
        "timestamp": np.arange(10)
    })
    return DataRec(RawData(data, user="user", item="item", rating="rating", timestamp="timestamp"))


def test_output_all_splits(sample_datarec):
    train = sample_datarec.data.iloc[:6]
    test = sample_datarec.data.iloc[6:8]
    val = sample_datarec.data.iloc[8:]

    result = Splitter.output(sample_datarec, train, test, val)

    assert set(result.keys()) == {"train", "test", "val"}
    assert isinstance(result["train"], DataRec)
    assert isinstance(result["test"], DataRec)
    assert isinstance(result["val"], DataRec)


def test_output_some_empty(sample_datarec):
    train = sample_datarec.data.iloc[:8]
    test = pd.DataFrame()
    val = sample_datarec.data.iloc[8:]

    result = Splitter.output(sample_datarec, train, test, val)

    assert set(result.keys()) == {"train", "val"}


def test_output_all_empty(sample_datarec):
    empty = pd.DataFrame()

    result = Splitter.output(sample_datarec, empty, empty, empty)

    assert result == {}
