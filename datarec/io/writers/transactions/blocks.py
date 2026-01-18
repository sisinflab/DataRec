import os
import math
import datetime as _dt
from typing import Union, TYPE_CHECKING, Literal

import pandas as pd

from datarec.io.rawdata import RawData
from datarec.io.utils import as_rawdata

if TYPE_CHECKING:
    from datarec.data.dataset import DataRec


def _stringify(value: object) -> str:
    if value is None:
        return ""
    if isinstance(value, float):
        if math.isnan(value) or math.isinf(value):
            return ""
    if isinstance(value, (pd.Timestamp, _dt.datetime, _dt.date)):
        return value.isoformat()
    return str(value)


def write_transactions_blocks(
    data: Union["RawData", "DataRec"],
    filepath: str,
    *,
    block_by: Literal["item", "user"],
    event_layout: Literal["id", "id,rating", "id,rating,timestamp"],
    include_user: bool = True,
    include_item: bool = True,
    include_rating: bool = False,
    include_timestamp: bool = False,
    sep: str = "\t",
    verbose: bool = True,
) -> None:
    """
    Writes transactional interaction data to a block text format:

        <BLOCK_ID>:
        id
        id,rating
        id,rating,timestamp

    The block header identifies either the item or the user depending on
    block_by. The event line id is the opposite entity.

    Args:
        data: RawData or DataRec instance.
        filepath: Output path.
        block_by: Whether blocks are grouped by "item" or by "user".
        event_layout: Layout of event lines.
        include_user: Must be True.
        include_item: Must be True.
        include_rating: Must be True if event_layout includes rating.
        include_timestamp: Must be True if event_layout includes timestamp.
        sep: Field separator used in event lines.
        verbose: Whether to print a confirmation message.
    """
    raw = as_rawdata(data)

    if not include_user:
        raise ValueError("Block format requires include_user=True.")
    if not include_item:
        raise ValueError("Block format requires include_item=True.")
    expects_rating = event_layout in ("id,rating", "id,rating,timestamp")
    expects_timestamp = event_layout == "id,rating,timestamp"
    if expects_rating and not include_rating:
        raise ValueError("event_layout includes rating; include_rating must be True.")
    if not expects_rating and include_rating:
        raise ValueError("event_layout does not include rating; include_rating must be False.")
    if expects_timestamp and not include_timestamp:
        raise ValueError("event_layout includes timestamp; include_timestamp must be True.")
    if not expects_timestamp and include_timestamp:
        raise ValueError("event_layout does not include timestamp; include_timestamp must be False.")

    if raw.user is None:
        raise ValueError("RawData.user is not defined.")
    if raw.item is None:
        raise ValueError("RawData.item is not defined.")
    if expects_timestamp and raw.timestamp is None:
        raise ValueError("RawData.timestamp is not defined but event_layout requires timestamp.")
    if expects_rating and raw.rating is None:
        raise ValueError("RawData.rating is not defined but event_layout requires rating.")

    cols = [raw.user, raw.item]
    if expects_rating:
        cols.append(raw.rating)  # type: ignore[arg-type]
    if expects_timestamp:
        cols.append(raw.timestamp)

    df = raw.data[cols]

    if df[raw.user].isna().any():
        raise ValueError("User column contains missing values; cannot write block format.")
    if df[raw.item].isna().any():
        raise ValueError("Item column contains missing values; cannot write block format.")
    if expects_timestamp and df[raw.timestamp].isna().any():  # type: ignore[index]
        raise ValueError("Timestamp column contains missing values; cannot write block format.")
    if expects_rating and df[raw.rating].isna().any():  # type: ignore[index]
        raise ValueError("Rating column contains missing values; cannot write block format.")

    if block_by == "item":
        block_col = raw.item
        other_col = raw.user
    else:
        block_col = raw.user
        other_col = raw.item

    out_dir = os.path.dirname(os.path.abspath(filepath))
    if out_dir and not os.path.exists(out_dir):
        os.makedirs(out_dir, exist_ok=True)

    with open(filepath, "w", encoding="utf-8") as f:
        for block_id, g in df.groupby(block_col, sort=False):
            f.write(f"{_stringify(block_id)}:\n")
            if event_layout == "id":
                g2 = g[[other_col]]
                for (other_id,) in g2.itertuples(index=False, name=None):
                    f.write(f"{_stringify(other_id)}\n")
            elif event_layout == "id,rating":
                g2 = g[[other_col, raw.rating]]  # type: ignore[list-item]
                for other_id, rating_val in g2.itertuples(index=False, name=None):
                    f.write(f"{_stringify(other_id)}{sep}{_stringify(rating_val)}\n")
            else:
                g2 = g[[other_col, raw.rating, raw.timestamp]]  # type: ignore[list-item]
                for other_id, rating_val, ts_val in g2.itertuples(index=False, name=None):
                    f.write(
                        f"{_stringify(other_id)}{sep}{_stringify(rating_val)}{sep}{_stringify(ts_val)}\n"
                    )

    if verbose:
        print(f"Block transactions written to '{filepath}'")
