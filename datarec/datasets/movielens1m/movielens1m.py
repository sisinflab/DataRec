import os
import pandas as pd
from datarec.data.dataset import DataRec
from datarec.io.paths import dataset_directory, dataset_raw_directory, RAW_DATA_FOLDER
from datarec.datasets.download import download_url
from datarec.data.format import data_from_inline

from datarec.datasets.movielens1m.movielens1m_v1 import MovieLens1M_V1


class MovieLens1M:
    latest_version = 'v1'

    def __new__(cls, version: str = 'latest', **kwargs) -> DataRec:
        versions = {'v1': MovieLens1M_V1}
        if version == 'latest':
            version = cls.latest_version
        if version in versions:
            return versions[version]()
        else:
            raise ValueError("MovieLens 1M: Unsupported version")
