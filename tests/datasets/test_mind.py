import pytest
from tests.datasets.helpers import dataset_versions, check_dataset


@pytest.mark.slow
@pytest.mark.parametrize("version", dataset_versions("mind"))
def test_mind(version):
    check_dataset("mind", version)
