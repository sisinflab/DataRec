import pytest
import pandas as pd
from datarec import DataRec, RawData
from datarec.splitters.uniform import RandomHoldOut, TemporalHoldOut
from datarec.splitters.user_stratified import (UserStratifiedHoldOut, LeaveRatioOut, LeaveRatioLast,
                                               LeaveOneLastItem, LeaveNLast, LeaveNOut, LeaveOneOut)


@pytest.fixture
def sample_datarec():
    data = pd.DataFrame({
        'user': [1, 1, 1, 1, 2, 2, 2, 2, 2, 3, 3, 3, 3, 3, 3],
        'item': [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15],
        'rating': [5, 4, 3, 2, 5, 4, 3, 2, 1, 5, 4, 3, 2, 1, 5],
        'timestamp': [10, 20, 30, 40, 50, 60, 70, 80, 90, 100, 110, 120, 130, 140, 150]
    })
    return DataRec(RawData(data, user='user', item='item', rating='rating', timestamp='timestamp'))


@pytest.mark.parametrize("splitter, params", [(RandomHoldOut, {"test_ratio": 0.2, "val_ratio": 0.2, "seed": 42}),
                                              (TemporalHoldOut, {"test_ratio": 0.2, "val_ratio": 0.2}),
                                              (UserStratifiedHoldOut, {"test_ratio": 0.2, "val_ratio": 0.2, "seed": 42}),
                                              (LeaveRatioOut, {"test_ratio": 0.2, "val_ratio": 0.2, "seed": 42}),
                                              (LeaveRatioLast, {"test_ratio": 0.2, "val_ratio": 0.2, "seed": 42}),
                                              (LeaveOneLastItem, {"test": True, "validation": True, "seed": 42}),
                                              (LeaveOneOut, {"test": True, "validation": True, "seed": 42}),
                                              (LeaveNLast, {"test_n": 2, "validation_n": 2, "seed": 42}),
                                              (LeaveNOut, {"test_n": 2, "validation_n": 2, "seed": 42})])
def test_reproducibility(sample_datarec, splitter, params):
    splitter1 = splitter(**params)
    splitter2 = splitter(**params)

    result1 = splitter1.run(sample_datarec)
    result2 = splitter2.run(sample_datarec)

    pd.testing.assert_frame_equal(result1["train"].data, result2["train"].data)
    pd.testing.assert_frame_equal(result1["test"].data, result2["test"].data)
    pd.testing.assert_frame_equal(result1["val"].data, result2["val"].data)
