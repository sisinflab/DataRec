from typing import Union
import pandas as pd
from datarec import DataRec
from datarec.processing.processor import Processor


class KCore:

    """
    This class filters a dataset based on a minimum number of records (core) for each group
    defined by a specific column.
    """
    
    def __init__(self, column: str, core: int):
        """
        Initializes the KCore object.
        
        Args:
            column (str): The column name used to group the data (e.g., user or item).
            core (int): The minimum number of records required for each group to be kept.
            
        Raises:
            TypeError: If 'core' is not an integer.
        """

        if not isinstance(core, int):
            raise TypeError('Core must be an integer.')

        self._column = column
        self._core = core

    def run(self, dataset: pd.DataFrame) -> pd.DataFrame:
        """
        Filters the dataset by keeping only groups with at least the specified number of records.

        Args:
            dataset (pd.DataFrame): The dataset to be filtered.

        Returns:
            (pd.DataFrame): A new dataframe with groups filtered by the core condition.
        
        Raises: 
            ValueError: If 'self._column' is not in the dataset.
        
        """

        if self._column not in dataset.columns:
            raise ValueError(f'Column "{self._column}" not in the dataset.')

        dataset = dataset.copy()
        groups = dataset.groupby([self._column])
        dataset = groups.filter(lambda x: len(x) >= self._core)
        return dataset


class UserKCore(Processor):
    """
    Filters a dataset based on a minimum number of records (core) for each user.
    
    This class applies a KCore filter on the user column of the dataset.
    """
    def __init__(self, core: int):
        """
        Initializes the UserKCore object.
        
        Args:
            core (int): The minimum number of records required for each user to be kept.
            
        Raises: 
            TypeErrore: If 'core' is not an integer.
        """
        if not isinstance(core, int):
            raise TypeError('Core must be an integer.')

        self.params = {k: v for k, v in locals().items() if k != 'self'}

        self.core = core

    def run(self, datarec: DataRec) -> DataRec:
        """
        Filters the dataset by user, applying the KCore filter, and returns a new DataRec object
        containing the filtered data.

        Args:
            datarec (DataRec): The DataRec object containing the dataset to be filtered.

        Returns:
            (DataRec): A new DataRec object with the filtered data.

        """

        core_obj = KCore(column=datarec.user_col, core=self.core)
        result = core_obj.run(datarec.data)

        return self.output(datarec, result, {'operation': self.__class__.__name__, 'params': self.params})


class ItemKCore(Processor):
    """
    Filters a dataset based on a minimum number of records (core) for each item.

    This class applies a KCore filter on the item column of the dataset.
    """
    def __init__(self, core: int):
        """
        Initializes the ItemKCore object.

        Args:
            core (int): The minimum number of records required for each item to be kept.
            
        Raises:
            TypeError: If "core" is not an integer.
        """

        if not isinstance(core, int):
            raise TypeError('Core must be an integer.')

        self.params = {k: v for k, v in locals().items() if k != 'self'}

        self.core = core

    def run(self, datarec: DataRec) -> DataRec:
        """
        Filters the dataset by item, applying the KCore filter, and returns a new DataRec object
        containing the filtered data.

        Args:
            datarec (DataRec): The DataRec object containing the dataset to be filtered.

        Returns:
            (DataRec): A new DataRec object with the filtered data.
        """

        core_obj = KCore(column=datarec.item_col, core=self.core)
        result = core_obj.run(datarec.data)

        return self.output(datarec, result, {'operation': self.__class__.__name__, 'params': self.params})


class IterativeKCore:
    """        
    Iteratively filters a dataset based on a set of columns and minimum core values.

    This class applies KCore filters to multiple columns and iteratively removes groups
    that do not meet the core requirement until no further changes occur.
    """
    def __init__(self, columns: list, cores: Union[int, list]):
        """
        Initializes the IterativeKCore object.

        Args:
            columns (list): A list of column names to apply the KCore filter on.
            cores (list of int or int): The minimum number of records required for each column to be kept.
        
        Raises:
            TypeError: If 'cores' in not a list or an integer.
        """

        self._columns = columns

        if isinstance(cores, list):
            self._cores = list(zip(columns, cores))
        elif isinstance(cores, int):
            self._cores = [(c, cores) for c in columns]
        else:
            raise TypeError('Cores must be a list or an integer.')

    def run(self, dataset: pd.DataFrame) -> pd.DataFrame:
        """
        Iteratively applies the KCore filters on the dataset until no changes occur, then returns the filtered dataset.

        Args:
            dataset (pd.DataFrame): The dataset to be iteratively filtered.

        Returns:
            (pd.DataFrame): The filtered dataset after all iterations.
        """

        data = dataset.copy()

        filters = {c: KCore(column=c, core=k) for c, k in self._cores}
        checks = [False for _ in self._columns]
        prev_len = len(data)

        while not all(checks):
            checks = []
            for c, f in filters.items():
                data = f.run(data)
                checks.append((prev_len - len(data)) == 0)
                prev_len = len(data)

        return data


