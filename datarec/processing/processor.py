import inspect

import pandas as pd
from datarec import DataRec
from datarec.io import RawData


class Processor:
    """
    Utility class for handling the output of preprocessing steps on `DataRec` 
    objects.

    This class provides functionality to build a new `DataRec` from 
    transformation results while updating the processing pipeline accordingly.
    """
    
    @staticmethod
    def output(datarec: DataRec, result: pd.DataFrame, step_info: dict) -> DataRec:
        """
        Create a new `DataRec` object from a transformation result and update 
        the processing pipeline with a new step.

        Args:
            datarec (DataRec): The original `DataRec` object from which the 
                transformation is derived.
            result (pd.DataFrame): The result of the transformation.
            step_info (dict): Metadata of the transformation.

        Returns:
            (DataRec): A new `DataRec` object wrapping the transformation result
                with an updated pipeline.
        """
        pipeline = datarec.pipeline.copy()
        pipeline.add_step(name='process', operation=step_info['operation'], params=step_info['params'])

        new_datarec = DataRec(
            RawData(result,
                    user=datarec.user_col,
                    item=datarec.item_col,
                    rating=datarec.rating_col if datarec.rating_col in result.columns else None,
                    timestamp=datarec.timestamp_col),
            derives_from=datarec,
            dataset_name=datarec.dataset_name,
            version_name=datarec.version_name,
            pipeline=pipeline
        )

        return new_datarec
