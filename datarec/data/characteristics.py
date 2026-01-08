from __future__ import annotations

import math
import numpy as np
from typing import TYPE_CHECKING, Callable, Dict

if TYPE_CHECKING:  # avoids circular import at runtime
    from datarec.data import DataRec

CHARACTERISTICS: Dict[str, Callable[..., float]] = {}


def characteristic(func=None, *, name=None):
    if func is None:
        return lambda f: characteristic(f, name=name)

    key = name or func.__name__
    if key in CHARACTERISTICS:
        raise ValueError(f"{key} already registered")
    CHARACTERISTICS[key] = func
    return func

@characteristic
def n_users(dr: DataRec, scale_factor: int = 1000):
    """
    Calculates the scaled square root of the user-item interaction space.
    """
    return int(dr.data[dr.user_col].nunique())

@characteristic
def n_items(dr: DataRec, scale_factor: int = 1000):
    """
    Calculates the scaled square root of the user-item interaction space.
    """
    return int(dr.data[dr.item_col].nunique())

@characteristic
def n_interactions(dr: DataRec, scale_factor: int = 1000):
    """
    Calculates the scaled square root of the user-item interaction space.
    """
    return int(len(dr.data))


@characteristic
def space_size(dr: DataRec, scale_factor: int = 1000):
    """
    Calculates the scaled square root of the user-item interaction space.
    """
    return math.sqrt(dr.n_users * dr.n_items) / scale_factor


@characteristic
def space_size_log(dr: DataRec):
    """
    Calculates the log10 of the space_size metric.
    """
    return math.log10(space_size(dr))


@characteristic
def shape(dr: DataRec):
    """
    Calculates the shape of the interaction matrix (n_users / n_items).
    """
    return dr.n_users / dr.n_items


@characteristic
def shape_log(dr: DataRec):
    """
    Calculates the log10 of the shape metric.
    """
    return math.log10(shape(dr))


@characteristic
def density(dr: DataRec):
    """
    Calculates the density of the user-item interaction matrix.
    """
    return dr.transactions / (dr.n_users * dr.n_items)


@characteristic
def density_log(dr: DataRec):
    """
    Calculates the log10 of the density metric.
    """
    return math.log10(density(dr))


def gini(x):
    """
    Calculates the Gini coefficient for a numpy array.

    Args:
        x (np.ndarray): An array of non-negative values.

    Returns:
        (float): The Gini coefficient, a measure of inequality.
    """
    x = np.sort(x)  # O(n log n)
    n = len(x)
    cum_index = np.arange(1, n + 1)
    return (np.sum((2 * cum_index - n - 1) * x)) / (n * np.sum(x))


@characteristic
def gini_item(dr: DataRec):
    """
    Calculates the Gini coefficient for item popularity.
    """
    return gini(np.array(list(dr.sorted_items.values())))


@characteristic
def gini_user(dr: DataRec):
    """
    Calculates the Gini coefficient for user activity.
    """
    return gini(np.array(list(dr.sorted_users.values())))


@characteristic
def ratings_per_user(dr: DataRec):
    """
    Calculates the average number of ratings per user.
    """
    return dr.transactions / dr.n_users

@characteristic
def ratings_per_item(dr: DataRec):
    """
    Calculates the average number of ratings per item.
    """
    return dr.transactions / dr.n_items

