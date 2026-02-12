import os
from typing import Optional, List, Any, Dict, Literal, cast

import pandas as pd

from datarec.io.rawdata import RawData
from datarec.io.readers._decorators import annotate_datarec_output
from datarec import DataRec


def _raise_parse_error(
    line_num: int,
    message: str,
    line: str,
    current_block: Optional[str],
    block_by: Literal["item", "user"],
) -> None:
    block_label = "item" if block_by == "item" else "user"
    block_info = f", {block_label}={current_block!r}" if current_block is not None else ""
    raise ValueError(f"Line {line_num}: {message}{block_info}. Line content: {line!r}")


@annotate_datarec_output
def read_transactions_blocks(
    filepath: str,
    *,
    block_by: Literal["item", "user"],
    event_layout: Literal["id", "id,rating", "id,rating,timestamp"],
    user_col: str = "user",
    item_col: str = "item",
    rating_col: Optional[str] = None,
    timestamp_col: Optional[str] = None,
    sep: str = "\t",
    chunksize: Optional[int] = None,
    dataset_name: str = "Unknown Dataset",
    version_name: str = "Unknown Version",
) -> DataRec:
    """
    Reads a block text format into transactional RawData.

    Block structure:
      - Header line per block: "<BLOCK_ID>:"
      - Event lines:
          - "id"
          - "id,rating"
          - "id,rating,timestamp"

    The block header identifies either the item or the user depending on
    block_by. The event line id is the opposite entity.

    Args:
        filepath: Path to the block text file.
        block_by: Whether blocks are grouped by "item" or by "user".
        event_layout: Layout of event lines.
        user_col: Output user column name.
        item_col: Output item column name.
        rating_col: Output rating column name (required if layout includes rating).
        timestamp_col: Output timestamp column name (required if layout includes timestamp).
        sep: Field separator used in event lines.
        chunksize: Optional number of rows per in-memory chunk before concatenation.
        dataset_name: Name to assign to the resulting DataRec dataset.
        version_name: Version identifier to assign to the resulting DataRec dataset.

    Returns:
        DataRec: A DataRec object containing all interactions row-by-row.
            (Returned via @annotate_datarec_output, which wraps the RawData.)
    """
    if not os.path.exists(filepath):
        raise FileNotFoundError(f"File not found: {filepath}")

    expects_rating = event_layout in ("id,rating", "id,rating,timestamp")
    expects_timestamp = event_layout == "id,rating,timestamp"

    if expects_rating and rating_col is None:
        raise ValueError("rating_col must be provided when event_layout includes rating.")
    if not expects_rating and rating_col is not None:
        raise ValueError("rating_col must be None when event_layout does not include rating.")
    if expects_timestamp and timestamp_col is None:
        raise ValueError("timestamp_col must be provided when event_layout includes timestamp.")
    if not expects_timestamp and timestamp_col is not None:
        raise ValueError("timestamp_col must be None when event_layout does not include timestamp.")

    frames: List[pd.DataFrame] = []
    users: List[Any] = []
    items: List[Any] = []
    ratings: List[Any] = [] if rating_col is not None else []
    timestamps: List[Any] = [] if timestamp_col is not None else []

    current_block_id: Optional[str] = None

    def _flush() -> None:
        if not users:
            return
        data: Dict[str, List[Any]] = {
            user_col: users.copy(),
            item_col: items.copy(),
        }
        if rating_col is not None:
            data[rating_col] = ratings.copy()
        if timestamp_col is not None:
            data[timestamp_col] = timestamps.copy()
        frames.append(pd.DataFrame(data))
        users.clear()
        items.clear()
        timestamps.clear()
        if rating_col is not None:
            ratings.clear()

    with open(filepath, "r", encoding="utf-8") as f:
        for line_num, raw_line in enumerate(f, start=1):
            line = raw_line.rstrip("\n")
            if line == "":
                _raise_parse_error(
                    line_num,
                    "Empty lines are not allowed",
                    raw_line,
                    current_block_id,
                    block_by,
                )

            stripped = line.strip()
            if stripped.endswith(":"):
                block_id = stripped[:-1].strip()
                if not block_id:
                    _raise_parse_error(
                        line_num,
                        "Missing block id in header",
                        raw_line,
                        current_block_id,
                        block_by,
                    )
                current_block_id = block_id
                continue

            if current_block_id is None:
                _raise_parse_error(
                    line_num,
                    "Event found before any block header",
                    raw_line,
                    current_block_id,
                    block_by,
                )

            parts = [p.strip() for p in line.split(sep)]
            if event_layout == "id":
                expected_fields = 1
            elif event_layout == "id,rating":
                expected_fields = 2
            else:
                expected_fields = 3
            if len(parts) != expected_fields:
                _raise_parse_error(
                    line_num,
                    f"Expected {expected_fields} fields separated by {sep!r}, got {len(parts)}",
                    raw_line,
                    current_block_id,
                    block_by,
                )

            other_id = parts[0]
            if event_layout == "id":
                rating_val = None
                date_val = None
            elif event_layout == "id,rating":
                rating_val = parts[1]
                date_val = None
            else:
                rating_val = parts[1]
                date_val = parts[2]

            if block_by == "item":
                users.append(other_id)
                items.append(current_block_id)
            else:
                users.append(current_block_id)
                items.append(other_id)

            if timestamp_col is not None:
                timestamps.append(date_val)
            if rating_col is not None:
                ratings.append(rating_val)

            if chunksize is not None and len(users) >= chunksize:
                _flush()

    _flush()

    if frames:
        data = pd.concat(frames, ignore_index=True)
    else:
        data_dict: Dict[str, List[Any]] = {
            user_col: users,
            item_col: items,
        }
        if rating_col is not None:
            data_dict[rating_col] = ratings
        if timestamp_col is not None:
            data_dict[timestamp_col] = timestamps
        data = pd.DataFrame(data_dict)

    raw = RawData(
        data,
        user=user_col,
        item=item_col,
        rating=rating_col,
        timestamp=timestamp_col,
    )

    # Wrapped by @annotate_datarec_output to return DataRec at call sites.
    return cast(DataRec, raw)
