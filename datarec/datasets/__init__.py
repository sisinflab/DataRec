from typing import Optional

from urllib.parse import urlparse
from datarec.datasets.base import DatasetEntryPoint
from datarec.data.datarec_builder import RegisteredDataset
from datarec.registry.utils import available_datasets
from datarec.data.resource import load_dataset_config


def list_datasets() -> list[str]:
    """Return the built-in dataset names registered in DataRec."""
    return sorted(available_datasets())

def list_dataset_versions(name: str) -> list[str]:
    """Return all available versions for a registered dataset."""
    conf = load_dataset_config(name)
    return list(conf.get("versions", []))

def latest_dataset_version(name: str) -> str:
    """Return the latest version for a registered dataset."""
    return load_dataset_config(name)["latest_version"]

def _is_url(value: str) -> bool:
    parsed = urlparse(value)
    return parsed.scheme in ("http", "https") and bool(parsed.netloc)


def load_dataset(name: str, version: str = "latest", **kwargs) -> RegisteredDataset:
    """
    Instantiate a dataset by registry name, or load a dataset from a remote registry YAML.

    If `name` is a URL, this delegates to `load_dataset_from_url`.
    """
    if _is_url(name):
        prepare_and_load = kwargs.pop("prepare_and_load", True)
        folder = kwargs.pop("folder", None)
        return load_dataset_from_url(name, folder=folder, prepare_and_load=prepare_and_load)

    if name not in available_datasets():
        raise ValueError(f"Dataset '{name}' is not registered. Available: {', '.join(list_datasets())}")

    if version == "latest":
        version = latest_dataset_version(name)

    if version not in list_dataset_versions(name):
        raise ValueError(
            f"Unsupported version '{version}' for dataset '{name}'. "
            f"Supported versions: {', '.join(list_dataset_versions(name))}"
        )

    for cls in DatasetEntryPoint.__subclasses__():
        if cls.dataset_name == name:
            return cls(version=version, **kwargs)

    raise ValueError(f"No entrypoint registered for dataset '{name}'.")


def load_dataset_from_url(url: str, *, folder: Optional[str] = None, prepare_and_load: bool = True):
    """
    Load a dataset from a remote registry YAML.

    Args:
        url (str): URL to a registry version YAML.
        folder (str | None): Optional output folder override.
        prepare_and_load (bool): When True, returns a loaded DataRec; otherwise returns RegisteredDataset.

    Returns:
        RegisteredDataset | DataRec: The dataset entrypoint or loaded dataset.
    """
    dataset = RegisteredDataset.from_url(url, folder=folder)
    if prepare_and_load:
        return dataset.prepare_and_load()
    return dataset

class AlibabaiFashion(DatasetEntryPoint):
    dataset_name = "alibaba_ifashion"

class AmazonBaby(DatasetEntryPoint):
    dataset_name = "amazon_baby"

class AmazonBeauty(DatasetEntryPoint):
    dataset_name = "amazon_beauty"

class AmazonBooks(DatasetEntryPoint):
    dataset_name = "amazon_books"

class AmazonClothing(DatasetEntryPoint):
    dataset_name = "amazon_clothing"

class AmazonMusic(DatasetEntryPoint):
    dataset_name = "amazon_music"

class AmazonOffice(DatasetEntryPoint):
    dataset_name = "amazon_office"

class AmazonSportsOutdoors(DatasetEntryPoint):
    dataset_name = "amazon_sports_and_outdoors"

class AmazonToysGames(DatasetEntryPoint):
    dataset_name = "amazon_toys_and_games"

class AmazonVideoGames(DatasetEntryPoint):
    dataset_name = "amazon_videogames"

class Ambar(DatasetEntryPoint):
    dataset_name = "ambar"

class CiaoDVD(DatasetEntryPoint):
    dataset_name = "ciao"

class CiteULike(DatasetEntryPoint):
    dataset_name = "citeulike"

class Epinions(DatasetEntryPoint):
    dataset_name = "epinions"

class Gowalla(DatasetEntryPoint):
    dataset_name = "gowalla"

class LastFM(DatasetEntryPoint):
    dataset_name = "lastfm"

class MIND(DatasetEntryPoint):
    dataset_name = "mind"

class Movielens(DatasetEntryPoint):
    dataset_name = "movielens"

class Yelp(DatasetEntryPoint):
    dataset_name = "yelp"

class Tmall(DatasetEntryPoint):
    dataset_name = "tmall"
