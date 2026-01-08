import pytest
from tests.datasets.helpers import dataset_versions, check_dataset


@pytest.mark.slow
@pytest.mark.parametrize("version", dataset_versions("epinions"))
def test_epinions(version):
    check_dataset("epinions", version)
