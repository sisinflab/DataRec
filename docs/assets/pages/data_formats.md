# Dataset Formats for Recommender Systems

Recommender-system datasets can be represented in different ways depending on the underlying **data model** and the **serialization format**.  
This page describes the common formats supported by DataRec and provides examples for each.

---

# 1. Data Models

## A. Transactional Interaction Data
Each row (or JSON object) represents **one interaction**:

```
(user, item, [rating], [timestamp], …)
```

Used in rating prediction, implicit feedback, and general user–item event logs.

## B. Sequential Interaction Data
Each row (or JSON object) represents **a sequence** of interactions for a user or session:

```
user → [item1, item2, item3, ...]
```

Used in sequential and session-based recommendation (e.g., SASRec, GRU4Rec).

---

# 2. Formats for Transactional Data

## 2.1 transactions/tabular

Each record corresponds to a single interaction.

```text
user    item    rating  timestamp
0       1       1       001
0       2       1       022
0       3       5       032
1       1       4       011
2       4       3       000
```

---

## 2.2 transactions/json

JSON array where each object is an interaction.

```json
[
  { "user": 0, "item": 1, "rating": 1, "timestamp": "001" },
  { "user": 0, "item": 2, "rating": 1, "timestamp": "022" },
  { "user": 1, "item": 1, "rating": 4, "timestamp": "011" }
]
```

---

## 2.3 transactions/jsonl

One JSON object per line, suitable for streaming and large datasets.

```json
{"user": 0, "item": 1, "rating": 1, "timestamp": "001"}
{"user": 0, "item": 2, "rating": 1, "timestamp": "022"}
{"user": 1, "item": 1, "rating": 4, "timestamp": "011"}
```

---

# 3. Formats for Sequential Data

## 3.1 sequences/tabular-inline

The sequence is stored in a **single column**, encoded as a string using a separator.

```text
user    sequence
0       1;2;3
1       1;2;4
2       4;5;6
3       2;4
```

---

## 3.2 sequences/tabular-wide

The sequence is distributed across multiple columns, with an **explicit user identifier**.

```text
user    item_1  item_2  item_3
0       1       2       3
1       1       2       4
2       4       5       6
```

Supports variable-length rows (ragged sequences).

---

## 3.3 sequences/tabular-implicit

Each row represents a sequence, but **no explicit user or session identifier is present**.  
The identity of the sequence is implicit and derived from the row position.

The first value often represents the declared sequence length and is typically ignored
during parsing.

```text
3  10  20  30
2  11  42
```

Interpretation:

- each row = one independent sequence instance
- a synthetic identifier (e.g., `sequence_id`) is generated internally
- sequences are treated as **pseudo-users** to maintain compatibility with
  user–item pipelines

Resulting transactional view:

```text
sequence_id  item
0            10
0            20
0            30
1            11
1            42
```

This format is common in sequential recommendation benchmarks where the notion of
"user" is not explicitly modeled.

---

## 3.4 sequences/json

Sequential data serialized using nested JSON structures.

### User-indexed representation

```json
{
  "0": [
    { "item": 1, "rating": 1, "timestamp": "001" },
    { "item": 2, "rating": 1, "timestamp": "022" }
  ],
  "1": [
    { "item": 1, "rating": 4, "timestamp": "011" }
  ]
}
```

### Array-based representation

```json
[
  {
    "user": 0,
    "sequence": [
      { "item": 1, "rating": 1, "timestamp": "001" },
      { "item": 2, "rating": 1, "timestamp": "022" }
    ]
  }
]
```

---

# 4. Summary Table

| Category                         | Description                                      | Example Type |
|----------------------------------|--------------------------------------------------|--------------|
| transactions/tabular             | One row = one interaction                        | CSV/TSV      |
| transactions/json                | JSON array of interaction objects                | JSON         |
| transactions/jsonl               | One JSON object per line                         | JSONL        |
| sequences/tabular-inline         | Sequence encoded in a single string column       | CSV/TSV      |
| sequences/tabular-wide           | Sequence spread across columns (explicit user)   | CSV/TSV      |
| sequences/tabular-implicit       | One sequence per row, implicit identifier        | CSV/TSV      |
| sequences/json                   | Sequence stored as nested lists/objects          | JSON         |

---

# 5. Choosing a Format

- Use **transactions** if order does not matter or for matrix/graph-based models.
- Use **sequences** for sequential or session-aware models.
- Prefer **tabular formats** for simplicity and speed.
- Use **JSON formats** when interactions include nested or variable-length metadata.
- Use **tabular-implicit** formats when sequences are independent instances
  without explicit user identifiers.

---

# 6. Automatic Detection in DataRec

DataRec can automatically recognize:

- transactional vs sequential data  
- tabular vs JSON formats  
- inline, wide, and implicit sequence structures  

allowing seamless loading into the unified `RawData` representation.