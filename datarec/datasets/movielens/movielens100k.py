"""Builder class for the MovieLens 100k dataset."""
import os
from datarec.data.datarec_builder import BaseDataRecBuilder
from datarec.data.dataset import DataRec
from datarec.io.paths import dataset_directory, dataset_raw_directory, RAW_DATA_FOLDER
from datarec.datasets.download import download_file, decompress_zip_file
from datarec.data.utils import verify_checksum


class MovieLens100k(BaseDataRecBuilder):
    """
    Builder class for the MovieLens 100k dataset.

    This dataset contains 100,000 ratings. It is not typically instantiated
    directly but is called by the `MovieLens` entry point class.

    The raw data is provided in a tab-separated file (`u.data`).

    Attributes:
        url (str): The URL from which the raw dataset is downloaded.
        CHECKSUM (str): The MD5 checksum to verify the integrity of the downloaded file.
        REQUIRED_FILES (list): A list of file paths expected after decompression.
    """
    url = 'https://files.grouplens.org/datasets/movielens/ml-100k.zip'
    data_file_name = os.path.basename(url)
    ratings_file_name = 'u.data'
    REQUIRED_FILES = [os.path.join('ml-100k', p) for p in [ratings_file_name]]
    CHECKSUM = "0e33842e24a9c977be4e0107933c0723"

    def __init__(self, folder=None):
        """
        Initializes the builder.

        This constructor sets up the necessary paths for caching the dataset.

        Args:
            folder (str, optional): A custom directory to store the dataset files.
                If None, a default user cache directory is used. Defaults to None.
        """
        self.dataset_name = 'MovieLens'
        self.version_name = '100k'

        self._data_folder = folder if folder \
            else dataset_directory(self.dataset_name)
        self._raw_folder = os.path.abspath(
            os.path.join(self._data_folder, self.version_name, RAW_DATA_FOLDER)) if folder \
            else os.path.join(dataset_raw_directory(self.dataset_name), self.version_name)

    def prepare(self):
        """
        Ensures all required raw files are downloaded and decompressed.

        This method checks for the existence of the required files. If they are
        not found, it triggers the download and decompression process.
        """
        if self.required_files() is not None:
            # All required files are already available
            return

        file_path = self.download()
        verify_checksum(file_path, self.CHECKSUM)
        self.decompress(file_path)

    def load(self):
        """
        Loads the prepared `u.data` file into a DataRec object.

        Returns:
            (DataRec): A DataRec object containing the user-item interactions.
        """
        from datarec.io import read_tabular

        ratings_file_path = self.required_files()[0]
        dataset = read_tabular(ratings_file_path, sep='\t', user_col=0, item_col=1, rating_col=2, timestamp_col=3,
                               header=None)
        return DataRec(rawdata=dataset,
                       dataset_name=self.dataset_name,
                       version_name=self.version_name)

    def required_files(self):
        """
        Check whether the required dataset files exist.

        Returns:
            (list[str]): Paths to required files if they exist, or None.
        """
        # compressed data file
        file_path = os.path.join(self._raw_folder, self.data_file_name)

        # check if the file is there
        paths = [os.path.join(self._raw_folder, f) for f in self.REQUIRED_FILES]
        if all([os.path.exists(p) for p in paths]):
            return paths
        # check if the compressed file is there
        elif os.path.exists(file_path):
            return self.decompress(file_path)
        else:
            return None

    def decompress(self, path):
        """
        Decompress the downloaded zip file and verify required files.

        Args:
            path (str): Path to the zip file.

        Returns:
            (list[str]): Paths to the extracted files if successful, or None.
        """
        decompress_zip_file(path, self._raw_folder)
        files = [os.path.join(self._raw_folder, f) for f in self.REQUIRED_FILES]
        if all([os.path.exists(f) for f in files]):
            return [os.path.join(self._raw_folder, f) for f in files]
        return None

    def download(self) -> str:
        """
        Download the raw dataset zip file to the raw folder.

        Returns:
            (str): Path to the downloaded zip file.
        """
        if not os.path.exists(self._raw_folder):
            os.makedirs(self._raw_folder)
            print('Created folder \'{}\''.format(self._raw_folder))

        # download dataset file (compressed file)
        file_path = os.path.join(self._raw_folder, self.data_file_name)
        download_file(self.url, file_path)

        return file_path

