import pandas as pd
import pytest

from datarec import DataRec
from datarec.io.rawdata import RawData
from datarec.io.readers.transactions.blocks import read_transactions_blocks
from datarec.io.writers.transactions.blocks import write_transactions_blocks


def _read_args(block_by, event_layout, **kwargs):
    return dict(
        block_by=block_by,
        event_layout=event_layout,
        user_col="user",
        item_col="item",
        **kwargs,
    )


def test_read_transactions_blocks_item_id(tmp_path):
    p = tmp_path / "blocks.txt"
    p.write_text(
        "1:\n"
        "10\n"
        "20\n"
        "2:\n"
        "30\n",
        encoding="utf-8",
    )

    rd = read_transactions_blocks(str(p), **_read_args("item", "id", sep=","))

    assert isinstance(rd, DataRec)
    assert rd.data[rd.user_col].tolist() == ["10", "20", "30"]
    assert rd.data[rd.item_col].tolist() == ["1", "1", "2"]
    assert rd.rating_col is None
    assert rd.timestamp_col is None


def test_read_transactions_blocks_item_id_rating(tmp_path):
    p = tmp_path / "blocks.txt"
    p.write_text(
        "1:\n"
        "10,4\n"
        "2:\n"
        "20,3\n",
        encoding="utf-8",
    )

    rd = read_transactions_blocks(
        str(p),
        **_read_args("item", "id,rating", rating_col="rating", sep=","),
    )

    assert isinstance(rd, DataRec)
    assert rd.data[rd.user_col].tolist() == ["10", "20"]
    assert rd.data[rd.item_col].tolist() == ["1", "2"]
    assert rd.data[rd.rating_col].tolist() == ["4", "3"]
    assert rd.timestamp_col is None


def test_read_transactions_blocks_item_id_rating_timestamp(tmp_path):
    p = tmp_path / "blocks.txt"
    p.write_text(
        "1:\n"
        "10,4,2005-01-01\n"
        "2:\n"
        "20,3,2005-01-02\n",
        encoding="utf-8",
    )

    rd = read_transactions_blocks(
        str(p),
        **_read_args(
            "item",
            "id,rating,timestamp",
            rating_col="rating",
            timestamp_col="timestamp",
            sep=",",
        ),
    )

    assert isinstance(rd, DataRec)
    assert rd.data[rd.user_col].tolist() == ["10", "20"]
    assert rd.data[rd.item_col].tolist() == ["1", "2"]
    assert rd.data[rd.rating_col].tolist() == ["4", "3"]
    assert rd.data[rd.timestamp_col].tolist() == ["2005-01-01", "2005-01-02"]


def test_read_transactions_blocks_user_id(tmp_path):
    p = tmp_path / "blocks.txt"
    p.write_text(
        "10:\n"
        "1\n"
        "2\n"
        "20:\n"
        "3\n",
        encoding="utf-8",
    )

    rd = read_transactions_blocks(str(p), **_read_args("user", "id", sep=","))

    assert isinstance(rd, DataRec)
    assert rd.data[rd.user_col].tolist() == ["10", "10", "20"]
    assert rd.data[rd.item_col].tolist() == ["1", "2", "3"]
    assert rd.rating_col is None
    assert rd.timestamp_col is None


def test_read_transactions_blocks_user_id_rating(tmp_path):
    p = tmp_path / "blocks.txt"
    p.write_text(
        "10:\n"
        "1,4\n"
        "20:\n"
        "2,3\n",
        encoding="utf-8",
    )

    rd = read_transactions_blocks(
        str(p),
        **_read_args("user", "id,rating", rating_col="rating", sep=","),
    )

    assert isinstance(rd, DataRec)
    assert rd.data[rd.user_col].tolist() == ["10", "20"]
    assert rd.data[rd.item_col].tolist() == ["1", "2"]
    assert rd.data[rd.rating_col].tolist() == ["4", "3"]
    assert rd.timestamp_col is None


