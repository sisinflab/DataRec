from datarec.data.dataset import DataRec
from datarec.datasets.epinions.epinions_v1 import Epinions_V1


class Epinions:
    latest_version = 'v1'
    def __new__(cls, version: str = 'latest', **kwargs) -> DataRec:

        versions = {'v1': Epinions_V1}
        if version == 'latest':
            version = cls.latest_version
        if version in versions:
            return versions[version]()
        else:
            raise ValueError("Epinions: Unsupported version")
