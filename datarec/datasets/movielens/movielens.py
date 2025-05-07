from datarec.data.dataset import DataRec

from datarec.datasets.movielens.movielens1m import MovieLens1M
from datarec.datasets.movielens.movielens20m import MovieLens20M


class MovieLens:
    latest_version = '1m'

    def __new__(cls, version: str = 'latest', **kwargs) -> DataRec:
        versions = {'1m': MovieLens1M,
                    '20m': MovieLens20M}
        if version == 'latest':
            version = cls.latest_version
        if version in versions:
            return versions[version]()
        else:
            raise ValueError(f"MovieLens {version}: Unsupported version \n Supported version:"
                             f"\n \t version \t name "
                             f"\n \t 1m \t Movielens 1 Million "
                             f"\n \t 20m \t Movielens 20 Million")
