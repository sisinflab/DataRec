"""Builder class for the v1 version of the Yelp Dataset."""
import os
import pandas as pd
from datarec.data.dataset import DataRec
from datarec.io.paths import dataset_directory, dataset_raw_directory, RAW_DATA_FOLDER
from datarec.datasets.download import download_browser, decompress_tar_file, decompress_zip_file
from datarec.data.utils import verify_checksum


class Yelp_v1(DataRec):
    """
    Builder class for the Yelp Dataset.

    This class handles the logic for downloading, preparing, and loading the
    Yelp dataset. It is not typically instantiated directly but is called by
    the `Yelp` entry point class.

    The download and preparation process is multi-step:
    1. A `.zip` archive is downloaded.
    2. The zip is extracted, revealing a `.tar` archive.
    3. The tar is extracted, revealing several `.json` files.
    This loader specifically processes `yelp_academic_dataset_review.json` to extract
    user-business interactions (ratings).

    Attributes:
        url (str): The URL from which the raw dataset is downloaded.
        CHECKSUM_ZIP (str): MD5 checksum for the initial downloaded .zip file.
        CHECKSUM_TAR (str): MD5 checksum for the intermediate .tar file.
    """
    website_url = 'https://www.yelp.com/dataset'
    url = 'https://business.yelp.com/external-assets/files/Yelp-JSON.zip'
    data_file_name = 'Yelp-JSON.zip'
    data_tar_file_name = 'yelp_dataset.tar'
    subdirectory_name = 'Yelp JSON'  # once extracted the zip file
    uncompressed_business_file_name = 'yelp_academic_dataset_business.json'
    uncompressed_checkin_file_name = 'yelp_academic_dataset_checkin.json'
    uncompressed_review_file_name = 'yelp_academic_dataset_review.json'
    uncompressed_tip_file_name = 'yelp_academic_dataset_tip.json'
    uncompressed_user_file_name = 'yelp_academic_dataset_user.json'
    REQUIRED_FILES = [uncompressed_business_file_name,
                      uncompressed_checkin_file_name,
                      uncompressed_review_file_name,
                      uncompressed_tip_file_name,
                      uncompressed_user_file_name]
    CHECKSUM_ZIP = 'b0c36fe2d00a52d8de44fa3b2513c9d2'
    CHECKSUM_TAR = '0bc8cc1481ccbbd140d2aba2909a928a'

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

        self.dataset_name = 'yelp'
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
            file_path = self.decompress(file_path) ## all files

        business_file_path, checkin_file_path, review_file_path, tip_file_path, user_file_path = file_path

        print(f'found {file_path}')
        self.process(review_file_path)

    def required_files(self):
        """
        Checks for the presence of the final required decompressed JSON files.

        Returns:
            (list or None): A list of paths to the required data files if they
                exist. Otherwise, returns None.
        """
        # compressed data file
        file_path = os.path.join(self._raw_folder, self.subdirectory_name)

        # check if the file is there
        paths = [os.path.join(self._raw_folder, self.subdirectory_name, f) for f in self.REQUIRED_FILES]
        if all([os.path.exists(p) for p in paths]):
            return paths
        # check if the compressed file is there
        elif os.path.exists(file_path):
            return self.decompress(file_path)
        else:
            return None

    def decompress(self, path):
        """
        Decompresses the dataset via a two-step process (zip then tar).

        Args:
            path (str): The file path of the initial downloaded .zip archive.

        Returns:
            (list or None): A list of paths to the final decompressed files if
                successful, otherwise None.
        """
        verify_checksum(path, self.CHECKSUM_ZIP)
        decompress_zip_file(path, self._raw_folder)


        tar_file_path = os.path.join(self._raw_folder, self.subdirectory_name, self.data_tar_file_name)
        verify_checksum(tar_file_path, self.CHECKSUM_TAR)

        decompress_tar_file(tar_file_path, os.path.join(self._raw_folder, self.subdirectory_name))
        files = [os.path.join(self._raw_folder, self.subdirectory_name, f) for f in self.REQUIRED_FILES]
        if all([os.path.exists(f) for f in files]):
            return [os.path.join(self._raw_folder, f) for f in files]
        return None

    def download(self) -> (str, str):
        """
        Downloads the raw dataset compressed archive.

        Returns:
            (str): The local file path to the downloaded .zip archive.
        """
        if not os.path.exists(self._raw_folder):
            os.makedirs(self._raw_folder)
            print('Created folder \'{}\''.format(self._raw_folder))

        file_name = os.path.basename(self.url)
        file_path = os.path.join(self._raw_folder, file_name)
        if not os.path.exists(file_path):
            download_browser(self.url, file_path)
        return file_path

    def process(self, path):
        """
        Processes the raw file and loads it into the class.

        This method reads the JSON file line by line. It extracts the user ID,
        business ID (as the item), star rating, and date. The date strings are
        then converted to Unix timestamps.

        Args:
            path (str): The path to the raw file.

        Returns:
            (None): This method assigns the processed data to `self.data` directly.
        """
        from datarec.io import read_json

        user_field = 'user_id'
        item_field = 'business_id'
        rating_field = 'stars'
        date_field = 'date'  # format: YYYY-MM-DD , e.g.: 2016-03-09
        dataset = read_json(path, user_field=user_field, item_field=item_field, rating_field=rating_field, timestamp_field=date_field)
        timestamps = pd.Series(dataset.data[date_field].apply(lambda x: x.timestamp()).values,
                               index=dataset.data.index, dtype='float64')
        dataset.data.loc[:, date_field] = timestamps
        self.data = dataset
