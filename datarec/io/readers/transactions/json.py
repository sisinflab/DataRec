import pandas as pd
import numpy as np
import os
from typing import Optional
from datarec.io.rawdata import RawData
from datarec.io.readers.transactions.tabular import IncrementalEncoder  # reuse lightweight encoder
from datarec.io.readers._decorators import annotate_rawdata_output


def read_transactions_json_base(
    filepath: str, 
    *,
    user_col: str, 
    item_col: str, 
    rating_col: Optional[str] = None, 
    timestamp_col: Optional[str] = None, 
    lines: bool = True,
    stream: bool = False,
    encode_ids: bool = False,
    chunksize: int = 100_000,
) -> RawData:
    """
    Reads a JSON (or JSON Lines) file and returns it as a RawData object.
    
    Arg names standardized to match read_tabular (user_col instead of user_field).

    Args:
        filepath: Path to the JSON file.
        user_col: JSON key corresponding to the user field (Required).
        item_col: JSON key corresponding to the item field (Required).
        rating_col: JSON key corresponding to the rating field.
        timestamp_col: JSON key corresponding to the timestamp field.
        lines: If True, reads the file as a JSON object per line (JSONL).
        stream: If True and `lines=True`, read in chunks.
        encode_ids: If True, encode user/item to int ids.
        chunksize: Rows per chunk when streaming JSONL.

    Returns:
        RawData: The loaded data.
    """
    if not os.path.exists(filepath):
        raise FileNotFoundError(f"File not found: {filepath}")

    std_fields = [user_col, item_col, rating_col, timestamp_col]
    assigned_fields = [c for c in std_fields if c is not None]

    if stream:
        if not lines:
            raise ValueError("Streaming is supported only for JSON Lines (lines=True).")
        return _read_transactions_json_stream(
            filepath=filepath,
            user_col=user_col,
            item_col=item_col,
            rating_col=rating_col,
            timestamp_col=timestamp_col,
            chunksize=chunksize,
            encode_ids=encode_ids,
        )

    data = pd.read_json(filepath, lines=lines)

    # Validate columns
    missing_cols = [c for c in assigned_fields if c not in data.columns]
    if missing_cols:
        raise ValueError(f'Fields not found in dataset: {missing_cols}')

    # Filter only relevant columns to save memory
    data = data[assigned_fields]

    user_encoder = None
    item_encoder = None
    if encode_ids:
        u_enc = IncrementalEncoder(offset=0)
        i_enc = IncrementalEncoder(offset=0)
        data[user_col] = u_enc.encode_many(data[user_col].tolist())
        data[item_col] = i_enc.encode_many(data[item_col].tolist())
        user_encoder = u_enc.forward
        item_encoder = i_enc.forward

    rawdata = RawData(
        data,
        user=user_col,
        item=item_col,
        rating=rating_col,
        timestamp=timestamp_col,
        user_encoder=user_encoder,
        item_encoder=item_encoder,
    )
    
    return rawdata


def _read_transactions_json_stream(
    *,
    filepath: str,
    user_col: str,
    item_col: str,
    rating_col: Optional[str],
    timestamp_col: Optional[str],
    chunksize: int,
    encode_ids: bool,
) -> RawData:
    u_enc = IncrementalEncoder(offset=0) if encode_ids else None
    i_enc = IncrementalEncoder(offset=0) if encode_ids else None

    parts = { "user": [], "item": [] }
    ratings = []
    timestamps = []

    reader = pd.read_json(filepath, lines=True, chunksize=chunksize)
    for chunk in reader:
        missing_cols = [c for c in [user_col, item_col] if c not in chunk.columns]
        if missing_cols:
            raise ValueError(f'Fields not found in dataset: {missing_cols}')
        cols = [c for c in [user_col, item_col, rating_col, timestamp_col] if c is not None]
        chunk = chunk[cols].dropna()

        if encode_ids:
            parts["user"].append(pd.Series([u_enc.encode_one(u) for u in chunk[user_col]]).to_numpy())
            parts["item"].append(pd.Series([i_enc.encode_one(i) for i in chunk[item_col]]).to_numpy())
        else:
            parts["user"].append(chunk[user_col].to_numpy())
            parts["item"].append(chunk[item_col].to_numpy())

        if rating_col and rating_col in chunk:
            ratings.append(chunk[rating_col].to_numpy())
        if timestamp_col and timestamp_col in chunk:
            timestamps.append(chunk[timestamp_col].to_numpy())

    data_dict = {
        user_col: np.concatenate(parts["user"]) if parts["user"] else np.array([], dtype=object),
        item_col: np.concatenate(parts["item"]) if parts["item"] else np.array([], dtype=object),
    }
    if ratings:
        data_dict[rating_col] = np.concatenate(ratings)
    if timestamps:
        data_dict[timestamp_col] = np.concatenate(timestamps)

    df = pd.DataFrame(data_dict)
    return RawData(
        df,
        user=user_col,
        item=item_col,
        rating=rating_col,
        timestamp=timestamp_col,
        user_encoder=u_enc.forward if u_enc else None,
        item_encoder=i_enc.forward if i_enc else None,
    )


@annotate_rawdata_output
def read_transactions_json(
    filepath: str, 
    *,
    user_col: str, 
    item_col: str, 
    rating_col: Optional[str] = None, 
    timestamp_col: Optional[str] = None, 
    lines: bool = True,
    stream: bool = False,
    encode_ids: bool = False,
    chunksize: int = 100_000) -> RawData:
    """
    Reads a JSON (or JSON Lines) file and returns it as a RawData object.
    
    Arg names standardized to match read_tabular (user_col instead of user_field).

    Args:
        filepath: Path to the JSON file.
        user_col: JSON key corresponding to the user field (Required).
        item_col: JSON key corresponding to the item field (Required).
        rating_col: JSON key corresponding to the rating field.
        timestamp_col: JSON key corresponding to the timestamp field.
        lines: If True, reads the file as a JSON object per line (JSONL).

    Returns:
        RawData: The loaded data.
    """
    return read_transactions_json_base(
        filepath,
        user_col=user_col,
        item_col=item_col,
        rating_col=rating_col,
        timestamp_col=timestamp_col,
        lines=False,
        stream=stream,
        encode_ids=encode_ids,
        chunksize=chunksize,
    )
