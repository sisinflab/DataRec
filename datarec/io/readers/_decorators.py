import os
import inspect
from functools import wraps
from typing import Callable
from datarec.pipeline.pipeline_step import PipelineStep

from datarec.io.rawdata import RawData


def annotate_rawdata_output(func: Callable) -> Callable:
    """Attach read metadata to RawData outputs.

    Stores a PipelineStep in `raw.pipeline_step` with:
    name="read", operation=<function_name>, params=<params>, replacing `filepath`
    with `filename`.
    """
    @wraps(func)
    def wrapper(*args, **kwargs):
        raw = func(*args, **kwargs)
        if isinstance(raw, RawData):
            bound = inspect.signature(func).bind_partial(*args, **kwargs)
            bound.apply_defaults()
            params = dict(bound.arguments)
            if "filepath" in params:
                params["filename"] = os.path.basename(params.pop("filepath"))
            raw.pipeline_step = PipelineStep("read", func.__name__, params)
        return raw
    return wrapper
