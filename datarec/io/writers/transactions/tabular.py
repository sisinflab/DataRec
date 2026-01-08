import os
from typing import Optional, Union, List, Dict, TYPE_CHECKING
from datarec.io.rawdata import RawData
from datarec.io.utils import as_rawdata

if TYPE_CHECKING:
    from datarec.data.dataset import DataRec


def write_transactions_tabular(
    data: Union["RawData", "DataRec"],
    filepath: str,
    *,
    sep: str = "\t",
    header: bool = True,
    decimal: str = ".",
    include_user: bool = True,
    include_item: bool = True,
    include_rating: bool = False,
    include_timestamp: bool = False,
    user_col: Optional[str] = None,
    item_col: Optional[str] = None,
    rating_col: Optional[str] = None,
    timestamp_col: Optional[str] = None,
    index: bool = False,
    engine: Optional[str] = None,
    verbose: bool = True,
) -> None:
    """
    Writes transactional interaction data to a tabular file (CSV/TSV/etc.).

    Output format: one interaction per row
        user, item, [rating], [timestamp]

    This writer accepts either:
    - RawData
    - DataRec (converted via `.to_rawdata()`)

    Args:
        data: RawData or DataRec instance.
        filepath: Output path.
        sep: Column delimiter (e.g., '\\t', ',', ';').
        header: Whether to write column names.
        decimal: Decimal separator passed to pandas.
        include_user: Whether to include the user column.
        include_item: Whether to include the item column.
        include_rating: Whether to include the rating column (if available).
        include_timestamp: Whether to include the timestamp column (if available).
        user_col: Output column name for user (optional rename).
        item_col: Output column name for item (optional rename).
        rating_col: Output column name for rating (optional rename).
        timestamp_col: Output column name for timestamp (optional rename).
        index: Whether to write the DataFrame index.
        engine: Optional pandas CSV engine hint.
        verbose: Whether to print a confirmation message.

    Returns:
        None
    """
    raw = as_rawdata(data)

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
    rename_map: Dict[object, str] = {}

    if user_col is not None:
        rename_map[raw.user] = user_col
    if item_col is not None:
        rename_map[raw.item] = item_col

    if include_rating:
        if raw.rating is None:
            raise ValueError("Rating column requested but not defined in RawData.")
        cols.append(raw.rating)
        if rating_col is not None:
            rename_map[raw.rating] = rating_col

    if include_timestamp:
        if raw.timestamp is None:
            raise ValueError("Timestamp column requested but not defined in RawData.")
        cols.append(raw.timestamp)
        if timestamp_col is not None:
            rename_map[raw.timestamp] = timestamp_col

    df = raw.data[cols]
    if rename_map:
        df = df.rename(columns=rename_map)

    out_dir = os.path.dirname(os.path.abspath(filepath))
    if out_dir and not os.path.exists(out_dir):
        os.makedirs(out_dir, exist_ok=True)

    to_csv_kwargs = dict(sep=sep, header=header, index=index, decimal=decimal)
    if engine is not None:
        to_csv_kwargs["engine"] = engine

    df.to_csv(filepath, **to_csv_kwargs)

    if verbose:
        print(f"Tabular dataset written to '{filepath}'")
