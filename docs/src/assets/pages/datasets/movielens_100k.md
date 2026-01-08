# Movielens

## Overview

**Dataset name:** Movielens  
**Latest version:** 1m  
**Available versions:** 100k, 1m, 20m  
**Source:** https://grouplens.org/datasets/movielens/

The MovieLens datasets are a collection of movie ratings data collected by the GroupLens Research project at the University of Minnesota.

---

## Citation

```bibtex
@article{DBLP:journals/tiis/HarperK16,
author       = {F. Maxwell Harper and
                Joseph A. Konstan},
title        = {The MovieLens Datasets: History and Context},
journal      = {{ACM} Trans. Interact. Intell. Syst.},
volume       = {5},
number       = {4},
pages        = {19:1--19:19},
year         = {2016}
}
```

---

## Version: 100k

### Data Sources

| Name | Source type | Archive | URL | Checksum |
|---|---|---|---|---|
| ml100k_zip | HttpSource | zip | https://files.grouplens.org/datasets/movielens/ml-100k.zip | md5:0e33842e24a9c977be4e0107933c0723 |

---

### Resources

#### ratings

- **Type:** interactions
- **Format:** `transactions_tabular`
- **Required:** yes
- **Source:** `ml100k_zip`
- **Filename:** `u.data`

**Schema**

```yaml
sep: "\t"
user_col: 0
item_col: 1
rating_col: 2
timestamp_col: 3
```

#### genre

- **Type:** content
- **Source:** `ml100k_zip`
- **Filename:** `u.genre`
- **About:** items

#### info

- **Type:** content
- **Source:** `ml100k_zip`
- **Filename:** `u.info`
- **About:** items

#### item

- **Type:** content
- **Source:** `ml100k_zip`
- **Filename:** `u.item`
- **About:** items

#### occupation

- **Type:** content
- **Source:** `ml100k_zip`
- **Filename:** `u.occupation`
- **About:** users

---

## Dataset Characteristics

Computed at: **2025-12-15**

| Metric | Value |
|---|---|
| n_users | 943 |
| n_items | 1682 |
| n_interactions | 100000 |
| space_size | 1.2594149435352908 |
| space_size_log | 0.10016884209961084 |
| shape | 0.56064209274673 |
| shape_log | -0.251314298724565 |
| density | 0.06304669364224531 |
| density_log | -1.2003376841992217 |
| gini_item | 0.628999631391201 |
| gini_user | 0.47190850477200424 |
| ratings_per_user | 106.04453870625663 |
| ratings_per_item | 59.45303210463734 |

---

## License & Usage

Please refer to the official dataset page for licensing and usage restrictions.
https://grouplens.org/datasets/movielens/