class UserItemIterativeKCore(Processor):

    """
    Iteratively filters a dataset based on both user and item columns with specified core values.

    This class applies the IterativeKCore filter to both the user and item columns of the dataset.
    """
    def __init__(self, user_core: int = None, item_core: int = None,
                 cores: Union[int, list, None] = None):
        """
        Initializes the UserItemIterativeKCore object.
        
        Args:
            user_core (int): The minimum number of interactions required per user.
            item_core (int): The minimum number of interactions required per item.
            cores (list or int, optional): Legacy parameter. A list of core values for user and item
                columns, or a single int for both.
            
        Raises:
            TypeError: If core values are missing or invalid.
        """

        if user_core is None and item_core is None and cores is None:
            raise TypeError('User and item cores must be provided.')

        if user_core is None and item_core is None and cores is not None:
            if isinstance(cores, list):
                if len(cores) != 2:
                    raise TypeError('Cores list must contain exactly two elements.')
                user_core, item_core = cores
            elif isinstance(cores, int):
                user_core = cores
                item_core = cores
            else:
                raise TypeError('Cores must be a list or an integer.')

        self.params = {k: v for k, v in locals().items() if k != 'self'}
        if user_core is not None or item_core is not None:
            self.params.pop('cores', None)

        if not isinstance(user_core, int) or not isinstance(item_core, int):
            raise TypeError('User and item cores must be integers.')

        self._user_core = user_core
        self._item_core = item_core

    def run(self, datarec: DataRec) -> DataRec:
        """
        Applies the iterative KCore filter to both user and item columns, and returns a new DataRec object
        containing the filtered data.

        Args:
            datarec (DataRec): The DataRec object containing the dataset to be filtered.

        Returns:
            (DataRec): A new DataRec object with the filtered data.
        """

        core_obj = IterativeKCore(columns=[datarec.user_col, datarec.item_col],
                                  cores=[self._user_core, self._item_core])
        result = core_obj.run(datarec.data)

        return self.output(datarec, result, {'operation': self.__class__.__name__, 'params': self.params})


class NRoundsKCore:
    """
    Filters a dataset based on a minimum number of records (core) for each column over multiple rounds.

    This class applies KCore filters iteratively over a specified number of rounds.
    """
    
    def __init__(self, columns: list, cores: Union[int, list], rounds: int):
        """
        Initializes the NRoundsKCore object.
        
        Args:
            columns (list): A list of column names to apply the KCore filter on.
            cores (list of int or int): The minimum number of records required for each column to be kept.
            rounds (int): The number of rounds to apply the filtering process.

        Raises:
            TypeError: If 'cores' is not a list or an integer.
            TypeError: If 'rounds' is not an integer.
        """

        self._columns = columns

        if isinstance(cores, list):
            self._cores = list(zip(columns, cores))
        elif isinstance(cores, int):
            self._cores = [(c, cores) for c in columns]
        else:
            raise TypeError('Cores must be a list or an integer.')

        if not isinstance(rounds, int):
            raise TypeError('Rounds must be an integer.')

        self._rounds = rounds

    def run(self, dataset: pd.DataFrame) -> pd.DataFrame:
        """
        Applies the KCore filters over the specified number of rounds and returns the filtered dataset.

        Args:
            dataset (pd.DataFrame): The dataset to be filtered.

        Returns:
            (pd.DataFrame): The dataset after filtering over the specified number of rounds.
        """

        data = dataset.copy()

        filters = {c: KCore(column=c, core=k) for c, k in self._cores}
        checks = [False for _ in self._columns]
        prev_len = len(data)

        for _ in range(self._rounds) or all(checks):
            checks = []
            for c, f in filters.items():
                data = f.run(data)
                checks.append((prev_len - len(data)) == 0)
                prev_len = len(data)
        return data


class UserItemNRoundsKCore(Processor):

    """
    Filters a dataset based on both user and item columns with specified core values over multiple rounds.

    This class applies the NRoundsKCore filter to both the user and item columns of the dataset.
    """
    
    def __init__(self, rounds: int, user_core: int = None, item_core: int = None,
                 cores: Union[int, list, None] = None):
        """
        Initializes the UserItemNRoundsKCore object.
        
        Args:
            rounds (int): The number of rounds to apply the filtering process.
            user_core (int): The minimum number of interactions required per user.
            item_core (int): The minimum number of interactions required per item.
            cores (int, list, optional): Legacy parameter. A list of core values for user and item
                columns, or a single int for both.
        
        Raises:
            TypeError: If core values are missing or invalid.
            TypeError: If 'rounds' is not an integer.
        """

        if user_core is None and item_core is None and cores is None:
            raise TypeError('User and item cores must be provided.')

        if user_core is None and item_core is None and cores is not None:
            if isinstance(cores, list):
                if len(cores) != 2:
                    raise TypeError('Cores list must contain exactly two elements.')
                user_core, item_core = cores
            elif isinstance(cores, int):
                user_core = cores
                item_core = cores
            else:
                raise TypeError('Cores must be a list or an integer.')

        if not isinstance(rounds, int):
            raise TypeError('Rounds must be an integer.')

        self.params = {k: v for k, v in locals().items() if k != 'self'}
        if user_core is not None or item_core is not None:
            self.params.pop('cores', None)

        if not isinstance(user_core, int) or not isinstance(item_core, int):
            raise TypeError('User and item cores must be integers.')

        self._user_core = user_core
        self._item_core = item_core
        self._rounds = rounds

    def run(self, datarec: DataRec) -> DataRec:
        """
        Applies the NRoundsKCore filter to both user and item columns over multiple rounds, and returns a new DataRec object
        containing the filtered data.

        Args:
            datarec (DataRec): The DataRec object containing the dataset to be filtered.

        Returns:
            (DataRec): A new DataRec object with the filtered data.
        """

        core_obj = NRoundsKCore(columns=[datarec.user_col, datarec.item_col],
                                cores=[self._user_core, self._item_core], rounds=self._rounds)
        result = core_obj.run(datarec.data)

        return self.output(datarec, result, {'operation': self.__class__.__name__, 'params': self.params})
