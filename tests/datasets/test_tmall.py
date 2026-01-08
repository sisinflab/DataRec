import pytest
from tests.datasets.helpers import dataset_versions, check_dataset


@pytest.mark.slow
@pytest.mark.parametrize("version", dataset_versions("tmall"))
def test_tmall(version):
    check_dataset("tmall", version)
