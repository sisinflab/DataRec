import pytest
from tests.datasets.helpers import dataset_versions, check_dataset


@pytest.mark.slow
@pytest.mark.parametrize("version", dataset_versions("amazon_music"))
def test_amazon_music(version):
    check_dataset("amazon_music", version)
