import os
from typing import List, Union, Dict, Any, Iterable, Collection
from abc import ABC, abstractmethod
from datarec.data.dataset import DataRec
from datarec.data.resource import load_dataset_config, set_resources, find_resource_by_type, find_ratings_resource, load_versions
from datarec.io.paths import dataset_raw_directory, RAW_DATA_FOLDER, pickle_version_filepath
from datarec.data.source import set_sources



class Dataset:

    def __init__(self, dataset_name:str, version:str, folder=None):

        self.dataset_name = dataset_name
        self.version = version
        self.output_folder = self.find_output_folder(folder=folder)
        self.config = load_dataset_config(dataset_name=self.dataset_name,
                                          dataset_version=self.version)
        
        # sets sources and resources data structures
        self.sources = set_sources(self.config, folder=self.output_folder)
        self.resources = set_resources(self.config)
        
        # links resources with sources and dataset info
        for resource in self.resources.values():
            resource.link_source(self.sources)
            resource.assign_dataset_info(self.dataset_name, self.version)
            resource.output_folder = self.output_folder
        
        # initialize prepared resources dictionary to keep track of prepared resources
        self.prepared_resources = {}


    def find_resource_by_constraints(
        self,
        *,
        only_required: bool = True,
        resource_types: Union[Collection[str], str, None] = None,
        resource_names: Union[Collection[str], str, None] = None):

        collection = self.resources
        if len(collection) == 0:
            raise ValueError('No prepared resource found. Use the method .prepare to prepare the dataset resources.')

        if isinstance(resource_types, str):
            resource_types = [resource_types]

        if isinstance(resource_names, str):
            resource_names = [resource_names]

        selected: dict[str, Any] = {}
        for res_name, res in collection.items():
            res_type = res.type
            # filter by required attribute
            if only_required and not res.required:
                continue
            # filter by resource type
            if resource_types is not None:
                if res_type not in resource_types:
                    continue
            # filter by resource name
            if resource_names is not None:
                if res_name not in resource_names:
                    continue

            selected |= {res_name: res}

        return selected


    def prepare(
        self,
        *,
        only_required: bool = True,
        use_cache: bool = True,
        resource_types: Union[Collection[str], str, None] = None,
        resource_names: Union[Collection[str], str, None] = None):
        """
        Prepare (download and decompress) all selected resources.
        Args:
            only_required (bool): Prepare only resources marked as required when True.
            use_cache (bool): Use cached resources when True.
            resource_types (Collection[str] | str | None): Resource types to include; all when None.
            resource_names (Collection[str] | str | None): Specific resource names to include; all when None.
        Returns:
            dict[str, Any]: Map from resource name to the prepared artifact (e.g. local path).
        """

        selected = self.find_resource_by_constraints(
            only_required=only_required,
            resource_names=resource_names,
            resource_types=resource_types)
        
        if len(selected) == 0:
            print('No resource found with the given requirements.')
        
        for res_name, res in selected.items():
            if res_name in self.prepared_resources.keys():
                print(f"Resource {res_name} was already prepared.")
                continue
            res.prepare(use_cache=use_cache)
            print(f"Resource {res_name} ready")
            self.prepared_resources |= {res_name: res}

    def prepare_interactions(
        self,
        *,
        only_required: bool = True,
        use_cache: bool = True,
        resource_names: Union[Collection[str], str, None] = None):
        """
        Prepare (download and decompress) ratings resources.
        Args:
            only_required (bool): Prepare only resources marked as required when True.
            use_cache (bool): Use cached resources when True.
            resource_names (Collection[str] | str | None): Specific resource names to include; all when None.
        Returns:
            dict[str, Any]: Map from resource name to the prepared artifact (e.g. local path).
        """
        self.prepare(
                    resource_types='interactions',
                    only_required=only_required,
                    use_cache=use_cache,
                    resource_names=resource_names)


    def load(
        self, *,
        use_cache: bool = False,
        to_cache: bool = False,
        resource_name: Union[str, None] = None,
        resource_type: Union[str, None] = 'interactions',
        only_required: bool = False) -> DataRec:
        """
        Load the dataset into a DataRec object.
        Args:
            use_cache (bool): Load from cache when True.
            to_cache (bool): Save to cache when True.
            resource_name (str | None): Specific resource name to load; all when None.
            resource_type (str | None): Resource type to load; all when None.
            only_required (bool): When True, consider only resources marked as required.
        Returns:
            DataRec: The loaded dataset.
        """
        resource = self.find_resource_by_constraints(
            only_required=only_required,
            resource_names=resource_name,
            resource_types=resource_type)
        if len(resource) > 1:
            raise ValueError(f'More than one resource match the name: {resource_name} and type: {resource_type}.\n \
                             Resources found: {resource.keys}. Please, select one by using the resource_name attribute.')
        if len(resource) == 0:
            raise ValueError(f'No resource found that matches the name: {resource_name} and type: {resource_type}')
        
        if len(resource) == 1:
            res_name, res = next(iter(resource.items()))
            if res.type == 'interactions':
                if res.prepared == True:
                    return res.load(use_cache=use_cache, to_cache=to_cache)
                else:
                    raise ValueError(f'Resource \'{res_name}\' must be prepared before loading it. Try calling .prepare method before.')
            else:
                raise ValueError(f'DataRec does not support load method for resources with \'{res.type}\' type.\
                                 This version of DataRec supports only \'ratings\' type.')
        
        raise ValueError('Something went wrong while loading the resource')

    def prepare_and_load(self) -> DataRec:
        """
        A convenience method that runs the full prepare and load pipeline.

        Returns:
            (DataRec): The fully prepared and loaded dataset.
        """
        self.prepare()
        return self.load()


    def prepare_content(self, ctype:str='all'):
        """
        Prepares content resources of the specified type.
        Args:
            ctype (str): The type of content to prepare. Use 'all' to prepare all content types.
        Raises:
            AssertionError: If the specified content type is not found.
        Returns:
            (None): None
        """
        resources = find_resource_by_type(self.resources, 'content')
        ctypes = set(resources.keys())
        assert ctype in ctypes or ctype == 'all', f"Content type {ctype} not found. Available content types: {ctypes}"
        if ctype == 'all':
            for res in resources.values():
                res_name = res.resource_name
                if res_name in self.prepared_resources:
                    continue
                res_path = res.prepare()
                self.prepared_resources = {res_name: res_path}
        else:
            res = resources[ctype]
            res_path= res.prepare()
            self.prepared_resources = {res.resource_name: res_path}

    def download(self)->List[str]:
        """
        Downloads the raw dataset files.
        Returns:
            (str): The path to the downloaded files.
        """
        resources = []
        for source in self.sources.values():
            resources.append(source.download())
        return resources

    def find_output_folder(self, folder=None) -> str:
        """
        Find the output folder for the given dataset and version.
        Args:
            folder (str): Explicit output folder path.
        Returns:
            (str): The output folder path.
        """
        if folder:
            return os.path.abspath(os.path.join(folder, RAW_DATA_FOLDER))
        return os.path.join(dataset_raw_directory(self.dataset_name, self.version))
    
    def free_cache(self, 
                   *,
                   resource_types: Union[Collection[str], str, None] = None,
                   resource_names: Union[Collection[str], str, None] = None):
        
        selected = self.find_resource_by_constraints(
            resource_names=resource_names,
            resource_types=resource_types)
        for res in selected.values():
            res.free_cache()
