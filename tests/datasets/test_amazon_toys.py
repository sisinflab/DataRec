import pytest
from datarec.datasets import AmazonToysGames


def test_load_amazon_toys_2023():
    dataset = AmazonToysGames(version='2023')
    print(dataset)