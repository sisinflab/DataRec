import pytest
from tests.datasets.helpers import dataset_versions, check_dataset


@pytest.mark.slow
@pytest.mark.parametrize("version", dataset_versions("lastfm"))
def test_lastfm(version):
    check_dataset("lastfm", version)
