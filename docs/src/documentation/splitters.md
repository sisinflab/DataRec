# Splitters Module Reference

This section provides a detailed API reference for all modules related to splitting datasets into training, validation, and test sets.

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