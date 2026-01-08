import pandas as pd
import os
import csv
import numpy as np
from typing import Optional, List, Union
from datarec.io.rawdata import RawData
from datarec.io.readers._decorators import annotate_rawdata_output


class IncrementalEncoder:
    """
    Streaming-friendly encoder that assigns integer IDs incrementally.

    Keeps forward (public -> int) and reverse (int -> public) mappings without
    requiring the full list upfront.
    """

    def __init__(self, offset: int = 0):
        self.offset = offset
        self._forward: dict = {}
        self._reverse: list = []

    def __len__(self):
        return len(self._forward)

    def encode_one(self, key):
        if key in self._forward:
            return self._forward[key]
        idx = self.offset + len(self._forward)
        self._forward[key] = idx
        self._reverse.append(key)
        return idx

    def encode_many(self, iterable):
        return [self.encode_one(k) for k in iterable]

    def decode_one(self, idx: int):
        pos = idx - self.offset
        if pos < 0 or pos >= len(self._reverse):
            raise KeyError(f"Id {idx} not in encoder")
        return self._reverse[pos]

    def decode_many(self, iterable):
        return [self.decode_one(i) for i in iterable]

    @property
    def forward(self):
        return self._forward

    @property
    def reverse(self):
        return self._reverse


@annotate_rawdata_output
def read_sequence_tabular_inline(
    filepath: str,
    *,
    user_col: str = "user",
    sequence_col: str = "sequence",
    sequence_sep: str = " ",
    timestamp_col: Optional[str] = "timestamp",
    meta_cols: Optional[List[str]] = None,
    col_sep: str = ",",
    header: Union[int, List[int], str, None] = None,
    cols: Optional[List[str]] = None,
    engine: str = "c",
    fallback_engine: str = "python",
    stream: bool = False,
    encode_ids: bool = False,
    chunksize: int = 100_000,
) -> RawData:
    """
    Reads a file where interaction sequences are stored in a single string column.
    
    Example: user_id,sequence -> 70,"495 1631 2317"

    Args:
        filepath: Path to the CSV file.
        user_col: Column name containing the user ID.
        sequence_col: Column containing the serialized interaction sequence.
        sequence_sep: Separator used inside the sequence string.
        timestamp_col: Column name for timestamp (if present).
        meta_cols: Additional metadata columns to keep.
        col_sep: Column separator used in the CSV file.
        header: Row number for the header.
        cols: Explicit column names if the file has no header.
        engine: Pandas CSV engine to use ("c" or "python"). Defaults to "c" with automatic
                fallback to `fallback_engine` on failure.
        fallback_engine: Engine to try if the primary one fails. Defaults to "python".
        stream: If True, process the file in chunks to reduce peak memory.
        encode_ids: If True, encode user/item to int ids using IncrementalEncoder (streaming or full).
        chunksize: Number of rows per chunk when streaming.

    Returns:
        RawData: Transactional data.
    """
    if not os.path.exists(filepath):
        raise FileNotFoundError(f"File not found: {filepath}")

    if meta_cols is None:
        meta_cols = []

    read_kwargs = dict(
        sep=col_sep,
        header=header,
        engine=engine,
        dtype=str,  # avoid type inference surprises
        encoding="utf-8",
        encoding_errors="ignore",
        quoting=csv.QUOTE_NONE,
    )
    if cols is not None:
        read_kwargs["names"] = cols

    if stream:
        return _read_sequence_tabular_inline_stream(
            filepath=filepath,
            user_col=user_col,
            sequence_col=sequence_col,
            sequence_sep=sequence_sep,
            timestamp_col=timestamp_col,
            meta_cols=meta_cols,
            read_kwargs=read_kwargs,
            fallback_engine=fallback_engine,
            encode_ids=encode_ids,
            chunksize=chunksize,
        )

    return _read_sequence_tabular_inline_full(
        filepath=filepath,
        user_col=user_col,
        sequence_col=sequence_col,
        sequence_sep=sequence_sep,
        timestamp_col=timestamp_col,
        meta_cols=meta_cols,
        read_kwargs=read_kwargs,
        fallback_engine=fallback_engine,
        encode_ids=encode_ids,
    )


