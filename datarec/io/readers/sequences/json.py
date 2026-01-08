import os
import json
import pandas as pd
from typing import Optional, Dict, Any, List
from datarec.io.rawdata import RawData
from datarec.io.readers._decorators import annotate_rawdata_output

@annotate_rawdata_output
def read_sequences_json(
    filepath: str,
    *,
    user_col: str = "user",
    item_col: str = "item",
    rating_col: Optional[str] = None,
    timestamp_col: Optional[str] = None,
) -> RawData:
    """
    Reads a JSON file representing sequential interaction data in the form:
    
    {
      "user_id": [
        { "item": ..., "rating": ..., "timestamp": ... },
        ...
      ],
      ...
    }

    Converts it into a transactional RawData format with one row per interaction.

    Args:
        filepath: Path to the JSON file.
        user_col: Name assigned to the user column in the output.
        item_col: Key containing the item field inside each event.
        rating_col: Key containing the rating field inside each event.
        timestamp_col: Key containing the timestamp field inside each event.

    Returns:
        RawData: A RawData object containing all interactions exploded row-by-row.
    """
    if not os.path.exists(filepath):
        raise FileNotFoundError(f"File not found: {filepath}")

    # Load the entire JSON structure
    with open(filepath, "r", encoding="utf-8") as f:
        payload: Dict[str, Any] = json.load(f)

    rows = []

    # Iterate over each user and their list of events
    for user_id, events in payload.items():
        if not isinstance(events, list):
            raise ValueError(f"Expected a list of events for user '{user_id}', got {type(events)}.")

        for event in events:
            # Extract required fields
            row = {user_col: user_id}

            # Mandatory
            if item_col not in event:
                raise ValueError(f"Missing item field '{item_col}' in event for user {user_id}.")
            row[item_col] = event[item_col]

            # Optional
            if rating_col is not None:
                row[rating_col] = event.get(rating_col)
            if timestamp_col is not None:
                row[timestamp_col] = event.get(timestamp_col)

            rows.append(row)

    # Build DataFrame
    data = pd.DataFrame(rows)

    # Reset index for consistency
    data = data.reset_index(drop=True)

    # Final RawData object
    raw = RawData(
        data,
        user=user_col,
        item=item_col,
        rating=rating_col,
        timestamp=timestamp_col,
    )

    return raw

@annotate_rawdata_output
def read_sequences_json_array(
    filepath: str,
    *,
    user_col: str = "user",
    item_col: str = "item",
    rating_col: Optional[str] = None,
    timestamp_col: Optional[str] = None,
    sequence_key: str = "sequence",
) -> RawData:
    """
    Reads a JSON file representing sequential interaction data in the form
    of an ARRAY of user-sequence objects, e.g.:

        [
          {
            "user": 0,
            "sequence": [
              { "item": 1, "rating": 1, "timestamp": "001" },
              { "item": 2, "rating": 1, "timestamp": "022" }
            ]
          },
          {
            "user": 1,
            "sequence": [
              { "item": 1, "rating": 4, "timestamp": "011" }
            ]
          }
        ]

    and converts it into a transactional RawData format with one row per
    interaction.

    Args:
        filepath: Path to the JSON file.
        user_col: Name assigned to the user column in the output.
                  Also used as the key to read the user identifier in
                  each top-level object.
        item_col: Key containing the item field inside each event.
        rating_col: Key containing the rating field inside each event.
        timestamp_col: Key containing the timestamp field inside each event.
        sequence_key: Key containing the list of events for each user.

    Returns:
        RawData: A RawData object containing all interactions exploded
                 row-by-row.
    """
    if not os.path.exists(filepath):
        raise FileNotFoundError(f"File not found: {filepath}")

    # Load the entire JSON structure
    with open(filepath, "r", encoding="utf-8") as f:
        payload: Any = json.load(f)

    if not isinstance(payload, list):
        raise ValueError(
            f"Expected a JSON array at top level, got {type(payload)} instead."
        )

    rows: List[Dict[str, Any]] = []

    # Iterate over each user-level object
    for obj in payload:
        if not isinstance(obj, dict):
            raise ValueError(
                f"Expected each element of the array to be an object, got {type(obj)}."
            )

        if user_col not in obj:
            raise ValueError(
                f"Missing user field '{user_col}' in top-level object: {obj}."
            )
        user_id = obj[user_col]

        if sequence_key not in obj:
            raise ValueError(
                f"Missing sequence field '{sequence_key}' in top-level object for user {user_id}."
            )

        events = obj[sequence_key]
        if not isinstance(events, list):
            raise ValueError(
                f"Expected '{sequence_key}' to be a list for user {user_id}, "
                f"got {type(events)}."
            )

        for event in events:
            if not isinstance(event, dict):
                raise ValueError(
                    f"Expected each event in '{sequence_key}' to be an object, got {type(event)}."
                )

            row: Dict[str, Any] = {user_col: user_id}

            # Mandatory item field
            if item_col not in event:
                raise ValueError(
                    f"Missing item field '{item_col}' in event for user {user_id}: {event}."
                )
            row[item_col] = event[item_col]

            # Optional fields
            if rating_col is not None:
                row[rating_col] = event.get(rating_col)
            if timestamp_col is not None:
                row[timestamp_col] = event.get(timestamp_col)

            rows.append(row)

    # Build DataFrame
    data = pd.DataFrame(rows).reset_index(drop=True)

    # Final RawData object
    raw = RawData(
        data,
        user=user_col,
        item=item_col,
        rating=rating_col,
        timestamp=timestamp_col,
    )

    return raw
