from datarec.data.dataset import DataRec

from datarec.datasets.movielens20m.movielens20m_v1 import MovieLens20M_V1


class MovieLens20M:
    latest_version = 'v1'

    def __new__(cls, version: str = 'latest', **kwargs) -> DataRec:

        versions = {'v1': MovieLens20M_V1}
        if version == 'latest':
            version = cls.latest_version
        if version in versions:
            return versions[version]()
        else:
            raise ValueError("MovieLens 20M: Unsupported version")
