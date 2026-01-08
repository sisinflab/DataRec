from datarec.data.datarec_builder import Dataset
from datarec.data.resource import load_dataset_config, load_versions

class DatasetEntryPoint:
    """Common entrypoint for versioned datasets."""

    dataset_name: str = ""

    def __new__(cls, version: str = "latest", **kwargs) -> Dataset:
        if not cls.dataset_name:
            raise ValueError(f"{cls.__name__}: dataset_name is not defined")

        conf = load_dataset_config(cls.dataset_name)
        versions = conf["versions"]
        latest_version = conf["latest_version"]

        if version not in versions and version != "latest":
            # no accepted version found
            supported = ", ".join(versions)
            raise ValueError(
                f"{cls.dataset_name} {version}: unsupported version. "
                f"Supported versions: {supported}"
            )
        if version == "latest":
            version = latest_version

        return Dataset(dataset_name=cls.dataset_name, version=version, **kwargs)