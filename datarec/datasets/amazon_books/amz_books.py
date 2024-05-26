from datarec.data.dataset import DataRec
from datarec.datasets.amazon_books.amz_books_v1 import AMZ_Books_V1


class AmazonBooks:
    latest_version = 'v1'

    def __new__(cls, version: str = 'latest', **kwargs) -> DataRec:
        versions = {'v1': AMZ_Books_V1}
        if version == 'latest':
            version = cls.latest_version
        if version in versions:
            return versions[version]()
        else:
            raise ValueError("Amazon Book: Unsupported version")
