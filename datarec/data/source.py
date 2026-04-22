import os
import shutil
from pathlib import Path
import requests
from dataclasses import dataclass
from typing import Optional, Union, Dict
from datarec.data.utils import verify_checksum
from datarec.data.download import decompress_file
import gdown

@dataclass
class Source:
    checksum: str = None
    checksums: Optional[Dict[str, str]] = None
    checksum_algorithm: str = "md5"
    prepared: bool = False
    source_name: Optional[str] = None
    filename: Optional[str] = None
    archive: Optional[str] = None
    inner_paths: Optional[Dict[str, str]] = None
    downloadable: bool = False
    output_folder: Optional[str] = None

    def path(self, output_folder=None) -> str:
        if output_folder is None:
            if self.output_folder is None:
                raise ValueError("Must specify an output folder")
            output_folder = self.output_folder
        return os.path.join(output_folder, self.filename)

    def is_locally_available(self, output_folder=None) -> bool:
        """
        Check if the source file exists in the output folder.
        """
        if output_folder is None:
            if self.output_folder is None:
                raise ValueError("Must specify an output folder")
        return os.path.exists(self.path())

    def verify_checksum(self, output_folder=None) -> None:
        print(f'{self.filename}: verifying checksum')
        if output_folder is None:
            output_folder = self.output_folder
        verify_checksum(self.path(output_folder), self.checksum, self.checksum_algorithm)

    def download(self) -> str:
        pass

    def prepare(self) -> None:
        """
        Prepares the source by downloading it if not available locally
        and verifying its checksum.
        Returns:
            (None)
        """
        if self.prepared:
            return
        # check if source file exists, if not download it
        if not self.is_locally_available():
            self.download()
        # verify source checksum
        self.verify_checksum()
        self.prepared = True

    def resource_paths(self) -> Dict[str, str]:
        """
        Returns a dictionary containing the paths of the resources inside the source.
        Returns:
            (dict): A dictionary containing the paths of the resources inside the source.
        """
        resources_path = {res: os.path.join(self.output_folder, inner_path) for res, inner_path in self.inner_paths.items()}
        return resources_path
    
    def resources_available(self) -> bool:
        """
        Check if all resources inside the source are available locally.
        Returns:
            (bool): True if all resources are available, False otherwise.
        """
        resource_paths = self.resource_paths()
        for resource_path in resource_paths.values():
            if not os.path.exists(resource_path):
                return False
        return True
        

    def get_resources(self, force=False) -> Dict[str, str]:
        """
        Returns a dictionary containing the paths of the resources inside the source.
        Args:
            force (bool): If True, forces re-extraction of resources even if they are already available.
        Returns:
            (dict): A dictionary containing the paths of the resources inside the source.
        """
        if self.resources_available() and not force:
            return self.resource_paths()

        if self.archive:
            decompress_file(self.path(), self.output_folder, self.archive)
        resources = {}
        for resource, inner_path in self.inner_paths.items():
            resource_path = os.path.join(self.output_folder, inner_path)
            if os.path.exists(resource_path):
                resources[resource] = resource_path
        return resources

@dataclass
class HttpSource(Source):
    url: str = None

    def download(self, output_folder=None) -> str:

        if output_folder is None:
            output_folder = self.output_folder

        if self.filename is None:
            raise RuntimeError(f"No filename provided")

        output_path = os.path.join(output_folder, self.filename)

        if not os.path.exists(output_folder):
            os.makedirs(output_folder)

        if os.path.exists(output_path):
            print(f"{self.filename}: File already exists, skipping download")
            return output_path

        response = requests.get(self.url, stream=True)
        response.raise_for_status()

        total = int(response.headers.get("content-length", 0))
        chunk_size = 8192
        downloaded = 0

        print(f"Downloading {self.filename} from {self.url}")
        with open(output_path, "wb") as f:
            for chunk in response.iter_content(chunk_size):
                if not chunk:
                    continue
                f.write(chunk)
                downloaded += len(chunk)
                if total:
                    percent = int(downloaded * 100 / total)
                    print(f"\r{self.filename}: {percent}% ({downloaded}/{total} bytes)", end="", flush=True)
                else:
                    print(f"\r{self.filename}: {downloaded} bytes downloaded", end="", flush=True)

        print()  # ensure newline after carriage returns
        print(f"{self.filename} downloaded from {self.url}")


