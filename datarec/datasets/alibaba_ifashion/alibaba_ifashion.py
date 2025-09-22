"""Entry point for loading different versions of the Alibaba-iFashion dataset."""
from datarec.datasets.alibaba_ifashion.alibaba_ifashion_v1 import AlibabaIFashion_V1


class AlibabaIFashion:
    """
    Entry point class to load various versions of the Alibaba-iFashion dataset.

    This class provides a single, convenient interface for accessing the dataset.
    Based on the `version` parameter, it selects and returns the appropriate
    dataset builder.

    The default version is 'latest', which currently corresponds to 'v1'.

    Examples:
        To load the latest version:
        >>> data_loader = AlibabaIFashion()

        To load a specific version:
        >>> data_loader = AlibabaIFashion(version='v1')
    """
    latest_version = 'v1'

    def __new__(cls, version: str = 'latest', **kwargs):
        """
        Initializes and returns the specified version of the Alibaba-iFashion dataset builder.

        This method acts as a dispatcher, instantiating the correct builder class
        that handles the downloading, caching, and loading for a specific dataset version.

        Args:
            version (str): The version of the dataset to load. Currently, only
            'v1' and 'latest' are supported. Defaults to 'latest'.
            **kwargs: Additional keyword arguments.

        Returns:
            (AlibabaIFashion_V1): An instance of the dataset builder class, ready to be used.

        Raises:
            ValueError: If an unsupported version string is provided.
        """
        versions = {'v1': AlibabaIFashion_V1}
        if version == 'latest':
            version = cls.latest_version
        if version in versions:
            return versions[version]()
        else:
            raise ValueError("Alibaba iFashion: Unsupported version")
