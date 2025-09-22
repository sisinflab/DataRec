"""Entry point for loading different versions of the Amazon Books dataset."""
from datarec.data.dataset import DataRec
from datarec.datasets.amazon_books.amz_books_2023 import AMZ_Books_2023
from datarec.datasets.amazon_books.amz_books_2018 import AMZ_Books_2018


class AmazonBooks:
    """
    Entry point class to load various versions of the Amazon Books dataset.

    This class provides a single, convenient interface for accessing the dataset.
    Based on the `version` parameter, it selects and returns the appropriate
    dataset builder for either the 2018 or 2023 version.

    The Amazon Books dataset contains product reviews and metadata from Amazon
    for the "Books" category.

    The default version is 'latest', which currently corresponds to the '2023' version.

    Examples:
        To load the latest version:
        >>> data_loader = AmazonBooks()

        To load a specific version:
        >>> data_loader = AmazonBooks(version='2018')
    """
    latest_version = '2023'

    def __new__(cls, version: str = 'latest', **kwargs) -> DataRec:
        """
        Initializes and returns the specified version of the Amazon Books dataset builder.

        This method acts as a dispatcher, instantiating the correct builder class
        that handles the downloading, caching, and loading for a specific dataset version.

        Args:
            version (str): The version of the dataset to load. Supported versions
                include '2023', '2018', and 'latest'. Defaults to 'latest'.
            **kwargs: Additional keyword arguments (not currently used for this dataset).

        Returns:
            (DataRec): An instance of the appropriate dataset builder class (e.g.,
                `AMZ_Books_2023`), populated with data.

        Raises:
            ValueError: If an unsupported version string is provided.
        """
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
