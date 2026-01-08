import pytest
from tests.datasets.helpers import dataset_versions, check_dataset


@pytest.mark.slow
@pytest.mark.parametrize("version", dataset_versions("alibaba_ifashion"))
def test_alibaba_ifashion(version):
    check_dataset("alibaba_ifashion", version)
