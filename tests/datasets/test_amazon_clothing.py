import pytest
from tests.datasets.helpers import dataset_versions, check_dataset


@pytest.mark.slow
@pytest.mark.parametrize("version", dataset_versions("amazon_clothing"))
def test_amazon_clothing(version):
    check_dataset("amazon_clothing", version)
