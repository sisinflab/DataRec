"""Entry point for loading different versions of the Gowalla dataset."""
from datarec.datasets.gowalla.gowalla_friendships import GowallaFriendships
from datarec.datasets.gowalla.gowalla_checkins import GowallaCheckins


class Gowalla:
    """
    Entry point class to load various types of data from the Gowalla dataset.

    This class provides a single, convenient interface for accessing the dataset.
    Based on the `version` parameter, it selects and returns the appropriate
    dataset builder for either the user check-ins or the social friendships graph.

    Gowalla was a location-based social network. Two types of data are available:
    - 'checkins': User interactions with locations (suitable for recommendation).
    - 'friendships': The user-user social network graph.

    The default version is 'latest', which currently corresponds to 'checkins'.

    Examples:
        To load the user check-in data (default):
        >>> data_loader = Gowalla()
        # or explicitly
        >>> data_loader = Gowalla(version='checkins')

        To load the social friendship graph:
        >>> data_loader = Gowalla(version='friendships')
    """
    latest_version = 'checkins'

    def __new__(self, version: str = 'latest', **kwargs):
        """
        Initializes and returns the specified version of the Gowalla dataset builder.

        This method acts as a dispatcher, instantiating the correct builder class
        that handles the downloading, caching, and loading for a specific data type.

        Args:
            version (str): The type of data to load. Supported versions
                include 'checkins', 'friendships', and 'latest'. Defaults to 'latest'.
            **kwargs: Additional keyword arguments (not currently used).

        Returns:
            (GowallaCheckins or GowallaFriendships): An instance of the appropriate dataset
                builder class, populated with data.

        Raises:
            ValueError: If an unsupported version string is provided.
        """

        versions = {'friendships': GowallaFriendships,
                    'checkins': GowallaCheckins}
        if version == 'latest':
            version = self.latest_version
        if version in versions:
            return versions[version]()
        else:
            raise ValueError("Gowalla: Unsupported version")
