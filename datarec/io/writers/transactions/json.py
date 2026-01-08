import os
import json
from typing import Optional, Union, List, Dict, Any, TYPE_CHECKING

import pandas as pd

from datarec.io.rawdata import RawData
from datarec.io.utils import as_rawdata

if TYPE_CHECKING:
    from datarec.data.dataset import DataRec

def write_transactions_json_base(
    data: Union["RawData", "DataRec"],
    filepath: str,
    *,
    user_col: str = "user",
    item_col: str = "item",
    rating_col: str = "rating",
    timestamp_col: str = "timestamp",
    include_user: bool = True,
    include_item: bool = True,
    include_rating: bool = False,
    include_timestamp: bool = False,
    lines: bool = True,
    indent: Optional[int] = 2,
    ensure_ascii: bool = False,
    verbose: bool = True,
) -> None:
    """
    Writes transactional interaction data to JSON (lines=False) or JSON Lines (lines=True).

    Output schema (per interaction):
        { user_col: ..., item_col: ..., [rating_col: ...], [timestamp_col: ...] }

    This writer accepts either:
    - RawData
    - DataRec (converted via `.to_rawdata()`)

    Args:
        data: RawData or DataRec instance.
        filepath: Output path.
        user_col: Output key for the user field.
        item_col: Output key for the item field.
        rating_col: Output key for the rating field (only used if include_rating=True).
        timestamp_col: Output key for the timestamp field (only used if include_timestamp=True).
        include_user: Whether to include the user field (must be True for transactional exports).
        include_item: Whether to include the item field (must be True for transactional exports).
        include_rating: Whether to include the rating field.
        include_timestamp: Whether to include the timestamp field.
        lines: If True writes JSONL; if False writes a single JSON array.
        indent: Pretty-print indentation for JSON array (ignored for JSONL).
        ensure_ascii: Whether to escape non-ascii characters.
        verbose: Whether to print a confirmation message.

    Returns:
        None
    """
    raw: RawData = as_rawdata(data)

    # Transactional exports should always contain user + item (coherent across formats)
    if not include_user:
        raise ValueError("Transactional export requires include_user=True.")
    if not include_item:
        raise ValueError("Transactional export requires include_item=True.")

    if raw.user is None:
        raise ValueError("User column is not defined in RawData.")
    if raw.item is None:
        raise ValueError("Item column is not defined in RawData.")

    cols: List[object] = [raw.user, raw.item]
    rename_map: Dict[object, str] = {raw.user: user_col, raw.item: item_col}

    if include_rating:
        if raw.rating is None:
            raise ValueError("include_rating=True but RawData.rating is not defined.")
        cols.append(raw.rating)
        rename_map[raw.rating] = rating_col

    if include_timestamp:
        if raw.timestamp is None:
            raise ValueError("include_timestamp=True but RawData.timestamp is not defined.")
        cols.append(raw.timestamp)
        rename_map[raw.timestamp] = timestamp_col

    df_out = raw.data[cols].rename(columns=rename_map)

    out_dir = os.path.dirname(os.path.abspath(filepath))
    if out_dir and not os.path.exists(out_dir):
        os.makedirs(out_dir, exist_ok=True)

    if lines:
        # JSONL: one JSON object per line (streaming-friendly)
        with open(filepath, "w", encoding="utf-8") as f:
            for record in df_out.to_dict(orient="records"):
                f.write(json.dumps(record, ensure_ascii=ensure_ascii))
                f.write("\n")
    else:
        # JSON array: write a single JSON array
        with open(filepath, "w", encoding="utf-8") as f:
            json.dump(
                df_out.to_dict(orient="records"),
                f,
                ensure_ascii=ensure_ascii,
                indent=indent,
            )

    if verbose:
        fmt = "JSONL" if lines else "JSON"
        print(f"{fmt} dataset written to '{filepath}'")


def write_transactions_json(
    data: Union["RawData", "DataRec"],
    filepath: str,
    *,
    user_col: str = "user",
    item_col: str = "item",
    rating_col: str = "rating",
    timestamp_col: str = "timestamp",
    include_user: bool = True,
    include_item: bool = True,
    include_rating: bool = False,
    include_timestamp: bool = False,
    indent: Optional[int] = 2,
    ensure_ascii: bool = False,
    verbose: bool = True,
) -> None:
    """
    Writes transactional interaction data as a single JSON array.
    """
    return write_transactions_json_base(
        data,
        filepath,
        user_col=user_col,
        item_col=item_col,
        rating_col=rating_col,
        timestamp_col=timestamp_col,
        include_user=include_user,
        include_item=include_item,
        include_rating=include_rating,
        include_timestamp=include_timestamp,
        lines=False,
        indent=indent,
        ensure_ascii=ensure_ascii,
        verbose=verbose,
    )
