from datarec.data.dataset import DataRec
from datarec.datasets.amazon_toys_and_games.amz_toys_v1 import AMZ_ToysGames_V1


class AmazonToysGames:
    latest_version = 'v1'

    def __new__(cls, version: str = 'latest', **kwargs) -> DataRec:
        versions = {'v1': AMZ_ToysGames_V1}
        if version == 'latest':
            version = cls.latest_version
        if version in versions:
            return versions[version]()
        else:
            raise ValueError("Amazon Toys and Games: Unsupported version")
