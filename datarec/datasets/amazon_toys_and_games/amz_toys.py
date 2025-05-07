from datarec.data.dataset import DataRec
from datarec.datasets.amazon_toys_and_games.amz_toys_2023 import AMZ_ToysGames_2023
from datarec.datasets.amazon_toys_and_games.amz_toys_2018 import AMZ_ToysGames_2018


class AmazonToysGames:
    latest_version = '2023'

    def __new__(cls, version: str = 'latest', **kwargs) -> DataRec:
        versions = {'2023': AMZ_ToysGames_2023,
                    '2018': AMZ_ToysGames_2018}
        if version == 'latest':
            version = cls.latest_version
        if version in versions:
            return versions[version]()
        else:
            raise ValueError(f"Amazon Toys and Games {version}: Unsupported version \n Supported version:"
                             f"\n \t version \t name "
                             f"\n \t 2023 \t Amazon Toys and Games 2023"
                             f"\n \t 2018 \t Amazon Toys and Games 2018")
