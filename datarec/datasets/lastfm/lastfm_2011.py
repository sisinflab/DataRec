"""Builder class for the 2011 version of the Last.fm dataset (HetRec 2011)."""
import os
from datarec.data.dataset import DataRec
from datarec.io.paths import dataset_directory, dataset_raw_directory, RAW_DATA_FOLDER
from datarec.datasets.download import download_file, decompress_zip_file
from datarec.data.utils import verify_checksum


class LastFM2011(DataRec):
    """
    Builder class for the Last.fm dataset (HetRec 2011 version).

    This class handles the logic for downloading, preparing, and loading the
    Last.fm dataset provided for the 2nd International Workshop on Information
    Heterogeneity and Fusion in Recommender Systems (HetRec 2011).

    The full archive contains multiple files (user-friends, tags, etc.), but this
    loader specifically processes the `user_artists.dat` file, which contains
    artists listened to by each user and a corresponding listening count (`weight`).

    Attributes:
        url (str): The URL from which the raw dataset is downloaded.
        CHECKSUM (str): The MD5 checksum to verify the integrity of the downloaded file.
        REQUIRED_FILES (list): A list of all files expected within the decompressed archive.
    """

    url = 'https://files.grouplens.org/datasets/hetrec2011/hetrec2011-lastfm-2k.zip'
    data_file_name = os.path.basename(url)
    decompressed_data_file_name = data_file_name.replace('.zip', '')

    user_artists_file_name = 'user_artists.dat'
    tags_file_name = 'tags.dat'
    artists_file_name = 'artists.dat'
    user_taggedartists_file_name = 'user_taggedartists.dat'
    user_taggedartists_timestamp_file_name = 'user_taggedartists-timestamps.dat'
    user_friends_file_name = 'user_friends.dat'

    REQUIRED_FILES = [p for p in
                      [user_friends_file_name, user_taggedartists_file_name, user_taggedartists_timestamp_file_name,
                       artists_file_name, tags_file_name, user_artists_file_name]]
    # REQUIRED_FILES = [os.path.join('ml-1m', p) for p in [movies_file_name, ratings_file_name, users_file_name]]
    CHECKSUM = '296d61afe4e8632b173fc2dd3be20ce2'

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

        self.dataset_name = 'lastfm'
        self.version_name = '2011'

        self._data_folder = folder if folder \
            else dataset_directory(self.dataset_name)
        self._raw_folder = os.path.abspath(os.path.join(self._data_folder, self.version_name, RAW_DATA_FOLDER)) if folder \
            else os.path.join(dataset_raw_directory(self.dataset_name), self.version_name)

        self.return_type = None

        # check if the required files have been already downloaded
        file_path = self.required_files()

        if file_path is None:
            file_path = self.download()
            file_path = self.decompress(file_path)

        user_friends_file_path, user_taggedartists_file_path, user_taggedartists_timestamp_file_path, artists_file_path, tags_file_path, user_artists_file_path = file_path
        self.process(user_artists_file_path)

    def required_files(self):
        """
        Checks for the presence of all required decompressed data files.

        Returns:
            (list or None): A list of paths to the required data files if they
                exist or can be created by decompression. Otherwise, returns None.
        """
        # compressed data file
        file_path = os.path.join(self._raw_folder, self.data_file_name)
        paths = [os.path.join(self._raw_folder, f) for f in self.REQUIRED_FILES]

        if all([os.path.exists(p) for p in paths]):
            return paths
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
        file_name = os.path.basename(self.url)
        file_path = os.path.join(self._raw_folder, file_name)
        download_file(self.url, file_path)

        return file_path

    def process(self, file_path):
        """
        Processes the raw `user_artists.dat` file and loads it into the class.

        This method reads the tab-separated file, which includes a header. It maps
        the 'userID', 'artistID', and 'weight' columns to the standard user, item,
        and rating columns, respectively. Note that timestamp information is not
        available in this specific file.

        Args:
            file_path (str): The path to the raw `user_artists.dat` file.

        Returns:
            (None): This method assigns the processed data to `self.data` directly.
        """

        from datarec.io import read_tabular
        dataset = read_tabular(file_path, sep='\t',
                               user_col='userID', item_col='artistID',
                               rating_col='weight',
                               header=0)
        self.data = dataset
