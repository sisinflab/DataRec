import pytest
from tests.datasets.helpers import dataset_versions, check_dataset


@pytest.mark.slow
@pytest.mark.parametrize("version", dataset_versions("citeulike"))
def test_citeulike(version):
    check_dataset("citeulike", version)
