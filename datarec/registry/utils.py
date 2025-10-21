from datarec.io.paths import REGISTRY_DATASETS_FOLDER
import os
from typing import List


def available_datasets()->List[str]:
    """
    Return a list of available built-in datasets
    Returns:
        List[str]: list of built-in datasets
    """
    return [d.replace('.yml', '') for d in os.listdir(REGISTRY_DATASETS_FOLDER)]

def print_available_datasets()->None:
    """
    Prints the list of available built-in datasets
    Returns:
        None
    """
    print("""
DataRec built-in datasets:
- """+'\n - '.join(available_datasets()))
