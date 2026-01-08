import pytest
from tests.datasets.helpers import dataset_versions, check_dataset


@pytest.mark.slow
@pytest.mark.parametrize("version", dataset_versions("amazon_books"))
def test_amazon_books(version):
    check_dataset("amazon_books", version)
