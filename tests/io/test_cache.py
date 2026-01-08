from pathlib import Path
import pytest
from datarec.io import cache as c


def test_cache_dir_respects_env_and_reuses(monkeypatch, tmp_path):
    custom = tmp_path / "custom_cache"
    monkeypatch.setenv("DATAREC_CACHE_DIR", str(custom))
    # reset after setting env so it reloads from env
    c.reset_cache_dir()
    path1 = c.cache_dir()
    # cache_dir should honor env override and create the folder
    assert path1 == custom.resolve()
    marker = path1 / "marker.txt"
    marker.write_text("datarec")
    # subsequent calls reuse same directory and preserve contents
    path2 = c.cache_dir()
    assert path2 == path1
    assert marker.read_text() == "datarec"
    c.reset_cache_dir()


def test_set_and_use_cache_dir(monkeypatch, tmp_path):
    c.reset_cache_dir()
    new_dir = tmp_path / "new_cache"
    result = c.set_cache_dir(new_dir)
    assert result == new_dir.resolve()
    assert result.exists()
    # context manager temporarily overrides and then restores
    with c.use_cache_dir(tmp_path / "ctx_cache") as ctx_dir:
        assert c.cache_dir() == ctx_dir
    assert c.cache_dir() == new_dir.resolve()
    c.reset_cache_dir()


def test_reload_cache_dir_from_env(monkeypatch, tmp_path):
    c.reset_cache_dir()
    monkeypatch.setenv("DATAREC_CACHE_DIR", str(tmp_path / "env_cache"))
    reloaded = c.reload_cache_dir_from_env()
    assert reloaded == (tmp_path / "env_cache").resolve()
    # removing env falls back to default (but still returns a Path)
    monkeypatch.delenv("DATAREC_CACHE_DIR", raising=False)
    monkeypatch.setattr(c, "user_cache_dir", lambda app_name, app_author: str(tmp_path / "default_cache"))
    fallback = c.reload_cache_dir_from_env()
    assert isinstance(fallback, Path)
    assert fallback.exists()
    c.reset_cache_dir()
