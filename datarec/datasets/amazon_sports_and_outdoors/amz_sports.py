from datarec.data.dataset import DataRec
from datarec.datasets.amazon_sports_and_outdoors.amz_sports_2023 import AMZ_SportsOutdoors_2023
from datarec.datasets.amazon_sports_and_outdoors.amz_sports_2018 import AMZ_SportsOutdoors_2018


class AmazonSportsOutdoors:
    latest_version = '2023'

    def __new__(cls, version: str = 'latest', **kwargs) -> DataRec:
        versions = {'2023': AMZ_SportsOutdoors_2023,
                    '2018': AMZ_SportsOutdoors_2018}
        if version == 'latest':
            version = cls.latest_version
        if version in versions:
            return versions[version]()
        else:
            raise ValueError(f"Amazon Sports and Outdoors {version}: Unsupported version \n Supported version:"
                             f"\n \t version \t name "
                             f"\n \t 2023 \t Amazon Sports and Outdoors 2023"
                             f"\n \t 2018 \t Amazon Sports and Outdoors 2018")
