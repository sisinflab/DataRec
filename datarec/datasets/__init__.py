from datarec.datasets.base import DatasetEntryPoint
from datarec.data.datarec_builder import Dataset
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

def load_dataset(name: str, version: str = "latest", **kwargs) -> Dataset:
    """
    Instantiate a dataset by registry name, validating available versions.
    """
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
