import importlib
from importlib import resources
import yaml
from types import ModuleType
from datarec.io.paths import DOCS_FOLDER
import os

def append_line(path: str, line: str)->None:
    """
    Append a line to the end of the path.
    Args:
        path (str): The path to append line to.
        line (str): The line to append.
    Returns:
        None
    """
    with open(path, "r") as file:
        text = file.read()
    new_line = text.endswith('\n')
    with open(path, "a") as file:
        if not new_line:
            line = "\n"+line
        file.write(line)

def retrieve_module_dataset_by_name(dataset_name)->ModuleType:
    """
    Retrieve the dataset python module by name
    Args:
        dataset_name (str): name of the dataset
    Returns:
        class 'module': module object
    """
    module_name = f"datarec.datasets.{dataset_name}"
    module = importlib.import_module(module_name)
    return module


def add_dataset(dataset_name)->str:
    """
    Add a dataset to the datasets_nav.md documentation file
    Args:
        dataset_name (str): name of the dataset
    Returns:
        str: path to the datasets_nav.md documentation file
    """
    mod = retrieve_module_dataset_by_name(dataset_name)
    with resources.files(mod).joinpath(f"{dataset_name}.yml").open("r") as f:
        config = yaml.safe_load(f)
    dataset_name = config['dataset_name']
    source = config['source']
    dataset_nav_path = os.path.join(DOCS_FOLDER, 'src', 'datasets_nav.md')
    row=f"| {dataset_name} | {source} |"
    append_line(dataset_nav_path, row)
    print(f'Added new row to \'{dataset_nav_path}\'.\nInserted row: {row}')
    return dataset_nav_path

