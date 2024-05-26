import os
import pandas as pd
from datarec.data.dataset import DataRec
from datarec.io.paths import dataset_directory, dataset_raw_directory, RAW_DATA_FOLDER
from datarec.datasets.download import download_compressed_file, decompress_zip_file
from datarec.data.format import data_from_inline
from datarec.io.rawdata import RawData


class MovieLens1M_V1(DataRec):
    url = 'https://files.grouplens.org/datasets/movielens/ml-1m.zip'
    data_file_name = os.path.basename(url)
    movies_file_name = 'movies.dat'
    ratings_file_name = 'ratings.dat'
    users_file_name = 'users.dat'
    REQUIRED_FILES = [os.path.join('ml-1m', p) for p in [movies_file_name, ratings_file_name, users_file_name]]

    def __init__(self, folder=None):
        super().__init__(None)

        self.dataset_name = 'movielens1m'
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
        # the order of tha paths is the same of REQUIRED_PATHS
        movies_file_path, ratings_file_path, users_file_path = file_path

        self.path = self.process(ratings_file_path)

    def required_files(self):
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
        # decompress downloaded file
        decompress_zip_file(path, self._raw_folder)
        files = [os.path.join(self._raw_folder, f) for f in self.REQUIRED_FILES]
        if all([os.path.exists(f) for f in files]):
            return [os.path.join(self._raw_folder, f) for f in files]
        return None

    def download(self) -> (str, str):
        """
        Download the raw data
        :returns paths of the downloaded files
        """
        if not os.path.exists(self._raw_folder):
            os.makedirs(self._raw_folder)
            print('Created folder \'{}\''.format(self._raw_folder))

        # download dataset file (compressed file)
        file_path = os.path.join(self._raw_folder, self.data_file_name)
        download_compressed_file(self.url, file_path)

        return file_path

    def process(self, file_path) -> str:
        """
        Process the downloaded files and save the processed dataset
        :param train_path: path to the training dataset
        :param test_path: path to the test dataset
        :return: path of the processed dataset
        """

        from datarec.io import read_tabular

        dataset = read_tabular(file_path, sep='::', user_col=0, item_col=1, rating_col=2, timestamp_col=3, header=None)
        self.data = dataset

        # add export

        return None

    # def process(self, train_path, test_path) -> str:
    #     """
    #     Process the downloaded files and save the processed dataset
    #     :param train_path: path to the training dataset
    #     :param test_path: path to the test dataset
    #     :return: path of the processed dataset
    #     """
    #
    #     from rec_data import read_txt
    #
    #     train = read_txt(train_path)
    #     test = read_txt(test_path)
    #     dataset = train + test
    #
    #     self.data = data_from_inline(dataset, user_col=0, item_col=1)
    #     self.set_user_col()
    #     self.set_item_col()
    #     dataset_path = os.path.join(self._data_folder, 'dataset.tsv')
    #     self.to_tabular(dataset_path, force_write=True)
    #
    #     return dataset_path