def test_read_transactions_blocks_user_id_rating_timestamp(tmp_path):
    p = tmp_path / "blocks.txt"
    p.write_text(
        "10:\n"
        "1,4,2005-01-01\n"
        "20:\n"
        "2,3,2005-01-02\n",
        encoding="utf-8",
    )

    rd = read_transactions_blocks(
        str(p),
        **_read_args(
            "user",
            "id,rating,timestamp",
            rating_col="rating",
            timestamp_col="timestamp",
            sep=",",
        ),
    )

    assert isinstance(rd, DataRec)
    assert rd.data[rd.user_col].tolist() == ["10", "20"]
    assert rd.data[rd.item_col].tolist() == ["1", "2"]
    assert rd.data[rd.rating_col].tolist() == ["4", "3"]
    assert rd.data[rd.timestamp_col].tolist() == ["2005-01-01", "2005-01-02"]


def test_read_transactions_blocks_event_before_header(tmp_path):
    p = tmp_path / "blocks.txt"
    p.write_text("10\n1:\n", encoding="utf-8")

    with pytest.raises(ValueError):
        read_transactions_blocks(str(p), **_read_args("item", "id", sep=","))


def test_read_transactions_blocks_bad_field_count(tmp_path):
    p = tmp_path / "blocks.txt"
    p.write_text("1:\n10,4,2005-01-01,extra\n", encoding="utf-8")

    with pytest.raises(ValueError):
        read_transactions_blocks(
            str(p),
            **_read_args(
                "item",
                "id,rating,timestamp",
                rating_col="rating",
                timestamp_col="timestamp",
                sep=",",
            ),
        )


def test_read_transactions_blocks_requires_rating_col(tmp_path):
    p = tmp_path / "blocks.txt"
    p.write_text("1:\n10,4\n", encoding="utf-8")

    with pytest.raises(ValueError):
        read_transactions_blocks(str(p), **_read_args("item", "id,rating", sep=","))


def test_read_transactions_blocks_requires_timestamp_col(tmp_path):
    p = tmp_path / "blocks.txt"
    p.write_text("1:\n10,4,2005-01-01\n", encoding="utf-8")

    with pytest.raises(ValueError):
        read_transactions_blocks(
            str(p),
            **_read_args("item", "id,rating,timestamp", rating_col="rating", sep=","),
        )


def test_read_transactions_blocks_disallows_extra_columns(tmp_path):
    p = tmp_path / "blocks.txt"
    p.write_text("1:\n10\n", encoding="utf-8")

    with pytest.raises(ValueError):
        read_transactions_blocks(
            str(p),
            **_read_args("item", "id", rating_col="rating", sep=","),
        )


def test_read_transactions_blocks_disallows_timestamp_col(tmp_path):
    p = tmp_path / "blocks.txt"
    p.write_text("1:\n10,4\n", encoding="utf-8")

    with pytest.raises(ValueError):
        read_transactions_blocks(
            str(p),
            **_read_args(
                "item",
                "id,rating",
                rating_col="rating",
                timestamp_col="timestamp",
                sep=",",
            ),
        )


def test_read_transactions_blocks_requires_explicit_params(tmp_path):
    p = tmp_path / "blocks.txt"
    p.write_text("1:\n10\n", encoding="utf-8")

    with pytest.raises(TypeError):
        read_transactions_blocks(str(p))


def test_write_transactions_blocks_item_id(tmp_path):
    df = pd.DataFrame({"user": ["10", "20"], "item": ["1", "1"]})
    raw = RawData(df, user="user", item="item")

    out = tmp_path / "blocks.txt"
    write_transactions_blocks(
        raw,
        str(out),
        block_by="item",
        event_layout="id",
        include_rating=False,
        include_timestamp=False,
        sep=",",
    )

    assert out.read_text(encoding="utf-8") == (
        "1:\n"
        "10\n"
        "20\n"
    )


def test_write_transactions_blocks_item_id_rating(tmp_path):
    df = pd.DataFrame({"user": ["10", "20"], "item": ["1", "2"], "rating": ["4", "3"]})
    raw = RawData(df, user="user", item="item", rating="rating")

    out = tmp_path / "blocks.txt"
    write_transactions_blocks(
        raw,
        str(out),
        block_by="item",
        event_layout="id,rating",
        include_rating=True,
        include_timestamp=False,
        sep=",",
    )

    assert out.read_text(encoding="utf-8") == (
        "1:\n"
        "10,4\n"
        "2:\n"
        "20,3\n"
    )


