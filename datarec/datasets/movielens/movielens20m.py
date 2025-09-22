"""Builder class for the MovieLens 20M dataset."""
import os
from datarec.data.dataset import DataRec
from datarec.io.paths import dataset_directory, dataset_raw_directory, RAW_DATA_FOLDER
from datarec.datasets.download import download_file, decompress_zip_file
from datarec.data.utils import verify_checksum


class MovieLens20M(DataRec):
    """
    Builder class for the MovieLens 20M dataset.

    This dataset contains 20 million ratings. It is not typically instantiated directly
    but is called by the `MovieLens` entry point class.

    This loader specifically processes the `ratings.csv` file from the archive.

    Attributes:
        url (str): The URL from which the raw dataset is downloaded.
        CHECKSUM (str): The MD5 checksum to verify the integrity of the downloaded file.
        REQUIRED_FILES (list): A list of all files expected after decompression.
    """
    url = 'https://files.grouplens.org/datasets/movielens/ml-20m.zip'
    data_file_name = os.path.basename(url)
    genome_scores_file_name = 'genome-scores.csv'
    genome_tags_file_name = 'genome-tags.csv'
    links_file_name = 'links.csv'
    movies_file_name = 'movies.csv'
    ratings_file_name = 'ratings.csv'
    tags_file_name = 'tags.csv'
    REQUIRED_FILES = [os.path.join('ml-20m', p) for p in [genome_scores_file_name,
                                                          genome_tags_file_name,
                                                          links_file_name,
                                                          movies_file_name,
                                                          ratings_file_name,
                                                          tags_file_name]]
    CHECKSUM = "cd245b17a1ae2cc31bb14903e1204af3"

    def __init__(self, folder=None):
        """
        Initializes the builder and orchestrates the data preparation workflow.

        This constructor sets up the necessary paths and automatically triggers
        the download, verification, and processing steps if the data is not
        already present in the specified cache directory.

        Args:
            folder (str, optional): A custom directory to store the dataset files.
                If None, a default user cache directory is used. Defaults to None.
        """
        super().__init__(None)

        self.dataset_name = 'MovieLens'
        self.version_name = '20m'

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
        genome_scores_file_path, genome_tags_file_path, links_file_path, movies_file_path, ratings_file_path,\
            tags_file_path = file_path

        self.process(ratings_file_path)


    def required_files(self):
        """
        Checks for the presence of all required decompressed data files.

        Returns:
            (list or None): A list of paths to the required data files if they
                exist or can be created by decompression. Otherwise, returns None.
        """
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
        """
        Decompresses the downloaded archive after verifying its checksum.

        Args:
            path (str): The file path of the compressed archive.

        Returns:
            (list or None): A list of paths to the decompressed files if successful,
                otherwise None.
        """
        verify_checksum(path, self.CHECKSUM)

        # decompress downloaded file
        decompress_zip_file(path, self._raw_folder)
        files = [os.path.join(self._raw_folder, f) for f in self.REQUIRED_FILES]
        if all([os.path.exists(f) for f in files]):
            return [os.path.join(self._raw_folder, f) for f in files]
        return None

    def download(self) -> str:
        """
        Downloads the raw dataset compressed archive.

        Returns:
            (str): The local file path to the downloaded archive.
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
        Processes the raw  file and loads it into the class.

        This method reads the file, which includes a header row, and maps
        the columns to the standard user, item, rating, and timestamp fields.

        Args:
            file_path (str): The path to the raw  file.

        Returns:
            (None): This method assigns the processed data to `self.data` directly.
        """

        from datarec.io import read_tabular

        dataset = read_tabular(file_path, sep=',',
                               user_col='userId', item_col='movieId', rating_col='rating', timestamp_col='timestamp',
                               header=0)
        self.data = dataset
