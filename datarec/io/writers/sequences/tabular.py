import os
from typing import Optional, Union, List, Dict, Any, TYPE_CHECKING

import pandas as pd

from datarec.io.rawdata import RawData
from datarec.io.utils import as_rawdata

if TYPE_CHECKING:
    from datarec.data.dataset import DataRec


def write_sequence_tabular_inline(
    data: Union["RawData", "DataRec"],
    filepath: str,
    *,
    user_col: str = "user",
    sequence_col: str = "sequence",
    sequence_sep: str = " ",
    include_timestamp: bool = False,
    timestamp_col: str = "timestamp",
    meta_cols: Optional[List[str]] = None,
    col_sep: str = ",",
    header: bool = True,
    index: bool = False,
    decimal: str = ".",
    engine: Optional[str] = None,
    verbose: bool = True,
) -> None:
    """
    Writes sequential interaction data to a tabular file where each row contains
    a single user and a serialized sequence in one column (inline format).

    Output format (one sequence per row):
        user_col, sequence_col, [timestamp_col], [meta_cols...]

    Notes:
    - The input is expected to be transactional RawData (one row per (user, item)),
      as produced by DataRec readers. This writer groups interactions by user and
      serializes the per-user item list using `sequence_sep`.
    - If include_timestamp=True, a per-user timestamp is derived by aggregating
      RawData timestamps using a deterministic strategy (min timestamp).
    - Metadata columns (meta_cols) are aggregated per user using a deterministic
      strategy (first value).

    Args:
        data: RawData or DataRec instance.
        filepath: Output path.
        user_col: Output column name for user IDs.
        sequence_col: Output column name for the serialized sequence.
        sequence_sep: Separator used to serialize items in the sequence string.
        include_timestamp: Whether to include a per-user timestamp column.
        timestamp_col: Output column name for timestamp (used only if include_timestamp=True).
        meta_cols: Additional metadata columns to include (if present in RawData).
        col_sep: Column delimiter for the output file.
        header: Whether to write column names.
        index: Whether to write the DataFrame index.
        decimal: Decimal separator passed to pandas.
        engine: Optional pandas CSV engine hint.
        verbose: Whether to print a confirmation message.

    Returns:
        None
    """
    raw = as_rawdata(data)

    if raw.user is None:
        raise ValueError("RawData.user is not defined.")
    if raw.item is None:
        raise ValueError("RawData.item is not defined.")

    if meta_cols is None:
        meta_cols = []

    df = raw.data

    # Validate timestamp intent vs availability
    if include_timestamp:
        if raw.timestamp is None:
            raise ValueError("include_timestamp=True but RawData.timestamp is not defined.")
        if raw.timestamp not in df.columns:
            raise ValueError(f"Timestamp column '{raw.timestamp}' not found in RawData.data.")

    # Determine which meta columns are available
    available_meta = [mc for mc in meta_cols if mc in df.columns]

    # Select needed columns (no copy)
    cols_needed: List[object] = [raw.user, raw.item]
    if include_timestamp:
        cols_needed.append(raw.timestamp)  # type: ignore[arg-type]
    cols_needed.extend(available_meta)

    df = df[cols_needed].dropna(subset=[raw.user, raw.item])

    # Aggregation strategy:
    # - items: list in input order
    # - timestamp: min (deterministic)
    # - meta: first (deterministic)
    agg: Dict[object, Any] = {raw.item: list}

    if include_timestamp:
        agg[raw.timestamp] = "min"  # type: ignore[index]

    for mc in available_meta:
        agg[mc] = "first"

    grouped = df.groupby(raw.user, sort=False, dropna=False).agg(agg).reset_index()

    # Serialize sequence
    grouped[sequence_col] = grouped[raw.item].apply(
        lambda items: sequence_sep.join(str(x).strip() for x in items if str(x).strip() != "")
    )

    # Drop users with empty sequences
    grouped = grouped[grouped[sequence_col] != ""]

    # Rename user (and timestamp if requested) to output names
    rename_map: Dict[object, str] = {raw.user: user_col}
    if include_timestamp:
        rename_map[raw.timestamp] = timestamp_col  # type: ignore[index]

    grouped = grouped.rename(columns=rename_map)

    # Drop the aggregated list column (raw.item), keep only the serialized sequence
    grouped = grouped.drop(columns=[raw.item])

    # Final column order
    out_cols: List[str] = [user_col, sequence_col]
    if include_timestamp:
        out_cols.append(timestamp_col)

    # Preserve user-requested ordering for meta_cols (only those available)
    for mc in meta_cols:
        if mc in grouped.columns and mc not in out_cols:
            out_cols.append(mc)

    grouped = grouped[out_cols]

    # Ensure output directory exists
    out_dir = os.path.dirname(os.path.abspath(filepath))
    if out_dir and not os.path.exists(out_dir):
        os.makedirs(out_dir, exist_ok=True)

    to_csv_kwargs = dict(sep=col_sep, header=header, index=index, decimal=decimal)
    if engine is not None:
        to_csv_kwargs["engine"] = engine

    grouped.to_csv(filepath, **to_csv_kwargs)

    if verbose:
        print(f"Inline sequence dataset written to '{filepath}'")

