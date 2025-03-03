import os
from datarec.data.dataset import DataRec
from datarec.io.paths import dataset_directory, dataset_raw_directory, RAW_DATA_FOLDER
from datarec.datasets.download import download_file, decompress_zip_file
from datarec.data.utils import verify_checksum


class MovieLens1M(DataRec):
    url = 'https://files.grouplens.org/datasets/movielens/ml-1m.zip'
    data_file_name = os.path.basename(url)
    movies_file_name = 'movies.dat'
    ratings_file_name = 'ratings.dat'
    users_file_name = 'users.dat'
    REQUIRED_FILES = [os.path.join('ml-1m', p) for p in [movies_file_name, ratings_file_name, users_file_name]]
    CHECKSUM = "c4d9eecfca2ab87c1945afe126590906"

    def __init__(self, folder=None):
        super().__init__(None)

        self.dataset_name = 'movielens'
        self.version_name = '1m'

        self._data_folder = folder if folder \
            else dataset_directory(self.dataset_name)
        self._raw_folder = os.path.abspath(os.path.join(self._data_folder, self.version_name, RAW_DATA_FOLDER)) if folder \
            else os.path.join(dataset_raw_directory(self.dataset_name), self.version_name)

        self.return_type = None

        # check if the required files have been already downloaded
        file_path = self.required_files()

        if file_path is None:
            file_path = self.download()
            file_path = self.decompress(file_path)

        print(f'files: {file_path}')
        # the order of tha paths is the same of REQUIRED_PATHS
        movies_file_path, ratings_file_path, users_file_path = file_path

        self.process(ratings_file_path)

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
        download_file(self.url, file_path)

        return file_path

    def process(self, file_path):
        """
        Process the downloaded files and save the processed dataset
        :param train_path: path to the training dataset
        :param test_path: path to the test dataset
        :return: path of the processed dataset
        """

        from datarec.io import read_tabular

        dataset = read_tabular(file_path, sep='::', user_col=0, item_col=1, rating_col=2, timestamp_col=3, header=None)
        self.data = dataset
