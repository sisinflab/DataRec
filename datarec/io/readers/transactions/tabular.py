import pandas as pd
import os
import numpy as np
from typing import Optional, List, Union, cast
from datarec.io.rawdata import RawData
from datarec.io.readers._decorators import annotate_datarec_output
from datarec import DataRec


class IncrementalEncoder:
    """Streaming-friendly encoder for public->int ids."""

    def __init__(self, offset: int = 0):
        self.offset = offset
        self._forward = {}
        self._reverse = []

    def encode_one(self, key):
        if key in self._forward:
            return self._forward[key]
        idx = self.offset + len(self._forward)
        self._forward[key] = idx
        self._reverse.append(key)
        return idx

    def encode_many(self, iterable):
        return [self.encode_one(k) for k in iterable]

    @property
    def forward(self):
        return self._forward


@annotate_datarec_output
def read_transactions_tabular(
    filepath: str,
    *,
    sep: str = "\t",
    user_col: Union[str, int],
    item_col: Union[str, int],
    rating_col: Optional[Union[str, int]] = None,
    timestamp_col: Optional[Union[str, int]] = None,
    header: Union[int, List[int], str, None] = None,
    skiprows: Union[int, List[int]] = 0,
    cols: Optional[List[str]] = None,
    engine: Optional[str] = 'c',
    fallback_engine: Optional[str] = 'python',
    stream: bool = False,
    encode_ids: bool = False,
    chunksize: int = 100_000,
    dataset_name: str = "Unknown Dataset",
    version_name: str = "Unknown Version",
) -> DataRec:
    """
    Reads a tabular data file (CSV, TSV, etc.) into a RawData object.

    Args:
        filepath: Path to the tabular data file.
        sep: Delimiter to use (default: tab).
        user_col: Column name or index for the user field (Required).
        item_col: Column name or index for the item field (Required).
        rating_col: Column name or index for the rating field.
        timestamp_col: Column name or index for the timestamp field.
        header: Row number(s) to use as the column names. Defaults to 'infer'.
        skiprows: Line numbers to skip at the start of the file.
        cols: Explicit column names if the file has no header. Passed as `names`
              to `pandas.read_csv`.
        engine: Pandas CSV engine.
        fallback_engine: Engine to try if the primary fails.
        stream: If True, read in chunks to reduce memory.
        encode_ids: If True, encode user/item to int ids using IncrementalEncoder.
        chunksize: Rows per chunk when streaming.
        dataset_name: Name to assign to the resulting DataRec dataset.
        version_name: Version identifier to assign to the resulting DataRec dataset.

    Returns:
        DataRec: The loaded data.
            (Returned via @annotate_datarec_output, which wraps the RawData.)
    """
    if not os.path.exists(filepath):
        raise FileNotFoundError(f"File not found: {filepath}")

    read_kwargs = dict(sep=sep, header=header, skiprows=skiprows, engine=engine)
    if cols is not None:
        read_kwargs["names"] = cols

    if stream:
        rawdata = _read_transactions_tabular_stream(
            filepath=filepath,
            user_col=user_col,
            item_col=item_col,
            rating_col=rating_col,
            timestamp_col=timestamp_col,
            read_kwargs=read_kwargs,
            fallback_engine=fallback_engine,
            encode_ids=encode_ids,
            chunksize=chunksize,
        )
        # Wrapped by @annotate_datarec_output to return DataRec at call sites.
        return cast(DataRec, rawdata)

    try:
        data = pd.read_csv(filepath, **read_kwargs)
    except Exception as exc:
        if fallback_engine and fallback_engine != engine:
            read_kwargs["engine"] = fallback_engine
            data = pd.read_csv(filepath, **read_kwargs)
        else:
            raise exc

    # Helper to resolve column name from string or index
    def _resolve_col(col: Optional[Union[str, int]]) -> Optional[object]:
        """
        Resolve a column specifier to an existing column label in `data.columns`.

        Rules:
        - str: treated as a column name (label)
        - int: if it matches an existing column label, use it as label;
                otherwise treat it as positional index.
        """
        if col is None:
            return None

        cols_index = data.columns

        if isinstance(col, int):
            # Prefer label semantics if the label exists (works also with numpy integer labels)
            if col in cols_index:
                # Return the exact label object stored in the Index (could be np.int64(0), etc.)
                return int(cols_index[cols_index.get_loc(col)])

            # Otherwise, interpret as positional index
            if col < 0 or col >= len(cols_index):
                raise ValueError(
                    f"Column index {col} is out of bounds for {len(cols_index)} columns."
                )
            return cols_index[col]

        # str case: strict label match
        if col not in cols_index:
            raise ValueError(
                f"Column '{col}' not found in dataset columns: {list(cols_index)}"
            )
        return col

    user_col_name = _resolve_col(user_col)
    item_col_name = _resolve_col(item_col)
    rating_col_name = _resolve_col(rating_col)
    timestamp_col_name = _resolve_col(timestamp_col)

    std_columns = [user_col_name, item_col_name, rating_col_name, timestamp_col_name]
    assigned_columns = [c for c in std_columns if c is not None]

    if not assigned_columns or user_col_name is None or item_col_name is None:
        raise ValueError("User and Item columns are required.")

    # Subset data to the relevant columns
    data = data[assigned_columns]

    user_encoder = None
    item_encoder = None
    if encode_ids:
        u_enc = IncrementalEncoder(offset=0)
        i_enc = IncrementalEncoder(offset=0)
        data[user_col_name] = u_enc.encode_many(data[user_col_name].tolist())
        data[item_col_name] = i_enc.encode_many(data[item_col_name].tolist())
        user_encoder = u_enc.forward
        item_encoder = i_enc.forward

    rawdata = RawData(
        data,
        user=user_col_name,
        item=item_col_name,
        rating=rating_col_name,
        timestamp=timestamp_col_name,
        user_encoder=user_encoder,
        item_encoder=item_encoder,
    )

    # Wrapped by @annotate_datarec_output to return DataRec at call sites.
    return cast(DataRec, rawdata)