def write_sequence_tabular_wide(
    data: Union["RawData", "DataRec"],
    filepath: str,
    *,
    user_col: str = "user",
    item_col_prefix: str = "item",
    col_sep: str = "\t",
    header: bool = False,
    index: bool = False,
    decimal: str = ".",
    verbose: bool = True,
) -> None:
    """
    Writes sequential interaction data to a tabular-wide format, where each row
    corresponds to a user and items are spread across multiple columns.

    Output example:
        user <sep> item_1 <sep> item_2 <sep> item_3

    Args:
        data: RawData or DataRec instance.
        filepath: Output path.
        user_col: Output column name for user IDs.
        item_col_prefix: Prefix for item columns (e.g., item_1, item_2, ...).
        col_sep: Column delimiter.
        header: Whether to write column names.
        index: Whether to write the DataFrame index.
        decimal: Decimal separator.
        verbose: Whether to print a confirmation message.

    Returns:
        None
    """
    raw = as_rawdata(data)

    if raw.user is None or raw.item is None:
        raise ValueError("RawData must define both user and item columns.")

    df = raw.data[[raw.user, raw.item]].dropna()

    # Preserve order of appearance
    grouped = (
        df.groupby(raw.user, sort=False)[raw.item]
        .apply(list)
        .reset_index()
    )

    # Build wide DataFrame
    max_len = grouped[raw.item].map(len).max()

    wide_items = pd.DataFrame(
        grouped[raw.item].tolist(),
        columns=[f"{item_col_prefix}_{i+1}" for i in range(max_len)],
    )

    out_df = pd.concat(
        [
            grouped[[raw.user]].rename(columns={raw.user: user_col}),
            wide_items,
        ],
        axis=1,
    )

    out_dir = os.path.dirname(os.path.abspath(filepath))
    if out_dir and not os.path.exists(out_dir):
        os.makedirs(out_dir, exist_ok=True)

    out_df.to_csv(
        filepath,
        sep=col_sep,
        header=header,
        index=index,
        decimal=decimal,
    )

    if verbose:
        print(f"Wide sequence dataset written to '{filepath}'")


def write_sequence_tabular_implicit(
    data: Union["RawData", "DataRec"],
    filepath: str,
    *,
    include_length_col: bool = True,
    col_sep: str = " ",
    header: bool = False,
    verbose: bool = True,
) -> None:
    """
    Writes sequential interaction data to a tabular-implicit format, where each row
    represents a sequence and no explicit user identifier is written.

    Output example (include_length_col=True, col_sep=" "):
        3 10 20 30
        2 11 42

    Notes:
    - Each unique user in RawData is treated as a sequence instance.
    - The user identifier is NOT written to file.
    - If include_length_col=True, the first token is the sequence length.

    Args:
        data: RawData or DataRec instance.
        filepath: Output path.
        include_length_col: Whether to prepend the sequence length token.
        col_sep: Token separator used within each row (must match the reader's `col_sep`).
        header: Whether to write a header row (generally False for this format).
        verbose: Whether to print a confirmation message.

    Returns:
        None
    """
    raw = as_rawdata(data)

    if raw.user is None or raw.item is None:
        raise ValueError("RawData must define both user and item columns.")

    df = raw.data[[raw.user, raw.item]].dropna(subset=[raw.user, raw.item])

    grouped = (
        df.groupby(raw.user, sort=False)[raw.item]
        .apply(list)
        .reset_index(drop=True)
    )

    rows = []
    for items in grouped:
        items_str = [str(x).strip() for x in items if str(x).strip() != ""]
        if not items_str:
            continue
        if include_length_col:
            row_tokens = [str(len(items_str))] + items_str
        else:
            row_tokens = items_str
        rows.append(col_sep.join(row_tokens))

    if not rows:
        raise ValueError("No valid sequences to write.")

    out_dir = os.path.dirname(os.path.abspath(filepath))
    if out_dir and not os.path.exists(out_dir):
        os.makedirs(out_dir, exist_ok=True)

    with open(filepath, "w", encoding="utf-8") as f:
        if header:
            # This format typically has no header; if requested, write a minimal one.
            f.write("sequence\n")
        for row in rows:
            f.write(row + "\n")

    if verbose:
        print(f"Implicit sequence dataset written to '{filepath}'")
