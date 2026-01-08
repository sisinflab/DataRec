import pytest
from tests.datasets.helpers import dataset_versions, check_dataset


@pytest.mark.slow
@pytest.mark.parametrize("version", dataset_versions("amazon_baby"))
def test_amazon_baby(version):
    check_dataset("amazon_baby", version)