def test_write_transactions_blocks_item_id_rating_timestamp(tmp_path):
    df = pd.DataFrame(
        {
            "user": ["10", "20"],
            "item": ["1", "2"],
            "rating": ["4", "3"],
            "timestamp": ["2005-01-01", "2005-01-02"],
        }
    )
    raw = RawData(df, user="user", item="item", rating="rating", timestamp="timestamp")

    out = tmp_path / "blocks.txt"
    write_transactions_blocks(
        raw,
        str(out),
        block_by="item",
        event_layout="id,rating,timestamp",
        include_rating=True,
        include_timestamp=True,
        sep=",",
    )

    assert out.read_text(encoding="utf-8") == (
        "1:\n"
        "10,4,2005-01-01\n"
        "2:\n"
        "20,3,2005-01-02\n"
    )


def test_write_transactions_blocks_user_id(tmp_path):
    df = pd.DataFrame({"user": ["10", "10"], "item": ["1", "2"]})
    raw = RawData(df, user="user", item="item")

    out = tmp_path / "blocks.txt"
    write_transactions_blocks(
        raw,
        str(out),
        block_by="user",
        event_layout="id",
        include_rating=False,
        include_timestamp=False,
        sep=",",
    )

    assert out.read_text(encoding="utf-8") == (
        "10:\n"
        "1\n"
        "2\n"
    )


def test_write_transactions_blocks_user_id_rating(tmp_path):
    df = pd.DataFrame({"user": ["10", "20"], "item": ["1", "2"], "rating": ["4", "3"]})
    raw = RawData(df, user="user", item="item", rating="rating")

    out = tmp_path / "blocks.txt"
    write_transactions_blocks(
        raw,
        str(out),
        block_by="user",
        event_layout="id,rating",
        include_rating=True,
        include_timestamp=False,
        sep=",",
    )

    assert out.read_text(encoding="utf-8") == (
        "10:\n"
        "1,4\n"
        "20:\n"
        "2,3\n"
    )


def test_write_transactions_blocks_user_id_rating_timestamp(tmp_path):
    df = pd.DataFrame(
        {
            "user": ["10", "20"],
            "item": ["1", "2"],
            "rating": ["4", "3"],
            "timestamp": ["2005-01-01", "2005-01-02"],
        }
    )
    raw = RawData(df, user="user", item="item", rating="rating", timestamp="timestamp")

    out = tmp_path / "blocks.txt"
    write_transactions_blocks(
        raw,
        str(out),
        block_by="user",
        event_layout="id,rating,timestamp",
        include_rating=True,
        include_timestamp=True,
        sep=",",
    )

    assert out.read_text(encoding="utf-8") == (
        "10:\n"
        "1,4,2005-01-01\n"
        "20:\n"
        "2,3,2005-01-02\n"
    )


def test_round_trip_transactions_blocks_item_id(tmp_path):
    content = "1:\n10\n20\n2:\n30\n"
    src = tmp_path / "blocks.txt"
    src.write_text(content, encoding="utf-8")

    rd = read_transactions_blocks(str(src), **_read_args("item", "id", sep=","))
    out = tmp_path / "blocks_out.txt"
    write_transactions_blocks(
        rd,
        str(out),
        block_by="item",
        event_layout="id",
        include_rating=False,
        include_timestamp=False,
        sep=",",
    )
    rd2 = read_transactions_blocks(str(out), **_read_args("item", "id", sep=","))

    assert isinstance(rd, DataRec)
    assert isinstance(rd2, DataRec)
    assert rd2.data.to_dict(orient="records") == rd.data.to_dict(orient="records")


def test_round_trip_transactions_blocks_item_id_rating(tmp_path):
    content = "1:\n10,4\n2:\n20,3\n"
    src = tmp_path / "blocks.txt"
    src.write_text(content, encoding="utf-8")

    rd = read_transactions_blocks(
        str(src),
        **_read_args("item", "id,rating", rating_col="rating", sep=","),
    )
    out = tmp_path / "blocks_out.txt"
    write_transactions_blocks(
        rd,
        str(out),
        block_by="item",
        event_layout="id,rating",
        include_rating=True,
        include_timestamp=False,
        sep=",",
    )
    rd2 = read_transactions_blocks(
        str(out),
        **_read_args("item", "id,rating", rating_col="rating", sep=","),
    )

    assert isinstance(rd, DataRec)
    assert isinstance(rd2, DataRec)
    assert rd2.data.to_dict(orient="records") == rd.data.to_dict(orient="records")


