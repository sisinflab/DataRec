# Amazon Music

## Overview

**Dataset name:** Amazon Music  
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
| ratings | HttpSource | gz | https://mcauleylab.ucsd.edu/public_datasets/data/amazon_2023/benchmark/0core/rating_only/Digital_Music.csv.gz | md5:592aaf8554ad1fec842edee82ba4d9e6 |

---

### Resources

#### ratings

- **Type:** interactions
- **Format:** `transactions_tabular`
- **Required:** yes
- **Source:** `ratings`
- **Filename:** `Digital_Music.csv`

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
| n_users | 100952 |
| n_items | 70511 |
| n_interactions | 128763 |
| space_size | 84.36958262312314 |
| space_size_log | 1.9261859006548787 |
| shape | 1.4317198734949157 |
| shape_log | 0.15585805337951963 |
| density | 1.8089196867576144e-05 |
| density_log | -4.742580714716903 |
| gini_item | 0.4038153653058994 |
| gini_user | 0.20280361886090198 |
| ratings_per_user | 1.2754873603296617 |
| ratings_per_item | 1.826140602175547 |

---

## License & Usage

Please refer to the official dataset page for licensing and usage restrictions.
https://amazon-reviews-2023.github.io/
