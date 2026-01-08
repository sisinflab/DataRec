import pytest
from tests.datasets.helpers import dataset_versions, check_dataset


@pytest.mark.slow
@pytest.mark.parametrize("version", dataset_versions("yelp"))
def test_yelp(version):
    check_dataset("yelp", version)
