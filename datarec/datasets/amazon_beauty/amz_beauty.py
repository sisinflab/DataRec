from datarec.data.dataset import DataRec
from datarec.datasets.amazon_beauty.amz_beauty_v1 import AMZ_Beatuy_V1


class AmazonBeauty:
    latest_version = 'v1'

    def __new__(cls, version: str = 'latest', **kwargs) -> DataRec:
        versions = {'v1': AMZ_Beatuy_V1}
        if version == 'latest':
            version = cls.latest_version
        if version in versions:
            return versions[version]()
        else:
            raise ValueError("Amazon Beauty: Unsupported version")
