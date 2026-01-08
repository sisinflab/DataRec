import pytest
from tests.datasets.helpers import dataset_versions, check_dataset


@pytest.mark.slow
@pytest.mark.parametrize("version", dataset_versions("amazon_toys_and_games"))
def test_amazon_toys(version):
    check_dataset("amazon_toys_and_games", version)
