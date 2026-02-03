import os
import yaml
import importlib
import urllib.request
from dataclasses import dataclass
from typing import Optional, Union, Dict, Any
from datarec.io.paths import registry_version_filepath, registry_dataset_filepath, pickle_version_filepath
from datarec.data.source import Source, SOURCE_TYPES
from datarec.io.readers.transactions import read_transactions_json, read_transactions_tabular, read_transactions_jsonl
from datarec.io.readers.sequences import read_sequence_tabular_inline, read_sequence_tabular_wide, read_sequences_json, read_sequences_json_array, read_sequence_tabular_implicit
from datarec.data.dataset import DataRec
from datarec import from_pickle

@dataclass
class Resource:
    resource_name: Optional[str] = None
    source_name: Optional[str] = None
    source: Optional[Source] = None
    filename: Optional[str] = None
    type: Optional[str] = None
    format: Optional[str] = None
    required: Optional[bool] = False
    about: Optional[str] = None
    dataset_name: Optional[str] = None
    version: Optional[str] = None
    output_folder: Optional[str] = None
    prepared = False

    def link_source(self, sources: dict[str, Source]):
        """
        Links the resource to its source.
        Args:
            sources (dict): A dictionary containing dataset sources objects.
        Returns:
            (None): None
        """
        if self.source_name is None:
            raise RuntimeError(f"No source provided for resource {self.filename}")
        if self.source_name not in sources:
            raise RuntimeError(f"Source {self.source_name} not found")
        self.source = sources[self.source_name]

    def is_locally_available(self) -> Union[str, bool]:
        """
        Checks if the resource file is available locally.
        Returns:
            (str): The local path of the resource file if available, otherwise False.
        """
        # Check that a source is linked to resource
        if self.source is None:
            raise RuntimeError(f"No source provided for resource {self.filename}")
        resource_path = self.path()
        # Check if resource file already exists
        if os.path.exists(resource_path):
            return True
        return False

    def prepare(self, *args, **kwargs):
        """
        Ensures the resource file is downloaded and available locally.
        """
        if self.source is None:
            raise RuntimeError(f"No source provided for resource {self.filename}")
        
        self.source.prepare()
        resources = self.source.get_resources()
        
        if self.resource_name not in resources:
            raise RuntimeError(f"Resource {self.resource_name} not found in source")
        self.prepared = True

    def path(self):
        """
        Returns the local path of the resource file.
        Raises an error if the output folder is not specified.
        Returns:
            (str): The local path of the resource file.
        """
        output_folder = self.source.output_folder
        if output_folder is None:
            raise ValueError("Must specify an output folder")
        inner_path = self.source.inner_paths.get(self.resource_name, None)
        if inner_path is None:
            raise RuntimeError(f"Resource {self.resource_name} not found in source inner paths")
        return os.path.join(output_folder, inner_path)

    def assign_dataset_info(self, dataset_name:str, version:str):
        """
        Assigns dataset name and version to the resource.
        Args:
            dataset_name (str): The name of the dataset.
            version (str): The version of the dataset.
        Returns:
            (None): None
        """
        self.dataset_name = dataset_name
        self.version = version

    def free_cache(self):
        """
        Frees the cached version of the resource if it exists.
        Returns:
            (None): None
        """
        pass



