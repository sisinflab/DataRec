from datarec.data.dataset import DataRec
from datarec.datasets.amazon_clothing.amz_clothing_2023 import AmazonClothing_2023
from datarec.datasets.amazon_clothing.amz_clothing_2018 import AmazonClothing_2018


class AmazonClothing:
    latest_version = '2023'

    def __new__(cls, version: str = 'latest', **kwargs) -> DataRec:

        versions = {'2023': AmazonClothing_2023,
                    '2018': AmazonClothing_2018}
        if version == 'latest':
            version = cls.latest_version
        if version in versions:
            return versions[version]()
        else:
            raise ValueError(f"Amazon Clothing {version}: Unsupported version \n Supported version:"
                             f"\n \t version \t name "
                             f"\n \t 2023 \t Amazon Clothing 2023"
                             f"\n \t 2018 \t Amazon Clothing 2018")
