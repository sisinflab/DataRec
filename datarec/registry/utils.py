import os
import yaml
from typing import List, Dict, Any
from datetime import datetime, timezone
from pathlib import Path
from datarec.data.resource import load_dataset_config
from datarec.data.datarec_builder import RegisteredDataset
from datarec.data.characteristics import CHARACTERISTICS
from datarec.io.paths import (
    REGISTRY_DATASETS_FOLDER,
    REGISTRY_METRICS_FOLDER,
    registry_metrics_filepath,
)

def available_datasets()->List[str]:
    """
    Return a list of available built-in datasets
    Returns:
        List[str]: list of built-in datasets
    """
    return sorted([d.replace('.yml', '') for d in os.listdir(REGISTRY_DATASETS_FOLDER)])

def print_available_datasets()->None:
    """
    Prints the list of available built-in datasets
    Returns:
        None
    """
    print("""
DataRec built-in datasets:
- """+'\n - '.join(available_datasets()))


def compute_dataset_characteristics(dataset_name: str,
                                    version: str,
                                    *,
                                    output_dir: str = REGISTRY_METRICS_FOLDER,
                                    use_cache: bool = True,
                                    overwrite: bool = False) -> str:
    """
    Compute and persist characteristics for a specific dataset/version.

    Returns:
        Path to the written YAML file.
    """
    os.makedirs(output_dir, exist_ok=True)
    out_path = registry_metrics_filepath(dataset_name, version)

    if os.path.exists(out_path) and not overwrite:
        print(f"Skip {dataset_name} {version}: file exists ({out_path})")
        return out_path

    dset = Dataset(dataset_name=dataset_name, version=version)
    dset.prepare(use_cache=use_cache)
    dr = dset.load(use_cache=use_cache, to_cache=use_cache, only_required=True)

    characteristics = {}
    for name, func in CHARACTERISTICS.items():
        try:
            value = func(dr)
            # Make YAML-friendly: unwrap numpy scalars if possible
            if hasattr(value, "item"):
                try:
                    value = value.item()
                except Exception:
                    pass
            characteristics[name] = value
        except Exception as exc:
            characteristics[name] = None
            characteristics[f"{name}_error"] = str(exc)

    payload = {
        "dataset": dataset_name,
        "version": version,
        "computed_at": datetime.now(timezone.utc).isoformat(),
        "characteristics": characteristics,
    }

    with open(out_path, "w") as f:
        yaml.safe_dump(payload, f, sort_keys=False)

    print(f"Wrote {out_path}")
    return out_path


def get_metrics_filepath(dataset_name: str, version: str) -> str:
    """
    Return the expected registry metrics filepath for a dataset/version.
    """
    return registry_metrics_filepath(dataset_name, version)


def compute_all_characteristics(output_dir: str = REGISTRY_METRICS_FOLDER,
                                use_cache: bool = True,
                                overwrite: bool = False) -> None:
    """
    Compute characteristics for every dataset/version and write YAML files.
    """
    os.makedirs(output_dir, exist_ok=True)

    for ds_name in available_datasets():
        conf = load_dataset_config(ds_name)
        versions = conf.get("versions", [])
        if isinstance(versions, dict):  # support both list and dict configs
            versions = list(versions.keys())

        for version in versions:
            try:
                compute_dataset_characteristics(
                    dataset_name=ds_name,
                    version=version,
                    output_dir=output_dir,
                    use_cache=use_cache,
                    overwrite=overwrite,
                )
            except Exception as exc:  # noqa: BLE001
                print(f"Failed {ds_name} {version}: {exc}")