@dataclass
class Interactions(Resource):
    schema: Optional[dict] = None
    _cache_ready: Optional[bool] = False

    def cache_path(self) -> str:
        """
        Returns the path of the cached version of the resource.
        Returns:
            (str): The path of the cached resource file.
        """
        if self.dataset_name is None or self.version is None:
            raise ValueError("Dataset name and version must be set to get cache path")
        return pickle_version_filepath(self.dataset_name, self.version)

    def _has_cache(self) -> bool:
        """
        Checks if a cached version of the resource exists.
        Returns:
            (bool): True if the cached file exists, otherwise False.
        """
        if self._cache_ready:
            return True
        
        if self.dataset_name is None or self.version is None:
            raise ValueError("Dataset name and version must be set to check for cache")
        self._cache_ready = os.path.exists(self.cache_path())
        return self._cache_ready
        
    def prepare(self, use_cache=True, *args, **kwargs):
        """
        Prepares the resource by ensuring it is downloaded and available locally.
        If a cached version exists, it skips downloading.
        """
        if use_cache is True and self._has_cache():
            self.prepared = True
            print(f"Resource '{self.resource_name}' found in cache. Skipping download.")
            return
        super().prepare(*args, **kwargs)

    def load(self, use_cache=True, to_cache=True) -> DataRec:
        """
        Loads the ratings resource into a DataRec dataset.
        Returns:
            DataRec: The loaded dataset.
        """
        if use_cache and self._has_cache():
            print(f"Loading resource '{self.resource_name}' from cache at {self.cache_path()}.")
            return from_pickle(filepath=self.cache_path())

        if self.format == 'transactions_tabular':
            schema = self.schema
            if schema is None:
                raise ValueError("Schema must be provided for transactions_tabular format")

            dataset = read_transactions_tabular(self.path(), 
                                                sep=schema['sep'],
                                                user_col=schema['user_col'],
                                                item_col=schema['item_col'],
                                                rating_col=schema.get('rating_col', None),
                                                timestamp_col=schema.get('timestamp_col', None),
                                                header=schema.get('header', None),
                                                skiprows=schema.get('skiprows', 0),
                                                cols=schema.get('cols', None),
                                                engine=schema.get('engine', 'c'),
                                                fallback_engine=schema.get('fallback_engine', 'python'),
                                                stream=schema.get('stream', False),
                                                encode_ids=schema.get('encode_ids', False),
                                                chunksize=schema.get('chunksize', 100_000))
        
        elif self.format == 'transactions_json':
            schema = self.schema
            if schema is None:
                raise ValueError("Schema must be provided for transactions json format")

            dataset = read_transactions_json(self.path(),
                                             user_col=schema['user_col'],
                                             item_col=schema['item_col'],
                                             rating_col=schema.get('rating_col', None),
                                             timestamp_col=schema.get('timestamp_col', None),
                                             stream=schema.get('stream', False),
                                             encode_ids=schema.get('encode_ids', False),
                                             chunksize=schema.get('chunksize', 100_000))
        
        elif self.format == 'transactions_jsonl':
            schema = self.schema
            if schema is None:
                raise ValueError("Schema must be provided for transactions jsonl format")

            dataset = read_transactions_jsonl(self.path(),
                                              user_col=schema['user_col'],
                                              item_col=schema['item_col'],
                                              rating_col=schema.get('rating_col', None),
                                              timestamp_col=schema.get('timestamp_col', None),
                                              stream=schema.get('stream', False),
                                              encode_ids=schema.get('encode_ids', False),
                                              chunksize=schema.get('chunksize', 100_000))

        elif self.format == 'sequence_tabular_inline':
            schema = self.schema
            if schema is None:
                raise ValueError("Schema must be provided for sequence tabular inline format")
            
            sequence_col = schema.get('sequence_col', None)
            if sequence_col is None:
                raise ValueError("sequence_col must be provided in schema for sequence tabular inline format")

            dataset = read_sequence_tabular_inline(
                self.path(),
                user_col=schema['user_col'],
                sequence_col=sequence_col,
                sequence_sep=schema.get('sequence_sep', ' '),
                timestamp_col=schema.get('timestamp_col', None),
                meta_cols=schema.get('meta_cols', None),
                col_sep=schema.get('col_sep', ','),
                header=schema.get('header', 0),
                cols=schema.get('cols', None),
                engine=schema.get('engine', 'c'),
                fallback_engine=schema.get('fallback_engine', 'python'),
                stream=schema.get('stream', schema.get('stream_encode', False)),
                encode_ids=schema.get('encode_ids', False),
                chunksize=schema.get('chunksize', 100_000),
            )

        elif self.format == 'sequence_tabular_wide':
            schema = self.schema
            if schema is None:
                raise ValueError("Schema must be provided for sequence tabular wide format")

            dataset = read_sequence_tabular_wide(self.path(),
                                                 user_col=schema.get('user_col', 'user'),
                                                 item_col=schema.get('item_col', 'item'),
                                                 col_sep=schema.get('col_sep', ' '),
                                                 header=schema.get('header', None),
                                                 encode_ids=schema.get('encode_ids', False))

        elif self.format == 'sequence_tabular_implicit':
            schema = self.schema
            if schema is None:
                raise ValueError("Schema must be provided for sequence tabular implicit format")

            dataset = read_sequence_tabular_implicit(self.path(),
                                                     user_col=schema.get('user_col', 'sequence_id'),
                                                     item_col=schema.get('item_col', 'item'),
                                                     col_sep=schema.get('col_sep', ' '),
                                                     header=schema.get('header', None),
                                                     drop_length_col=schema.get('drop_length_col', True),
                                                     encode_ids=schema.get('encode_ids', False))

        elif self.format == 'sequence_json':
            schema = self.schema
            if schema is None:
                raise ValueError("Schema must be provided for sequence json format")

            dataset = read_sequences_json(self.path(),
                                          user_col=schema['user_col'],
                                          item_col=schema['item_col'],
                                          rating_col=schema.get('rating_col', None),
                                          timestamp_col=schema.get('timestamp_col', None))
            
        elif self.format == 'sequence_json_array':
            schema = self.schema
            if schema is None:
                raise ValueError("Schema must be provided for sequence json array format")

            dataset = read_sequences_json_array(self.path(),
                                                user_col=schema['user_col'],
                                                item_col=schema['item_col'],
                                                rating_col=schema.get('rating_col', None),
                                                timestamp_col=schema.get('timestamp_col', None),
                                                sequence_key=schema.get('sequence_key', 'sequence'))

        else:
            raise NotImplementedError(f"Format {self.format} not supported for resource loading.")
        
        if self.dataset_name is None:
            print("Warning: dataset_name is not set for the resource. Using 'unknown_dataset'.")
            self.dataset_name = "unknown_dataset"
        if self.version is None:
            print("Warning: version is not set for the resource. Using 'unknown_version'.")
            self.version = "unknown_version"

        dr = DataRec(rawdata=dataset, dataset_name=self.dataset_name, version_name=self.version, registry_dataset=True)
        
        # cache the dataset in pickle format
        if to_cache:
            dr.to_pickle()

        return dr
    
    def free_cache(self):
        """
        Frees the cached version of the resource if it exists.
        Returns:
            (None): None
        """
        if self._has_cache():
            os.remove(self.cache_path())
            self._cache_ready = False
            print(f"Cache for resource '{self.resource_name}' has been removed.")


