import pytest
import pandas as pd
from datarec import DataRec, RawData
from datarec.processing.kcore import (KCore, UserKCore, ItemKCore, IterativeKCore, UserItemIterativeKCore, NRoundsKCore,
                                      UserItemNRoundsKCore)


@pytest.fixture
def sample_datarec():
    data = pd.DataFrame({
        'user': ['A', 'A', 'B', 'B', 'C', 'C', 'C'],
        'item': ['X', 'Y', 'Z', 'X', 'Y', 'Z', 'X'],
        'rating': [1, 2, 3, 4, 5, 6, 7],
        'timestamp': [1, 2, 3, 4, 5, 6, 7]
    })
    return DataRec(RawData(data, user='user', item='item', rating='rating', timestamp='timestamp'))


# Test KCore
def test_kcore_initialization():
    kcore = KCore(column='user', core=2)
    assert kcore._column == 'user'
    assert kcore._core == 2


def test_kcore_invalid_column():
    with pytest.raises(ValueError):
        kcore = KCore(column='invalid', core=2)
        kcore.run(pd.DataFrame({'user': [1, 2], 'item': ['A', 'B']}))


def test_kcore_invalid_core_type():
    with pytest.raises(TypeError):
        KCore(column='user', core='invalid')


def test_kcore_run(sample_datarec):
    kcore = KCore(column='user_id', core=3)
    result = kcore.run(sample_datarec.data)
    assert len(result) == 3


# Test UserKCore
def test_userkcore_initialization():
    userkcore = UserKCore(core=2)
    assert userkcore.core == 2


def test_userkcore_run(sample_datarec):
    userkcore = UserKCore(core=3)
    result_datarec = userkcore.run(sample_datarec)
    assert len(result_datarec.data) == 3


# Test ItemKCore
def test_itemkcore_initialization():
    itemkcore = ItemKCore(core=2)
    assert itemkcore.core == 2


def test_itemkcore_run(sample_datarec):
    itemkcore = ItemKCore(core=3)
    result_datarec = itemkcore.run(sample_datarec)
    assert len(result_datarec.data) == 3

@pytest.fixture
def sample_iterative_datarec():
    data = pd.DataFrame({
        'user': ['A', 'A', 'B', 'B', 'C', 'C', 'C', 'D'],
        'item': ['X', 'Y', 'Z', 'X', 'Y', 'Z', 'X', 'W'],
        'rating': [1, 2, 3, 4, 5, 6, 7, 8],
        'timestamp': [1, 2, 3, 4, 5, 6, 7, 8]
    })
    return DataRec(RawData(data, user='user', item='item', rating='rating', timestamp='timestamp'))


# Test IterativeKCore
def test_iterativekcore_initialization():
    iterativekcore = IterativeKCore(columns=['user_id', 'item_id'], cores=[2, 2])
    assert iterativekcore._columns == ['user_id', 'item_id']
    assert iterativekcore._cores == [('user_id', 2), ('item_id', 2)]


def test_iterativekcore_run(sample_iterative_datarec):
    iterativekcore = IterativeKCore(columns=['user_id', 'item_id'], cores=[2, 2])
    result = iterativekcore.run(sample_iterative_datarec.data)
    assert len(result) == 7


# Test UserItemIterativeKCore
def test_useritemiterativekcore_initialization():
    useritemiterativekcore = UserItemIterativeKCore(cores=2)
    assert useritemiterativekcore._cores == 2


def test_useritemiterativekcore_run(sample_iterative_datarec):
    useritemiterativekcore = UserItemIterativeKCore(cores=2)
    result_datarec = useritemiterativekcore.run(sample_iterative_datarec)
    assert len(result_datarec.data) == 7


# Test NRoundsKCore
def test_nroundskcore_initialization():
    nroundskcore = NRoundsKCore(columns=['user_id', 'item_id'], cores=[2, 2], rounds=2)
    assert nroundskcore._columns == ['user_id', 'item_id']
    assert nroundskcore._cores == [('user_id', 2), ('item_id', 2)]
    assert nroundskcore._rounds == 2


def test_nroundskcore_run(sample_iterative_datarec):
    nroundskcore = NRoundsKCore(columns=['user_id', 'item_id'], cores=[2, 2], rounds=2)
    result = nroundskcore.run(sample_iterative_datarec.data)
    assert len(result) == 7


# Test UserItemNRoundsKCore
def test_useritemnroundskcore_initialization():
    useritemnroundskcore = UserItemNRoundsKCore(cores=2, rounds=2)
    assert useritemnroundskcore._cores == 2
    assert useritemnroundskcore._rounds == 2


def test_useritemnroundskcore_run(sample_iterative_datarec):
    useritemnroundskcore = UserItemNRoundsKCore(cores=2, rounds=2)
    result_datarec = useritemnroundskcore.run(sample_iterative_datarec)
    assert len(result_datarec.data) == 7
