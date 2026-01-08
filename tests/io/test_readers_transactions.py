from pathlib import Path

from datarec.io.readers.transactions.tabular import read_transactions_tabular
from datarec.io.readers.transactions.json import read_transactions_json
from datarec.io.readers.transactions.jsonl import read_transactions_jsonl


def test_read_transactions_tabular_header_and_stream(tmp_path):
    p = tmp_path / "tx.tsv"
    p.write_text("user\titem\trating\ntom\tit1\t5\nbob\tit2\t3\n", encoding="utf-8")
    rd = read_transactions_tabular(
        str(p),
        sep="\t",
        user_col="user",
        item_col="item",
        rating_col="rating",
        header=0,
        stream=True,
        encode_ids=True,
        chunksize=1,
    )
    assert len(rd.data) == 2
    assert rd.rating_col == "rating"
    assert rd.user_encoder is not None
    assert rd.item_encoder is not None


def test_read_transactions_tabular_no_header(tmp_path):
    p = tmp_path / "tx_no_header.tsv"
    p.write_text("tom\tit1\t5\nbob\tit2\t3\n", encoding="utf-8")
    rd = read_transactions_tabular(
        str(p),
        sep="\t",
        user_col=0,
        item_col=1,
        rating_col=2,
        header=None,
    )
    assert len(rd.data) == 2
    assert set(rd.data[rd.user]) == {"tom", "bob"}


def test_read_transactions_json(tmp_path):
    p = tmp_path / "tx.json"
    p.write_text(
        '[{"user":"u1","item":"i1","rating":5},{"user":"u2","item":"i2","rating":4}]',
        encoding="utf-8",
    )
    rd = read_transactions_json(
        str(p),
        user_col="user",
        item_col="item",
        rating_col="rating",
        stream=False,
    )
    assert len(rd.data) == 2
    assert set(rd.data[rd.user]) == {"u1", "u2"}


def test_read_transactions_jsonl_stream(tmp_path):

    p = tmp_path / "tx.jsonl"
    p.write_text(
        '{"user":"u1","item":"i1","rating":5}\n{"user":"u1","item":"i2","rating":4}\n',
        encoding="utf-8",
    )
    rd = read_transactions_jsonl(
        str(p),
        user_col="user",
        item_col="item",
        rating_col="rating",
        stream=True,
        encode_ids=True,
        chunksize=1,
    )
    assert len(rd.data) == 2
    assert rd.user_encoder is not None
    assert rd.item_encoder is not None
