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

## Version: 20m

### Data Sources

| Name | Source type | Archive | URL | Checksum |
|---|---|---|---|---|
| ml20m_zip | HttpSource | zip | https://files.grouplens.org/datasets/movielens/ml-20m.zip | md5:cd245b17a1ae2cc31bb14903e1204af3 |

---

### Resources

#### ratings

- **Type:** interactions
- **Format:** `transactions_tabular`
- **Required:** yes
- **Source:** `ml20m_zip`
- **Filename:** `ratings.csv`

**Schema**

```yaml
sep: ','
user_col: userId
item_col: movieId
rating_col: rating
timestamp_col: timestamp
header: 0
```

#### genome_scores

- **Type:** content
- **Source:** `ml20m_zip`
- **Filename:** `genome_scores.csv`
- **About:** items

#### genome_tags

- **Type:** content
- **Source:** `ml20m_zip`
- **Filename:** `genome_tags.csv`
- **About:** items

#### links

- **Type:** content
- **Source:** `ml20m_zip`
- **Filename:** `links.csv`
- **About:** items

#### movies

- **Type:** content
- **Source:** `ml20m_zip`
- **Filename:** `movies.csv`
- **About:** users

#### tags

- **Type:** content
- **Source:** `ml20m_zip`
- **Filename:** `tags.csv`
- **About:** users

---

## Dataset Characteristics

Computed at: **2025-12-15**

| Metric | Value |
|---|---|
| n_users | 138493 |
| n_items | 26744 |
| n_interactions | 20000263 |
| space_size | 60.8593196807194 |
| space_size_log | 1.784327093264329 |
| shape | 5.178469937182172 |
| shape_log | 0.7142014593596334 |
| density | 0.0053998478135544505 |
| density_log | -2.267618479929789 |
| gini_item | 0.902942497565131 |
| gini_user | 0.5807014936671218 |
| ratings_per_user | 144.4135299257002 |
| ratings_per_item | 747.8411232425965 |

---

## License & Usage

Please refer to the official dataset page for licensing and usage restrictions.
https://grouplens.org/datasets/movielens/
