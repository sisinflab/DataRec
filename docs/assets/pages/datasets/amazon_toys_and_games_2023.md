# Amazon Toys and Games

## Overview

**Dataset name:** Amazon Toys and Games  
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
| ratings | HttpSource | gz | https://mcauleylab.ucsd.edu/public_datasets/data/amazon_2023/benchmark/0core/rating_only/Toys_and_Games.csv.gz | md5:542250672811854e9803d90b1f52cc14 |

---

### Resources

#### ratings

- **Type:** interactions
- **Format:** `transactions_tabular`
- **Required:** yes
- **Source:** `ratings`
- **Filename:** `Toys_and_Games.csv`

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
| n_users | 8116226 |
| n_items | 890667 |
| n_interactions | 16052440 |
| space_size | 2688.652945759642 |
| space_size_log | 3.429534746637998 |
| shape | 9.112525781240352 |
| shape_log | 0.9596387700376451 |
| density | 2.2206062715211785e-06 |
| density_log | -5.653528437968423 |
| gini_item | 0.8119593755054738 |
| gini_user | 0.4065159260942122 |
| ratings_per_user | 1.9778207260369536 |
| ratings_per_item | 18.02294235668325 |

---

## License & Usage

Please refer to the official dataset page for licensing and usage restrictions.
https://amazon-reviews-2023.github.io/
