import os
from datarec.data.dataset import DataRec
from datarec.io.paths import dataset_directory, dataset_raw_directory, RAW_DATA_FOLDER
from datarec.datasets.download import download_file, decompress_gz
from datarec.data.utils import verify_checksum


class Epinions_V1(DataRec):
    url = 'https://snap.stanford.edu/data/soc-Epinions1.txt.gz'
    data_file_name = os.path.basename(url)
    decompressed_file_name = data_file_name.replace('.gz', '')
    REQUIRED_FILES = [decompressed_file_name]
    CHECKSUM = '8df7433d4486ba68eb25e623feacff04'

    def __init__(self, folder=None):
        super().__init__(None)

        self.dataset_name = 'epinions'
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
        decompressed_file = os.path.join(self._raw_folder, self.decompressed_file_name)
        decompress_gz(path, decompressed_file)
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
        :param file_path: path to the dataset
        :return: path of the processed dataset
        """

        from datarec.io import read_tabular

        dataset = read_tabular(file_path, sep='\t',
                               user_col=0, item_col=1,
                               header=None, skiprows=4)

        self.data = dataset
