import os
import pandas as pd
from datarec.data.dataset import DataRec
from datarec.io.paths import dataset_directory, dataset_raw_directory, RAW_DATA_FOLDER
from datarec.datasets.download import download_url, decompress_tar_file
from datarec.data.format import data_from_inline


class Yelp_v1(DataRec):
    website_url = 'https://www.yelp.com/dataset'
    data_file_name = 'yelp_dataset.tar'
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

    def __init__(self, folder=None):
        super().__init__(pd.DataFrame(), user=True, item=True, rating='implicit')

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

        print(f'found {file_path}')
        # TODO : process method
        # self.path = self.process(train_path, test_path)

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
        decompress_tar_file(path, self._raw_folder)
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

        print(f'\nThis version of Yelp dataset requires the user to manually download it.\n'
              f'Please, go to {self.website_url} on your browser and click on \'Download Dataset\''
              f' or go directly on https://www.yelp.com/dataset/download.\n'
              f'Then, move or copy \'yelp_dataset.tar\' in the following directory:\n'
              f'\'{self._raw_folder}\'\n'
              f'Please, do not change the original file name and try again.')

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
