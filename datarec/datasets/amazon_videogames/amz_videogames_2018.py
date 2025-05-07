import os
from datarec.data.dataset import DataRec
from datarec.io.paths import dataset_directory, dataset_raw_directory, RAW_DATA_FOLDER
from datarec.datasets.download import download_file
from datarec.data.utils import verify_checksum


class AMZ_VideoGames_2018(DataRec):
    url = 'https://mcauleylab.ucsd.edu/public_datasets/data/amazon_v2/categoryFilesSmall/Video_Games.csv'
    data_file_name = os.path.basename(url)
    decompressed_data_file_name = data_file_name
    CHECKSUM = 'feecdbf6bf247e54d2a572e2be503515'

    def __init__(self, folder=None):
        super().__init__(None)

        self.dataset_name = 'amazon_video_games'
        self.version_name = '2018'

        self._data_folder = folder if folder \
            else dataset_directory(self.dataset_name)
        self._raw_folder = os.path.abspath(os.path.join(self._data_folder, self.version_name, RAW_DATA_FOLDER)) if folder \
            else os.path.join(dataset_raw_directory(self.dataset_name), self.version_name)
        # check if the required files have been already downloaded
        file_path = self.required_files()

        if file_path is None:
            file_path = self.download()
            file_path = self.decompress(file_path)

        print(f'files: {file_path}')

        self.process(file_path)

    def required_files(self):
        # compressed data file
        file_path = os.path.join(self._raw_folder, self.data_file_name)
        uncompressed_file_path = os.path.join(self._raw_folder, self.decompressed_data_file_name)

        # check if the file is there
        if os.path.exists(uncompressed_file_path):
            return uncompressed_file_path
        # check if the compressed file is there
        elif os.path.exists(file_path):
            return self.decompress(file_path)
        else:
            return None

    def decompress(self, path):
        return path

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
        download_file(self.url, file_path, size=115388622)

        return file_path

    def process(self, file_path):
        """
        Process the downloaded files and save the processed dataset
        :param file_path: path to the dataset
        :return: path of the processed dataset
        """
        verify_checksum(file_path, self.CHECKSUM)

        from datarec.io import read_tabular

        dataset = read_tabular(file_path, sep=',',
                               user_col=0, item_col=1,
                               rating_col=2, timestamp_col=3,
                               header=None)
        self.data = dataset
