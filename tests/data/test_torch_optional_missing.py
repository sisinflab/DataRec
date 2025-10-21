import sys
import importlib
import pytest

def test_raises_clear_error_if_torch_missing(monkeypatch):

    monkeypatch.setitem(sys.modules, "torch", None)

    with pytest.raises(ImportError, match="Torch is required"):
        import datarec.data.torch_dataset as td
        importlib.reload(td)
