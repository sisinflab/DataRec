"""Entry point for loading different versions of the Amazon Beauty dataset."""
from datarec.data.dataset import DataRec
from datarec.datasets.amazon_beauty.amz_beauty_2023 import AMZ_Beauty_2023


class AmazonBeauty:
    """
    Entry point class to load various versions of the Amazon Beauty dataset.

    This class provides a single, convenient interface for accessing the dataset.
    Based on the `version` parameter, it selects and returns the appropriate
    dataset builder.

    The Amazon Beauty dataset contains product reviews and metadata from Amazon,
    specialized for the "Beauty and Personal Care" category.

    The default version is 'latest', which currently corresponds to the '2023' version.

    Examples:
        To load the latest version:
        >>> data_loader = AmazonBeauty()

        To load a specific version:
        >>> data_loader = AmazonBeauty(version='2023')
    """
    latest_version = '2023'

    def __new__(cls, version: str = 'latest', **kwargs) -> DataRec:
        """
        Initializes and returns the specified version of the Amazon Beauty dataset builder.

        This method acts as a dispatcher, instantiating the correct builder class
        that handles the downloading, caching, and loading for a specific dataset version.

        Args:
            version (str): The version of the dataset to load. Currently, only
                '2023' and 'latest' are supported. Defaults to 'latest'.
            **kwargs: Additional keyword arguments (not currently used for this dataset).

        Returns:
            (AMZ_Beauty_2023): An instance of the dataset builder class, populated with data.

        Raises:
            ValueError: If an unsupported version string is provided.
        """
        versions = {'2023': AMZ_Beauty_2023}
        if version == 'latest':
            version = cls.latest_version
        if version in versions:
            return versions[version]()
        else:
            raise ValueError(f"Amazon Beauty {version}: Unsupported version \n Supported version:"
                             f"\n \t version \t name "
                             f"\n \t 2023 \t Amazon Beauty and Personal Care 2023")
