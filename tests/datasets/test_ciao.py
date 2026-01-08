import pytest
from tests.datasets.helpers import dataset_versions, check_dataset


@pytest.mark.slow
@pytest.mark.parametrize("version", dataset_versions("ciao"))
def test_ciao(version):
    check_dataset("ciao", version)
