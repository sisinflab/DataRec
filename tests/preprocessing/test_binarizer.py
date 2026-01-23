import pytest
import pandas as pd
from datarec import DataRec
from datarec.io import RawData
from datarec.processing.binarizer import Binarize


@pytest.fixture
def sample_data():
    data = {
        'user': [1, 2, 3, 4],
        'item': [10, 20, 30, 40],
        'rating': [2.5, 3.5, 1.5, 4.0],
        'timestamp': [100, 200, 300, 400]
    }
    return DataRec(RawData(pd.DataFrame(data), user='user', item='item', rating='rating', timestamp='timestamp'))


def test_binarize_implicit(sample_data):
    binarizer = Binarize(threshold=3.0, keep='positive', drop_rating_col=True)
    result = binarizer.run(sample_data)

    assert len(result.data) == 2
    assert 'rating' not in result.data.columns


def test_binarize_explicit(sample_data):
    binarizer = Binarize(threshold=3.0, keep='all', drop_rating_col=False, over_threshold=1, under_threshold=0)
    result = binarizer.run(sample_data)

    assert (result.data['rating'] == 1).sum() == 2
    assert (result.data['rating'] == 0).sum() == 2


def test_binarize_keep_positive_without_drop(sample_data):
    binarizer = Binarize(threshold=3.0, keep='positive', drop_rating_col=False)
    result = binarizer.run(sample_data)

    assert len(result.data) == 2
    assert (result.data['rating'] == 1).sum() == 2


def test_binarize_implicit_legacy(sample_data):
    binarizer = Binarize(threshold=3.0, implicit=True)
    result = binarizer.run(sample_data)

    assert len(result.data) == 2
    assert 'rating' not in result.data.columns


def test_binarize_missing_rating_column():
    data = {
        'user': [1, 2],
        'item': [10, 20],
        'timestamp': [100, 200]
    }
    datarec = DataRec(RawData(pd.DataFrame(data), user='user', item='item', timestamp='timestamp'))
    binarizer = Binarize(threshold=3.0)

    # Without a rating column, binarization should fail when accessing the missing field
    with pytest.raises(KeyError):
        binarizer.run(datarec)
