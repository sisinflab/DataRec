import os
from datarec.data.dataset import DataRec
from datarec.data.datarec_builder import BaseDataRecBuilder
from datarec.io.paths import dataset_directory, dataset_raw_directory, RAW_DATA_FOLDER
from datarec.datasets.download import download_file, decompress_gz
from datarec.data.utils import verify_checksum
from datarec.io import read_tabular


class AMZ_Office_2014(BaseDataRecBuilder):
    url = 'http://snap.stanford.edu/data/amazon/productGraph/categoryFiles/ratings_Office_Products.csv'
    data_file_name = os.path.basename(url)
    decompressed_data_file_name = data_file_name
    REQUIRED_FILES = [decompressed_data_file_name]
    CHECKSUM = 'e9f730718d699509ea2443a5f58928ca'

    def __init__(self, folder=None):

        self.dataset_name = 'AmazonOffice'
        self.version_name = '2014'

        self._data_folder = folder if folder \
            else dataset_directory(self.dataset_name)
        self._raw_folder = os.path.abspath(os.path.join(self._data_folder, self.version_name, RAW_DATA_FOLDER)) if folder \
            else dataset_raw_directory(self.dataset_name)

        self.return_type = None

    def download(self) -> (str, str):
        """
        Download the raw data
        :returns paths of the downloaded files
        """
        if not os.path.exists(self._raw_folder):
            os.makedirs(self._raw_folder)
            print('Raw files folder missing. Folder created at \'{}\''.format(self._raw_folder))

        # download dataset file
        file_name = os.path.basename(self.url)
        file_path = os.path.join(self._raw_folder, file_name)
        print('Downloading data file from {}'.format(self.url))
        download_file(self.url, file_path, size=559019689)

        return file_path

    def prepare(self):
        """
        Ensure all required raw files are present and decompressed.
        Downloads and verifies the archive if necessary.
        """
        decompress_path = os.path.join(self._raw_folder, self.decompressed_data_file_name)

        if not os.path.exists(decompress_path):
            decompress_path = self.download()

        verify_checksum(decompress_path, self.CHECKSUM)

    def load(self):
        """
        Load the dataset into a DataRec object.

        Returns:
            DataRec: The loaded dataset.
        """
        ratings_path = os.path.join(self._raw_folder, self.decompressed_data_file_name)

        dataset = read_tabular(ratings_path, sep=',',
                               user_col=0, item_col=1,
                               rating_col=2, timestamp_col=3,
                               header=None)

        dr = DataRec(dataset_name=self.dataset_name, version_name=self.version_name)
        dr.data = dataset

        return dr
