"""Entry point for loading different versions of the CiaoDVD dataset."""
from datarec.datasets.ciao.ciao_v1 import Ciao_V1


class Ciao:
    """
    Entry point class to load various versions of the CiaoDVD dataset.

    This class provides a single, convenient interface for accessing the dataset.
    Based on the `version` parameter, it selects and returns the appropriate
    dataset builder.

    CiaoDVD is a dataset for DVD recommendations, also containing social trust data.
    This loader focuses on the movie ratings.

    The default version is 'latest', which currently corresponds to 'v1'.

    Examples:
        To load the latest version:
        >>> data_loader = Ciao()

        To load a specific version:
        >>> data_loader = Ciao(version='v1')
    """
    latest_version = 'v1'
    def __new__(self, version: str = 'latest', **kwargs):
        """
        Initializes and returns the specified version of the CiaoDVD dataset builder.

        This method acts as a dispatcher, instantiating the correct builder class
        that handles the downloading, caching, and loading for a specific dataset version.

        Args:
            version (str): The version of the dataset to load. Currently, only
                'v1' and 'latest' are supported. Defaults to 'latest'.
            **kwargs: Additional keyword arguments (not currently used for this dataset).

        Returns:
            (Ciao_V1): An instance of the dataset builder class, populated with data.

        Raises:
            ValueError: If an unsupported version string is provided.
        """

        versions = {'v1': Ciao_V1}
        if version == 'latest':
            version = self.latest_version
        if version in versions:
            return versions[version]()
        else:
            raise ValueError("Ciao: Unsupported version")
