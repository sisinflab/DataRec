import pytest
from datarec.io.paths import get_cache_dir
from appdirs import user_cache_dir
from pathlib import Path


def test_cache_dir_respects_env_variable_and_reuses_existing_dir(tmp_path, monkeypatch):
    """
    Test that get_cache_dir creates the directory if it doesn't exist,
    and reuses it if already present without deleting its contents.
    """
    ...
    custom_cache_dir = tmp_path / "custom_cache"
    monkeypatch.setenv("DATAREC_CACHE_DIR", str(custom_cache_dir))

    # First call: should create the directory
    path1 = get_cache_dir()
    assert path1.exists()
    assert path1.is_dir()

    # Write a marker file
    marker = path1 / "marker.txt"
    marker.write_text("datarec")

    # Second call: should return the same path and preserve the data
    path2 = get_cache_dir()
    assert path2.exists()
    assert (path2 / "marker.txt").read_text() == "datarec"
    assert path1 == path2


def test_cache_dir_uses_default_location_and_matches_expected():
    """
    Test that get_cache_dir uses the OS-specific default cache location
    and that the returned path matches what is expected.
    """
    expected = Path(user_cache_dir("datarec", "sisinflab")).resolve()
    result = get_cache_dir()
    assert result == expected
    assert result.exists()
    assert result.is_dir()
