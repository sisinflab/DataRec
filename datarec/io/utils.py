from typing import Union
from datarec.io.rawdata import RawData


def as_rawdata(data: Union["RawData", "DataRec"]) -> RawData:
    """
    Normalize input to RawData.

    Accepts:
    - RawData
    - DataRec (converted via `.to_rawdata()`)

    Returns:
        RawData

    Raises:
        TypeError: if the input cannot be converted to RawData.
    """
    if isinstance(data, RawData):
        return data

    if hasattr(data, "to_rawdata"):
        raw = data.to_rawdata()
        if isinstance(raw, RawData):
            return raw

    raise TypeError(
        "data must be a RawData or a DataRec-like object exposing `.to_rawdata()`."
    )