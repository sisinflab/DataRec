import sys
import importlib
import pytest


def test_raises_clear_error_if_torch_missing(monkeypatch):
    """Import should fail cleanly when torch is absent."""
    monkeypatch.setitem(sys.modules, "torch", None)

    with pytest.raises(ImportError):
        import datarec.data.torch_dataset as td  # noqa: F401
        importlib.reload(td)
