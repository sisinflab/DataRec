"""Entry point for loading different versions of the Yelp dataset."""
from datarec.datasets.yelp.yelp_v1 import Yelp_v1


class Yelp:
    """
    Entry point class to load various versions of the Yelp Dataset.

    This class provides a single, convenient interface for accessing the dataset.
    Based on the `version` parameter, it selects and returns the appropriate
    dataset builder.

    The default version is 'latest', which currently corresponds to 'v1'.

    Examples:
        To load the latest version:
        >>> data_loader = Yelp()

        To load a specific version:
        >>> data_loader = Yelp(version='v1')
    """
    latest_version = 'v1'

    def __new__(self, version: str = 'latest', **kwargs):
        """
        Initializes and returns the specified version of the Yelp dataset builder.

        This method acts as a dispatcher, instantiating the correct builder class
        that handles the downloading, caching, and loading for a specific dataset version.

        Args:
            version (str): The version of the dataset to load. Currently, only
                'v1' and 'latest' are supported. Defaults to 'latest'.
            **kwargs: Additional keyword arguments (not currently used for this dataset).

        Returns:
            (Yelp_v1): An instance of the dataset builder class, populated with data.

        Raises:
            ValueError: If an unsupported version string is provided.
        """

        versions = {'v1': Yelp_v1}
        if version == 'latest':
            version = self.latest_version
        if version in versions:
            return versions[version]()
        else:
            raise ValueError("Yelp dataset: Unsupported version")