@dataclass
class GdownSource(Source):
    url: str = None

    def download(self, output_folder=None) -> str:

        if output_folder is None:
            output_folder = self.output_folder

        if self.filename is None:
            raise RuntimeError(f"No filename provided")

        output_path = os.path.join(output_folder, self.filename)

        if not os.path.exists(output_folder):
            os.makedirs(output_folder)

        if os.path.exists(output_path):
            print(f"{self.filename}: File already exists, skipping download")
            return output_path

        gdown.download(self.url, output_path, quiet=False)

        print()  # ensure newline after carriage returns
        print(f"{self.filename} downloaded from {self.url}")

@dataclass
class KaggleSource(Source):
    dataset_name: str = None

    def _validate_multi_file_checksums(self) -> None:
        if self.checksums is None:
            return
        if self.inner_paths is None:
            raise RuntimeError("KaggleSource defines 'checksums' but no 'inner_paths'")

        checksum_keys = set(self.checksums.keys())
        inner_path_keys = set(self.inner_paths.keys())
        if checksum_keys != inner_path_keys:
            raise RuntimeError(
                f"KaggleSource checksums keys must match inner_paths keys. "
                f"checksums={sorted(checksum_keys)}, inner_paths={sorted(inner_path_keys)}"
            )

    def is_locally_available(self, output_folder=None) -> bool:
        """
        Kaggle datasets may materialize multiple files, so availability is based
        on the declared resources rather than on a single filename.
        """
        if output_folder is None:
            output_folder = self.output_folder
        if output_folder is None:
            raise ValueError("Must specify an output folder")

        if self.inner_paths:
            return self.resources_available()

        if self.filename is None:
            raise RuntimeError("KaggleSource requires either 'inner_paths' or 'filename'")

        return os.path.exists(os.path.join(output_folder, self.filename))

    def verify_checksum(self, output_folder=None) -> None:
        """
        Preserve the existing checksum flow for single-file Kaggle sources while
        allowing multi-file sources to verify each declared file.
        """
        if output_folder is None:
            output_folder = self.output_folder

        if self.checksums is not None:
            self._validate_multi_file_checksums()
            print(f"{self.source_name}: verifying checksums")
            for resource_name, expected_checksum in self.checksums.items():
                inner_path = self.inner_paths[resource_name]
                file_path = os.path.join(output_folder, inner_path)
                print(f"{resource_name}: verifying checksum")
                verify_checksum(file_path, expected_checksum, self.checksum_algorithm)
            return

        if self.checksum is None:
            return

        if self.filename is None:
            print(f"{self.source_name}: skipping checksum verification for multi-file Kaggle source")
            return

        super().verify_checksum(output_folder)

    def download(self, output_folder=None) -> str:
        import kagglehub

        if output_folder is None:
            output_folder = self.output_folder

        if not os.path.exists(output_folder):
            os.makedirs(output_folder)

        if self.is_locally_available(output_folder):
            label = self.filename or self.dataset_name or self.source_name
            print(f"{label}: Files already available, skipping download")
            if self.filename is not None:
                return os.path.join(output_folder, self.filename)
            return output_folder

        if self.dataset_name is None:
            raise RuntimeError("No Kaggle dataset_name provided")

        self._validate_multi_file_checksums()
        
        # kaggle downloads files in its own cache folder, so we need to move it to the output folder
        kaggle_path = Path(kagglehub.dataset_download(self.dataset_name))

        if self.inner_paths:
            missing = [path for path in self.inner_paths.values() if not (kaggle_path / path).exists()]
            if missing:
                raise RuntimeError(
                    f"Expected files not found in Kaggle download path {kaggle_path}: {missing}"
                )
        elif self.filename is not None:
            kaggle_filename = kaggle_path / self.filename
            if not kaggle_filename.exists():
                raise RuntimeError(f"File {self.filename} not found in Kaggle download path {kaggle_filename}")
        else:
            raise RuntimeError("KaggleSource requires either 'inner_paths' or 'filename'")
        
        # we move all the downloaded files to avoid downloading them again in the future
        for item in kaggle_path.iterdir():
            destination = Path(output_folder) / item.name
            if item.is_dir():
                shutil.copytree(item, destination, dirs_exist_ok=True)
            else:
                shutil.copy2(item, destination)

        print()  # ensure newline after carriage returns
        label = self.filename or self.dataset_name or self.source_name
        print(f"{label} downloaded from Kaggle")
        if self.filename is not None:
            return os.path.join(output_folder, self.filename)
        return output_folder

@dataclass
class ManualSource(Source):
    message: str = ''

    def download(self) -> str:
        print(self.message)
        os.makedirs(self.output_folder, exist_ok=True)
        print(f"Then, place the downloaded files in the following directory:\n'{self.output_folder}")
        input('Press Enter to continue after downloading the dataset...')

        output_path = os.path.join(self.output_folder, self.filename)
        if not os.path.exists(output_path):
            raise FileNotFoundError(f'File not found. The file was expected to be found at \'{output_path}\'')
        print('File found, continuing...')
        return output_path


