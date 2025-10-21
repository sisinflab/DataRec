import pytest
from datarec.datasets import Ambar


def test_ambar():
    dataset = Ambar(version='2024').prepare_and_load()

    assert dataset.transactions == 3311462
    assert dataset.space_size == 117.33423188907831
    assert dataset.space_size_log == 2.069424734636089
    assert dataset.shape == 0.06986152941627001
    assert dataset.shape_log == -1.1557619109718333
    assert dataset.density == 0.00024053058441535148
    assert dataset.density_log == -3.618829693517537
    assert dataset.gini_item == 0.7527298907837248
    assert dataset.gini_user == 0.26300532146144723
    assert dataset.ratings_per_user == 106.77657756424725
    assert dataset.ratings_per_item == 7.4595750144732955

