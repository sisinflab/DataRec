import os
import pandas as pd
from datarec.data.dataset import DataRec
from datarec.io.paths import dataset_directory, dataset_raw_directory, RAW_DATA_FOLDER
from datarec.datasets.download import download_browser, decompress_tar_file, decompress_zip_file
from datarec.data.utils import verify_checksum


class Yelp_v1(DataRec):
    website_url = 'https://www.yelp.com/dataset'
    url = 'https://business.yelp.com/external-assets/files/Yelp-JSON.zip'
    data_file_name = 'Yelp-JSON.zip'
    data_tar_file_name = 'yelp_dataset.tar'
    subdirectory_name = 'Yelp JSON'  # once extracted the zip file
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
    CHECKSUM_ZIP = 'b0c36fe2d00a52d8de44fa3b2513c9d2'
    CHECKSUM_TAR = '0bc8cc1481ccbbd140d2aba2909a928a'

    def __init__(self, folder=None):
        super().__init__(None)

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
            file_path = self.decompress(file_path) ## all files

        business_file_path, checkin_file_path, review_file_path, tip_file_path, user_file_path = file_path

        print(f'found {file_path}')
        self.process(review_file_path)

    def required_files(self):
        # compressed data file
        file_path = os.path.join(self._raw_folder, self.subdirectory_name)

        # check if the file is there
        paths = [os.path.join(self._raw_folder, self.subdirectory_name, f) for f in self.REQUIRED_FILES]
        if all([os.path.exists(p) for p in paths]):
            return paths
        # check if the compressed file is there
        elif os.path.exists(file_path):
            return self.decompress(file_path)
        else:
            return None

    def decompress(self, path):
        verify_checksum(path, self.CHECKSUM_ZIP)
        decompress_zip_file(path, self._raw_folder)


        tar_file_path = os.path.join(self._raw_folder, self.subdirectory_name, self.data_tar_file_name)
        verify_checksum(tar_file_path, self.CHECKSUM_TAR)

        decompress_tar_file(tar_file_path, os.path.join(self._raw_folder, self.subdirectory_name))
        files = [os.path.join(self._raw_folder, self.subdirectory_name, f) for f in self.REQUIRED_FILES]
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

        file_name = os.path.basename(self.url)
        file_path = os.path.join(self._raw_folder, file_name)
        if not os.path.exists(file_path):
            download_browser(self.url, file_path)
        return file_path

    def process(self, path):
        from datarec.io import read_json

        user_field = 'user_id'
        item_field = 'business_id'
        rating_field = 'stars'
        date_field = 'date'  # format: YYYY-MM-DD , e.g.: 2016-03-09
        dataset = read_json(path, user_field=user_field, item_field=item_field, rating_field=rating_field, timestamp_field=date_field)
        timestamps = pd.Series(dataset.data[date_field].apply(lambda x: x.timestamp()).values,
                               index=dataset.data.index, dtype='float64')
        dataset.data.loc[:, date_field] = timestamps
        self.data = dataset
