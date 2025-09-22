"""Builder class for the v1 version of the CiaoDVD dataset."""
import os
import pandas as pd
from datarec.data.dataset import DataRec
from datarec.io.paths import dataset_directory, dataset_raw_directory, RAW_DATA_FOLDER
from datarec.datasets.download import download_file, decompress_zip_file
from datarec.data.utils import verify_checksum


class Ciao_V1(DataRec):
    """
    Builder class for the CiaoDVD dataset.

    This class handles the logic for downloading, preparing, and loading the
    CiaoDVD dataset from the LibRec repository. It is not typically instantiated
    directly but is called by the `Ciao` entry point class.

    The dataset was introduced in the paper "ETAF: An Extended Trust Antecedents
    Framework for Trust Prediction". The archive contains multiple files; this
    loader specifically processes `movie-ratings.txt`.

    Attributes:
        url (str): The URL from which the raw dataset is downloaded.
        CHECKSUM (str): The MD5 checksum to verify the integrity of the downloaded file.
        REQUIRED_FILES (list): A list of files expected within the decompressed archive.
    """
    url = 'https://guoguibing.github.io/librec/datasets/CiaoDVD.zip'
    data_file_name = os.path.basename(url)
    movie_file_name = 'movie-ratings.txt'
    review_file_name = 'review-ratings.txt'
    trusts_file_name = 'trusts.txt'
    REQUIRED_FILES = [movie_file_name, review_file_name, trusts_file_name]
    CHECKSUM = '43a39e068e3fc494a7f7f7581293e2c2'


    def __init__(self, folder=None):
        """
        Initializes the builder and orchestrates the data preparation workflow.

        This constructor sets up the necessary paths and automatically triggers
        the download, verification, and processing steps if the data is not
        already present in the specified cache directory.

        Args:
            folder (str, optional): A custom directory to store the dataset files.
                If None, a default user cache directory is used. Defaults to None.
        """
        super().__init__(None)

        self.dataset_name = 'ciaoDVD'
        self.version_name = 'v1'

        self._data_folder = folder if folder \
            else dataset_directory(self.dataset_name)
        self._raw_folder = os.path.abspath(os.path.join(self._data_folder, RAW_DATA_FOLDER)) if folder \
            else dataset_raw_directory(self.dataset_name)

        self.return_type = None

        # check if the required files have been already downloaded
        file_path = self.required_files()

        if file_path is None:
            file_path = self.download()
            file_path = self.decompress(file_path)

        print(f'files: {file_path}')

        rating_file_path = os.path.abspath(os.path.join(self._raw_folder, self.movie_file_name))
        self.process(rating_file_path)

    def required_files(self):
        """
        Checks for the presence of the required decompressed data files.

        It first looks for the final, uncompressed files. If not found, it
        looks for the compressed archive and decompresses it.

        Returns:
            (list or None): A list of paths to the required data files if they
                exist or can be created by decompression. Otherwise, returns None.
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
        Decompresses the downloaded archive after verifying its checksum.

        Args:
            path (str): The file path of the compressed archive.

        Returns:
            (list or None): A list of paths to the decompressed files if successful,
                otherwise None.
        """
        verify_checksum(path, self.CHECKSUM)

        # decompress downloaded file
        decompress_zip_file(path, self._raw_folder)
        files = [os.path.join(self._raw_folder, f) for f in self.REQUIRED_FILES]
        if all([os.path.exists(f) for f in files]):
            return [os.path.join(self._raw_folder, f) for f in files]
        return None

    def download(self) -> (str, str):
        """
        Downloads the raw dataset compressed archive.

        Returns:
            (str): The local file path to the downloaded archive.
        """
        if not os.path.exists(self._raw_folder):
            os.makedirs(self._raw_folder)
            print('Created folder \'{}\''.format(self._raw_folder))

        # download dataset file (compressed file)
        file_path = os.path.join(self._raw_folder, self.data_file_name)
        download_file(self.url, file_path, size=5814757)

        return file_path

    def process(self, path) -> None:
        """
        Processes the raw `movie-ratings.txt` data and loads it into the class.

        This method reads the file, which has no header. It also parses the
        date strings in 'YYYY-MM-DD' format and converts them to Unix timestamps.

        Args:
            path (str): The path to the raw `movie-ratings.txt` file.

        Returns:
            (None): This method assigns the processed data to `self.data` directly.
        """

        from datarec.io import read_tabular

        user_col = 0
        item_col = 1
        rating_col = 4
        timestamp_col = 5
        dataset = read_tabular(path, sep=',', user_col=user_col, item_col=item_col, rating_col=rating_col, timestamp_col=timestamp_col, header=None)
        # timestamps = pd.Series(dataset.data[timestamp_col].apply(lambda x: x.timestamp()).values,
        #                        index=dataset.data.index, dtype='float64')

        # Convert the date strings to datetime objects using the specified format
        dataset.data[timestamp_col] = pd.to_datetime(dataset.data[timestamp_col], format='%Y-%m-%d')

        # Now extract the Unix timestamps (in seconds)
        timestamps = pd.Series(dataset.data[timestamp_col].apply(lambda x: x.timestamp()).values,
                               index=dataset.data.index, dtype='float64')
        dataset.data[timestamp_col] = timestamps

        self.data = dataset
