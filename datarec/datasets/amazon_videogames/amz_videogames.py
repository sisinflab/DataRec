from datarec.data.dataset import DataRec
from datarec.datasets.amazon_videogames.amz_videogames_2023 import AMZ_VideoGames_2023
from datarec.datasets.amazon_videogames.amz_videogames_2018 import AMZ_VideoGames_2018


class AmazonVideoGames:
    latest_version = '2023'

    def __new__(cls, version: str = 'latest', **kwargs) -> DataRec:

        versions = {'2023': AMZ_VideoGames_2023,
                    '2018': AMZ_VideoGames_2018}
        if version == 'latest':
            version = cls.latest_version
        if version in versions:
            return versions[version]()
        else:
            raise ValueError(f"Amazon Video Games {version}: Unsupported version \n Supported version:"
                             f"\n \t version \t name "
                             f"\n \t 2023 \t Amazon Video Games 2023"
                             f"\n \t 2018 \t Amazon Video Games 2018")
