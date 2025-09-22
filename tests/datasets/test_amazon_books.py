import pytest
from datarec.datasets import AmazonBooks


def test_load_amazon_books_2023():
    dataset = AmazonBooks(version='2023')
    print(dataset)