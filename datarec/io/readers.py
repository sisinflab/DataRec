import tqdm

from datarec.io.rawdata import RawData
import pandas as pd
import os


def fill_rawdata(data, user=None, item=None, rating=None, timestamp=None, path=None):
    """
    Create a RawData object from raw data and assign column names to RawData object attributes.

    Args:
        data (pd.DataFrame): Data to create RawData object from.
        user (str): Column name for user field.
        item (str): Column name for item field.
        rating (str): Column name for rating field.
        timestamp (str): Column name for timestamp field.
        path (str): Path where the original file is stored.


    """
    rawdata = RawData(data)

    # set columns
    rawdata.user = user
    rawdata.item = item
    rawdata.rating = rating
    rawdata.timestamp = timestamp

    # set file path
    rawdata.path = path


def read_json(filepath, user_field=None, item_field=None, rating_field=None, timestamp_field=None, lines=True):
    """
    Reads a JSON file and returns it as a RawData object.
    Args:
        filepath (str): path to JSON file.
        user_field (str): JSON key for user field.
        item_field (str): JSON key for item field.
        rating_field (str): JSON key for rating field.
        timestamp_field (str): JSON key for timestamp field.
        lines (bool): Read the file as a JSON object per line.

    Returns:
        (RawData): RawData object

    """
    # check that file exists
    if os.path.exists(filepath) is False:
        raise FileNotFoundError

    std_fields = [user_field, item_field, rating_field, timestamp_field]
    assigned_fields = [c for c in std_fields if c is not None]

    # at least one column given check
    if len(assigned_fields) == 0:
        raise AttributeError('Fields are missing. At least one should be assigned')

    # read data
    data = pd.read_json(filepath, lines=lines)

    # check that columns are aligned
    for c in assigned_fields:
        if c not in data.columns:
            raise ValueError(f'Field {c} not found in the dataset. Please, check the value and retry')

    rawdata = RawData(data[assigned_fields])

    # set columns
    rawdata.user = user_field if user_field is not None else None
    rawdata.item = item_field if item_field is not None else None
    rawdata.rating = rating_field if rating_field is not None else None
    rawdata.timestamp = timestamp_field if timestamp_field is not None else None
    return rawdata


def read_tabular(filepath: str, sep: str, user_col=None, item_col=None, rating_col=None, timestamp_col=None,
                 header="infer", skiprows=0):
    """
    Reads a tabular data file and returns it as a pandas DataFrame.
    Args:
        filepath (str): Path to tabular data file.
        sep (str): Separator to use.
        user_col (str): Column name for user field.
        item_col (str): Column name for item field.
        rating_col (str): Column name for rating field.
        timestamp_col (str): Column name for timestamp field.
        header (nt, Sequence of int, ‘infer’ or None): Row number(s) containing column labels and marking the start of the data (zero-indexed). Default behavior is to infer the column names.
        skiprows (int, list of int or Callable): Line numbers to skip (0-indexed) or number of lines to skip (int) at the start of the file.

    Returns:
        (RawData): RawData object.

    """
    # check that file exists
    if os.path.exists(filepath) is False:
        raise FileNotFoundError

    std_columns = [user_col, item_col, rating_col, timestamp_col]
    assigned_columns = [c for c in std_columns if c is not None]

    # at least one column given check
    if len(assigned_columns) == 0:
        raise AttributeError('Columns are missing. At least one should be assigned')

    # read data
    data = pd.read_table(filepath_or_buffer=filepath, sep=sep, header=header, skiprows=skiprows, engine='python')

    # check that columns are aligned
    for c in assigned_columns:
        if c not in data.columns:
            raise ValueError(f'Column {c} not found in the dataset. Please, check the value and retry')

    rawdata = RawData(data=data[assigned_columns])

    # set columns
    rawdata.user = user_col if (user_col is not None) else None
    rawdata.item = item_col if item_col is not None else None
    rawdata.rating = rating_col if rating_col is not None else None
    rawdata.timestamp = timestamp_col if timestamp_col is not None else None

    return rawdata


def read_inline(filepath: str, cols=None, user_col='user', item_col='item', col_sep=',', history_sep=';'):
    """
    Read a CSV file and return a RawData object.
    Args:
        filepath (str): Path to CVS file.
        cols (list[str]): List of column names.
        user_col (str): Column name for user field.:
        item_col (str): Column name for item field.
        col_sep (str): Separator to use.
        history_sep (str): Separator for multiple items.

    Returns:
        (RawData): RawData object.

    """
    if cols is None:
        cols = ['user', 'item']
    assert os.path.exists(filepath), f'File not found at {filepath}'
    to_drop_cols = [c for c in cols if c not in (user_col, item_col)]

    data = pd.read_csv(filepath, sep=col_sep, header=None, names=cols)
    data = data.dropna(subset=['user', 'item'])
    data = data.drop(columns=to_drop_cols)
    data[item_col] = data[item_col].apply(lambda x: [item.strip() for item in x.split(history_sep)])
    data = data.explode('item')
    data = data.reset_index(drop=True)
    return RawData(data, user='user', item='item')


def read_inline_chunk(filepath: str, cols=None, user_col='user', item_col='item'):
    """
    Read a CSV file a chunk of rows at a time and return a RawData object.
    Args:
        filepath (str): Path to CSV file.
        cols (list[str]): List of column names.
        user_col (str): Column name for user field.
        item_col (str): Column name for item field.

    Returns:
        (RawData): RawData object.

    """
    if cols is None:
        cols = ['user', 'item']
    assert os.path.exists(filepath), f'File not found at {filepath}'
    to_drop_cols = [c for c in cols if c not in (user_col, item_col)]

    data_chunks = pd.read_csv(filepath, sep=',', header=None, names=cols, chunksize=100000)
    data = None

    for chunk in tqdm.tqdm(data_chunks):
        chunk = chunk.drop(columns=to_drop_cols)
        chunk[item_col] = chunk[item_col].apply(lambda x: [item.strip() for item in x.split(';')])
        chunk = chunk.explode('item')
        if data is not None:
            data = pd.concat([data, chunk])
        else:
            data = chunk

    data = data.reset_index(drop=True)
    return RawData(data, user='user', item='item')
