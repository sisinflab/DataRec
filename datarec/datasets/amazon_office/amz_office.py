from datarec.data.datarec_builder import BaseDataRecBuilder
from datarec.datasets.amazon_office.amz_office_2023 import AMZ_Office_2023
from datarec.datasets.amazon_office.amz_office_2014 import AMZ_Office_2014


class AmazonOffice:
    latest_version = '2023'

    def __new__(cls, version: str = 'latest', **kwargs) -> BaseDataRecBuilder:
        versions = {'2014': AMZ_Office_2014,
                    '2023': AMZ_Office_2023}
        if version == 'latest':
            version = cls.latest_version
        if version in versions:
            return versions[version]()
        else:
            raise ValueError(f"Amazon Beauty {version}: Unsupported version \n Supported version:"
                             f"\n \t version \t name "
                             f"\n \t 2014 \t Amazon Office Products 2014"
                             f"\n \t 2023 \t Amazon Office Products 2023")
