# Processing Module Reference

This section provides a detailed API reference for all modules related to **preprocessing** and **filtering** datasets.
Processing steps operate on `DataRec` and return a new `DataRec` with the **pipeline updated**.

## On This Page

- [Processing Components](#processing-components)
- [Minimal usage](#minimal-usage)

## Minimal usage

```python
from datarec.processing import FilterOutDuplicatedInteractions, UserItemIterativeKCore

data = FilterOutDuplicatedInteractions().run(data)
data = UserItemIterativeKCore(cores=5).run(data)
```

## Processing Components

::: datarec.processing.binarizer
::: datarec.processing.cold
::: datarec.processing.kcore
::: datarec.processing.processor
::: datarec.processing.rating
::: datarec.processing.temporal
