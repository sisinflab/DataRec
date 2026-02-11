from pathlib import Path

from datarec.io.readers.sequences.tabular import (
    read_sequence_tabular_inline,
    read_sequence_tabular_wide,
    read_sequence_tabular_implicit,
)


def test_read_sequence_tabular_inline(tmp_path):
    """
    Inline reader should explode sequences correctly and support encoding.
    """
    p = tmp_path / "seq_inline.tsv"
    p.write_text(
        "u1,a b c\n"
        "u2,d e\n",
        encoding="utf-8",
    )
    rd = read_sequence_tabular_inline(
        str(p),
        user_col="user",
        sequence_col="sequence",
        col_sep=",",
        sequence_sep=" ",
        header=None,
        cols=["user", "sequence"],
        stream=False,
    )
    # Expect 5 rows exploded
    assert len(rd.data) == 5
    assert set(rd.data[rd._user_col]) == {"u1", "u2"}
    assert set(rd.data[rd._item_col]) == {"a", "b", "c", "d", "e"}

    rd_enc = read_sequence_tabular_inline(
        str(p),
        user_col="user",
        sequence_col="sequence",
        col_sep=",",
        sequence_sep=" ",
        header=None,
        cols=["user", "sequence"],
        stream=True,
        encode_ids=True,
        chunksize=1,
    )
    assert rd_enc.is_encoded(on="users") is True
    assert rd_enc.is_encoded(on="items") is True
    assert rd_enc.data[rd_enc._user_col].max() >= 1
    assert rd_enc.data[rd_enc._item_col].max() >= 2


def test_read_sequence_tabular_wide(tmp_path):
    """
    Wide reader should handle ragged rows.
    """
    
    p = tmp_path / "seq_wide.tsv"
    p.write_text(
        "u1\ti1\ti2\ni2\ti3\n",
        encoding="utf-8",
    )
    rd = read_sequence_tabular_wide(
        str(p),
        user_col="user",
        item_col="item",
        col_sep="\t"
    )
    assert len(rd.data) == 3
    assert set(rd.data[rd.user_col]) == {"i2", "u1"}  # header row included as data
    assert set(rd.data[rd.item_col]) >= {"i1", "i2", "i3"}


def test_read_sequence_tabular_implicit(tmp_path):
    """
    Implicit reader should treat each row as a sequence id.
    """
    p = tmp_path / "seq_impl.tsv"
    p.write_text(
        "3 10 20 30\n"
        "2 11 42\n",
        encoding="utf-8",
    )
    rd = read_sequence_tabular_implicit(
        str(p),
        user_col="seq_id",
        item_col="item",
        col_sep=" ",
        header=None,
        drop_length_col=True,
        encode_ids=True,
    )
    assert len(rd.data) == 5
    assert rd.is_encoded(on="users") is True
    assert rd.is_encoded(on="items") is True
