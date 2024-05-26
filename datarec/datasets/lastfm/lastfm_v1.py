import os
import pandas as pd
from datarec.data.dataset import DataRec
from datarec.io.paths import dataset_directory, dataset_raw_directory, RAW_DATA_FOLDER
from datarec.datasets.download import download_compressed_file
from datarec.data.format import data_from_inline


class LastFM_V1(DataRec):
    url = 'https://files.grouplens.org/datasets/hetrec2011/hetrec2011-lastfm-2k.zip'

    def __init__(self, folder=None):
        super().__init__(pd.DataFrame(), user=True, item=True, rating='implicit')

        self.dataset_name = 'lastfm'
        self.version_name = 'v1'

        self._data_folder = folder if folder \
            else dataset_directory(self.dataset_name)
        self._raw_folder = os.path.abspath(os.path.join(self._data_folder, RAW_DATA_FOLDER)) if folder \
            else dataset_raw_directory(self.dataset_name)

        self.return_type = None

        self.download()

        # TODO : process method
        # self.path = self.process(train_path, test_path)

    def download(self) -> (str, str):
        """
        Download the raw data
        :returns paths of the downloaded files
        """
        if not os.path.exists(self._raw_folder):
            os.makedirs(self._raw_folder)
            print('Created folder \'{}\''.format(self._raw_folder))

        # download dataset file (compressed file)
        file_name = os.path.basename(self.url)
        file_path = os.path.join(self._raw_folder, file_name)
        download_compressed_file(self.url, file_path)

        return file_path


    def process(self, train_path, test_path) -> str:
        # TODO: fare in seguito
        """
        Process the downloaded files and save the processed dataset
        :param train_path: path to the training dataset
        :param test_path: path to the test dataset
        :return: path of the processed dataset
        """

        from datarec import read_txt

        train = read_txt(train_path)
        test = read_txt(test_path)
        dataset = train + test

        self.data = data_from_inline(dataset, user_col=0, item_col=1)
        for col in self.data.columns:
            self.data[col] = self.data[col].astype(int)
        self.data = self.data.sort_values([self.user_col, self.item_col]).reset_index(drop=True)

        dataset_path = os.path.join(self._data_folder, 'dataset.tsv')
        self.to_tabular(dataset_path, force_write=True)

        return dataset_path

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
