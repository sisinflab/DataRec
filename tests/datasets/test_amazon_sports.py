import pytest
from tests.datasets.helpers import dataset_versions, check_dataset


@pytest.mark.slow
@pytest.mark.parametrize("version", dataset_versions("amazon_sports_and_outdoors"))
def test_amazon_sports(version):
    check_dataset("amazon_sports_and_outdoors", version)
