import os
import pandas as pd
from datarec.data.dataset import DataRec
from datarec.io.paths import dataset_directory, dataset_raw_directory, RAW_DATA_FOLDER
from datarec.datasets.download import download_url
from datarec.data.format import data_from_inline

from datarec.datasets.gowalla.gowalla_v1 import Gowalla_V1


class Gowalla:
    latest_version = 'v1'
    def __new__(self, version: str = 'latest', **kwargs):

        versions = {'v1': Gowalla_V1}
        if version == 'latest':
            version = self.latest_version
        if version in versions:
            return versions[version]()
        else:
            raise ValueError("Gowalla: Unsupported version")
