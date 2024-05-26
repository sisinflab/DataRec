import os
import pandas as pd
from datarec.data.dataset import DataRec
from datarec.io.paths import dataset_directory, dataset_raw_directory, RAW_DATA_FOLDER
from datarec.datasets.download import download_url
from datarec.data.format import data_from_inline

from datarec.datasets.alibaba_ifashion.alibaba_ifashion_v1 import AlibabaIFashion_V1


class AlibabaIFashion:
    latest_version = 'v1'
    def __new__(self, version: str = 'latest', **kwargs):

        versions = {'v1': AlibabaIFashion_V1}
        if version == 'latest':
            version = self.latest_version
        if version in versions:
            return versions[version]()
        else:
            raise ValueError("Alibaba iFashion: Unsupported version")
