import os
import inspect
from functools import wraps
from typing import Callable, TypeVar, cast
try:
    from typing import ParamSpec
except ImportError:  # Python < 3.10
    from typing_extensions import ParamSpec
from datarec.pipeline.pipeline_step import PipelineStep
from datarec.pipeline.pipeline import Pipeline
from datarec import DataRec

from datarec.io.rawdata import RawData


P = ParamSpec("P")
R = TypeVar("R")


def annotate_rawdata_output(func: Callable[P, R]) -> Callable[P, R]:
    """Attach read metadata to RawData outputs.

    Stores a PipelineStep in `raw.pipeline_step` with:
    name="read", operation=<function_name>, params=<params>, replacing `filepath`
    with `filename`.
    """
    @wraps(func)
    def wrapper(*args: P.args, **kwargs: P.kwargs):
        raw = func(*args, **kwargs)
        if isinstance(raw, RawData):
            bound = inspect.signature(func).bind_partial(*args, **kwargs)
            bound.apply_defaults()
            params = dict(bound.arguments)
            if "filepath" in params:
                params["filename"] = os.path.basename(params.pop("filepath"))
            raw.pipeline_step = PipelineStep("read", func.__name__, params)
        return cast(R, raw)
    return cast(Callable[P, R], wrapper)


def annotate_datarec_output(func: Callable[P, R]) -> Callable[P, DataRec]:
    """Attach read metadata to DataRec outputs.

    Builds a read PipelineStep from the function signature, replacing `filepath`
    with `filename`. If the wrapped function returns RawData, it is wrapped into
    a DataRec with a single-step pipeline. If it returns DataRec, the read step
    is appended to its pipeline.
    """
    @wraps(func)
    def wrapper(*args: P.args, **kwargs: P.kwargs):
        result = func(*args, **kwargs)

        bound = inspect.signature(func).bind_partial(*args, **kwargs)
        bound.apply_defaults()
        params = dict(bound.arguments)
        if "filepath" in params:
            params["filename"] = os.path.basename(params.pop("filepath"))

        pipeline_step = PipelineStep("read", func.__name__, params)
        # pipeline = Pipeline()
        # pipeline.steps.append(pipeline_step)

        if isinstance(result, RawData):
            result.pipeline_step = pipeline_step
            dataset_name = params.get("dataset_name", "datarec")
            version_name = params.get("version_name", "no_version_provided")
            return DataRec(
                rawdata=result,
                registry_dataset=False,
                dataset_name=dataset_name,
                version_name=version_name,
            )

        if isinstance(result, DataRec):
            if result.pipeline is None:
                result.pipeline = Pipeline()
                result.pipeline.steps.append(pipeline_step)
            else:
                result.pipeline.steps.append(pipeline_step)
            return result

        return cast(DataRec, result)
    return cast(Callable[P, DataRec], wrapper)
