import math

import pytest
import pandas as pd

from datarec.data.dataset import DataRec, DATAREC_USER_COL, DATAREC_ITEM_COL, DATAREC_RATING_COL
from datarec.io.rawdata import RawData


@pytest.fixture
def toy_datarec():
    df = pd.DataFrame(
        {
            DATAREC_USER_COL: [1, 1, 2, 3],
            DATAREC_ITEM_COL: [10, 11, 10, 12],
            DATAREC_RATING_COL: [5, 4, 3, 2],
        }
    )
    rd = RawData(df, user=DATAREC_USER_COL, item=DATAREC_ITEM_COL, rating=DATAREC_RATING_COL)
    return DataRec(rd)


def test_basic_characteristics(toy_datarec: DataRec):
    dr = toy_datarec
    # Transactions
    assert dr.transactions == 4
    # Users/Items counts
    assert dr.n_users == 3
    assert dr.n_items == 3
    # Density = transactions / (users * items)
    assert dr.density() == pytest.approx(4 / (3 * 3))
    assert dr.density_log() == pytest.approx(math.log10(dr.density()))
    # Shape = users/items
    assert dr.shape() == pytest.approx(3 / 3)
    assert dr.shape_log() == pytest.approx(math.log10(dr.shape()))
    # Ratings per user/item
    assert dr.ratings_per_user() == pytest.approx(4 / 3)
    assert dr.ratings_per_item() == pytest.approx(4 / 3)


def test_gini_characteristics(toy_datarec: DataRec):
    dr = toy_datarec
    g_user = dr.gini_user()
    g_item = dr.gini_item()
    assert 0 <= g_user <= 1
    assert 0 <= g_item <= 1


def test_characteristic_accessor(toy_datarec: DataRec):
    dr = toy_datarec
    # All registered characteristics should be accessible via .characteristics
    for name in dr.list_characteristics():
        value = getattr(dr.characteristics, name)()
        assert value is not None
