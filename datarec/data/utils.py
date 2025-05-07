import os
import hashlib
from typing import Union
import statistics


def set_column_name(columns: list, value: Union[str, int], rename=True, default_name=None) -> (list, str):
    columns = list(columns)

    if isinstance(value, str):
        if value not in columns:
            raise ValueError(f'column \'{value}\' is not a valid column name.')
        selected_column = value

    elif isinstance(value, int):
        if value in columns:
            selected_column = value
        else:
            if value not in range(len(columns)):
                raise ValueError(f'column int \'{value}\' is out of range ({len(columns)} columns).')
            selected_column = columns[value]
    else:
        raise ValueError(f'column value must be either a string (column name) or an integer (column index)')

    if rename is True:
        columns[columns.index(selected_column)] = default_name
        return columns, default_name

    return columns, selected_column


def quartiles(count: dict):
    q1, q2, q3 = statistics.quantiles(count.values())

    def assign(value):
        if value <= q2:
            if value <= q1:
                return 0
            else:
                return 1
        else:
            if value <= q3:
                return 2
            else:
                return 3

    return {k: assign(f) for k, f in count.items()}


def popularity(quartiles: dict):
    categories_map = \
        {3: 'most popular',
         2: 'popular',
         1: 'common',
         0: 'long tail'}

    categories = \
        {'most popular': [],
         'popular': [],
         'common': [],
         'long tail': []}

    for k, q in quartiles.items():
        categories[categories_map[q]].append(k)

    return categories


def verify_checksum(file_path: str, checksum: str) -> None:
    if not os.path.isfile(file_path):
        raise FileNotFoundError(f'File \'{file_path}\ not found.')

    md5 = hashlib.md5()
    with open(file_path, "rb") as f:
        for chunck in iter(lambda: f.read(65536), b""):
            md5.update(chunck)

    digest = md5.hexdigest()
    if not digest == checksum:
        raise RuntimeError(f"Checksum mismatch for '{file_path}': expected {digest}, but got {checksum}. "
                           f"The file may be corrupted or a new version has been downloaded.")

    print(f'Checksum verified.')
