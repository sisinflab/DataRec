# Amazon Video Games

## Overview

**Dataset name:** Amazon Video Games  
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
| ratings | HttpSource | gz | https://mcauleylab.ucsd.edu/public_datasets/data/amazon_2023/benchmark/0core/rating_only/Video_Games.csv.gz | md5:60fdc3e812de871c30d65722e9a91a0a |

---

### Resources

#### ratings

- **Type:** interactions
- **Format:** `transactions_tabular`
- **Required:** yes
- **Source:** `ratings`
- **Filename:** `Video_Games.csv`

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
| n_users | 2766656 |
| n_items | 137249 |
| n_interactions | 4555500 |
| space_size | 616.2148727059418 |
| space_size_log | 2.789732176058451 |
| shape | 20.157931933930303 |
| shape_log | 1.304445974412738 |
| density | 1.1996973480987134e-05 |
| density_log | -4.920928301142955 |
| gini_item | 0.8571064226609856 |
| gini_user | 0.3353671504827272 |
| ratings_per_user | 1.646572613292003 |
| ratings_per_item | 33.19149866301394 |

---

## License & Usage

Please refer to the official dataset page for licensing and usage restrictions.
https://amazon-reviews-2023.github.io/
