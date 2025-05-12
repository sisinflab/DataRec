import pytest
from datarec.datasets import MovieLens1M


def test_movielens1M_v1():
    dataset = MovieLens1M()

    assert dataset.transactions == 1000209
    assert dataset.space_size == 4.731198579641315
    assert dataset.space_size_log == 0.6749711768020052
    assert dataset.shape == 1.6297895304910954
    assert dataset.shape_log == 0.21213152363825305
    assert dataset.density == 0.044683625622312845
    assert dataset.density_log == -1.34985159554118
    assert dataset.gini_item == 0.6335616301416965
    assert dataset.gini_user == 0.5286242435264804
    assert dataset.ratings_per_user == 165.5975165562914
    assert dataset.ratings_per_item == 269.88909875876953
