from datarec.io.readers.transactions.json import read_transactions_json_base
from typing import Optional, cast
from datarec.io.readers._decorators import annotate_datarec_output
from datarec import DataRec

@annotate_datarec_output
def read_transactions_jsonl(
    filepath: str, 
    *,
    user_col: str, 
    item_col: str, 
    rating_col: Optional[str] = None, 
    timestamp_col: Optional[str] = None,
    stream: bool = False,
    encode_ids: bool = False,
    chunksize: int = 100_000,
    dataset_name: str = "Unknown Dataset",
    version_name: str = "Unknown Version",
) -> DataRec:
    """
    Reads a JSON Lines file and returns it as a RawData object.
    
    Arg names standardized to match read_tabular (user_col instead of user_field).

    Args:
        filepath: Path to the JSON file.
        user_col: JSON key corresponding to the user field (Required).
        item_col: JSON key corresponding to the item field (Required).
        rating_col: JSON key corresponding to the rating field.
        timestamp_col: JSON key corresponding to the timestamp field.
        dataset_name: Name to assign to the resulting DataRec dataset.
        version_name: Version identifier to assign to the resulting DataRec dataset.

    Returns:
        DataRec: The loaded data.
            (Returned via @annotate_datarec_output, which wraps the RawData.)
    """
    rawdata = read_transactions_json_base(
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
    # Wrapped by @annotate_datarec_output to return DataRec at call sites.
    return cast(DataRec, rawdata)
