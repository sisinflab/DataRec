import os
import pandas as pd
from datarec.data.dataset import DataRec
from datarec.io.paths import dataset_directory, dataset_raw_directory, RAW_DATA_FOLDER
from datarec.datasets.download import download_url, decompress_zip_file
from datarec.data.format import data_from_inline
import gdown

class AlibabaIFashion_V1(DataRec):
    item_data_url = 'https://drive.google.com/uc?id=17MAGl20_mf9V8j0-J6c7T3ayfZd-dIx8'
    outfit_data_url = 'https://drive.google.com/uc?id=1HFKUqBe5oMizU0lxy6sQE5Er1w9x-cC4'
    user_data_url = 'https://drive.google.com/uc?id=1G_1SV9H7fQMPPJOBmZpCnCkgifSsb9Ar'

    data_file_name = 'alibaba_ifashion'

    uncompressed_item_file_name = 'item_data.txt'
    uncompressed_outfit_file_name = 'outfit_data.txt'
    uncompressed_user_file_name = 'user_data.txt'

    # item_file_name = 'item_data.txt'
    # outfit_file_name = 'outfit_data.txt'
    # user_file_name = 'user_data.txt'
    REQUIRED_FILES = [uncompressed_item_file_name, uncompressed_outfit_file_name, uncompressed_user_file_name]

    def __init__(self, folder=None):
        super().__init__(pd.DataFrame(), user=True, item=True, rating='implicit')

        self.dataset_name = 'alibaba_ifashion'
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

        # download item data
        item_data_file_name = 'item_data.txt.zip'
        item_data_path = os.path.join(self._raw_folder, item_data_file_name)
        gdown.download(self.item_data_url, item_data_path, quiet=False)
        print(f'Alibaba iFashion item data downloaded at \'{item_data_path}\'')

        # download outfit data
        outfit_data_file_name = 'outfit_data.txt.zip'
        outfit_data_path = os.path.join(self._raw_folder, outfit_data_file_name)
        gdown.download(self.outfit_data_url, outfit_data_path, quiet=False)
        print(f'Alibaba iFashion outfit data downloaded at \'{outfit_data_path}\'')

        # download user data
        user_data_file_name = 'user_data.txt.zip'
        user_data_path = os.path.join(self._raw_folder, user_data_file_name)
        gdown.download(self.user_data_url, user_data_path, quiet=False)
        print(f'Alibaba iFashion user data downloaded at \'{user_data_path}\'')

        return item_data_path, outfit_data_path, user_data_path


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