def test_round_trip_transactions_blocks_item_id_rating_timestamp(tmp_path):
    content = "1:\n10,4,2005-01-01\n2:\n20,3,2005-01-02\n"
    src = tmp_path / "blocks.txt"
    src.write_text(content, encoding="utf-8")

    rd = read_transactions_blocks(
        str(src),
        **_read_args(
            "item",
            "id,rating,timestamp",
            rating_col="rating",
            timestamp_col="timestamp",
            sep=",",
        ),
    )
    out = tmp_path / "blocks_out.txt"
    write_transactions_blocks(
        rd,
        str(out),
        block_by="item",
        event_layout="id,rating,timestamp",
        include_rating=True,
        include_timestamp=True,
        sep=",",
    )
    rd2 = read_transactions_blocks(
        str(out),
        **_read_args(
            "item",
            "id,rating,timestamp",
            rating_col="rating",
            timestamp_col="timestamp",
            sep=",",
        ),
    )

    assert isinstance(rd, DataRec)
    assert isinstance(rd2, DataRec)
    assert rd2.data.to_dict(orient="records") == rd.data.to_dict(orient="records")


def test_round_trip_transactions_blocks_user_id(tmp_path):
    content = "10:\n1\n2\n20:\n3\n"
    src = tmp_path / "blocks.txt"
    src.write_text(content, encoding="utf-8")

    rd = read_transactions_blocks(str(src), **_read_args("user", "id", sep=","))
    out = tmp_path / "blocks_out.txt"
    write_transactions_blocks(
        rd,
        str(out),
        block_by="user",
        event_layout="id",
        include_rating=False,
        include_timestamp=False,
        sep=",",
    )
    rd2 = read_transactions_blocks(str(out), **_read_args("user", "id", sep=","))

    assert isinstance(rd, DataRec)
    assert isinstance(rd2, DataRec)
    assert rd2.data.to_dict(orient="records") == rd.data.to_dict(orient="records")


def test_round_trip_transactions_blocks_user_id_rating(tmp_path):
    content = "10:\n1,4\n20:\n2,3\n"
    src = tmp_path / "blocks.txt"
    src.write_text(content, encoding="utf-8")

    rd = read_transactions_blocks(
        str(src),
        **_read_args("user", "id,rating", rating_col="rating", sep=","),
    )
    out = tmp_path / "blocks_out.txt"
    write_transactions_blocks(
        rd,
        str(out),
        block_by="user",
        event_layout="id,rating",
        include_rating=True,
        include_timestamp=False,
        sep=",",
    )
    rd2 = read_transactions_blocks(
        str(out),
        **_read_args("user", "id,rating", rating_col="rating", sep=","),
    )

    assert isinstance(rd, DataRec)
    assert isinstance(rd2, DataRec)
    assert rd2.data.to_dict(orient="records") == rd.data.to_dict(orient="records")


def test_round_trip_transactions_blocks_user_id_rating_timestamp(tmp_path):
    content = "10:\n1,4,2005-01-01\n20:\n2,3,2005-01-02\n"
    src = tmp_path / "blocks.txt"
    src.write_text(content, encoding="utf-8")

    rd = read_transactions_blocks(
        str(src),
        **_read_args(
            "user",
            "id,rating,timestamp",
            rating_col="rating",
            timestamp_col="timestamp",
            sep=",",
        ),
    )
    out = tmp_path / "blocks_out.txt"
    write_transactions_blocks(
        rd,
        str(out),
        block_by="user",
        event_layout="id,rating,timestamp",
        include_rating=True,
        include_timestamp=True,
        sep=",",
    )
    rd2 = read_transactions_blocks(
        str(out),
        **_read_args(
            "user",
            "id,rating,timestamp",
            rating_col="rating",
            timestamp_col="timestamp",
            sep=",",
        ),
    )

    assert isinstance(rd, DataRec)
    assert isinstance(rd2, DataRec)
    assert rd2.data.to_dict(orient="records") == rd.data.to_dict(orient="records")


def test_write_transactions_blocks_requires_explicit_params(tmp_path):
    df = pd.DataFrame({"user": ["10"], "item": ["1"]})
    raw = RawData(df, user="user", item="item")

    out = tmp_path / "blocks.txt"
    with pytest.raises(TypeError):
        write_transactions_blocks(raw, str(out))
