import pytest
from tests.datasets.helpers import dataset_versions, check_dataset


@pytest.mark.slow
@pytest.mark.parametrize("version", dataset_versions("ambar"))
def test_ambar(version):
    check_dataset("ambar", version)
