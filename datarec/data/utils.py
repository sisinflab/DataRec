import os
import hashlib
from typing import Union
import statistics


def set_column_name(columns: list, value: Union[str, int], rename=True, default_name=None) -> (list, str):
    """
    Identifies a column by its name or index and optionally renames it.

    This utility function provides a flexible way to handle DataFrame columns. It
    can find a column based on its current name (string) or its position (integer).
    If `rename` is True, it replaces the found column name in the list of columns
    with a `default_name`.

    Args:
        columns (list): The list of current column names in the DataFrame.
        value (Union[str, int]): The identifier for the column, either its name
            or its integer index.
        rename (bool, optional): If True, the identified column's name is
            changed to `default_name` in the returned list. Defaults to True.
        default_name (str, optional): The new name for the column if `rename` is
            True. Defaults to None.

    Returns:
        (tuple[list, str]): A tuple containing:
            - The (potentially modified) list of column names.
            - The final name of the selected column (either the original or the
              `default_name` if renamed).

    Raises:
        ValueError: If the `value` is not a valid column name or index, or if
            it is not a string or integer.
    """
    columns = list(columns)

    if isinstance(value, str):
        if value not in columns:
            raise ValueError(f'column \'{value}\' is not a valid column name.')
        selected_column = value

    elif isinstance(value, int):
        if value in columns:
            selected_column = value
        else:
            if value not in range(len(columns)):
                raise ValueError(f'column int \'{value}\' is out of range ({len(columns)} columns).')
            selected_column = columns[value]
    else:
        raise ValueError(f'column value must be either a string (column name) or an integer (column index). Got {type(value)} instead.')

    if rename is True:
        columns[columns.index(selected_column)] = default_name
        return columns, default_name

    return columns, selected_column


def quartiles(count: dict):
    """ 
    Assigns quartile indices (0-3) to items based on their frequency counts.

    The function divides the input values into four quartiles using the 
    median and quantiles. Each item is assigned an integer:
        0: long tail (lowest quartile)
        1: common
        2: popular
        3: most popular (highest quartile)

    Args:
        count (dict): A dictionary mapping items to numeric counts or frequencies.

    Returns:
        (dict): A dictionary mapping each item to its quartile index (0-3).
    """
    q1, q2, q3 = statistics.quantiles(count.values())

    def assign(value):
        if value <= q2:
            if value <= q1:
                return 0
            else:
                return 1
        else:
            if value <= q3:
                return 2
            else:
                return 3

    return {k: assign(f) for k, f in count.items()}


def popularity(quartiles: dict):
    """ 
    Categorizes items based on their quartile indices.

    Converts quartile indices (0-3) into descriptive popularity categories:
        0 -> 'long tail'
        1 -> 'common'
        2 -> 'popular'
        3 -> 'most popular'

    Args:
        quartiles (dict): A dictionary mapping items to quartile indices (0-3).

    Returns:
        (dict): A dictionary mapping each popularity category to a list of items.
    """
    categories_map = \
        {3: 'most popular',
         2: 'popular',
         1: 'common',
         0: 'long tail'}

    categories = \
        {'most popular': [],
         'popular': [],
         'common': [],
         'long tail': []}

    for k, q in quartiles.items():
        categories[categories_map[q]].append(k)

    return categories


def verify_checksum(file_path: str, checksum: str) -> None:
    """
    Verifies the MD5 checksum of a file.

    This function computes the MD5 hash of the file at the given path and
    compares it to the expected checksum. If the file does not exist, a
    FileNotFoundError is raised. If the checksum does not match, a RuntimeError
    is raised indicating possible corruption or version mismatch.

    Args:
        file_path (str): The path to the file to verify.
        checksum (str): The expected MD5 checksum.

    Raises:
        FileNotFoundError: If the specified file does not exist.
        RuntimeError: If the computed checksum does not match the expected value.
    """
    
    if not os.path.isfile(file_path):
        raise FileNotFoundError(f"File '{file_path}' not found.")

    md5 = hashlib.md5()
    with open(file_path, "rb") as f:
        for chunck in iter(lambda: f.read(65536), b""):
            md5.update(chunck)

    digest = md5.hexdigest()
    if not digest == checksum:
        raise RuntimeError(f"Checksum mismatch for '{file_path}': expected {checksum}, but got {digest}. "
                           f"The file may be corrupted or a new version has been downloaded.")

    print(f'Checksum verified.')



