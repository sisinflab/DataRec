"""Builder class for the 2023 version of the Amazon Video Games dataset."""
import os
from datarec.data.dataset import DataRec
from datarec.io.paths import dataset_directory, dataset_raw_directory, RAW_DATA_FOLDER
from datarec.datasets.download import download_file, decompress_gz
from datarec.data.utils import verify_checksum


class AMZ_VideoGames_2023(DataRec):
    """
    Builder class for the Amazon Video Games dataset (2023 version).

    This class handles the logic for downloading, preparing, and loading the
    2023 version of the "Video Games" dataset. It is not typically
    instantiated directly but is called by the `AmazonVideoGames` entry point class.

    The dataset is from the "Bridging Language and Items for Retrieval and
    Recommendation" paper and is provided as a compressed CSV file with a header.

    Attributes:
        url (str): The URL from which the raw dataset is downloaded.
        CHECKSUM (str): The MD5 checksum to verify the integrity of the downloaded file.
    """
    url = 'https://mcauleylab.ucsd.edu/public_datasets/data/amazon_2023/benchmark/0core/rating_only/Video_Games.csv.gz'
    data_file_name = os.path.basename(url)
    decompressed_data_file_name = data_file_name.replace('.gz', '')
    CHECKSUM = '60fdc3e812de871c30d65722e9a91a0a'

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

        self.dataset_name = 'amazon_video_games'
        self.version_name = '2023'

        self._data_folder = folder if folder \
            else dataset_directory(self.dataset_name)
        self._raw_folder = os.path.abspath(os.path.join(self._data_folder, self.version_name, RAW_DATA_FOLDER)) if folder \
            else os.path.join(dataset_raw_directory(self.dataset_name), self.version_name)
        # check if the required files have been already downloaded
        file_path = self.required_files()

        if file_path is None:
            file_path = self.download()
            file_path = self.decompress(file_path)

        print(f'files: {file_path}')

        self.process(file_path)

    def required_files(self):
        """
        Checks for the presence of the required decompressed data file.

        It first looks for the final, uncompressed file. If not found, it
        looks for the compressed archive and decompresses it.

        Returns:
            (str or None): The path to the required data file if it exists or can be
                created by decompression. Otherwise, returns None.
        """
        # compressed data file
        file_path = os.path.join(self._raw_folder, self.data_file_name)
        uncompressed_file_path = os.path.join(self._raw_folder, self.decompressed_data_file_name)

        # check if the file is there
        if os.path.exists(uncompressed_file_path):
            return uncompressed_file_path
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
            (str): The path to the decompressed file.
        """
        verify_checksum(path, self.CHECKSUM)

        # decompress downloaded file
        decompressed_file_path = os.path.join(self._raw_folder, self.decompressed_data_file_name)
        return decompress_gz(path, decompressed_file_path)

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
        file_name = os.path.basename(self.url)
        file_path = os.path.join(self._raw_folder, file_name)
        download_file(self.url, file_path, size=115388622)

        return file_path

    def process(self, file_path):
        """
        Processes the raw data and loads it into the class.

        This method reads the decompressed file, which includes a header row,
        into a pandas DataFrame and assigns it to the `self.data` attribute.

        Args:
            file_path (str): The path to the raw data file.

        Returns:
            (None): This method assigns the processed data to `self.data` directly.
        """

        from datarec.io import read_tabular

        dataset = read_tabular(file_path, sep=',',
                               user_col='user_id', item_col='parent_asin',
                               rating_col='rating', timestamp_col='timestamp',
                               header=0)
        self.data = dataset
