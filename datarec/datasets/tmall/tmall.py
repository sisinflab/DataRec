"""Entry point for loading different versions of the Tmall dataset."""
from datarec.datasets.tmall.tmall_v1 import Tmall_v1


class Tmall:
    """
    Entry point class to load various versions of the Tmall dataset.

    This class provides a single, convenient interface for accessing the dataset.
    Based on the `version` parameter, it selects and returns the appropriate
    dataset builder.

    This dataset was released for the IJCAI-16 Contest and contains user
    interactions from the Tmall.com platform for a nearby store recommendation task.

    **Note:** This dataset requires manual download from the official source.

    The default version is 'latest', which currently corresponds to 'v1'.

    Examples:
        To load the latest version:
        >>> data_loader = Tmall()
    """
    latest_version = 'v1'

    def __new__(self, version: str = 'latest', **kwargs):
        """
        Initializes and returns the specified version of the Tmall dataset builder.

        This method acts as a dispatcher, instantiating the correct builder class
        that handles the preparation and loading for a specific dataset version.

        Args:
            version (str): The version of the dataset to load. Currently, only
                'v1' and 'latest' are supported. Defaults to 'latest'.
            **kwargs: Additional keyword arguments (not currently used for this dataset).

        Returns:
            (Tmall_v1): An instance of the dataset builder class, populated with data.

        Raises:
            ValueError: If an unsupported version string is provided.
        """

        versions = {'v1': Tmall_v1}
        if version == 'latest':
            version = self.latest_version
        if version in versions:
            return versions[version]()
        else:
            raise ValueError("Tmall dataset: Unsupported version")
