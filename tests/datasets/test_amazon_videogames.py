import pytest
from tests.datasets.helpers import dataset_versions, check_dataset


@pytest.mark.slow
@pytest.mark.parametrize("version", dataset_versions("amazon_videogames"))
def test_amazon_videogames(version):
    check_dataset("amazon_videogames", version)
