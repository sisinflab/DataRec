import pytest
from datarec.datasets import AmazonVideoGames


def test_load_amazon_videogames_2023():
    dataset = AmazonVideoGames(version='2023')
    print(dataset)