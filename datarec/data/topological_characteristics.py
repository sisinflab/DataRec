from __future__ import annotations

import math
import numpy as np
import importlib
from typing import TYPE_CHECKING, Callable, Dict, Optional

if TYPE_CHECKING:  # avoids circular import at runtime
    from datarec.data.graph import GraphRec

TOPOLOGICAL_CHARACTERISTICS: Dict[str, Callable[..., float]] = {}
nx = None  # lazy-loaded
bipartite = None  # lazy-loaded


def _require_networkx():
    """
    Lazy-import networkx and its bipartite helpers to keep the dependency optional
    until a topological characteristic is actually used.
    """
    global nx, bipartite
    if nx is None or bipartite is None:
        try:
            nx = importlib.import_module("networkx")
            bipartite = importlib.import_module("networkx.algorithms.bipartite")
        except ImportError as exc:
            raise ImportError(
                "networkx is required for topological characteristics. "
                "Install it with `pip install networkx`."
            ) from exc


def topological_characteristic(func=None, *, name=None):
    if func is None:
        return lambda f: topological_characteristic(f, name=name)

    key = name or func.__name__
    if key in TOPOLOGICAL_CHARACTERISTICS:
        raise ValueError(f"{key} already registered")
    TOPOLOGICAL_CHARACTERISTICS[key] = func
    return func

@topological_characteristic
def average_degree(gr: GraphRec):
    _require_networkx()
    return (2 * gr.num_edges) / (gr.n_user_nodes + gr.n_item_nodes)

@topological_characteristic
def average_degree_log(gr: GraphRec):
    _require_networkx()
    return math.log10(average_degree(gr))


@topological_characteristic
def average_degree_users(gr: GraphRec):
    _require_networkx()
    return gr.num_edges / gr.n_user_nodes


@topological_characteristic
def average_degree_users_log(gr: GraphRec):
    _require_networkx()
    return math.log10(gr.average_degree_users())


@topological_characteristic
def average_degree_items(gr: GraphRec):
    _require_networkx()
    return gr.num_edges / gr.n_item_nodes


@topological_characteristic
def average_degree_items_log(gr: GraphRec):
    _require_networkx()
    return math.log10(gr.average_degree_items())


@topological_characteristic
def average_clustering_coefficient_dot(gr: GraphRec):
    _require_networkx()
    return bipartite.average_clustering(gr.graph, mode='dot')

@topological_characteristic
def average_clustering_coefficient_dot_log(gr: GraphRec):
    _require_networkx()
    return math.log10(gr.average_clustering_coefficient_dot())

@topological_characteristic
def average_clustering_coefficient_min(gr: GraphRec):
    _require_networkx()
    return bipartite.average_clustering(gr.graph, mode='min')

@topological_characteristic
def average_clustering_coefficient_min_log(gr: GraphRec):
    _require_networkx()
    return math.log10(gr.average_clustering_coefficient_min())

@topological_characteristic
def average_clustering_coefficient_max(gr: GraphRec):
    _require_networkx()
    return bipartite.average_clustering(gr.graph, mode='max')

@topological_characteristic
def average_clustering_coefficient_max_log(gr: GraphRec):
    _require_networkx()
    return math.log10(gr.average_clustering_coefficient_max())

@topological_characteristic
def average_clustering_coefficient_dot_users(gr: GraphRec):
    _require_networkx()
    return bipartite.average_clustering(gr.graph, mode='dot', nodes=gr.user_nodes)

@topological_characteristic
def average_clustering_coefficient_dot_users_log(gr: GraphRec):
    _require_networkx()
    return math.log10(gr.average_clustering_coefficient_dot_users())

@topological_characteristic
def average_clustering_coefficient_dot_items(gr: GraphRec):
    _require_networkx()
    return bipartite.average_clustering(gr.graph, mode='dot', nodes=gr.item_nodes)

@topological_characteristic
def average_clustering_coefficient_dot_items_log(gr: GraphRec):
    _require_networkx()
    return math.log10(gr.average_clustering_coefficient_dot_items())

@topological_characteristic
def average_clustering_coefficient_min_users(gr: GraphRec):
    _require_networkx()
    return bipartite.average_clustering(gr.graph, mode='min', nodes=gr.user_nodes)

@topological_characteristic
def average_clustering_coefficient_min_users_log(gr: GraphRec):
    _require_networkx()
    return math.log10(gr.average_clustering_coefficient_min_users())

@topological_characteristic
def average_clustering_coefficient_min_items(gr: GraphRec):
    _require_networkx()
    return bipartite.average_clustering(gr.graph, mode='min', nodes=gr.item_nodes)

@topological_characteristic
def average_clustering_coefficient_min_items_log(gr: GraphRec):
    _require_networkx()
    return math.log10(gr.average_clustering_coefficient_min_items())

@topological_characteristic
def average_clustering_coefficient_max_users(gr: GraphRec):
    _require_networkx()
    return bipartite.average_clustering(gr.graph, mode='max', nodes=gr.user_nodes)

@topological_characteristic
def average_clustering_coefficient_max_users_log(gr: GraphRec):
    _require_networkx()
    return math.log10(gr.average_clustering_coefficient_max_users())

@topological_characteristic
def average_clustering_coefficient_max_items(gr: GraphRec):
    _require_networkx()
    return bipartite.average_clustering(gr.graph, mode='max', nodes=gr.item_nodes)


@topological_characteristic
def average_clustering_coefficient_max_items_log(gr: GraphRec):
    _require_networkx()
    return math.log10(gr.average_clustering_coefficient_max_items())

@topological_characteristic
def degree_assortativity_users(gr: GraphRec):
    _require_networkx()
    bipartite.projected_graph(gr.graph, gr.user_nodes)
    return nx.degree_pearson_correlation_coefficient(gr.user_graph, nodes=gr.user_nodes)

@topological_characteristic
def degree_assortativity_items(gr: GraphRec):
    _require_networkx()
    bipartite.projected_graph(gr.graph, gr.item_nodes)
    return nx.degree_pearson_correlation_coefficient(gr.item_graph, nodes=gr.item_nodes)
