from datarec.io.rawdata import RawData
import pandas as pd

ACCEPTED_TAB_DELIMITERS = [',', ';', '\t', '::']


def write_tabular(rawdata: RawData, path, sep='\t', header=True, decimal='.',
                  user=True, item=True, rating=True, timestamp=True, verbose=True):
    """
    Write a RawData dataset to a CSV/TSV file.

    Args:
        rawdata (RawData): RawData instance.
        path (str): Path to the CSV/TSV file.
        sep (str): Separator to use.
        header (bool or list[str]): Write out the column names. If a list of strings is given it is assumed to be aliases for the column names.
        decimal (str): Character recognized as decimal separator.
        user (bool): Whether to write the user information. If True, the user information will be written in the file.
        item (bool): Whether to write the item information. If True, the item information will be written in the file.
        rating (bool): Whether to write the rating information. If True, the rating information will be written in the file.
        timestamp (bool): Whether to write the timestamp information. If True, the timestamp information will be written in the file.
        verbose (bool): Print out additional information.

    Returns:
        (CSV/TSV file)

    """
    cols = []
    if user:
        if rawdata.user:
            cols.append(rawdata.user)
        else:
            raise ValueError('User column not defined in the DataRec.')
    if item:
        if rawdata.item:
            cols.append(rawdata.item)
        else:
            raise ValueError('Item column not defined in the DataRec.')
    if rating:
        if rawdata.rating:
            cols.append(rawdata.rating)
        else:
            raise ValueError('Rating column not defined in the DataRec.')
    if timestamp:
        if rawdata.timestamp:
            cols.append(rawdata.timestamp)
        else:
            raise ValueError('Timestamp column not defined in the DataRec.')

    data: pd.DataFrame = rawdata.data[cols]

    if sep in ACCEPTED_TAB_DELIMITERS:
        if sep == "::":
            file = data.to_csv(sep='*', header=header, index=False, decimal=decimal)
            file.replace('*', '::')
            with open(file, 'w') as f:
                f.write(file)
        else:
            data.to_csv(path, sep=sep, header=header, index=False, decimal=decimal)
            if verbose:
                print(f'A dataset has been stored at \'{path}\'')
    else:
        raise ValueError


def write_json(rawdata: RawData, path, user=True, item=True, rating=True, timestamp=True):
    """
    Write a RawData dataset to a JSON file.
    Args:
        rawdata (RawData): RawData instance.
        path (str): Path to the JSON file.
        user (bool): Whether to write the user information. If True, the user information will be written in the file.
        item (bool): Whether to write the item information. If True, the item information will be written in the file.
        rating (bool): Whether to write the rating information. If True, the rating information will be written in the file.
        timestamp (bool): Whether to write the timestamp information. If True, the timestamp information will be written in the file.

    Returns:
        (JSON file)

    """

    cols = []
    if user:
        cols.append(rawdata.user)
    if item:
        cols.append(rawdata.item)
    if rating:
        cols.append(rawdata.rating)
    if timestamp:
        cols.append(rawdata.timestamp)

    data: pd.DataFrame = rawdata.data[cols]

    data.to_json(path, orient='records', lines=True)

