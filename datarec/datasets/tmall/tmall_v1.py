import os
from datarec.data.dataset import DataRec
from datarec.io.paths import dataset_directory, dataset_raw_directory, RAW_DATA_FOLDER
from datarec.datasets.download import decompress_zip_file
from datarec.data.utils import verify_checksum


class Tmall_v1(DataRec):
    website_url = 'https://tianchi.aliyun.com/dataset/dataDetail?dataId=53'
    data_file_name = 'IJCAI16_data.zip'
    uncompressed_user_item_file_name = 'ijcai2016_taobao.csv'
    REQUIRED_FILES = [uncompressed_user_item_file_name]
    CHECKSUM = 'c4f4f0b8860984723652d2e91bcddc01'

    def __init__(self, folder=None):
        super().__init__(None)

        self.dataset_name = 'tmall'
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

        print(f'found {file_path}')
        self.process(file_path[0])

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
        decompress_zip_file(input_file=path, output_dir=self._raw_folder)
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

        print(f'\nThis version of Tmall dataset requires the user to manually download it.\n'
              f'Please, go to {self.website_url} on your browser, register, and click on the download button.\n'
              f'Then, move or copy \'{self.data_file_name}\' in the following directory:\n'
              f'\'{self._raw_folder}\'\n'
              f'Please, do not change the original file name and try again.')
        file_path = os.path.join(self._raw_folder, self.data_file_name)
        return file_path

    def process(self, file_path):

        from datarec.io import read_tabular

        dataset = read_tabular(file_path, sep=',', user_col='use_ID', item_col='ite_ID', rating_col='act_ID', timestamp_col='time', header=0)
        self.data = dataset
