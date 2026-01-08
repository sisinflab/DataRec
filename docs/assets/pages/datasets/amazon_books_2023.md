# Amazon Books

## Overview

**Dataset name:** Amazon Books  
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
| ratings | HttpSource | gz | https://mcauleylab.ucsd.edu/public_datasets/data/amazon_2023/benchmark/0core/rating_only/Books.csv.gz | md5:9d5d693dae385efa9053961675e1f14a |

---

### Resources

#### ratings

- **Type:** interactions
- **Format:** `transactions_tabular`
- **Required:** yes
- **Source:** `ratings`
- **Filename:** `Books.csv`

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
| n_users | 10297355 |
| n_items | 4446065 |
| n_interactions | 29139329 |
| space_size | 6766.292164699586 |
| space_size_log | 3.8303507464489135 |
| shape | 2.3160603814834015 |
| shape_log | 0.3647498775956473 |
| density | 6.364701700188797e-07 |
| density_log | -6.196221945976983 |
| gini_item | 0.7336893261122213 |
| gini_user | 0.5401752191408588 |
| ratings_per_user | 2.8297877464649903 |
| ratings_per_item | 6.55395928759476 |

---

## License & Usage

Please refer to the official dataset page for licensing and usage restrictions.
https://amazon-reviews-2023.github.io/
