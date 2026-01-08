import pytest
from tests.datasets.helpers import dataset_versions, check_dataset


@pytest.mark.slow
@pytest.mark.parametrize("version", dataset_versions("gowalla"))
def test_gowalla(version):
    check_dataset("gowalla", version)
