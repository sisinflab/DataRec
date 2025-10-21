import os
from dataclasses import dataclass
from typing import Optional, List
from datarec.data.utils import verify_checksum
import requests
from datarec.io.paths import registry_version_filepath
import yaml


@dataclass
class Source:
    url: str
    checksum: str = None
    checksum_algorithm: str = "sha256"
    filename: Optional[str] = None
    archive: Optional[str] = None
    inner_paths: Optional[List[str]] = None
    output_folder: str = None
    downloadable: bool = False

    def path(self, output_folder=None) -> str:
        if output_folder is None:
            if self.output_folder is None:
                raise ValueError("Must specify an output folder")
            output_folder = self.output_folder
        return os.path.join(output_folder, self.filename)

    def verify_checksum(self, output_folder=None) -> None:
        print(f'{self.filename}: verifying checksum')
        if output_folder is None:
            output_folder = self.output_folder
        verify_checksum(self.path(output_folder), self.checksum)

    def download(self) -> None:
        pass


class GitHubSource(Source):

    def download(self, output_folder=None) -> str:
        if not self.downloadable:
            return self.path(output_folder)

        if output_folder is None:
            output_folder = self.output_folder

        if self.filename is None:
            raise RuntimeError(f"No filename provided")

        output_path = os.path.join(output_folder, self.filename)

        if not os.path.exists(output_folder):
            os.makedirs(output_folder)

        if os.path.exists(output_path):
            print(f"{self.filename}: File already exists, skipping download")
            return output_path

        response = requests.get(self.url)
        response.raise_for_status()

        with open(output_path, "wb") as f:
            f.write(response.content)
        print(f'{self.filename} downloaded from {self.url}')
        return output_path

class HttpSource(Source):

    def download(self, output_folder=None) -> str:

        if output_folder is None:
            output_folder = self.output_folder

        if self.filename is None:
            raise RuntimeError(f"No filename provided")

        output_path = os.path.join(output_folder, self.filename)

        if not os.path.exists(output_folder):
            os.makedirs(output_folder)

        if os.path.exists(output_path):
            print(f"{self.filename}: File already exists, skipping download")
            return output_path

        response = requests.get(self.url)
        response.raise_for_status()

        with open(output_path, "wb") as f:
            f.write(response.content)
        print(f'{self.filename} downloaded from {self.url}')
        return output_path

SOURCE_TYPES = {
    'Source': Source,
    'GitHubSource': GitHubSource,
    'HttpSource': HttpSource
}

def load_dataset_config(dataset_name:str, dataset_version:str)->dict:
    """
    Given the dataset name returns the path of the dataset configuration file in the dataset registry
    Args:
        dataset_name (str): name of the dataset
        dataset_version (str): version of the dataset
    Returns:
        (dict): dataset configuration
    """
    config_path = registry_version_filepath(dataset_name, dataset_version)
    with open(config_path, "r") as f:
        config = yaml.safe_load(f)
    assert dataset_version == config['version'], \
        "Dataset version must be the same as the one in the config file."
    return config

def set_sources(config:dict) -> dict[str, Source]:
    """
    Given a dataset configuration, return a new dataset configuration
    Args:
        config (dict): dataset configuration
    Returns:
        (dict): a dictionary containing dataset sources objects
    """
    sources = dict()
    for source_name, raw_source in config['sources'].items():
        source_type = SOURCE_TYPES[raw_source['source_type']]
        source = source_type(**raw_source['args'])
        sources[source_name] = source
    return sources