def _read_sequence_tabular_inline_stream(
    *,
    filepath: str,
    user_col: str,
    sequence_col: str,
    sequence_sep: str,
    timestamp_col: Optional[str],
    meta_cols: List[str],
    read_kwargs: dict,
    fallback_engine: str,
    encode_ids: bool,
    chunksize: int,
) -> RawData:
    """Streaming path: process chunks with optional incremental encoding."""
    engines = [read_kwargs["engine"]] if not fallback_engine or fallback_engine == read_kwargs["engine"] else [read_kwargs["engine"], fallback_engine]
    last_exc = None

    for eng in engines:
        try:
            user_enc = IncrementalEncoder(offset=0) if encode_ids else None
            item_enc = IncrementalEncoder(offset=0) if encode_ids else None

            encoded_users: list[np.ndarray] = []
            encoded_items: list[np.ndarray] = []
            encoded_ts: list[np.ndarray] = []
            encoded_meta: dict[str, list[np.ndarray]] = {}

            local_kwargs = dict(read_kwargs)
            local_kwargs["engine"] = eng

            reader = pd.read_csv(filepath, chunksize=chunksize, **local_kwargs)
            for chunk in reader:
                _process_chunk(
                    chunk, user_col, sequence_col, sequence_sep,
                    timestamp_col, meta_cols, user_enc, item_enc,
                    encoded_users, encoded_items, encoded_ts, encoded_meta, encode_ids
                )

            users_arr = np.concatenate(encoded_users) if encoded_users else np.array([], dtype=object)
            items_arr = np.concatenate(encoded_items) if encoded_items else np.array([], dtype=object)

            data_dict = {user_col: users_arr, "items": items_arr}
            has_timestamp = timestamp_col and len(encoded_ts) > 0
            if has_timestamp:
                data_dict[timestamp_col] = np.concatenate(encoded_ts)
            for mc, parts in encoded_meta.items():
                data_dict[mc] = np.concatenate(parts)

            data = pd.DataFrame(data_dict)
            final_timestamp = timestamp_col if has_timestamp else None
            return RawData(
                data,
                user=user_col,
                item="items",
                timestamp=final_timestamp,
                user_encoder=user_enc.forward if user_enc else None,
                item_encoder=item_enc.forward if item_enc else None,
            )
        except Exception as exc:  # noqa: BLE001
            last_exc = exc
            continue

    raise last_exc


def _read_sequence_tabular_inline_full(
    *,
    filepath: str,
    user_col: str,
    sequence_col: str,
    sequence_sep: str,
    timestamp_col: Optional[str],
    meta_cols: List[str],
    read_kwargs: dict,
    fallback_engine: str,
    encode_ids: bool,
) -> RawData:
    """Non-streaming path: load all data then (optionally) encode."""
    try:
        data = pd.read_csv(filepath, **read_kwargs)
    except Exception as exc:
        if fallback_engine and fallback_engine != read_kwargs.get("engine"):
            local_kwargs = dict(read_kwargs)
            local_kwargs["engine"] = fallback_engine
            data = pd.read_csv(filepath, **local_kwargs)
        else:
            raise exc

    if user_col not in data.columns:
        raise ValueError(f"User column '{user_col}' not found.")
    if sequence_col not in data.columns:
        raise ValueError(f"Sequence column '{sequence_col}' not found.")

    cols_to_keep = [user_col, sequence_col]
    has_timestamp = timestamp_col and timestamp_col in data.columns
    if has_timestamp:
        cols_to_keep.append(timestamp_col)
    for mc in meta_cols:
        if mc in data.columns and mc not in cols_to_keep:
            cols_to_keep.append(mc)

    data = data[cols_to_keep].dropna()
    data["items"] = data[sequence_col].astype(str).str.split(sequence_sep)
    data = data.explode("items")
    data = data.drop(columns=[sequence_col])
    data["items"] = data["items"].str.strip()
    data = data[data["items"] != ""]
    data = data.reset_index(drop=True)

    user_encoder = None
    item_encoder = None
    if encode_ids:
        user_enc = IncrementalEncoder(offset=0)
        item_enc = IncrementalEncoder(offset=0)
        data[user_col] = user_enc.encode_many(data[user_col].tolist())
        data["items"] = item_enc.encode_many(data["items"].tolist())
        user_encoder = user_enc.forward
        item_encoder = item_enc.forward

    final_timestamp = timestamp_col if has_timestamp else None
    return RawData(
        data,
        user=user_col,
        item="items",
        timestamp=final_timestamp,
        user_encoder=user_encoder,
        item_encoder=item_encoder,
    )


