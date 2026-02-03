import os
import pytest

from datarec.data.datarec_builder import RegisteredDataset
from datarec.data.resource import load_dataset_config


def dataset_versions(dataset_name: str) -> list[str]:
    """
    Return declared versions for a dataset from the registry config.
    """
    conf = load_dataset_config(dataset_name)
    versions = conf.get("versions", [])
    if isinstance(versions, dict):
        versions = list(versions.keys())
    return list(versions)


def check_dataset(dataset_name: str, version: str, *, only_required: bool = True) -> None:
    """
    Prepare and load a dataset version, performing basic sanity checks.
    """
    manual_datasets = {"yelp", "tmall", "mind"}
    if dataset_name in manual_datasets and not os.getenv("DATAREC_MANUAL"):
        pytest.skip("Manual dataset download required; set DATAREC_MANUAL=1 to enable.")
    dset = RegisteredDataset(dataset_name=dataset_name, version=version)
    dset.prepare(use_cache=True, only_required=only_required)
    dr = dset.load(use_cache=True, to_cache=False, only_required=only_required)

    assert len(dr) > 0, f"{dataset_name} {version} should have interactions"
    assert dr.n_users > 0 and dr.n_items > 0, f"{dataset_name} {version} users/items must be > 0"
    assert dr.user_col is not None and dr.item_col is not None
    # Ensure no NaN in user/item columns
    assert not dr.data[dr.user_col].isna().any()
    assert not dr.data[dr.item_col].isna().any()
