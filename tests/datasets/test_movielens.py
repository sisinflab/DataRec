import pytest
from tests.datasets.helpers import dataset_versions, check_dataset


@pytest.mark.slow
@pytest.mark.parametrize("version", dataset_versions("movielens"))
def test_movielens(version):
    check_dataset("movielens", version)


