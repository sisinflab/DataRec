import math
import pandas as pd
import numpy as np
from typing import Union
from collections import Counter
from .utils import set_column_name, quartiles, popularity
from datarec.io.rawdata import RawData

DATAREC_USER_COL = 'user_id'
DATAREC_ITEM_COL = 'item_id'
DATAREC_RATING_COL = 'rating'
DATAREC_TIMESTAMP_COL = 'timestamp'


class DataRec:
    def __init__(
            self,
            rawdata: RawData = None,
            copy: bool = False,
            dataset_name: str = 'datarec',
            version_name: str = 'no_version_provided',
            *args,
            **kwargs
    ):

        self.path = None
        self._data = None
        self.dataset_name = dataset_name
        self.version_name = version_name

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
        self._ratings_col = None
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
        return self.data.__str__()

    def __repr__(self):
        return self.data.__repr__()

    def __len__(self):
        return len(self.data)

    def set_columns(self, rawdata):

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
        return self._data

    @data.setter
    def data(self, value: RawData):
        if (value is not None and
                not isinstance(value, RawData)):
            raise ValueError(f'Data must be RawData or None if empty. Found {type(value)}')
        value = value if value is not None else pd.DataFrame()

        self._data = value.data
        self.reset()
        self.set_columns(value)

    @property
    def user_col(self):
        return self._user_col

    @user_col.setter
    def user_col(self, value: Union[str, int]):
        self.set_user_col(value, rename=True)

    def set_user_col(self, value: Union[str, int] = DATAREC_USER_COL, rename=True):
        self.data.columns, self._user_col = set_column_name(columns=list(self.data.columns),
                                                            value=value,
                                                            default_name=DATAREC_USER_COL,
                                                            rename=rename)

    @property
    def item_col(self):
        return self._item_col

    @item_col.setter
    def item_col(self, value: Union[str, int]):
        self.set_item_col(value, rename=True)

    def set_item_col(self, value: Union[str, int] = DATAREC_ITEM_COL, rename=True):
        self.data.columns, self._item_col = set_column_name(columns=list(self.data.columns),
                                                            value=value,
                                                            default_name=DATAREC_ITEM_COL,
                                                            rename=rename)

    @property
    def rating_col(self):
        return self._rating_col

    @rating_col.setter
    def rating_col(self, value: Union[str, int]):
        self.set_rating_col(value, rename=True)

    def set_rating_col(self, value: Union[str, int] = DATAREC_RATING_COL, rename=True):
        self.data.columns, self._rating_col = set_column_name(columns=list(self.data.columns),
                                                              value=value,
                                                              default_name=DATAREC_RATING_COL,
                                                              rename=rename)

    @property
    def timestamp_col(self):
        return self._timestamp_col

    @timestamp_col.setter
    def timestamp_col(self, value: Union[str, int]):
        self.set_timestamp_col(value, rename=True)

    def set_timestamp_col(self, value: Union[str, int] = DATAREC_TIMESTAMP_COL, rename=True):
        self.data.columns, self._timestamp_col = set_column_name(columns=list(self.data.columns),
                                                                 value=value,
                                                                 default_name=DATAREC_TIMESTAMP_COL,
                                                                 rename=rename)

    @property
    def users(self):
        return self.data[self.user_col].unique().tolist()

    @property
    def items(self):
        return self.data[self.item_col].unique().tolist()

    @property
    def n_users(self):
        return int(self.data[self.user_col].nunique())

    @property
    def n_items(self):
        return int(self.data[self.item_col].nunique())

    @property
    def columns(self):
        return self.data.columns

    @columns.setter
    def columns(self, columns):
        self.data.columns = columns

    @property
    def sorted_items(self):
        if self._sorted_items is None:
            count_items = self.data.groupby(self.item_col).count().sort_values(by=[self.user_col])
            self._sorted_items = dict(zip(count_items.index, count_items[self.user_col]))
        return self._sorted_items

    @property
    def sorted_users(self):
        if self._sorted_users is None:
            count_users = self.data.groupby(self.user_col).count().sort_values(by=[self.item_col])
            self._sorted_users = dict(zip(count_users.index, count_users[self.item_col]))
        return self._sorted_users

    # --- MAPPING FUNCTIONS ---
    @property
    def transactions(self):
        if self._transactions is None:
            self._transactions = len(self.data)
        return self._transactions

    @staticmethod
    def public_to_private(lst, offset=0):
        return dict(zip(lst, range(offset + lst, offset + len(lst))))

    @staticmethod
    def private_to_public(pub_to_prvt: dict):
        mapping = {el: idx for idx, el in pub_to_prvt.items()}
        if len(pub_to_prvt) != len(mapping):
            print('WARNING: private to public mapping could be incorrect. Please, check your code.')
        return mapping

    def map_users_and_items(self, offset=0, items_shift=False):
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
        self.data[self.user_col] = self.data[self.user_col].map(user_mapping)
        self.data[self.item_col] = self.data[self.item_col].map(item_mapping)

    def to_public(self):
        if self._is_private:
            self.map_dataset(self._private_to_public_users, self._private_to_public_items)
        self._is_private = False

    def to_private(self):
        if not self._is_private:
            self.map_dataset(self._public_to_private_users, self._public_to_private_items)
        self._is_private = True

    # -- METRICS --
    def get_metric(self, metric):
        assert metric in self.metrics, f'{self.__class__.__name__}: metric \'{metric}\' not found.'
        func = getattr(self, metric)
        return func()

    @property
    def space_size(self):
        if self._space_size is None:
            scale_factor = 1000
            self._space_size = math.sqrt(self.n_users * self.n_items) / scale_factor
        return self._space_size

    @property
    def space_size_log(self):
        if self._space_size_log is None:
            self._space_size_log = math.log10(self.space_size)
        return self._space_size_log

    @property
    def shape(self):
        if self._shape is None:
            self._shape = self.n_users / self.n_items
        return self._shape

    @property
    def shape_log(self):
        if self._shape_log is None:
            self._shape_log = math.log10(self.shape)
        return self._shape_log

    @property
    def density(self):
        if self._density is None:
            self._density = self.transactions / (self.n_users * self.n_items)
        return self._density

    @property
    def density_log(self):
        if self._density_log is None:
            self._density_log = math.log10(self.density)
        return self._density_log

    @staticmethod
    def gini(x):
        total = 0
        for i, xi in enumerate(x[:-1], 1):
            total += np.sum(np.abs(xi - x[i:]))
        return total / (len(x) ** 2 * np.mean(x))

    @property
    def gini_item(self):
        if self._gini_item is None:
            self._gini_item = self.gini(np.array(list(self.sorted_items.values())))
        return self._gini_item

    @property
    def gini_user(self):
        if self._gini_user is None:
            self._gini_user = self.gini(np.array(list(self.sorted_users.values())))
        return self._gini_user

    @property
    def ratings_per_user(self):

        if self._ratings_per_user is None:
            self._ratings_per_user = self.transactions / self.n_users
        return self._ratings_per_user

    @property
    def ratings_per_item(self):
        if self._ratings_per_item is None:
            self._ratings_per_item = self.transactions / self.n_items
        return self._ratings_per_item

    def users_frequency(self):
        fr = dict(Counter(self.data[self.user_col]))
        return dict(sorted(fr.items(), key=lambda item: item[1], reverse=True))

    def users_relative_frequency(self):
        return {u: (f / self.transactions) for u, f in self.users_frequency().items()}

    def items_frequency(self):
        fr = dict(Counter(self.data[self.item_col]))
        return dict(sorted(fr.items(), key=lambda item: item[1], reverse=True))

    def items_relative_frequency(self):
        return {u: (f / self.transactions) for u, f in self.items_frequency().items()}

    def users_quartiles(self):
        return quartiles(self.users_frequency())

    def items_quartiles(self):
        return quartiles(self.items_frequency())

    def users_popularity(self):
        return popularity(self.users_quartiles())

    def items_popularity(self):
        return popularity(self.items_quartiles())

    def copy(self):
        new_dr = DataRec(rawdata=self.to_rawdata(),
                         copy=True)

        new_dr.__implicit = self.__implicit
        new_dr._user_col = self.user_col
        new_dr._item_col = self.item_col
        new_dr._rating_col = self.rating_col
        new_dr._timestamp_col = self.timestamp_col
        new_dr._is_private = self._is_private
        return new_dr

    def to_rawdata(self):
        raw = RawData(self.data)
        raw.user = self.user_col
        raw.item = self.item_col
        raw.rating = self.rating_col
        raw.timestamp = self.timestamp_col

        return raw


def share_info(datarec_source: DataRec, datarec_target: DataRec) -> None:
    """
    Given a DataRec target gets the main dataset information from DataRec source
    @param datarec_source: datarec recommendation dataset
    @param datarec_target: datarec recommendation dataset
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
