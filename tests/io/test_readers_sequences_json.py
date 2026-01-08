from pathlib import Path

from datarec.io.readers.sequences.json import read_sequences_json, read_sequences_json_array


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
    rd = read_sequences_json(
        str(p),
        user_col="user",
        item_col="item",
        rating_col="rating",
        timestamp_col="timestamp",
    )
    assert len(rd.data) == 3
    assert set(rd.data[rd.user]) == {"u1", "u2"}
    assert set(rd.data[rd.item]) == {"i1", "i2", "i3"}


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
    assert len(rd.data) == 3
    assert set(rd.data[rd.user]) == {"u1", "u2"}
    assert set(rd.data[rd.item]) == {1, 2, 3}
