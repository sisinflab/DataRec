from typing import Optional, Union, TYPE_CHECKING

from datarec.io.rawdata import RawData
from datarec.io.writers.transactions.json import write_transactions_json_base

if TYPE_CHECKING:
    from datarec.data.dataset import DataRec

def write_transactions_jsonl(
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
    ensure_ascii: bool = False,
    verbose: bool = True,
) -> None:
    """
    Writes transactional interaction data as JSON Lines (one JSON object per line).
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
        lines=True,
        indent=None,
        ensure_ascii=ensure_ascii,
        verbose=verbose,
    )
