import pytest
from datarec.datasets import AmazonOffice


def test_load_amazon_beauty_2023():
    dataset = AmazonOffice(version='2023')
    print(dataset)