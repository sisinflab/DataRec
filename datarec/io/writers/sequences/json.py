import os
import json
import math
import datetime as _dt
from typing import Optional, Union, List, Dict, Any, TYPE_CHECKING

import pandas as pd

from datarec.io.rawdata import RawData
from datarec.io.utils import as_rawdata

if TYPE_CHECKING:
    from datarec.data.dataset import DataRec


def _json_safe(x: Any) -> Any:
    """
    Convert common pandas/numpy/scalar types into JSON-serializable Python types.
    """
    # Fast-path for already-safe primitives
    if x is None or isinstance(x, (str, int, float, bool)):
        # Normalize NaN/inf floats
        if isinstance(x, float):
            if math.isnan(x) or math.isinf(x):
                return None
        return x

    # pandas / numpy scalar -> python scalar
    if hasattr(x, "item") and callable(getattr(x, "item")):
        try:
            return _json_safe(x.item())
        except Exception:
            pass

    # pandas Timestamp / datetime / date
    if isinstance(x, (pd.Timestamp, _dt.datetime, _dt.date)):
        # pd.Timestamp is also datetime-like; isoformat is JSON-safe
        return x.isoformat()

    # pandas NA / numpy NaN
    try:
        if pd.isna(x):
            return None
    except Exception:
        pass

    # Fallback: string representation (last resort, keeps file writable)
    return str(x)


def write_sequences_json(
    data: Union["RawData", "DataRec"],
    filepath: str,
    *,
    item_col: str = "item",
    rating_col: str = "rating",
    timestamp_col: str = "timestamp",
    include_rating: bool = False,
    include_timestamp: bool = False,
    ensure_ascii: bool = False,
    indent: Optional[int] = 2,
    verbose: bool = True,
) -> None:
    """
    Writes sequential interaction data to a JSON mapping in the form:

        {
          "<user_id>": [
            { "<item_col>": ..., "<rating_col>": ..., "<timestamp_col>": ... },
            ...
          ],
          ...
        }

    Notes:
    - The input is expected to be transactional RawData (one row per interaction).
    - User identifiers become JSON object keys (strings). Therefore, the output does
      NOT contain a user field name (no `user_col` parameter).

    Args:
        data: RawData or DataRec instance.
        filepath: Output path.
        item_col: Output key for the item field inside each event.
        rating_col: Output key for the rating field inside each event (only if include_rating=True).
        timestamp_col: Output key for the timestamp field inside each event (only if include_timestamp=True).
        include_rating: Whether to include rating in each event.
        include_timestamp: Whether to include timestamp in each event.
        ensure_ascii: Whether to escape non-ascii characters.
        indent: Pretty-print indentation level.
        verbose: Whether to print a confirmation message.

    Returns:
        None
    """
    raw = as_rawdata(data)

    if raw.user is None:
        raise ValueError("RawData.user is not defined.")
    if raw.item is None:
        raise ValueError("RawData.item is not defined.")
    if include_rating and raw.rating is None:
        raise ValueError("include_rating=True but RawData.rating is not defined.")
    if include_timestamp and raw.timestamp is None:
        raise ValueError("include_timestamp=True but RawData.timestamp is not defined.")

    cols: List[object] = [raw.user, raw.item]
    if include_rating:
        cols.append(raw.rating)  # type: ignore[arg-type]
    if include_timestamp:
        cols.append(raw.timestamp)  # type: ignore[arg-type]

    df = raw.data[cols].dropna(subset=[raw.user, raw.item])

    payload: Dict[str, List[Dict[str, Any]]] = {}

    # Preserve order of appearance
    for uid, g in df.groupby(raw.user, sort=False):
        # Build event dicts in a vectorized-ish way
        g2 = g.rename(columns={raw.item: item_col})

        keep_cols = [item_col]
        if include_rating:
            g2 = g2.rename(columns={raw.rating: rating_col})  # type: ignore[arg-type]
            keep_cols.append(rating_col)
        if include_timestamp:
            g2 = g2.rename(columns={raw.timestamp: timestamp_col})  # type: ignore[arg-type]
            keep_cols.append(timestamp_col)

        records = g2[keep_cols].to_dict(orient="records")

        # Make JSON-safe
        safe_events: List[Dict[str, Any]] = []
        for rec in records:
            safe_events.append({k: _json_safe(v) for k, v in rec.items()})

        payload[str(_json_safe(uid))] = safe_events

    out_dir = os.path.dirname(os.path.abspath(filepath))
    if out_dir and not os.path.exists(out_dir):
        os.makedirs(out_dir, exist_ok=True)

    with open(filepath, "w", encoding="utf-8") as f:
        json.dump(payload, f, ensure_ascii=ensure_ascii, indent=indent)

    if verbose:
        print(f"Sequences JSON mapping written to '{filepath}'")

