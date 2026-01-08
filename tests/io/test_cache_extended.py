from pathlib import Path

import pytest

from datarec.io import cache as c


def test_cache_size_and_list(tmp_path, monkeypatch):
    # isolate cache root
    monkeypatch.setenv("DATAREC_CACHE_DIR", str(tmp_path / "cache_root"))
    c.reset_cache_dir()
    root = c.cache_dir()
    # create nested structure
    subdir = root / "foo"
    subdir.mkdir(parents=True, exist_ok=True)
    f1 = subdir / "a.txt"
    f1.write_text("abc", encoding="utf-8")
    f2 = root / "b.txt"
    f2.write_text("abcd", encoding="utf-8")

    contents = c.list_cache_contents(max_depth=1)
    paths = {Path(entry.path) for entry in contents}
    assert subdir in paths
    assert f2 in paths

    size_all = c.cache_size()
    assert size_all >= len("abc") + len("abcd")
    size_sub = c.cache_size("foo")
    assert size_sub >= len("abc")


def test_clear_cache_force(tmp_path, monkeypatch):
    monkeypatch.setenv("DATAREC_CACHE_DIR", str(tmp_path / "cache_root"))
    c.reset_cache_dir()
    root = c.cache_dir()
    target = root / "dataset" / "v1"
    target.mkdir(parents=True, exist_ok=True)
    f = target / "data.txt"
    f.write_text("datarec", encoding="utf-8")

    # clear a subpath
    result = c.clear_cache(target="dataset", force=True)
    assert f not in result["removed"]  # directory removal, not file listing
    assert (root / "dataset").exists() is False

    # clearing non-existing path returns empty result
    empty = c.clear_cache(target="missing", force=True)
    assert empty["removed"] == []
