import pytest
import networkx as nx

from datarec.data.dataset import DataRec, DATAREC_USER_COL, DATAREC_ITEM_COL
from datarec.data.graph import GraphRec
from datarec.io.rawdata import RawData


@pytest.fixture
def toy_graphrec():
    # Simple bipartite graph: u1-u2, items i1-i2
    import pandas as pd
    df = pd.DataFrame(
        {
            DATAREC_USER_COL: ["u1", "u1", "u2"],
            DATAREC_ITEM_COL: ["i1", "i2", "i1"],
        }
    )
    rd = RawData(df, user=DATAREC_USER_COL, item=DATAREC_ITEM_COL)
    dr = DataRec(rd)
    return GraphRec(dr)


@pytest.mark.skipif(nx is None, reason="networkx not installed")
def test_topological_characteristics(toy_graphrec: GraphRec):
    gr = toy_graphrec
    # Basic properties
    assert gr.num_edges == 3
    assert gr.n_user_nodes == 2
    assert gr.n_item_nodes == 2
    # Some characteristics should be computable without exceptions
    assert gr.average_degree() > 0
    assert gr.average_degree_users() > 0
    assert gr.average_degree_items() > 0
    assert gr.characteristics.average_clustering_coefficient_dot() >= 0
    assert gr.characteristics.average_clustering_coefficient_min() >= 0