class Encoder:
    """
    A simple encoder class to encode and decode IDs.
    """

    def __init__(self):
        self.encoding = dict()

    def is_encoded(self) -> bool:
        """
        Checks if the encoding dictionary is not empty.

        Returns:
            (bool): True if the encoding dictionary is not empty, False otherwise.
        """
        return bool(self.encoding)

    def build_encoding(self, lst: list, offset: int=0) -> None:
        """
        Encodes a list of public IDs into integer IDs.

        Args:
            lst (list): A list of public IDs.
            offset (int): The starting integer for the private IDs.
        """
        if self.is_encoded():
            raise ValueError('Encoding dictionary is not empty. Please, reset it before building a new encoding.')
        self.encoding = dict(zip(lst, range(offset, offset + len(lst))))

    def reset_encoding(self) -> None:
        """
        Resets the encoding dictionary.
        """
        self.encoding = dict()

    def change_offset(self, offset: int) -> None:
        """
        Changes the offset of the current encoding.

        Args:
            offset (int): The new starting integer for the private IDs.
        """
        if not self.encoding:
            raise ValueError('Encoding dictionary is empty. Please, build the encoding first.')
        lst = list(self.encoding.values())
        current_min = min(lst)
        new_offset = offset - current_min
        self.encoding = {idx: el + new_offset for idx, el in self.encoding.items()}

    def apply_encoding(self, encoding: dict) -> None:
        """
        Applies an external encoding dictionary.

        Args:
            encoding (dict): A dictionary encoding IDs.
        """
        if self.is_encoded():
            raise ValueError('Encoding dictionary is not empty. Please, reset it before applying a new encoding.')
        self.encoding = encoding
    
    def encode(self, lst: list) -> list:
        """
        Encodes a list of public IDs into integer IDs using the built encoding.

        Args:
            lst (list): A list of public IDs.

        Returns:
            (list): A list of encoded integer IDs.
        """
        if self.is_encoded() is False:
            raise ValueError('Encoding dictionary is empty. Please, build the encoding first.')
        return [self.encoding[el] for el in lst]

    def decode(self, lst: list) -> list:
        """
        Creates a reverse mapping from private IDs back to public IDs.

        Args:
            lst (list): A list of private IDs.

        Returns:
            (list): A list of decoded public IDs.
        """
        if self.is_encoded() is False:
            raise ValueError('Encoding dictionary is empty. Please, build the encoding first.')
        decoder = {el: idx for idx, el in self.encoding.items()}
        if len(decoder) != len(self.encoding):
            print('WARNING: the ID encoding could be incorrect. Please, check your data.')
        return [decoder[el] for el in lst]
    

class IncrementalEncoder:
    """
    Streaming-friendly encoder that assigns integer IDs incrementally.

    Preserves reproducibility by keeping both forward (public -> int)
    and reverse (int -> public) mappings without requiring the full list upfront.
    """

    def __init__(self, offset: int = 0):
        self.offset = offset
        self._forward: dict = {}          # public -> int
        self._reverse: list = []          # index -> public (index = id - offset)

    def __len__(self):
        return len(self._forward)

    def encode_one(self, key):
        """
        Encode a single key, creating a new id if unseen.
        """
        if key in self._forward:
            return self._forward[key]
        idx = self.offset + len(self._forward)
        self._forward[key] = idx
        self._reverse.append(key)
        return idx

    def encode_many(self, iterable):
        """
        Encode an iterable of keys, returning a list of int ids.
        """
        return [self.encode_one(k) for k in iterable]

    def decode_one(self, idx: int):
        """
        Decode a single id back to the original key.
        """
        pos = idx - self.offset
        if pos < 0 or pos >= len(self._reverse):
            raise KeyError(f"Id {idx} not in encoder")
        return self._reverse[pos]

    def decode_many(self, iterable):
        """
        Decode an iterable of ids back to original keys.
        """
        return [self.decode_one(i) for i in iterable]

    @property
    def forward(self):
        return self._forward

    @property
    def reverse(self):
        return self._reverse
