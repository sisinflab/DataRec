import os
from . import PROJECT_DIRECTORY
from pathlib import Path
from appdirs import user_cache_dir


def get_cache_dir(app_name="datarec", app_author="sisinflab"):
    """
    Returns the appropriate cache directory for the library, creating it if it doesn't exist.
    Respects the DATAREC_CACHE_DIR environment variable if set.

    Returns:
        Path: The absolute path to the cache directory.
    """
    env_override = os.getenv("DATAREC_CACHE_DIR")
    path = Path(env_override) if env_override else Path(user_cache_dir(app_name, app_author))
    path.mkdir(parents=True, exist_ok=True)
    return path


DATA_DIR = get_cache_dir()
RESULT_DIR = os.path.join(PROJECT_DIRECTORY, 'results')
CONFIG_DIR = os.path.join(PROJECT_DIRECTORY, 'config_files')
RAW_DATA_FOLDER = 'raw'
PROCESSED_DATA_FOLDER = 'processed'
DATASET_NAME = 'dataset.tsv'


def dataset_directory(dataset_name: str, must_exist=False) -> str:
    """
    Given the dataset name returns the dataset directory
    Args:
        dataset_name (str): name of the dataset
        must_exist (bool): flag for forcing to check if the folder exists

    Returns:
        (str): the path of the directory containing the dataset data
    """
    dataset_dir = os.path.join(DATA_DIR, dataset_name)
    if must_exist and not os.path.exists(dataset_dir):
        raise FileNotFoundError(f'Directory at {dataset_dir} not found. Please, check that dataset directory exists')
    return os.path.abspath(dataset_dir)


def dataset_raw_directory(dataset_name: str) -> str:
    """
    Given the dataset name returns the directory containing the raw data of the dataset
    Args:
        dataset_name (str): name of the dataset

    Returns:
        (str): the path of the directory containing the raw data of the dataset
    """
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
