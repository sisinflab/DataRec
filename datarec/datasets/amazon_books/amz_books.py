from datarec.data.dataset import DataRec
from datarec.datasets.amazon_books.amz_books_2023 import AMZ_Books_2023
from datarec.datasets.amazon_books.amz_books_2018 import AMZ_Books_2018


class AmazonBooks:
    latest_version = '2023'

    def __new__(cls, version: str = 'latest', **kwargs) -> DataRec:
        versions = {'2023': AMZ_Books_2023,
                    '2018': AMZ_Books_2018}
        if version == 'latest':
            version = cls.latest_version
        if version in versions:
            return versions[version]()
        else:
            raise ValueError(f"Amazon Books {version}: Unsupported version \n Supported version:"
                             f"\n \t version \t name "
                             f"\n \t 2023 \t Amazon Books 2023"
                             f"\n \t 2018 \t Amazon Books 2018")
