# DataRec Data Formats

This document describes the dataset formats supported by DataRec, with a short
spec for each structure and the matching I/O helpers. The Read/Write entries
refer to the DataRec functions that load a file into RawData (Read) or export
RawData back to that format (Write).

## Index

- [Field conventions](#field-conventions)
- [Sequences](#sequences)
    - [Tabular (inline)](#tabular-inline)
    - [Tabular (wide)](#tabular-wide)
    - [Tabular (implicit)](#tabular-implicit)
    - [JSON (mapping)](#json-mapping)
    - [JSON (mapping, item-only)](#json-mapping-item-only)
    - [JSON (array)](#json-array)
- [Transactions](#transactions)
    - [Tabular](#tabular)
    - [JSON](#json)
    - [JSONL](#jsonl)
    - [Blocks (text)](#blocks-text)
- [Extending this catalog](#extending-this-catalog)


## Field conventions

Common fields across datasets:

- `user`: user identifier (string or integer)
- `item`: item identifier (string or integer)
- `rating`: preference value (integer/float)
- `timestamp`: temporal signal (string or integer)

## Sequences

Sequence datasets store per-user ordered lists.

### Tabular (inline)

- One row per user
- `item` contains a delimiter-separated sequence (semicolon)
- Optional `timestamp` column for aligned sequences
- Read: [read_sequence_tabular_inline](../../documentation/io.md#datarec.io.readers.sequences.tabular.read_sequence_tabular_inline)
- Write: [write_sequence_tabular_inline](../../documentation/io.md#datarec.io.writers.sequences.tabular.write_sequence_tabular_inline)

Example (`interactions`):

```tsv
user	item
0	1;2;3
1	1;2;4
```

Example (`timestamp`):

```tsv
user	item	timestamp
0	1;2;3	000
1	1;2;4	010
```

### Tabular (wide)

- One row per user
- Each item is a separate column
- Read: [read_sequence_tabular_wide](../../documentation/io.md#datarec.io.readers.sequences.tabular.read_sequence_tabular_wide)
- Write: [write_sequence_tabular_wide](../../documentation/io.md#datarec.io.writers.sequences.tabular.write_sequence_tabular_wide)

Example:

```tsv
user	item
0	1	2	3
1	1	2	4
```

### Tabular (implicit)

- First value is `user`
- Remaining columns are items
- Optional headerless variant for tabular data
- Read: [read_sequence_tabular_implicit](../../documentation/io.md#datarec.io.readers.sequences.tabular.read_sequence_tabular_implicit)
- Write: [write_sequence_tabular_implicit](../../documentation/io.md#datarec.io.writers.sequences.tabular.write_sequence_tabular_implicit)

Example:

```tsv
user	item
5	1	2	3	6	7
3	1	2	4
```

### JSON (mapping)

- Top-level object keyed by `user`
- Value is an ordered list of events
- Read: [read_sequences_json](../../documentation/io.md#datarec.io.readers.sequences.json.read_sequences_json)
- Write: [write_sequences_json](../../documentation/io.md#datarec.io.writers.sequences.json.write_sequences_json)

Example (`interactions`):

```json
{
  "0": [
    { "item": 1 },
    { "item": 2 }
  ]
}
```

Example (`ratings`):

```json
{
  "0": [
    { "item": 1, "rating": 1 },
    { "item": 2, "rating": 1 }
  ]
}
```

Example (`timestamp`):

```json
{
  "0": [
    { "item": 1, "rating": 1, "timestamp": "001" },
    { "item": 2, "rating": 1, "timestamp": "022" }
  ]
}
```

### JSON (mapping, item-only)

- Top-level object keyed by `user`
- Value is an ordered list of item ids (scalars only)
- Read: [read_sequences_json_items](../../documentation/io.md#datarec.io.readers.sequences.json.read_sequences_json_items)
- Write: [write_sequences_json_items](../../documentation/io.md#datarec.io.writers.sequences.json.write_sequences_json_items)

Example (`interactions`):

```json
{
  "0": [1, 2, 3],
  "1": [4]
}
```

### JSON (array)

- Top-level array
- Each entry contains `user` and `sequence`
- Read: [read_sequences_json_array](../../documentation/io.md#datarec.io.readers.sequences.json.read_sequences_json_array)
- Write: [write_sequences_json_array](../../documentation/io.md#datarec.io.writers.sequences.json.write_sequences_json_array)

Example (`interactions`):

```json
[
  {
    "user": "0",
    "sequence": [
      { "item": 1 },
      { "item": 2 }
    ]
  }
]
```

Example (`timestamp`):

```json
[
  {
    "user": "0",
    "sequence": [
      { "item": 1, "rating": 1, "timestamp": "001" },
      { "item": 2, "rating": 1, "timestamp": "022" }
    ]
  }
]
```

## Transactions

Transaction datasets store one event per row/object.

### Tabular

- One row per event
- Optional headerless variant for tabular data
- Read: [read_transactions_tabular](../../documentation/io.md#datarec.io.readers.transactions.tabular.read_transactions_tabular)
- Write: [write_transactions_tabular](../../documentation/io.md#datarec.io.writers.transactions.tabular.write_transactions_tabular)

Example (`ratings`):

```tsv
user	item	ratings
0	1	1
0	2	1
```

Example (`timestamp`):

```tsv
user	item	ratings	timestamp
0	1	1	001
0	2	1	022
```

### JSON

- Top-level array
- One object per event
- Read: [read_transactions_json](../../documentation/io.md#datarec.io.readers.transactions.json.read_transactions_json)
- Write: [write_transactions_json](../../documentation/io.md#datarec.io.writers.transactions.json.write_transactions_json)

Example (`ratings`):

```json
[
  { "user": 0, "item": 1, "rating": 1 },
  { "user": 0, "item": 2, "rating": 1 }
]
```

### JSONL

- One JSON object per line
- Read: [read_transactions_jsonl](../../documentation/io.md#datarec.io.readers.transactions.jsonl.read_transactions_jsonl)
- Write: [write_transactions_jsonl](../../documentation/io.md#datarec.io.writers.transactions.jsonl.write_transactions_jsonl)

Example (`interactions`):

```json
{"user": 0, "item": 1}
{"user": 0, "item": 2}
```

Example (`timestamp`):

```json
{"user": 0, "item": 1, "rating": 1, "timestamp": "001"}
{"user": 0, "item": 2, "rating": 1, "timestamp": "022"}
```

### Blocks (text)

- Block format with an explicit block id header
- Modes:
  - Item-wise blocks: `<ITEM_ID>:` then events
  - User-wise blocks: `<USER_ID>:` then events
- Event layouts:
  - `id`
  - `id,rating`
  - `id,rating,timestamp`
- Date is kept as string; reader is streaming
- Read: [read_transactions_blocks](../../documentation/io.md#datarec.io.readers.transactions.blocks.read_transactions_blocks)
- Write: [write_transactions_blocks](../../documentation/io.md#datarec.io.writers.transactions.blocks.write_transactions_blocks)

Example (item-wise, id):

```text
1:
10
20
```

Example (item-wise, id,rating):

```text
1:
10,4
20,3
```

Example (item-wise, id,rating,timestamp):

```text
1:
10,4,2005-01-01
20,3,2005-01-02
```

Example (user-wise, id):

```text
10:
1
2
```

Example (user-wise, id,rating):

```text
10:
1,4
2,3
```

Example (user-wise, id,rating,timestamp):

```text
10:
1,4,2005-01-01
2,3,2005-01-02
```

## Extending this catalog

To add a new dataset format:

1. Define the new format structure (fields and serialization).
2. Provide a minimal example that exercises the loader.
3. Add a new subsection under the appropriate data type.