@dataclass
class NestedSource(Source):
    parent_source_name: str = ''
    parent_source: Optional[Source] = None

    # def path(self, output_folder=None) -> str:
    #     output_folder = self.parent_source.output_folder
    #     if output_folder is None:
    #         raise ValueError("Must specify an output folder")
    #     if self.parent_source is None:
    #         raise RuntimeError('Parent source {self.parent_source_name} is not available. You need to link the parent source before (see self.link_parent_source).')
        
    #     inner_paths = self.parent_source.inner_paths
    #     if inner_paths is None:
    #         raise RuntimeError(f'Inner paths not found in parent source \'{self.parent_source_name}\'.')
        
    #     inner_path = inner_paths.get(self.source_name, None)
    #     if inner_path is None:
    #         raise RuntimeError(f"NestedSource {self.source_name} not found in parent source \'{self.parent_source_name}\' inner paths")
        
    #     return os.path.join(output_folder, inner_path)

    def link_parent_source(self, sources: dict[str, Source]):
        """
        Links the resource to its source.
        Args:
            sources (dict): A dictionary containing dataset sources objects.
        Returns:
            (None): None
        """
        if self.parent_source_name is None:
            raise RuntimeError(f"No source provided for resource {self.filename}")
        if self.parent_source_name not in sources:
            raise RuntimeError(f"Source {self.parent_source_name} not found")
        self.parent_source = sources[self.parent_source_name]

        output_folder = self.parent_source.output_folder
        if output_folder is None:
            raise ValueError("Must specify an output folder")

        inner_paths = self.parent_source.inner_paths
        if inner_paths is None:
            raise RuntimeError(f'Inner paths not found in parent source \'{self.parent_source_name}\'.')
        
        inner_path = inner_paths.get(self.source_name, None)
        if inner_path is None:
            raise RuntimeError(f"NestedSource {self.source_name} not found in parent source \'{self.parent_source_name}\' inner paths")
        
        inner_parent_path = os.path.dirname(inner_path)
        self.output_folder = os.path.join(self.parent_source.output_folder, inner_parent_path)


    def prepare(self) -> None:
        """
        Prepares the source by downloading it if not available locally
        and verifying its checksum.
        Returns:
            (None)
        """
        if self.prepared:
            return
        # check if source file exists, if not download it
        if not self.is_locally_available():
            if self.parent_source_name is None:
                raise RuntimeError(f"Parent source name not defined for nested source")
            if self.parent_source is None:
                raise RuntimeError(f"Parent source not set for nested source")
            
            # prepare parent source
            if not self.parent_source.prepared:
                self.parent_source.prepare()
            
            # check that this resource is available in parent source
            resources = self.parent_source.get_resources()
            if self.source_name not in resources:
                raise RuntimeError(f"Resource {self.filename} not found in parent source")
            
            # verify checksum
            self.verify_checksum()
            
            self.prepared = True
        return


SOURCE_TYPES = {
    'Source': Source,
    'HttpSource': HttpSource,
    'GdownSource': GdownSource,
    'ManualSource': ManualSource,
    'KaggleSource': KaggleSource,
    'NestedSource': NestedSource
}


def set_source(source_name:str, source_conf:dict) -> Source:
    """
    Given a resource configuration, return a new resource object
    Args:
        resource_name (str): name of the resource
        raw_resource (dict): resource configuration
    Returns:
        (Source): a dataset source object
    """
    source_type_name = source_conf['source_type']
    if source_type_name not in SOURCE_TYPES:
        raise ValueError(f"Unsupported source type '{source_type_name}'. Supported types: {', '.join(SOURCE_TYPES.keys())}")    
    source_type = SOURCE_TYPES[source_type_name]
    source = source_type(source_name=source_name, **source_conf['args'])
    return source

def set_sources(config:dict, folder:Optional[str]=None) -> dict[str, Source]:
    """
    Given a dataset configuration, return a new dataset configuration
    Args:
        config (dict): dataset configuration
        folder (str): source output folder
    Returns:
        (dict): a dictionary containing dataset sources objects
    """
    sources = dict()
    for source_name, raw_source in config['sources'].items():
        source = set_source(source_name, raw_source)
        if folder is not None:
            source.output_folder = folder
        sources[source_name] = source

    # link parent source to nested sources, if any
    for source in sources.values():
        if isinstance(source, NestedSource):
            source.link_parent_source(sources)
    return sources