RESOURCE_TYPES = {
    'resource': Resource,
    'interactions': Interactions,
    'content': Resource,
    'documentation': Resource
}


def load_dataset_config(dataset_name: str, dataset_version: str = "") -> dict:
    """
    Load a dataset configuration from the local registry.

    Args:
        dataset_name (str): name of the dataset
        dataset_version (str): version of the dataset. When empty, load the dataset-level registry file.
    Returns:
        (dict): dataset configuration
    """
    if dataset_version:
        config_path = registry_version_filepath(dataset_name, dataset_version)
    else:
        config_path = registry_dataset_filepath(dataset_name)
    assert os.path.exists(config_path), f"Config file {config_path} does not exist"
    with open(config_path, "r") as f:
        config = yaml.safe_load(f)
    return config


def load_dataset_config_from_url(url: str) -> dict:
    """
    Load a dataset configuration YAML from a remote URL.

    Args:
        url (str): URL pointing to a registry dataset or version YAML.

    Returns:
        (dict): Parsed dataset configuration.
    """
    try:
        with urllib.request.urlopen(url) as response:
            content = response.read().decode("utf-8")
    except Exception as exc:
        raise RuntimeError(f"Failed to load dataset config from URL: {url}") from exc

    config = yaml.safe_load(content)
    if not isinstance(config, dict):
        raise ValueError("Remote registry config must be a mapping.")
    return config

def set_resource(resource_name: str, resource_conf: dict) -> Resource:
    """
    Given a resource configuration, return a new resource object
    Args:
        resource_name (str): name of the resource
        resource_conf (dict): resource configuration
    Returns:
        (Resource): a dataset resource object"""
    resource_typename = resource_conf.get('type', 'Resource')
    resource_type = RESOURCE_TYPES.get(resource_typename.lower(), None)
    if resource_type is None:
        raise ValueError(f'Resource type {resource_typename.lower()} not allowed. Available resource types: {RESOURCE_TYPES.keys()}.')
    resource = resource_type(**resource_conf)
    resource.resource_name = resource_name
    return resource

def set_resources(config:dict) -> dict[str, Resource]:
    """
    Given a dataset configuration, return a new dataset configuration
    Args:
        config (dict): dataset configuration
    Returns:
        (dict): a dictionary containing dataset sources objects
    """
    resources = dict()
    for resource_name, raw_resource in config['resources'].items():
        resources[resource_name] = set_resource(resource_name, raw_resource)
    return resources

def load_class(class_import: str):
    """
    Given a class import name, return a class object
    """
    module_name, class_name = class_import.rsplit(".", 1)
    module = importlib.import_module(module_name)
    return getattr(module, class_name)

def load_versions(dataset_name:str)->dict:
    """
    Given a dataset name, return a dictionary containing dataset versions and relative classes
    """
    conf = load_dataset_config(dataset_name)
    return {n: load_class(m) for n, m in conf['versions'].items()}

def find_ratings_resource(resources:dict)->Interactions:
    """
    Given a dictionary of resources, return the ratings resource
    Args:
        resources (dict): a dictionary containing dataset resources objects
    Returns:
        (Resource): the ratings resource object
    """
    for res in resources.values():
        if res.type == 'ratings':
            return res
    raise RuntimeError(f"Resource type 'ratings' not found in resources")

def find_resource_by_type(resources:dict, rtype:str)->Dict[str, Resource]:
    """
    Given a dictionary of resources, return the ratings resource
    Args:
        resources (dict): a dictionary containing dataset resources objects
        rtype (str): resource type to find
    Returns:
        (Resource): the ratings resource object
    """
    found = {}
    for res in resources.values():
        if res.type == rtype:
            found[res.resource_name] = res
    if len(found) == 0:
        raise RuntimeError(f"Resource type '{rtype}' not found in resources")
    return found
