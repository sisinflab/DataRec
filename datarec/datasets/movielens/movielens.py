"""Entry point for loading different versions of the MovieLens dataset."""
from datarec.data.dataset import DataRec
from datarec.datasets.movielens.movielens100k import BaseDataRecBuilder
from datarec.datasets.movielens.movielens1m import MovieLens1M
from datarec.datasets.movielens.movielens20m import MovieLens20M
from datarec.datasets.movielens.movielens100k import MovieLens100k


class MovieLens:
    """Entry point class to load various versions of the MovieLens dataset.

    This class provides a single, convenient interface for accessing the dataset.
    Based on the `version` parameter, it selects and returns the appropriate
    dataset builder.

    The MovieLens datasets are a collection of movie ratings data collected by the
    GroupLens Research project at the University of Minnesota.

    The default version is 'latest', which currently corresponds to the '1m' version.

    Examples:
        To load the latest version (1M):
        >>> ml_1m = MovieLens().prepare_and_load()

        To load a specific version (e.g., 100k):
        >>> ml_100k = MovieLens(version='100k').prepare_and_load()
    """
    latest_version = '1m'

    def __new__(cls, version: str = 'latest', **kwargs) -> BaseDataRecBuilder:
        """
        Initializes and returns the specified version of the MovieLens dataset builder.

        This method acts as a dispatcher, instantiating the correct builder class
        that handles the downloading, caching, and loading for a specific dataset version.

        Note: The returned object is a builder. You must call `.prepare_and_load()`
        on it to get a populated `DataRec` object.

        Args:
            version (str): The version of the dataset to load. Supported versions
                include '1m', '20m', '100k', and 'latest'. Defaults to 'latest'.
            **kwargs: Additional keyword arguments (not currently used).

        Returns:
            (BaseDataRecBuilder): An instance of the appropriate dataset builder class
                (e.g., `MovieLens1M`), ready to prepare and load data.

        Raises:
            ValueError: If an unsupported version string is provided.
        """
        versions = {'1m': MovieLens1M,
                    '20m': MovieLens20M,
                    '100k': MovieLens100k}
        if version == 'latest':
            version = cls.latest_version
        if version in versions:
            return versions[version]()
        else:
            raise ValueError(f"MovieLens {version}: Unsupported version \n Supported version:"
                             f"\n \t version \t name "
                             f"\n \t 1m \t Movielens 1 Million "
                             f"\n \t 20m \t Movielens 20 Million")
