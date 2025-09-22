import os
from datarec.data.dataset import DataRec
from datarec.data.datarec_builder import BaseDataRecBuilder
from datarec.io.paths import dataset_directory, dataset_raw_directory, RAW_DATA_FOLDER
from datarec.datasets.download import download_file, decompress_zip_file
from datarec.data.utils import verify_checksum
from datarec.io import read_tabular


class MovieLens1M(BaseDataRecBuilder):
    """
    Builder class for the MovieLens 1M dataset.

    This dataset contains 1 million ratings. It is not typically instantiated directly but is
    called by the `MovieLens` entry point class.

    The raw ratings data is provided in `ratings.dat` with a `::` separator.

   Attributes:
       url (str): The URL from which the raw dataset is downloaded.
       CHECKSUM (str): The MD5 checksum to verify the integrity of the downloaded file.
       REQUIRED_FILES (list): A list of file paths expected after decompression.
   """
    url = 'https://files.grouplens.org/datasets/movielens/ml-1m.zip'
    data_file_name = os.path.basename(url)
    movies_file_name = 'movies.dat'
    ratings_file_name = 'ratings.dat'
    users_file_name = 'users.dat'
    REQUIRED_FILES = [os.path.join('ml-1m', p) for p in [movies_file_name, ratings_file_name, users_file_name]]
    CHECKSUM = "c4d9eecfca2ab87c1945afe126590906"

    def __init__(self, folder=None):
        """
        Initializes the builder.

        This constructor sets up the necessary paths for caching the dataset.

        Args:
            folder (str, optional): A custom directory to store the dataset files.
                If None, a default user cache directory is used. Defaults to None.
        """
        self.dataset_name = 'MovieLens'
        self.version_name = '1m'

        self._data_folder = folder if folder else dataset_directory(self.dataset_name)
        self._raw_folder = (
            os.path.abspath(os.path.join(self._data_folder, self.version_name, RAW_DATA_FOLDER))
            if folder
            else os.path.join(dataset_raw_directory(self.dataset_name), self.version_name)
        )

    def download(self) -> str:
        """
        Downloads the raw dataset archive file.

        Returns:
            (str): The local file path to the downloaded zip file.
        """
        if not os.path.exists(self._raw_folder):
            os.makedirs(self._raw_folder)
            print(f"Created folder '{self._raw_folder}'")

        file_path = os.path.join(self._raw_folder, self.data_file_name)
        if not os.path.exists(file_path):
            download_file(self.url, file_path)
        return file_path

    def prepare(self):
        """
        Ensures all required raw files are downloaded and decompressed.

        This method checks for the existence of the required files. If they are
        not found, it triggers the download and decompression process.
        """
        raw_paths = [os.path.join(self._raw_folder, f) for f in self.REQUIRED_FILES]
        if all(os.path.exists(p) for p in raw_paths):
            return

        archive_path = os.path.join(self._raw_folder, self.data_file_name)
        if not os.path.exists(archive_path):
            archive_path = self.download()

        verify_checksum(archive_path, self.CHECKSUM)
        decompress_zip_file(archive_path, self._raw_folder)

    def load(self) -> DataRec:
        """
        Loads the prepared `ratings.dat` file into a DataRec object.

        Returns:
            (DataRec): A DataRec object containing the user-item interactions.
        """
        ratings_path = os.path.join(self._raw_folder, 'ml-1m', self.ratings_file_name)
        dataset = read_tabular(ratings_path, sep='::', user_col=0, item_col=1, rating_col=2, timestamp_col=3, header=None)

        dr = DataRec(dataset_name=self.dataset_name, version_name=self.version_name)
        dr.data = dataset
        return dr
