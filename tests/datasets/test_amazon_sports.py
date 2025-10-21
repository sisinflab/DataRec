import pytest
from datarec.datasets import AmazonSportsOutdoors


def test_load_amazon_sports_2023():
    dataset = AmazonSportsOutdoors(version='2023')
    print(dataset)