def _read_transactions_tabular_stream(
    *,
    filepath: str,
    user_col,
    item_col,
    rating_col,
    timestamp_col,
    read_kwargs: dict,
    fallback_engine: Optional[str],
    encode_ids: bool,
    chunksize: int,
) -> RawData:
    engines = [read_kwargs["engine"]] if not fallback_engine or fallback_engine == read_kwargs["engine"] else [read_kwargs["engine"], fallback_engine]
    last_exc = None

    for eng in engines:
        try:
            u_enc = IncrementalEncoder(offset=0) if encode_ids else None
            i_enc = IncrementalEncoder(offset=0) if encode_ids else None

            encoded_cols = { "user": [], "item": [] }
            encoded_rating = []
            encoded_ts = []

            local_kwargs = dict(read_kwargs)
            local_kwargs["engine"] = eng

            reader = pd.read_csv(filepath, chunksize=chunksize, **local_kwargs)
            for chunk in reader:
                user_col_name, item_col_name, rating_col_name, timestamp_col_name = _resolve_columns(chunk, user_col, item_col, rating_col, timestamp_col)
                cols_to_keep = [c for c in [user_col_name, item_col_name, rating_col_name, timestamp_col_name] if c is not None]
                chunk = chunk[cols_to_keep].dropna()

                if encode_ids:
                    encoded_cols["user"].append(np.fromiter((u_enc.encode_one(u) for u in chunk[user_col_name]), dtype=np.int64))
                    encoded_cols["item"].append(np.fromiter((i_enc.encode_one(i) for i in chunk[item_col_name]), dtype=np.int64))
                else:
                    encoded_cols["user"].append(chunk[user_col_name].to_numpy())
                    encoded_cols["item"].append(chunk[item_col_name].to_numpy())

                if rating_col_name is not None:
                    encoded_rating.append(chunk[rating_col_name].to_numpy())
                if timestamp_col_name is not None:
                    encoded_ts.append(chunk[timestamp_col_name].to_numpy())

            users_arr = np.concatenate(encoded_cols["user"]) if encoded_cols["user"] else np.array([], dtype=object)
            items_arr = np.concatenate(encoded_cols["item"]) if encoded_cols["item"] else np.array([], dtype=object)
            data_dict = { "user": users_arr, "item": items_arr }
            if rating_col is not None and encoded_rating:
                data_dict["rating"] = np.concatenate(encoded_rating)
            if timestamp_col is not None and encoded_ts:
                data_dict["timestamp"] = np.concatenate(encoded_ts)

            df = pd.DataFrame(data_dict)
            return RawData(
                df,
                user="user",
                item="item",
                rating="rating" if "rating" in data_dict else None,
                timestamp="timestamp" if "timestamp" in data_dict else None,
                user_encoder=u_enc.forward if u_enc else None,
                item_encoder=i_enc.forward if i_enc else None,
            )
        except Exception as exc:  # noqa: BLE001
            last_exc = exc
            continue

    raise last_exc


def _resolve_columns(data: pd.DataFrame,
                     user_col: Union[str, int],
                     item_col: Union[str, int],
                     rating_col: Optional[Union[str, int]],
                     timestamp_col: Optional[Union[str, int]]):
    """Resolve column labels for user/item/rating/timestamp supporting int indices."""

    def _resolve_col(col: Optional[Union[str, int]]) -> Optional[object]:
        if col is None:
            return None
        cols_index = data.columns
        if isinstance(col, int):
            if col in cols_index:
                return cols_index[cols_index.get_loc(col)]
            if col < 0 or col >= len(cols_index):
                raise ValueError(f"Column index {col} is out of bounds for {len(cols_index)} columns.")
            return cols_index[col]
        if col not in cols_index:
            raise ValueError(f"Column '{col}' not found in dataset columns: {list(cols_index)}")
        return col

    return (
        _resolve_col(user_col),
        _resolve_col(item_col),
        _resolve_col(rating_col),
        _resolve_col(timestamp_col),
    )
