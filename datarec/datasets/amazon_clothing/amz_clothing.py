from datarec.data.dataset import DataRec
from datarec.datasets.amazon_clothing.amz_clothing_v1 import AmazonClothing_V1


class AmazonClothing:
    latest_version = 'v1'

    def __new__(cls, version: str = 'latest', **kwargs) -> DataRec:

        versions = {'v1': AmazonClothing_V1}
        if version == 'latest':
            version = cls.latest_version
        if version in versions:
            return versions[version]()
        else:
            raise ValueError("Amazon Clothing Shoes and Jewelry: Unsupported version")