def _process_chunk(df_chunk,
                   user_col,
                   sequence_col,
                   sequence_sep,
                   timestamp_col,
                   meta_cols,
                   user_enc: Optional[IncrementalEncoder],
                   item_enc: Optional[IncrementalEncoder],
                   encoded_users: list,
                   encoded_items: list,
                   encoded_ts: list,
                   encoded_meta: dict,
                   encode_ids: bool):
    """Internal helper to process a chunk with incremental encoding."""
    if meta_cols is None:
        meta_cols = []

    if user_col not in df_chunk.columns:
        raise ValueError(f"User column '{user_col}' not found.")
    if sequence_col not in df_chunk.columns:
        raise ValueError(f"Sequence column '{sequence_col}' not found.")

    cols_to_keep = [user_col, sequence_col]
    has_timestamp = timestamp_col and timestamp_col in df_chunk.columns
    if has_timestamp:
        cols_to_keep.append(timestamp_col)
    for mc in meta_cols:
        if mc in df_chunk.columns and mc not in cols_to_keep:
            cols_to_keep.append(mc)

    df_chunk = df_chunk[cols_to_keep].dropna()
    df_chunk["items"] = df_chunk[sequence_col].astype(str).str.split(sequence_sep)
    df_chunk = df_chunk.explode("items")
    df_chunk = df_chunk.drop(columns=[sequence_col])
    df_chunk["items"] = df_chunk["items"].str.strip()
    df_chunk = df_chunk[df_chunk["items"] != ""]
    df_chunk = df_chunk.reset_index(drop=True)

    if encode_ids:
        encoded_users.append(np.fromiter((user_enc.encode_one(u) for u in df_chunk[user_col]), dtype=np.int64))
        encoded_items.append(np.fromiter((item_enc.encode_one(i) for i in df_chunk["items"]), dtype=np.int64))
    else:
        encoded_users.append(df_chunk[user_col].to_numpy())
        encoded_items.append(df_chunk["items"].to_numpy())

    if has_timestamp:
        encoded_ts.append(df_chunk[timestamp_col].to_numpy())
    for mc in meta_cols:
        if mc in df_chunk.columns:
            encoded_meta.setdefault(mc, []).append(df_chunk[mc].to_numpy())


@annotate_rawdata_output
def read_sequence_tabular_wide(
    filepath: str,
    *,
    user_col: str = "user",
    item_col: str = "item",
    col_sep: str = "\t",
    header: Optional[int] = None,
    encode_ids: bool = False,
) -> RawData:
    """
    Reads a file containing variable-length interaction sequences (ragged).
    
    Example: u0\ti0\ti1\ti3

    Args:
        filepath: Path to the text/CSV file.
        user_col: Name to assign to the user column.
        item_col: Name to assign to the item column.
        col_sep: Delimiter used in the file.
        header: Row number (0-indexed) to use as the header (to be skipped).

    Returns:
        RawData: Transactional DataFrame.
    """
    if not os.path.exists(filepath):
        raise FileNotFoundError(f"File not found: {filepath}")

    if header is not None and header < 0:
        raise ValueError(f"header must be >= 0 or None, got {header}.")

    if header is not None:
        _skiprows = header + 1 
    else:
        _skiprows = 0

    # Fast Loading (Raw Text)
    df_raw = pd.read_csv(
        filepath,
        sep="\0",
        header=None,
        names=["_raw_string"],
        skiprows=_skiprows,
        engine="c",
        quoting=csv.QUOTE_NONE,
    )

    if df_raw.empty:
        raise ValueError("The provided file is empty or all rows were skipped.")

    # Vectorized processing
    df_raw["_split"] = df_raw["_raw_string"].str.split(col_sep)
    df_raw[user_col] = df_raw["_split"].str[0].str.strip()
    df_raw["_items_list"] = df_raw["_split"].str[1:]

    df_long = df_raw.explode("_items_list")
    df_long = df_long.rename(columns={"_items_list": item_col})
    df_long = df_long[[user_col, item_col]]
    
    df_long = df_long.dropna(subset=[item_col])
    
    df_long[item_col] = df_long[item_col].astype(str).str.strip()
    df_long = df_long[df_long[item_col] != ""]

    df_long = df_long.reset_index(drop=True)

    user_encoder = None
    item_encoder = None
    if encode_ids:
        u_enc = IncrementalEncoder(offset=0)
        i_enc = IncrementalEncoder(offset=0)
        df_long[user_col] = u_enc.encode_many(df_long[user_col].tolist())
        df_long[item_col] = i_enc.encode_many(df_long[item_col].tolist())
        user_encoder = u_enc.forward
        item_encoder = i_enc.forward

    return RawData(df_long, user=user_col, item=item_col, user_encoder=user_encoder, item_encoder=item_encoder)


