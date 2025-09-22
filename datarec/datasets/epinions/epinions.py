"""Entry point for loading different versions of the Epinions dataset."""
from datarec.data.dataset import DataRec
from datarec.datasets.epinions.epinions_v1 import Epinions_V1


class Epinions:
    """
    Entry point class to load various versions of the Epinions dataset.

    This class provides a single, convenient interface for accessing the dataset.
    Based on the `version` parameter, it selects and returns the appropriate
    dataset builder.

    Epinions is a who-trust-whom online social network from a general consumer
    review site. Members of the site can decide whether to "trust" each other.

    The default version is 'latest', which currently corresponds to 'v1'.

    Examples:
        To load the latest version:
        >>> data_loader = Epinions()

        To load a specific version:
        >>> data_loader = Epinions(version='v1')
    """
    latest_version = 'v1'
    def __new__(cls, version: str = 'latest', **kwargs) -> DataRec:
        """
        Initializes and returns the specified version of the Epinions dataset builder.

        This method acts as a dispatcher, instantiating the correct builder class
        that handles the downloading, caching, and loading for a specific dataset version.

        Args:
            version (str): The version of the dataset to load. Currently, only
                'v1' and 'latest' are supported. Defaults to 'latest'.
            **kwargs: Additional keyword arguments (not currently used for this dataset).

        Returns:
            (Epinions_V1): An instance of the dataset builder class, populated with data.

        Raises:
            ValueError: If an unsupported version string is provided.
        """

        versions = {'v1': Epinions_V1}
        if version == 'latest':
            version = cls.latest_version
        if version in versions:
            return versions[version]()
        else:
            raise ValueError("Epinions: Unsupported version")
