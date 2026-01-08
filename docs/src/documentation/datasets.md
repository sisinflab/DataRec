# Datasets Reference

This section provides a detailed API reference for all modules related to built‑in datasets in the `datarec` library.
Dataset entry points live in `datarec.datasets` and connect to registry metadata and versions.

## On This Page

- [Dataset Entry Points](#dataset-entry-points)
- [Registry Utilities](#registry-utilities)
- [Minimal usage](#minimal-usage)

## Minimal usage

```python
from datarec.datasets import Movielens

data = Movielens(version="1m").prepare_and_load()
```

## Dataset Entry Points

::: datarec.datasets

## Registry Utilities

::: datarec.registry.utils
