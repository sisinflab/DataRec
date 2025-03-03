import os
import pandas as pd
from datarec.data.dataset import DataRec
from datarec.io.paths import dataset_directory, dataset_raw_directory, RAW_DATA_FOLDER
from datarec.datasets.download import download_file, decompress_zip_file
from datarec.data.utils import verify_checksum


class Ciao_V1(DataRec):
    url = 'https://guoguibing.github.io/librec/datasets/CiaoDVD.zip'
    data_file_name = os.path.basename(url)
    movie_file_name = 'movie-ratings.txt'
    review_file_name = 'review-ratings.txt'
    trusts_file_name = 'trusts.txt'
    REQUIRED_FILES = [movie_file_name, review_file_name, trusts_file_name]
    CHECKSUM = '43a39e068e3fc494a7f7f7581293e2c2'


    def __init__(self, folder=None):
        super().__init__(None)

        self.dataset_name = 'ciaoDVD'
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

        rating_file_path = os.path.abspath(os.path.join(self._raw_folder, self.movie_file_name))
        self.process(rating_file_path)

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
        verify_checksum(path, self.CHECKSUM)

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
        download_file(self.url, file_path, size=5814757)

        return file_path

    def process(self, path) -> None:

        from datarec.io import read_tabular

        user_col = 0
        item_col = 1
        rating_col = 4
        timestamp_col = 5
        dataset = read_tabular(path, sep=',', user_col=user_col, item_col=item_col, rating_col=rating_col, timestamp_col=timestamp_col, header=None)
        # timestamps = pd.Series(dataset.data[timestamp_col].apply(lambda x: x.timestamp()).values,
        #                        index=dataset.data.index, dtype='float64')

        # Convert the date strings to datetime objects using the specified format
        dataset.data[timestamp_col] = pd.to_datetime(dataset.data[timestamp_col], format='%Y-%m-%d')

        # Now extract the Unix timestamps (in seconds)
        timestamps = pd.Series(dataset.data[timestamp_col].apply(lambda x: x.timestamp()).values,
                               index=dataset.data.index, dtype='float64')
        dataset.data[timestamp_col] = timestamps

        self.data = dataset
