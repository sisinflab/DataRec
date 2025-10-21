"""Entry point for loading different versions of the Ambar dataset."""
from datarec.datasets.movielens.movielens100k import BaseDataRecBuilder
from datarec.datasets.ambar.ambar_2024 import Ambar2024


class Ambar:
    """Entry point class to load various versions of the Ambar dataset.

    This class provides a single, convenient interface for accessing the dataset.
    Based on the `version` parameter, it selects and returns the appropriate
    dataset builder.

    The AMBAR dataset is a dataset in the music domain. It contains both user feedback and
    attributes, including sensitive features. The users have been anonymized.

    The 'latest' currently corresponds to the RecSys2024 version.

    Examples:
        To load the latest version (RecSys2024):
        >>> ambar = Ambar().prepare_and_load()

        To load a specific version (e.g., RecSys2024):
        >>> ambar = Ambar(version='2024').prepare_and_load()
    """
    latest_version = '2024'

    def __new__(cls, version: str = 'latest', **kwargs) -> BaseDataRecBuilder:
        """
        Initializes and returns the specified version of the Ambar dataset builder.

        This method acts as a dispatcher, instantiating the correct builder class
        that handles the downloading, caching, and loading for a specific dataset version.

        Note: The returned object is a builder. You must call `.prepare_and_load()`
        on it to get a populated `DataRec` object.

        Args:
            version (str): The version of the dataset to load. Supported versions
                include '2024', and 'latest'. Defaults to 'latest'.
            **kwargs: Additional keyword arguments (not currently used).

        Returns:
            (BaseDataRecBuilder): An instance of the appropriate dataset builder class
                (e.g., `Ambar2024`), ready to prepare and load data.

        Raises:
            ValueError: If an unsupported version string is provided.
        """
        versions = {'2024': Ambar2024}
        if version == 'latest':
            version = cls.latest_version
        if version in versions:
            return versions[version]()
        else:
            raise ValueError(f"Ambar {version}: Unsupported version \n Supported version:"
                             f"\n \t version \t name "
                             f"\n \t 2024 \t Ambar RecSys2024 \n")
