from datarec.data.dataset import DataRec
from datarec.data.datarec_builder import BaseDataRecBuilder
from datarec.io import read_tabular
from datarec.data.source import load_dataset_config, set_sources
import os

class Ambar2024(BaseDataRecBuilder):
    """
    Builder class for the AMBAR 2024 dataset.

    The AMBAR 2024 dataset contains music recommendation data, including ratings,
    artists, tracks, and user information. This class handles dataset downloading,
    checksum validation, and loading into a DataRec object.
    """
    dataset_name = 'ambar'
    version = '2024'

    def __init__(self, folder=None):
        """
        Initializes the builder.

        This constructor sets up the necessary paths for caching the dataset.

        Args:
            folder (str, optional): A custom directory to store the dataset files.
                If None, a default user cache directory is used. Defaults to None.
        """

        self.config = load_dataset_config(dataset_name=self.dataset_name,
                                          dataset_version=self.version)
        self.sources_info = self.config['sources_info']
        self.sources = set_sources(self.config)
        self.output_folder = self.find_output_folder(folder=folder)
        for source in self.sources.values():
            source.output_folder = self.output_folder

    def prepare(self):
        """
        Ensures all required raw files are downloaded and decompressed.

        This method checks for the existence of the required files. If they are
        not found, it triggers the download and decompression process.
        """
        self.download()

    def download(self):
        """
        Downloads the raw dataset file.
        Returns:
            (str): The local file path to the downloaded file.
        """
        for s in self.config['sources_info']['required']:
            source = self.sources[s]
            if not os.path.exists(source.path()):
                s.download()
            source.verify_checksum()

    def download_content(self, ctype:str='all') -> None:
        """
        Downloads supplementary files containing content information.
        Args:
            ctype (str, optional): Content type to download.
            When set to 'all' all the possible content types are downloaded.
            Defaults to 'all'.
        Returns:
            (None): None
        """
        ctypes = self.config['sources_info']['content']
        assert ctype in ctypes or ctype == 'all'
        if ctype == 'all':
            contents = [self.sources[ct] for ct in ctypes]
        else:
            contents = [[self.sources[ctype]]]
        for source in contents:
            source.download()
            source.verify_checksum()


    def load(self) -> DataRec:
        """
        Loads the prepared `ratings.dat` file into a DataRec object.

        Returns:
            (DataRec): A DataRec object containing the user-item interactions.
        """
        ratings_source_name = self.config['sources_info']['ratings']
        ratings = self.sources[ratings_source_name]
        ratings_path = ratings.path()
        dataset = read_tabular(ratings_path, sep=',', user_col='user_id', item_col='track_id', rating_col='rating',
                               header=0)
        return DataRec(dataset, dataset_name=self.dataset_name, version_name=self.version)
