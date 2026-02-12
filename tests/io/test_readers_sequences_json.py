from pathlib import Path
import json

import pytest

from datarec import DataRec
from datarec.io.readers.sequences.json import (
    read_sequences_json,
    read_sequences_json_array,
    read_sequences_json_items,
)


def test_read_sequences_json(tmp_path):
    p = tmp_path / "seq.json"
    p.write_text(
        '{\n'
        '  "u1": [\n'
        '    {"item":"i1","rating":5},\n'
        '    {"item":"i2"}\n'
        '  ],\n'
        '  "u2": [\n'
        '    {"item":"i3","timestamp":123}\n'
        '  ]\n'
        '}\n',
        encoding="utf-8",
    )
    dr = read_sequences_json(
        str(p),
        user_col="user",
        item_col="item",
        rating_col="rating",
        timestamp_col="timestamp",
    )
    assert isinstance(dr, DataRec)
    assert len(dr.data) == 3
    assert set(dr.data[dr.user_col]) == {"u1", "u2"}
    assert set(dr.data[dr.item_col]) == {"i1", "i2", "i3"}


def test_read_sequences_json_array(tmp_path):
    p = tmp_path / "seq_array.json"
    p.write_text(
        '[\n'
        '  {"user":"u1","sequence":[{"item": 1, "rating": 5},{"item": 2, "rating": 4}]},\n'
        '  {"user":"u2","sequence":[{"item": 3, "rating": 2}]}\n'
        ']',
        encoding="utf-8",
    )
    rd = read_sequences_json_array(
        str(p),
        user_col="user",
        item_col="item",
        sequence_key="sequence",
        rating_col="rating",
    )
    assert isinstance(rd, DataRec)
    assert len(rd.data) == 3
    assert set(rd.data[rd.user_col]) == {"u1", "u2"}
    assert set(rd.data[rd.item_col]) == {1, 2, 3}


def test_read_sequences_json_items(tmp_path):
    p = tmp_path / "seq_items.json"
    payload = {"0": [4755, 9066, 9765], "1": [2975]}
    p.write_text(json.dumps(payload), encoding="utf-8")

    rd = read_sequences_json_items(
        str(p),
        user_col="user",
        item_col="item",
    )
    assert isinstance(rd, DataRec)

    assert len(rd.data) == 4
    assert set(rd.data[rd.user_col]) == {"0", "1"}
    assert list(rd.data[rd.data[rd.user_col] == "0"][rd.item_col]) == [4755, 9066, 9765]
    assert list(rd.data[rd.data[rd.user_col] == "1"][rd.item_col]) == [2975]


def test_read_sequences_json_items_requires_object(tmp_path):
    p = tmp_path / "seq_items.json"
    p.write_text(json.dumps([1, 2, 3]), encoding="utf-8")

    with pytest.raises(ValueError):
        read_sequences_json_items(str(p))


def test_read_sequences_json_items_requires_list_per_user(tmp_path):
    p = tmp_path / "seq_items.json"
    p.write_text(json.dumps({"0": {"item": 1}}), encoding="utf-8")

    with pytest.raises(ValueError):
        read_sequences_json_items(str(p))


def test_read_sequences_json_items_requires_scalar_items(tmp_path):
    p = tmp_path / "seq_items.json"
    p.write_text(json.dumps({"0": [{"item": 1}]}), encoding="utf-8")

    with pytest.raises(ValueError):
        read_sequences_json_items(str(p))


def test_read_sequences_json_items_rejects_rating_or_timestamp(tmp_path):
    p = tmp_path / "seq_items.json"
    p.write_text(json.dumps({"0": [1, 2]}), encoding="utf-8")

    with pytest.raises(ValueError):
        read_sequences_json_items(str(p), rating_col="rating")

    with pytest.raises(ValueError):
        read_sequences_json_items(str(p), timestamp_col="timestamp")
