import pytest
from tests.datasets.helpers import dataset_versions, check_dataset


@pytest.mark.slow
@pytest.mark.parametrize("version", dataset_versions("amazon_beauty"))
def test_amazon_beauty(version):
    check_dataset("amazon_beauty", version)
