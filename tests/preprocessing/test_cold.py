import pytest
import pandas as pd
from datarec import DataRec, RawData
from datarec.processing.cold import ColdFilter

@pytest.fixture
def sample_data():
    data = pd.DataFrame({
        'user': [1, 1, 2, 3, 3, 3, 4],
        'item': [10, 20, 30, 40, 50, 70, 70],
        'rating': [5, 4, 3, 5, 2, 1, 4],
        'timestamp': [111, 112, 113, 114, 115, 116, 117]
    })
    return DataRec(RawData(data, user='user', item='item', rating='rating', timestamp='timestamp'))


def test_cold_users(sample_data):
    filter_cold = ColdFilter(interactions=2, mode="user")
    new_datarec = filter_cold.run(sample_data)

    filtered_users = set(new_datarec.data['user_id'].unique())
    assert filtered_users == {1, 2, 4}


def test_cold_items(sample_data):
    filter_cold = ColdFilter(interactions=1, mode="item")
    new_datarec = filter_cold.run(sample_data)

    filtered_items = set(new_datarec.data['item_id'].unique())
    assert filtered_items == {10, 20, 30, 40, 50}


def test_cold_users_no_filter(sample_data):
    filter_cold = ColdFilter(interactions=4, mode="user")
    new_datarec = filter_cold.run(sample_data)

    assert new_datarec.data.equals(sample_data.data)


def test_cold_items_no_filter(sample_data):
    filter_cold = ColdFilter(interactions=2, mode="item")
    new_datarec = filter_cold.run(sample_data)

    assert new_datarec.data.equals(sample_data.data)


def test_cold_filter_type_error():
    with pytest.raises(TypeError):
        ColdFilter(interactions='not an int', mode="user")


def test_cold_filter_invalid_mode():
    with pytest.raises(ValueError):
        ColdFilter(interactions=2, mode="invalid_mode")
