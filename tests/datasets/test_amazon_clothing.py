import pytest
from datarec.datasets import AmazonClothing


def test_load_amazon_clothing_2023():
    dataset = AmazonClothing(version='2023')
    print(dataset)