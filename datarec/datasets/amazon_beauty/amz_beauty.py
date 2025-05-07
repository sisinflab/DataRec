from datarec.data.dataset import DataRec
from datarec.datasets.amazon_beauty.amz_beauty_2023 import AMZ_Beatuy_2023


class AmazonBeauty:
    latest_version = '2023'

    def __new__(cls, version: str = 'latest', **kwargs) -> DataRec:
        versions = {'2023': AMZ_Beatuy_2023}
        if version == 'latest':
            version = cls.latest_version
        if version in versions:
            return versions[version]()
        else:
            raise ValueError(f"Amazon Beauty {version}: Unsupported version \n Supported version:"
                             f"\n \t version \t name "
                             f"\n \t 2023 \t Amazon Beauty and Personal Care 2023")
