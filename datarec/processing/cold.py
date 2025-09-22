from datarec import DataRec, RawData
from datarec.processing.processor import Processor


class ColdFilter(Processor):
    """
    A filtering class to retain only cold users or cold items, i.e., those with at most `interactions` interactions
    in the original DataRec dataset.
    """

    def __init__(self, interactions: int, mode: str = "user"):
        """
        Initializes the ColdFilter object.

        Args:
            interactions (int): The maximum number of interactions a user or item can have to be retained.
            mode (str): Filtering mode, either "user" for cold users or "item" for cold items.

        Raises:
            TypeError: If `interactions` is not an integer.
            ValueError: If `mode` is not "user" or "item".
        """
        if not isinstance(interactions, int):
            raise TypeError('Interactions must be an integer.')

        if mode not in {"user", "item"}:
            raise ValueError('Mode must be "user" or "item".')

        self.params = {k: v for k, v in locals().items() if k != 'self'}

        self.interactions = interactions
        self.mode = mode

    def run(self, datarec: DataRec) -> DataRec:
        """
        Filters the dataset to keep only cold users or cold items with at most `self.interactions` interactions.

        Args:
            datarec (DataRec): The input dataset wrapped in a DataRec object.

        Returns:
            (DataRec): A new DataRec object containing only the filtered users or items.
        """

        dataset = datarec.data.copy()
        group_col = datarec.user_col if self.mode == "user" else datarec.item_col
        groups = dataset.groupby(group_col)
        result = groups.filter(lambda x: len(x) <= self.interactions).reset_index(drop=True)

        return self.output(datarec, result, {'operation': self.__class__.__name__, 'params': self.params})

