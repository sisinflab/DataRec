"""Builder class for the large version of the MIND dataset."""
import os
from datarec.data.dataset import DataRec
from datarec.io import RawData
from datarec.io.paths import dataset_directory, RAW_DATA_FOLDER
from datarec.datasets.download import decompress_zip_file
from datarec.io.readers import read_inline
from datarec.data.utils import verify_checksum


class MindLarge(DataRec):
    """
    Builder class for the large version of the MIND dataset.

    This class handles the logic for preparing and loading the MINDlarge dataset.
    It is not typically instantiated directly but is called by the `Mind` entry
    point class.

    **Note on usage:** The MIND dataset must be downloaded manually. This class will
    prompt the user to download the required zip files and place them in the
    correct cache directory before proceeding with decompression and processing.

    The dataset is pre-split into train, validation, and test sets, which can be
    loaded individually.

    Attributes:
        source (str): The official website for the dataset.
        REQUIRED (dict): A dictionary detailing the filenames and checksums for
            each data split (train, validation, test).
    """
    source = 'https://msnews.github.io/#Download'

    REQUIRED = {
        'train': {
            'compressed': 'MINDlarge_train.zip',
            'decompressed': ['behaviors.tsv', 'entity_embedding.vec', 'relation_embedding.vec', 'news.tsv'],
            'interactions': 'behaviors.tsv',
            'checksum': '5be1c8f9a6809092db5fc0ac23d60f72'
        },
        'validation': {
            'compressed': 'MINDlarge_dev.zip',
            'decompressed': ['behaviors.tsv', 'entity_embedding.vec', 'relation_embedding.vec', 'news.tsv'],
            'interactions': 'behaviors.tsv',
            'checksum': '8f3dd8923172048b0e5980e7ee40841b'
        },
        'test': {
            'compressed': 'MINDlarge_test.zip',
            'decompressed': ['behaviors.tsv', 'entity_embedding.vec', 'relation_embedding.vec', 'news.tsv'],
            'interactions': 'behaviors.tsv',
            'checksum': '50406027c032898d9eddf9c8a8ecbc17'
        }
    }

    SPLITS = ('train', 'validation', 'test')

    NAME = 'MIND'
    VERSION = 'small'

    def __init__(self, folder=None, split='train'):
        """
        Initializes the builder and orchestrates the data preparation workflow.

        This constructor sets up paths and checks for the required files. If the
        compressed archives are missing, it provides instructions for manual
        download. It then proceeds to decompress and process the specified split.

        Args:
            folder (str, optional): A custom directory to store the dataset files.
                If None, a default user cache directory is used. Defaults to None.
            split (str, optional): The data split to load, one of 'train',
                'validation', or 'test'. Defaults to 'train'.
        """
        super().__init__(None)

        self.dataset_name = self.NAME
        self.version_name = self.VERSION

        # set data folder and raw folder
        self._data_folder = folder if folder \
            else dataset_directory(self.dataset_name)
        self._raw_folder = os.path.abspath(os.path.join(
            self._data_folder, self.version_name, RAW_DATA_FOLDER)) if folder \
            else os.path.join(dataset_directory(self.dataset_name), self.version_name, RAW_DATA_FOLDER)

        if not os.path.exists(self._data_folder):
            os.makedirs(self._data_folder)
            print('Created data folder \'{}\''.format(self._data_folder))

        if not os.path.exists(self._raw_folder):
            os.makedirs(self._raw_folder)
            print('Created raw folder \'{}\''.format(self._raw_folder))

        # check if the required files have been already downloaded
        found, missing = self.required_files()

        for file_type in missing:
            file_path = self.download(file_type=file_type)
            self.decompress(file_type, file_path)

        self.process(split=split)

    def required_files(self):
        """
        Checks for the presence of the required compressed and decompressed files.

        Returns:
            (tuple[list, list]): A tuple where the first element is a list of
                found splits and the second is a list of missing splits.
        """
        found, missing = [], []

        # check each required file
        for rn, rf in self.REQUIRED.items():
            # check if decompressed file is there
            comp, dec = rf['compressed'], rf['decompressed']
            decompressed_path = [os.path.join(self._raw_folder, rn, dec_name) for dec_name in dec]
            # all the decompressed files should be there, otherwise it needs to decompress the compressed file again
            if all([os.path.exists(p) for p in decompressed_path]):
                # files found!
                found.append(rn)
            else:
                # check if compressed file is there
                compressed_path = os.path.join(self._raw_folder, comp)
                if os.path.exists(compressed_path):
                    # decompress compressed file
                    self.decompress(file_type=rn, path=compressed_path)
                    # files ready!
                    found.append(rn)
                else:
                    # add missing file to missing list
                    missing.append(rn)
        return found, missing

    def decompress(self, file_type, path):
        """
        Decompresses the specified zip archive after verifying its checksum.

        Args:
            file_type (str): The split type ('train', 'validation', 'test').
            path (str): The file path of the compressed .zip archive.

        Returns:
            (list): A list of paths to the decompressed files.

        Raises:
            FileNotFoundError: If decompression fails to produce the expected files.
        """
        assert file_type in ('train', 'validation', 'test'), 'Invalid required file type'

        verify_checksum(path, self.REQUIRED[file_type]['checksum'])

        # decompress downloaded file
        output_folder = os.path.join(self._raw_folder, file_type)
        if not os.path.exists(output_folder):
            os.makedirs(output_folder)
        decompress_zip_file(path, output_folder)

        # check that all the files in the compressed file exist
        files = [os.path.join(output_folder, f) for f in self.REQUIRED[file_type]['decompressed']]
        if all([os.path.exists(f) for f in files]):
            return files
        else:
            raise FileNotFoundError(f'Error decompressing file \'{path}\'')

    def download(self, file_type) -> str:
        """
        Guides the user to manually download the dataset archive.

        This method does not download automatically. Instead, it prints instructions
        and waits for the user to place the required file in the cache directory.

        Args:
            file_type (str): The split type ('train', 'validation', 'test') to download.

        Returns:
            (str): The local file path to the user-provided archive.

        Raises:
            FileNotFoundError: If the file is not found after the user confirms download.
        """
        print(f'\'{file_type}\' MIND file not found.')

        print('Microsoft News Dataset (MIND) requires manual download from the source.\n'
              'Please download the dataset from the following link:\n'
              'https://msnews.github.io/#Download\n'
              'Then, place the downloaded files in the following directory:\n'
              f'{self._raw_folder}')

        # press continue after downloading the dataset
        input('Press Enter to continue after downloading the dataset...')

        file_path = os.path.join(self._raw_folder, self.REQUIRED[file_type]['compressed'])
        if not os.path.exists(file_path):
            raise FileNotFoundError(f'MIND \'{file_type}\' file not found.')
        return file_path

    def process_split(self, split) -> RawData:
        """
        Processes a single split from the decompressed files.

        This method reads the `behaviors.tsv` file for a given split, which
        is in an 'inline' format, and parses it.

        Args:
            split (str): The data split to process ('train', 'validation', or 'test').

        Returns:
            (RawData): A RawData object containing the user-item interactions.

        Raises:
            ValueError: If an invalid split name is provided.
        """

        if split not in self.SPLITS:
            raise ValueError(f'Invalid split type: {split}')

        # read the dataset
        file_path = os.path.join(self._raw_folder, split, self.REQUIRED[split]['interactions'])
        print('Reading file:', file_path)
        return read_inline(file_path, cols=['impression_id', 'user', 'time', 'item', 'impressions'],
                           col_sep='\t', history_sep=' ')

    def process(self, split) -> None:
        """
        Loads the processed data for the specified split into the class.

        Args:
            split (str): The data split to load ('train', 'validation', or 'test').

        Returns:
            (None): This method assigns the processed data to `self.data` directly.

        Raises:
            ValueError: If an invalid split name is provided.
        """

        if split not in self.SPLITS and split != 'merge':
            raise ValueError(f'Invalid split type: {split}')

        if split == 'merge':
            # merge all the splits
            data = None
            for s in self.SPLITS:
                print('Processing split:', s)
                if data is None:
                    data = self.process_split(split=s)
                else:
                    data = data + self.process_split(split=s)
            print('Split merged successfully')
            print('Sorting data...')
            data.data = data.data.sort_values(by=[data.user, data.item])
            print('Reindexing data...')
            data.data = data.data.reset_index(drop=True)
            print(f'{split} split processed successfully')
            self.data = data
        else:
            self.data = self.process_split(split=split)
            print(f'{split} split processed successfully')
