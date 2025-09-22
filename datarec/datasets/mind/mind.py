"""Entry point for loading different versions of the MIND dataset."""
from datarec.datasets.mind.mindLarge import MindLarge
from datarec.datasets.mind.mindSmall import MindSmall


class Mind:
    """
    Entry point class to load various versions of the MIND dataset.

    This class provides a single, convenient interface for accessing the Microsoft
    News Dataset (MIND). Based on the `version` parameter, it selects and returns
    the appropriate dataset builder for either the 'small' or 'large' version.

    MIND is a large-scale dataset for news recommendation research. It contains user
    click histories on a news website.

    **Note:** This dataset requires manual download from the official source.

    The default version is 'latest', which currently corresponds to the 'large' version.

    Examples:
        To load the training split of the large version (default):
        >>> data_loader = Mind()

        To load the validation split of the small version:
        >>> data_loader = Mind(version='small', split='validation')
    """
    latest_version = 'large'
    versions = {'large': MindLarge,
                'small': MindSmall}


    def __new__(cls, version: str = 'latest', split: str = 'train', **kwargs):
        """
        Initializes and returns the specified version of the MIND dataset builder.

        This method acts as a dispatcher, instantiating the correct builder class
        that handles the preparation and loading for a specific dataset version and split.

        Args:
            version (str): The version of the dataset to load. Supported versions
                include 'large', 'small', and 'latest'. Defaults to 'latest'.
            split (str): The data split to load. For 'large', options are 'train',
                'validation', 'test'. For 'small', options are 'train', 'validation'.
                Defaults to 'train'.
            **kwargs: Additional keyword arguments (not currently used).

        Returns:
            (MindLarge or MindSmall): An instance of the dataset builder class,
                populated with data from the specified split.

        Raises:
            ValueError: If an unsupported version string is provided.
        """

        if version == 'latest':
            version = cls.latest_version
        if version in cls.versions:
            return cls.versions[version](split=split)
        else:
            raise ValueError("Mind dataset: Unsupported version")