def write_sequences_json_array(
    data: Union["RawData", "DataRec"],
    filepath: str,
    *,
    user_col: str = "user",
    item_col: str = "item",
    rating_col: str = "rating",
    timestamp_col: str = "timestamp",
    sequence_key: str = "sequence",
    include_rating: bool = False,
    include_timestamp: bool = False,
    ensure_ascii: bool = False,
    indent: Optional[int] = 2,
    verbose: bool = True,
) -> None:
    """
    Writes sequential interaction data to a JSON array format:

        [
          {
            "<user_col>": <user_id>,
            "<sequence_key>": [
              { "<item_col>": ..., "<rating_col>": ..., "<timestamp_col>": ... },
              ...
            ]
          },
          ...
        ]

    Notes:
    - The input is expected to be transactional RawData (one row per interaction).
      This writer groups interactions by user and produces a per-user sequence list.
    - Unlike the mapping format, user ids remain values (not JSON keys).

    Args:
        data: RawData or DataRec instance.
        filepath: Output path.
        user_col: Output key for the user field in each top-level object.
        item_col: Output key for the item field inside each event.
        rating_col: Output key for the rating field inside each event (only if include_rating=True).
        timestamp_col: Output key for the timestamp field inside each event (only if include_timestamp=True).
        sequence_key: Output key containing the list of events per user.
        include_rating: Whether to include rating in each event.
        include_timestamp: Whether to include timestamp in each event.
        ensure_ascii: Whether to escape non-ascii characters.
        indent: Pretty-print indentation level.
        verbose: Whether to print a confirmation message.

    Returns:
        None
    """
    raw = as_rawdata(data)

    if raw.user is None:
        raise ValueError("RawData.user is not defined.")
    if raw.item is None:
        raise ValueError("RawData.item is not defined.")
    if include_rating and raw.rating is None:
        raise ValueError("include_rating=True but RawData.rating is not defined.")
    if include_timestamp and raw.timestamp is None:
        raise ValueError("include_timestamp=True but RawData.timestamp is not defined.")

    cols: List[object] = [raw.user, raw.item]
    if include_rating:
        cols.append(raw.rating)  # type: ignore[arg-type]
    if include_timestamp:
        cols.append(raw.timestamp)  # type: ignore[arg-type]

    df = raw.data[cols].dropna(subset=[raw.user, raw.item])

    payload: List[Dict[str, Any]] = []

    for uid, g in df.groupby(raw.user, sort=False):
        g2 = g.rename(columns={raw.item: item_col})

        keep_cols = [item_col]
        if include_rating:
            g2 = g2.rename(columns={raw.rating: rating_col})  # type: ignore[arg-type]
            keep_cols.append(rating_col)
        if include_timestamp:
            g2 = g2.rename(columns={raw.timestamp: timestamp_col})  # type: ignore[arg-type]
            keep_cols.append(timestamp_col)

        records = g2[keep_cols].to_dict(orient="records")
        safe_events = [{k: _json_safe(v) for k, v in rec.items()} for rec in records]

        payload.append(
            {
                user_col: _json_safe(uid),
                sequence_key: safe_events,
            }
        )

    out_dir = os.path.dirname(os.path.abspath(filepath))
    if out_dir and not os.path.exists(out_dir):
        os.makedirs(out_dir, exist_ok=True)

    with open(filepath, "w", encoding="utf-8") as f:
        json.dump(payload, f, ensure_ascii=ensure_ascii, indent=indent)

    if verbose:
        print(f"Sequences JSON array written to '{filepath}'")
