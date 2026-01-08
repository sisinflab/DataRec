# Amazon Beauty

## Overview

**Dataset name:** Amazon Beauty  
**Latest version:** 2023  
**Available versions:** 2023  
**Source:** https://amazon-reviews-2023.github.io/

A large-scale Amazon Reviews dataset, collected by McAuley Lab

---

## Citation

```bibtex
@article{DBLP:journals/corr/abs-2403-03952,
author       = {Yupeng Hou and
                Jiacheng Li and
                Zhankui He and
                An Yan and
                Xiusi Chen and
                Julian J. McAuley},
title        = {Bridging Language and Items for Retrieval and Recommendation},
journal      = {CoRR},
volume       = {abs/2403.03952},
year         = {2024}
}
```

---

## Version: 2023

### Data Sources

| Name | Source type | Archive | URL | Checksum |
|---|---|---|---|---|
| ratings | HttpSource | gz | https://mcauleylab.ucsd.edu/public_datasets/data/amazon_2023/benchmark/0core/rating_only/Beauty_and_Personal_Care.csv.gz | md5:6b9dfce7fca70dd05e1bcf77c1953c40 |

---

### Resources

#### ratings

- **Type:** interactions
- **Format:** `transactions_tabular`
- **Required:** yes
- **Source:** `ratings`
- **Filename:** `Beauty_and_Personal_Care.csv`

**Schema**

```yaml
sep: ','
user_col: user_id
item_col: parent_asin
rating_col: rating
timestamp_col: timestamp
header: 0
```

---

## Dataset Characteristics

Computed at: **2025-12-15**

| Metric | Value |
|---|---|
| n_users | 11325787 |
| n_items | 1028731 |
| n_interactions | 23591312 |
| space_size | 3413.383685772374 |
| space_size_log | 3.5331851084509505 |
| shape | 11.009473808021728 |
| shape_log | 1.0417665625926829 |
| density | 2.024798812171433e-06 |
| density_log | -5.693618122624369 |
| gini_item | 0.8549725671297695 |
| gini_user | 0.42172362782257544 |
| ratings_per_user | 2.0829733068439307 |
| ratings_per_item | 22.932440064506658 |

---

## License & Usage

Please refer to the official dataset page for licensing and usage restrictions.
https://amazon-reviews-2023.github.io/
