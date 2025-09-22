"""Builder class for the Gowalla friendships (social network) dataset."""
import os
from datarec.data.dataset import DataRec
from datarec.io.paths import dataset_directory, dataset_raw_directory, RAW_DATA_FOLDER
from datarec.datasets.download import download_file, decompress_gz
from datarec.data.utils import verify_checksum


class GowallaFriendships(DataRec):
    """
    Builder class for the Gowalla friendships dataset.

    This class handles the logic for downloading, preparing, and loading the
    user-user social network graph from the Stanford SNAP repository. It is not
    typically instantiated directly but is called by the `Gowalla` entry point class
    when `version='friendships'`.

    The dataset contains the social friendship network of Gowalla users. Each row
    represents a directed edge from one user to another.

    Attributes:
        url (str): The URL from which the raw dataset is downloaded.
        CHECKSUM (str): The MD5 checksum to verify the integrity of the downloaded file.
    """
    url = 'https://snap.stanford.edu/data/loc-gowalla_edges.txt.gz'
    data_file_name = os.path.basename(url)
    decompressed_file_name = data_file_name.replace('.gz', '')
    REQUIRED_FILES = [decompressed_file_name]
    CHECKSUM = '68bce8dc51609fe32bbd95e668aaf65e'

    def __init__(self, folder=None):
        """
        Initializes the builder and orchestrates the data preparation workflow.

        Args:
            folder (str, optional): A custom directory to store the dataset files.
                If None, a default user cache directory is used. Defaults to None.
        """
        super().__init__(None)

        self.dataset_name = 'gowalla'
        self.version_name = 'friendships'

        self._data_folder = folder if folder \
            else dataset_directory(self.dataset_name)
        self._raw_folder = os.path.abspath(os.path.join(self._data_folder, RAW_DATA_FOLDER)) if folder \
            else dataset_raw_directory(self.dataset_name)

        self.return_type = None

        # check if the required files have been already downloaded
        file_path = self.required_files()

        if file_path is None:
            file_path = self.download()
            file_path = self.decompress(file_path)  # only one file

        self.process(file_path[0])

    def required_files(self):
        """
        Checks for the presence of the required decompressed data file.

        Returns:
            (list or None): A list containing the path to the required data file if
                it exists or can be created by decompression. Otherwise, returns None.
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
            (list or None): A list containing the path to the decompressed file
                if successful, otherwise None.
        """
        verify_checksum(path, self.CHECKSUM)

        # decompress downloaded file
        decompressed_file = os.path.join(self._raw_folder, self.decompressed_file_name)
        decompress_gz(path, decompressed_file)
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
        download_file(self.url, file_path, size=6351523)

        return file_path

    def process(self, file_path):
        """
        Processes the raw friendship data and loads it into the class.

        This method reads the file, which has no header. Each row
        represents a user-user link. To fit the DataRec structure, the first
        user column is mapped to 'user_id' and the second to 'item_id'.

        Args:
            file_path (str): The path to the raw friendship data file.

        Returns:
            (None): This method assigns the processed data to `self.data` directly.
        """

        from datarec.io import read_tabular

        dataset = read_tabular(file_path, sep='\t', user_col=0, item_col=1, header=None)
        self.data = dataset
