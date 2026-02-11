from typing import Union
from datarec.io.rawdata import RawData
import os

def as_rawdata(data: Union["RawData", "DataRec"]) -> RawData:
    """
    Normalize input to RawData.

    Accepts:
    - RawData
    - DataRec (converted via `.to_rawdata()`)

    Returns:
        RawData

    Raises:
        TypeError: if the input cannot be converted to RawData.
    """
    if isinstance(data, RawData):
        return data

    if hasattr(data, "to_rawdata"):
        raw = data.to_rawdata()
        if isinstance(raw, RawData):
            return raw

    raise TypeError(
        "data must be a RawData or a DataRec-like object exposing `.to_rawdata()`."
    )


def read_char_file(dataset_name: str, dataset_version: str) -> dict:
    """
    Reads the characteristics file for a given dataset and version.

    Args:
        dataset_name (str): Name of the dataset.
        dataset_version (str): Version of the dataset.

    Returns:
        dict: Characteristics data.
    """
    from datarec.io.paths import registry_metrics_filepath
    import yaml

    char_file_path = registry_metrics_filepath(dataset_name, dataset_version)
    print(char_file_path)
    if not os.path.exists(char_file_path):
        return dict()
    with open(char_file_path, 'r') as f:
        characteristics = yaml.safe_load(f)
    if characteristics['dataset'] != dataset_name or characteristics['version'] != dataset_version:
        raise ValueError("Characteristics file does not match the specified dataset name and version.")
    return characteristics['characteristics']

import inspect

def get_call_context():
    frame = inspect.currentframe()
    caller = frame.f_back if frame and frame.f_back else None
    
    if caller is None:
        return "<unknown>", {}
    
    return caller.f_code.co_name, caller.f_locals.copy()