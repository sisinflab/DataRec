from datarec.data.dataset import DataRec
from datarec.datasets.amazon_sports_and_outdoors.amz_sports_v1 import AMZ_SportsOutdoors_V1


class AmazonSportsOutdoors:
    latest_version = 'v1'

    def __new__(cls, version: str = 'latest', **kwargs) -> DataRec:
        versions = {'v1': AMZ_SportsOutdoors_V1}
        if version == 'latest':
            version = cls.latest_version
        if version in versions:
            return versions[version]()
        else:
            raise ValueError("Amazon Sports and Outdoors: Unsupported version")
