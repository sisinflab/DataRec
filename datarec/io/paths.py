import os
from . import PROJECT_DIRECTORY

DATA_DIR = os.path.join(PROJECT_DIRECTORY, 'data')
RESULT_DIR = os.path.join(PROJECT_DIRECTORY, 'results')
CONFIG_DIR = os.path.join(PROJECT_DIRECTORY, 'config_files')
RAW_DATA_FOLDER = 'raw'
PROCESSED_DATA_FOLDER = 'processed'
DATASET_NAME = 'dataset.tsv'


def dataset_directory(dataset_name: str, must_exist=False) -> str:
    """
    Given the dataset name returns the dataset directory
    @param dataset_name: name of the dataset
    @param must_exist: flag for forcing to check if the folder exists
    @return: the path of the directory containing the dataset data
    """
    dataset_dir = os.path.join(DATA_DIR, dataset_name)
    if must_exist and not os.path.exists(dataset_dir):
        raise FileNotFoundError(f'Directory at {dataset_dir} not found. Please, check that dataset directory exists')
    return os.path.abspath(dataset_dir)


def dataset_raw_directory(dataset_name: str) -> str:
    """
    Given the dataset name returns the directory containing the raw data of the dataset
    @param dataset_name: name of the dataset
    @return: the path of the directory containing the dataset data
    """
    return os.path.join(dataset_directory(dataset_name), RAW_DATA_FOLDER)


def dataset_processed_directory(dataset_name: str) -> str:
    """
    Given the dataset name returns the directory containing the processed data of the dataset
    @param dataset_name: name of the dataset
    @return: the path of the directory containing the dataset data
    """
    return os.path.join(dataset_directory(dataset_name), PROCESSED_DATA_FOLDER)


def dataset_filepath(dataset_name: str) -> str:
    """
    Given the dataset name returns the path of the dataset data
    @param dataset_name: name of the dataset
    @return: the path of the dataset data
    """
    return os.path.join(dataset_directory(dataset_name), DATASET_NAME)
