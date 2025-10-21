import pytest
from datarec.datasets import AmazonMusic


def test_load_amazon_music_2023():
    dataset = AmazonMusic(version='2023')
    print(dataset)