@annotate_rawdata_output
def read_sequence_tabular_implicit(
    filepath: str,
    *,
    user_col: str = "sequence_id",
    item_col: str = "item",
    col_sep: str = " ",
    header: Optional[int] = None,
    drop_length_col: bool = True,
    encode_ids: bool = False,
) -> RawData:
    """
    Reads a tabular file where each row represents a sequence with an
    implicit identifier (row-based), optionally starting with a declared
    sequence length.

    Example:
        3  10  20  30
        2  11  42

    Each row is interpreted as a distinct sequence (pseudo-user).
    The first column may represent the declared sequence length and is
    ignored by default.

    Args:
        filepath: Path to the text/CSV file.
        user_col: Name assigned to the implicit sequence identifier column.
        item_col: Name assigned to the item column.
        col_sep: Delimiter used in the file.
        header: Optional row index to skip as header.
        drop_length_col: If True, the first column is treated as sequence
                         length and discarded.

    Returns:
        RawData: Transactional DataFrame where each sequence is treated
                 as a pseudo-user.
    """
    if not os.path.exists(filepath):
        raise FileNotFoundError(f"File not found: {filepath}")

    if header is not None and header < 0:
        raise ValueError(f"header must be >= 0 or None, got {header}.")

    skiprows = header + 1 if header is not None else 0

    # Load each line as a raw string (ragged-safe, fast)
    df_raw = pd.read_csv(
        filepath,
        sep="\0",
        header=None,
        names=["_raw_string"],
        skiprows=skiprows,
        engine="c",
        quoting=csv.QUOTE_NONE,
    )

    if df_raw.empty:
        raise ValueError("The provided file is empty or all rows were skipped.")

    # Split line into tokens
    df_raw["_split"] = df_raw["_raw_string"].str.strip().str.split(col_sep)

    # Generate implicit sequence id (row-based)
    df_raw[user_col] = df_raw.index.astype(str)

    # Drop declared length if requested
    if drop_length_col:
        df_raw["_items_list"] = df_raw["_split"].str[1:]
    else:
        df_raw["_items_list"] = df_raw["_split"]

    # Explode sequences
    df_long = df_raw.explode("_items_list")

    df_long = df_long.rename(columns={"_items_list": item_col})
    df_long = df_long[[user_col, item_col]]

    # Cleanup
    df_long = df_long.dropna(subset=[item_col])
    df_long[item_col] = df_long[item_col].astype(str).str.strip()
    df_long = df_long[df_long[item_col] != ""]

    df_long = df_long.reset_index(drop=True)

    user_encoder = None
    item_encoder = None
    if encode_ids:
        u_enc = IncrementalEncoder(offset=0)
        i_enc = IncrementalEncoder(offset=0)
        df_long[user_col] = u_enc.encode_many(df_long[user_col].tolist())
        df_long[item_col] = i_enc.encode_many(df_long[item_col].tolist())
        user_encoder = u_enc.forward
        item_encoder = i_enc.forward

    return RawData(df_long, user=user_col, item=item_col, user_encoder=user_encoder, item_encoder=item_encoder)
