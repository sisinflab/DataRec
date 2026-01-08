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

## Version: 1m

### Data Sources

| Name | Source type | Archive | URL | Checksum |
|---|---|---|---|---|
| ml1m_zip | HttpSource | zip | https://files.grouplens.org/datasets/movielens/ml-1m.zip | md5:c4d9eecfca2ab87c1945afe126590906 |

---

### Resources

#### ratings

- **Type:** interactions
- **Format:** `transactions_tabular`
- **Required:** yes
- **Source:** `ml1m_zip`
- **Filename:** `ratings.dat`

**Schema**

```yaml
sep: '::'
user_col: 0
item_col: 1
rating_col: 2
timestamp_col: 3
engine: python
```

#### movies

- **Type:** content
- **Source:** `ml1m_zip`
- **Filename:** `movies.dat`
- **About:** items

#### users

- **Type:** content
- **Source:** `ml1m_zip`
- **Filename:** `users.dat`
- **About:** users

---

## Dataset Characteristics

Computed at: **2025-12-15**

| Metric | Value |
|---|---|
| n_users | 6040 |
| n_items | 3706 |
| n_interactions | 1000209 |
| space_size | 4.731198579641315 |
| space_size_log | 0.6749711768020052 |
| shape | 1.6297895304910954 |
| shape_log | 0.21213152363825302 |
| density | 0.044683625622312845 |
| density_log | -1.34985159554118 |
| gini_item | 0.6335616301416965 |
| gini_user | 0.5286242435264804 |
| ratings_per_user | 165.5975165562914 |
| ratings_per_item | 269.88909875876953 |

---

## License & Usage

Please refer to the official dataset page for licensing and usage restrictions.
https://grouplens.org/datasets/movielens/
