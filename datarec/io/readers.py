import tqdm

from datarec.io.rawdata import RawData
import pandas as pd
import os


def fill_rawdata(data, user=None, item=None, rating=None, timestamp=None, path=None):
    rawdata = RawData(data)

    # set columns
    rawdata.user = user
    rawdata.item = item
    rawdata.rating = rating
    rawdata.timestamp = timestamp

    # set file path
    rawdata.path = path


def read_json(filepath, user_field=None, item_field=None, rating_field=None, timestamp_field=None, lines=True):
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
