import pytest
from datarec.datasets import MovieLens


def test_movielens1m():
    dataset = MovieLens(version='1m').prepare_and_load()

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


def test_movielens100k():
    dataset = MovieLens(version='100k').prepare_and_load()

    assert dataset.transactions == 100000
    assert dataset.space_size == 1.2594149435352908
    assert dataset.space_size_log == 0.10016884209961084
    assert dataset.shape == 0.56064209274673
    assert dataset.shape_log == -0.251314298724565
    assert dataset.density == 0.06304669364224531
    assert dataset.density_log == -1.2003376841992217
    assert dataset.gini_item == 0.628999631391201
    assert dataset.gini_user == 0.47190850477200424
    assert dataset.ratings_per_user == 106.04453870625663
    assert dataset.ratings_per_item == 59.45303210463734



