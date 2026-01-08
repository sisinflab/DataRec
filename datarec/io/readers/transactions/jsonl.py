from datarec.io.readers.transactions.json import read_transactions_json_base
from typing import Optional
from datarec.io.rawdata import RawData
from datarec.io.readers._decorators import annotate_rawdata_output

@annotate_rawdata_output
def read_transactions_jsonl(
    filepath: str, 
    *,
    user_col: str, 
    item_col: str, 
    rating_col: Optional[str] = None, 
    timestamp_col: Optional[str] = None,
    stream: bool = False,
    encode_ids: bool = False,
    chunksize: int = 100_000) -> RawData:
    """
    Reads a JSON Lines file and returns it as a RawData object.
    
    Arg names standardized to match read_tabular (user_col instead of user_field).

    Args:
        filepath: Path to the JSON file.
        user_col: JSON key corresponding to the user field (Required).
        item_col: JSON key corresponding to the item field (Required).
        rating_col: JSON key corresponding to the rating field.
        timestamp_col: JSON key corresponding to the timestamp field.

    Returns:
        RawData: The loaded data.
    """
    return read_transactions_json_base(
        filepath,
        user_col=user_col,
        item_col=item_col,
        rating_col=rating_col,
        timestamp_col=timestamp_col,
        lines=True,
        stream=stream,
        encode_ids=encode_ids,
        chunksize=chunksize,
    )
