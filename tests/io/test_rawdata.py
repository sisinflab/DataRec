from datarec.io.rawdata import RawData
from tests.utils import dummy_fixed_dataset, dummy_random_dataset


def test_empty_data():
    data = RawData()
    assert isinstance(data, RawData)
    assert data.user is None
    assert data.item is None
    assert data.rating is None
    assert data.timestamp is None
    assert data.header is False


def test_random_data():
    dummy_data = dummy_random_dataset()
    data = RawData(dummy_data)
    assert isinstance(data, RawData)


def test_raw_data_properties():
    dummy_data = dummy_fixed_dataset()
    rawdata = RawData(dummy_data['data'], user='user_id', item='item_id', rating='rating', timestamp='timestamp')
    assert list(rawdata[rawdata.user]) == list(dummy_data['user'])
    assert list(rawdata[rawdata.item]) == list(dummy_data['item'])
    assert list(rawdata[rawdata.rating]) == list(dummy_data['rating'])
    assert list(rawdata[rawdata.timestamp]) == list(dummy_data['timestamp'])
    assert len(rawdata) == dummy_data['len']


def test_raw_data_append():
    dummy_data = dummy_fixed_dataset()
    rawdata1 = RawData(dummy_data['data'], user='user_id', item='item_id', rating='rating', timestamp='timestamp')
    rawdata2 = RawData(dummy_data['data'], user='user_id', item='item_id', rating='rating', timestamp='timestamp')
    rawdata3 = rawdata1 + rawdata2
    assert len(rawdata3) == len(rawdata1) + len(rawdata2)


def test_random_raw_data_append():
    rawdata1 = RawData(dummy_random_dataset())
    rawdata2 = RawData(dummy_random_dataset())
    rawdata3 = rawdata1 + rawdata2
    assert len(rawdata3) == len(rawdata1) + len(rawdata2)
