import math
import warnings
import pandas as pd
import numpy as np
from typing import Union, Optional, Any
from collections import Counter
from .utils import set_column_name, quartiles, popularity, Encoder
from datarec.io.rawdata import RawData
from datarec.pipeline import Pipeline
from datarec.data.characteristics import CHARACTERISTICS
from datarec.io import paths

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
            registry_dataset: bool = False,
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
            registry_dataset (bool): Whether the DataRec derives from a registered dataset.
            
        """
        self.path = None
        self._data = None
        self.dataset_name = dataset_name
        self.version_name = version_name

        rawdata_step = None
        if rawdata is not None:
            if copy:
                self._data: pd.DataFrame = rawdata.data.copy()
            else:
                self._data: pd.DataFrame = rawdata.data
            
            if rawdata.pipeline_step is not None:
                rawdata_step = rawdata.pipeline_step
        
        # PIPELINE INITIALIZATION
        if pipeline:
            self.pipeline = pipeline
        else:
            if registry_dataset:
                self.pipeline = Pipeline()
                self.pipeline.add_step("load", "registry_dataset", {"dataset_name": self.dataset_name, "version": self.version_name})
            elif rawdata_step is not None:
                self.pipeline = Pipeline()
                self.pipeline.steps.append(rawdata_step)
            else:
                warnings.warn("No pipeline provided. Initializing empty pipeline.")
                self.pipeline = Pipeline()

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

        # map users and items with a 0-indexed mapping
        self.user_id_encoder = Encoder()
        self.item_id_encoder = Encoder()
        
        # Apply external encoders (e.g., from streaming readers) if provided
        if rawdata is not None:
            if getattr(rawdata, "user_encoder", None):
                self.user_id_encoder.apply_encoding(rawdata.user_encoder)
            if getattr(rawdata, "item_encoder", None):
                self.item_id_encoder.apply_encoding(rawdata.item_encoder)

        # ------------------------------
        # --------- PROPERTIES ---------
        self._sorted_users = None
        self._sorted_items = None

        self._n_users = None
        self._n_items = None
        self._transactions = None

        self.characteristics = CharacteristicAccessor(self)
        

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

        self.__assigned_columns = []

    @property
    def data(self) -> pd.DataFrame:
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

    @property
    def transactions(self):
        """
        Returns the total number of interactions (rows) in the dataset.
        """
        if self._transactions is None:
            self._transactions = len(self.data)
        return self._transactions

    # --- ID ENCODING/DECODING FUNCTIONS ---

    def is_encoded(self, on:str) -> bool:
        """
        Checks if user or item IDs are encoded to private integer IDs.

        Args:
            on (str): 'users' to check user encoding, 'items' for item encoding.
        Returns:
            (bool): True if the specified IDs are encoded, False otherwise.
        """
        if on == 'users':
            return self.user_id_encoder.is_encoded()
        elif on == 'items':
            return self.item_id_encoder.is_encoded()
        else:
            raise ValueError("Parameter 'on' must be either 'users' or 'items'.")
        

    def encode(self, users=True, items=True) -> None:
        """
        Converts user and item IDs to encoded integer IDs.
        Args:
            users (bool): If True, encodes user IDs.
            items (bool): If True, encodes item IDs.
        """
        if users:
            if not self.user_id_encoder.is_encoded():
                raise ValueError("User encoder is empty. Build or apply an encoding before calling encode().")
            self.data[self.user_col] = self.user_id_encoder.encode(self.data[self.user_col].tolist())
        if items:
            if not self.item_id_encoder.is_encoded():
                raise ValueError("Item encoder is empty. Build or apply an encoding before calling encode().")
            self.data[self.item_col] = self.item_id_encoder.encode(self.data[self.item_col].tolist())

    def decode(self, users=True, items=True) -> None:
        """
        Converts user and item IDs back to original IDs.
        Args:
            users (bool): If True, encodes user IDs.
            items (bool): If True, encodes item IDs.
        """
        if users:
            self.data[self.user_col] = self.user_id_encoder.decode(self.data[self.user_col].tolist())
        if items:
            self.data[self.item_col] = self.item_id_encoder.decode(self.data[self.item_col].tolist())

    def reset_encoding(self, on='all') -> None:
        """
        Resets the encoding for users or items.
        
        Args:
            on (str): 'users' to reset user encoding, 'items' for item encoding.
        """
        if on == 'users':
            self.decode(users=True, items=False)
            self.user_id_encoder.reset_encoding()
        elif on == 'items':
            self.decode(users=False, items=True)
            self.item_id_encoder.reset_encoding()
        elif on == 'all':
            self.decode(users=True, items=True)
            self.user_id_encoder.reset_encoding()
            self.item_id_encoder.reset_encoding()
        else:
            raise ValueError("Parameter 'on' must be either 'users' or 'items'.")


    def build_encoding(self, on='users', offset=0) -> None:
        """
        Builds the encoding for users or items.

        Args:
            on (str): 'users' to build user encoding, 'items' for item encoding, 'all' for both.
            offset (int): The starting integer for the private IDs.
        """
        if on == 'users':
            self.user_id_encoder.build_encoding(self.users, offset=offset)
        elif on == 'items':
            self.item_id_encoder.build_encoding(self.items, offset=offset)
        elif on == 'all':
            self.user_id_encoder.build_encoding(self.users, offset=offset)
            self.item_id_encoder.build_encoding(self.items, offset=offset)
        else:
            raise ValueError("Parameter 'on' must be either 'users' or 'items'.")
        

    # -- CHARACTERISTICS --

    def characteristic(self, name: str, **kwargs: Any) -> Any:
        """
        Retrieves a calculated dataset characteristic by name.

        Args:
            name (str): The name of the characteristic to retrieve.
            **kwargs: Additional arguments to pass to the characteristic function.

        Returns:
            The value of the requested characteristic.
        """
        return getattr(self.characteristics, name)(**kwargs)
    
    def space_size(self, **kwargs):
        return self.characteristic("space_size", **kwargs)

    def space_size_log(self, **kwargs):
        return self.characteristic("space_size_log", **kwargs)

    def shape(self, **kwargs):
        return self.characteristic("shape", **kwargs)

    def shape_log(self, **kwargs):
        return self.characteristic("shape_log", **kwargs)

    def density(self, **kwargs):
        return self.characteristic("density", **kwargs)

    def density_log(self, **kwargs):
        return self.characteristic("density_log", **kwargs)

    def gini_item(self, **kwargs):
        return self.characteristic("gini_item", **kwargs)

    def gini_user(self, **kwargs):
        return self.characteristic("gini_user", **kwargs)

    def ratings_per_user(self, **kwargs):
        return self.characteristic("ratings_per_user", **kwargs)

    def ratings_per_item(self, **kwargs):
        return self.characteristic("ratings_per_item", **kwargs)

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

    def list_characteristics(self) -> list[str]:
        """Return the names of all characteristics that can be computed on this dataset."""
        return sorted(CHARACTERISTICS.keys())

    def describe_characteristics(self) -> dict[str, str]:
        """Return a mapping name -> short docstring for each available characteristic."""
        return {
            name: (func.__doc__ or "").strip()
            for name, func in CHARACTERISTICS.items()
        }

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

        new_dr._user_col = self.user_col
        new_dr._item_col = self.item_col
        new_dr._rating_col = self.rating_col
        new_dr._timestamp_col = self.timestamp_col
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

    def to_torch_dataset(self, task: str = "pointwise", autoprepare: bool = True, **kwargs: Any) -> Any:
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
        except ModuleNotFoundError:
            raise ImportError(
                "Torch is required for this feature. Please install it with `pip install datarec[torch]` or"
                " `pip install -r requirements/requirements-torch.txt`."
            )

        if autoprepare:
            self.build_encoding(on='all', offset=0)
            self.encode()
        else:
            warnings.warn(
                "Autoprepare is set to False. "
                "Ensure that the dataset is prepared correctly before using it with PyTorch."
            )

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
        
    def to_graphrec(self):
        """
        Converts the current DataRec object into a GraphRec object.

        This method creates a GraphRec instance representing the bipartite graph
        of user-item interactions contained in the DataRec object.

        Returns:
            (GraphRec): A new GraphRec object representing the interaction graph.
        """
        from datarec.data.graph import GraphRec
        return GraphRec(self)
    
    def to_pickle(self, filepath: str = '') -> None:
        """
        Save the current DataRec object to a pickle file.

        Args:
            filepath (str): The path (including filename) where the pickle file will be saved.
        """
        import pickle

        if filepath == '':
            filepath = paths.pickle_version_filepath(self.dataset_name, self.version_name)

        print(f'Saving DataRec to {filepath}')

        with open(filepath, 'wb') as f:
            pickle.dump(self, f)

        print(f'DataRec correctly saved to {filepath}')


class CharacteristicAccessor:
    """
    Accessor for dataset characteristics.
    Allows dynamic retrieval of dataset characteristics as attributes.
    
    Args:
        dr (DataRec): The DataRec object to access characteristics from.
    """
    def __init__(self, dr: DataRec):
        self._datarec = dr

    def __getattr__(self, name):
        try:
            func = CHARACTERISTICS[name]
        except KeyError:
            raise AttributeError(name) from None

        def bound(**kwargs):
            return func(self._datarec, **kwargs)
        
        bound.__doc__ = func.__doc__
        return bound


def from_pickle(dataset_name:str = '', version_name:str = '', filepath: str = '') -> DataRec:
    """
    Load a DataRec object from a pickle file.

    Args:
        dataset_name (str): The name of the dataset.
        version_name (str): The version identifier of the dataset.
        filepath (str): The path to the pickle file.
    Returns:
        (DataRec): The loaded DataRec object.
    """
    import pickle

    if filepath == '':
        if dataset_name == '' and version_name == '':
            raise ValueError("Either dataset_name and version_name or filepath must be provided.")
        filepath = paths.pickle_version_filepath(dataset_name, version_name)

    print(f'Loading DataRec from {filepath}')

    with open(filepath, 'rb') as f:
        dr = pickle.load(f)

    print(f'DataRec correctly loaded from {filepath}')

    return dr
