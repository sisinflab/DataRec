import math
import warnings

import pandas as pd
import numpy as np
from typing import Union, Optional
from collections import Counter
from .utils import set_column_name, quartiles, popularity
from datarec.io.rawdata import RawData
from datarec.pipeline import Pipeline

DATAREC_USER_COL = 'user_id'
DATAREC_ITEM_COL = 'item_id'
DATAREC_RATING_COL = 'rating'
DATAREC_TIMESTAMP_COL = 'timestamp'


class DataRec:

    """
    Core data structure for recommendation datasets in the DataRec framework.

    This class wraps a Pandas DataFrame and standardizes common columns
    (user, item, rating, timestamp) to provide a consistent interface
    for recommendation tasks. It supports data preprocessing, 
    user/item remapping (public vs private IDs), frequency analysis, 
    sparsity/density metrics, Gini coefficients, and conversion into 
    PyTorch datasets for training.
    """
    
    def __init__(
            self,
            rawdata: RawData = None,
            copy: bool = False,
            dataset_name: str = 'datarec',
            version_name: str = 'no_version_provided',
            pipeline: Optional[Pipeline] = None,
            *args,
            **kwargs
    ):
        """
        Initializes the DataRec object.
            
        Args:
            rawdata (RawData): The input dataset wrapped in a RawData object.
                If None, the DataRec is initialized empty.
            copy (bool): Whether to copy the input DataFrame to avoid 
                modifying the original RawData.
            dataset_name (str): A name to identify the dataset.
            version_name (str): A version identifier 
                for the dataset.
            pipeline (Pipeline): A pipeline object to track preprocessing steps.
            
        """


        
        self.path = None
        self._data = None
        self.dataset_name = dataset_name
        self.version_name = version_name

        if pipeline:
            self.pipeline = pipeline
        else:
            self.pipeline = Pipeline()
            self.pipeline.add_step("load", self.dataset_name, {'version': self.version_name})

        if rawdata is not None:
            if copy:
                self._data: pd.DataFrame = rawdata.data.copy()
            else:
                self._data: pd.DataFrame = rawdata.data

        # ------------------------------------
        # --------- STANDARD COLUMNS ---------
        # if a column is None it means that the DataRec does not have that information
        self.__assigned_columns = []

        self._user_col = None
        self._item_col = None
        self._rating_col = None
        self._timestamp_col = None

        if rawdata:
            self.set_columns(rawdata)

        # dataset is assumed to be the public version of the dataset
        self._is_private = False
        self.__implicit = False

        # ------------------------------
        # --------- PROPERTIES ---------
        self._sorted_users = None
        self._sorted_items = None

        # map users and items with a 0-indexed mapping
        self._public_to_private_users = None
        self._public_to_private_items = None
        self._private_to_public_users = None
        self._private_to_public_items = None

        # metrics
        self._transactions = None
        self._space_size = None
        self._space_size_log = None
        self._shape = None
        self._shape_log = None
        self._density = None
        self._density_log = None
        self._gini_item = None
        self._gini_user = None
        self._ratings_per_user = None
        self._ratings_per_item = None

        # more analyses
        self.metrics = ['transactions', 'space_size', 'space_size_log', 'shape', 'shape_log', 'density', 'density_log',
                        'gini_item', 'gini_user', 'ratings_per_user', 'ratings_per_item']

    def __str__(self):
        """
        Returns 'self.data' as a string variable.
        
        Returns:
            (str): 'self.data' as a string variable.
        """
        return self.data.__str__()

    def __repr__(self):
        """
        Returns the official string representation of the internal DataFrame.
        """
        return self.data.__repr__()

    def _repr_html_(self):
        """
        Returns an HTML representation of the internal DataFrame for rich displays.
        """
        return self.data._repr_html_()

    def __len__(self):
        """
        Returns the total number of samples in the dataset.
        
        Returns:
            (int): number of samples in the dataset.
        """
        return len(self.data)

    def set_columns(self, rawdata):
        """
        Assign dataset column names from a RawData object and reorder the data accordingly.
        
        Args:
            rawdata (RawData): A RawData object containing the column names for 
                user, item, rating, and timestamp.
        """
        if rawdata.user is not None:
            self.user_col = rawdata.user
            self.__assigned_columns.append(self.user_col)
        if rawdata.item is not None:
            self.item_col = rawdata.item
            self.__assigned_columns.append(self.item_col)
        if rawdata.rating is not None:
            self.rating_col = rawdata.rating
            self.__assigned_columns.append(self.rating_col)
        if rawdata.timestamp is not None:
            self.timestamp_col = rawdata.timestamp
            self.__assigned_columns.append(self.timestamp_col)

        # re-order columns
        self._data = self.data[self.__assigned_columns]

    def reset(self):
        
        """
        Reset cached statistics and assigned columns of the DataRec object.

        This method clears all precomputed dataset statistics (e.g., sorted users, 
        density, Gini indices, shape, ratings per user/item) and empties the list 
        of assigned columns. It is automatically called when the underlying data is changed.
        """
        self._sorted_users = None
        self._sorted_items = None
        self._transactions = None
        self._space_size = None
        self._space_size_log = None
        self._shape = None
        self._shape_log = None
        self._density = None
        self._density_log = None
        self._gini_item = None
        self._gini_user = None
        self._ratings_per_user = None
        self._ratings_per_item = None

        self.__assigned_columns = []

    @property
    def data(self):
        """
        The underlying pandas DataFrame holding the interaction data.
        """
        return self._data

    @data.setter
    def data(self, value: RawData):
        """
        Sets the internal DataFrame from a RawData object and resets stats.
        """
        if (value is not None and
                not isinstance(value, RawData)):
            raise ValueError(f'Data must be RawData or None if empty. Found {type(value)}')
        value = value if value is not None else pd.DataFrame()

        self._data = value.data
        self.reset()
        self.set_columns(value)

    @property
    def user_col(self):
        """
        The name of the user ID column.
        """
        return self._user_col

    @user_col.setter
    def user_col(self, value: Union[str, int]):
        """
        Sets and renames the user column to the internal standard name.
        """
        self.set_user_col(value, rename=True)

    def set_user_col(self, value: Union[str, int] = DATAREC_USER_COL, rename=True):
        """
        Identifies and optionally renames the user column.

        Args:
            value (Union[str, int]): The current name or index of the user column.
            rename (bool): If True, renames the column to the standard internal name.
        """
        self.data.columns, self._user_col = set_column_name(columns=list(self.data.columns),
                                                            value=value,
                                                            default_name=DATAREC_USER_COL,
                                                            rename=rename)

    @property
    def item_col(self):
        """
        The name of the item ID column.
        """
        return self._item_col

    @item_col.setter
    def item_col(self, value: Union[str, int]):
        """
        Sets and renames the item column to the internal standard name.
        """
        self.set_item_col(value, rename=True)

    def set_item_col(self, value: Union[str, int] = DATAREC_ITEM_COL, rename=True):
        """
        Identifies and optionally renames the item column.

        Args:
            value (Union[str, int]): The current name or index of the item column.
            rename (bool): If True, renames the column to the standard internal name.
        """
        self.data.columns, self._item_col = set_column_name(columns=list(self.data.columns),
                                                            value=value,
                                                            default_name=DATAREC_ITEM_COL,
                                                            rename=rename)

    @property
    def rating_col(self):
        """
        The name of the rating column.
        """
        return self._rating_col

    @rating_col.setter
    def rating_col(self, value: Union[str, int]):
        """
        Sets and renames the rating column to the internal standard name.
        """
        self.set_rating_col(value, rename=True)

    def set_rating_col(self, value: Union[str, int] = DATAREC_RATING_COL, rename=True):
        """
        Identifies and optionally renames the rating column.

        Args:
            value (Union[str, int]): The current name or index of the rating column.
            rename (bool): If True, renames the column to the standard internal name.
        """
        self.data.columns, self._rating_col = set_column_name(columns=list(self.data.columns),
                                                              value=value,
                                                              default_name=DATAREC_RATING_COL,
                                                              rename=rename)

    @property
    def timestamp_col(self):
        """
        The name of the timestamp column.
        """
        return self._timestamp_col

    @timestamp_col.setter
    def timestamp_col(self, value: Union[str, int]):
        """
        Sets and renames the timestamp column to the internal standard name.
        """
        self.set_timestamp_col(value, rename=True)

    def set_timestamp_col(self, value: Union[str, int] = DATAREC_TIMESTAMP_COL, rename=True):
        """
        Identifies and optionally renames the timestamp column.

        Args:
            value (Union[str, int]): The current name or index of the timestamp column.
            rename (bool): If True, renames the column to the standard internal name.
        """
        self.data.columns, self._timestamp_col = set_column_name(columns=list(self.data.columns),
                                                                 value=value,
                                                                 default_name=DATAREC_TIMESTAMP_COL,
                                                                 rename=rename)

    @property
    def users(self):
        """
        Returns a list of unique user IDs in the dataset.
        """
        return self.data[self.user_col].unique().tolist()

    @property
    def items(self):
        """
        Returns a list of unique item IDs in the dataset.
        """
        return self.data[self.item_col].unique().tolist()

    @property
    def n_users(self):
        """
        Returns the number of unique users.
        """
        return int(self.data[self.user_col].nunique())

    @property
    def n_items(self):
        """
        Returns the number of unique items.
        """
        return int(self.data[self.item_col].nunique())

    @property
    def columns(self):
        """
        Returns the list of column names of the internal DataFrame.
        """
        return self.data.columns

    @columns.setter
    def columns(self, columns):
        """
        Sets the column names of the internal DataFrame.
        """
        self.data.columns = columns

    @property
    def sorted_items(self):
        """
        Returns a dictionary of items sorted by their interaction count.
        """
        if self._sorted_items is None:
            count_items = self.data.groupby(self.item_col).count().sort_values(by=[self.user_col])
            self._sorted_items = dict(zip(count_items.index, count_items[self.user_col]))
        return self._sorted_items

    @property
    def sorted_users(self):
        """
        Returns a dictionary of users sorted by their interaction count.
        """
        if self._sorted_users is None:
            count_users = self.data.groupby(self.user_col).count().sort_values(by=[self.item_col])
            self._sorted_users = dict(zip(count_users.index, count_users[self.item_col]))
        return self._sorted_users

    # --- MAPPING FUNCTIONS ---
    @property
    def transactions(self):
        """
        Returns the total number of interactions (rows) in the dataset.
        """
        if self._transactions is None:
            self._transactions = len(self.data)
        return self._transactions

    @staticmethod
    def public_to_private(lst, offset=0):
        """
        Creates a mapping from public (original) IDs to private (integer) IDs.

        Args:
            lst (list): A list of public IDs.
            offset (int): The starting integer for the private IDs.

        Returns:
            (dict): A dictionary mapping public IDs to private integer IDs.
        """
        return dict(zip(lst, range(offset, offset + len(lst))))

    @staticmethod
    def private_to_public(pub_to_prvt: dict):
        """
        Creates a reverse mapping from private IDs back to public IDs.

        Args:
            pub_to_prvt (dict): A dictionary mapping public IDs to private IDs.

        Returns:
            (dict): A dictionary mapping private IDs to public IDs.
        """
        mapping = {el: idx for idx, el in pub_to_prvt.items()}
        if len(pub_to_prvt) != len(mapping):
            print('WARNING: private to public mapping could be incorrect. Please, check your code.')
        return mapping

    def map_users_and_items(self, offset=0, items_shift=False):
        """
        Generates the public-to-private and private-to-public ID mappings.

        This method creates the dictionaries needed to convert user and item IDs
        to a dense, zero-indexed integer range suitable for machine learning models.

        Args:
            offset (int): The starting integer for the ID mappings. Defaults to 0.
            items_shift (bool): If True, item private IDs will start after the last
                user private ID, creating a single contiguous ID space. Defaults to False.
        """
        # map users and items with a 0-indexed mapping
        users_offset = offset
        items_offset = offset

        # users
        self._public_to_private_users = self.public_to_private(self.users, offset=users_offset)
        self._private_to_public_users = self.private_to_public(self._public_to_private_users)

        # items
        if items_shift:
            items_offset = offset + self.n_users
        self._public_to_private_items = self.public_to_private(self.items, offset=items_offset)
        self._private_to_public_items = self.private_to_public(self._public_to_private_items)

    def map_dataset(self, user_mapping, item_mapping):
        """
        Applies ID mappings to the user and item columns of the DataFrame.

        This is an in-place operation that modifies the internal DataFrame.

        Args:
            user_mapping (dict): The dictionary to map user IDs.
            item_mapping (dict): The dictionary to map item IDs.
        """
        self.data[self.user_col] = self.data[self.user_col].map(user_mapping)
        self.data[self.item_col] = self.data[self.item_col].map(item_mapping)

    def to_public(self):
        """
        Converts user and item IDs back to their original (public) values.
        """
        if self._is_private:
            self.map_dataset(self._private_to_public_users, self._private_to_public_items)
        self._is_private = False

    def to_private(self):
        """
        Converts user and item IDs to their dense, zero-indexed (private) integer values.
        """
        if not self._is_private:
            self.map_dataset(self._public_to_private_users, self._public_to_private_items)
        self._is_private = True

    # -- METRICS --
    def get_metric(self, metric):
        """
        Retrieves a calculated dataset metric by name.

        Args:
            metric (str): The name of the metric to compute (e.g., 'density', 'gini_user').

        Returns:
            The value of the computed metric.
        """
        assert metric in self.metrics, f'{self.__class__.__name__}: metric \'{metric}\' not found.'
        func = getattr(self, metric)
        return func()

    @property
    def space_size(self):
        """
        Calculates the scaled square root of the user-item interaction space.
        """
        if self._space_size is None:
            scale_factor = 1000
            self._space_size = math.sqrt(self.n_users * self.n_items) / scale_factor
        return self._space_size

    @property
    def space_size_log(self):
        """
        Calculates the log10 of the space_size metric.
        """
        if self._space_size_log is None:
            self._space_size_log = math.log10(self.space_size)
        return self._space_size_log

    @property
    def shape(self):
        """
        Calculates the shape of the interaction matrix (n_users / n_items).
        """
        if self._shape is None:
            self._shape = self.n_users / self.n_items
        return self._shape

    @property
    def shape_log(self):
        """
        Calculates the log10 of the shape metric.
        """
        if self._shape_log is None:
            self._shape_log = math.log10(self.shape)
        return self._shape_log

    @property
    def density(self):
        """
        Calculates the density of the user-item interaction matrix.
        """
        if self._density is None:
            self._density = self.transactions / (self.n_users * self.n_items)
        return self._density

    @property
    def density_log(self):
        """
        Calculates the log10 of the density metric.
        """
        if self._density_log is None:
            self._density_log = math.log10(self.density)
        return self._density_log

    @staticmethod
    def gini(x):
        """
        Calculates the Gini coefficient for a numpy array.

        Args:
            x (np.ndarray): An array of non-negative values.

        Returns:
            (float): The Gini coefficient, a measure of inequality.
        """
        x = np.sort(x)  # O(n log n)
        n = len(x)
        cum_index = np.arange(1, n + 1)
        return (np.sum((2 * cum_index - n - 1) * x)) / (n * np.sum(x))


    @property
    def gini_item(self):
        """
        Calculates the Gini coefficient for item popularity.
        """
        if self._gini_item is None:
            self._gini_item = self.gini(np.array(list(self.sorted_items.values())))
        return self._gini_item

    @property
    def gini_user(self):
        """
        Calculates the Gini coefficient for user activity.
        """
        if self._gini_user is None:
            self._gini_user = self.gini(np.array(list(self.sorted_users.values())))
        return self._gini_user

    @property
    def ratings_per_user(self):
        """
        Calculates the average number of ratings per user.
        """
        if self._ratings_per_user is None:
            self._ratings_per_user = self.transactions / self.n_users
        return self._ratings_per_user

    @property
    def ratings_per_item(self):
        """
        Calculates the average number of ratings per item.
        """
        if self._ratings_per_item is None:
            self._ratings_per_item = self.transactions / self.n_items
        return self._ratings_per_item

    def users_frequency(self):
        """
        Computes the absolute frequency of each user in the dataset.

        Returns:
            (dict): A dictionary mapping user IDs to the number of interactions, 
                sorted in descending order of frequency.
        """
        fr = dict(Counter(self.data[self.user_col]))
        return dict(sorted(fr.items(), key=lambda item: item[1], reverse=True))

    def users_relative_frequency(self):
        """
        Computes the relative frequency of each user in the dataset.

        Returns:
            (dict): A dictionary mapping user IDs to their relative frequency 
                (fraction of total transactions).
        """
        return {u: (f / self.transactions) for u, f in self.users_frequency().items()}

    def items_frequency(self):
        """
        Computes the absolute frequency of each item in the dataset.

        Returns:
            (dict): A dictionary mapping item IDs to the number of interactions, 
                sorted in descending order of frequency.
        """
        fr = dict(Counter(self.data[self.item_col]))
        return dict(sorted(fr.items(), key=lambda item: item[1], reverse=True))

    def items_relative_frequency(self):
        """
        Computes the relative frequency of each item in the dataset.

        Returns:
            (dict): A dictionary mapping item IDs to their relative frequency 
                (fraction of total transactions).
        """
        return {u: (f / self.transactions) for u, f in self.items_frequency().items()}

    def users_quartiles(self):
        """
        Assigns quartile indices to users based on their frequency.

        Returns:
            (dict): A dictionary mapping each user ID to a quartile index (0-3),
                where 0 = lowest, 3 = highest frequency.
        """ 
        return quartiles(self.users_frequency())

    def items_quartiles(self):
        """
        Assigns quartile indices to items based on their frequency.

        Returns:
            (dict): A dictionary mapping each item ID to a quartile index (0-3),
                where 0 = lowest, 3 = highest frequency.
        """
        return quartiles(self.items_frequency())

    def users_popularity(self):
        """
        Categorizes users into descriptive popularity groups based on quartiles.

        Returns:
            (dict): A dictionary mapping popularity categories ('long tail', 
                'common', 'popular', 'most popular') to lists of user IDs.
        """
        return popularity(self.users_quartiles())

    def items_popularity(self):
        """
        Categorizes items into descriptive popularity groups based on quartiles.

        Returns:
            (dict): A dictionary mapping popularity categories ('long tail', 
                'common', 'popular', 'most popular') to lists of item IDs.
        """
        return popularity(self.items_quartiles())

    def copy(self):
        """
        Create a deep copy of the current DataRec object.
        
        This method duplicates the DataRec instance, including its data,
        metadata (user, item, rating, timestamp columns), pipeline, and internal
        state such as privacy settings and implicit flags.
        
        Returns:
            (DataRec): A new DataRec object that is a deep copy of the current instance.
        """
        pipeline = self.pipeline.copy()

        new_dr = DataRec(rawdata=self.to_rawdata(),
                         pipeline=pipeline,
                         copy=True)

        new_dr.__implicit = self.__implicit
        new_dr._user_col = self.user_col
        new_dr._item_col = self.item_col
        new_dr._rating_col = self.rating_col
        new_dr._timestamp_col = self.timestamp_col
        new_dr._is_private = self._is_private
        return new_dr

    def to_rawdata(self):
        """
        Convert the current DataRec object into a RawData object.

        This method creates a RawData instance containing the same data and
        metadata (user, item, rating, timestamp columns) as the DataRec object.

        Returns:
            (RawData): A new RawData object containing the DataRec's data and column information.
        """
        raw = RawData(self.data)
        raw.user = self.user_col
        raw.item = self.item_col
        raw.rating = self.rating_col
        raw.timestamp = self.timestamp_col
        return raw

    def save_pipeline(self, filepath: str) -> None:
        """
        Save the current processing pipeline to a YAML file.

        Args:
            filepath (str): The path (including filename) where the pipeline 
                YAML file will be saved.
        """
        print(f'Saving pipeline to {filepath}')

        self.pipeline.to_yaml(filepath)

        print(f'Pipeline correctly saved to {filepath}')

    def to_torch_dataset(self, task="pointwise", autoprepare=True, **kwargs):
        """
        Converts the current DataRec object into a PyTorch-compatible dataset.

        This method prepares the dataset (e.g., remaps user/item IDs to a dense index space)
        and returns a `torch.utils.data.Dataset` object suitable for training with PyTorch.

        Args:
            task (str): The recommendation task type. Must be one of:
                - "pointwise": returns PointwiseTorchDataset
                - "pairwise": returns PairwiseTorchDataset
                - "ranking": returns RankingTorchDataset
            autoprepare (bool): If True, automatically applies user/item remapping
                and switches the dataset to private IDs. If False, assumes the dataset
                is already properly prepared.
            **kwargs: Additional arguments passed to the specific torch dataset class.

        Returns:
            (torch.utils.data.Dataset): A PyTorch dataset instance corresponding to the selected task.

        Raises:
            ImportError: If PyTorch is not installed.
            ValueError: If an unknown task name is provided.
        """

        try:
            import torch
        except ImportError:
            raise ImportError(
                "PyTorch is required to use the to_torch_dataset() method. "
                "Please install it with `pip install torch`."
            )

        # Preparazione automatica del dataset
        if autoprepare:
            self.map_users_and_items()
            self.to_private()
        else:
            warnings.warn(
                "Autoprepare is set to False. "
                "Ensure that the dataset is prepared correctly before using it with PyTorch."
            )

        # Selezione del dataset PyTorch
        if task == "pointwise":
            from datarec.data.torch_dataset import PointwiseTorchDataset
            return PointwiseTorchDataset(self, **kwargs)
        elif task == "pairwise":
            from datarec.data.torch_dataset import PairwiseTorchDataset
            return PairwiseTorchDataset(self, **kwargs)
        elif task == "ranking":
            from datarec.data.torch_dataset import RankingTorchDataset
            return RankingTorchDataset(self, **kwargs)
        else:
            raise ValueError(f"Unknown task: {task}")


def share_info(datarec_source: DataRec, datarec_target: DataRec) -> None:
    """
    Copy dataset metadata and mappings from one DataRec object to another
    
    This function transfers core attributes from a source DataRec
    to a target DataRec. 
    
    Args:
        datarec_source (DataRec): The source DataRec from which information 
            is copied.
        datarec_target (DataRec): The target DataRec that will be updated 
            with the source information.

    """
    ds = datarec_source
    dt = datarec_target

    dt._is_private = ds._is_private
    dt.__implicit = ds.__implicit

    dt.dataset_name = ds.dataset_name
    dt.version_name = ds.version_name
    dt.user_col = ds.user_col
    dt.item_col = ds.item_col
    dt.rating_col = ds.rating_col
    dt.timestamp_col = ds.timestamp_col

    dt._sorted_users = ds._sorted_users
    dt._sorted_items = ds._sorted_users
    dt._public_to_private_users = ds._public_to_private_users
    dt._public_to_private_items = ds._public_to_private_items
    dt._private_to_public_users = ds._private_to_public_users
    dt._private_to_public_items = ds._private_to_public_items
