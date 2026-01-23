import pytest
pytest.importorskip("torch", reason="Torch not installed; skipping Torch datasets tests")

import numpy as np
from datarec.datasets import Movielens
from datarec.data.torch_dataset import (
    PointwiseTorchDataset,
    PairwiseTorchDataset,
    RankingTorchDataset,
)

@pytest.fixture
def prepared_datarec():
    dr = Movielens(version="1m").prepare_and_load()
    # dr.map_users_and_items()
    # dr.to_private()
    return dr

def test_pointwise_dataset(prepared_datarec):
    dataset = PointwiseTorchDataset(prepared_datarec)
    assert len(dataset) > 0
    sample = dataset[0]
    assert set(sample.keys()) == {"user", "item", "rating"}
    assert isinstance(sample["user"], (int, np.integer))
    assert isinstance(sample["item"], (int, np.integer))
    assert isinstance(sample["rating"], (int, float, np.integer, np.floating))

def test_pairwise_dataset(prepared_datarec):
    dataset = PairwiseTorchDataset(prepared_datarec, num_negatives=2)
    assert len(dataset) > 0
    sample = dataset[0]
    assert set(sample.keys()) == {"user", "pos_items", "neg_items"}
    assert isinstance(sample["neg_items"], list)
    assert len(sample["neg_items"]) == 2
    assert all(isinstance(i, (int, float, np.integer, np.floating)) for i in sample["neg_items"])

def test_ranking_dataset(prepared_datarec):
    dataset = RankingTorchDataset(prepared_datarec)
    assert len(dataset) > 0
    sample = dataset[0]
    assert set(sample.keys()) == {"user", "item"}
    assert isinstance(sample["user"], (int, float, np.integer, np.floating))
    assert isinstance(sample["item"], (int, float, np.integer, np.floating))