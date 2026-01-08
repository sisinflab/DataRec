import os
from . import PROJECT_DIRECTORY
from datarec.io.cache import cache_dir


DATASETS_CLASSES_DIR = os.path.join(PROJECT_DIRECTORY, 'datasets')
RESULT_DIR = os.path.join(PROJECT_DIRECTORY, 'results')
CONFIG_DIR = os.path.join(PROJECT_DIRECTORY, 'config_files')
RAW_DATA_FOLDER = 'resource'
PROCESSED_DATA_FOLDER = 'processed'
DATASET_NAME = 'dataset.tsv'
DOCS_FOLDER = os.path.join(PROJECT_DIRECTORY, 'docs')
REGISTRY_FOLDER = os.path.join(PROJECT_DIRECTORY, 'datarec', 'registry')
REGISTRY_DATASETS_FOLDER = os.path.join(REGISTRY_FOLDER, 'datasets')
REGISTRY_VERSIONS_FOLDER = os.path.join(REGISTRY_FOLDER, 'versions')
REGISTRY_METRICS_FOLDER = os.path.join(REGISTRY_FOLDER, "metrics")


def dataset_directory(dataset_name: str, must_exist=False) -> str:
    """
    Given the dataset name returns the dataset directory
    Args:
        dataset_name (str): name of the dataset
        must_exist (bool): flag for forcing to check if the folder exists

    Returns:
        (str): the path of the directory containing the dataset data
    """
    dataset_dir = os.path.join(cache_dir(), dataset_name)
    if must_exist and not os.path.exists(dataset_dir):
        raise FileNotFoundError(f'Directory at {dataset_dir} not found. Please, check that dataset directory exists')
    return os.path.abspath(dataset_dir)


def dataset_version_directory(dataset_name: str, dataset_version: str, must_exist=False) -> str:
    """
    Given the dataset name and its version returns the dataset directory
    Args:
        dataset_name (str): name of the dataset
        version_name (str): version of the dataset
        must_exist (bool): flag for forcing to check if the folder exists

    Returns:
        (str): the path of the directory containing the dataset data
    """
    dataset_dir = os.path.join(dataset_directory(dataset_name), dataset_version)
    if must_exist and not os.path.exists(dataset_dir):
        raise FileNotFoundError(f'Directory at {dataset_dir} not found. Please, check that dataset directory exists')
    return os.path.abspath(dataset_dir)

def dataset_raw_directory(dataset_name: str, dataset_version: str=None) -> str:
    """
    Given the dataset name returns the directory containing the raw data of the dataset
    Args:
        dataset_name (str): name of the dataset
        dataset_version (str): version of the dataset
    Returns:
        (str): the path of the directory containing the raw data of the dataset
    """
    if dataset_version:
        return os.path.join(dataset_version_directory(dataset_name, dataset_version), RAW_DATA_FOLDER)
    return os.path.join(dataset_directory(dataset_name), RAW_DATA_FOLDER)

def dataset_processed_directory(dataset_name: str) -> str:
    """
    Given the dataset name returns the directory containing the processed data of the dataset
    Args:
        dataset_name (str): name of the dataset

    Returns:
        (str): the path of the directory containing the processed data of the dataset
    """
    return os.path.join(dataset_directory(dataset_name), PROCESSED_DATA_FOLDER)

def dataset_filepath(dataset_name: str) -> str:
    """
    Given the dataset name returns the path of the dataset data
    Args:
        dataset_name (str): name of the dataset

    Returns:
        (str): the path of the dataset data
    """
    return os.path.join(dataset_directory(dataset_name), DATASET_NAME)

def registry_dataset_filepath(dataset_name: str) -> str:
    """
    Given the dataset name returns the path of the dataset configuration file in the dataset registry
    Args:
        dataset_name (str): name of the dataset
    Returns:
        (str): the path of the dataset configuration file
    """
    return os.path.join(REGISTRY_DATASETS_FOLDER, dataset_name) + '.yml'

def registry_version_filepath(dataset_name: str, dataset_version: str) -> str:
    """
    Given the dataset name returns the path of the dataset configuration file in the dataset registry
    Args:
        dataset_name (str): name of the dataset
        dataset_version (str): version of the dataset
    Returns:
        (str): the path of the dataset configuration file
    """
    return os.path.join(REGISTRY_VERSIONS_FOLDER, dataset_name+'_'+dataset_version) + '.yml'


def registry_metrics_filepath(dataset_name: str, dataset_version: str) -> str:
    """
    Given dataset name and version, return the path of the precomputed metrics file
    in the registry metrics folder.
    """
    return os.path.join(REGISTRY_METRICS_FOLDER, f"{dataset_name}_{dataset_version}.yml")


def pickle_version_filepath(dataset_name: str, dataset_version: str) -> str:
    """
    Given the dataset name and version returns the path of the pickled version of the dataset
    Args:
        dataset_name (str): name of the dataset
        dataset_version (str): version of the dataset
    Returns:
        (str): the path of the pickled version of the dataset
    """
    return os.path.join(dataset_version_directory(dataset_name=dataset_name, dataset_version=dataset_version), dataset_name+'_'+dataset_version) + '.pkl'
