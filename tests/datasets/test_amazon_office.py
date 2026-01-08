import pytest
from tests.datasets.helpers import dataset_versions, check_dataset


@pytest.mark.slow
@pytest.mark.parametrize("version", dataset_versions("amazon_office"))
def test_amazon_office(version):
    check_dataset("amazon_office", version)
