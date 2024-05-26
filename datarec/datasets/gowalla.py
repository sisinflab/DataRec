import os
import pandas as pd
from datarec.data.dataset import DataRec
from datarec.io.paths import dataset_directory, dataset_raw_directory, RAW_DATA_FOLDER
from .download import download_url
from datarec.data.format import data_from_inline


class Gowalla(DataRec):

    train_url = ('https://raw.githubusercontent.com/huangtinglin/'
                 'Knowledge_Graph_based_Intent_Network/main/data/amazon-book/train.txt')
    test_url = ('https://raw.githubusercontent.com/huangtinglin/'
                'Knowledge_Graph_based_Intent_Network/main/data/amazon-book/test.txt')

    def __init__(self, folder=None):
        super().__init__(pd.DataFrame(), user=True, item=True, rating='implicit')

        self.dataset_name = 'gowalla'
        self._data_folder = folder if folder \
            else dataset_directory(self.dataset_name)
        self._raw_folder = os.path.abspath(os.path.join(self._data_folder, RAW_DATA_FOLDER)) if folder\
            else dataset_raw_directory(self.dataset_name)

        self.return_type = None

        train_path, test_path = self.download()
        self.path = self.process(train_path, test_path)

    def download(self) -> (str, str):
        """
        Download the raw data
        :returns paths of the downloaded files
        """
        if not os.path.exists(self._raw_folder):
            os.makedirs(self._raw_folder)
            print('Created folder \'{}\''.format(self._raw_folder))

        # download train file
        train_path = os.path.join(self._raw_folder, 'train.txt')
        download_url(self.train_url, train_path)
        print('Downloaded file at \'{}\''.format(train_path))

        # download test file
        test_path = os.path.join(self._raw_folder, 'test.txt')
        download_url(self.test_url, test_path)
        print('Downloaded file at \'{}\''.format(test_path))

        return train_path, test_path

    def process(self, train_path, test_path) -> str:
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

