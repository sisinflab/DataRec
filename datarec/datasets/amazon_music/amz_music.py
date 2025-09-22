from datarec.data.dataset import DataRec
from datarec.datasets.amazon_music.amz_music_2023 import AMZ_Music_2023


class AmazonMusic:
    latest_version = '2023'

    def __new__(cls, version: str = 'latest', **kwargs) -> DataRec:
        versions = {'2023': AMZ_Music_2023}
        if version == 'latest':
            version = cls.latest_version
        if version in versions:
            return versions[version]()
        else:
            raise ValueError(f"Amazon Beauty {version}: Unsupported version \n Supported version:"
                             f"\n \t version \t name "
                             f"\n \t 2023 \t Amazon Baby Products 2023")
