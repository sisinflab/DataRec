from datarec.datasets.movielens.movielens100k import BaseDataRecBuilder
from datarec.datasets.amazon_baby.amz_baby_2014 import AMZ_Baby_2014
from datarec.datasets.amazon_baby.amz_baby_2023 import AMZ_Baby_2023


class AmazonBaby:
    latest_version = '2023'

    def __new__(cls, version: str = 'latest', **kwargs) -> BaseDataRecBuilder:
        versions = {'2014': AMZ_Baby_2014,
                    '2023': AMZ_Baby_2023}
        if version == 'latest':
            version = cls.latest_version
        if version in versions:
            return versions[version]()
        else:
            raise ValueError(f"Amazon Beauty {version}: Unsupported version \n Supported version:"
                             f"\n \t version \t name "
                             f"\n \t 2014 \t Amazon Baby Products 2014"
                             f"\n \t 2023 \t Amazon Baby Products 2023")
