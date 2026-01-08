import pytest
from pathlib import Path
from datarec.io import paths as p


def test_dataset_paths_use_cache_dir(monkeypatch, tmp_path):
    base = tmp_path / "cache_root"

    def fake_cache_dir():
        base.mkdir(parents=True, exist_ok=True)
        return base.resolve()

    monkeypatch.setattr(p, "cache_dir", fake_cache_dir)

    # dataset_directory should be rooted under cache_dir and not auto-create subfolders
    root = Path(p.dataset_directory("foo"))
    assert root == base / "foo"
    assert not root.exists()

    # version directory path should compose under dataset_directory
    ver = Path(p.dataset_version_directory("foo", "v1"))
    assert ver == base / "foo" / "v1"
    assert not ver.exists()

    # raw directory path should append RAW_DATA_FOLDER
    raw = Path(p.dataset_raw_directory("foo", "v1"))
    assert raw == ver / p.RAW_DATA_FOLDER

    # processed directory path should append PROCESSED_DATA_FOLDER
    proc = Path(p.dataset_processed_directory("foo"))
    assert proc == base / "foo" / p.PROCESSED_DATA_FOLDER

    # dataset_filepath should point to dataset file under dataset_directory
    data_path = Path(p.dataset_filepath("foo"))
    assert data_path == base / "foo" / p.DATASET_NAME

    # pickle_version_filepath should live under version directory
    pkl = Path(p.pickle_version_filepath("foo", "v1"))
    assert pkl == ver / f"foo_v1.pkl"


def test_registry_paths_suffixes():
    assert str(p.registry_dataset_filepath("foo")).endswith("registry/datasets/foo.yml")
    assert str(p.registry_version_filepath("foo", "v1")).endswith("registry/versions/foo_v1.yml")
    assert str(p.registry_metrics_filepath("foo", "v1")).endswith("registry/metrics/foo_v1.yml")
