import os
from datarec.data.dataset import DataRec
from datarec.io.paths import dataset_directory, dataset_raw_directory, RAW_DATA_FOLDER
from datarec.datasets.download import download_file, decompress_zip_file
from datarec.data.utils import verify_checksum


class LastFM2011(DataRec):
    """
    This dataset is derived from the file user_artists.dat

    From the original readme file:
       * user_artists.dat

        This file contains the artists listened by each user.

        It also provides a listening count for each [user, artist] pair.

    This dataset is interpreted an implicit dataset and the information about the listening counts is dropped
    """

    url = 'https://files.grouplens.org/datasets/hetrec2011/hetrec2011-lastfm-2k.zip'
    data_file_name = os.path.basename(url)
    decompressed_data_file_name = data_file_name.replace('.zip', '')

    user_artists_file_name = 'user_artists.dat'
    tags_file_name = 'tags.dat'
    artists_file_name = 'artists.dat'
    user_taggedartists_file_name = 'user_taggedartists.dat'
    user_taggedartists_timestamp_file_name = 'user_taggedartists-timestamps.dat'
    user_friends_file_name = 'user_friends.dat'

    REQUIRED_FILES = [p for p in
                      [user_friends_file_name, user_taggedartists_file_name, user_taggedartists_timestamp_file_name,
                       artists_file_name, tags_file_name, user_artists_file_name]]
    # REQUIRED_FILES = [os.path.join('ml-1m', p) for p in [movies_file_name, ratings_file_name, users_file_name]]
    CHECKSUM = '296d61afe4e8632b173fc2dd3be20ce2'

    def __init__(self, folder=None):
        super().__init__(None)

        self.dataset_name = 'lastfm'
        self.version_name = '2011'

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

        user_friends_file_path, user_taggedartists_file_path, user_taggedartists_timestamp_file_path, artists_file_path, tags_file_path, user_artists_file_path = file_path
        self.process(user_artists_file_path)

    def required_files(self):
        # compressed data file
        file_path = os.path.join(self._raw_folder, self.data_file_name)
        paths = [os.path.join(self._raw_folder, f) for f in self.REQUIRED_FILES]

        if all([os.path.exists(p) for p in paths]):
            return paths
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
        file_name = os.path.basename(self.url)
        file_path = os.path.join(self._raw_folder, file_name)
        download_file(self.url, file_path)

        return file_path

    def process(self, file_path):

        from datarec.io import read_tabular
        dataset = read_tabular(file_path, sep='\t',
                               user_col='userID', item_col='artistID',
                               rating_col='weight',
                               header=0)
        self.data = dataset
