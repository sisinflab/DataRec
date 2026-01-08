# Data Module Reference

This section provides a detailed API reference for the `datarec.data` package, which
defines the **core dataset abstraction**, **dataset builders**, and supporting utilities.

## On This Page

- [Core Data Utilities](#core-data-utilities)
- [Dataset Builders](#dataset-builders)
- [DataRec and Data Wrappers](#datarec-and-data-wrappers)
- [Torch Dataset Wrappers](#torch-dataset-wrappers)

## Core Data Utilities

Utilities shared across the data layer (**encoders**, helpers, characteristics helpers).

::: datarec.data.utils

## Dataset Builders

Dataset builder used by the registry to **prepare** and **load** resources.

::: datarec.data.datarec_builder

## DataRec and Data Wrappers

Core dataset container and helpers.

::: datarec.data.dataset
::: datarec.data.source
::: datarec.data.resource

## Torch Dataset Wrappers

PyTorch-compatible dataset wrappers.

::: datarec.data.torch_dataset
