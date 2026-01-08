from __future__ import annotations

import os
import math
import pandas as pd
import numpy as np
from collections import Counter
from datarec.data.topological_characteristics import TOPOLOGICAL_CHARACTERISTICS
from typing import TYPE_CHECKING
import importlib
from typing import Optional

if TYPE_CHECKING:  # avoids circular import at runtime
    from datarec.data import DataRec

nx = None  # lazy-loaded
bipartite = None  # lazy-loaded


def _require_networkx():
    """
    Lazy-load networkx to keep the dependency optional until a graph is actually built.
    """
    global nx, bipartite
    if nx is None or bipartite is None:
        try:
            nx = importlib.import_module("networkx")
            bipartite = importlib.import_module("networkx.algorithms.bipartite")
        except ImportError as exc:
            raise ImportError(
                "networkx is required for graph operations. "
                "Install it with `pip install networkx`."
            ) from exc


class GraphRec:

    def __init__(self, dr: DataRec):
        _require_networkx()

        if dr.is_encoded(on='users'):
            dr.reset_encoding()

        if dr.is_encoded(on='items'):
            dr.reset_encoding()
        
        dr.build_encoding(on='users', offset=0)
        dr.build_encoding(on='items', offset=dr.n_users)
        dr.encode()

        self.graph = nx.from_pandas_edgelist(
            dr.data,
            source=dr.user_col,
            target=dr.item_col,
            create_using=nx.Graph())
    

        self.characteristics = CharacteristicAccessor(self)

    def __repr__(self) -> str:
        return self.graph.__repr__()
    
    def __str__(self):
        return self.graph.__str__()

    @property
    def num_edges(self):
        _require_networkx()
        return len(self.graph.edges)
    
    @property
    def num_nodes(self):
        _require_networkx()
        return len(self.graph.nodes)
    
    @property
    def user_nodes(self):
        _require_networkx()
        return bipartite.sets(self.graph)[0]
    
    @property
    def item_nodes(self):
        _require_networkx()
        return bipartite.sets(self.graph)[1]
    
    @property
    def n_user_nodes(self):
        return len(self.user_nodes)
    
    @property
    def n_item_nodes(self):
        return len(self.item_nodes)
    
    def set_bipartite_node_attributes(self):
        _require_networkx()
        user_nodes, item_nodes = self.user_nodes, self.item_nodes
        nx.set_node_attributes(self.graph, {u: 0 for u in user_nodes}, "bipartite")
        nx.set_node_attributes(self.graph, {i: 1 for i in item_nodes}, "bipartite")
    
    @property
    def user_graph(self):
        _require_networkx()
        import time
        start = time.time()
        ug = bipartite.projected_graph(self.graph, self.user_nodes)
        end = time.time()
        print(f'User graph projection took {end - start} seconds.')
        return ug
    
    @property
    def item_graph(self):
        _require_networkx()
        return bipartite.projected_graph(self.graph, self.item_nodes)
    
    def to_datarec(self) -> DataRec:
        """
        Converts the graph back to a DataRec object.

        Returns:
            DataRec: The converted DataRec object.
        """
        _require_networkx()
        from datarec.data import DataRec
        from datarec.io import RawData
        edges = nx.to_pandas_edgelist(self.graph, source='user_id', target='item_id')
        dr = DataRec(RawData(edges, user='user_id', item='item_id'))
        return dr
    
    # Topological charactertistics
    
    def characteristic(self, name: str, **kwargs):
        """
        Retrieves a calculated dataset characteristic by name.

        Args:
            name (str): The name of the characteristic to retrieve.
            **kwargs: Additional arguments to pass to the characteristic function.

        Returns:
            The value of the requested characteristic.
        """
        return getattr(self.characteristics, name)(**kwargs)  

    def average_degree(self, **kwargs):
        return self.characteristic("average_degree", **kwargs)
    
    def average_degree_users(self, **kwargs):
        return self.characteristic("average_degree_users", **kwargs)
    
    def average_degree_items(self, **kwargs):
        return self.characteristic("average_degree_items", **kwargs)

    def average_degree_log(self, **kwargs):
        return self.characteristic("average_degree_log", **kwargs)

    def average_degree_users_log(self, **kwargs):
        return self.characteristic("average_degree_users_log", **kwargs)

    def average_degree_items_log(self, **kwargs):
        return self.characteristic("average_degree_items_log", **kwargs)

    def average_clustering_coefficient_dot(self, **kwargs):
        return self.characteristic("average_clustering_coefficient_dot", **kwargs)

    def average_clustering_coefficient_min(self, **kwargs):
        return self.characteristic("average_clustering_coefficient_min", **kwargs)

    def average_clustering_coefficient_max(self, **kwargs):
        return self.characteristic("average_clustering_coefficient_max", **kwargs)

    def average_clustering_coefficient_dot_users(self, **kwargs):
        return self.characteristic("average_clustering_coefficient_dot_users", **kwargs)

    def average_clustering_coefficient_dot_items(self, **kwargs):
        return self.characteristic("average_clustering_coefficient_dot_items", **kwargs)

    def average_clustering_coefficient_min_users(self, **kwargs):
        return self.characteristic("average_clustering_coefficient_min_users", **kwargs)

    def average_clustering_coefficient_min_items(self, **kwargs):
        return self.characteristic("average_clustering_coefficient_min_items", **kwargs)

    def average_clustering_coefficient_max_users(self, **kwargs):
        return self.characteristic("average_clustering_coefficient_max_users", **kwargs)

    def average_clustering_coefficient_max_items(self, **kwargs):
        return self.characteristic("average_clustering_coefficient_max_items", **kwargs)

    def average_clustering_coefficient_dot_log(self, **kwargs):
        return self.characteristic("average_clustering_coefficient_dot_log", **kwargs)

    def average_clustering_coefficient_min_log(self, **kwargs):
        return self.characteristic("average_clustering_coefficient_min_log", **kwargs)

    def average_clustering_coefficient_max_log(self, **kwargs):
        return self.characteristic("average_clustering_coefficient_max_log", **kwargs)

    def average_clustering_coefficient_dot_users_log(self, **kwargs):
        return self.characteristic("average_clustering_coefficient_dot_users_log", **kwargs)

    def average_clustering_coefficient_dot_items_log(self, **kwargs):
        return self.characteristic("average_clustering_coefficient_dot_items_log", **kwargs)

    def average_clustering_coefficient_min_users_log(self, **kwargs):
        return self.characteristic("average_clustering_coefficient_min_users_log", **kwargs)

    def average_clustering_coefficient_min_items_log(self, **kwargs):
        return self.characteristic("average_clustering_coefficient_min_items_log", **kwargs)

    def average_clustering_coefficient_max_users_log(self, **kwargs):
        return self.characteristic("average_clustering_coefficient_max_users_log", **kwargs)

    def average_clustering_coefficient_max_items_log(self, **kwargs):
        return self.characteristic("average_clustering_coefficient_max_items_log", **kwargs)

    def degree_assortativity(self, **kwargs):
        return self.characteristic("degree_assortativity", **kwargs)

    def degree_assortativity_users(self, **kwargs):
        return self.characteristic("degree_assortativity_users", **kwargs)

    def degree_assortativity_items(self, **kwargs):
        return self.characteristic("degree_assortativity_items", **kwargs)

    def make_graph_connected(self) -> None:
        """
        Makes the dataset graph connected by retaining only the biggest connected portion.
        Updates the dataset accordingly by filtering out users and items not present in the connected graph.
        """
        _require_networkx()
        # if graph is not connected, retain only the biggest connected portion
        if not nx.is_connected(self.graph):
            print(f'The dataset graph is not connected. Building the connected subgraph.')
            self.graph = self.graph.subgraph(max(nx.connected_components(self.graph), key=len))
        print(f'The graph is connected.')
        user_nodes, item_nodes = bipartite.sets(self.graph)
        print(f'{self.__class__.__name__}: graph characteristics'
              f'\n nodes: {len(self.graph.nodes)}'
              f'\n edges: {len(self.graph.edges)}'
              f'\n user nodes: {len(user_nodes)}'
              f'\n item nodes: {len(item_nodes)}')



class CharacteristicAccessor:
    """
    Accessor for dataset characteristics.
    Allows dynamic retrieval of dataset characteristics as attributes.
    
    Args:
        datarec (DataRec): The DataRec object to access characteristics from.
    """
    def __init__(self, dr: GraphRec):
        self._datarec = dr

    def __getattr__(self, name):
        try:
            func = TOPOLOGICAL_CHARACTERISTICS[name]
        except KeyError:
            raise AttributeError(name) from None

        def bound(**kwargs):
            return func(self._datarec, **kwargs)
        
        bound.__doc__ = func.__doc__
        return bound
