import pytest
from datarec.datasets import AmazonBeauty


def test_load_amazon_beauty_2023():
    dataset = AmazonBeauty(version='2023')
    print(dataset)