# Splitters Module Reference

This section provides a detailed API reference for all modules related to **splitting** datasets into training, validation, and test sets.
Use **uniform** splitters to sample globally, and **user‑stratified** splitters to split each user’s history independently.
Temporal splitters preserve time ordering when timestamps are available.

## On This Page

- [Core Splitting Utilities](#core-splitting-utilities)
- [Uniform Splitting Strategies](#uniform-splitting-strategies)
- [User-Stratified Splitting Strategies](#user-stratified-splitting-strategies)

Minimal usage:

```python
from datarec.splitters import RandomHoldOut

splitter = RandomHoldOut(test_ratio=0.2, val_ratio=0.1, seed=42)
splits = splitter.run(datarec)
train, val, test = splits["train"], splits["val"], splits["test"]
```

## Core Splitting Utilities

These modules define the base class and common utilities used by all splitters.

::: datarec.splitters.splitter
::: datarec.splitters.utils

## Uniform Splitting Strategies

These splitters operate on the entire dataset globally.

::: datarec.splitters.uniform.hold_out
::: datarec.splitters.uniform.temporal.hold_out
::: datarec.splitters.uniform.temporal.threshold

## User-Stratified Splitting Strategies

These splitters operate on a per-user basis, ensuring that each user's interaction history is partitioned across the splits.

::: datarec.splitters.user_stratified.hold_out
::: datarec.splitters.user_stratified.leave_out
::: datarec.splitters.user_stratified.temporal.leave_out
