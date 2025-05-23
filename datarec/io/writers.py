from datarec.io.rawdata import RawData
import pandas as pd

ACCEPTED_TAB_DELIMITERS = [',', ';', '\t', '::']


def write_tabular(rawdata: RawData, path, sep='\t', header=True, decimal='.',
                  user=True, item=True, rating=True, timestamp=True, verbose=True):
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

