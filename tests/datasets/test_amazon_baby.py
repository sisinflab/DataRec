from datarec.datasets import AmazonBaby


def test_load_amazon_baby_2023():
    dataset = AmazonBaby(version='2023').prepare_and_load()
    print(dataset)


def test_load_amazon_baby_2014():
    dataset = AmazonBaby(version='2014').prepare_and_load()
    print(dataset)
