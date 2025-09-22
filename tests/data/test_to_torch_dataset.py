import pytest
from datarec.datasets import MovieLens

@pytest.mark.parametrize("task", ["pointwise", "pairwise", "ranking"])
def test_to_torch_dataset_prepared(task):
    """
    Test that to_torch_dataset returns a correct dataset instance
    for all supported tasks when autoprepare is enabled.
    """
    dr = MovieLens(version="1m")
    dataset = dr.to_torch_dataset(task=task, autoprepare=True)
    assert hasattr(dataset, "__getitem__")
    assert hasattr(dataset, "__len__")


def test_to_torch_dataset_invalid_task():
    """
    Test that to_torch_dataset raises ValueError for unknown tasks.
    """
    dr = MovieLens(version="1m")
    with pytest.raises(ValueError, match="Unknown task"):
        dr.to_torch_dataset(task="invalid_task")


def test_to_torch_dataset_no_torch(monkeypatch):
    """
    Test that to_torch_dataset raises ImportError when torch is not available.
    """
    import sys
    monkeypatch.setitem(sys.modules, "torch", None)
    dr = MovieLens(version="1m")
    with pytest.raises(ImportError, match="PyTorch is required"):
        dr.to_torch_dataset()
