"""Builder class for version 'v1' of the Alibaba-iFashion dataset."""
from datarec.data.dataset import DataRec
from datarec.io.paths import dataset_directory, dataset_raw_directory, RAW_DATA_FOLDER
from datarec.datasets.download import decompress_zip_file, decompress_7z_file
import os
import gdown
import warnings
from datarec.data.utils import verify_checksum


class AlibabaIFashion_V1(DataRec):
    """
    Builder class for the Alibaba-iFashion dataset (KDD 2019 version).

    This class handles the logic for downloading, preparing, and loading the
    Alibaba-iFashion dataset. It is not typically instantiated directly but is
    called by the `AlibabaIFashion` entry point class.

    The dataset was released for the paper "POG: Personalized Outfit Generation
    for Fashion Recommendation at Alibaba iFashion". It contains user-item interactions,
    item metadata, and outfit compositions. This loader focuses on processing the
    user-item interaction data from `user_data.txt`.

    Attributes:
        item_data_url (str): The URL for the item metadata file.
        outfit_data_url (str): The URL for the outfit composition file.
        user_data_url (str): The URL for the user-item interaction file.
        CHECKSUM_ITEM (str): MD5 checksum for the compressed item data archive.
        CHECKSUM_USER (str): MD5 checksum for the compressed user data archive.
        CHECKSUM_OUTFIT (str): MD5 checksum for the compressed outfit data archive.
    """
    item_data_url = 'https://drive.google.com/uc?id=17MAGl20_mf9V8j0-J6c7T3ayfZd-dIx8'
    outfit_data_url = 'https://drive.google.com/uc?id=1HFKUqBe5oMizU0lxy6sQE5Er1w9x-cC4'
    user_data_url = 'https://drive.google.com/uc?id=1G_1SV9H7fQMPPJOBmZpCnCkgifSsb9Ar'

    compressed_item_file_name = 'item_data.txt.zip'
    compressed_outfit_file_name = 'outfit_data.txt.zip'
    compressed_user_file_name = 'user_data.7z'

    data_file_name = 'alibaba_ifashion'

    uncompressed_item_file_name = 'item_data.txt'
    uncompressed_outfit_file_name = 'outfit_data.txt'
    uncompressed_user_file_name = 'user_data.txt'

    REQUIRED_FILES = [uncompressed_item_file_name, uncompressed_outfit_file_name, uncompressed_user_file_name]
    CHECKSUM_ITEM = 'f501244e784ae33defb71b3478d1125c'
    CHECKSUM_USER = '2ff9254d67fb13d04824621ca1387622'
    CHECKSUM_OUTFIT = 'f24078606235c122bd1d1c988766e83f'

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

        super().__init__(user=True, item=True, rating='implicit')

        self.dataset_name = 'alibaba_ifashion'
        self.version_name = 'v1'

        self._data_folder = folder if folder \
            else dataset_directory(self.dataset_name)
        self._raw_folder = os.path.abspath(os.path.join(self._data_folder, RAW_DATA_FOLDER)) if folder \
            else dataset_raw_directory(self.dataset_name)

        self.return_type = None

        # check if the required files have been already downloaded
        rq_found, rq_missing = self.required_files()
        # download and decompress the required files that are missing
        rq_found, rq_missing = self.download(found=rq_found, missing=rq_missing)
        assert len(rq_found) == len(self.REQUIRED_FILES), len(rq_missing) == 0

        data_path = None
        for p, n in rq_found:
            if n == self.uncompressed_user_file_name:
                data_path = p
                break
        assert data_path is not None, 'User data file not found'

        self.path = self.process(data_path=data_path)

    def required_files(self):
        """
        Checks for the presence of the required decompressed data files.

        Returns:
            (tuple[list, list]): A tuple where the first element is a list of
                found files and the second is a list of missing files. Each
                item in the lists is a tuple of (path, filename).
        """
        # check if the file is there
        req_files = [(os.path.join(self._raw_folder, f), f) for f in self.REQUIRED_FILES]
        found, missing = [], []
        # required file path, required file name
        for rfp, rfn in req_files:
            if os.path.isfile(rfp):
                found.append((rfp, rfn))
                print(f'Required file \'{rfn}\' found')
            else:
                missing.append((rfp, rfn))
        return found, missing

    def download_item_data(self):
        """
        Downloads, verifies, and decompresses the item data file.

        Returns:
            (str): The path to the decompressed item data file.
        """
        file_path = os.path.join(self._raw_folder, self.compressed_item_file_name)
        print(f'Downloading {self.dataset_name} item data...')
        gdown.download(self.item_data_url, file_path, quiet=False)
        print(f'{self.dataset_name} item data downloaded at \'{file_path}\'')
        verify_checksum(file_path, self.CHECKSUM_ITEM)
        print('Decompressing zip file...')
        decompress_zip_file(file_path, self._raw_folder)
        print('Deleting zip file...')
        os.remove(file_path)
        return os.path.join(self._raw_folder, self.uncompressed_item_file_name)

    def download_outfit_data(self):
        """
        Downloads, verifies, and decompresses the outfit data file.

        Returns:
            (str): The path to the decompressed outfit data file.
        """
        file_path = os.path.join(self._raw_folder, self.compressed_outfit_file_name)
        print(f'Downloading {self.dataset_name} outfit data...')
        gdown.download(self.outfit_data_url, file_path, quiet=False)
        print(f'{self.dataset_name} outfit data downloaded at \'{file_path}\'')
        verify_checksum(file_path, self.CHECKSUM_OUTFIT)
        print('Decompressing zip file...')
        decompress_zip_file(file_path, self._raw_folder)
        print('Deleting zip file...')
        os.remove(file_path)
        return os.path.join(self._raw_folder, self.uncompressed_outfit_file_name)

    def download_user_data(self):
        """
        Downloads, verifies, and decompresses the user interaction data file.

        Returns:
            (str): The path to the decompressed user data file.
        """
        file_path = os.path.join(self._raw_folder, self.compressed_user_file_name)
        print(f'Downloading {self.dataset_name} user data...')
        gdown.download(self.user_data_url, file_path, quiet=False)
        print(f'{self.dataset_name} user data downloaded at \'{file_path}\'')
        verify_checksum(file_path, self.CHECKSUM_USER)
        print('Decompressing 7z file...')
        decompress_7z_file(file_path, self._raw_folder)
        print('Deleting 7z file...')
        os.remove(file_path)
        return os.path.join(self._raw_folder, self.uncompressed_user_file_name)

    def download(self, found: list, missing: list) -> (str, str):
        """
        Downloads all missing files for the dataset.

        Iterates through the list of missing files and calls the appropriate download helper function for each one.

        Args:
            found (list): A list of file tuples that were already found locally.
            missing (list): A list of file tuples that need to be downloaded.

        Returns:
            (tuple[list, list]): The updated lists of found and missing files after
                the download and verification process.
        """
        if not os.path.exists(self._raw_folder):
            os.makedirs(self._raw_folder)
            print('Created raw files folder at \'{}\''.format(self._raw_folder))

        downloaded = []
        for required_file in missing:
            file_path, file_name = required_file

            if file_name == 'item_data.txt':
                self.download_item_data()
                downloaded.append(required_file)
            elif file_name == 'outfit_data.txt':
                self.download_outfit_data()
                downloaded.append(required_file)
            elif file_name == 'user_data.txt':
                self.download_user_data()
                downloaded.append(required_file)
            else:
                raise warnings.warn(f'You are trying to download a not required file for {self.dataset_name}.'
                                    f' \n The file will not be downloaded.', UserWarning)

        for required_file in downloaded:
            missing.remove(required_file)
            found.append(required_file)
        return found, missing

    def process(self, data_path) -> None:
        """
        Processes the raw user interaction data and loads it into the class.

        The user interaction data is in an 'inline' format, where each line
        contains a user followed by a semicolon-separated list of their item
        interactions. This method uses `read_inline` to parse this format into
        a standard user-item pair DataFrame.

        Args:
            data_path (str): The path to the raw `user_data.txt` file.

        Returns:
            (None): This method assigns the processed data to `self.data` directly.
        """
        from datarec.io.readers import read_inline
        self.data = read_inline(data_path, cols=['user', 'item', 'outfit'],
                                user_col='user', item_col='item',
                                col_sep=',', history_sep=';')
        return None
