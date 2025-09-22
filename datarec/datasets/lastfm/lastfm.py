"""Entry point for loading different versions of the Last.fm dataset."""
from datarec.datasets.lastfm.lastfm_2011 import LastFM2011


class LastFM:
    """
    Entry point class to load various versions of the Last.fm dataset.

    This class provides a single, convenient interface for accessing the dataset.
    Based on the `version` parameter, it selects and returns the appropriate
    dataset builder.

    This dataset contains social networking, tagging, and music artist listening
    information from the Last.fm online music system. This loader focuses on the
    user-artist listening data. It was released during the HetRec 2011 workshop.

    The default version is 'latest', which currently corresponds to '2011'.

    Examples:
        To load the latest version:
        >>> data_loader = LastFM()

        To load a specific version:
        >>> data_loader = LastFM(version='2011')
    """
    VERSIONS = {'2011': LastFM2011}
    latest_version = '2011'

    def __new__(cls, version: str = 'latest', **kwargs):
        """
        Initializes and returns the specified version of the Last.fm dataset builder.

        This method acts as a dispatcher, instantiating the correct builder class
        that handles the downloading, caching, and loading for a specific dataset version.

        Args:
            version (str): The version of the dataset to load. Currently, only
                '2011' and 'latest' are supported. Defaults to 'latest'.
            **kwargs: Additional keyword arguments (not currently used for this dataset).

        Returns:
            (LastFM2011): An instance of the dataset builder class, populated with data.

        Raises:
            ValueError: If an unsupported version string is provided.
        """

        if version == 'latest':
            version = cls.latest_version
        if version in cls.VERSIONS:
            return cls.VERSIONS[version]()
        else:
            raise ValueError(f"HetRec LastFM {version}: Unsupported version \n Supported version:"
                             f"\n \t version \t name "
                             f"\n \t 2011 \t LastFM (HetRec) 2011")
